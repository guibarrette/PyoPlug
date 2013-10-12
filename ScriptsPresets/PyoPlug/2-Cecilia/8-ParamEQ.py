"""
Parametric equalization module

Sliders:

    - Overall Amplitude : The amplitude curve applied on the total duration of the performance
    - Freq 1 : Center frequency of the first EQ
    - Freq 1 Q : Q factor of the first EQ
    - Freq 1 Boost/Cut : Gain of the first EQ
    - Freq 2 : Center frequency of the second EQ
    - Freq 2 Q : Q factor of the second EQ
    - Freq 2 Boost/Cut : Gain of the second EQ
    - Freq 3 : Center frequency of the third EQ
    - Freq 3 Q : Q factor of the third EQ
    - Freq 3 Boost/Cut : Gain of the third EQ
    - Freq 4 : Center frequency of the fourth EQ
    - Freq 5 Q : Q factor of the fourth EQ
    - Freq 5 Boost/Cut : Gain of the fourth EQ
    
    - EQ Type 1 : EQ type of the first EQ
    - EQ Type 2 : EQ type of the second EQ
    - EQ Type 3 : EQ type of the third EQ
    - EQ Type 4 : EQ type of the fourth EQ
    - # of Voices : Number of voices played simultaneously (polyphony), only available at initialization time
    - Polyphony Spread : Pitch variation between voices (chorus), only available at initialization time
    
"""

# User Interface
defineUI(id=1, name="env", label="Amplitude", unit="x", init=.8)
defineUI(id=2, name="freq1gain", label="Freq1Boost/Cut", min=-48, max=24, init=-3, rel="lin", unit="dB", col="khaki"),
defineUI(id=3, name="freq1", label="Freq 1", min=1, max=20000, init=500, rel="log", unit="Hz", col="khaki", half=True),
defineUI(id=4, name="freq1q", label="Freq 1 Q", min=0.5, max=10, init=0.707, rel="lin", unit="x", col="khaki",half=True),
defineUI(id=5, name="freq2gain", label="Freq2Boost/Cut", min=-48, max=24, init=-3, rel="lin", unit="dB", col="red"),
defineUI(id=6, name="freq2", label="Freq 2", min=1, max=20000, init=1000, rel="log", unit="Hz", col="red", half=True),
defineUI(id=7, name="freq2q", label="Freq 2 Q", min=0.5, max=10, init=0.707, rel="lin", unit="x", col="red", half=True),
defineUI(id=8, name="freq3gain", label="Freq3Boost/Cut", min=-48, max=24, init=-3, rel="lin", unit="dB", col="blue1"),
defineUI(id=9, name="freq3", label="Freq 3", min=1, max=20000, init=1500, rel="log", unit="Hz", col="blue1", half=True),
defineUI(id=10, name="freq3q", label="Freq 3 Q", min=0.5, max=10, init=0.707, rel="lin", unit="x", col="blue1", half=True),
defineUI(id=11, name="freq4gain", label="Freq4Boost/Cut", min=-48, max=24, init=-3, rel="lin", unit="dB", col="green1"),
defineUI(id=12, name="freq4", label="Freq 4", min=1, max=20000, init=2000, rel="log", unit="Hz", col="green1", half=True),
defineUI(id=13, name="freq4q", label="Freq 4 Q", min=0.5, max=10, init=0.707, rel="lin", unit="x", col="green1", half=True),
defineUI(id=14, name="eq1typeval", func="eq1type", label="EQ1Type", init="Lowshelf", col="khaki", value=["Peak/Notch", "Lowshelf", "Highshelf"]),
defineUI(id=15, name="eq2typeval", func="eq2type", label="EQ2Type", init="Peak/Notch", col="red", value=["Peak/Notch", "Lowshelf", "Highshelf"]),
defineUI(id=16, name="eq3typeval", func="eq3type", label="EQ3Type", init="Peak/Notch", col="blue1", value=["Peak/Notch", "Lowshelf", "Highshelf"]),
defineUI(id=17, name="eq4typeval", func="eq4type", label="EQ4Type", init="Highshelf", col="green1", value=["Peak/Notch", "Lowshelf", "Highshelf"]),
defineUI(id=18, name="balance", func="balancefunc", label = "Balance", init= "Off", col="blue", value=["Off","Compress", "Source"])


# DSP
snd = stereoIn
eq1 = EQ(snd, freq=freq1, q=freq1q, boost=freq1gain, type=1)
eq2 = EQ(eq1, freq=freq2, q=freq2q, boost=freq2gain, type=0)
eq3 = EQ(eq2, freq=freq3, q=freq3q, boost=freq3gain, type=0)
eq4 = EQ(eq3, freq=freq4, q=freq4q, boost=freq4gain, type=2, mul=env)

osc = Sine(10000,mul=.1)
balanced = Balance(eq4, osc, freq=10)
out = Interp(eq4, balanced).out(chnl=[0,1])

#INIT
# balance(balance_index, balance_value)

def eq1type():
    eq1.type = int(eq1typeval.get())

def eq2type():
    eq2.type = int(eq2typeval.get())

def eq3type():
    eq3.type = int(eq3typeval.get())

def eq4type():
    eq4.type = int(eq4typeval.get())
      
def balancefunc():
    index = int(balance.get())
    if index == 0:
        out.interp  = 0
    elif index == 1:
        out.interp= 1
        balanced.input2 = osc
    elif index == 2:
        out.interp = 1
        balanced.input2 = snd

