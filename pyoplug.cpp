//-------------------------------------------------------------------------------------------------------
// Using VST 2.4 and Audio Unit Plug-Ins SDK
// $Date: 2013/06/03 09:08:27 $
//
// Category     : Pyo DSP plugin
// Filename     : pyoplug.cpp
// Created by   : Guillaume Barrette
// Description  : Plugin that use the pyo library in python to transform or generate sounds
//
// © 2013, Guillaume Barrette, All Rights Reserved
//-------------------------------------------------------------------------------------------------------

// If one day a custom GUI is developped
//#ifndef __pyoeditor__
//#include "editor/pyoeditor.h"
//#endif

#include <iostream>

#include "pyoplug.h"


// Utillity to sort files in a folder in numerical order
bool is_not_digit(char c)
{
    return !std::isdigit(c);
}

bool numeric_string_compare(const std::string& s1, const std::string& s2)
{
    // handle empty strings...
    std::string::const_iterator it1 = s1.begin(), it2 = s2.begin();
    
    if (std::isdigit(s1[0]) && std::isdigit(s2[0])) {
        int n1, n2;
        std::stringstream ss(s1);
        ss >> n1;
        ss.clear();
        ss.str(s2);
        ss >> n2;
        
        if (n1 != n2) return n1 < n2;
        
        it1 = std::find_if(s1.begin(), s1.end(), is_not_digit);
        it2 = std::find_if(s2.begin(), s2.end(), is_not_digit);
    }
    
    return std::lexicographical_compare(it1, s1.end(), it2, s2.end());
}

