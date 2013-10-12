/*
*	File:		PyoPlugAU.cpp
*	
*	Version:	1.0
* 
*	Created:	13-08-13
*	
*	Copyright:  Copyright © 2013 Guillaume Barrette, All Rights Reserved
* 
*	Disclaimer:	IMPORTANT:  This Apple software is supplied to you by Apple Computer, Inc. ("Apple") in 
*				consideration of your agreement to the following terms, and your use, installation, modification 
*				or redistribution of this Apple software constitutes acceptance of these terms.  If you do 
*				not agree with these terms, please do not use, install, modify or redistribute this Apple 
*				software.
*
*				In consideration of your agreement to abide by the following terms, and subject to these terms, 
*				Apple grants you a personal, non-exclusive license, under Apple's copyrights in this 
*				original Apple software (the "Apple Software"), to use, reproduce, modify and redistribute the 
*				Apple Software, with or without modifications, in source and/or binary forms; provided that if you 
*				redistribute the Apple Software in its entirety and without modifications, you must retain this 
*				notice and the following text and disclaimers in all such redistributions of the Apple Software. 
*				Neither the name, trademarks, service marks or logos of Apple Computer, Inc. may be used to 
*				endorse or promote products derived from the Apple Software without specific prior written 
*				permission from Apple.  Except as expressly stated in this notice, no other rights or 
*				licenses, express or implied, are granted by Apple herein, including but not limited to any 
*				patent rights that may be infringed by your derivative works or by other works in which the 
*				Apple Software may be incorporated.
*
*				The Apple Software is provided by Apple on an "AS IS" basis.  APPLE MAKES NO WARRANTIES, EXPRESS OR 
*				IMPLIED, INCLUDING WITHOUT LIMITATION THE IMPLIED WARRANTIES OF NON-INFRINGEMENT, MERCHANTABILITY 
*				AND FITNESS FOR A PARTICULAR PURPOSE, REGARDING THE APPLE SOFTWARE OR ITS USE AND OPERATION ALONE 
*				OR IN COMBINATION WITH YOUR PRODUCTS.
*
*				IN NO EVENT SHALL APPLE BE LIABLE FOR ANY SPECIAL, INDIRECT, INCIDENTAL OR CONSEQUENTIAL 
*				DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS 
*				OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) ARISING IN ANY WAY OUT OF THE USE, 
*				REPRODUCTION, MODIFICATION AND/OR DISTRIBUTION OF THE APPLE SOFTWARE, HOWEVER CAUSED AND WHETHER 
*				UNDER THEORY OF CONTRACT, TORT (INCLUDING NEGLIGENCE), STRICT LIABILITY OR OTHERWISE, EVEN 
*				IF APPLE HAS BEEN ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
*
*/
/*=============================================================================
	PyoPlugAU.cpp
	
=============================================================================*/
#include "PyoPlugAU.h"


//~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

COMPONENT_ENTRY(PyoPlugAU)


//~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
//	PyoPlugAU::PyoPlugAU
//~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
PyoPlugAU::PyoPlugAU(AudioUnit component)
	: AUEffectBase(component, false), PyoPlug(44100, 512)
{
	CreateElements();

//    pyoComponent = component;
//    auNumInputs = (SInt16) GetInput(0)->GetStreamFormat().mChannelsPerFrame;
//    auNumOutputs = (SInt16) GetOutput(0)->GetStreamFormat().mChannelsPerFrame;
    
//	CAStreamBasicDescription streamDescIn;
//	streamDescIn.SetCanonical(MAX_CHANNELS, false);	// number of input channels
//	streamDescIn.mSampleRate = GetSampleRate();
//    
//	CAStreamBasicDescription streamDescOut;
//	streamDescOut.SetCanonical(MAX_CHANNELS, false);	// number of output channels
//	streamDescOut.mSampleRate = GetSampleRate();
//    
//	Inputs().GetIOElement(0)->SetStreamFormat(streamDescIn);
//	Outputs().GetIOElement(0)->SetStreamFormat(streamDescOut);
    
	Globals()->UseIndexedParameters(NBR_PARAMS);
    // default parameters value
    for(int i=0; i<NBR_PARAMS; i++){
        Globals()->SetParameter(i, 0);
    }
    
//    SetParamHasSampleRateDependency(true);
//    PropertyChanged(kAudioUnitCustomProperty_FilterFrequencyResponse, kAudioUnitScope_Global, 0 );
    
    // Initialize Sampling Rate and Buffer Size variables
//    srInUse = 44100;
    bufSizeInUse = 512;
    
//    AUChannelInfo.inChannels = -1;
//    AUChannelInfo.outChannels = -2;
//    pyoSetSampleRate((float)GetSampleRate());
//    kAudioDevicePropertyBufferFrameSize
    
//    void (*pSampleRateUpdaterFunc)(void*, AudioUnit, AudioUnitPropertyID, AudioUnitScope, AudioUnitElement) = SampleRateUpdater;
//    AudioUnitAddPropertyListener(component, kAudioUnitProperty_StreamFormat, (AudioUnitPropertyListenerProc) pSampleRateUpdaterFunc, this);
//    AudioUnitAddPropertyListener(component, kAudioUnitProperty_SampleRate, (AudioUnitPropertyListenerProc) pSampleRateUpdaterFunc, 0);
//    AudioUnitAddPropertyListener(component, kAudioUnitProperty_ParameterInfo, (AudioUnitPropertyListenerProc) SampleRateUpdater, this);
	
        
#if AU_DEBUG_DISPATCHER
	mDebugDispatcher = new AUDebugDispatcher (this);
#endif
}

