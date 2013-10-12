"""
Spectral filter module (FFT)

Sliders under the graph:

    - Filters interpolation : Morph between the two filters
    - Dry / Wet : Mix between the original signal and the delayed signals

Dropdown menus, toggles and sliders on the bottom left:

    - Filter Range : Limits of the filter
    - FFT Size : Size of the FFT
    - FFT Envelope : Shape of the FFT
    - FFT Overlaps : Number of FFT overlaps
    - # of Voices : Number of voices played simultaneously (polyphony), only available at initialization time
    - Polyphony Spread : Pitch variation between voices (chorus), only available at initialization time
    
Graph only parameters :

    - Spectral Filter 1 : Shape of the first filter
    - Spectral Filter 2 : Shape of the second filter
    - Overall Amplitude : The amplitude curve applied on the total duration of the performance
"""

# User Interface
defineUI(id=1, name="env", label="Amplitude", unit="x", init=.8)
# cgraph(name="filter_table_1", label="Spectral Filter 1", table=True, size=8192, func=[(0,0),(0.05,1),(0.1,0),(0.2,0),(0.3,.7),(0.4,0),(0.5,0),(0.6,.5),(0.7,0),(1,0)], col="green"),
# cgraph(name="filter_table_2", label="Spectral Filter 2", table=True, size=8192, func=[(0,0),(0.02,1),(0.07,0),(0.25,0),(0.35,.7),(0.5,0),(0.65,0),(0.75,.5),(0.9,0),(1,0)], col="forestgreen"),
defineUI(id=2, name="interpol", label="FiltInterpolation", min=0, max=1, init=0, rel="lin", unit="x", col="olivegreen")
defineUI(id=3, name="mix", label="Dry/Wet", min=0, max=1, init=1, rel="lin", unit="x", col="blue")
defineUI(id=4, name="filter_range", func="filter_rangefunc", label="FilterRange", init="Up to Nyquist/2", value=["Up to Nyquist", "Up to Nyquist/2", "Up to Nyquist/4", "Up to Nyquist/8"], col="green")
defineUI(id=5, name="fftsize", func="fftsizefunc", label="FFTSize", init="1024", value=["16", "32", "64", "128", "256", "512", "1024", "2048", "4096", "8192"], col="red")
defineUI(id=6, name="wtype", func="wtypefunc", label="FFTEnvelope", init="Hanning", col="red", value=["Rectangular", "Hamming", "Hanning", "Bartlett", "Blackman 3", "Blackman 4", "Blackman 7", "Tuckey", "Sine"])
defineUI(id=7, name="overlaps", func="overlapsfunc", label="FFTOverlaps", rate="i", init="4", value=["1", "2", "4", "8", "16"])


# DSP
filter_table_1 = DataTable(10, [(0,0),(0.05,1),(0.1,0),(0.2,0),(0.3,.7),(0.4,0),(0.5,0),(0.6,.5),(0.7,0),(1,0)])
filter_table_2 = DataTable(10, [(0,0),(0.02,1),(0.07,0),(0.25,0),(0.35,.7),(0.5,0),(0.65,0),(0.75,.5),(0.9,0),(1,0)])

snd = stereoIn

size = int(fftsize_value)
olaps = 4
oneOverSr = 1.0 / sr
frange_bounds = {0: 2, 1: 4, 2: 8, 3:16}

delsrc = Delay(snd, delay=size*oneOverSr*2)

filter = NewTable(8192./sr)
interpolation = TableMorph(interpol, filter, [filter_table_1, filter_table_2])

fin = FFT(snd, size=size, overlaps=olaps)

frange_bound = frange_bounds[filter_range_index]
index = Scale(fin["bin"], 0, size, 0, frange_bound, 1)
amp = Pointer(filter, Clip(index, 0, 1))

real = fin["real"] * amp
imag = fin["imag"] * amp

fout = IFFT(real, imag, size=size, overlaps=olaps)
ffout = fout.mix(nchnls)
fade = SigTo(value=1, time=.05, init=1)
out = Interp(delsrc*env, ffout*env, mix, mul=fade).out()



def fftsizefunc():
    newsize = int(fftsize.get())
    fade.value = 0
    time.sleep(.05)
    delsrc.delay = newsize*oneOverSr*2
    fin.size = newsize
    fout.size = newsize
    index.inmax = newsize
    time.sleep(.05)
    fade.value = 1

def wtypefunc():
    fin.wintype = int(wtype.get())
    fout.wintype = int(wtype.get())
        
def overlapsfunc():
    olaps = int(overlaps.get())
    size = int(fftsize.get())
    wintype = int(wtype.get())
    fin = FFT(snd, size=size, overlaps=olaps, wintype=wintype)
    fout = IFFT(real, imag, size=size, overlaps=olaps, wintype=wintype)
    foutTmp = fout.mix(nchnls)
    

def filter_rangefunc():
    index.outmax = frange_bounds[index]