//-------------------------------------------------------------------------------------------------------
PyoPlug::PyoPlug (float pyoSmplRate, int pyoBufSize)	// 1 program, 1 parameter only
{
    /* Initialization parameters */
    pyoSampleRate = pyoSmplRate;
    pyoBufferSize = pyoBufSize;
    
    /* Path Variable */
    strcpy(pathPresetDir, "/Library/Audio/Presets/PyoPlug/");
    pathHome = getenv("HOME");
    
    // default parameters value
    for(int i=0; i<NBR_PARAMS; i++){
        paramValues[i] = 0;
    }
    
    if(!Py_IsInitialized())
    {        
        Py_OptimizeFlag = 2;			// Optimize the python interpreter			2 = optimize more by removing docs strings
        //Py_NoSiteFlag = 1;  			// Faster startup... use only if don't need to load site.py
        
        Py_Initialize();    			// Initialize the python interpreter
        
        PyEval_InitThreads();
        PyEval_ReleaseLock();
    }
    
    folderInUse = 0;
    scriptInUse = 0;    // init the plugin to the default script = 0
    
    PyEval_AcquireLock();               // get the GIL
	pySubInterp = Py_NewInterpreter();  // Add a new sub-interpreter
    PyRun_SimpleString("import os\n"
                       "import sys\n"
                       "import time\n"
                       "import ctypes\n"
                       "try:\n"
                       "    from pyo64 import *\n"
                       "    pyo64Imported = 1\n"
                       "except ImportError:\n"
                       "    from pyo import *\n"
                       "    pyo64Imported = 0");
    
    /* get the list of folder and script */
    getFoldersList();
    getScriptList();
    
    char pyStr[120];
    sprintf(pyStr, "pyoPlugServer = Server(sr=%f, nchnls=%i, buffersize=%i, duplex=1, audio='embedded').boot()", pyoSampleRate, MAX_CHANNELS, pyoBufferSize);
    PyRun_SimpleString(pyStr);
    PyRun_SimpleString("pyoPlugServer.start()\n"
                       "pyoPlugServer.setServer()");
    
    getPyoAddresses();
    
    char pyoOscPort[30];
    sprintf(oscPort, "%i", (10000+pyoServerID));
    sprintf(pyoOscPort, "pyoPlugOscPort = %s", oscPort);
    PyRun_SimpleString(pyoOscPort);
    oscAddr = lo_address_new("127.0.0.1", oscPort);            // OSC used inside this plugin, Host NULL = "127.0.0.1"
    
    char nbrParamsPlug[25];
    sprintf(nbrParamsPlug, "NBR_PARAMS = %i", (NBR_PARAMS));
    PyRun_SimpleString(nbrParamsPlug); 
    
    char pyoScript[200];
    sprintf(pyoScript, "pathToPyoScript = '%s%s%s/%s'", pathHome, pathPresetDir, folderName.at(folderInUse).c_str(), fileName.at(scriptInUse).c_str());
    PyRun_SimpleString(pyoScript);
    
    /* create the defineUI function to give an easy way to set the parameter's user interface */
    // *args and **kwargs are used to avoid some errors by users (ex: extra arguments not used be the plugin or badly written
    PyRun_SimpleString("def defineUI(id=1, name='paramName', func='none', arg=None, label='Param', file=False, path='none', unit=' ', min=0., max=1., init=0., rel='lin', power=0., value=['none'], *args, **kwargs):\n"
                       "    globals()[name] = Sig(value=pyoPlugParam[id])\n"
                       "    if(name != 'paramName'):\n"
                       "        if(func != 'none'):\n"
                       "            pyoPlugFuncDict[id] = [func,arg]\n"
                       "    if(label == 'Param'):\n"
                       "        label = 'Param'+str(id)\n"
                       "    if(file == True):\n"
                       "        if(path == 'none'):\n"
                       "            path = os.path.join(os.path.expanduser('~'), 'Library/Audio/Presets/PyoPlug/0-Sounds/')\n"
                       "        value = [i for i in os.listdir(path) if not i.startswith('.')]\n"
                       "        globals()['filesList'+str(id)] = list(value)\n"
                       "        max = len(value)\n"
                       "        for i in range(max): globals()['filesList'+str(id)][i] = path+value[i]\n"
                       "    if(isinstance(init, basestring)==True):\n"
                       "        try:\n"
                       "            init=value.index(init)\n"
                       "        except ValueError:\n"
                       "            init=0\n"
                       "    pyoPlugParamUI[id] = {'name':name, 'func':func, 'arg':arg, 'label':label, 'file':file, 'path':path, 'unit':unit, 'min':min, 'max':max, 'init':init, 'rel':rel, 'power':power, 'value':value}");
    
    // Set DAW variables in python
    char vstVar[15];
    sprintf(vstVar, "sr = %f", pyoSampleRate);
    PyRun_SimpleString(vstVar);
    sprintf(vstVar, "bufferSize = %i", pyoBufferSize);
    PyRun_SimpleString(vstVar);
    
    /* Duplicate function to more easily translate Cecilia scripts:
     Duplicates elements in a sequence according to the `num` parameter.
     This method is useful to creates lists that match the number of channels
     multiplied by the number of voices from a cpoly or a splitter widget.*/
    PyRun_SimpleString("def duplicate(seq, num):\n"
                       "    tmp = [x for x in seq for i in range(num)]\n"
                       "    return tmp");
    
    PyRun_SimpleString("varsDefault = dir()");  // to get the default list of variables so they don't get deleted with pyDelVariables()
    
    setOSCMessages();
    runPyoScript();
    getOSCParams();
    
	PyEval_ReleaseThread(pySubInterp);                  // Release the created thread
    PyEval_ReleaseLock(); 
}

//-------------------------------------------------------------------------------------------------------
PyoPlug::~PyoPlug ()
{
	PyEval_AcquireLock();              // get the GIL
    PyThreadState_Swap(pySubInterp);   // Swap to this plugin thread 
    //    PyRun_SimpleString("s.setServer()\n"
    //                       "s.shutdown()\n");
    //    PyRun_SimpleString("pan.stop()");
    //    PyRun_SimpleString("s.setServer()");
	Py_EndInterpreter(pySubInterp);    // Finish with this sub-interpreter
    PyEval_ReleaseLock();              // Release the GIL
    /*
     pyoPlugCount -= 1;
     if(pyoPlugCount == 0)
     {
     //PyGILState_Ensure();    // or PyEval_AcquireLock(); ?
     PyThreadState_Swap(mainThreadState);
     Py_Finalize();
     }
     */
}

