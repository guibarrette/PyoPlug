import random
"""
Pulsar synthesis module

Sliders under the graph:

    - Base Frequency : Base pitch of the synthesis
    - Pulsar Width : Amount of silence added to one period
    - Detune Factor : Amount of jitter applied to the pitch
    - Detune Speed : Speed of the jitter applied to the pitch

Dropdown menus, toggles and sliders on the bottom left:

    - Wave Shape : Shape used for the synthesis
    - Custom Wave : Define a custom wave shape by entering amplitude values
    - Window Type : Pulsar envelope
    - # of Voices : Number of voices played simultaneously (polyphony), only available at initialization time
    - Polyphony Spread : Pitch variation between voices (chorus), only available at initialization time

Graph only parameters :

    - Overall Amplitude : The amplitude curve applied on the total duration of the performance
"""

# User Interface
defineUI(id=1, name="env", label="Amplitude", unit="x", init=.8)
defineUI(id=2, name="bfreq", label="BaseFrequency", min=0.1, max=1000, init=20, rel="log", unit="Hz", col="blue")
defineUI(id=3, name="width", label="PulsarWidth", min=0.0001, max=1, init=0.18, rel="lin", unit="x", col="lightgreen")
defineUI(id=4, name="detune", label="DetuneFactor", min=0.0001, max=0.999, init=0.005, rel="log", unit="x", col="red")
defineUI(id=5, name="detunesp", label="DetuneSpeed", min=0.0001, max=100, init=0.3, rel="log", unit="Hz", col="red")
defineUI(id=6, name="srcindex", func="srcindex_up", label="SourceIndex", min=0., max=1., init=0.5, rel="lin", unit="x", up=True, col="red")
defineUI(id=7, name="wsize", func="wsizefunc", label="WindSize", init="512", col="green1", value=["32", "64", "128", "256", "512", "1024", "2048", "4092", "8096", "16384","32768"])
defineUI(id=8, name="wtype", label="Window Type", init="Tuckey", col="chorusyellow", value=["Rectangular", "Hamming", "Hanning", "Bartlett", "Blackman 3", "Blackman 4", "Blackman 7", "Tuckey", "Sine"])
defineUI(id=9, name="sndidx", func="sndchoice", label="SndTable", file=True, init="ounkmaster.aif", path=os.path.join(os.path.expanduser('~'), "Library/Audio/Presets/PyoPlug/0-Sounds/"))


# DSP
# src = stereoIn
usrPath = os.path.expanduser('~')
src = SndTable(os.path.join(usrPath, "Library/Audio/Presets/PyoPlug/0-Sounds/ounkmaster.aif"))
nchnls = len(src)
window_size = 512
polyphony_spread = 0.7
number_of_voices = 2

index = int(0.5 * src.getSize(False))
samples = [src[i].getTable()[index:index+int(window_size)] for i in range(nchnls)]
t = DataTable(size=len(samples[0]), chnls=len(samples), init=samples)
e = WinTable(type=7, size=8192)
rnd1 = Randi(min=1-detune, max=1+detune, freq=detunesp)
rnd2 = Randi(min=1-detune, max=1+detune, freq=detunesp)
polyfreqs = [random.uniform(1.0-polyphony_spread, 1.0+polyphony_spread) for i in range(number_of_voices)]
ply1 = [bfreq*i*rnd1 for i in polyfreqs]
ply2 = [bfreq*i*rnd2 for i in polyfreqs]
ply3 = [bfreq*i for i in polyfreqs]
pfreqs = ply3+ply1+ply2+ply3
out = Pulsar(t, e, freq=pfreqs, frac=width, phase=0, interp=2, mul=0.3*env).out(chnl=[0,1])

def sndchoice():
    src.setSound(filesList9[int(sndidx.get())])
    index = int(srcindex.get() * src.getSize(False))
    samples = [src[i].getTable()[index:index+int(window_size)] for i in range(nchnls)]
    t = DataTable(size=len(samples[0]), chnls=len(samples), init=samples)
    out.table = t

def wtype():
    e.type = index

def wsizefunc():
    window_size = int(wsize.get())
    index = int(srcindex.get() * src.getSize(False))
    samples = [src[i].getTable()[index:index+int(value)] for i in range(nchnls)]
    t = DataTable(size=len(samples[0]), chnls=len(samples), init=samples)
    out.table = t

def srcindex_up():
    index = int(srcindex.get() * src.getSize(False))
    samples = [src[i].getTable()[index:index+int(window_size)] for i in range(nchnls)]
    t = DataTable(size=len(samples[0]), chnls=len(samples), init=samples)
    out.table = t
        


