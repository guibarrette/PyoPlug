# Need to get orderval to work

"""
Convolution brickwall lowpass/highpass filter.

"""

# User Interface
defineUI(id=1, name="env", label="Amplitude", unit="x", init=.8)
defineUI(id=2, name="freq", label="CutoffFreq", min=20, max=18000, init=1000, rel="log", unit="Hz", col="green")
defineUI(id=3, name="bw", label="Bandwidth", min=20, max=18000, init=1000, rel="log", unit="Hz", col="green")
defineUI(id=4, name="orderval", func="order", label="FiltOrder", min=32, max=1024, init=256, res="int", rel="lin", up=True, col="grey")
defineUI(id=5, name="typeval", func="type", label="LabelType", value=["Lowpass", "Highpass","BandStop","BandPass"], init="Lowpass", col="green")
defineUI(id=6, name="balance", func="balancefunc", label="Balance", init= "Off", col="blue", value=["Off","Compress", "Source"])

# DSP
snd = stereoIn
deg = IRWinSinc(snd, freq=freq, bw=bw, type=0, order=256, mul=env)

#BALANCE
osc = Sine(10000, mul=.1)
balanced = Balance(deg, osc, freq=10)
out = Interp(deg, balanced).out(chnl=[0,1])

#INIT
# balance(balance_index, balance_value)

def type():
        deg.type = int(typeval.get())

def order():
    deg = IRWinSinc(snd, freq=freq, bw=bw, type=int(typeval.get()), order=int(orderval.get()), mul=env)
    balanced.setInput(deg)

def balancefunc():
    index = int(balance.get())
    if index == 0:
       out.interp  = 0
    elif index == 1:
       out.interp  = 1
       balanced.input2 = osc
    elif index == 2:
       out.interp = 1
       balanced.input2 = snd
