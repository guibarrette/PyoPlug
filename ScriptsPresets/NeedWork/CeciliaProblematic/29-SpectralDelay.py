"""
Spectral delay module (FFT)

Sliders under the graph:

    - Bin Regions : Split points for FFT processing
    - Band 1 Delay : Delay time applied on the first band
    - Band 1 Amp : Gain of the delayed first band
    - Band 2 Delay : Delay time applied on the second band
    - Band 2 Amp : Gain of the delayed second band
    - Band 3 Delay : Delay time applied on the third band
    - Band 3 Amp : Gain of the delayed third band
    - Band 4 Delay : Delay time applied on the fourth band
    - Band 4 Amp : Gain of the delayed fourth band
    - Band 5 Delay : Delay time applied on the fifth band
    - Band 5 Amp : Gain of the delayed fifth band
    - Band 6 Delay : Delay time applied on the sixth band
    - Band 6 Amp : Gain of the delayed sixth band
    - Feedback : Amount of delayed signal fed back in the delays (band independant)
    - Dry / Wet : Mix between the original signal and the delayed signals

Dropdown menus, toggles and sliders on the bottom left:

    - FFT Size : Size of the FFT
    - FFT Envelope : Shape of the FFT
    - FFT Overlaps : Number of FFT overlaps
    - # of Voices : Number of voices played simultaneously (polyphony), only available at initialization time
    - Polyphony Spread : Pitch variation between voices (chorus), only available at initialization time
    
Graph only parameters :

    - Overall Amplitude : The amplitude curve applied on the total duration of the performance
"""

# User Interface
defineUI(id=1, name="env", label="Amplitude", unit="x", init=.8)
# csplitter(name="splitter", label="Bin regions", min=2, max=90, init=[5,15,30,50,75], num_knobs=5, res="int", rel="lin", up=True, unit="%", col="grey"),
defineUI(id=2, name="split1", func="splitter", label="Freq1Split", min=2, max=90, init=5, num_knobs=3, rel="lin", gliss=0, up=True, unit="Hz", col="grey")
defineUI(id=3, name="split2", func="splitter", label="Freq2Split", min=2, max=90, init=15, num_knobs=3, rel="lin", gliss=0, up=True, unit="Hz", col="grey")
defineUI(id=4, name="split3", func="splitter", label="Freq3Split", min=2, max=90, init=30, num_knobs=3, rel="lin", gliss=0, up=True, unit="Hz", col="grey")
defineUI(id=5, name="split4", func="splitter", label="Freq4Split", min=2, max=90, init=50, num_knobs=3, rel="lin", gliss=0, up=True, unit="Hz", col="grey")
defineUI(id=6, name="split5", func="splitter", label="Freq5Split", min=2, max=90, init=75, num_knobs=3, rel="lin", gliss=0, up=True, unit="Hz", col="grey")
defineUI(id=7, name="delay1", label="Band1Delay", min=1, max=200, init=17, res="int", rel="lin", unit="x*siz", col="red",half=True)
defineUI(id=8, name="delay1amp", label="Band1Amp", min=-90, max=18, init=0, rel="lin", unit="db", col="orange",half=True)
defineUI(id=9, name="delay2", label="Band2Delay", min=0, max=200, init=14, res="int", rel="lin", unit="x*siz", col="red",half=True)
defineUI(id=10, name="delay2amp", label="Band2Amp", min=-90, max=18, init=0, rel="lin", unit="db", col="orange",half=True)
defineUI(id=11, name="delay3", label="Band3Delay", min=0, max=200, init=11, res="int", rel="lin", unit="x*siz", col="red",half=True)
defineUI(id=12, name="delay3amp", label="Ban 3Amp", min=-90, max=18, init=0, rel="lin", unit="db", col="orange",half=True)
defineUI(id=13, name="delay4", label="Band4Delay", min=0, max=200, init=8, res="int", rel="lin", unit="x*siz", col="red",half=True)
defineUI(id=14, name="delay4amp", label="Band4Amp", min=-90, max=18, init=0, rel="lin", unit="db", col="orange",half=True)
defineUI(id=15, name="delay5", label="Band5Delay", min=0, max=200, init=5, res="int", rel="lin", unit="x*siz", col="red",half=True)
defineUI(id=16, name="delay5amp", label="Band5Amp", min=-90, max=18, init=0, rel="lin", unit="db", col="orange",half=True)
defineUI(id=17, name="delay6", label="Band6Delay", min=0, max=200, init=2, res="int", rel="lin", unit="x*siz", col="red",half=True)
defineUI(id=18, name="delay6amp", label="Band6Amp", min=-90, max=18, init=0, rel="lin", unit="db", col="orange",half=True)
defineUI(id=19, name="feed", label="Feedback", min=0, max=1, init=0.5, rel="lin", unit="x", col="green")
defineUI(id=20, name="mix", label="Dry/Wet", min=0, max=1, init=0.5, rel="lin", unit="x", col="blue")
defineUI(id=21, name="fftsize", func="fftsizefunc", label="FFTSize", init="1024", value=["16", "32", "64", "128", "256", "512", "1024", "2048", "4096", "8192"], col="red")
defineUI(id=22, name="wtype", func="wtypefunc", label="FFTEnvelope", init="Hanning", col="red", value=["Rectangular", "Hamming", "Hanning", "Bartlett", "Blackman 3", "Blackman 4", "Blackman 7", "Tuckey", "Sine"])
defineUI(id=23, name="overlaps", func="overlapsfunc", label="FFTOverlaps", rate="i", init="4", value=["1", "2", "4", "8", "16"])



