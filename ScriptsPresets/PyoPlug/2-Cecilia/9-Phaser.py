"""
Phaser effect module

Sliders under the graph:

    - Center Freq : Center frequency of the phaser
    - Q Factor : Q factor (resonance) of the phaser
    - Notch Spread : Distance between phaser notches
    - Feedback : Amount of phased signal fed back into the phaser
    - Dry / Wet : Mix between the original signal and the phased signal

Dropdown menus, toggles and sliders on the bottom left:

    - Number of Stages : Changes notches bandwidth (stacked filters)
    - # of Voices : Number of voices played simultaneously (polyphony), only available at initialization time
    - Polyphony Spread : Pitch variation between voices (chorus), only available at initialization time

Graph only parameters :

    - Overall Amplitude : The amplitude curve applied on the total duration of the performance
"""

# User Interface
defineUI(id=1, name="env", label="Amplitude", unit="x", init=.8)
defineUI(id=2, name="centerfreq", label="CenterFreq", min=20, max=20000, init=400, func=[(0,20),(1,20000)], rel="log", unit="Hz", col="blue"),
defineUI(id=3, name="fq", label="QFactor", min=0.5, max=10, init=5, rel="lin", unit="Q", col="royalblue"),
defineUI(id=4, name="spread", label="NotchSpread", min=0.01, max=1, init=1, rel="lin", unit="x", col="lightblue"),
defineUI(id=5, name="fb", label="Feedback", min=0, max=0.999, init=0.7, rel="lin", unit="x", col="green"),
defineUI(id=6, name="drywet", label="Dry / Wet", min=0, max=1, init=0.8, rel="lin", unit="x", col="blue"),
defineUI(id=7, name="stages", label="NbrOfStages", init="8", rate="i", col="grey", value=["1","2","3","4","5","6","7","8","9","10","11","12"]),

# DSP
snd = stereoIn
phaser = Phaser(input=snd, freq=centerfreq, spread=spread, q=fq, feedback=fb, num=8+1, mul=0.5)
out = Interp(snd, phaser, drywet, mul=env).out(chnl=[0,1])
    