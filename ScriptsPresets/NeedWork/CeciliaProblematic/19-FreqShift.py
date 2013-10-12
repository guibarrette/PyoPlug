"""
Frequency shifter module

Sliders:

    - Overall Amplitude : The amplitude curve applied on the total duration of the performance
    - Frequency Shift : Frequency shift value
    - Dry / Wet : Mix between the original signal and the shifted signals

"""

# User Interface
defineUI(id=1, name="env", label="Amplitude", unit="x", init=.8)
defineUI(id=2, name="shift1", label="FreqShift1", min=0, max=2000, init=500, rel="lin", unit="Hz", col="green")
defineUI(id=3, name="shift2", label="FreqShift2", min=0, max=2000, init=100, rel="lin", unit="Hz", col="green")
defineUI(id=4, name="filterf", label="FiltFreq", min=30, max=20000, init=15000, rel="log", unit="Hz", col="olivegreen",half=True)
defineUI(id=5, name="filterq", label="FilterQ", min=0.5, max=10, init=0.707, rel="log", unit="Q", col="olivegreen",half=True)
defineUI(id=6, name="delay", label="FeedDelay", min=0.001, max=1, init=.1, rel="lin", unit="sec", col="orange1")
defineUI(id=7, name="feedback", func="feedchange", label="Feedback", min=0, max=0.999, init=0.5, rel="lin", unit="x", col="orange2",half=True)
defineUI(id=8, name="gain", label="FeedGain", min=0, max=1, init=0, rel="lin", unit="x", col="orange3",half=True)
defineUI(id=9, name="drywet", label="Dry/Wet", min=0, max=1, init=1, rel="lin", unit="x", col="blue")
defineUI(id=10, name="balance", func="balancefunc", label="Balance", init= "Off", col="blue", value=["Off","Compress", "Source"])


# DSP
snd = stereoIn
biquad = Biquadx(snd, freq=filterf, q=filterq, type=0, stages=2, mul=1)
feed1 = Sig(0, add=biquad)
feed2 = Sig(0, add=biquad)
up1 = FreqShift(input=feed1, shift=shift1, mul=0.5)
up2 = FreqShift(input=feed2, shift=shift2, mul=0.5)
feeddelay1 = Delay(up1, delay=delay, feedback=feedback, mul=gain)
feeddelay2 = Delay(up1, delay=delay, feedback=feedback, mul=gain)
feed1.value = feeddelay2
feed2.value = feeddelay1
deg = Interp(snd, up1+up2, drywet, mul=env)

osc = Sine(10000,mul=.1)
balanced = Balance(deg, osc, freq=10)
out = Interp(deg, balanced).out()

#INIT
# balance(balance_index, balance_value)

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

def feedchange():
    feed1.value = feeddelay2
    feed2.value = feeddelay1
