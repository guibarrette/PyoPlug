"""
Multi-band frequency shifter module

Sliders:

    - Overall Amplitude : The amplitude curve applied on the total duration of the performance
    - Frequency Splitter : Split points for multi-band processing
    - Freq Shift Band 1 : Shift frequency of first band
    - Gain Band 1: Gain of the shifted first band
    - Freq Shift Band 2 : Shift frequency of second band
    - Gain Band 2 : Gain of the shifted second band
    - Freq Shift Band 3 : Shift frequency of third band
    - Gain Band 3 : Gain of the shifted third band
    - Freq Shift Band 4 : Shift frequency of fourth band
    - Gain Band 5 : Gain of the shifted fourth band
    - Dry / Wet : Mix between the original signal and the shifted signals

"""

# User Interface
defineUI(id=1, name="env", label="Amplitude", unit="x", init=.8)
defineUI(id=2, name="split1", func="splitter", label="Freq1Split", min=100, max=18000, init=150, num_knobs=3, rel="log", gliss=0, up=True, unit="Hz", col="grey")
defineUI(id=3, name="split2", func="splitter", label="Freq2Split", min=100, max=18000, init=500, num_knobs=3, rel="log", gliss=0, up=True, unit="Hz", col="grey")
defineUI(id=4, name="split3", func="splitter", label="Freq3Split", min=100, max=18000, init=2000, num_knobs=3, rel="log", gliss=0, up=True, unit="Hz", col="grey")
defineUI(id=5, name="shift1", label="FreqShiftBand1", min=0, max=2000, init=500, rel="lin", unit="Hz", col="lightgreen", half=True)
defineUI(id=6, name="gain1", label="GainBand1", min=-48, max=18, init=0, rel="lin", unit="dB", col="lightblue", half=True)
defineUI(id=7, name="shift2", label="FreqShiftBand2", min=0, max=2000, init=500, rel="lin", unit="Hz", col="lightgreen", half=True)
defineUI(id=8, name="gain2", label="GainBand2", min=-48, max=18, init=0, rel="lin", unit="dB", col="lightblue", half=True)
defineUI(id=9, name="shift3", label="FreqShiftBand3", min=0, max=2000, init=500, rel="lin", unit="Hz", col="lightgreen", half=True)
defineUI(id=10, name="gain3", label="GainBand3", min=-48, max=18, init=0, rel="lin", unit="dB", col="lightblue", half=True)
defineUI(id=11, name="shift4", label="FreqShiftBand4", min=0, max=2000, init=500, rel="lin", unit="Hz", col="lightgreen", half=True)
defineUI(id=12, name="gain4", label="GainBand4", min=-48, max=18, init=0, rel="lin", unit="dB", col="lightblue", half=True)
defineUI(id=13, name="drywet", label="Dry / Wet", min=0, max=1, init=1, rel="lin", unit="x", col="blue")


# DSP
snd = stereoIn
nchnls = len(snd)
freqs = [150,500,2000]  # for initialization

FBfade = SigTo(value=1, time=.01, init=1)
split = FourBand(input=snd, freq1=freqs[0], freq2=freqs[1], freq3=freqs[2], mul=FBfade)
shifts = duplicate([shift1,shift2,shift3,shift4], len(snd))
mul1 = DBToA(gain1)
mul2 = DBToA(gain2)
mul3 = DBToA(gain3)
mul4 = DBToA(gain4)
muls = duplicate([mul1,mul2,mul3,mul4], len(snd))
fs = Hilbert(input=split)
quad = Sine(shifts, [0, 0.25])
mod1 = fs['real'][0]*quad[0]
mod2 = fs['imag'][0]*quad[1]
mod3 = fs['real'][1]*quad[2]
mod4 = fs['imag'][1]*quad[3]
mod5 = fs['real'][2]*quad[4]
mod6 = fs['imag'][2]*quad[5]
mod7 = fs['real'][3]*quad[6]
mod8 = fs['imag'][3]*quad[7]
up1 = Sig(mod1-mod2)
up2 = Sig(mod3-mod4)
up3 = Sig(mod5-mod6)
up4 = Sig(mod7-mod8)
ups = Mix([up1, up2, up3, up4], voices=len(snd)*4)
realups = Sig(ups, mul=muls).mix(nchnls)
out = Interp(snd, realups, drywet, mul=env*0.2).out(chnl=[0,1])

def splitter():
    FBfade.value = 0
    time.sleep(.02)
    split.freq1 = split1.get()
    split.freq2 = split2.get()
    split.freq3 = split3.get()
    time.sleep(.02)
    FBfade.value = 1

