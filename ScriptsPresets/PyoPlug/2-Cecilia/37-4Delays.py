"""
Waveterrain synthesis module

2 stereo delays with parallel or serial routing:

    - Delay 1 Right : Delay time of first delay
    - Delay 1 Left : Delay time of second delay
    - Delay 1 Feedback : Amount of delayed signal fed back to the delay
    - Delay 1 Mix : Gain of the delayed signal
    - Delay 2 Right : Delay time of third delay
    - Delay 2 Left : Delay time of fourth delay
    - Delay 2 Feedback : Amount of delayed signal fed back to the delay
    - Delay 2 Mix : Gain of the delayed signal
    - Jitter Amp : Amplitude of the jitter applied on the delays amplitudes
    - Jitter Speed : Speed of the jitter applied on the delays amplitudes
    - Filter Freq : Center frequency of the filter
    - Filter Q : Q factor of the filter
    - Dry / Wet : Mix between the original signal and the processed signals

Dropdown menus, toggles and sliders on the bottom left:

    - Delay Routing : Type of routing
    - Filter Type : Type of filter
    - # of Voices : Number of voices played simultaneously (polyphony), only available at initialization time
    - Polyphony Spread : Pitch variation between voices (chorus), only available at initialization time

Graph only parameters :

    - Overall Amplitude : The amplitude curve applied on the total duration of the performance
"""

# User Interface
defineUI(id=1, name="env", label="Amplitude", unit="x", init=.8)
defineUI(id=2, name="del1l", label="Del1Left", min=0.0001, max=10, init=0.26, gliss=0.1, rel="log", unit="sec", half=True, col="blue")
defineUI(id=3, name="del2l", label="Del2Left", min=0.0001, max=10, init=0.16, gliss=0.1, rel="log", unit="sec", half=True, col="green")
defineUI(id=4, name="del1r", label="Del1Right", min=0.0001, max=10, gliss=0.1, init=0.25, rel="log", unit="sec", half=True, col="blue")
defineUI(id=5, name="del2r", label="Del2Right", min=0.0001, max=10, init=0.15, gliss=0.1, rel="log", unit="sec", half=True, col="green")
defineUI(id=6, name="del1f", label="Del1Feedback", min=0, max=0.999, init=0.5, rel="lin", unit="x", half=True, col="blue")
defineUI(id=7, name="del2f", label="Del2Feedback", min=0, max=0.999, init=0.5, rel="lin", unit="x", half=True, col="green")
defineUI(id=8, name="del1m", label="Del1Mix", min=-48, max=18, init=0, rel="lin", unit="dB", half=True, col="blue")
defineUI(id=9, name="del2m", label="Del2Mix", min=-48, max=18, init=0, rel="lin", unit="dB", half=True, col="green")
defineUI(id=10, name="jitamp", label="JitterAmp", min=0.0001, max=1, init=0.1, rel="log", unit="x", col="red2", half=True)
defineUI(id=11, name="jitspeed", label="JitterSpeed", min=0.0001, max=50, init=0.03, rel="log", unit="Hz", col="red2", half=True)
defineUI(id=12, name="filter", label="FiltFreq", min=30, max=20000, init=15000, rel="log", unit="Hz", col="tan")
defineUI(id=13, name="filterq", label="FiltQ", min=0.5, max=10, init=0.707, rel="log", unit="Q", col="tan")
defineUI(id=14, name="drywet", label="Dry / Wet", min=0, max=1, init=1, rel="lin", unit="x", col="blue")
defineUI(id=15, name="routing", func="routingfunc", label="DelRouting", init="Parallel", col="purple1", value=["Serial","Parallel"])
defineUI(id=16, name="filttype", func="filttypefunc", label="FiltType", init="Lowpass", col="chorusyellow", value=["Lowpass","Highpass","Bandpass","Bandstop"])
defineUI(id=17, name="filtrouting", func="filtroutingfunc", label="FiltRouting", init="Pre", col="chorusyellow", value=["Pre","Post"])
defineUI(id=18, name="balance", func="balancefunc", label = "Balance", init= "Off", col="blue", value=["Off","Compress", "Source"])


# DSP
snd = stereoIn
prefilt = Biquadx(snd, freq=filter, q=filterq, type=0, stages=2, mul=0.25)
filtChoice = SigTo(0, time=0.1, init=0)
toDelays = Interp(prefilt, snd, interp=filtChoice)
jit1 = Randi(min=1-jitamp, max=1+jitamp, freq=jitspeed)
jit2 = Randi(min=1-jitamp, max=1+jitamp, freq=jitspeed)
jit3 = Randi(min=1-jitamp, max=1+jitamp, freq=jitspeed)
jit4 = Randi(min=1-jitamp, max=1+jitamp, freq=jitspeed)
amp1 = DBToA(del1m)
amp2 = DBToA(del2m)
delay1 = Delay(toDelays, delay=[del1l*jit1,del1r*jit2], feedback=del1f, maxdelay=10, mul=amp1)
delay2 = Delay(toDelays, delay=[del2l*jit3,del2r*jit4], feedback=del2f, maxdelay=10, mul=amp2)
dels = delay1+delay2
postfilt = Biquadx(dels, freq=filter, q=filterq, type=0, stages=2, mul=0.25)
toOuts = Interp(dels, postfilt, interp=filtChoice)
deg = Interp(snd, toOuts, drywet, mul=env)

osc = Sine(10000,mul=.1)
balanced = Balance(deg, osc, freq=10)
out = Interp(deg, balanced).out(chnl=[0,1])

#INIT
# balance(balance_index, balance_value)
# routing(routing_index, routing_value)
# filtrouting(filtrouting_index, filtrouting_value)

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

def filttypefunc():
    prefilt.type = int(filttype.get())
    postfilt.type = int(filttype.get())

def routingfunc():
    if int(routing.get()) == 0:
        delay2.setInput(delay1, 0.1)
        postfilt.setInput(delay2, 0.1)
    else:
        delay2.setInput(toDelays, 0.1)
        postfilt.setInput(dels, 0.1)

def filtroutingfunc():
    filtChoice.value = int(filtrouting.get())
            