//~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
//	PyoPlugAU::PyoPlugAUKernel::Initialize()
//~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
OSStatus	PyoPlugAU::Initialize()
{
    PyoPlug((float)GetSampleRate(), bufSizeInUse);  // Reinitialize Pyo; this is where the sampling rate gets updated. 
                                                    // Also, the Initialize() function is called when buffer size changes
//    UInt32 bufSize = 0;
//    UInt32 size = sizeof(UInt32);
//    AudioUnitGetProperty(pyoComponent, kAudioUnitProperty_MaximumFramesPerSlice, kAudioUnitScope_Global, 0, &bufSize, &size);
//    printf("%i\n", (int)bufSize);
//    printf("%f\n", (float)GetSampleRate());
    
    auNumInputs = (SInt16) GetInput(0)->GetStreamFormat().mChannelsPerFrame;
    auNumOutputs = (SInt16) GetOutput(0)->GetStreamFormat().mChannelsPerFrame;
//    printf("%i\n", auNumInputs);
//    printf("%i\n", auNumOutputs);
    
    // does the unit publish specific information about channel configurations?
    const AUChannelInfo *auChannelConfigs = NULL;
    UInt32 numIOconfigs = SupportedNumChannels(&auChannelConfigs);
    
    if ((numIOconfigs > 0) && (auChannelConfigs != NULL))
    {
        bool foundMatch = false;
        for (UInt32 i = 0; (i < numIOconfigs) && !foundMatch; ++i)
        {
            SInt16 configNumInputs = auChannelConfigs[i].inChannels;
            SInt16 configNumOutputs = auChannelConfigs[i].outChannels;
            if ((configNumInputs < 0) && (configNumOutputs < 0))
            {
                // unit accepts any number of channels on input and output
                if (((configNumInputs == -1) && (configNumOutputs == -2))
                    || ((configNumInputs == -2) && (configNumOutputs == -1)))
                {
                    foundMatch = true;
                }
                // unit accepts any number of channels on input and output IFF
                // they are the same number on both scopes
                else
                    if (((configNumInputs == -1) && (configNumOutputs == -1))
                        && (auNumInputs == auNumOutputs))
                    {
                        foundMatch = true;
                    }
                // unit has specified a particular number of channels on both scopes
                    else
                        continue;
            }
            else
            {
                // the -1 case on either scope is saying that the unit
                // doesn't care about the number of channels on that scope
                bool inputMatch = (auNumInputs == configNumInputs) || (configNumInputs == -1);
                bool outputMatch = (auNumOutputs == configNumOutputs) || (configNumOutputs == -1);
                if (inputMatch && outputMatch)
                    foundMatch = true;
            }
        }
        if (!foundMatch)
            return kAudioUnitErr_FormatNotSupported;
    }
    
    CAStreamBasicDescription streamDescIn;
	streamDescIn.SetCanonical(auNumInputs, false);	// number of input channels
	streamDescIn.mSampleRate = GetSampleRate();
    
	CAStreamBasicDescription streamDescOut;
	streamDescOut.SetCanonical(auNumOutputs, false);	// number of output channels
	streamDescOut.mSampleRate = GetSampleRate();
    
	Inputs().GetIOElement(0)->SetStreamFormat(streamDescIn);
	Outputs().GetIOElement(0)->SetStreamFormat(streamDescOut);
    
	return noErr;
}