//-----------------------------------------------------------------------------------------
bool PyoPlug::pyoSetSendParameter (int index, float value)
{  
    bool scriptUpdated = false;     // To find out if a new script as been loaded
    paramNormValues[index] = value;
    if(index == 0){
        paramValues[index] = value;
        
        int tempFolderNbr = (int)(value*(MAX_NBR_SCRIPTS));
        if(tempFolderNbr >= folderCount){
            tempFolderNbr = folderCount-1;
        }
        if( tempFolderNbr != folderInUse){
            folderInUse = tempFolderNbr;        // Script will be changed to the one in parameter "scriptInUse"
            
            shutdownScript();
            getScriptList();
            // to be sure not to have an out of index script
            if(scriptInUse >= scriptCount){
                scriptInUse = scriptCount-1;
            }
            loadScript(false);
            scriptUpdated = true;
        }
    }
    // if change script : Parameter 0
    else if(index == 1){
        paramValues[index] = value;
        
        int tempScriptNbr = (int)(value*(MAX_NBR_SCRIPTS));
        if(tempScriptNbr >= scriptCount){
            tempScriptNbr = scriptCount-1;
        }
        if( tempScriptNbr != scriptInUse){
            scriptInUse = tempScriptNbr;       // Script will be changed to the one in parameter "scriptInUse"
            
            shutdownScript();
            loadScript(false);
            scriptUpdated = true;
        }
    }
    // if change other parameter
    else{
        // Parameters OSC send
        double tmpValue;
        char oscPath[20];
        sprintf(oscPath, "/param%i", (index-1));
        /* Convert Value */
        if(strcmp(paramRelValue[index], "log") == 0 || strcmp(paramRelValue[index], "Log") == 0){
            if(paramPowerValue[index] == 0){
                tmpValue = log10((value*(1-0.1)+0.1)*10);   // value*(1-0.1)+0.1)*10 to keep the log between 0 and 1
            }
            else{
                tmpValue = log((value*(1-0.1)+0.1)*paramPowerValue[index])/log(paramPowerValue[index]);
            }
        }
        else if(strcmp(paramRelValue[index], "exp") == 0 || strcmp(paramRelValue[index], "Exp") == 0){
            if(paramPowerValue[index] == 0){
                tmpValue = pow(value,2);
            }
            else{
                tmpValue = pow(value, paramPowerValue[index]);
            }
        }
        else{
            tmpValue = value;
        }
        /* Send value to Pyo */
        if(strcmp(paramValueValue[index][0], "none") != 0){
            paramValues[index] = value*(valueListCount[index]);
            if(paramValues[index] == valueListCount[index]){
                paramValues[index] = valueListCount[index] - 0.00001;     // So the value doesn't get out of the range of the list
            }
            if(valuesAreNbr[index] == 1){
                // if values are only numbers, send the number represented by the index
                lo_send(oscAddr, oscPath, "f", (float)std::strtod(paramValueValue[index][(int)paramValues[index]], NULL));
            }
            else{
                // else send the index number
                lo_send(oscAddr, oscPath, "i", (int)paramValues[index]);
            }
        }
        else if(strcmp(paramUnitValue[index], "Hz") == 0 || strcmp(paramUnitValue[index], "hz") == 0){
            // if still at init value
            if (paramMaxValue[index] == 1){
                paramValues[index] = (tmpValue * pyoSampleRate * 0.5);
                lo_send(oscAddr, oscPath, "f", paramValues[index]);
            }
            // if user changed the max or min freq
            else {
                paramValues[index] = (tmpValue*(paramMaxValue[index]-paramMinValue[index]) + paramMinValue[index]);
                lo_send(oscAddr, oscPath, "f", paramValues[index]);
            }
        }
        else if(strcmp(paramUnitValue[index], "dB") == 0 || strcmp(paramUnitValue[index], "db") == 0){
            paramValues[index] = (tmpValue*(paramMaxValue[index]-paramMinValue[index]) + paramMinValue[index]);
            lo_send(oscAddr, oscPath, "f", paramValues[index]);
        }
        else{
            paramValues[index] = (tmpValue*(paramMaxValue[index]-paramMinValue[index]) + paramMinValue[index]);
            lo_send(oscAddr, oscPath, "f", paramValues[index]);
        }
    }
    return scriptUpdated;
}

//-----------------------------------------------------------------------------------------
float PyoPlug::pyoGetParameter (int index)
{
    return paramNormValues[index];
}


//-----------------------------------------------------------------------------------------
//void PyoPlug::pyoGetParameterName (VstInt32 index, char* label)
const char* PyoPlug::pyoGetParameterName (int index)
{
    return paramLabelValue[index];
}

