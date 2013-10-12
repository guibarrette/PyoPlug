import random
"""
Additive synthesis module

Sliders under the graph:

    - Base Frequency : Base pitch of the synthesis
    - Partials Spread : Distance between partials
    - Partials Freq Rand Amp : Amplitude of the jitter applied on the partials pitch
    - Partials Freq Rand Speed : Frequency of the jitter applied on the partials pitch
    - Partials Amp Rand Amp : Amplitude of the jitter applied on the partials amplitude
    - Partials Amp Rand Speed : Frequency of the jitter applied on the partials amplitude
    - Amplitude Factor : Spread of amplitude between partials
    - Chorus Depth : Amplitude of the chorus
    - Chorus Feedback : Amount of chorused signal fed back to the chorus
    - Chorus Dry / Wet : Mix between the original synthesis and the chorused signal

Dropdown menus, toggles and sliders on the bottom left:

    - # of Partials : Number of partials present
    - Wave Shape : Shape used for the synthesis
    - Custom Wave : Define a custom wave shape by entering amplitude values
    - # of Voices : Number of voices played simultaneously (polyphony), only available at initialization time
    - Polyphony Spread : Pitch variation between voices (chorus), only available at initialization time

Graph only parameters :

    - Overall Amplitude : The amplitude curve applied on the total duration of the performance
"""


# User Interface
defineUI(id=1, name="env", label="Amplitude", unit="x", init=.8)
defineUI(id=2, name="freq", label="BaseFrequency", min=10, max=10000, init=150, rel="log", unit="Hz", col="blue")
defineUI(id=3, name="spread", label="PartialsSpread", min=0.0001, max=4, init=0.003, rel="log", unit="x", col="red3")
defineUI(id=4, name="rndampspeedf", label=" FreqRandSpeed", min=0.0001, max=100, init=1, rel="log", unit="Hz", col="blue3",half=True)
defineUI(id=5, name="rndampspeed", label=" AmpRandSpeed", min=0.0001, max=20, init=1, rel="log", unit="Hz", col="green3",half=True)
defineUI(id=6, name="rndampf", label=" FreqRandAmp", min=0.0001, max=1, init=0.02, rel="log", unit="x", col="blue3",half=True)
defineUI(id=7, name="rndamp", label=" AmpRandAmp", min=0.0001, max=1, init=0.01, rel="log", unit="x", col="green3",half=True)
defineUI(id=8, name="ampfactor", label="AmpFactor", min=0.5, max=1, init=0.85, rel="lin", unit="x", col="green")
defineUI(id=9, name="num", func="numpartial", label="#ofPartials", init="20", col="grey", rate="i", value=["5","10","20","40","80","160","320","640"])
defineUI(id=10, name="shape", func="shapefunc", label="Wave Shape", init="Square", col="green", value=["Sine","Sawtooth","Square","Complex1", "Complex2", "Complex3"])
# defineUI(id=10, name="shape", func="shapefunc", label="Wave Shape", init="Square", col="green", value=["Sine","Sawtooth","Square","Complex1", "Complex2", "Complex3", "Custom"])
# cgen(name="custom", label="Custom Wave", init=[1,0,0.5,0.3,0,0,0.2,0,0.1,0,0.09,0,0.05], popup=("shape", 6), col="forestgreen")


# DSP
# customtable = custom_value
number_of_voices = 8
polyphony = .7
wavetable = HarmTable(size=8192)
polyfreqs = [random.uniform(1.0-polyphony, 1.0+polyphony) for i in range(number_of_voices*2)]
ply = [i*freq for i in polyfreqs]
out = OscBank(table=wavetable, freq=ply, spread=spread, slope=ampfactor, fjit=True, frndf=rndampspeedf, frnda=rndampf, arndf=rndampspeed, arnda=rndamp, num=20, mul=env).out(chnl=[0,1])

#INIT
wavedict = {'Sine':[1], 'Sawtooth':[1, 0.5, 0.333, 0.25, 0.2, 0.167, 0.143, 0.111, 0.1], 'Square':[1, 0, 0.333, 0, 0.2, 0, 0.143, 0, 0.111],
                    'Complex1':[1, 0, 0, 0, 0.3, 0, 0, 0, 0.2, 0, 0, 0.05], 'Complex2':[1, 0, 0, 0.3, 0, 0, 0.2, 0, 0, 0, 0, 0.1, 0, 0, 0.05, 0, 0, 0.02],
                    'Complex3':[1, 0, 0, 0.2, 0, 0.1, 0, 0, 0, 0.3, 0, 0.1, 0, 0, 0.05, 0, 0, 0.1, 0, 0.05, 0, 0, 0, 0.05, 0, 0, 0.02]}
                    # 'Custom':customtable}

# shape(shape_index, shape_value)

def shapefunc():
    wavetable.replace(wavedict.values()[int(shape.get())])

def numpartial():
    out.stop()
    global out
    out = OscBank(table=wavetable, freq=ply, spread=spread, slope=ampfactor, fjit=True, frndf=rndampspeedf, frnda=rndampf, arndf=rndampspeed, arnda=rndamp, num=int(num.get()), mul=env).out()

# def custom(self, value):
#     customtable = value

