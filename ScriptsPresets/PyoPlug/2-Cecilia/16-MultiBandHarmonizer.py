"""
Multi-band harmonizer module

Sliders:

    - Overall Amplitude : The amplitude curve applied on the total duration of the performance
    - Frequency Splitter : Split points for multi-band processing
    - Transpo Band 1 : Pitch shift for the first band
    - Feedback Band 1 : Amount of harmonized signal fed back into the first band harmonizer
    - Gain Band 1 : Gain of the harmonized first band
    - Transpo Band 2 : Pitch shift for the second band
    - Feedback Band 2 : Amount of harmonized signal fed back into the second band harmonizer
    - Gain Band 2 : Gain of the harmonized second band
    - Transpo Band 3 : Pitch shift for the third band
    - Feedback Band 3 : Amount of harmonized signal fed back into the third band harmonizer
    - Gain Band 3 : Gain of the harmonized third band
    - Transpo Band 4 : Pitch shift for the fourth band
    - Feedback Band 4 : Amount of harmonized signal fed back into the fourth band harmonizer
    - Gain Band 4 : Gain of the harmonized fourth band
    - Dry / Wet : Mix between the original signal and the harmonized signals

"""

# User Interface
defineUI(id=1, name="env", label="Amplitude", unit="x", init=.8)
defineUI(id=2, name="split1", func="splitter", label="Freq1Split", min=100, max=18000, init=150, num_knobs=3, rel="log", gliss=0, up=True, unit="Hz", col="grey")
defineUI(id=3, name="split2", func="splitter", label="Freq2Split", min=100, max=18000, init=500, num_knobs=3, rel="log", gliss=0, up=True, unit="Hz", col="grey")
defineUI(id=4, name="split3", func="splitter", label="Freq3Split", min=100, max=18000, init=2000, num_knobs=3, rel="log", gliss=0, up=True, unit="Hz", col="grey")
defineUI(id=5, name="transp1", label="TranspoBand1", min=-24, max=24, init=2, rel="lin", unit="semi", col="green"),
defineUI(id=6, name="fb1", label="FeedBand1", min=0, max=0.999, init=0.6, rel="lin", unit="x", col="green"),
defineUI(id=7, name="gain1", label="GainBand1", min=-48, max=18, init=0, rel="lin", unit="dB", col="green"),
defineUI(id=8, name="transp2", label="TranspoBand2", min=-24, max=24, init=4, rel="lin", unit="semi", col="forestgreen"),
defineUI(id=9, name="fb2", label="FeedBand2", min=0, max=0.999, init=0.5, rel="lin", unit="x", col="forestgreen"),
defineUI(id=10, name="gain2", label="GainBand2", min=-48, max=18, init=0, rel="lin", unit="dB", col="forestgreen"),
defineUI(id=11, name="transp3", label="TranspoBand3", min=-24, max=24, init=-2, rel="lin", unit="semi", col="olivegreen"),
defineUI(id=12, name="fb3", label="FeedBand3", min=0, max=0.999, init=0.5, rel="lin", unit="x", col="olivegreen"),
defineUI(id=13, name="gain3", label="GainBand3", min=-48, max=18, init=0, rel="lin", unit="dB", col="olivegreen"),
defineUI(id=14, name="transp4", label="TranspoBand4", min=-24, max=24, init=-4, rel="lin", unit="semi", col="lightgreen"),
defineUI(id=15, name="fb4", label="FeedBand4", min=0, max=0.999, init=0.6, rel="lin", unit="x", col="lightgreen"),
defineUI(id=16, name="gain4", label="GainBand4", min=-48, max=18, init=0, rel="lin", unit="dB", col="lightgreen"),
defineUI(id=17, name="drywet", label="Dry / Wet", min=0, max=1, init=1, rel="lin", unit="x", col="blue"),
defineUI(id=18, name="winsize", func="winsizefunc", label="Win Size", init="0.1", col="chorusyellow", value=["0.025","0.05","0.1","0.15","0.2","0.25","0.5","0.75","1"]),


# DSP
snd = stereoIn
nchnls = len(snd)
freqs = [150,500,2000]  # for initialization

FBfade = SigTo(value=1, time=.01, init=1)
split = FourBand(input=snd, freq1=freqs[0], freq2=freqs[1], freq3=freqs[2], mul=FBfade)
transps = duplicate([transp1,transp2,transp3,transp4], len(snd))
mul1 = DBToA(gain1)
mul2 = DBToA(gain2)
mul3 = DBToA(gain3)
mul4 = DBToA(gain4)
muls = duplicate([mul1,mul2,mul3,mul4], len(snd))
fbs = duplicate([fb1, fb2, fb3, fb4], len(snd))
harm = Harmonizer(input=split, transpo=transps, feedback=fbs, winsize=0.1, mul=muls)
harms = harm.mix(nchnls)
out = Interp(snd, harms, drywet, mul=env*0.5).out(chnl=[0,1])
        
def winsizefunc():
    harm.winsize = winsize.get()    # need specify float() before ?

def splitter():
    FBfade.value = 0
    time.sleep(.02)
    split.freq1 = split1.get()
    split.freq2 = split2.get()
    split.freq3 = split3.get()
    time.sleep(.02)
    FBfade.value = 1

