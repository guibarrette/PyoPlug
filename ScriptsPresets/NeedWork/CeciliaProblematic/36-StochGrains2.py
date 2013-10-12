# User Interface
defineUI(id=1, name="env", label="Amplitude", unit="x", init=.8)
# cgraph(name="grainenv", label="Grain Envelope", func=[(0,0),(.1,1),(.4,.8),(.7,.3),(1,0)], table=True, col="orange"),
defineUI(id=2, name="pitch_off", label="Pitch Offset", min=-12, max=12, init=0, rel="lin", res="int", unit="midi", col="red"),
# defineUI(id=1, name="pitch", label="Pitch Range", min=12, max=115, init=[48,72], rel="lin", unit="midi", col="filterred"),
defineUI(id=3, name="pitch_min", label="PitchMin", min=12, max=115, init=48, rel="lin", unit="midi", col="filterred")
defineUI(id=4, name="pitch_max", label="PitchMax", min=12, max=115, init=72, rel="lin", unit="midi", col="filterred")
# defineUI(id=1, name="speed_rng", label="Speed Range", min=.005, max=5, init=[.05, .25], rel="log", unit="sec", col="green"),
defineUI(id=5, name="speed_min", label="SpeedMin", min=.005, max=5, init=.05, rel="log", unit="sec", col="green")
defineUI(id=6, name="speed_max", label="SpeedMax", min=.005, max=5, init=.25, rel="log", unit="sec", col="green")
# defineUI(id=1, name="dur_rng", label="Duration Range", min=0.005, max=10, init=[.25,2], rel="log", unit="sec", col="forestgreen"),
defineUI(id=7, name="dur_min", label="DurationMin", min=0.005, max=10, init=.25, rel="log", unit="sec", col="forestgreen"),
defineUI(id=8, name="dur_max", label="DurationMax", min=0.005, max=10, init=2, rel="log", unit="sec", col="forestgreen"),
# defineUI(id=1, name="start_rng", label="Sample Start Range", min=0, max=1, init=[.1,.5], rel="lin", unit="%", col="forestgreen"),
defineUI(id=9, name="start_min", label="SampleStartMin", min=0, max=1, init=.1, rel="lin", unit="%", col="forestgreen"),
defineUI(id=10, name="start_max", label="SampleStartMax", min=0, max=1, init=.5, rel="lin", unit="%", col="forestgreen"),
# defineUI(id=1, name="dbamp_rng", label="Intensity Range", min=-90, max=0, init=[-18,-6], rel="lin", unit="dB", col="chorusyellow"),
defineUI(id=11, name="dbamp_min", label="IntensityMin", min=-90, max=0, init=-18, rel="lin", unit="dB", col="chorusyellow"),
defineUI(id=12, name="dbamp_max", label="IntensityMax", min=-90, max=0, init=-6, rel="lin", unit="dB", col="chorusyellow"),
# defineUI(id=1, name="pan_rng", label="Pan Range", min=0, max=1, init=[0,1], rel="lin", unit="x", col="khaki"),
defineUI(id=13, name="pan_min", label="PanMin", min=0, max=1, init=0, rel="lin", unit="x", col="khaki"),
defineUI(id=14, name="pan_max", label="PanMax", min=0, max=1, init=1, rel="lin", unit="x", col="khaki"),
defineUI(id=15, name="density", label="Density", min=0, max=100, init=100, rel="lin", unit="%", col="orange"),
defineUI(id=16, name="seed", func="seed_up", label="GlobalSeed", min=0, max=5000, init=0, rel="lin", res="int", unit="x", up=True),
defineUI(id=17, name="genmethod", func="genmethodfunc", label="PitchScaling", value=['All-over', 'Serial', 'Major', 'Minor', 'Seventh', 'Minor 7', 
        'Major 7', 'Minor 7 b5', 'Diminished', 'Diminished 7', 'Ninth', 'Major 9', 'Minor 9', 'Eleventh', 'Major 11', 
        'Minor 11', 'Thirteenth', 'Major 13', 'Whole-tone'], init="Major 11", col="red"),
