//-------------------------------------------------------------------------------------------------------
// VST Plug-Ins SDK
// Version 2.4		$Date: 2006/11/13 09:08:28 $
//
// Category     : VST 2.x SDK Samples
// Filename     : pyoeditor.h
// Created by   : Steinberg Media Technologies
// Description  : Simple Surround Delay plugin with Editor using VSTGUI
//
// � 2006, Steinberg Media Technologies, All Rights Reserved
//-------------------------------------------------------------------------------------------------------

#ifndef __pyoeditor__
#define __pyoeditor__

#define VSTGUI_ENABLE_DEPRECATED_METHODS 1
#define VST_FORCE_DEPRECATED 1

// include VSTGUI
#ifndef __vstgui__
#include "vstgui.sf/vstgui/vstgui.h"
#endif



//-----------------------------------------------------------------------------
class PyoEditor : public AEffGUIEditor, public CControlListener
{
public:
	PyoEditor (AudioEffect* effect);
	virtual ~PyoEditor ();

public:
	virtual bool open (void* ptr);
	virtual void close ();

	virtual void setParameter (VstInt32 index, float value);
	virtual void valueChanged (CDrawContext* context, CControl* control);

private:
	// Controls
	CVerticalSlider* delayFader;
	CVerticalSlider* feedbackFader;
	CVerticalSlider* volumeFader;

	CParamDisplay* delayDisplay;
	CParamDisplay* feedbackDisplay;
	CParamDisplay* volumeDisplay;

	// Bitmap
	CBitmap* hBackground;
};

#endif
