"""
Multi-band algorithmic beatmaker module

Sliders under the graph:

    - Frequency Splitter : Split points for multi-band processing
    - # of Taps : Number of taps in a measure
    - Tempo : Speed of taps
    - Tap Length : Length of taps
    - Beat 1 Index : Soundfile index of the first beat
    - Beat 2 Index : Soundfile index of the second beat
    - Beat 3 Index : Soundfile index of the third beat
    - Beat 1 Distribution : Repartition of taps for the first beat (100% weak --> 100% down)
    - Beat 2 Distribution : Repartition of taps for the second beat (100% weak --> 100% down)
    - Beat 3 Distribution : Repartition of taps for the third beat (100% weak --> 100% down)
    - Beat 1 Gain : Gain of the first beat
    - Beat 2 Gain : Gain of the second beat
    - Beat 3 Gain : Gain of the third beat
    - Global Seed : Seed value for the algorithmic beats, using the same seed with the same distributions will yield the exact same beats

Dropdown menus, toggles and sliders on the bottom left:

    - # of Voices : Number of voices played simultaneously (polyphony), only available at initialization time
    - Polyphony Spread : Pitch variation between voices (chorus), only available at initialization time
    
Graph only parameters :

    - Beat 1 ADSR : Envelope of taps for the first beat in breakpoint fashion
    - Beat 2 ADSR : Envelope of taps for the second beat in breakpoint fashion
    - Beat 3 ADSR : Envelope of taps for the third beat in breakpoint fashion
    - Overall Amplitude : The amplitude curve applied on the total duration of the performance
"""

# User Interface
defineUI(id=1, name="env", label="Amplitude", unit="x", init=.8)
defineUI(id=2, name="split1", func="splitter", label="Freq1Split", min=100, max=18000, init=150, num_knobs=3, rel="log", gliss=0, up=True, unit="Hz", col="grey")
defineUI(id=3, name="split2", func="splitter", label="Freq2Split", min=100, max=18000, init=500, num_knobs=3, rel="log", gliss=0, up=True, unit="Hz", col="grey")
defineUI(id=4, name="split3", func="splitter", label="Freq3Split", min=100, max=18000, init=2000, num_knobs=3, rel="log", gliss=0, up=True, unit="Hz", col="grey")
# cgraph(name="adsr1", label="Beat 1 ADSR", func=[(0,0),(0.1,1),(0.122,0.25),(1,0)], table=True, col="blue")
# cgraph(name="adsr2", label="Beat 2 ADSR", func=[(0,0),(0.1,1),(0.122,0.25),(1,0)], table=True, col="blue")
# cgraph(name="adsr3", label="Beat 3 ADSR", func=[(0,0),(0.1,1),(0.122,0.25),(1,0)], table=True, col="blue")
# cgraph(name="adsr4", label="Beat 4 ADSR", func=[(0,0),(0.1,1),(0.122,0.25),(1,0)], table=True, col="blue")
defineUI(id=5, name="taps", func="newdist", label="#ofTaps", min=1, max=64, init=16, res="int", rel="lin", unit="x")
defineUI(id=6, name="tempo", label="Tempo", min=20, max=240, gliss=0, init=120, rel="lin", unit="bpm", col="green")
defineUI(id=7, name="tapsl", label="TapLength", min=0.1, max=1, init=0.1, rel="lin", unit="sec", col="tan")
defineUI(id=8, name="bindex1", label="Beat1Index", min=0, max=1, init=0, rel="lin", unit="x", col="olivegreen",half=True)
defineUI(id=9, name="bindex2", label="Beat2Index", min=0, max=1, init=0.4, rel="lin", unit="x", col="lightblue",half=True)
defineUI(id=10, name="we1", label="Beat1Distribution", min=0, max=100, init=80, res="int", rel="lin", unit="%", col="olivegreen",half=True)
defineUI(id=11, name="we2", label="Beat2Distribution", min=0, max=100, init=80, res="int", rel="lin", unit="%", col="lightblue",half=True)
defineUI(id=12, name="gain1", label="Beat1Gain", min=-48, max=18, init=0, rel="lin", unit="dB", col="olivegreen",half=True)
defineUI(id=13, name="gain2", label="Beat2Gain", min=-48, max=18, init=0, rel="lin", unit="dB", col="lightblue",half=True)
defineUI(id=14, name="bindex3", label="Beat3Index", min=0, max=1, init=0.8, rel="lin", unit="x", col="lightblue",half=True)
defineUI(id=15, name="bindex4", label="Beat4Index", min=0, max=1, init=0.9, rel="lin", unit="x", col="olivegreen",half=True)
defineUI(id=16, name="we3", label="Beat3Distribution", min=0, max=100, init=30, rel="lin", res="int", unit="%", col="lightblue",half=True)
defineUI(id=17, name="we4", label="Beat4Distribution", min=0, max=100, init=20, rel="lin", res="int", unit="%", col="olivegreen",half=True)
defineUI(id=18, name="gain3", label="Beat3Gain", min=-48, max=18, init=0, rel="lin", unit="dB", col="lightblue",half=True)
defineUI(id=19, name="gain4", label="Beat4Gain", min=-48, max=18, init=0, rel="lin", unit="dB", col="olivegreen",half=True)
defineUI(id=20, name="seed", func="seed_up", label="GlobalSeed", min=0, max=5000, init=0, rel="lin", res="int", unit="x", up=True)
defineUI(id=21, name="snd", func="sndchoice", label="SoundLoaded", file=True, init="ounkmaster.aif", path=os.path.join(os.path.expanduser('~'), "Library/Audio/Presets/PyoPlug/0-Sounds/"))


