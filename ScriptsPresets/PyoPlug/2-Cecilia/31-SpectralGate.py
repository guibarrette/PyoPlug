"""
Spectral gate module (FFT)

Sliders under the graph:

    - Gate Threshold : dB value at which the gate becomes active
    - Gate Attenuation : Gain in dB of the gated signal
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
defineUI(id=2, name="gthresh", label="Gate Threshold", min=-120, max=0, init=-30, rel="lin", unit="db", col="orange")
defineUI(id=3, name="gatt", label="Gate Attenuation", min=-120, max=0, init=-120, rel="lin", unit="db", col="khaki")
defineUI(id=4, name="fftsize", func="fftsizefunc", label="FFTSize", init="1024", value=["16", "32", "64", "128", "256", "512", "1024", "2048", "4096", "8192"], col="red")
defineUI(id=5, name="wtype", func="wtypefunc", label="FFTEnvelope", init="Hanning", col="red", value=["Rectangular", "Hamming", "Hanning", "Bartlett", "Blackman 3", "Blackman 4", "Blackman 7", "Tuckey", "Sine"])
defineUI(id=6, name="overlaps", func="overlapsfunc", label="FFTOverlaps", rate="i", init="4", value=["1", "2", "4", "8", "16"])


# DSP
snd = stereoIn
nchnls = len(snd)

size = 1024
olaps = 4
wintype = 2

snd2 = Sig(value=snd, mul=0.5)
fin = FFT(snd2, size=size, overlaps=olaps, wintype=wintype)
# fin = Sig(finTmp)     # to have an easy way to switch signal

pol = CarToPol(fin["real"], fin["imag"])
amp = Compare(pol["mag"]*50, DBToA(gthresh), ">")
att = DBToA(gatt)
scl = amp * (1 - att) + att
car = PolToCar(pol["mag"]*scl, pol["ang"])

fout = IFFT(car["real"], car["imag"], size=size, overlaps=olaps, wintype=wintype)
# fout = Sig(foutTmp)
ffout = fout.mix(nchnls)
fade = SigTo(value=1, time=.05, init=1)
out = Sig(ffout*env, mul=fade).out(chnl=[0,1])


def fftsizefunc():
    newsize = int(fftsize.get())
    fade.value = 0
    time.sleep(.05)
    fin.size = newsize
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
    # fin = FFT(snd2, size=size, overlaps=olaps, wintype=wintype)
    # fout = IFFT(car["real"], car["imag"], size=size, overlaps=olaps, wintype=wintype)