/*
//~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
//	PyoPlugAU::PyoPlugAUKernel::SampleRateUpdater()
//~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
void PyoPlugAU::SampleRateUpdater(void *				inRefCon,
                                  AudioUnit             inUnit,
                                  AudioUnitPropertyID	inID,
                                  AudioUnitScope		inScope,
                                  AudioUnitElement      inElement)
{
    printf("SRchanged\n");
}
*/

//~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
//	PyoPlugAU::SupportedNumChannels
//~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
UInt32 PyoPlugAU::SupportedNumChannels (const AUChannelInfo** outInfo)
{
	// set an array of arrays of different combinations of supported numbers
	// of ins and outs
	static const AUChannelInfo sChannels[1] = {{ -1, -2}};
	if (outInfo) *outInfo = sChannels;
	return sizeof (sChannels) / sizeof (AUChannelInfo);
}


//~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
//	PyoPlugAU::GetParameterValueStrings
//~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
OSStatus PyoPlugAU::GetParameterValueStrings(AudioUnitScope         inScope,
                                             AudioUnitParameterID	inParameterID,
                                             CFArrayRef             *outStrings)
{
    return kAudioUnitErr_InvalidProperty;
}



//~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
//	PyoPlugAU::GetParameterInfo
//~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
OSStatus PyoPlugAU::GetParameterInfo(AudioUnitScope         inScope,
                                     AudioUnitParameterID	inParameterID,
                                     AudioUnitParameterInfo	&outParameterInfo )
{
	OSStatus result = noErr;

	outParameterInfo.flags = 	kAudioUnitParameterFlag_IsWritable
						|		kAudioUnitParameterFlag_IsReadable;
    CFStringRef kParameterName;
    
    auParamInfo[inParameterID] = outParameterInfo;
    
    if (inScope == kAudioUnitScope_Global) {
        /*
        kParameterName = CFStringCreateWithCString(kCFAllocatorDefault, pyoGetParameterName(inParameterID), kCFStringEncodingUTF8);
        AUBase::FillInParameterName (outParameterInfo, kParameterName, false);
        outParameterInfo.unit = kAudioUnitParameterUnit_Generic;
        outParameterInfo.minValue = (float)paramMinValue[inParameterID];
        outParameterInfo.maxValue = (float)paramMaxValue[inParameterID];
        outParameterInfo.defaultValue = (float)paramInitValue[inParameterID];
        */
        
        // if Folder or Script parameter
        if(inParameterID == 0 || inParameterID == 1){
            kParameterName = CFStringCreateWithCString(kCFAllocatorDefault, paramLabelValue[inParameterID], kCFStringEncodingUTF8);
            AUBase::FillInParameterName (outParameterInfo, kParameterName, false);
            outParameterInfo.unit = kAudioUnitParameterUnit_Generic;
            outParameterInfo.minValue = 0;
            outParameterInfo.maxValue = MAX_NBR_SCRIPTS;
            outParameterInfo.defaultValue = 0;
        }
        
        /*
        else if(inParameterID == 1){
            kParameterName = CFStringCreateWithCString(kCFAllocatorDefault, pyoGetParameterName(inParameterID), kCFStringEncodingUTF8);
            AUBase::FillInParameterName (outParameterInfo, kParameterName, false);
            outParameterInfo.unit = kAudioUnitParameterUnit_Generic;
            outParameterInfo.minValue = (float)paramMinValue[inParameterID];
            outParameterInfo.maxValue = (float)paramMaxValue[inParameterID];
            outParameterInfo.defaultValue = (float)paramInitValue[inParameterID];
        }
        else if(strcmp(paramValueValue[inParameterID][0], "none") != 0){
            // print no value to only keep the place for the parameter label
            kParameterName = CFStringCreateWithCString(kCFAllocatorDefault, pyoGetParameterName(inParameterID), kCFStringEncodingUTF8);// = pyoGetParameterName(inParameterID);
            //            CFStringCreateWithCString(kCFAllocatorDefault, pyoGetParameterName(inParameterID), kCFStringEncodingUTF8); 
            //            CFStringCreateWithCString(kParameterName, pyoGetParameterName(inParameterID));
            AUBase::FillInParameterName (outParameterInfo, kParameterName, false);
            outParameterInfo.unit = kAudioUnitParameterUnit_Generic;
            outParameterInfo.minValue = (float)paramMinValue[inParameterID];
            outParameterInfo.maxValue = (float)paramMaxValue[inParameterID];
            outParameterInfo.defaultValue = (float)paramInitValue[inParameterID];
        }
         */
        else{
//            float2string (paramValues[inParameterID], text, kVstMaxParamStrLen);
            kParameterName = CFStringCreateWithCString(kCFAllocatorDefault, paramLabelValue[inParameterID], kCFStringEncodingUTF8); // = pyoGetParameterName(inParameterID);
//            CFStringCreateWithCString(kCFAllocatorDefault, pyoGetParameterName(inParameterID), kCFStringEncodingUTF8); 
//            CFStringCreateWithCString(kParameterName, pyoGetParameterName(inParameterID));
            AUBase::FillInParameterName (outParameterInfo, kParameterName, false);
            outParameterInfo.unit = kAudioUnitParameterUnit_Generic;
            outParameterInfo.minValue = (float)paramMinValue[inParameterID];
            outParameterInfo.maxValue = (float)paramMaxValue[inParameterID];
            outParameterInfo.defaultValue = (float)paramInitValue[inParameterID];
        }
         
	} else {
        result = kAudioUnitErr_InvalidParameter;
    }
	return result;
}


