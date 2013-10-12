"""
Multi-band delay module

Sliders under the graph:

    - Frequency Splitter : Split points for multi-band processing
    - Band 1 Drive : Amount of distortion applied on the first band
    - Band 1 Slope : Harshness of distorted first band
    - Band 1 Gain : Gain of the distorted first band
    - Band 2 Drive : Amount of distortion applied on the second band
    - Band 2 Slope : Harshness of distorted second band
    - Band 2 Gain : Gain of the distorted second band
    - Band 3 Drive : Amount of distortion applied on the third band
    - Band 3 Slope : Harshness of distorted third band
    - Band 3 Gain : Gain of the distorted third band
    - Band 4 Drive : Amount of distortion applied on the fourth band
    - Band 4 Slope : Harshness of distorted fourth band
    - Band 4 Gain : Gain of the distorted fourth band

Dropdown menus, toggles and sliders on the bottom left:

    - # of Voices : Number of voices played simultaneously (polyphony), only available at initialization time
    - Polyphony Spread : Pitch variation between voices (chorus), only available at initialization time

Graph only parameters :

    - Overall Amplitude : The amplitude curve applied on the total duration of the performance
"""
    
# User Interface
defineUI(id=1, name="env", label="Amplitude", unit="x", init=.8)
defineUI(id=2, name="split1", func="splitter", label="Freq1Split", min=100, max=18000, init=150, num_knobs=3, rel="log", gliss=0, up=True, unit="Hz", col="grey")
defineUI(id=3, name="split2", func="splitter", label="Freq2Split", min=100, max=18000, init=500, num_knobs=3, rel="log", gliss=0, up=True, unit="Hz", col="grey")
defineUI(id=4, name="split3", func="splitter", label="Freq3Split", min=100, max=18000, init=2000, num_knobs=3, rel="log", gliss=0, up=True, unit="Hz", col="grey")
defineUI(id=5, name="drive1", label="Band1Drive", min=0, max=1, init=0.75, rel="lin", unit="x", col="lightblue", half=True)
defineUI(id=6, name="drive1slope", label="Band1Slope", min=0, max=1, init=0.5, rel="lin", unit="x", col="green2", half=True)
defineUI(id=7, name="drive2", label="Band2Drive", min=0, max=1, init=0.75, rel="lin", unit="x", col="lightblue", half=True)
defineUI(id=8, name="drive2slope", label="Band2Slope", min=0, max=1, init=0.5, rel="lin", unit="x", col="green2", half=True)
defineUI(id=9, name="drive3", label="Band3Drive", min=0, max=1, init=0.75, rel="lin", unit="x", col="lightblue", half=True)
defineUI(id=10, name="drive3slope", label="Band3Slope", min=0, max=1, init=0.5, rel="lin", unit="x", col="green2", half=True)
defineUI(id=11, name="drive4", label="Band4Drive", min=0, max=1, init=0.75, rel="lin", unit="x", col="lightblue", half=True)
defineUI(id=12, name="drive4slope", label="Band4Slope", min=0, max=1, init=0.5, rel="lin", unit="x", col="green2", half=True)
defineUI(id=13, name="drive1mul", label="Band1Gain", min=-48, max=18, init=0, rel="lin", unit="dB", col="red3", half=True)
defineUI(id=14, name="drive2mul", label="Band2Gain", min=-48, max=18, init=0, rel="lin", unit="dB", col="red3", half=True)
defineUI(id=15, name="drive3mul", label="Band3Gain", min=-48, max=18, init=0, rel="lin", unit="dB", col="red3", half=True)
defineUI(id=16, name="drive4mul", label="Band4Gain", min=-48, max=18, init=0, rel="lin", unit="dB", col="red3", half=True)


# DSP
snd = stereoIn
nchnls = len(snd)
freqs = [150,500,2000]  # for initialization

FBfade = SigTo(value=1, time=.01, init=1)
split = FourBand(input=snd, freq1=freqs[0], freq2=freqs[1], freq3=freqs[2], mul=FBfade)
drives = duplicate([drive1,drive2,drive3,drive4], len(snd))
slopes = duplicate([drive1slope,drive2slope,drive3slope,drive4slope], len(snd))
mul1 = DBToA(drive1mul)
mul2 = DBToA(drive2mul)
mul3 = DBToA(drive3mul)
mul4 = DBToA(drive4mul)
muls = duplicate([mul1,mul2,mul3,mul4], len(snd))
disto = Disto(input=split, drive=drives, slope=slopes, mul=[i*0.1 for i in muls]).mix(nchnls)
out = disto*env
out.out(chnl=[0,1])

def splitter():
    FBfade.value = 0
    time.sleep(.02)
    split.freq1 = split1.get()
    split.freq2 = split2.get()
    split.freq3 = split3.get()
    time.sleep(.02)
    FBfade.value = 1

