import random
"""
8 detuned resonators with jitter control

Sliders under the graph:

    - Pitch Offset : Base pitch of all the resonators
    - Amp Random Amp : Amplitude of the jitter applied on the resonators amplitude
    - Amp Random Speed : Frequency of the jitter applied on the resonators amplitude
    - Delay Random Amp : Amplitude of the jitter applied on the resonators delay (pitch)
    - Delay Random Speed : Frequency of the jitter applied on the resonators delay (pitch)
    - Detune Factor : Detune spread of the resonators
    - Pitch Voice 1 : Pitch of the first resonator
    - Pitch Voice 2 : Pitch of the second resonator
    - Pitch Voice 3 : Pitch of the third resonator
    - Pitch Voice 4 : Pitch of the fourth resonator
    - Pitch Voice 5 : Pitch of the fifth resonator
    - Pitch Voice 6 : Pitch of the sixth resonator
    - Pitch Voice 7 : Pitch of the seventh resonator
    - Pitch Voice 8 : Pitch of the eigth resonator
    - Feedback : Amount of resonators fed back in the resonators
    - Dry / Wet : Mix between the original signal and the resonators

Dropdown menus, toggles and sliders on the bottom left:

    - Voice 1 : Mute or unmute first resonator
    - Voice 2 : Mute or unmute second resonator
    - Voice 3 : Mute or unmute third resonator
    - Voice 4 : Mute or unmute fourth resonator
    - Voice 5 : Mute or unmute fifth resonator
    - Voice 6 : Mute or unmute sixth resonator
    - Voice 7 : Mute or unmute seventh resonator
    - Voice 8 : Mute or unmute eigth resonator
    - # of Voices : Number of voices played simultaneously (polyphony), only available at initialization time
    - Polyphony Spread : Pitch variation between voices (chorus), only available at initialization time

Graph only parameters :

    - Overall Amplitude : The amplitude curve applied on the total duration of the performance
"""

# User Interface
defineUI(id=1, name="env", label="Amplitude", unit="x", init=.8)
defineUI(id=2, name="offset", label="PitchOffset", min=-2400, max=2400, init=0, rel="lin", unit="cnts", col="blue")
defineUI(id=3, name="rndamp", label="AmpRandAmp", min=0, max=1, init=0, rel="lin", unit="x", col="lightblue", half=True)
defineUI(id=4, name="rnddelamp", label="DelRandAmp", min=0, max=0.25, init=0, rel="lin", unit="x", col="marineblue", half=True)
defineUI(id=5, name="rndspeed", label="AmpRandSpeed", min=0.001, max=100, init=0.25, rel="log", unit="Hz", col="lightblue", half=True)
defineUI(id=6, name="rnddelspeed", label="DelRandSpeed", min=0.001, max=100, init=6, rel="log", unit="Hz", col="marineblue", half=True)
defineUI(id=7, name="detune", label="DetuneFactor", min=0.001, max=1, init=0.5, rel="lin", unit="x", col="orange")
defineUI(id=8, name="voice1", label="PitchVoice1", min=1, max=130, init=60, rel="lin", unit="semi", half=True, col="green")
defineUI(id=9, name="voice2", label="PitchVoice2", min=1, max=130, init=72, rel="lin", unit="semi", half=True, col="green")
defineUI(id=10, name="voice3", label="PitchVoice3", min=1, max=130, init=84, rel="lin", unit="semi", half=True, col="green")
defineUI(id=11, name="voice4", label="PitchVoice4", min=1, max=130, init=96, rel="lin", unit="semi", half=True, col="green")
defineUI(id=12, name="voice5", label="PitchVoice5", min=1, max=130, init=48, rel="lin", unit="semi", half=True, col="green")
defineUI(id=13, name="voice6", label="PitchVoice6", min=1, max=130, init=67, rel="lin", unit="semi", half=True, col="green")
defineUI(id=14, name="voice7", label="PitchVoice7", min=1, max=130, init=36, rel="lin", unit="semi", half=True, col="green")
defineUI(id=15, name="voice8", label="PitchVoice8", min=1, max=130, init=87, rel="lin", unit="semi", half=True, col="green")
defineUI(id=16, name="fb", label="Feedback", min=0.01, max=0.9999, init=0.5, rel="lin", unit="x", col="red")
defineUI(id=17, name="drywet", label="Dry/Wet", min=0, max=1, init=1, rel="lin", unit="x", col="blue")
defineUI(id=18, name="onoffv1", func="onoffv1func", label="Vx1-OnOff", init="1", value=["0","1"], stack=True, col="green")
defineUI(id=19, name="onoffv2", func="onoffv2func", label="Vx2-OnOff", init="1", value=["0","1"], stack=True, col="green")
defineUI(id=20, name="onoffv3", func="onoffv3func", label="Vx3-OnOff", init="1", value=["0","1"], stack=True, col="green")
defineUI(id=21, name="onoffv4", func="onoffv4func", label="Vx4-OnOff", init="1", value=["0","1"], stack=True, col="green")
defineUI(id=22, name="onoffv5", func="onoffv5func", label="Vx5-OnOff", init="1", value=["0","1"], stack=True, col="green")
defineUI(id=23, name="onoffv6", func="onoffv6func", label="Vx6-OnOff", init="1", value=["0","1"], stack=True, col="green")
defineUI(id=24, name="onoffv7", func="onoffv7func", label="Vx7-OnOff", init="1", value=["0","1"], stack=True, col="green")
defineUI(id=25, name="onoffv8", func="onoffv8func", label="Vx8-OnOff", init="1", value=["0","1"], stack=True, col="green")


# DSP
snd = stereoIn
chnls = len(snd)
num = 8 * chnls
defamp = Sig([0.005 for i in range(num)])
ra = Randi(min=1-rndamp, max=1+rndamp, freq=rndspeed*[random.uniform(.95,1.05) for i in range(num)])
rf = Randi(min=1-rnddelamp, max=1+rnddelamp, freq=rnddelspeed*[random.uniform(.95,1.05) for i in range(num)])
off_transpo = CentsToTranspo(offset)
frs = duplicate([voice1, voice2, voice3, voice4, voice5, voice6, voice7, voice8], chnls)
freqs = MToF(frs, mul=off_transpo)
all_freqs = freqs*rf
snd2 = Sig(value=snd, mul=0.25)
wgs = AllpassWG(input=snd2, freq=all_freqs, feed=fb, detune=detune, minfreq=1, mul=ra*defamp)
out = Interp(snd, wgs.mix(chnls), drywet, mul=env).out(chnl=[0,1])

#INIT
# onoffv1(onoffv1_value)
# onoffv2(onoffv2_value)
# onoffv3(onoffv3_value)
# onoffv4(onoffv4_value)
# onoffv5(onoffv5_value)
# onoffv6(onoffv6_value)
# onoffv7(onoffv7_value)
# onoffv8(onoffv8_value)

def onoff(i, value):
    l = defamp.value
    l[i*2:i*2+2] = [value, value]
    defamp.value = l

def onoffv1func():
    onoff(0, int(onoffv1.get()))

def onoffv2func():
    onoff(1, int(onoffv2.get()))

def onoffv3func():
    onoff(2, int(onoffv3.get()))

def onoffv4func():
    onoff(3, int(onoffv4.get()))

def onoffv5func():
    onoff(4, int(onoffv5.get()))

def onoffv6func():
    onoff(5, int(onoffv6.get()))

def onoffv7func():
    onoff(6, int(onoffv7.get()))

def onoffv8func():
    onoff(7, int(onoffv8.get()))