//~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
//	PyoPlugAU::SetParameter
//~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
//void PyoPlugAU::SetParameter(AudioUnitParameterID			paramID,
//                             AudioUnitParameterValue		value)
//{
//    Globals()->SetParameter(paramID, value);
//    //Send parameters to Pyo
////    for(int i=0; i<NBR_PARAMS; i++){
////    GetSampleRate();
////    pyoSetSendParameter(paramID, value);
//    printf("%f\n", value);
////    }
////    AudioUnitSetParameter();
//}

OSStatus PyoPlugAU::SetParameter(AudioUnitParameterID           inID,
                                 AudioUnitScope 				inScope,
                                 AudioUnitElement 				inElement,
                                 AudioUnitParameterValue		inValue,
                                 UInt32							inBufferOffsetInFrames){
    
    float pyoValue = inValue;
    if(inID == 0 || inID == 1){
        inValue = (int)inValue;
        pyoValue = inValue/(MAX_NBR_SCRIPTS);
//        PropertyChanged(kAudioUnitProperty_ParameterInfo, kAudioUnitScope_Global, 0);
    }
    else{
        pyoValue = (inValue-paramMinValue[inID])/(paramMaxValue[inID]-paramMinValue[inID]);
    }
    
    bool scriptUpdated;
    scriptUpdated = pyoSetSendParameter(inID, pyoValue);
//    AUEventListenerNotify();
    
    // Trying to update the GUI
    if(scriptUpdated){
//        CFStringRef kParameterName;
        PropertyChanged(kAudioUnitProperty_ParameterInfo, kAudioUnitScope_Global, 0);
        for(int i=2; i<(NBR_PARAMS); i++){
//            Globals()->SetParameter(i, (paramInitValue[i]-paramMinValue[i])/(paramMaxValue[i]-paramMinValue[i]));
            Globals()->SetParameter(i, paramInitValue[i]);
//            kParameterName = CFStringCreateWithCString(kCFAllocatorDefault, paramLabelValue[i], kCFStringEncodingUTF8);
//            AUBase::FillInParameterName (auParamInfo[i], kParameterName, false);
//            GetParameterInfo(kAudioUnitScope_Global, i, auParamInfo[i]);
        }
//        AudioUnitSetProperty();
//        AudioUnitProperty newProperty;
//        newProperty.mAudioUnit = GetComponentInstance();
//        newProperty.mPropertyID = kAudioUnitProperty_ParameterInfo;
//        newProperty.mScope = kAudioUnitScope_Global;
//        newProperty.mElement = 0;
//        PropertyChanged(kAudioUnitProperty_ParameterList, kAudioUnitScope_Global, 0);
//        PropertyChanged(kAudioUnitProperty_ParameterInfo, kAudioUnitScope_Global, 0);
//        PropertyChanged(kAudioUnitProperty_ParameterList, kAudioUnitScope_Global, 0);
//        AudioUnitSetProperty(component, kAudioUnitProperty_ParameterInfo,);
//        AudioUnitSetProperty(gOutputUnit, kAudioUnitProperty_StreamFormat, kAudioUnitScope_Input, 0, &streamFormat, sizeof(streamFormat));
    }
    
#if !TARGET_OS_IPHONE
	if (inScope == kAudioUnitScope_Group) {
		return SetGroupParameter (inID, inElement, inValue, inBufferOffsetInFrames);
	}
#endif
	
	AUElement *elem = SafeGetElement(inScope, inElement);
	elem->SetParameter(inID, inValue);
	return noErr;
}