//-----------------------------------------------------------------------------------------
//void PyoPlug::getParameterDisplay (VstInt32 index, char* text)
void PyoPlug::pyoGetParameterDisplay (int index, char* outStr)
{
    if(index == 0 || index == 1 || strcmp(paramValueValue[index][0], "none") != 0){
        strcpy(outStr, "");
        // print no value to only keep the place for the parameter label
    }
    else{
        sprintf(outStr, "%f", paramValues[index]);
    }
}

//-----------------------------------------------------------------------------------------
//void PyoPlug::getParameterLabel (VstInt32 index, char* label)
const char* PyoPlug::pyoGetParameterLabel (int index)
{
    if(index == 0){
        return(folderName.at(folderInUse).c_str());
    }
    else if(index == 1){
        return(fileName.at(scriptInUse).c_str());
    }
    else {
        if(strcmp(paramValueValue[index][0], "none") != 0){
            return(paramValueValue[index][ (int)paramValues[index] ]);
        }
        else{
            return(paramUnitValue[index]);
        }
    }
}


/*
 //-----------------------------------------------------------------------------------------
 void PyoPlug::suspend ()
 {
 }
 
 //-----------------------------------------------------------------------------------------
 void PyoPlug::resume ()
 {
 }
 */

//-----------------------------------------------------------------------------------------
void PyoPlug::pyoSetSampleRate (float sampleRate)
{
    pyoSampleRate = sampleRate;
    
    shutdownScript();
    
    char pyoSRStr[50];
    sprintf(pyoSRStr, "pyoPlugServer.setSamplingRate(%f)", pyoSampleRate);
    PyRun_SimpleString(pyoSRStr);
    
    char vstVar[15];
    sprintf(vstVar, "sr = %f", pyoSampleRate);
    PyRun_SimpleString(vstVar);
    
    loadScript(false);
}

//-----------------------------------------------------------------------------------------
void PyoPlug::pyoSetBufferSize (int blockSize) 
{ 
    pyoBufferSize = blockSize;
    
    shutdownScript();
    
    char pyoBufStr[50];
    sprintf(pyoBufStr, "pyoPlugServer.setBufferSize(%i)", pyoBufferSize);
    PyRun_SimpleString(pyoBufStr);
    
    char vstVar[15];
    sprintf(vstVar, "bufferSize = %i", pyoBufferSize);
    PyRun_SimpleString(vstVar);
    
    loadScript(true);
}


//-------------------------------------------------------------------------------------------------------
void PyoPlug::getPyoAddresses(void){
    /* Hack : Setting the input and ouput buffers to point to the memory address of pyo's server IO buffers */
    PyRun_SimpleString("inputBufAddr = pyoPlugServer.getInputAddr()\n"
                       "outputBufAddr = pyoPlugServer.getOutputAddr()\n"
                       "pyoServerAddr = pyoPlugServer.getServerAddr()\n"
                       "pyoServerID = pyoPlugServer.getServerID()\n"
                       "embeddedCallback = pyoPlugServer.getEmbedICallbackAddr()");
    
    PyObject* module = PyImport_AddModule((char*)"__main__");        // get the modules of the python application
    
    /* Setting the pointer address directly to the plugin IO */
    PyObject* obj = PyObject_GetAttrString(module, "inputBufAddr");  // get the result of the inputBufAddr python variable
    char *inputAddr = PyString_AsString(obj);                        // pass it to c++
    unsigned long long uAddr = strtoul(inputAddr,NULL,0);            // unsigned long for 32 bits memory address ; unsigned long long for 64 bits
    pyoInputBuf = reinterpret_cast<double*>(uAddr);                  // in c++ cast style	; supposed to be safer than the c cast
    pyoInputBufFlt = reinterpret_cast<float*>(uAddr);
    
    obj = PyObject_GetAttrString(module, "outputBufAddr");
    char *outputAddr = PyString_AsString(obj);
    uAddr = strtoul(outputAddr,NULL,0);
    pyoOutputBuf = reinterpret_cast<float*>(uAddr);
    
    //    obj = PyObject_GetAttrString(module, "pyoServerAddr");
    //    char *serverAddr = PyString_AsString(obj);
    //    uAddr = strtoul(serverAddr,NULL,0);
    //    pyo_Server = reinterpret_cast<Server*>(uAddr);
    
    obj = PyObject_GetAttrString(module, "pyoServerID");
    pyoServerID = PyInt_AsLong(obj);
    
    obj = PyObject_GetAttrString(module, "embeddedCallback");
    char *callbackAddr = PyString_AsString(obj);
    uAddr = strtoul(callbackAddr,NULL,0);
    pyoEmbed_callback = reinterpret_cast<callPtr*>(uAddr);
    
    obj = PyObject_GetAttrString(module, "pyo64Imported");
    pyo64Imported = PyInt_AsLong(obj);
}


