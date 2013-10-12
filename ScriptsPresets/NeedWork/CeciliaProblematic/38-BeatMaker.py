"""
Algorithmic beatmaker module

Sliders under the graph:

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
# defineUI(id=2, name="adsr1", label="Beat1ADSR", func=[(0,0),(0.001,1),(0.122,0.25),(1,0)], table=True, col="blue")
# defineUI(id=3, name="adsr2", label="Beat2ADSR", func=[(0,0),(0.001,1),(0.122,0.25),(1,0)], table=True, col="blue")
# defineUI(id=4, name="adsr3", label="Beat3ADSR", func=[(0,0),(0.001,1),(0.122,0.25),(1,0)], table=True, col="blue")
# defineUI(id=5, name="adsr4", label="Beat4ADSR", func=[(0,0),(0.001,1),(0.122,0.25),(1,0)], table=True, col="blue")
defineUI(id=2, name="tapsval", func="newdist", label="#ofTaps", min=1, max=64, init=16, res="int", rel="lin", unit="x", col= "lightgreen")
defineUI(id=3, name="tempo", label="Tempo", min=20, max=240, gliss=0, init=120, rel="lin", unit="bpm", col="green")
defineUI(id=4, name="tapsl1", label="Beat1TapLength", min=0.1, max=1, init=0.1, rel="lin", unit="sec", col="blue",half=True)
defineUI(id=5, name="bindex1", label="Beat1Index", min=0, max=1, init=0, rel="lin", unit="x", col="olivegreen",half=True)
defineUI(id=6, name="tapsl2", label="Beat2TapLength", min=0.1, max=1, init=0.2, rel="lin", unit="sec", col="blue",half=True)
defineUI(id=7, name="bindex2", label="Beat2Index", min=0, max=1, init=0.3, rel="lin", unit="x", col="olivegreen",half=True)
defineUI(id=8, name="tapsl3", label="Beat3TapLength", min=0.1, max=1, init=0.4, rel="lin", unit="sec", col="blue",half=True)
defineUI(id=9, name="bindex3", label="Beat3Index", min=0, max=1, init=0.7, rel="lin", unit="x", col="olivegreen",half=True)
defineUI(id=10, name="tapsl4", label="Beat4TapLength", min=0.1, max=1, init=0.6, rel="lin", unit="sec", col="blue",half=True)
defineUI(id=11, name="bindex4", label="Beat4Index", min=0, max=1, init=1.0, rel="lin", unit="x", col="olivegreen",half=True)
defineUI(id=12, name="gain1", label="Beat1Gain", min=-48, max=18, init=0, rel="lin", unit="dB", col="chorusyellow",half=True)
defineUI(id=13, name="we1", label="Beat1Distribution", min=0, max=100, init=80, res="int", rel="lin", unit="%", col="red3",half=True)
defineUI(id=14, name="gain2", label="Beat2Gain", min=-48, max=18, init=0, rel="lin", unit="dB", col="chorusyellow",half=True)
defineUI(id=15, name="we2", label="Beat2Distribution", min=0, max=100, init=50, rel="lin", res="int", unit="%", col="red3",half=True)
defineUI(id=16, name="gain3", label="Beat3Gain", min=-48, max=18, init=0, rel="lin", unit="dB", col="chorusyellow",half=True)
defineUI(id=17, name="we3", label="Beat3Distribution", min=0, max=100, init=30, rel="lin", res="int", unit="%", col="red3",half=True)
defineUI(id=18, name="gain4", label="Beat4Gain", min=-48, max=18, init=0, rel="lin", unit="dB", col="chorusyellow",half=True)
defineUI(id=19, name="we4", label="Beat4Distribution", min=0, max=100, init=10, rel="lin",  res="int", unit="%", col="red3",half=True)
defineUI(id=20, name="seed", func="seed_up", label="Globalseed", min=0, max=5000, init=0, rel="lin", res="int", unit="x", up=True)
defineUI(id=21, name="sndidx", func="sndchoice", label="SndTable", file=True, init="ounkmaster.aif", path=os.path.join(os.path.expanduser('~'), "Library/Audio/Presets/PyoPlug/0-Sounds/"))

def newseg1():
    linseg1.setList([(0,bindex1.get()),(tapsl1.get(),1/(snd.getDur(False)/tapsl1.get())+bindex1.get())])

def newseg2():
    linseg2.setList([(0,bindex2.get()),(tapsl2.get(),1/(snd.getDur(False)/tapsl2.get())+bindex2.get())])

def newseg3():
    linseg3.setList([(0,bindex3.get()),(tapsl3.get(),1/(snd.getDur(False)/tapsl3.get())+bindex3.get())])

def newseg4():
    linseg4.setList([(0,bindex4.get()),(tapsl4.get(),1/(snd.getDur(False)/tapsl4.get())+bindex4.get())])

# DSP
adsr1 = DataTable(4, [(0,0),(0.001,1),(0.122,0.25),(1,0)])
adsr2 = DataTable(4, [(0,0),(0.001,1),(0.122,0.25),(1,0)])
adsr3 = DataTable(4, [(0,0),(0.001,1),(0.122,0.25),(1,0)])
adsr4 = DataTable(4, [(0,0),(0.001,1),(0.122,0.25),(1,0)])

# snd = stereoIn
# tempo = 120
usrPath = os.path.expanduser('~')
snd = SndTable(os.path.join(usrPath, "Library/Audio/Presets/PyoPlug/0-Sounds/ounkmaster.aif"))
last_we1 =last_we2 = last_we3 = last_we4 = last_taps = -1
# rtempo = 1/(tempo/15)
rtempo = 1/(120/15)
number_of_voices = 8
polyphony_spread = 0.7

# s.setGlobalSeed(0)
beat1 = Beat(time=rtempo, taps=16, w1=80, w2=40, w3=20, poly=16).play()
beat2 = Beat(time=rtempo, taps=16, w1=50, w2=100, w3=50, poly=16).play()
beat3 = Beat(time=rtempo, taps=16, w1=30, w2=60, w3=70, poly=16).play()
beat4 = Beat(time=rtempo, taps=16, w1=30, w2=60, w3=70, poly=16).play()
beat4 = Beat(time=rtempo, taps=16, w1=30, w2=60, w3=70, poly=8).play()
tre1 = TrigEnv(input=beat1, table=adsr1, dur=tapsl1, mul=beat1['amp'])
tre2 = TrigEnv(input=beat2, table=adsr2, dur=tapsl2, mul=beat2['amp'])
tre3 = TrigEnv(input=beat3, table=adsr3, dur=tapsl3, mul=beat3['amp'])
tre4 = TrigEnv(input=beat4, table=adsr4, dur=tapsl4, mul=beat4['amp'])
linseg1 = TrigLinseg(input=beat1, list=[(0,0),(0.1,1/(snd.getDur(False)/0.1)+0)])
linseg2 = TrigLinseg(input=beat2, list=[(0,0.3),(0.2,(1/(snd.getDur(False)/0.2))+0.3)])
linseg3 = TrigLinseg(input=beat3, list=[(0,0.7),(0.4,(1/(snd.getDur(False)/0.4))+0.7)])
linseg4 = TrigLinseg(input=beat4, list=[(0,1),(0.6,(1/(snd.getDur(False)/0.6))+1)])
trf1 = TrigFunc(linseg1['trig'], newseg1)
trf2 = TrigFunc(linseg2['trig'], newseg2)
trf3 = TrigFunc(linseg3['trig'], newseg3)
trf4 = TrigFunc(linseg4['trig'], newseg4)
again1 = DBToA(gain1)
again2 = DBToA(gain2)
again3 = DBToA(gain3)
again4 = DBToA(gain4)
pointer1 = Pointer(table=snd, index=linseg1, mul=tre1*again1)
pointer2 = Pointer(table=snd, index=linseg2, mul=tre2*again2)
pointer3 = Pointer(table=snd, index=linseg3, mul=tre3*again3)
pointer4 = Pointer(table=snd, index=linseg4, mul=tre4*again4)
mixx = pointer1+pointer2+pointer3+pointer4
sig = Sig(mixx, mul=env).mix(nchnls)
chorusd = Scale(input=Sig(polyphony_spread), inmin=0.0001, inmax=0.5, outmin=0, outmax=5)
chorusb = Scale(input=Sig(number_of_voices), inmin=1, inmax=10, outmin=0, outmax=1)
out = Chorus(input=sig, depth=chorusd, feedback=0.25, bal=chorusb).out()

# trigend = TrigFunc(beat1["end"], newdist)

def sndchoice():
    snd.setSound(filesList21[int(sndidx.get())])
    newseg1()
    newseg2()
    newseg3()
    newseg4()
    pointer1.setTable(snd)
    pointer2.setTable(snd)
    pointer3.setTable(snd)
    pointer4.setTable(snd)
    mixx = pointer1+pointer2+pointer3+pointer4
    sig.setValue(mixx)

def seed_up():
    # s.setGlobalSeed(int(seed.get()))
    beat1.new()
    beat2.new()
    beat3.new()
    beat4.new()

def newtaps(value):
    beat1.setTaps(value)
    beat2.setTaps(value)
    beat3.setTaps(value)
    beat4.setTaps(value)

def newdist1(value):
    # value = int(we1.get())
    w1 = value
    if value <= 50:
        w2 = value*2
    else:
        w2 = (100-value)*2
    w3 = 100-value
    
    beat1.setW1(w1)
    beat1.setW2(w2)
    beat1.setW3(w3)
    
def newdist2(value):
    # value = int(we2.get())
    w1 = value
    if value <= 50:
        w2 = value*2
    else:
        w2 = (100-value)*2
    w3 = 100-value
    
    beat2.setW1(w1)
    beat2.setW2(w2)
    beat2.setW3(w3)
    
def newdist3(value):
    # value = int(we3.get())
    if value <= 50:
        w2 = value*2
    else:
        w2 = (100-value)*2
    w3 = 100-value
    
    beat3.setW1(w1)
    beat3.setW2(w2)
    beat3.setW3(w3)
    
def newdist4(value):
    # value = int(we4.get())
    if value <= 50:
        w2 = value*2
    else:
        w2 = (100-value)*2
    w3 = 100-value
            
    beat4.setW1(w1)
    beat4.setW2(w2)
    beat4.setW3(w3)

def newdist():
    taps = int(tapsval.get())
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