defineUI(id=18, name="pitalgo", func="pitalgofunc", label="Pitch Algorithm", value=['Uniform', 'Linear min', 'Linear max', 'Triangular', 
        'Expon min', 'Expon max', 'Bi-exponential', 'Cauchy', 'Weibull', 'Gaussian', 'Poisson', 'Walker', 'Loopseg'], 
        init="Uniform", col="filterred"),
defineUI(id=19, name="speedalgo", func="speedalgofunc", label="Speed Algorithm", value=['Uniform', 'Linear min', 'Linear max', 'Triangular', 
        'Expon min', 'Expon max', 'Bi-exponential', 'Cauchy', 'Weibull', 'Gaussian', 'Poisson', 'Walker', 'Loopseg'], 
        init="Uniform", col="green"),
defineUI(id=20, name="duralgo", func="duralgofunc", label="Duration Algorithm", value=['Uniform', 'Linear min', 'Linear max', 'Triangular', 
        'Expon min', 'Expon max', 'Bi-exponential', 'Cauchy', 'Weibull', 'Gaussian', 'Poisson', 'Walker', 'Loopseg'], 
        init="Uniform", col="forestgreen"),
defineUI(id=21, name="mulalgo", func="mulalgofunc", label="Intensity Algorithm", value=['Uniform', 'Linear min', 'Linear max', 'Triangular', 
        'Expon min', 'Expon max', 'Bi-exponential', 'Cauchy', 'Weibull', 'Gaussian', 'Poisson', 'Walker', 'Loopseg'], 
        init="Uniform", col="chorusyellow"),
defineUI(id=22, name="numofvoices", label="Max Num of Grains", value=['5','10','15','20','25','30','40','50','60'], init='10', rate="i")
defineUI(id=23, name="tableidx", func="tablefunc", label="SoundLoaded", file=True, init="ounkmaster.aif", path=os.path.join(os.path.expanduser('~'), "Library/Audio/Presets/PyoPlug/0-Sounds/"))

class GrainSnd:
    def __init__(self, order, count, table, freq, start, dur, pan, mul, env, nchnls, table_dur):
        self.trig = Select(count, order)
        self.freq = SampHold(freq, self.trig, 1.0)
        self.start_rng = SampHold(start, self.trig, 1.0)
        self.start = TrigXnoise(self.trig, mul=self.start_rng[1]-self.start_rng[0], add=self.start_rng[0])
        self.dur_rng = SampHold(dur, self.trig, 1.0)
        self.dur = TrigXnoise(self.trig, mul=self.dur_rng[1]-self.dur_rng[0], add=self.dur_rng[0])
        self.pan = TrigRand(self.trig, pan[0], pan[1])
        self.mul = TrigXnoise(self.trig, mul=mul[1]-mul[0], add=mul[0])
        self.amp = TrigEnv(self.trig, env, self.dur, mul=self.mul*0.25)
        self.pointer = TrigEnv(self.trig, LinTable(), self.dur, mul=self.dur*self.freq/table_dur, add=self.start)
        self.s1 = Pointer(table, self.pointer, mul=self.amp)
        self.out = SPan(self.s1, outs=nchnls, pan=self.pan)


# DSP
# table = addFilein("snd")
grainenv = DataTable(5, [(0,0),(.1,1),(.4,.8),(.7,.3),(1,0)])
usrPath = os.path.expanduser('~')
table = SfPlayer(os.path.join(usrPath, "Library/Audio/Presets/PyoPlug/0-Sounds/ounkmaster.aif"), loop=True)
table_dur = table.getDur()
s.setGlobalSeed(int(seed.get()))
num = int(numofvoices_value)
scaledict =    {'Major':[0,4,7], 'Minor':[0,3,7], 'Seventh':[0,4,7,10], 'Minor 7':[0,3,7,10], 'Major 7':[0,4,7,11], 
                    'Minor 7 b5':[0,3,6,10], 'Diminished':[0,3,6], 'Diminished 7':[0,3,6,9], 'Minor 9':[0,3,7,10,14], 
                    'Major 9':[0,4,7,11,14], 'Ninth':[0,4,7,10,14], 'Minor 11':[0,3,7,10,14,17], 'Major 11':[0,4,7,11,14,18], 
                    'Eleventh':[0,4,7,10,14,18], 'Major 13':[0,4,7,11,14,18,21], 'Thirteenth':[0,4,7,10,14,18,21], 
                    'Serial':[0,1,2,3,4,5,6,7,8,9,10,11], 'Whole-tone': [0,2,4,6,8,10]}

