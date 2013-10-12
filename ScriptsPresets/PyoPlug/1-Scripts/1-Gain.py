# User interface
defineUI(id=1, name="env", label="Amplitude", unit="x", init=.8)

# DSP
audioIn = stereoIn

gain = Sig(audioIn, mul=env)
out = gain.out(chnl=[0,1])