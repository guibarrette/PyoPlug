"""
Morphing module (FFT)

Sliders under the graph:

    - Morph src1 <-> src2 : Morphing index between the two sources
    - Dry / Wet : Mix between the original signal and the morphed signal

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
# csampler(name="snd1", label="Source 1"),
# csampler(name="snd2", label="Source 2"),
defineUI(id=2, name="interp", label="Morph src1 <-> src2", min=0, max=1, init=0.5, rel="lin", unit="x", col="green")
defineUI(id=3, name="mix", label="Dry/Wet", min=0, max=1, init=1, rel="lin", unit="x", col="blue")
defineUI(id=4, name="fftsize", func="fftsizefunc", label="FFTSize", init="1024", value=["16", "32", "64", "128", "256", "512", "1024", "2048", "4096", "8192"], col="red")
defineUI(id=5, name="wtype", func="wtypefunc", label="FFTEnvelope", init="Hanning", col="red", value=["Rectangular", "Hamming", "Hanning", "Bartlett", "Blackman 3", "Blackman 4", "Blackman 7", "Tuckey", "Sine"])
defineUI(id=6, name="overlaps", func="overlapsfunc", label="FFTOverlaps", rate="i", init="4", value=["1", "2", "4", "8", "16"])
defineUI(id=7, name="snd2idx", func="snd2func", label="SoundLoaded", file=True, init="ounkmaster.aif", path=os.path.join(os.path.expanduser('~'), "Library/Audio/Presets/PyoPlug/0-Sounds/"))


# DSP
snd1 = stereoIn
# snd2 = addSampler("snd2", amp=.7)
usrPath = os.path.expanduser('~')
snd2Tmp = SfPlayer(os.path.join(usrPath, "Library/Audio/Presets/PyoPlug/0-Sounds/ounkmaster.aif"), loop=True)
snd2 = Sig(snd2Tmp) # To have an easy way to switch signal
nchnls = len(snd1)

size = 1024
olaps = 4
wintype = 2
oneOverSr = 1.0 / sr

delsrc = Delay(snd1, delay=size*oneOverSr*2)

fin1 = FFT(snd1, size=size, overlaps=olaps, wintype=wintype)
fin2 = FFT(snd2, size=size, overlaps=olaps, wintype=wintype)

pol1 = CarToPol(fin1["real"], fin1["imag"])
pol2 = CarToPol(fin2["real"], fin2["imag"])

mag3 = pol1["mag"] * pol2["mag"] * 200
pha3 = pol1["ang"] + pol2["ang"]

mag = Selector([pol1["mag"]*0.25, mag3, pol2["mag"]*0.25], voice=interp*2)
pha = Selector([pol1["ang"], pha3, pol2["ang"]], voice=interp*2)

# converts back to rectangular
car = PolToCar(mag, pha)

fout = IFFT(car["real"], car["imag"], size=size, overlaps=olaps, wintype=wintype)

ffoutTmmp = fout.mix(nchnls)
ffout = Sig(ffoutTmmp)
fade = SigTo(value=1, time=.05, init=1)
out = Interp(delsrc*env*0.5, ffout*env, mix, mul=fade).out()

def snd2func():
    snd2Tmp = SfPlayer(filesList7[int(snd2idx.get())], loop=True)     # resetting the SfPlayer so it can change to a sound file of any numbers of channels
    snd2.setValue(snd2Tmp)

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
    winType = int(wtype.get())
    fin1.wintype = winType
    fin2.wintype = winType
    fout.wintype = winType
        
def overlapsfunc():
    olaps = int(overlaps.get())
    size = int(fftsize.get())
    wintype = int(wtype.get())
    fin1 = FFT(snd1, size=size, overlaps=olaps, wintype=wintype)
    fin2 = FFT(snd2, size=size, overlaps=olaps, wintype=wintype)
    pol1.setInReal(fin1["real"])
    pol1.setInImag(fin1["imag"])
    pol2.setInReal(fin2["real"])
    pol2.setInImag(fin2["imag"])

    mag3 = pol1["mag"] * pol2["mag"] * 200
    pha3 = pol1["ang"] + pol2["ang"]

    mag.setInputs([pol1["mag"]*0.25, mag3, pol2["mag"]*0.25])
    pha.setInputs([pol1["ang"], pha3, pol2["ang"]])
    
    fout = IFFT(car["real"], car["imag"], size=size, overlaps=olaps, wintype=wintype)
    ffoutTmmp = fout.mix(nchnls)
    ffout.setValue(ffoutTmmp)
        