//-------------------------------------------------------------------------------------------------------
void PyoPlug::killSubInter(void){
    PyEval_AcquireLock();              // get the GIL
    PyThreadState_Swap(pySubInterp);   // Swap to this plugin thread 
    //    PyRun_SimpleString("s.shutdown()");
	Py_EndInterpreter(pySubInterp);    // Finish with this sub-interpreter
    PyEval_ReleaseLock();              // Release the GIL
}


//-------------------------------------------------------------------------------------------------------
void PyoPlug::getFoldersList(void){
    // Get list of folders
    DIR *dir;
    struct dirent *ent;
    char * combinedPath = new char[std::strlen(pathHome)+std::strlen(pathPresetDir)+1];
    std::strcpy(combinedPath, pathHome);
    std::strcat(combinedPath, pathPresetDir);
    
    if ((dir = opendir (combinedPath)) != NULL) {
        /* print all the files and directories within directory */
        folderCount = 0;
        while ((ent = readdir (dir)) != NULL) {
            if (strncmp(ent->d_name, ".", sizeof(char)) == 0 || strcmp(ent->d_name, "00-Bypass") == 0 || strcmp(ent->d_name, "0-Sounds") == 0){
                continue;
            }
            else{
                folderCount++;
                folderName.push_back( std::string(ent->d_name));
            }
        }
        closedir (dir);
        std::sort(folderName.begin(), folderName.end(), numeric_string_compare);
    }
    else {
        /* could not open directory */
        printf("Could not open directory\n");
    }
}


//-------------------------------------------------------------------------------------------------------
void PyoPlug::getScriptList(void){
    // Get list of files in folder
    int len;
    const char *pyExtension;
    DIR *dir;
    struct dirent *ent;
    
    char * combinedPath = new char[std::strlen(pathHome)+std::strlen(pathPresetDir)+std::strlen(folderName.at(folderInUse).c_str())+1];
    std::strcpy(combinedPath, pathHome);
    std::strcat(combinedPath, pathPresetDir);
    std::strcat(combinedPath, folderName.at(folderInUse).c_str());
    fileName.clear();
    
    if ((dir = opendir (combinedPath)) != NULL) {
        /* print all the files and directories within directory */
        scriptCount = 0;
        while ((ent = readdir (dir)) != NULL) {
//            if (strncmp(ent->d_name, ".", sizeof(char)) == 0){
            len = strlen(ent->d_name);
            pyExtension = &ent->d_name[len-3];
            if (strcmp(pyExtension, ".py") != 0){
                continue;
            }
            else{
                scriptCount++;
                fileName.push_back( std::string(ent->d_name));
            }
        }
        closedir (dir);
        std::sort(fileName.begin(), fileName.end(), numeric_string_compare);
    }
    else {
        /* could not open directory */
        printf("Could not open directory\n");
    }
}

//-------------------------------------------------------------------------------------------------------
void PyoPlug::setOSCMessages(void){
    // shortcut to mono and stereo input
    PyRun_SimpleString("monoIn = Input(chnl=0)\n"
                       "stereoIn = Input(chnl=[0, 1])");
    
    PyRun_SimpleString("pyoPlugFuncDict = {}");     // Create the dict for the user function's call
    
    PyRun_SimpleString("paramAddrList = ['/param'+str(i) for i in range(NBR_PARAMS)]\n"
                       "paramAddrList.extend(['/smplPos', '/posMus', '/bpm', '/timeSigNum', '/timeSigDenom', '/isPlaying'])");
    
    PyRun_SimpleString("pyoPlugParam = OscReceive(port=pyoPlugOscPort, address=paramAddrList)\n"
                       "pyoPlugParam.setInterpolation(0)");        // with 0 interpolation = way less cpu used and values are more precise
    
    PyRun_SimpleString("pyoPlugParamUI = [{'name':'paramName', 'label':'Param'+str(i), 'file':False, 'path':'none', 'unit':' ', 'min':0., 'max':1., 'init':0., 'rel':'lin', 'power':0., 'value':['none']} for i in range(NBR_PARAMS)]");
    
    // Set DAW variables in python
    PyRun_SimpleString("dawSamplePos = Sig(value=pyoPlugParam['/smplPos'])\n"
                       "dawQuartetPos = Sig(value=pyoPlugParam['/posMus'])\n"
                       "dawBPM = Sig(value=pyoPlugParam['/bpm'])\n"
                       "dawTimeSigNum = Sig(value=pyoPlugParam['/timeSigNum'])\n"
                       "dawTimeSigDenom = Sig(value=pyoPlugParam['/timeSigDenom'])\n"
                       "dawIsPlaying = Sig(value=pyoPlugParam['/isPlaying'])\n");
}

