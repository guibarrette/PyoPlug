"""
Distortion module with pre and post filters

Sliders:

    - Overall Amplitude : The amplitude curve applied on the total duration of the performance
    - Pre Filter Freq : Center frequency of the filter applied before distortion
    - Pre Filter Q : Q factor of the filter applied before distortion
    - Drive : Amount of distortion applied on the signal
    - Post Filter Freq : Center frequency of the filter applied after distortion
    - Post Filter Q : Q factor of the filter applied after distortion
    - Pre Filter Type : Type of filter used before distortion
    - Post Filter Type : Type of filter used after distortion
    - # of Voices : Number of voices played simultaneously (polyphony), only available at initialization time
    - Polyphony Spread : Pitch variation between voices (chorus), only available at initialization time

"""

# User Interface
defineUI(id=1, name="env", label="Amplitude", unit="x", init=.8)
defineUI(id=2, name="prefiltf", label="PreFiltFreq", min=100, max=18000, init=250, unit="Hz", rel="exp")
defineUI(id=3, name="prefiltq", label="PreFiltQ", min=.5, max=10, init=0.707, rel="log")
defineUI(id=4, name="drv", label="Drive", min=0.5, max=1, init=.9, rel="lin")
defineUI(id=5, name="cut", label="PostFiltFreq", min=100, max=18000, init=5000, rel="exp")
defineUI(id=6, name="q", label="PostFiltQ", min=.5, max=10, init=0.707, rel="log")
defineUI(id=7, name="prefilttyp", func="prefilttype", label="PreFiltType", init="Highpass", value=["Lowpass","Highpass","Bandpass","Bandstop"])
# defineUI(id=7, name="prefilttype", func="true", label="PreFiltType", init=1, value=["0","1","2","3","0"])
defineUI(id=8, name="postfilttyp", func="postfilttype", label="PostFiltType", init="Lowpass", value=["Lowpass","Highpass","Bandpass","Bandstop"])
defineUI(id=9, name="balance", func="balancefunc", label = "Balance", init= "Off", col="blue", value=["Off","Compress", "Source"])

# DSP
snd = stereoIn
snd_filt = Biquadx(snd, freq=prefiltf, q=prefiltq, type=1, stages=2)
disto = Disto(snd_filt, drive=drv, slope=0, mul=.2)
deg = Biquadx(disto, freq=cut, q=q, stages=2, type=0, mul=env)

osc = Sine(10000,mul=.1)
balanced = Balance(deg, osc, freq=10)
out = Interp(deg, balanced).out(chnl=[0,1])

def prefilttype():
    snd_filt.type = int(prefilttyp.get())

def postfilttype():
    deg.type = int(postfilttyp.get())

def balancefunc():
    index = int(balance.get())
    if index == 0:
        out.interp  = 0
    elif index ==1:
       out.interp  = 1
       balanced.input2 = osc
    elif index == 2:
       out.interp = 1
       balanced.input2 = snd