# DSP
snd = stereoIn
nchnls = len(snd)

size = 1024
olaps = 1   # to make it faster to init
wintype = 2

num = olaps*nchnls # number of streams for ffts
oneOverSr = 1.0 / sr

delsrc = Delay(snd, delay=size*oneOverSr*2)

binmin, binmax = [5, 75]    # initialization

# delays conversion : number of frames -> seconds
delay_scale = (size/2) * oneOverSr
del1 = Sig(delay1, mul=delay_scale)
del2 = Sig(delay2, mul=delay_scale)
del3 = Sig(delay3, mul=delay_scale)
del4 = Sig(delay4, mul=delay_scale)
del5 = Sig(delay5, mul=delay_scale)
del6 = Sig(delay6, mul=delay_scale)
delays = duplicate([del1,del2,del3,del4,del5,del6], num)
amps = duplicate([DBToA(delay1amp),DBToA(delay2amp),DBToA(delay3amp), DBToA(delay4amp),DBToA(delay5amp),DBToA(delay6amp)], num)

snd2 = Sig(value=snd, mul=0.5)
fin = FFT(snd2, size=size, overlaps=olaps, wintype=wintype)
# fin = Sig(finTmp)

# splits regions between `binmins` and `binmaxs`
bins = Between(fin["bin"], min=binmin, max=binmax)
swre = fin["real"] * bins
swim = fin["imag"] * bins
# apply delays with mix to match `num` audio streams
delre = Delay(swre, delay=delays, feedback=feed, maxdelay=20, mul=amps).mix(num)
delim = Delay(swim, delay=delays, feedback=feed, maxdelay=20, mul=amps).mix(num)

fout = IFFT(delre, delim, size=size, overlaps=olaps, wintype=wintype)
foutTmp = fout.mix(nchnls)
ffout = Sig(foutTmp)
fade = SigTo(value=1, time=.05, init=1)
out = Interp(delsrc*env, ffout*env, mix, mul=fade).out()


# Before because we need to set variables directly at the initialization of the script
def getBinRegions():
    binscl = [split1.get(), split2.get(), split3.get(), split4.get(), split5.get()]
    binmin = [x for x in binscl]
    binmin.insert(0, 0.0)
    binmax = [x for x in binscl]
    binmax.append(100.0)
    binmin = duplicate([int(x * 0.01 * size / 2) for x in binmin], num)
    binmax = duplicate([int(x * 0.01 * size / 2) for x in binmax], num)
    return binmin, binmax
    
def splitter():
    binmin, binmax = getBinRegions()
    bins.min = binmin
    bins.max = binmax

def fftsizefunc():
    newsize = int(fftsize.get())
    delay_scale = (size/2) * oneOverSr
    fade.value = 0
    time.sleep(.05)
    delsrc.delay = size*oneOverSr*2
    del1.mul = delay_scale
    del2.mul = delay_scale
    del3.mul = delay_scale
    del4.mul = delay_scale
    del5.mul = delay_scale
    del6.mul = delay_scale
    delays = duplicate([del1,del2,del3,del4,del5,del6], num)
    delre.delay = delays
    delim.delay = delays
    fin.size = size
    fout.size = size
    binmin, binmax = getBinRegions()
    bins.min = binmin
    bins.max = binmax
    time.sleep(.05)
    fade.value = 1

def wtypefunc():
    wintype = int(wtype.get())
    fin.wintype = wintype
    fout.wintype = wintype
        
def overlapsfunc():
    olaps = int(overlaps.get())
    size = int(fftsize.get())
    wintype = int(wtype.get())
    num = olaps*nchnls # number of streams for ffts
    delays = duplicate([del1,del2,del3,del4,del5,del6], num)
    amps = duplicate([DBToA(delay1amp),DBToA(delay2amp),DBToA(delay3amp), DBToA(delay4amp),DBToA(delay5amp),DBToA(delay6amp)], num)
    # delre = Delay(swre, delay=delays, feedback=feed, maxdelay=20, mul=amps).mix(num)
    # delim = Delay(swim, delay=delays, feedback=feed, maxdelay=20, mul=amps).mix(num)
    fin = FFT(snd2, size=size, overlaps=olaps, wintype=wintype)
    bins.setInput(fin)
    swre = fin["real"] * bins
    swim = fin["imag"] * bins
    delre.setInput(swre)
    delim.setInput(swim)
    delre.delay = delays
    delre.mul = amps
    delim.delay = delays
    delim.mul = amps
    fout = IFFT(delre, delim, size=size, overlaps=olaps, wintype=wintype)
    foutTmp = fout.mix(nchnls)
    ffout.setValue(foutTmp)