speedgen = XnoiseDur(min=speed_rng[0], max=speed_rng[1])
new = Change(speedgen)
newpass = Percent(new, density)
count = VoiceManager(newpass)

pitfloat = TrigXnoise(newpass, mul=pitch[1]-pitch[0], add=pitch_off+pitch[0])
freq = MToT(pitfloat)
pitint = TrigXnoiseMidi(newpass, mrange=(0, 120), mul=0.007874015748031496)
pitch_range = pitch[1]-pitch[0]
scl = Snap(pitint*pitch_range+pitch[0]+pitch_off, choice=scaledict["Serial"], scale=2)
frtostack = Sig(freq)

mul_rng = DBToA(dbamp_rng)

stack = [GrainSnd(i, count, table, frtostack, start_rng, dur_rng, pan_rng, 
                        mul_rng, grainenv, nchnls, table_dur) for i in range(num)]
stack_mix = Mix([gr.out for gr in stack], voices=nchnls)
out = Sig(stack_mix)

count.setTriggers([obj.amp["trig"] for obj in stack])

speedalgo(speedalgo_index, speedalgo_value)
mulalgo(mulalgo_index, mulalgo_value)
duralgo(duralgo_index, duralgo_value)
pitalgo(pitalgo_index, pitalgo_value)
genmethod(genmethod_index, genmethod_value)

def tablefunc():
    table = SfPlayer(filesList23[int(specidx.get())], loop=True)     # resetting the SfPlayer so it can change to a sound file of any numbers of channels
    table_dur = table.getDur()
    proc.setInput(spec)

def assignX1X2(index, *args):
    for arg in args:
        arg.dist = index
        if index in [4,5,6]:
            arg.x1 = 8
        elif index == 7:
            arg.x1 = 2
        elif index == 8:
            arg.x1 = 0.5
            arg.x2 = 3.2
        elif index == 9:
            arg.x1 = 0.5
            arg.x2 = 1
        elif index == 10:
            arg.x1 = 3
            arg.x2 = 2
        elif index in [11,12]:
            arg.x1 = 1
            arg.x2 = .25

def speedalgofunc():
    assignX1X2(int(speedalgo.get()), speedgen)

def pitalgofunc():
    assignX1X2(int(pitalgo.get()), pitfloat, pitint)

def duralgofunc():
    assignX1X2(int(duralgo.get()), *[obj.dur for obj in stack])

def mulalgofunc():
    assignX1X2(int(mulalgo.get()), *[obj.mul for obj in stack])

def genmethodfunc(index, value):
    genmethodlist = ['All-over', 'Serial', 'Major', 'Minor', 'Seventh', 'Minor 7', 
        'Major 7', 'Minor 7 b5', 'Diminished', 'Diminished 7', 'Ninth', 'Major 9', 'Minor 9', 'Eleventh', 'Major 11', 
        'Minor 11', 'Thirteenth', 'Major 13', 'Whole-tone']
    value = genmethodlist[int(genmethod.get())]
    if value == "All-over":
        pitfloat.play()
        freq.play()
        frtostack.value = freq
        pitint.stop()
        scl.stop()
    else:
        scl.choice = scaledict[value]
        pitint.play()
        scl.play()
        frtostack.value = scl
        pitfloat.stop()
        freq.stop()

def seed_up():
    s.setGlobalSeed(int(seed.get()))


