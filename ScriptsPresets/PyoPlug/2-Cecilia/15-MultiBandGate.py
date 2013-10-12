"""
Multi-band noise gate module

Sliders under the graph:

    - Frequency Splitter : Split points for multi-band processing
    - Threshold Band 1 : dB value at which the gate becomes active on the first band
    - Gain Band 1: Gain of the gated first band
    - Threshold Band 2 : dB value at which the gate becomes active on the second band
    - Gain Band 2 : Gain of the gated second band
    - Threshold Band 3 : dB value at which the gate becomes active on the third band
    - Gain Band 3 : Gain of the gated third band
    - Threshold Band 4 : dB value at which the gate becomes active on the fourth band
    - Gain Band 4 : Gain of the gated fourth band
    - Rise Time : Time taken by the gate to close
    - Fall Time : Time taken by the gate to open

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
defineUI(id=5, name="thresh1", label="ThreshBand1", min=-80, max=-0.1, init=-60, rel="lin", unit="dB", col="red")
defineUI(id=6, name="gain1", label="GainBand1", min=-48, max=18, init=0, rel="lin", unit="dB", col="red")
defineUI(id=7, name="thresh2", label="ThreshBand2", min=-80, max=-0.1, init=-60, rel="lin", unit="dB", col="chorusyellow")
defineUI(id=8, name="gain2", label="GainBand2", min=-48, max=18, init=0, rel="lin", unit="dB", col="chorusyellow")
defineUI(id=9, name="thresh3", label="ThreshBand3", min=-80, max=-0.1, init=-60, rel="lin", unit="dB", col="green")
defineUI(id=10, name="gain3", label="GainBand3", min=-48, max=18, init=0, rel="lin", unit="dB", col="green")
defineUI(id=11, name="thresh4", label="ThreshBand4", min=-80, max=-0.1, init=-60, rel="lin", unit="dB", col="orange")
defineUI(id=12, name="gain4", label="GainBand4", min=-48, max=18, init=0, rel="lin", unit="dB", col="orange")
defineUI(id=13, name="gaterise", label="Rise Time", min=0.001, max=1, init=0.01, rel="lin", unit="sec", col="blue")
defineUI(id=14, name="gatefall", label="Fall Time", min=0.001, max=1, init=0.01, rel="lin", unit="sec", col="blue")


# DSP
snd = stereoIn
nchnls = len(snd)
freqs = [150,500,2000]  # for initialization

FBfade = SigTo(value=1, time=.01, init=1)
split = FourBand(input=snd, freq1=freqs[0], freq2=freqs[1], freq3=freqs[2], mul=FBfade)
threshs = duplicate([thresh1,thresh2,thresh3,thresh4], len(snd))
mul1 = DBToA(gain1)
mul2 = DBToA(gain2)
mul3 = DBToA(gain3)
mul4 = DBToA(gain4)
muls = duplicate([mul1,mul2,mul3,mul4], len(snd))
gate = Gate(input=split, thresh=threshs, risetime=gaterise, falltime=gatefall, lookahead=5.00, outputAmp=False, mul=muls).mix(nchnls)
out = gate*env
out.out(chnl=[0,1])

def splitter():
    FBfade.value = 0
    time.sleep(.02)
    split.freq1 = split1.get()
    split.freq2 = split2.get()
    split.freq3 = split3.get()
    time.sleep(.02)
    FBfade.value = 1
