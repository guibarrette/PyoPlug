"""
Stereo delay module with jitter control

Sliders under the graph:

    - Delay Left : Delay time of first delay
    - Delay Right : Delay time of second delay
    - AmpModDepth Left : Range of the amplitude jitter for the first delay
    - AmpModDepth Right : Range of the amplitude jitter for the second delay
    - AmpModFreq Left : Speed of the amplitude jitter for the first delay
    - AmpModFreq Right : Speed of the amplitude jitter for the second delay
    - DelayModDepth Left : Range of the delay time jitter for the first delay
    - DelayModDepth Right : Range of the delay time jitter for the second delay
    - DelayModFreq Left : Speed of the delay time jitter for the first delay
    - DelayModFreq Right : Speed of the delay time jitter for the second delay
    - Feedback : Amount of delayed signal fed back in the delay chain
    - Dry / Wet : Mix between the original signal and the delayed signals

Dropdown menus, toggles and sliders on the bottom left:

    - # of Voices : Number of voices played simultaneously (polyphony), only available at initialization time
    - Polyphony Spread : Pitch variation between voices (chorus), only available at initialization time
    
Graph only parameters :

    - Overall Amplitude : The amplitude curve applied on the total duration of the performance
"""

# User Interface
defineUI(id=1, name="env", label="Amplitude", unit="x", init=.8)
defineUI(id=2, name="dell", label="DelayLeft", min=0.0001, max=15, init=0.5, gliss=0.1, rel="log", unit="sec", half=True, col="green")
defineUI(id=3, name="delr", label="DelayRight", min=0.0001, max=15, init=1, gliss=0.1, rel="log", unit="sec", half=True, col="green")
defineUI(id=4, name="jitampl", label="AmpModDepthL", min=0.001, max=1, init=0.5, rel="log", unit="x", half=True, col="blue")
defineUI(id=5, name="jitampr", label="AmpModDepthR", min=0.001, max=1, init=0.5, rel="log", unit="x", half=True, col="red2")
defineUI(id=6, name="jitampspeedl", label="AmpModFreqL", min=0.001, max=200, init=1, rel="log", unit="Hz", half=True, col="blue")
defineUI(id=7, name="jitampspeedr", label="AmpModFreqR", min=0.001, max=200, init=1.1, rel="log", unit="Hz", half=True, col="red2")
defineUI(id=8, name="jittimel", label="DelModDepthL", min=0.001, max=1, init=0.5, rel="log", unit="x", half=True, col="blue3")
defineUI(id=9, name="jittimer", label="DelModDepthR", min=0.001, max=1, init=0.5, rel="log", unit="x", half=True, col="red4")
defineUI(id=10, name="jittimespeedl", label="DelModFreqL", min=0.001, max=200, init=1, rel="log", unit="Hz", half=True, col="blue3")
defineUI(id=11, name="jittimespeedr", label="DelModFreqR", min=0.001, max=200, init=1.1, rel="log", unit="Hz", half=True, col="red4")
defineUI(id=12, name="fb", label="Feedback", min=0, max=0.999, init=0.8, rel="lin", unit="x", col="forestgreen")
defineUI(id=13, name="drywet", label="Dry/Wet", min=0, max=1, init=1, rel="lin", unit="x", col="blue")


# DSP
### Amplitude and Delay modulations are not correctly handled...
snd = stereoIn
jitl = Randi(min=1-jitampl, max=1+jitampl, freq=jitampspeedl)
jitr = Randi(min=1-jitampr, max=1+jitampr, freq=jitampspeedr)
jittl = Randi(min=1-jittimel, max=1+jittimel, freq=jittimespeedl)
jittr = Randi(min=1-jittimer, max=1+jittimer, freq=jittimespeedr)
delay = Delay(snd, delay=[dell*jittl,delr*jittr], feedback=fb, maxdelay=15, mul=[jitl,jitr])
out = Interp(snd, delay, drywet, mul=env*0.5).out(chnl=[0,1])

