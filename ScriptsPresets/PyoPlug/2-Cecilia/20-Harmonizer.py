"""
2 voices harmonizer module

Sliders:

    - Overall Amplitude : The amplitude curve applied on the total duration of the performance
    - Transpo Voice 1 : Pitch shift of the first voice
    - Transpo Voice 2 : Pitch shift of the second voice
    - Feedback : Amount of transposed signal fed back into the harmonizers (feedback is voice independent)
    - Dry / Wet : Mix between the original signal and the harmonized signals

    - Win Size Voice 1 : Window size of the first harmonizer (delay)
    - Win Size Voice 2 : Window size of the second harmonizer (delay)

"""

# User Interface
defineUI(id=1, name="env", label="Amplitude", unit="x", init=.8)
defineUI(id=2, name="transp1", label="TranspoVoice1", min=-36, max=36, init=-7, rel="lin", unit="semi", col="red")
defineUI(id=3, name="transp2", label="TranspoVoice2", min=-36, max=36, init=3, rel="lin", unit="semi", col="red")
defineUI(id=4, name="fb", label="Feedback", min=0, max=0.999, init=0, rel="lin", unit="x", col="orange")
defineUI(id=5, name="mix", label="Harm1/Harm2", min=0, max=1, init=.5, rel="lin", unit="x", col="green")
defineUI(id=6, name="drywet", label="Dry / Wet", min=0, max=1, init=1, rel="lin", unit="x", col="blue")
defineUI(id=7, name="winsize", func="winsizefunc", label="WinSizeVoice1", init="0.1", col="chorusyellow", value=["0.025","0.05","0.1","0.15","0.2","0.25","0.5","0.75","1"])
defineUI(id=8, name="winsize2", func="winsize2func", label="WinSizeVoice2", init="0.1", col="chorusyellow", value=["0.025","0.05","0.1","0.15","0.2","0.25","0.5","0.75","1","Voice 1 + 0.01"])


# DSP
snd = stereoIn
harm1 = Harmonizer(input=snd, transpo=transp1, feedback=fb, winsize=0.1, mul=.5)
harm2 = Harmonizer(input=snd, transpo=transp2, feedback=fb, winsize=0.1, mul=.5)
harms = harm2*mix + harm1*(1-mix)
dcb = DCBlock(harms)
out = Interp(snd, dcb, drywet, mul=env).out(chnl=[0,1])   

def winsizefunc():
    harm1.winsize = winsize.get()

def winsize2func():
    if index == 9:
        harm2.winsize = winsize.get()+0.01
    else:
        harm2.winsize = winsize2.get()
        
