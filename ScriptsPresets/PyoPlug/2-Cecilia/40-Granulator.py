import random
"""
Granulator module

Sliders under the graph:

    - Transpose : Base pitch of the grains
    - Grain Position : Soundfile index
    - Position Random : Jitter applied on the soundfile index
    - Pitch Random : Jitter applied on the pitch of the grains using the discreet transpo list
    - Grain Duration : Length of the grains
    - # of Grains : Number of grains

Dropdown menus, toggles and sliders on the bottom left:

    - Grain Env : Shape of the grains
    - Discreet Transpo : List of pitch ratios
    - # of Voices : Number of voices played simultaneously (polyphony), only available at initialization time
    - Polyphony Spread : Pitch variation between voices (chorus), only available at initialization time
    
Graph only parameters :

    - Overall Amplitude : The amplitude curve applied on the total duration of the performance
"""

# User Interface
defineUI(id=1, name="env", label="Amplitude", unit="x", init=.8)
# defineUI(id=2, name="grainenv", label="GrainEnvelope", func=[(0,0),(0.5,1),(1,0)], table=True, curved=True, col="chorusyellow")
defineUI(id=2, name="transp", label="Transpose", min=-4800, max=4800, init=0, rel="lin", unit="cnts", col="green")
defineUI(id=3, name="pos", label="GrainPosition", min=0, max=1, init=0, rel="lin", unit="x", col="blue")
defineUI(id=4, name="posrnd", label="PositionRandom", min=0, max=0.5, init=0.005, rel="lin", unit="x", col="red3",half=True)
defineUI(id=5, name="pitrnd", label="PitchRandom", min=0, max=0.5, init=0.005, rel="lin", unit="x", col="red3",half=True)
defineUI(id=6, name="cut", label="FiltFreq", min=100, max=18000, init=20000, rel="log", unit="Hz", col="green3")
defineUI(id=7, name="filterq", label="FiltQ", min=0.5, max=10, init=0.707, rel="log", unit="Q", col="green3")
defineUI(id=8, name="dur", func="dur_up", label="GrainDuration", min=0.01, max=10, init=0.1, up=True, rel="log", unit="sec", col="blue",half=True)
defineUI(id=9, name="num", func="num_up", label="#ofGrains", min=1, max=150, init=24, rel="lin", gliss=0, res="int", up=True, unit="grs", col="tan",half=True)
defineUI(id=10, name="filttype", func="filttypefunc", label="FiltType", init="Lowpass", col="green3", value=["Lowpass","Highpass","Bandpass","Bandstop"])
defineUI(id=11, name="balance", func="balancefunc", label = "Balance", init= "Off", col="blue", value=["Off","Compress", "Source"])
defineUI(id=12, name="discreet", func="discreetfunc", label="DiscreetTranspo", init=1, min=0, max=4, col="forestgreen")
defineUI(id=13, name="sndidx", func="sndchoice", label="SndTable", file=True, init="ounkmaster.aif", path=os.path.join(os.path.expanduser('~'), "Library/Audio/Presets/PyoPlug/0-Sounds/"))


# DSP
grainenv = HannTable()

polyphony_spread = .7
number_of_voices = 1
amp_scl = Map(200, 1, "lin")
firstamp = amp_scl.set(24)
pitrnds = [random.uniform(1.0-polyphony_spread, 1.0+polyphony_spread) for i in range(number_of_voices*2)]

# t = stereoIn
usrPath = os.path.expanduser('~')
t = SndTable(os.path.join(usrPath, "Library/Audio/Presets/PyoPlug/0-Sounds/ounkmaster.aif"))
posr = Noise(posrnd*t.getSize(False))
pitr = Noise(pitrnd, add=1)
discr = Choice(choice=[1], freq=250)
pitch = CentsToTranspo(transp, mul=pitrnds)
pospos = Sig(pos, mul=t.getSize(False), add=posr)
gr = Granulator(t, grainenv, pitch=pitch, pos=pospos, dur=dur*pitr*discr, grains=24, basedur=0.1, mul=env* 0.1 * firstamp)
gro = Biquadx(gr, freq=cut, q=filterq, type=int(filttype.get()), stages=2)


osc = Sine(10000,mul=.1)
balanced = Balance(gro, osc, freq=10)
out = Interp(gro, balanced).out(chnl=[0,1])

#INIT
# balance(balance_index, balance_value)

def sndchoice():
    t.setSound(filesList13[int(sndidx.get())])
    posr.setType(posrnd*t.getSize(False))
    pospos.mul = t.getSize(False)
    gr.setTable(t)

def balancefunc():
    index = int(balance.get())
    if index == 0:
        out.interp  = 0
    elif index ==1:
       out.interp  = 1
       balanced.input2 = osc
    elif index == 2:
       out.interp = 1
       balanced.input2 = gr

def filttypefunc():
    gro.type = int(filttype.get())

def dur_up():
    value = dur.get()
    gr.basedur = value
    gr.dur = value*discr
    
def num_up():
    grnum = int(num.get())
    gr.grains = grnum
    gr.mul = env * 0.1 * amp_scl.set(grnum)

def discreetfunc():
    discr.choice = discreet.get()