//~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
//	PyoPlugAU::GetPropertyInfo
//~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
OSStatus PyoPlugAU::GetPropertyInfo (AudioUnitPropertyID  inID,
                                     AudioUnitScope       inScope,
                                     AudioUnitElement	  inElement,
                                     UInt32               &outDataSize,
                                     Boolean              &outWritable)
{
	return AUEffectBase::GetPropertyInfo (inID, inScope, inElement, outDataSize, outWritable);
}

//~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
//	PyoPlugAU::GetProperty
//~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
OSStatus PyoPlugAU::GetProperty(AudioUnitPropertyID inID,
                                AudioUnitScope 		inScope,
                                AudioUnitElement 	inElement,
                                void                *outData )
{
	return AUEffectBase::GetProperty (inID, inScope, inElement, outData);
}


//~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
// PyoPlugAU::ProcessBufferLists
//~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
OSStatus PyoPlugAU::ProcessBufferLists	(AudioUnitRenderActionFlags&	iFlags,
                                         const AudioBufferList&         inBufferList,
                                         AudioBufferList&               outBufferList,
                                         UInt32                         iFrames)
{
//    // Update Pyo sample rate if changed
//    float srNow = (float)GetSampleRate();
//    if(srInUse != srNow){
//        pyoSetSampleRate(srNow);
//        srInUse = srNow;
//    }
    // Update Pyo buffer size if changed
    if(bufSizeInUse != iFrames){
        pyoSetBufferSize((int)iFrames);
        bufSizeInUse = iFrames;
    }
    
    UpdateDAWInfo();
    
    // Process the buffers, Pyo Callback
	// call the kernels to handle either interleaved or deinterleaved 
    // if using audio units version 1
    if(inBufferList.mNumberBuffers == 1) { 
        // process each interleaved channel individually 
        float **inputs = new float*[MAX_CHANNELS];
        for(int i=0; i < auNumInputs; i++){
//            if(i < auNumInputs){
                inputs[i] = (float*)inBufferList.mBuffers[0].mData + i;
//            }
//            else{
//                inputs[i] = 0;
//            }
        }
        
        float **outputs = new float*[MAX_CHANNELS]; 
        for(int i=0; i < auNumOutputs; i++){
//            if(i < auNumOutputs){
                outputs[i] = (float*)outBufferList.mBuffers[0].mData + i;
//            }
//            else{
//                outputs[i] = 0;
//            }
        }
        
        pyoFloatProcessing(inputs, outputs, (int)iFrames, auNumInputs);
    } 
    // if using audio units version 2
    else { 
        float **inputs = new float*[MAX_CHANNELS * sizeof(float*)]; 
        for(int i=0; i < auNumInputs; i++){
//            if(i < auNumInputs){
                inputs[i] = (float*)inBufferList.mBuffers[i].mData;
//            }
//            else{
//                inputs[i] = 0;
//            }
        }
        
        float **outputs = new float*[MAX_CHANNELS * sizeof(float*)]; 
        for(int i=0; i < auNumOutputs; i++){
//            if(i < auNumOutputs){
                outputs[i] = (float*)outBufferList.mBuffers[i].mData;
//            }
//            else{
//                outputs[i] = 0;
//            }
        }
        
        int pyoNumChnls;
        if(auNumInputs >= auNumOutputs){
            pyoNumChnls = auNumInputs;
        }
        else{
            pyoNumChnls = auNumOutputs;
        }
        
        pyoFloatProcessing(inputs, outputs, (int)iFrames, pyoNumChnls);
    }
    
    return noErr; 
}


//~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
// PyoPlugAU::updateTiming
//~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
void PyoPlugAU::UpdateDAWInfo (void)
{
    Float64 BPM;
    Float32 timeSigNum;
    UInt32 timeSigDenum;
    Float64 musPos;
    Float64 smplPos;
    Boolean isPlaying;
    
    CallHostBeatAndTempo(&musPos, &BPM);
    CallHostMusicalTimeLocation(NULL, &timeSigNum, &timeSigDenum, NULL);
    CallHostTransportState(&isPlaying, NULL, &smplPos, NULL, NULL, NULL);
    
    pyoUpdateDAWInfo(smplPos, musPos, BPM, timeSigNum, timeSigDenum, isPlaying);
}
