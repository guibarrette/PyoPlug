"""
Ranged filter module using lowpass and highpass filters

Sliders:

    - Overall Amplitude : The amplitude curve applied on the total duration of the performance
    - Filter Limits : Range of the filter (min = lowpass, max = highpass)

    - Number of Stages : Amount of stacked biquad filters
    - # of Voices : Number of voices played simultaneously (polyphony), only available at initialization time
    - Polyphony Spread : Pitch variation between voices (chorus), only available at initialization time

"""

# User Interface
defineUI(id=1, name="env", label="Amplitude", unit="x", init=.8)
defineUI(id=2, name="fultrangehp", label="Filt1LimitsHp", min=20, max=20000, init=100, rel="log", unit="Hz", col="green")
defineUI(id=2, name="fultrangelp", label="Filt1LimitsLp", min=20, max=20000, init=200, rel="log", unit="Hz", col="green")
defineUI(id=3, name="filtrangeCAChp", label="Filt2Limits1Hp", min=20, max=20000, init=1000, rel="log", unit="Hz", col="green")
defineUI(id=3, name="filtrangeCAClp", label="Filt2Limits2Lp", min=20, max=20000, init=2000, rel="log", unit="Hz", col="green")
defineUI(id=4, name="mix", label = "Mix", min=0,max=1,init=0.5,rel="lin", unit="%",col="orange")
defineUI(id=5, name="filtnum", func="filtnumfunc", label="NbrOfStages", init="4", col="orange", value=["1","2","3","4","5","6"])
defineUI(id=6, name="balance", func="balancefunc", label = "Balance", init= "Off", col="blue", value=["Off","Compress", "Source"])


# DSP
snd = stereoIn

lp = Biquadx(input=snd, freq=fultrangelp, q=1, type=0, stages=4, mul=1)
hp = Biquadx(input=lp, freq=fultrangehp, q=1, type=1, stages=4, mul=0.5*env)

lp2 = Biquadx(input=snd, freq=filtrangeCAClp, q=1, type=0, stages=4, mul=1)
hp2 = Biquadx(input=lp2, freq=filtrangeCAChp, q=1, type=1, stages=4, mul=0.5*env)

#BALANCE                
osc = Sine(10000,mul=.1)
balanced1 = Balance(hp, osc, freq=10)
balanced2 = Balance(hp2, osc, freq=10)
out1 = Interp(hp, balanced1)
out2 = Interp(hp2, balanced2)
out = (out1*mix + out2*(1.0-mix)) * 0.5
out.out(chnl=[0,1])

#INIT
# balance(balance_index, balance_value)

def filtnumfunc():
    value = filtnum.get()
    lp.stages = int(value)
    hp.stages = int(value)
    lp2.stages = int(value)
    hp2.stages = int(value)

def balancefunc():
    index = int(balance.get())
    if index == 0:
        out1.interp = 0
        out2.interp = 0
    elif index ==1:
        out1.interp = 1
        out2.interp = 1
        balanced1.input2 = osc
        balanced2.input2 = osc
    elif index == 2:
        out1.interp = 1
        out2.interp = 1
        balanced1.input2 = snd
        balanced2.input2 = snd
