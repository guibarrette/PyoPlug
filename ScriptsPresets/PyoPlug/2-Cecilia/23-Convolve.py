"""
Circular convolution filtering module

Sliders under the graph:

    - Dry / Wet : Mix between the original signal and the convoluted signal

Dropdown menus, toggles and sliders on the bottom left:

    - Size : Buffer size of the convolution
    - # of Voices : Number of voices played simultaneously (polyphony), only available at initialization time
    - Polyphony Spread : Pitch variation between voices (chorus), only available at initialization time

Graph only parameters :

    - Overall Amplitude : The amplitude curve applied on the total duration of the performance
"""



# User Interface
# cfilein(name="sndtable", label="Impulse")
defineUI(id=1, name="env", label="Amplitude", unit="x", init=.8)
defineUI(id=2, name="drywet", label="Dry/Wet", min=0, max=1, init=1, rel="lin", unit="x", col="blue")
defineUI(id=3, name="size", func="sizefunc", label="Size", init="512", col="grey", rate="i", value=["128","256","512","1024","2048"])
defineUI(id=4, name="balance", func="balancefunc", label = "Balance", init= "Off", col="blue", value=["Off","Compress", "Source"])
defineUI(id=5, name="sndidx", func="sndchoice", label="SndTable", file=True, init="ounkmaster.aif", path=os.path.join(os.path.expanduser('~'), "Library/Audio/Presets/PyoPlug/0-Sounds/"))


# DSP
snd = stereoIn
# sndtable = addFilein("sndtable")
usrPath = os.path.expanduser('~')
sndtable = SndTable(os.path.join(usrPath, "Library/Audio/Presets/PyoPlug/0-Sounds/ounkmaster.aif"))
convo = Convolve(snd, sndtable, size=512, mul=0.5)
deg = Interp(snd, convo, drywet, mul=env)

osc = Sine(10000,mul=.1)
balanced = Balance(deg, osc, freq=10)
out = Interp(deg, balanced).out(chnl=[0,1])

#INIT
# balance(balance_index, balance_value)

def sndchoice():
    sndtable.setSound(filesList5[int(sndidx.get())])
    convo.setTable(sndtable)

def sizefunc():
    # global convo
    # convo.setMul(0)
    # del convo
    convo.stop()    # Stop the processing so it's not duplicated
    # globals()['convo'] = Convolve(snd, sndtable, size=int(size.get()), mul=0.5)     # initialize a new global convo object
    global convo
    convo = Convolve(snd, sndtable, size=int(size.get()), mul=0.5)
    deg.setInput2(convo)    # set the second input to the new convolution object
    # convo.start()
    # conv.play()
    # convo.setValue(convTmp2)
    # deg = Interp(snd, convo, drywet, mul=env)
    # convo.set(size=int(size.get()))

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
