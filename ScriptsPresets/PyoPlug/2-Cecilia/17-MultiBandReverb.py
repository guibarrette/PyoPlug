"""
Multi-band reverb module

Sliders under the graph:

    - Frequency Splitter : Split points for multi-band processing
    - Reverb Band 1 : Amount of reverb applied on first band
    - Cutoff Band 1 : Cutoff frequency of the reverb's lowpass filter (damp) for the first band
    - Gain Band 1 : Gain of the reverberized first band
    - Reverb Band 2 : Amount of reverb applied on second band
    - Cutoff Band 2 : Cutoff frequency of the reverb's lowpass filter (damp) for the second band
    - Gain Band 2 : Gain of the reverberized second band
    - Reverb Band 3 : Amount of reverb applied on third band
    - Cutoff Band 3 : Cutoff frequency of the reverb's lowpass filter (damp) for the third band
    - Gain Band 3 : Gain of the reverberized third band
    - Reverb Band 4 : Amount of reverb applied on fourth band
    - Cutoff Band 4 : Cutoff frequency of the reverb's lowpass filter (damp) for the fourth band
    - Gain Band 4 : Gain of the reverberized fourth band
    - Dry / Wet : Mix between the original signal and the harmonized signals

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
defineUI(id=5, name="fb1", label="ReverbBand1", min=0, max=0.999, init=0.5, rel="lin", unit="x", col="chorusyellow")
defineUI(id=6, name="cutoff1", label="CutOffBand1", min=20, max=20000, init=5000, rel="log", unit="Hz", col="chorusyellow")
defineUI(id=7, name="gain1", label="GainBand1", min=-48, max=18, init=0, rel="lin", unit="dB", col="chorusyellow")
defineUI(id=8, name="fb2", label="ReverbBand2", min=0, max=0.999, init=0.5, rel="lin", unit="x", col="green")
defineUI(id=9, name="cutoff2", label="CutOffBand2", min=20, max=20000, init=5000, rel="log", unit="Hz", col="green")
defineUI(id=10, name="gain2", label="GainBand2", min=-48, max=18, init=0, rel="lin", unit="dB", col="green")
defineUI(id=11, name="fb3", label="ReverbBand3", min=0, max=0.999, init=0.5, rel="lin", unit="x", col="orange")
defineUI(id=12, name="cutoff3", label="CutOffBand3", min=20, max=20000, init=5000, rel="log", unit="Hz", col="orange")
defineUI(id=13, name="gain3", label="GainBand3", min=-48, max=18, init=0, rel="lin", unit="dB", col="orange")
defineUI(id=14, name="fb4", label="ReverbBand4", min=0, max=0.999, init=0.5, rel="lin", unit="x", col="tan")
defineUI(id=15, name="cutoff4", label="CutOffBand4", min=20, max=20000, init=5000, rel="log", unit="Hz", col="tan")
defineUI(id=16, name="gain4", label="GainBand4", min=-48, max=18, init=0, rel="lin", unit="dB", col="tan")
defineUI(id=17, name="drywet", label="Dry/Wet", min=0, max=1, init=0.8, rel="lin", unit="x", col="blue")


# DSP
snd = stereoIn
nchnls = len(snd)
freqs = [150,500,2000]  # for initialization

FBfade = SigTo(value=1, time=.01, init=1)
split = FourBand(input=snd, freq1=freqs[0], freq2=freqs[1], freq3=freqs[2], mul=FBfade)
fbs = duplicate([fb1,fb2,fb3,fb4], len(snd))
cutoffs = duplicate([cutoff1,cutoff2,cutoff3,cutoff4], len(snd))
mul1 = DBToA(gain1)
mul2 = DBToA(gain2)
mul3 = DBToA(gain3)
mul4 = DBToA(gain4)
muls = duplicate([mul1,mul2,mul3,mul4], len(snd))
verb = WGVerb(input=split, feedback=fbs, cutoff=cutoffs, bal=drywet, mul=muls).mix(nchnls)
out = verb*env
out.out(chnl=[0,1])

def splitter():
    FBfade.value = 0
    time.sleep(.02)
    split.freq1 = split1.get()
    split.freq2 = split2.get()
    split.freq3 = split3.get()
    time.sleep(.02)
    FBfade.value = 1
