"""
Sampling rate and bit depth degradation module with optional wrap clipping

Sliders:

    - Overall Amplitude : The amplitude curve applied on the total duration of the performance
    - Bit Depth : Resolution of the amplitude in bits
    - Sampling Rate Ratio : Ratio of the new sampling rate compared to the original one
    - Wrap Threshold : Clipping limits between -1 and 1 (signal then wraps around the thresholds)
    - Filter Freq : Center frequency of the filter
    - Filter Q : Q factor of the filter
    - Dry / Wet : Mix between the original signal and the degraded signal
    - Filter Type : Type of filter
    - Clip Type : Choose between degradation only or with wrap around clipping
    
"""

# User Interface
defineUI(id=1, name='env', label='Amplitude', unit='x', min=0, max=1, init=.8)
defineUI(id=2, name='bitDepth', func="bitDepthFunc", label='BitDepth', unit='bits', min=1, max=16, init=8)
defineUI(id=3, name='srRatio', func="srRatioFunc", label='SRRatio', unit='x', min=0.01, max=1, init=0.8)
defineUI(id=4, name='clipval', func="clipfunc", label='WrapThresh', unit='x', min=0.01, max=1, init=0.8)
defineUI(id=5, name='filterf', label='FiltFreq', unit='Hz', min=30, max=20000, init=15000)
defineUI(id=6, name='filterq', label='FilterQ', unit='Q', min=0.5, max=10, init=0.707)
defineUI(id=7, name="comptypeval", func="comptype", label="PreFiltType", init="Lowpass", value=["Lowpass","Highpass","Bandpass","Bandstop"])
defineUI(id=8, name='drywet', label='DryWet', unit='x', min=0, max=1, init=1)

# DSP
snd = stereoIn
degr = Degrade(input=snd, bitdepth=8, srscale=0.8, mul=1)
wrap = Wrap(degr, -1, 1)
biquad = Biquadx(wrap, freq=filterf, q=filterq, type=0, stages=4, mul=0.7)
deg = Interp(snd, biquad, drywet, mul=env)

osc = Sine(10000,mul=.1)
balanced = Balance(deg, osc, freq=10)
out = Interp(deg, balanced).out(chnl=[0,1])

def comptype():
    deg.type = int(comptypeval.get())

def clipfunc():
    wrap.setMin(clipval.get() - 1)
    wrap.setMax(clipval.get())

def bitDepthFunc():
    degr.setBitdepth(bitDepth.get())

def srRatioFunc():
    degr.setSrscale(srRatio.get())
