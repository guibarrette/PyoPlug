"""
Multi-band delay module

Sliders:

    - Overall Amplitude : The amplitude curve applied on the total duration of the performance
    - Frequency Splitter : Split points for multi-band processing
    - Delay Band 1 : Delay time for the first band
    - Feedback Band 1 : Amount of delayed signal fed back into the first band delay
    - Gain Band 1 : Gain of the delayed first band
    - Delay Band 2 : Delay time for the second band
    - Feedback Band 2 : Amount of delayed signal fed back into the second band delay
    - Gain Band 2 : Gain of the delayed second band
    - Delay Band 3 : Delay time for the third band
    - Feedback Band 3 : Amount of delayed signal fed back into the third band delay
    - Gain Band 3 : Gain of the delayed third band
    - Delay Band 4 : Delay time for the fourth band
    - Feedback Band 4 : Amount of delayed signal fed back into the fourth band delay
    - Gain Band 4 : Gain of the delayed fourth band
    - Dry / Wet : Mix between the original signal and the delayed signals

"""

# User Interface
defineUI(id=1, name="env", label="Amplitude", unit="x", init=.8)
defineUI(id=2, name="split1", func="splitter", label="Freq1Split", min=100, max=18000, init=150, num_knobs=3, rel="log", gliss=0, up=True, unit="Hz", col="grey")
defineUI(id=3, name="split2", func="splitter", label="Freq2Split", min=100, max=18000, init=500, num_knobs=3, rel="log", gliss=0, up=True, unit="Hz", col="grey")
defineUI(id=4, name="split3", func="splitter", label="Freq3Split", min=100, max=18000, init=2000, num_knobs=3, rel="log", gliss=0, up=True, unit="Hz", col="grey")
defineUI(id=5, name="del1", label="DelBand1", min=0.0001, max=15, init=0.5, gliss=0.1, rel="log", unit="sec", half=True, col="forestgreen")
defineUI(id=6, name="del2", label="DelBand2", min=0.0001, max=15, init=0.5, gliss=0.1, rel="log", unit="sec", half=True, col="lightblue")
defineUI(id=7, name="fb1", label="FeedBand1", min=0, max=0.999, init=0.6, rel="lin", unit="x", half=True, col="forestgreen")
defineUI(id=8, name="fb2", label="FeedBand2", min=0, max=0.999, init=0.6, rel="lin", unit="x", half=True, col="lightblue")
defineUI(id=9, name="gain1", label="GainBand1", min=-48, max=18, init=0, rel="lin", unit="dB", half=True, col="forestgreen")
defineUI(id=10, name="gain2", label="GainBand2", min=-48, max=18, init=0, rel="lin", unit="dB", half=True, col="lightblue")
defineUI(id=11, name="del3", label="DelBand3", min=0.0001, max=15, init=0.5, gliss=0.1, rel="log", unit="sec", half=True, col="lightblue")
defineUI(id=12, name="del4", label="DelBand4", min=0.0001, max=15, init=0.5, gliss=0.1, rel="log", unit="sec", half=True, col="forestgreen")
defineUI(id=13, name="fb3", label="FeedBand3", min=0, max=0.999, init=0.6, rel="lin", unit="x", half=True, col="lightblue")
defineUI(id=14, name="fb4", label="FeedBand4", min=0, max=0.999, init=0.6, rel="lin", unit="x", half=True, col="forestgreen")
defineUI(id=15, name="gain3", label="GainBand3", min=-48, max=18, init=0, rel="lin", unit="dB", half=True, col="lightblue")
defineUI(id=16, name="gain4", label="GainBand4", min=-48, max=18, init=0, rel="lin", unit="dB", half=True, col="forestgreen")
defineUI(id=17, name="drywet", label="Dry / Wet", min=0, max=1, init=1, rel="lin", unit="x", col="blue")


# DSP
snd = stereoIn
nchnls = len(snd)
freqs = [150,500,2000]  # for initialization

FBfade = SigTo(value=1, time=.01, init=1)
split = FourBand(input=snd, freq1=freqs[0], freq2=freqs[1], freq3=freqs[2], mul=FBfade)
dels = duplicate([del1,del2,del3,del4], len(snd))
fbs = duplicate([fb1,fb2,fb3,fb4], len(snd))
mul1 = DBToA(gain1)
mul2 = DBToA(gain2)
mul3 = DBToA(gain3)
mul4 = DBToA(gain4)
muls = duplicate([mul1,mul2,mul3,mul4], len(snd))
delay = Delay(input=split, delay=dels, feedback=fbs, maxdelay=15, mul=muls).mix(nchnls)
out = Interp(snd, delay, drywet, mul=0.5*env).out(chnl=[0,1])

def splitter():
    FBfade.value = 0
    time.sleep(.02)
    split.freq1 = split1.get()
    split.freq2 = split2.get()
    split.freq3 = split3.get()
    time.sleep(.02)
    FBfade.value = 1

