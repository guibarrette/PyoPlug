"""
FM modified filter module

Sliders:

    - Overall Amplitude : The amplitude curve applied on the total duration of the performance
    - Filter Freq : Center frequency of the filter
    - Resonance : Q factor of the filter
    - Mod Depth : Amplitude of the LFO
    - Mod Freq : Speed of the LFO
    - Dry / Wet : Mix between the original signal and the filtered signal
    - Filter Type : Type of filter
    - Mod Type : LFO shape
    
    - # of Voices : Number of voices played simultaneously (polyphony), only available at initialization time
    - Polyphony Spread : Pitch variation between voices (chorus), only available at initialization time
"""

# User Interface
defineUI(id=1, name="env", label="Amplitude", unit="x", init=.8)
defineUI(id=2, name="centerfreq", label="FiltFreq", min=20, max=20000, init=2000, rel="log", unit="Hz", col="forestgreen")
defineUI(id=3, name="filterq", label="Resonance", min=0.5, max=10, init=0.707, rel="lin", unit="Q", col="olivegreen")
defineUI(id=4, name="moddepthAM", label="AM Depth", min=0.001, max=1, init=0.5, rel="lin", unit="x", col="tan", half=True)
defineUI(id=5, name="moddepthFM", label="FM Depth", min=0.001, max=1, init=0.85, rel="lin", unit="x", col="marineblue", half=True)
defineUI(id=6, name="modfreqAM", label="AM Freq", min=0.01, max=2000, init=1, rel="log", unit="Hz", col="tan", half=True)
defineUI(id=7, name="modfreqFM", label="FM Freq", min=0.01, max=2000, init=10, rel="log", unit="Hz", col="marineblue", half=True)
defineUI(id=8, name="drywet", label="Dry / Wet", min=0, max=1, init=1, rel="lin", unit="x")
defineUI(id=9, name="filttypeval", func="filttype", label="FiltType", init="Bandpass", col="chorusyellow", value=["Lowpass","Highpass","Bandpass","Bandstop"])
defineUI(id=10, name="modtypeFMval", func="modtypeFM", label="FM Mod Type", init="Saw Up", col="grey", value=["Saw Up", "Saw Down", "Square", "Triangle", "Pulse", "Bipolar Pulse", "Sample&Hold", "Modulated Sine"])
defineUI(id=11, name="modtypeAMval", func="modtypeAM", label="AM Mod Type", init="Triangle", col="grey", value=["Saw Up", "Saw Down", "Square", "Triangle", "Pulse", "Bipolar Pulse", "Sample and Hold", "Modulated Sine"])
defineUI(id=12, name="balance", func="balancefunc", label = "Balance", init= "Off", col="blue", value=["Off","Compress", "Source"])

# DSP
snd = stereoIn
lfomodAM = LFO(freq=modfreqAM, sharp=1, type=3, mul=0.5, add=0.5)
lfomodAMPort = Port(lfomodAM,risetime=0.001,falltime=0.001)
lfomodFM = LFO(freq=modfreqFM, sharp=1, type=0, mul=0.5, add=0.5)
filt = Biquadx(input=snd, freq=centerfreq*(lfomodFM*(moddepthFM*2)+(1-moddepthFM))+50, q=filterq, type=2, stages=2, mul=0.7 *(lfomodAMPort*moddepthAM+(1-moddepthAM)))
deg = Interp(snd, filt, drywet, mul=env)

osc = Sine(10000,mul=.1)
balanced = Balance(deg, osc, freq=10)
out = Interp(deg, balanced).out(chnl=[0,1])

#INIT
# balance(balance_index, balance_value)

def filttype():
    filt.type = int(filttypeval.get())

def modtypeFM():
    lfomodFM.type = int(modtypeFMval.get())

def modtypeAM():
    lfomodAM.type = int(modtypeAMval.get())

def balancefunc():
    index = int(balance.get())
    if index == 0:
        out.interp  = 0
    elif index == 1:
        out.interp  = 1
        balanced.input2 = osc
    elif index == 2:
        out.interp = 1
        balanced.input2 = snd            