//-------------------------------------------------------------------------------------------------------
void PyoPlug::getOSCParams(void){
    int i, j, k;
    PyObject *listObj, *dictObj, *obj, *objList;
    PyObject* module = PyImport_AddModule((char*)"__main__");       // get the modules of the python application
    for(i=2; i<NBR_PARAMS; i++){                                    // i = 2 to skip the Folder and Script sliders
        k = i-1;
        listObj = PyObject_GetAttrString(module, "pyoPlugParamUI");        // Get the list of dicts
        dictObj = PyList_GetItem(listObj, k);                       // Get the specified dict
        
        obj = PyDict_GetItemString(dictObj, "label");               // Get values from keys in dict
        std::strcpy(paramLabelValue[i], PyString_AsString(obj));
        obj = PyDict_GetItemString(dictObj, "unit");
        std::strcpy(paramUnitValue[i], PyString_AsString(obj));
        obj = PyDict_GetItemString(dictObj, "min");
        paramMinValue[i] = PyFloat_AsDouble(obj);
        obj = PyDict_GetItemString(dictObj, "max");
        paramMaxValue[i] = PyFloat_AsDouble(obj);
        obj = PyDict_GetItemString(dictObj, "init");
        paramInitValue[i] = PyFloat_AsDouble(obj);
        obj = PyDict_GetItemString(dictObj, "rel");
        std::strcpy(paramRelValue[i], PyString_AsString(obj));
        obj = PyDict_GetItemString(dictObj, "power");
        paramPowerValue[i] = PyFloat_AsDouble(obj);
        obj = PyDict_GetItemString(dictObj, "value");
        valueListCount[i] = PyList_Size(obj);
        for(j=0; j<valueListCount[i]; j++){
            objList = PyList_GetItem(obj, j);
            std::strcpy(paramValueValue[i][j], PyString_AsString(objList));
        }
        char * test;
        float testVal;
        valuesAreNbr[i] = 1;   // set to true initially
        for(j=0; j<valueListCount[i]; j++){
            testVal = std::strtod(paramValueValue[i][j], &test);
            if(*test){
                // if conversion failed
                valuesAreNbr[i] = 0;
                break;
            }
        }
    }
    
    std::strcpy(paramLabelValue[0], "Folder");
    paramMinValue[0] = 0;
    paramMaxValue[0] = 1;
    paramInitValue[0] = 0;
    std::strcpy(paramLabelValue[1], "Script");
    paramMinValue[1] = 0;
    paramMaxValue[1] = 1;
    paramInitValue[1] = 0;
}


