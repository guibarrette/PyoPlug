

# User Interface
defineUI(id=1, name="env", label="Amplitude", unit="x", init=.8)
# defineUI(id=2, name="grainenv", label="Grain Envelope", func=[(0,0),(.01,1),(.2,.4),(.5,.3),(1,0)], table=True, col="orange"),
# defineUI(id=3, name="brightenv", label="Brightness Envelope", func=[(0,1),(.2,.2),(1,0)], table=True, col="chorusyellow"),
defineUI(id=4, name="pitch_off", label="PitchOffset", min=-12, max=12, init=0, rel="lin", res="int", unit="midi", col="red"),
defineUI(id=5, name="pitch_min", label="PitchMin", min=12, max=115, init=48, rel="lin", unit="midi", col="filterred"),
defineUI(id=5, name="pitch_max", label="PitchMax", min=12, max=115, init=84, rel="lin", unit="midi", col="filterred"),
defineUI(id=6, name="speed_rng", label="Speed Range", min=.005, max=5, init=[.05, .25], rel="log", unit="sec", col="green"),
defineUI(id=7, name="dur_rng", label="Duration Range", min=.005, max=20, init=[.5,5], rel="log", unit="sec", col="forestgreen"),
defineUI(id=8, name="bright_rng", label="Brightness Range", min=0, max=1, init=[0,.1], rel="lin", unit="x", col="marineblue"),
defineUI(id=9, name="detune_rng", label="Detune Range", min=0.0001, max=1, init=[0.0001, 0.0005], rel="log", unit="x", col="royalblue"),
defineUI(id=10, name="dbamp_rng", label="Intensity Range", min=-90, max=0, init=[-18,-6], rel="lin", unit="dB", col="chorusyellow"),
defineUI(id=11, name="pan_rng", label="Pan Range", min=0, max=1, init=[0,1], rel="lin", unit="x", col="khaki"),
defineUI(id=12, name="density", label="Density", min=0, max=100, init=100, rel="lin", unit="%", col="orange"),
defineUI(id=13, name="seed", func="seed_up", label="Global seed", min=0, max=5000, init=0, rel="lin", res="int", unit="x", up=True),
defineUI(id=14, name="synth", func="synthfunc", label="SynthType", value=['FM', 'Looped Sine', 'Impulse train', 'CrossFM', 'Sawtooth', 'Square', 'Pulsar', 'AddSynth'], init="FM", col="compblue"),
defineUI(id=15, name="genmethod", label="Pitch Scaling", value=['All-over', 'Serial', 'Major', 'Minor', 'Seventh', 'Minor 7', 'Major 7', 'Minor 7 b5', 'Diminished', 'Diminished 7', 'Ninth', 'Major 9', 'Minor 9', 'Eleventh', 'Major 11', 'Minor 11', 'Thirteenth', 'Major 13', 'Whole-tone'], init="Major 11", col="red"),
defineUI(id=16, name="pitalgo", label="Pitch Algorithm", value=['Uniform', 'Linear min', 'Linear max', 'Triangular', 'Expon min', 'Expon max', 'Bi-exponential', 'Cauchy', 'Weibull', 'Gaussian', 'Poisson', 'Walker', 'Loopseg'], init="Uniform", col="filterred"),
defineUI(id=17, name="speedalgo", label="Speed Algorithm", value=['Uniform', 'Linear min', 'Linear max', 'Triangular', 'Expon min', 'Expon max', 'Bi-exponential', 'Cauchy', 'Weibull', 'Gaussian', 'Poisson', 'Walker', 'Loopseg'], init="Uniform", col="green"),
defineUI(id=18, name="duralgo", label="Duration Algorithm", value=['Uniform', 'Linear min', 'Linear max', 'Triangular', 'Expon min', 'Expon max', 'Bi-exponential', 'Cauchy', 'Weibull', 'Gaussian', 'Poisson', 'Walker', 'Loopseg'], init="Uniform", col="forestgreen"),
defineUI(id=19, name="mulalgo", label="Intensity Algorithm", value=['Uniform', 'Linear min', 'Linear max', 'Triangular', 'Expon min', 'Expon max', 'Bi-exponential', 'Cauchy', 'Weibull', 'Gaussian', 'Poisson', 'Walker', 'Loopseg'], init="Uniform", col="chorusyellow"),
defineUI(id=20, name="numofvoices", label="MaxNumOfGrains", value=['5','10','15','20','25','30','40','50','60'], init='10', rate="i")


# DSP
GRAIN_SAWTOOTH_WAVEFORM = SawTable(20)
GRAIN_SQUARE_WAVEFORM = SquareTable(30)
GRAIN_SINC_WAVEFORM = SincTable(freq=3.14159*16, windowed=True)
GRAIN_PULSAR_WAVEFORM = SincTable(freq=3.14159*4, windowed=True)
GRAIN_ENVELOPE_WAVEFORM = HannTable()
GRAIN_SINE_WAVEFORM = HarmTable([1,0,0,.1,0,.3,0,0,.2,0,0,.1,0,0,.15,0,.1,0,0,.2,0,.1,0,0,.1,0,0,.07,0,.05])