# DSP
adsr1 = DataTable(size=4, [(0,0),(0.1,1),(0.122,0.25),(1,0)])
adsr2 = DataTable(size=4, [(0,0),(0.1,1),(0.122,0.25),(1,0)])
adsr3 = DataTable(size=4, [(0,0),(0.1,1),(0.122,0.25),(1,0)])
adsr4 = DataTable(size=4, [(0,0),(0.1,1),(0.122,0.25),(1,0)])

# snd = addFilein("snd")
usrPath = os.path.expanduser('~')
snd = SndTable(os.path.join(usrPath, "Library/Audio/Presets/PyoPlug/0-Sounds/snd_3.aif"))
polyphony_spread = 0.7
number_of_voices = 8

last_we1 = last_we2 = last_we3 = last_we4 = last_taps = -1
rtempo = 1/(tempo/15)
# setGlobalSeed(int(seed.get()))
beat1 = Beat(time=rtempo, taps=16, w1=80, w2=40, w3=20, poly=8).play()
beat2 = Beat(time=rtempo, taps=16, w1=50, w2=100, w3=50, poly=8).play()
beat3 = Beat(time=rtempo, taps=16, w1=30, w2=60, w3=70, poly=8).play()
beat4 = Beat(time=rtempo, taps=16, w1=15, w2=30, w3=90, poly=8).play()
tre1 = TrigEnv(input=beat1, table=adsr1, dur=tapsl, mul=beat1['amp'])
tre2 = TrigEnv(input=beat2, table=adsr2, dur=tapsl, mul=beat2['amp'])
tre3 = TrigEnv(input=beat3, table=adsr3, dur=tapsl, mul=beat3['amp'])
tre4 = TrigEnv(input=beat4, table=adsr4, dur=tapsl, mul=beat4['amp'])
linseg1 = TrigLinseg(input=beat1, list=[(0,0),(0.1,1/(snd.getDur(False)/0.1)+0)])
linseg2 = TrigLinseg(input=beat2, list=[(0,0.4),(0.1,(1/(snd.getDur(False)/0.1))+0.4)])
linseg3 = TrigLinseg(input=beat3, list=[(0,0.8),(0.1,(1/(snd.getDur(False)/0.1))+0.8)])
linseg4 = TrigLinseg(input=beat4, list=[(0,0.9),(0.1,(1/(snd.getDur(False)/0.1))+0.9)])
trf1 = TrigFunc(linseg1['trig'], newseg1)
trf2 = TrigFunc(linseg2['trig'], newseg2)
trf3 = TrigFunc(linseg3['trig'], newseg3)
trf4 = TrigFunc(linseg4['trig'], newseg4)
again1 = DBToA(gain1)
again2 = DBToA(gain2)
again3 = DBToA(gain3)
again4 = DBToA(gain4)
pointer1 = Biquad(Pointer(table=snd, index=linseg1, mul=tre1*again1), freq=split1, q=0.707, type=0)
pointer2 = Biquad(Pointer(table=snd, index=linseg2, mul=tre2*again2), freq=split2, q=0.707, type=2)
pointer3 = Biquad(Pointer(table=snd, index=linseg3, mul=tre3*again3), freq=split3, q=0.707, type=1)
pointer4 = Biquad(Pointer(table=snd, index=linseg4, mul=tre4*again4), freq=split3, q=0.707, type=1)
mixx = pointer1+pointer2+pointer3+pointer4
sig = Sig(mixx, mul=env).mix(nchnls)
chorusd = Scale(input=Sig(polyphony_spread), inmin=0.0001, inmax=0.5, outmin=0, outmax=5)
chorusb = Scale(input=Sig(number_of_voices), inmin=1, inmax=10, outmin=0, outmax=1)
out = Chorus(input=sig, depth=chorusd, feedback=0.25, bal=chorusb).out()