//-------------------------------------------------------------------------------------------------------
void PyoPlug::initParams(void){
    int i;
    double tmpValue;
    // set parameters
    for(i=2; i<NBR_PARAMS; i++){
        /* Send value to Pyo */
        tmpValue = paramInitValue[i];
        
        if(strcmp(paramValueValue[i][0], "none") != 0){
            tmpValue = (paramInitValue[i]/valueListCount[i]);
        }
        else if(strcmp(paramUnitValue[i], "Hz") == 0 || strcmp(paramUnitValue[i], "hz") == 0){
            // if still at init value
            if (paramMaxValue[i] == 1){
                tmpValue = (paramInitValue[i] / pyoSampleRate / 0.5);
            }
            // if user changed the max freq
            else {
                tmpValue = (paramInitValue[i]-paramMinValue[i])/(paramMaxValue[i]-paramMinValue[i]);
            }
        }
        else if(strcmp(paramUnitValue[i], "dB") == 0 || strcmp(paramUnitValue[i], "db") == 0){
            // if still at init value
            if (paramMaxValue[i] == 1 && paramMinValue[i] == 0){
                paramMaxValue[i] = 6;
                paramMinValue[i] = -120;
            }
            // if user changed the max freq
            tmpValue = (paramInitValue[i]-paramMinValue[i])/(paramMaxValue[i]-paramMinValue[i]);
        }
        else{
            tmpValue = (paramInitValue[i]-paramMinValue[i])/(paramMaxValue[i]-paramMinValue[i]);
        }
        
        /* Convert Value */
        if(strcmp(paramRelValue[i], "log") == 0 || strcmp(paramRelValue[i], "Log") == 0){
            if(paramPowerValue[i] == 0){
                tmpValue = (pow(10, tmpValue)/10-0.1)/(1-0.1);  // 10 = log base ; 0.1 & 1 = minimum and maximum value to map the log between 0 and 1
            }
            else{
                tmpValue = (pow(paramPowerValue[i], tmpValue)/paramPowerValue[i]-0.1)/(1-0.1);
            }
        }
        else if(strcmp(paramRelValue[i], "exp") == 0 || strcmp(paramRelValue[i], "Exp") == 0){
            if(paramPowerValue[i] == 0){
                tmpValue = pow(tmpValue, (1./2.));
            }
            else{
                tmpValue = pow(tmpValue, (1./paramPowerValue[i]));
            }
        }
//        else{
//            tmpValue = tmpValue;
//        }
        pyoSetSendParameter(i, tmpValue);
    }
    
    // BPM
    lo_send(oscAddr, "/bpm", "f", pyoBPM);
    // Numerator Time Signature
    lo_send(oscAddr, "/timeSigNum", "i", pyoTimeSigNum);
    // Denomerator Time Signature
    lo_send(oscAddr, "/timeSigDenom", "i", pyoTimeSigDenom);
    // DAW is playing
    lo_send(oscAddr, "/isPlaying", "i", pyoIsPlaying);
}

//-------------------------------------------------------------------------------------------------------
void PyoPlug::runPyoScript(void){
    char pyoScript[200];
    sprintf(pyoScript, "pathToPyoScript = '%s%s%s/%s'", pathHome, pathPresetDir, folderName.at(folderInUse).c_str(), fileName.at(scriptInUse).c_str());
    PyRun_SimpleString(pyoScript);
    PyRun_SimpleString("try:\n"
                       "    execfile(pathToPyoScript)\n"
                       "except:\n"
                       "    errMess=Sine(200).out(dur=2)");    // Start the default preset
    
    // Set call to user functions
    PyRun_SimpleString("for key in pyoPlugFuncDict.keys():\n"
                       "    globals()['changeParam'+str(key)] = Change(pyoPlugParam[key])\n"
                       "    globals()['trigfunc'+str(key)] = TrigFunc(globals()['changeParam'+str(key)], globals()[pyoPlugFuncDict[key][0]], pyoPlugFuncDict[key][1])\n");
}

//-------------------------------------------------------------------------------------------------------
void PyoPlug::pyDelVariables(void){
    PyRun_SimpleString("varsUser = dir()\n"
                       "varsUsed = list(set(varsUser)-set(varsDefault))\n"
                       "varsUsed.remove('varsDefault')\n"
                       "varsUsed.remove('i')\n"
                       "for i in varsUsed:  delattr(sys.modules[__name__], i)\n"
                       "#time.sleep(0.1)");
}

//-----------------------------------------------------------------------------------------
void PyoPlug::shutdownScript(void) 
{     
    PyEval_AcquireLock();              // get the GIL
    PyThreadState_Swap(pySubInterp);   // Swap to this plugin thread
    PyRun_SimpleString("pyoPlugServer.setServer()\n"
                       "pyoPlugServer.shutdown()");
    
    pyDelVariables();   // delete the variables used in the script so the garbage collector free everything not in use anymore
                        // needed especially to free liblo port
}

