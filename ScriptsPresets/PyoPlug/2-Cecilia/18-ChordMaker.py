"""
Sampler-based harmonizer module with multiple voices

Sliders under the graph:

    - Overall Amplitude : The amplitude curve applied on the total duration of the performance
    - Transpo Voice 1 : Pitch shift of the first voice
    - Gain Voice 1 : Gain of the transposed first voice
    - Transpo Voice 2 : Pitch shift of the second voice
    - Gain Voice 2 : Gain of the transposed second voice
    - Transpo Voice 3 : Pitch shift of the third voice
    - Gain Voice 3 : Gain of the transposed third voice
    - Transpo Voice 4 : Pitch shift of the fourth voice
    - Gain Voice 4 : Gain of the transposed fourth voice
    - Transpo Voice 5 : Pitch shift of the fifth voice
    - Gain Voice 5 : Gain of the transposed fifth voice
    - Feedback : Amount of transposed signal fed back into the harmonizers (feedback is voice independent)
    - Dry / Wet : Mix between the original signal and the harmonized signals
    
    - Voice 1 : Mute or unmute the first voice
    - Voice 2 : Mute or unmute the second voice
    - Voice 3 : Mute or unmute the third voice
    - Voice 4 : Mute or unmute the fourth voice
    - Voice 5 : Mute or unmute the fifth voice
    
"""

# User Interface
defineUI(id=1, name="env", label="Amplitude", unit="x", init=.8)
defineUI(id=2, name="transp1", label="TranspoVoice1", min=-24, max=24, init=0, rel="lin", unit="semi", col="red",half=True)
defineUI(id=3, name="gain1", label="GainVoice1", min=-48, max=18, init=0, rel="lin", unit="dB", col="green",half=True)
defineUI(id=4, name="transp2", label="TranspoVoice2", min=-24, max=24, init=3, rel="lin", unit="semi", col="red",half=True)
defineUI(id=5, name="gain2", label="GainVoice2", min=-48, max=18, init=0, rel="lin", unit="dB", col="green",half=True)
defineUI(id=6, name="transp3", label="TranspoVoice3", min=-24, max=24, init=5, rel="lin", unit="semi", col="red",half=True)
defineUI(id=7, name="gain3", label="GainVoice3", min=-48, max=18, init=0, rel="lin", unit="dB", col="green",half=True)
defineUI(id=8, name="transp4", label="TranspoVoice4", min=-24, max=24, init=-2, rel="lin", unit="semi", col="red",half=True)
defineUI(id=9, name="gain4", label="GainVoice4", min=-48, max=18, init=0, rel="lin", unit="dB", col="green",half=True)
defineUI(id=10, name="transp5", label="TranspoVoice5", min=-24, max=24, init=-4, rel="lin", unit="semi", col="red",half=True)
defineUI(id=11, name="gain5", label="GainVoice5", min=-48, max=18, init=0, rel="lin", unit="dB", col="green",half=True)
defineUI(id=12, name="fb", label="Feedback", min=0, max=0.999, init=0, rel="lin", unit="x", col="orange")
defineUI(id=13, name="drywet", label="Dry / Wet", min=0, max=1, init=1, rel="lin", unit="x", col="blue")
defineUI(id=14, name="winsize", func="winsizefunc", label="WinSize", init="0.1", col="chorusyellow", value=["0.025","0.05","0.1","0.15","0.2","0.25","0.5","0.75","1"])
defineUI(id=15, name="onoffv1", func="onoffv1func", label="Vx1-OnOff", init=1, min=0, max=1, value=["0","1"], stack=True, col="green")
defineUI(id=16, name="onoffv2", func="onoffv2func", label="Vx2-OnOff", init=1, min=0, max=1, value=["0","1"], stack=True, col="green")
defineUI(id=17, name="onoffv3", func="onoffv3func", label="Vx3-OnOff", init=1, min=0, max=1, value=["0","1"], stack=True, col="green")
defineUI(id=18, name="onoffv4", func="onoffv4func", label="Vx4-OnOff", init=1, min=0, max=1, value=["0","1"], stack=True, col="green")
defineUI(id=19, name="onoffv5", func="onoffv5func", label="Vx5-OnOff", init=1, min=0, max=1, value=["0","1"], stack=True, col="green")
defineUI(id=20, name="balance", func="balancefunc", label = "Balance", init= "Off", col="blue", value=["Off","Compress", "Source"])


# DSP
snd = stereoIn
mul1 = DBToA(gain1, mul=1)
mul2 = DBToA(gain2, mul=1)
mul3 = DBToA(gain3, mul=1)
mul4 = DBToA(gain4, mul=1)
mul5 = DBToA(gain5, mul=1)
harm1 = Harmonizer(input=snd, transpo=transp1, feedback=fb, winsize=0.1, mul=mul1*0.3)
harm2 = Harmonizer(input=snd, transpo=transp2, feedback=fb, winsize=0.1, mul=mul2*0.3)
harm3 = Harmonizer(input=snd, transpo=transp3, feedback=fb, winsize=0.1, mul=mul3*0.3)
harm4 = Harmonizer(input=snd, transpo=transp4, feedback=fb, winsize=0.1, mul=mul4*0.3)
harm5 = Harmonizer(input=snd, transpo=transp5, feedback=fb, winsize=0.1, mul=mul5*0.3)
harms = harm1+harm2+harm3+harm4+harm5
drydel = Delay(snd, delay=0.1*0.5)
deg = Interp(drydel, harms, drywet, mul=env)

osc = Sine(10000,mul=.1)
balanced = Balance(deg, osc, freq=10)
out = Interp(deg, balanced).out(chnl=[0,1])

#INIT
#balance(balance_index, balance_value)

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

def winsizefunc():
    harm1.winsize = float(winsize.get())
    harm2.winsize = float(winsize.get())
    harm3.winsize = float(winsize.get())
    harm4.winsize = float(winsize.get())
    harm5.winsize = float(winsize.get())
    drydel.delay = float(winsize.get())*0.5

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
        