class Grain:
    def __init__(self, order, count, freq, det, bri, dur, pan, mul, env, brienv):
        trig = Select(count, order)
        freq = SampHold(freq, trig, 1.0)
        dur = TrigXnoise(trig, mul=dur[1]-dur[0], add=dur[0])
        det = TrigRand(trig, det[0], det[1])
        bri = TrigRand(trig, bri[0], bri[1])
        pan = TrigRand(trig, pan[0], pan[1])
        mul = TrigXnoise(trig, mul=mul[1]-mul[0], add=mul[0])
        amp = TrigEnv(trig, env, dur, mul=mul*.1)

    def stop(self):
        for obj in __dict__.values():
            obj.stop()
        return self

    def play(self):
        for obj in __dict__.values():
            obj.play()
        return self

class GrainFM(Grain):
    def __init__(self, order, count, freq, det, bri, dur, pan, mul, env, brienv, nchnls):
        Grain.__init__(self, order, count, freq, det, bri, dur, pan, mul, env, brienv)
        ind = TrigEnv(trig, brienv, dur, mul=bri*20)
        s1 = FM(carrier=freq, ratio=det*.4+1, index=ind, mul=amp)
        out = SPan(s1, outs=nchnls, pan=pan)

class GrainSL(Grain):
    def __init__(self, order, count, freq, det, bri, dur, pan, mul, env, brienv, nchnls):
        Grain.__init__(self, order, count, freq, det, bri, dur, pan, mul, env, brienv)
        feed = TrigEnv(trig, brienv, dur, mul=bri*.3)
        s1 = SineLoop(freq, feedback=feed, mul=amp)
        detune = det * .3 + 1
        s2 = SineLoop(freq*detune, feedback=feed, mul=amp)
        out = SPan(s1+s2, outs=nchnls, pan=pan)

class GrainBlit(Grain):
    def __init__(self, order, count, freq, det, bri, dur, pan, mul, env, brienv, nchnls):
        Grain.__init__(self, order, count, freq, det, bri, dur, pan, mul, env, brienv)
        cutoff = TrigEnv(trig, brienv, dur, mul=bri*10000, add=100)
        s1 = Osc(GRAIN_SINC_WAVEFORM, freq, mul=amp)
        detune = det * .3 + 1
        s2 = Osc(GRAIN_SINC_WAVEFORM, freq*detune, mul=amp)
        filt = Tone(s1+s2, cutoff, mul=4)
        out = SPan(filt, outs=nchnls, pan=pan)

class GrainCrossFM(Grain):
    def __init__(self, order, count, freq, det, bri, dur, pan, mul, env, brienv, nchnls):
        Grain.__init__(self, order, count, freq, det, bri, dur, pan, mul, env, brienv)
        ind = TrigEnv(trig, brienv, dur, mul=bri*4)
        s1 = CrossFM(carrier=freq, ratio=det*.4+1, ind1=4, ind2=ind, mul=amp)
        out = SPan(s1, outs=nchnls, pan=pan)

class GrainSaw(Grain):
    def __init__(self, order, count, freq, det, bri, dur, pan, mul, env, brienv, nchnls):
        Grain.__init__(self, order, count, freq, det, bri, dur, pan, mul, env, brienv)
        cutoff = TrigEnv(trig, brienv, dur, mul=bri*10000, add=100)
        s1 = Osc(GRAIN_SAWTOOTH_WAVEFORM, freq, mul=amp)
        detune = det * .3 + 1
        s2 = Osc(GRAIN_SAWTOOTH_WAVEFORM, freq*detune, mul=amp)
        filt = Tone(s1+s2, cutoff, mul=.7)
        out = SPan(filt, outs=nchnls, pan=pan)

class GrainSquare(Grain):
    def __init__(self, order, count, freq, det, bri, dur, pan, mul, env, brienv, nchnls):
        Grain.__init__(self, order, count, freq, det, bri, dur, pan, mul, env, brienv)
        cutoff = TrigEnv(trig, brienv, dur, mul=bri*10000, add=100)
        s1 = Osc(GRAIN_SQUARE_WAVEFORM, freq, mul=amp)
        detune = det * .3 + 1
        s2 = Osc(GRAIN_SQUARE_WAVEFORM, freq*detune, mul=amp)
        filt = Tone(s1+s2, cutoff, mul=.7)
        out = SPan(filt, outs=nchnls, pan=pan)

class GrainPulsar(Grain):
    def __init__(self, order, count, freq, det, bri, dur, pan, mul, env, brienv, nchnls):
        Grain.__init__(self, order, count, freq, det, bri, dur, pan, mul, env, brienv)
        frac = TrigEnv(trig, brienv, dur, mul=bri)
        scl_frac = Scale(frac, 0, 1, 1, 0.05)
        s1 = Pulsar(GRAIN_PULSAR_WAVEFORM, env=GRAIN_ENVELOPE_WAVEFORM, freq=freq, frac=scl_frac, mul=amp)
        detune = det * .3 + 1
        s2 = Pulsar(GRAIN_PULSAR_WAVEFORM, env=GRAIN_ENVELOPE_WAVEFORM, freq=freq*detune, frac=scl_frac, mul=amp)
        out = SPan(s1+s2, outs=nchnls, pan=pan)

