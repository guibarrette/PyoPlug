/*
    PureData Extension
    $Date: 2013/10/01 10:02:32 $
 
    Category     : Pyo DSP plugin
    Filename     : pyoplugPd.cpp
    Created by   : Guillaume Barrette
    Description  : pyoplug~; PureData extension that use the pyo library in python to transform or generate sounds
 
    © 2013, Guillaume Barrette, All Rights Reserved
 
    based on the simplemsp~ example
*/

#include "pyoplug.h"

#include "m_pd.h"

#ifdef __cplusplus
extern "C" {
#endif

// global class pointer variable
static t_class *pyoplug_tilde_class;

// struct to represent the object's state
typedef struct _pyoplug_tilde {
    t_object  x_obj;        // the object itself
    t_sample f_inMess;      // the value of a property of our object
    t_sample f;
    
    PyoPlug  *pyoplugClass;     // PyoPlug class pointer
    float    maxSR;             // var to keep reference to the sampling rate
    int      maxBufferSize;     // var to keep reference to the buffer size
} t_pyoplug_tilde;

// Method Prototypes
void pyoplug_tilde_setup(void);
void *pyoplug_tilde_new(t_floatarg f);
void pyoplug_tilde_dsp(t_pyoplug_tilde *x, t_signal **sp);
t_int *pyoplug_tilde_perform(t_int *w);

    
void pyoplug_tilde_setup(void) {
    pyoplug_tilde_class = class_new(gensym("pyoplug~"), (t_newmethod)pyoplug_tilde_new, 0, sizeof(t_pyoplug_tilde), CLASS_DEFAULT, A_DEFFLOAT, 0);
        
    class_addmethod(pyoplug_tilde_class, (t_method)pyoplug_tilde_dsp, gensym("dsp"), A_NULL);
    CLASS_MAINSIGNALIN(pyoplug_tilde_class, t_pyoplug_tilde, f);
}

void *pyoplug_tilde_new(t_floatarg f)
{
    t_pyoplug_tilde *x = (t_pyoplug_tilde *)pd_new(pyoplug_tilde_class);
        
    // init param; they will be updated when the DAC is enabled
    x->maxSR = 44100;
    x->maxBufferSize = 512;
    x->pyoplugClass = new PyoPlug(x->maxSR, x->maxBufferSize);
        
    //    x->f_pan = f;
        
    inlet_new(&x->x_obj, &x->x_obj.ob_pd, &s_signal, &s_signal);
    floatinlet_new (&x->x_obj, &x->f_inMess);
    outlet_new(&x->x_obj, &s_signal);
    outlet_new(&x->x_obj, &s_signal);
        
    return (void *)x;
}

// this function is called when the DAC is enabled, and "registers" a function for the signal chain in Max 5 and earlier and Pd.
// In this case we register the 32-bit, "pyoplug_tilde_perform" method.
void pyoplug_tilde_dsp(t_pyoplug_tilde *x, t_signal **sp)
{
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
        
    dsp_add(pyoplug_tilde_perform, 6, x, sp[0]->s_vec, sp[1]->s_vec, sp[2]->s_vec, sp[3]->s_vec, sp[0]->s_n);
}

    
// Process the buffers
t_int *pyoplug_tilde_perform(t_int *w)
{
    t_pyoplug_tilde *x = (t_pyoplug_tilde *)(w[1]);
    //t_sample  *in =    (t_sample *)(w[2]);
    //t_sample  *in2 =    (t_sample *)(w[3]);
    //t_sample  *out =    (t_sample *)(w[4]);
    
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
        
    return (w+7);
}


#ifdef __cplusplus
} // extern "C"
#endif
