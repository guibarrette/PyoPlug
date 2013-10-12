"""
Cross synthesis module (FFT)

Sliders under the graph:

    - Exciter Pre Filter Freq : Frequency of the pre-FFT filter
    - Exciter Pre Filter Q : Q of the pre-FFT filter
    - Dry / Wet : Mix between the original signal and the processed signal

Dropdown menus, toggles and sliders on the bottom left:

    - Exc Pre Filter Type : Type of the pre-FFT filter
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
# csampler(name="snd1", label="Spectral Envelope")
# csampler(name="snd2", label="Source Exciter")
defineUI(id=2, name="prefiltf", label="ExciterPreFiltFreq", min=40, max=18000, init=150, rel="log", unit="Hz", col="green")
defineUI(id=3, name="prefiltq", label="ExciterPreFiltQ", min=.5, max=10, init=0.707, rel="log", col="green")
defineUI(id=4, name="mix", label="Dry/Wet", min=0, max=1, init=1, rel="lin", unit="x", col="blue")
defineUI(id=5, name="prefilttype", func="prefilttypefunc", label="ExcPreFiltType", init="Highpass", col="green", value=["Lowpass","Highpass","Bandpass","Bandstop"])
defineUI(id=6, name="fftsize", func="fftsizefunc", label="FFTSize", init="1024", value=["16", "32", "64", "128", "256", "512", "1024", "2048", "4096", "8192"], col="red")
defineUI(id=7, name="wtype", func="wtypefunc", label="FFTEnvelope", init="Hanning", col="red", value=["Rectangular", "Hamming", "Hanning", "Bartlett", "Blackman 3", "Blackman 4", "Blackman 7", "Tuckey", "Sine"])
defineUI(id=8, name="overlaps", func="overlapsfunc", label="FFTOverlaps", rate="i", init="4", value=["1", "2", "4", "8", "16"])
defineUI(id=9, name="snd2idx", func="snd2func", label="SoundLoaded", file=True, init="ounkmaster.aif", path=os.path.join(os.path.expanduser('~'), "Library/Audio/Presets/PyoPlug/0-Sounds/"))


# DSP
snd1 = stereoIn
# snd2 = addSampler("snd2")
usrPath = os.path.expanduser('~')
snd2 = SfPlayer(os.path.join(usrPath, "Library/Audio/Presets/PyoPlug/0-Sounds/ounkmaster.aif"), loop=True)
snd2_filt = Biquadx(snd2, freq=prefiltf, q=prefiltq, type=1, stages=2)
nchnls = len(snd1)

size = 1024
olaps = 4
wintype = 2
oneOverSr = 1.0 / sr

delsrc = Delay(snd1, delay=size*oneOverSr*2)

fin1 = FFT(snd1, size=size, overlaps=olaps, wintype=wintype)
fin2 = FFT(snd2_filt, size=size, overlaps=olaps, wintype=wintype)

# fin1 = Sig(fin1Tmp)     # to have an easy way to switch signal
# fin2 = Sig(fin2Tmp)

# get the magnitude of the first sound
mag = Sqrt(fin1["real"]*fin1["real"] + fin1["imag"]*fin1["imag"], mul=60)
# scale `real` and `imag` parts of the second sound by the magnitude of the first one
real = fin2["real"] * mag
imag = fin2["imag"] * mag

fout = IFFT(real, imag, size=size, overlaps=olaps, wintype=wintype)
# fout - Sig(foutTmp)

ffout = Sig(fout.mix(nchnls))
# ffout = Mix(fout, nchnls)
fade = SigTo(value=1, time=.03, init=1)
out = Interp(delsrc*env*0.5, ffout*env, mix, mul=fade).out(chnl=[0,1])

def snd2func():
    # global snd2
    snd2 = SfPlayer(filesList9[int(snd2idx.get())], loop=True)     # resetting the SfPlayer so it can change to a sound file of any numbers of channels
    # spec.setSound(filesList9[int(specidx.get())])
    snd2_filt.setInput(snd2)

def prefilttypefunc():
    snd2_filt.type = int(prefilttype.get())

def fftsizefunc():
    newsize = int(fftsize.get())
    fade.value = 0
    time.sleep(.05)
    delsrc.delay = newsize*oneOverSr*2
    fin1.size = newsize
    fin2.size = newsize
    fout.size = newsize
    time.sleep(.05)
    fade.value = 1

def wtypefunc():
    fin1.wintype = int(wtype.get())
    fin2.wintype = int(wtype.get())
    fout.wintype = int(wtype.get())
        
def overlapsfunc():
    olaps = int(overlaps.get())
    size = int(fftsize.get())
    wintype = int(wtype.get())
    # fin1.overlaps = olaps
    # fin2.overlaps = olaps
    # fout.overlaps = olaps
    # fin1.stop()
    # fin2.stop()
    # fout.stop()
    # global fin1, fin2, fout
    fin1 = FFT(snd1, size=size, overlaps=olaps, wintype=wintype)
    fin2 = FFT(snd2_filt, size=size, overlaps=olaps, wintype=wintype)
    # get the magnitude of the first sound
    mag = Sqrt(fin1["real"]*fin1["real"] + fin1["imag"]*fin1["imag"], mul=60)
    # scale `real` and `imag` parts of the second sound by the magnitude of the first one
    real = fin2["real"] * mag
    imag = fin2["imag"] * mag
    fout = IFFT(real, imag, size=size, overlaps=olaps, wintype=wintype)
    ffout.setValue(fout.mix(nchnls))