//-----------------------------------------------------------------------------------------
void PyoPlug::loadScript(bool newBuffer) 
{     
    if(newBuffer == true){
        PyRun_SimpleString("pyoPlugServer.boot()\n"
                           "pyoPlugServer.start()");
        getPyoAddresses();
    }
    else{
        PyRun_SimpleString("pyoPlugServer.boot(newBuffer=False)\n"
                           "pyoPlugServer.start()");
    }
    
    setOSCMessages();
    runPyoScript();
    getOSCParams();
        
    PyEval_ReleaseThread(pySubInterp);  // Release the created thread
    PyEval_ReleaseLock();               // Release the GIL
    
    initParams();
}

//-------------------------------------------------------------------------------------------------------
void PyoPlug::pyoFloatProcessing(float** inputs, float** outputs, int buffersize, int numChnls){
    int i, j;
    // Send to a double or float input buffer to pyo
    if (pyo64Imported){
        /* Plugin input buffer (double) to Pyo */
        for (i=0; i<buffersize; i++) {
            for (j=0; j<numChnls; j++) {
                pyoInputBuf[(i*MAX_CHANNELS)+j] = (double)inputs[j][i];
            }
        }
    }
    else{
        /* Plugin input buffer (float) to Pyo */
        for (i=0; i<buffersize; i++) {
            for (j=0; j<numChnls; j++) {
                pyoInputBufFlt[(i*MAX_CHANNELS)+j] = (float)inputs[j][i];
            }
        }
    }
    
    /* Pyo process buffer */
    //    pyoEmbed_callback(*pyo_Server);
    pyoEmbed_callback(pyoServerID);
    
    /* Pyo output buffer to plugin */
    for (i=0; i<buffersize; i++) {
        for (j=0; j<numChnls; j++) {
            outputs[j][i] = (float)pyoOutputBuf[(i*MAX_CHANNELS)+j];
        }
    }
}

//-------------------------------------------------------------------------------------------------------
void PyoPlug::pyoDoubleProcessing(double** inputs, double** outputs, int buffersize, int numChnls){
    int i, j;
    // Send to a double or float input buffer to pyo
    if (pyo64Imported){
        /* Plugin input buffer (double) to Pyo */
        for (i=0; i<buffersize; i++) {
            for (j=0; j<numChnls; j++) {
                pyoInputBuf[(i*MAX_CHANNELS)+j] = (double)inputs[j][i];
            }
        }
    }
    else{
        /* Plugin input buffer (float) to Pyo */
        for (i=0; i<buffersize; i++) {
            for (j=0; j<numChnls; j++) {
                pyoInputBufFlt[(i*MAX_CHANNELS)+j] = (float)inputs[j][i];
            }
        }
    }
    
    /* Pyo process buffer */
    //    pyoEmbed_callback(*pyo_Server);
    pyoEmbed_callback(pyoServerID);
    
    /* Pyo output buffer to plugin */
    for (i=0; i<buffersize; i++) {
        for (j=0; j<numChnls; j++) {
            outputs[j][i] = (double)pyoOutputBuf[(i*MAX_CHANNELS)+j];
        }
    }
}





//-------------------------------------------------------------------------------------------------------
void PyoPlug::pyoUpdateDAWInfo(double smplPos, double posMus, double bpm, int timeSigNum, int timeSigDenom, int isPlaying){
    
    // System Time in nanoseconds
    lo_send(oscAddr, "/smplPos", "f", smplPos);
    // Musical Position, in Quarter Note
    lo_send(oscAddr, "/posMus", "f", posMus);
    
    // Using "if" to reduce CPU utilization by not sending every OSC message at every call, but only when the parameter has changed
    // Tempo in BPM
    if(pyoBPM != bpm){
        lo_send(oscAddr, "/bpm", "f", bpm);
        pyoBPM = bpm;
    }
    
    // Numerator Time Signature
    if(pyoTimeSigNum != timeSigNum){
        lo_send(oscAddr, "/timeSigNum", "i", timeSigNum);
        pyoTimeSigNum = timeSigNum;
    }
    
    // Denomerator Time Signature
    if(pyoTimeSigDenom != timeSigDenom){
        lo_send(oscAddr, "/timeSigDenom", "i", timeSigDenom);
        pyoTimeSigDenom = timeSigDenom;
    }
    
    // Is Playing
    if(pyoIsPlaying != isPlaying){
        lo_send(oscAddr, "/isPlaying", "i", isPlaying);
        pyoIsPlaying = isPlaying;
    }    
}
