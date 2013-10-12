# Set the Spectral envelope and Exciter: SFPlayer()
# Need time position from DAW, Suspend and Resume from DAW

"""
Module's documentation

"""
# User Interface
# csampler(name="spec", label="Spectral Envelope"),
# csampler(name="exci", label="Exciter"),
defineUI(id=1, name="env", label="Amplitude", unit="x", init=.8)
defineUI(id=2, name="freq", label="BaseFreq", min=10, max=1000, init=80, rel="log", unit="Hz", col="green"),
defineUI(id=3, name="spread", label="FreqSpread", min=0.25, max=2, init=1.25, rel="log", unit="x", col="forestgreen"),
defineUI(id=4, name="q", label="QFactor", min=0.5, max=200, init=20, rel="log", unit="Q", col="orange"),
defineUI(id=5, name="slope", label="TimeResponse", min=0, max=1, init=0.5, rel="lin", unit="x", col="red"),
defineUI(id=6, name="gain", label="Gain", min=-90, max=18, init=0, rel="lin", unit="dB", col="blue"),
defineUI(id=7, name="stagesval", func="stages", label="NumOfbands", min=4, max=64, init=20, rel="lin", res="int", unit="x", up=True),
defineUI(id=8, name="balance", func="balancefunc", label="Balance", init= "Source", col="blue", value=["Off","Compress", "Source"])
defineUI(id=9, name="specidx", func="specfunc", label="SoundLoaded", file=True, init="ounkmaster.aif", path=os.path.join(os.path.expanduser('~'), "Library/Audio/Presets/PyoPlug/0-Sounds/"))
# defineUI(id=9, name="specidx", func="specfunc", label="SndLoaded", file=True, init="ounkmaster.aif", path="/Users/Gui/Library/Audio/Presets/PyoPlug/0-Sounds/")


# DSP
# spec = addSampler("spec")
exci = stereoIn
# exci = SfPlayer("/Users/Gui/Library/Audio/Presets/PyoPlug/0-Sounds/ounkmaster.aif", speed=[1,1], loop=True, mul=.3).play()
# spec = stereoIn
# exci = addSampler("exci")
# spec = SndTable("/Users/Gui/Library/Audio/Presets/PyoPlug/0-Sounds/ounkmaster.aif")
usrPath = os.path.expanduser('~')
spec = SfPlayer(os.path.join(usrPath, "Library/Audio/Presets/PyoPlug/0-Sounds/ounkmaster.aif"), loop=True)
nchnls = len(exci)
proc = Vocoder(spec, exci, freq=freq, spread=spread, q=q, slope=slope, stages=20, mul=DBToA(gain))
deg = Mix(proc, voices=nchnls, mul=env)

osc = Sine(10000,mul=.1)
balanced = Balance(deg, osc, freq=10)
out = Interp(deg, balanced).out(chnl=[0,1])

#INIT
# balance(balance_index, balance_value)

def stages():
    proc.stages = int(stagesval.get())

def balancefunc():
    index = int(balance.get())
    if index == 0:
        out.interp= 0
    elif index ==1:
        out.interp= 1
        balanced.input2 = osc
    elif index == 2:
        out.interp = 1
        balanced.input2 = spec
    else:
        out.interp = 1
        balanced.input2 = exci

def specfunc():
    # global spec
    spec = SfPlayer(filesList9[int(specidx.get())], loop=True)     # resetting the SfPlayer so it can change to a sound file of any numbers of channels
    # spec.setSound(filesList9[int(specidx.get())])
    proc.setInput(spec)
 