trigend = TrigFunc(beat1["end"], newdist)
        
# def sndchoice():
#     spec.setSound(filesList9[int(specidx.get())])
#     proc.setInput(spec)

def seed_up():
    # setGlobalSeed(int(value))
    beat1.new()
    beat2.new()
    beat3.new()
    
def newseg1():
    linseg1.setList([(0,bindex1.get()),(tapsl.get(),1/(snd.getDur(False)/tapsl.get())+bindex1.get())])
    
def newseg2():
    linseg2.setList([(0,bindex2.get()),(tapsl.get(),1/(snd.getDur(False)/tapsl.get())+bindex2.get())])
    
def newseg3():
    linseg3.setList([(0,bindex3.get()),(tapsl.get(),1/(snd.getDur(False)/tapsl.get())+bindex3.get())])
    
def newseg4():
    linseg4.setList([(0,bindex4.get()),(tapsl.get(),1/(snd.getDur(False)/tapsl.get())+bindex4.get())])
    
def newtaps():
    beat1.setTaps(value)
    beat2.setTaps(value)
    beat3.setTaps(value)
    beat4.setTaps(value)
    
def newdist1(value):
    # w1 = int(value)
    if value <= 50:
        w2 = int(value*2)
    else:
        w2 = int((100-value)*2)
    w3 = int(100-value)
        
    beat1.setW1(w1)
    beat1.setW2(w2)
    beat1.setW3(w3)
    
def newdist2(value):
    # w1 = int(value)
    if value <= 50:
        w2 = int(value*2)
    else:
        w2 = int((100-value)*2)
    w3 = int(100-value)
    
    beat2.setW1(w1)
    beat2.setW2(w2)
    beat2.setW3(w3)
    
def newdist3(value):
    # w1 = int(value)
    if value <= 50:
        w2 = int(value*2)
    else:
        w2 = int((100-value)*2)
    w3 = int(100-value)
    
    beat3.setW1(w1)
    beat3.setW2(w2)
    beat3.setW3(w3)

def newdist4(value):
    # w1 = int(value)
    if value <= 50:
        w2 = int(value*2)
    else:
        w2 = int((100-value)*2)
    w3 = int(100-value)

    beat4.setW1(w1)
    beat4.setW2(w2)
    beat4.setW3(w3)
    
def newdist():
    taps = int(taps.get())
    if taps != last_taps:
        last_taps = taps
        newtaps(taps)
    value = int(we1.get())
    if value != last_we1:
        last_we1 = value
        newdist1(value)
    value = int(we2.get())
    if value != last_we2:
        last_we2 = value
        newdist2(value)
    value = int(we3.get())
    if value != last_we3:
        last_we3 = value
        newdist3(value)
    value = int(we4.get())
    if value != last_we4:
        last_we4 = value
        newdist4(value)