class GrainAddSynth(Grain):
    def __init__(self, order, count, freq, det, bri, dur, pan, mul, env, brienv, nchnls):
        Grain.__init__(self, order, count, freq, det, bri, dur, pan, mul, env, brienv)
        cutoff = TrigEnv(trig, brienv, dur, mul=bri*10000, add=100)
        s1 = OscBank(GRAIN_SINE_WAVEFORM, freq=freq, spread=det*.25, slope=1, num=8, fjit=True, mul=amp)
        s2 = Tone(s1, cutoff, mul=4)
        out = SPan(s2, outs=nchnls, pan=pan)


# DSP
s.setGlobalSeed(int(seed.get()))
grainenv = DataTable(5, [(0,0),(.01,1),(.2,.4),(.5,.3),(1,0)])
brightenv = DataTable(3, [(0,1),(.2,.2),(1,0)])
num = int(numofvoices_value)
current_synth = 0
scaledict =    {'Major':[0,4,7], 'Minor':[0,3,7], 'Seventh':[0,4,7,10], 'Minor 7':[0,3,7,10], 'Major 7':[0,4,7,11], 
                    'Minor 7 b5':[0,3,6,10], 'Diminished':[0,3,6], 'Diminished 7':[0,3,6,9], 'Minor 9':[0,3,7,10,14], 
                    'Major 9':[0,4,7,11,14], 'Ninth':[0,4,7,10,14], 'Minor 11':[0,3,7,10,14,17], 'Major 11':[0,4,7,11,14,18], 
                    'Eleventh':[0,4,7,10,14,18], 'Major 13':[0,4,7,11,14,18,21], 'Thirteenth':[0,4,7,10,14,18,21], 
                    'Serial':[0,1,2,3,4,5,6,7,8,9,10,11], 'Whole-tone': [0,2,4,6,8,10]}
stack_dict = {"FM": GrainFM, "Looped Sine": GrainSL, "Impulse train": GrainBlit, "AddSynth": GrainAddSynth,
                   "CrossFM": GrainCrossFM, "Sawtooth": GrainSaw, "Square": GrainSquare, "Pulsar": GrainPulsar}

speedgen = XnoiseDur(min=speed_rng[0], max=speed_rng[1])
new = Change(speedgen)
newpass = Percent(new, density)
count = VoiceManager(newpass)

pitfloat = TrigXnoise(newpass, mul=pitch_max-pitch_min, add=pitch_off+pitch_min)
freq = MToF(pitfloat)
pitint = TrigXnoiseMidi(newpass, mul=0.007874015748031496)
pitch_range = pitch_max-pitch_min
scl = Snap(pitint*pitch_range+pitch_min+pitch_off, choice=scaledict["Serial"], scale=1)
frtostack = Sig(freq)

mul_rng = DBToA(dbamp_rng)

for key in stack_dict.keys():
    stack = [stack_dict[key](i, count, frtostack, detune_rng, bright_rng, dur_rng, 
            pan_rng, mul_rng, grainenv, brightenv, nchnls).stop() for i in range(num)]
    stack_mix = Mix([gr.out for gr in stack], voices=nchnls).stop()
    stack_dict[key] = [stack, stack_mix]

count.setTriggers([obj.amp["trig"] for obj in stack_dict[current_synth][0]])

[obj.play() for obj in stack_dict[current_synth][0]]
stack_dict[current_synth][1].play()
out = Sig(stack_dict[current_synth][1]).out()

speedalgo(speedalgo_index, speedalgo_value)
mulalgo(mulalgo_index, mulalgo_value)
duralgo(duralgo_index, duralgo_value)
pitalgo(pitalgo_index, pitalgo_value)
genmethod(genmethod_index, genmethod_value)

def synthfunc():
    value = int(synth.get())
    [obj.stop() for obj in stack_dict[current_synth][0]]
    [obj.play() for obj in stack_dict[value][0]]
    stack_dict[value][1].play()
    out.value = stack_dict[value][1]
    current_synth = value
    count.setTriggers([obj.amp["trig"] for obj in stack_dict[current_synth][0]])

def assignX1X2(self, index, *args):
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

def speedalgo(self, index, value):
    assignX1X2(index, speedgen)

def pitalgo(self, index, value):
    assignX1X2(index, pitfloat, pitint)

def duralgo(self, index, value):
    for key in stack_dict.keys():
        assignX1X2(index, *[obj.dur for obj in stack_dict[key][0]])

def mulalgo(self, index, value):
    for key in stack_dict.keys():
        assignX1X2(index, *[obj.mul for obj in stack_dict[key][0]])

def genmethod(self, index, value):
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


