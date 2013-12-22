//-------------------------------------------------------------------------------------------------------
// VST and Audio Unit Plug-Ins SDK
// Version 2.4		$Date: 2013/06/03 09:08:27 $
//
// Category     : Pyo DSP plugin
// Filename     : pyoplug.h
// Created by   : Guillaume Barrette
// Description  : Plugin that use the pyo library in python to transform or generate sounds
//
// © 2013, Guillaume Barrette, All Rights Reserved
//-------------------------------------------------------------------------------------------------------

#ifndef __pyoplug_h__
#define __pyoplug_h__
    
#include <Python/Python.h>
#include <sstream>
#include <string>
#include <dirent.h>
#include <vector>
#include <stdlib.h>     /* srand, rand */
#include <time.h>       /* time */

//#include "servermodule.h"
#include "lo/lo.h"

//#ifdef __cplusplus
//extern "C" {
//#endif

//#include <Python/Python.h>
//#include <string>
//#include <dirent.h>
//#include "lo/lo.h"

#define PYOPLUGNAME "PyoPlug"
#define PYOPLUGMANUF "Pyo"
#define PYOPLUGUNIQUEID 'gPyo'
#define PYOPLUGVERSION 1.0

#define MAX_CHANNELS 8          // Maximum number of channels the plugin can use
#define NBR_PARAMS 200+2        // +2 for the Folder and Script Parameters
#define MAX_NBR_SCRIPTS 100     // 100 to easily find the script wanted if the label is not shown: 0.01 = script 2
                                // also used for maximum number of folders

//-------------------------------------------------------------------------------------------------------

//typedef int callPtr(Server);
typedef int callPtr(int);

class PyoPlug
{
public:
    PyoPlug (float pyoSmplRate, int pyoBufSize);
	~PyoPlug ();

    char pathPresetDir[32];
    char *pathHome;
    
    float paramValues[NBR_PARAMS];
    float paramNormValues[NBR_PARAMS];  // normalized between 0 and 1
    double paramMinValue[NBR_PARAMS];
    double paramMaxValue[NBR_PARAMS];
    double paramInitValue[NBR_PARAMS];
    char paramUnitValue[NBR_PARAMS][6];
    char paramLabelValue[NBR_PARAMS][20];
    char paramRelValue[NBR_PARAMS][4];
    double paramPowerValue[NBR_PARAMS];
    char paramValueValue[NBR_PARAMS][100][10];
    int valueListCount[NBR_PARAMS];
    int valuesAreNbr[NBR_PARAMS];
    
    int folderCount;
    int folderInUse;
    int scriptCount;
    int scriptInUse;
    std::vector <std::string> folderName;
    std::vector <std::string> fileName;    
    
    void pyoSetSampleRate (float sampleRate);
    void pyoSetBufferSize (int blockSize);
    
	// Parameters
	bool pyoSetSendParameter (int index, float value);
	virtual float pyoGetParameter (int index);
	virtual const char* pyoGetParameterLabel (int index);
	virtual void pyoGetParameterDisplay (int index, char* outStr);
	virtual const char* pyoGetParameterName (int index);    
    
    void pyoFloatProcessing(float** inputs, float** outputs, int buffersize, int numChnls);
    void pyoDoubleProcessing(double** inputs, double** outputs, int buffersize, int numChnls);
    
    void pyoUpdateDAWInfo(double smplPos, double posMus, double bpm, int timeSigNum, int timeSigDenum, int isPlaying);
    
    
private:  
    
    PyThreadState *pySubInterp;
    PyThreadState *_save;
    double *pyoInputBuf;
    float *pyoInputBufFlt;
    float *pyoOutputBuf;
    
    int pyo64Imported;
    int pyoServerID;
//    int pyoOSCPort;
//    Server *pyo_Server;
    callPtr *pyoEmbed_callback;
    
    float pyoSampleRate;
    int pyoBufferSize;
    
    double pyoBPM;
    int pyoTimeSigNum;
    int pyoTimeSigDenom;
    int pyoIsPlaying;
    
    lo_address oscAddr;
//    char oscPort[5];
    char pyoScriptPreset[20];
    char serverSetParams[20];
    
    void getPyoAddresses(void);
//    void killSubInter(void);
    void getFoldersList(void);
    void getScriptList(void);
    void setOSCMessages(void);
    void getOSCParams(void);
    void initParams(void);
    void runPyoScript(void);
    void pyDelVariables(void);
    void shutdownScript(void);
    void loadScript(bool);
};

//#ifdef __cplusplus
//} // extern "C"
//#endif
    
#endif
