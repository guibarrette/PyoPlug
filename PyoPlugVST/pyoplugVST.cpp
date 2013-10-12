//-------------------------------------------------------------------------------------------------------
// VST Plug-Ins SDK
// Version 2.4		$Date: 2013/06/03 09:08:27 $
//
// Category     : Pyo DSP plugin
// Filename     : pyoplugVST.cpp
// Created by   : Guillaume Barrette
// Description  : Plugin that use the pyo library in python to transform or generate sounds
//
// © 2013, Guillaume Barrette, All Rights Reserved
//-------------------------------------------------------------------------------------------------------

//#ifndef __pyoeditor__
//#include "editor/pyoeditor.h"
//#endif

#include "pyoplugVST.h"

//-------------------------------------------------------------------------------------------------------
AudioEffect* createEffectInstance (audioMasterCallback audioMaster)
{
	return new PyoPlugVST (audioMaster);
}

//-------------------------------------------------------------------------------------------------------
PyoPlugVST::PyoPlugVST (audioMasterCallback audioMaster)
: AudioEffectX (audioMaster, 1, NBR_PARAMS), PyoPlug(44100, 512)	// 1 program, nbr of parameters; initialize Pyo with default parameters
{
	setNumInputs (MAX_CHANNELS);		// inputs channels
	setNumOutputs (MAX_CHANNELS);		// outputs channels
	setUniqueID (PYOPLUGUNIQUEID);      // identify
	canProcessReplacing ();             // supports replacing output
	canDoubleReplacing ();              // supports double precision processing

    vst_strncpy (programName, "Default", kVstMaxProgNameLen);	// default program name
    
    // create the editor
//    editor = new PyoEditor (this);
}

//-------------------------------------------------------------------------------------------------------
PyoPlugVST::~PyoPlugVST ()
{
}

//-------------------------------------------------------------------------------------------------------
void PyoPlugVST::setProgramName (char* name)
{
	vst_strncpy (programName, name, kVstMaxProgNameLen);
}

//-----------------------------------------------------------------------------------------
void PyoPlugVST::getProgramName (char* name)
{
	vst_strncpy (name, programName, kVstMaxProgNameLen);
}

//-----------------------------------------------------------------------------------------
void PyoPlugVST::setParameter (VstInt32 index, float value)
{  
    pyoSetSendParameter(index, value);
    if(index == 0 || index == 1){
        
    }
}

//-----------------------------------------------------------------------------------------
float PyoPlugVST::getParameter (VstInt32 index)
{
    return paramNormValues[index];
}

//-----------------------------------------------------------------------------------------
void PyoPlugVST::getParameterName (VstInt32 index, char* label)
{
    vst_strncpy (label, pyoGetParameterName(index), kVstMaxParamStrLen);
}

//-----------------------------------------------------------------------------------------
void PyoPlugVST::getParameterDisplay (VstInt32 index, char* text)
{
    if(index == 0 || index == 1 || strcmp(paramValueValue[index][0], "none") != 0){
        // print no value to only keep the place for the parameter label
    }
    else{
        float2string (paramValues[index], text, kVstMaxParamStrLen);
    }
}

//-----------------------------------------------------------------------------------------
void PyoPlugVST::getParameterLabel (VstInt32 index, char* label)
{
    vst_strncpy (label, pyoGetParameterLabel(index), kVstMaxParamStrLen);
}

//------------------------------------------------------------------------
bool PyoPlugVST::getEffectName (char* name)
{
	vst_strncpy (name, PYOPLUGNAME, kVstMaxEffectNameLen);
	return true;
}

//------------------------------------------------------------------------
bool PyoPlugVST::getProductString (char* text)
{
	vst_strncpy (text, PYOPLUGNAME, kVstMaxProductStrLen);
	return true;
}

//------------------------------------------------------------------------
bool PyoPlugVST::getVendorString (char* text)
{
    vst_strncpy (text, PYOPLUGMANUF, kVstMaxVendorStrLen);
	return true;
}

//-----------------------------------------------------------------------------------------
VstInt32 PyoPlugVST::getVendorVersion ()
{ 
	return PYOPLUGVERSION * 1000;
}



//-----------------------------------------------------------------------------------------
void PyoPlugVST::suspend ()
{
}

//-----------------------------------------------------------------------------------------
void PyoPlugVST::resume ()
{
}

//-----------------------------------------------------------------------------------------
void PyoPlugVST::setSampleRate (float sampleRate)
{
    this->sampleRate = sampleRate;
    pyoSetSampleRate(sampleRate);
}

//-----------------------------------------------------------------------------------------
void PyoPlugVST::setBlockSize (VstInt32 blockSize) 
{ 
    this->blockSize = blockSize; 
    pyoSetBufferSize(blockSize);
}


// DSP
//-----------------------------------------------------------------------------------------
void PyoPlugVST::processReplacing (float** inputs, float** outputs, VstInt32 sampleFrames)
{
    updateDAWInfo();
    pyoFloatProcessing(inputs, outputs, sampleFrames, MAX_CHANNELS);
}

//-----------------------------------------------------------------------------------------
void PyoPlugVST::processDoubleReplacing (double** inputs, double** outputs, VstInt32 sampleFrames)
{
    updateDAWInfo();
    pyoDoubleProcessing(inputs, outputs, sampleFrames, MAX_CHANNELS);
}


//-------------------------------------------------------------------------------------------------------
void PyoPlugVST::updateDAWInfo(void)
{
    
    VstTimeInfo* myTime = getTimeInfo (kVstPpqPosValid | kVstTempoValid | kVstTimeSigValid | kVstBarsValid | kVstTransportPlaying);
    
    if (myTime)
    {
        bool playing = (myTime && (myTime->flags & kVstTransportPlaying)) != false;
        pyoUpdateDAWInfo(myTime->samplePos, myTime->ppqPos, myTime->tempo, myTime->timeSigNumerator, myTime->timeSigDenominator, playing);
    }
}
