"""
Table-based transposition module with multiple voices

Sliders :

    - Overall Amplitude : The amplitude curve applied on the total duration of the performance
    - Transpo Voice 1 : Play speed of the first voice
    - Gain Voice 1 : Gain of the transposed first voice
    - Transpo Voice 2 : Play speed of the second voice
    - Gain Voice 2 : Gain of the transposed second voice
    - Transpo Voice 3 : Play speed of the third voice
    - Gain Voice 3 : Gain of the transposed third voice
    - Transpo Voice 4 : Play speed of the fourth voice
    - Gain Voice 4 : Gain of the transposed fourth voice
    - Transpo Voice 5 : Play speed of the fifth voice
    - Gain Voice 5 : Gain of the transposed fifth voice

Dropdown menus, toggles and sliders on the bottom left:

    - Voice 1 : Mute or unmute the first voice
    - Voice 2 : Mute or unmute the second voice
    - Voice 3 : Mute or unmute the third voice
    - Voice 4 : Mute or unmute the fourth voice
    - Voice 5 : Mute or unmute the fifth voice
    - # of Voices : Number of voices played simultaneously (polyphony), only available at initialization time
    - Polyphony Spread : Pitch variation between voices (chorus), only available at initialization time

"""

# User Interface
defineUI(id=1, name="env", label="Amplitude", unit="x", init=.8)
defineUI(id=2, name="transpo1", label="Transpo Voice 1", min=-4800, max=4800, init=0, rel="lin", unit="cnts", col="green",half=True)
defineUI(id=3, name="gain1", label="GainVx1", min=-48, max=18, init=0, rel="lin", unit="dB", col="green",half=True)
defineUI(id=4, name="transpo2", label="Transpo Voice 2", min=-4800, max=4800, init=10, rel="lin", unit="cnts", col="blue",half=True)
defineUI(id=5, name="gain2", label="GainVx2", min=-48, max=18, init=0, rel="lin", unit="dB", col="blue",half=True)
defineUI(id=6, name="transpo3", label="Transpo Voice 3", min=-4800, max=4800, init=400, rel="lin", unit="cnts", col="orange",half=True)
defineUI(id=7, name="gain3", label="GainVx3", min=-48, max=18, init=0, rel="lin", unit="dB", col="orange",half=True)
defineUI(id=8, name="transpo4", label="Transpo Voice 4", min=-4800, max=4800, init=-300, rel="lin", unit="cnts", col="lightblue",half=True)
defineUI(id=9, name="gain4", label="GainVx4", min=-48, max=18, init=0, rel="lin", unit="dB", col="lightblue",half=True)
defineUI(id=10, name="transpo5", label="Transpo Voice 5", min=-4800, max=4800, init=-800, rel="lin", unit="cnts", col="lightgreen",half=True)
defineUI(id=11, name="gain5", label="GainVx5", min=-48, max=18, init=0, rel="lin", unit="dB", col="lightgreen",half=True)
defineUI(id=12, name="onoffv1", func="onoffv1func", label="Vx1-OnOff", init=1, min=0, max=1, value=["0","1"], stack=True, col="green")
defineUI(id=13, name="onoffv2", func="onoffv2func", label="Vx2-OnOff", init=1, min=0, max=1, value=["0","1"], stack=True, col="green")
defineUI(id=14, name="onoffv3", func="onoffv3func", label="Vx3-OnOff", init=1, min=0, max=1, value=["0","1"], stack=True, col="green")
defineUI(id=15, name="onoffv4", func="onoffv4func", label="Vx4-OnOff", init=1, min=0, max=1, value=["0","1"], stack=True, col="green")
defineUI(id=16, name="onoffv5", func="onoffv5func", label="Vx5-OnOff", init=1, min=0, max=1, value=["0","1"], stack=True, col="green")
defineUI(id=17, name="sndidx", func="sndchoice", label="SoundLoaded", file=True, init="snd_3.aif", path=os.path.join(os.path.expanduser('~'), "Library/Audio/Presets/PyoPlug/0-Sounds/"))


# DSP
# snd = stereoIn
usrPath = os.path.expanduser('~')
snd = SndTable(os.path.join(usrPath, "Library/Audio/Presets/PyoPlug/0-Sounds/snd_3.aif"))
number_of_voices = 2
polyphony_spread = .7
nchnls = 2

factor1 = CentsToTranspo(transpo1)
factor2 = CentsToTranspo(transpo2)
factor3 = CentsToTranspo(transpo3)
factor4 = CentsToTranspo(transpo4)
factor5 = CentsToTranspo(transpo5)
sndRate = Sig(snd.getRate())
phasor1 = Phasor(sndRate*factor1)
phasor2 = Phasor(sndRate*factor2)
phasor3 = Phasor(sndRate*factor3)
phasor4 = Phasor(sndRate*factor4)
phasor5 = Phasor(sndRate*factor5)
mul1 = DBToA(gain1, mul=1)
mul2 = DBToA(gain2, mul=1)
mul3 = DBToA(gain3, mul=1)
mul4 = DBToA(gain4, mul=1)
mul5 = DBToA(gain5, mul=1)
voice1 = Pointer(snd, phasor1, mul=mul1*0.2)
voice2 = Pointer(snd, phasor2, mul=mul2*0.2)
voice3 = Pointer(snd, phasor3, mul=mul3*0.2)
voice4 = Pointer(snd, phasor4, mul=mul4*0.2)
voice5 = Pointer(snd, phasor5, mul=mul5*0.2)
mixxx = voice1+voice2+voice3+voice4+voice5
# sig = mixxx*env
chorusd = Scale(input=Sig(polyphony_spread), inmin=0.0001, inmax=0.5, outmin=0, outmax=5)
chorusb = Scale(input=Sig(number_of_voices), inmin=1, inmax=10, outmin=0, outmax=1)
sig = Mix(mixxx*env, voices=nchnls)
out = Chorus(input=sig, depth=chorusd, feedback=0.25, bal=chorusb).out(chnl=[0,1])

def sndchoice():
    # global snd
    # snd = SndTable(filesList17[int(sndidx.get())])
    snd.setSound(filesList17[int(sndidx.get())])
    sndRate.setValue(snd.getRate())

def onoffv1func():
    mul1.mul = int(onoffv1.get())

def onoffv2func():
    mul2.mul = int(onoffv2.get())

def onoffv3func():
    mul3.mul = int(onoffv3.get())

def onoffv4func():
    mul4.mul = int(onoffv4.get())

def onoffv5func():
    mul5.mul = int(onoffv5.get())
            


