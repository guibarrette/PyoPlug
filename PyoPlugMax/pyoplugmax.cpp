/**
    Max External
    $Date: 2013/09/22 09:01:49 $
 
    Category     : Pyo DSP plugin
    Filename     : pyoplugVST.cpp
    Created by   : Guillaume Barrette
    Description  : pyoplug~; Max external that use the pyo library in python to transform or generate sounds

    © 2013, Guillaume Barrette, All Rights Reserved
*/

#include "pyoplug.h"
    
#include "ext.h"			// standard Max include, always required (except in Jitter)
#include "ext_obex.h"		// required for "new" style objects
#include "z_dsp.h"			// required for MSP objects

#ifdef __cplusplus
extern "C" {
#endif

// struct to represent the object's state
typedef struct _pyoplugmax {
	t_pxobject		ob;			// the object itself (t_pxobject in MSP instead of t_object)
	double			offset; 	// the value of a property of our object
    
    PyoPlug         *pyoplugClass;
    float           maxSR;
    int             maxBufferSize;
} t_pyoplugmax;


// method prototypes
void *pyoplugmax_new(t_symbol *s, long argc, t_atom *argv);
void pyoplugmax_free(t_pyoplugmax *x);
void pyoplugmax_assist(t_pyoplugmax *x, void *b, long m, long a, char *s);
void pyoplugmax_float(t_pyoplugmax *x, double f);
void pyoplugmax_dsp(t_pyoplugmax *x, t_signal **sp, short *count);
void pyoplugmax_dsp64(t_pyoplugmax *x, t_object *dsp64, short *count, double samplerate, long maxvectorsize, long flags);
t_int *pyoplugmax_perform(t_int *w);
void pyoplugmax_perform64(t_pyoplugmax *x, t_object *dsp64, double **ins, long numins, double **outs, long numouts, long sampleframes, long flags, void *userparam);


// global class pointer variable
static t_class *pyoplugmax_class = NULL;

//***********************************************************************************************

int C74_EXPORT main(void)
{	
	// object initialization, note the use of dsp_free for the freemethod, which is required
	// unless you need to free allocated memory, in which case you should call dsp_free from
	// your custom free function.

	t_class *c = class_new("pyoplug~", (method)pyoplugmax_new, (method)dsp_free, (long)sizeof(t_pyoplugmax), 0L, A_GIMME, 0);
	
	class_addmethod(c, (method)pyoplugmax_float,		"float",	A_FLOAT, 0);
	class_addmethod(c, (method)pyoplugmax_dsp,          "dsp",		A_CANT, 0);		// Old 32-bit MSP dsp chain compilation for Max 5 and earlier
	class_addmethod(c, (method)pyoplugmax_dsp64,		"dsp64",	A_CANT, 0);		// New 64-bit MSP dsp chain compilation for Max 6
	class_addmethod(c, (method)pyoplugmax_assist,       "assist",	A_CANT, 0);
	
	class_dspinit(c);
	class_register(CLASS_BOX, c);
	pyoplugmax_class = c;

	return 0;
}


void *pyoplugmax_new(t_symbol *s, long argc, t_atom *argv)
{
//    PyoPlug *pyoplugClassNew = new PyoPlug(44100, 512);
    //pyoplugClass = new PyoPlug(maxSR, maxBufferSize);
//    pyoplugClassPtr = new pyoplugClass(44100, 512);
    //pyoplugClass.PyoPlug(44100, 512);
    
	t_pyoplugmax *x = (t_pyoplugmax *)object_alloc(pyoplugmax_class);

    // init param; they will be updated when the DAC is enabled
    x->maxSR = 44100;
    x->maxBufferSize = 512;
    x->pyoplugClass = new PyoPlug(x->maxSR, x->maxBufferSize);
    
	if (x) {
		dsp_setup((t_pxobject *)x, 2);	// MSP inlets: arg is # of inlets and is REQUIRED! 
										// use 0 if you don't need inlets
		
        inlet_new(x, "signal");
        inlet_new(x, "signal");
        
        outlet_new(x, "signal"); 		// signal outlet (note "signal" rather than NULL)
		outlet_new(x, "signal");
        x->offset = 0.0;
	}
	return (x);
}


// NOT CALLED!, we use dsp_free for a generic free function
void pyoplugmax_free(t_pyoplugmax *x) 
{
	;
}


//***********************************************************************************************

void pyoplugmax_assist(t_pyoplugmax *x, void *b, long m, long a, char *s)
{
	if (m == ASSIST_INLET) { //inlet
		sprintf(s, "I am inlet %ld", a);
	} 
	else {	// outlet
		sprintf(s, "I am outlet %ld", a); 			
	}
}


void pyoplugmax_float(t_pyoplugmax *x, double f)
{
	x->offset = f;
}


//***********************************************************************************************

// this function is called when the DAC is enabled, and "registers" a function for the signal chain in Max 5 and earlier.
// In this case we register the 32-bit, "pyoplugmax_perform" method.
void pyoplugmax_dsp(t_pyoplugmax *x, t_signal **sp, short *count)
{
	//post("my sample rate is: %f", sp[0]->s_sr);
	
    // Update Pyo buffer size if changed
    if(x->maxSR != (float)sp[0]->s_sr){
        x->pyoplugClass->pyoSetSampleRate((float)sp[0]->s_sr);
        x->maxSR = (float)sp[0]->s_sr;
    }
    
    // Update Pyo buffer size if changed
    if(x->maxBufferSize != (int)sp[0]->s_n){
        x->pyoplugClass->pyoSetBufferSize((int)sp[0]->s_n);
        x->maxBufferSize = (int)sp[0]->s_n;
    }
    
	// dsp_add
	// 1: (t_perfroutine p) perform method
	// 2: (long argc) number of args to your perform method
	// 3...: argc additional arguments, all must be sizeof(pointer) or long
	// these can be whatever, so you might want to include your object pointer in there
	// so that you have access to the info, if you need it.
	dsp_add(pyoplugmax_perform, 4, x, sp[0]->s_vec, sp[1]->s_vec, sp[0]->s_n);
}


// this is the Max 6 version of the dsp method -- it registers a function for the signal chain in Max 6,
// which operates on 64-bit audio signals.
void pyoplugmax_dsp64(t_pyoplugmax *x, t_object *dsp64, short *count, double samplerate, long maxvectorsize, long flags)
{
	//post("my sample rate is: %f", samplerate);
	
    // Update Pyo buffer size if changed
    if(x->maxSR != (float)samplerate){
        x->pyoplugClass->pyoSetSampleRate((float)samplerate);
        x->maxSR = (float)samplerate;
    }
    
    // Update Pyo buffer size if changed
    if(x->maxBufferSize != (int)maxvectorsize){
        x->pyoplugClass->pyoSetBufferSize((int)maxvectorsize);
        x->maxBufferSize = (int)maxvectorsize;
    }
	// instead of calling dsp_add(), we send the "dsp_add64" message to the object representing the dsp chain
	// the arguments passed are:
	// 1: the dsp64 object passed-in by the calling function
	// 2: the symbol of the "dsp_add64" message we are sending
	// 3: a pointer to your object
	// 4: a pointer to your 64-bit perform method
	// 5: flags to alter how the signal chain handles your object -- just pass 0
	// 6: a generic pointer that you can use to pass any additional data to your perform method
	
	object_method(dsp64, gensym("dsp_add64"), x, pyoplugmax_perform64, 0, NULL);
}


//***********************************************************************************************

// this is the 32-bit perform method for Max 5 and earlier
t_int *pyoplugmax_perform(t_int *w)
{
	// DO NOT CALL post IN HERE, but you can call defer_low (not defer)
	
	// args are in a vector, sized as specified in pyoplugmax_dsp method
	// w[0] contains &pyoplugmax_perform, so we start at w[1]
	t_pyoplugmax *x = (t_pyoplugmax *)(w[1]);
//	t_float *inL = (t_float *)(w[2]);
//	t_float *outL = (t_float *)(w[3]);
//	int n = (int)w[4];
	
	int sampleFrames =           (int)(w[6]);
    
    int pyoNumChnls = 2;
    
    float **inputs = new float*[MAX_CHANNELS * sizeof(float*)]; 
    for(int i=0; i < pyoNumChnls; i++){
        inputs[i] = (float*)(w[2+i]);
    }
    
    float **outputs = new float*[MAX_CHANNELS * sizeof(float*)]; 
    for(int i=0; i < pyoNumChnls; i++){
        outputs[i] = (float*)(w[4+i]);
    }        
    
    x->pyoplugClass->pyoFloatProcessing(inputs, outputs, sampleFrames, pyoNumChnls);
		
	// you have to return the NEXT pointer in the array OR MAX WILL CRASH
	return w + 5;
}


// this is 64-bit perform method for Max 6
void pyoplugmax_perform64(t_pyoplugmax *x, t_object *dsp64, double **ins, long numins, double **outs, long numouts, long sampleframes, long flags, void *userparam)
{
    x->pyoplugClass->pyoDoubleProcessing(ins, outs, (int)sampleframes, (int)numouts);
}
    
    
#ifdef __cplusplus
} // extern "C"
#endif

