import random
"""
Looper module with optional amplitude and frequency modulation

Sliders under the graph:

    - AM Range : Amplitude of the AM LFO
    - AM Speed : Frequency of the AM LFO
    - FM Range : Amplitude of the FM LFO
    - FM Speed : Frequency of the FM LFO
    - Index Range : Range of the soundfile to loop
    - Dry / Wet : Mix between the original signal and the processed signal

Dropdown menus, toggles and sliders on the bottom left:

    - AM LFO Type : Shape of the AM wave
    - AM On/Off : Activate or deactivate amplitude modulation
    - FM LFO Type : Shape of the FM wave
    - FM On/Off : Activate or deactivate frequency modulation
    - # of Voices : Number of voices played simultaneously (polyphony), only available at initialization time
    - Polyphony Spread : Pitch variation between voices (chorus), only available at initialization time

Graph only parameters :

    - Overall Amplitude : The amplitude curve applied on the total duration of the performance
"""


# User Interface
defineUI(id=1, name="env", label="Amplitude", unit="x", init=.8)
defineUI(id=2, name="ammin", label="AMmin", min=0.001, max=1, init=0.3, rel="lin", unit="x", col="green")
defineUI(id=3, name="ammax", label="AMmax", min=0.001, max=1, init=0.5, rel="lin", unit="x", col="green")
defineUI(id=4, name="amspeed", label="AMSpeed", min=0.001, max=2000, init=4, rel="log", unit="Hz", col="green")
defineUI(id=5, name="fmmin", label="FMmin", min=0.001, max=0.2, init=0.01, rel="lin", unit="x", col="orange")
defineUI(id=6, name="fmmax", label="FMmax", min=0.001, max=0.2, init=0.05, rel="lin", unit="x", col="orange")
defineUI(id=7, name="fmspeed", label="FMSpeed", min=0.001, max=2000, init=4, rel="log", unit="Hz", col="orange")
defineUI(id=8, name="indexMin", label="LoopMin", min=0, max=1, init=0, rel="lin", unit="x", col="tan")
defineUI(id=9, name="indexMax", label="LoopMax", min=0, max=1, init=1, rel="lin", unit="x", col="tan")
defineUI(id=10, name="drywet", label="Dry/Wet", min=0, max=1, init=1, rel="lin", unit="x", col="grey")
defineUI(id=11, name="ampwave", func="ampwavefunc", label="AM LFO Type", init="Square", col="green", value=["Saw Up", "Saw Down", "Square", "Triangle", "Pulse", "Bipolar Pulse", "Sample and Hold", "Modulated Sine"])
defineUI(id=12, name="onoffam", func="onoffamfunc", label="AM On/Off", init=0, min=0, max=1, value=["0","1"], col="green")
defineUI(id=13, name="freqwave", func="freqwavefunc", label="FM LFO Type", init="Square", col="orange", value=["Saw Up", "Saw Down", "Square", "Triangle", "Pulse", "Bipolar Pulse", "Sample and Hold", "Modulated Sine"])
defineUI(id=14, name="onofffm", func="onofffmfunc", label="FM On/Off", init=0, min=0, max=1, value=["0","1"], col="orange")
defineUI(id=15, name="sndidx", func="sndchoice", label="SoundLoaded", file=True, init="ounkmaster.aif", path=os.path.join(os.path.expanduser('~'), "Library/Audio/Presets/PyoPlug/0-Sounds/"))


# DSP
usrPath = os.path.expanduser('~')
snd = SndTable(os.path.join(usrPath, "Library/Audio/Presets/PyoPlug/0-Sounds/ounkmaster.aif"))
number_of_voices = 2
polyphony_spread = .7

lfoam = LFO(freq=amspeed, sharp=1, type=2, mul=0.37, add=0.6)
lfoamrange = Randi(min=ammin, max=ammax, freq=amspeed, mul=lfoam)
lfofm = LFO(freq=fmspeed, sharp=1, type=2, mul=0.05, add=1)
sig1 = Sig(fmmin)
sig2 = Sig(fmmax)
lfofmrange = Randi(min=1-sig1, max=1+sig2, freq=fmspeed, mul=lfofm)
getdur = snd.getDur(False)
loopdur = indexMax*getdur-indexMin*getdur
pitrnds = [random.uniform(1.0-polyphony_spread, 1.0+polyphony_spread) for i in range(number_of_voices*2)]
ply = [i*lfofmrange for i in pitrnds]
pointer = Looper(snd, pitch=ply, start=indexMin*getdur, dur=loopdur, startfromloop=True, xfadeshape=1, autosmooth=True, mul=lfoamrange)
pointer2 = Looper(snd, pitch=pitrnds, start=indexMin*getdur, dur=loopdur, xfadeshape=1, startfromloop=True, autosmooth=True, mul=1)
out = Interp(pointer2, pointer, drywet, mul=env).out(chnl=[0,1])

#INIT
# onoffam(onoffam_value)
# onofffm(onofffm_value)

def sndchoice():
    snd.setSound(filesList15[int(sndidx.get())])
    getdur = snd.getDur(False)
    loopdur = indexMax*getdur-indexMin*getdur
    pointer.setTable(snd)
    pointer.setStart(indexMin*getdur)
    pointer2.setTable(snd)
    pointer2.setStart(indexMin*getdur)

def ampwavefunc():
    lfoam.type = int(ampwave.get())
    
def freqwavefunc():
    lfofm.type = int(freqwave.get())
            
def onoffamfunc():
    if int(onoffam.get()) == 0:
        pointer.mul = 1
    else:
        pointer.mul = lfoamrange
    
def onofffmfunc():
    if int(onofffm.get) == 0:
        pointer.pitch = pitrnds
    else:
        pointer.pitch = lfofmrange*pitrnds

