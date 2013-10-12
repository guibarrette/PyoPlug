import random
"""
Multiple waveguide models module

Sliders under the graph:

    - Base Freq : Base pitch of he waveguides
    - WG Expansion : Spread between waveguides
    - WG Feedback : Length of the waveguides
    - WG Filter : Center frequency of the filter
    - Amp Deviation Amp : Amplitude of the jitter applied on the waveguides amplitude
    - Amp Deviation Speed : Frequency of the jitter applied on the waveguides amplitude
    - Freq Deviation Amp : Amplitude of the jitter applied on the waveguides pitch
    - Freq Deviation Speed : Frequency of the jitter applied on the waveguides pitch
    - Dry / Wet : Mix between the original signal and the waveguides

Dropdown menus, toggles and sliders on the bottom left:

    - Filter Type : Type of filter used
    - # of Voices : Number of voices played simultaneously (polyphony), only available at initialization time
    - Polyphony Spread : Pitch variation between voices (chorus), only available at initialization time

Graph only parameters :

    - Overall Amplitude : The amplitude curve applied on the total duration of the performance
"""


# User Interface
defineUI(id=1, name="env", label="Amplitude", unit="x", init=.8)
defineUI(id=2, name="basefreq", label="Base Freq", min=10, max=1000, init=40, rel="log", unit="Hz", col="blue"),
defineUI(id=3, name="exp", label="WG Expansion", min=0, max=4, init=0.9975, rel="lin", unit="x", col="lightblue"),
defineUI(id=4, name="fb", label="WG Feedback", min=0, max=0.999, init=0.7, rel="lin", unit="x", col="lightblue"),
defineUI(id=5, name="filter", label="Filter Cutoff", min=50, max=20000, init=20000, rel="log", unit="Hz", col="chorusyellow"),
defineUI(id=6, name="dev", label="Amp Dev Amp", min=0.001, max=1, init=0.01, rel="log", unit="x", col="green4", half = True),
defineUI(id=7, name="fdev", label="Freq Dev Amp", min=0.001, max=1, init=0.01, rel="log", unit="x", col="green2", half = True),
defineUI(id=8, name="speed", label="Amp Dev Speed", min=0.01, max=120, init=1, rel="log", unit="Hz", col="green4", half = True),
defineUI(id=9, name="fspeed", label="Freq Dev Speed", min=0.01, max=120, init=1, rel="log", unit="Hz", col="green2", half = True),
defineUI(id=10, name="drywet", label="Dry / Wet", min=0, max=1, init=1, rel="lin", unit="x", col="blue"),
defineUI(id=11, name="filttype", func="filttypefunc", label="Filter Type", init="Lowpass", col="chorusyellow", value=["Lowpass","Highpass","Bandpass","Bandstop"]),
defineUI(id=12, name="balance", func="balancefunc", label = "Balance", init= "Off", col="blue", value=["Off","Compress", "Source"])


# DSP
snd = stereoIn
chnls = len(snd)
num = 12 * chnls
ra = Randi(min=1-dev, max=1+dev, freq=speed*[random.uniform(0.85,1.15) for i in range(num)], mul=0.03)
rf = Randi(min=1-fdev, max=1+fdev, freq=fspeed*[random.uniform(0.97,1.03) for i in range(num)])
voices = [basefreq*Pow(exp, i) for i in range(num)]
frs = duplicate(voices, chnls)
wgs = Waveguide(input=snd, freq=Dummy(frs)*rf, dur=60*fb, minfreq=10, mul=ra)
wgsm = wgs.mix(chnls)
biquad = Biquadx(wgsm, freq=filter, q=1, type=0, stages=2, mul=1)
deg = Interp(snd, biquad, drywet, mul=env)

osc = Sine(10000,mul=.1)
balanced = Balance(deg, osc, freq=10)
out = Interp(deg, balanced).out(chnl=[0,1])

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

def filttypefunc():
    biquad.type = int(filttype.get())
            


