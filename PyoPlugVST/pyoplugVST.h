//-------------------------------------------------------------------------------------------------------
// VST Plug-Ins SDK
// Version 2.4		$Date: 2013/06/03 09:08:27 $
//
// Category     : Pyo DSP plugin
// Filename     : pyoplugVST.h
// Created by   : Guillaume Barrette
// Description  : Plugin that use the pyo library in python to transform or generate sounds
//
// © 2013, Guillaume Barrette, All Rights Reserved
//-------------------------------------------------------------------------------------------------------

#ifndef __pyoplugvst_h__
#define __pyoplugvst_h__

#include "pyoplug.h"

#include "vstsdk2.4/public.sdk/source/vst2.x/audioeffectx.h"

//-------------------------------------------------------------------------------------------------------

class PyoPlugVST : public AudioEffectX, public PyoPlug
{
public:
	PyoPlugVST (audioMasterCallback audioMaster);
	~PyoPlugVST ();

	// Processing
	virtual void processReplacing (float** inputs, float** outputs, VstInt32 sampleFrames);
	virtual void processDoubleReplacing (double** inputs, double** outputs, VstInt32 sampleFrames);

	// Program
	virtual void setProgramName (char* name);
	virtual void getProgramName (char* name);
    
    virtual void resume ();
    virtual void suspend ();
    
    virtual void setSampleRate (float sampleRate);
    virtual void setBlockSize (VstInt32 blockSize);
    
	// Parameters
	virtual void setParameter (VstInt32 index, float value);
	virtual float getParameter (VstInt32 index);
	virtual void getParameterLabel (VstInt32 index, char* label);
	virtual void getParameterDisplay (VstInt32 index, char* text);
	virtual void getParameterName (VstInt32 index, char* text);

	virtual bool getEffectName (char* name);
	virtual bool getVendorString (char* text);
	virtual bool getProductString (char* text);
	virtual VstInt32 getVendorVersion ();
    
    void updateDAWInfo(void);

protected:
	char programName[kVstMaxProgNameLen + 1];
};

#endif
