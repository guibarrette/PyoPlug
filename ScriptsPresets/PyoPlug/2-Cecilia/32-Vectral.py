"""
Vectral module (FFT)

Sliders under the graph:

    - Gate Threshold : dB value at which the gate becomes active
    - Gate Attenuation : Gain in dB of the gated signal
    - Upward Time Factor : Filter coefficient for increasing bins
    - Downward Time Factor : Filter coefficient for decreasing bins
    - Phase Time Factor : Phase blur
    - High Freq Damping : High frequencies damping factor
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
defineUI(id=1, name="gthresh", label="Gate Threshold", min=-120, max=0, init=-30, rel="lin", unit="db", col="red")
defineUI(id=1, name="gatt", label="Gate Attenuation", min=-120, max=0, init=-120, rel="lin", unit="db", col="red")
defineUI(id=1, name="upfac", label="Upward Time Factor", min=0, max=1, init=0.5, rel="lin", unit="x", col="orange")
defineUI(id=1, name="downfac", label="Downward Time Factor", min=0, max=1, init=0.3, rel="lin", unit="x", col="orange")
defineUI(id=1, name="anglefac", label="Phase Time Factor", min=0, max=1, init=0.1, rel="lin", unit="x", col="orange")
defineUI(id=1, name="damp", label="High Freq Damping", min=0, max=1, init=0.9, rel="lin", unit="x", col="green")
defineUI(id=1, name="mix", label="Dry / Wet", min=0, max=1, init=1, rel="lin", unit="x", col="blue")
defineUI(id=4, name="fftsize", func="fftsizefunc", label="FFTSize", init="1024", value=["16", "32", "64", "128", "256", "512", "1024", "2048", "4096", "8192"], col="red")
defineUI(id=5, name="wtype", func="wtypefunc", label="FFTEnvelope", init="Hanning", col="red", value=["Rectangular", "Hamming", "Hanning", "Bartlett", "Blackman 3", "Blackman 4", "Blackman 7", "Tuckey", "Sine"])
defineUI(id=6, name="overlaps", func="overlapsfunc", label="FFTOverlaps", rate="i", init="4", value=["1", "2", "4", "8", "16"])


# DSP
snd = stereoIn
nchnls = len(snd)

size = 1024
olaps = 4
wintype = 2

chnls = nchnls
num = olaps*chnls # number of streams for ffts
oneOverSr = 1.0 / sr

delsrc = Delay(snd, delay=size*oneOverSr*2)

snd2 = Sig(value=snd, mul=0.5)
fin = FFT(snd2, size=size, overlaps=olaps)

pol = CarToPol(fin["real"], fin["imag"])
amp = Compare(pol["mag"]*50, DBToA(gthresh), ">")
att = DBToA(gatt)
scl = amp * (1 - att) + att

mag = Vectral(pol["mag"]*scl, framesize=size, overlaps=olaps, down=downfac, up=upfac, damp=damp)

delta = FrameDelta(pol["ang"], framesize=size, overlaps=olaps)
ang = Vectral(delta, framesize=size, overlaps=olaps, up=anglefac, down=anglefac)
accum = FrameAccum(ang, framesize=size, overlaps=olaps)

car = PolToCar(mag, accum)

fout = IFFT(car["real"], car["imag"], size=size, overlaps=olaps)
ffout = fout.mix(chnls)
fade = SigTo(value=1, time=.05, init=1)
out = Interp(delsrc*env, ffout*env, mix, mul=fade).out(chnl=[0,1])

def fftsizefunc():
    newsize = int(fftsize.get())
    fade.value = 0
    time.sleep(.05)
    delsrc.delay = newsize*oneOverSr*2
    fin.size = newsize
    mag.framesize = newsize
    delta.framesize = newsize
    ang.framesize = newsize
    accum.framesize = newsize
    fout.size = newsize
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
    # fin = FFT(snd*0.5, size=size, overlaps=olaps, wintype=wintype)
    # fout = IFFT(car["real"], car["imag"], size=size, overlaps=olaps, wintype=wintype)

