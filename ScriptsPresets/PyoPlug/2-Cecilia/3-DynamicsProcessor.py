"""
Compression and gate module

Sliders:

    - Overall Amplitude : The amplitude curve applied on the total duration of the performance
    - Input Gain : Adjust the amount of signal sent to the processing chain
    - Compression Thresh : dB value at which the compressor becomes active
    - Compression Rise Time : Time taken by the compressor to reach compression ratio
    - Compression Fall Time : Time taken by the compressor to reach uncompressed state
    - Compression Knee : Steepness of the compression curve
    - Gate Thresh : dB value at which the gate becomes active
    - Gate Slope : Shape of the gate (rise time and fall time)
    - Output Gain : Makeup gain applied after the processing chain
    - Compression Ratio : Ratio between the compressed signal and the uncompressed signal
"""

# User Interface  
defineUI(id=1, name="env", label="Amplitude", unit="x", init=.7)
defineUI(id=2, name="inputgain", label="InputGain", min=-48, max=18, init=0, rel="lin", unit="dB")
defineUI(id=3, name="compthresh", label="CompThresh", min=-60, max=-0.1, init=-20, rel="lin", unit="dB")
defineUI(id=4, name="comprise", label="CompRiseTime", min=0.01, max=1, init=0.01, rel="lin", unit="sec")
defineUI(id=5, name="compfall", label="CompFallTime", min=0.01, max=1, init=0.1, rel="lin", unit="sec")
defineUI(id=6, name="compknee", label="CompKnee", min=0, max=1, init=0, rel="lin", unit="x")
defineUI(id=7, name="gatethresh", label="GateThresh", min=-80, max=-0.1, init=-60, rel="lin", unit="dB")
defineUI(id=8, name="gateslope", label="GateSlope", min=0.01, max=1, init=0.05, rel="lin", unit="x")
defineUI(id=9, name="outputgain", label="OutputGain", min=-48, max=18, init=0, rel="lin", unit="dB")
defineUI(id=10, name="compratio", label="CompRatio", min=0.25, max=100, init=3, rel="exp", unit='x')

# DSP
# snd = Input(chnl=0)
# snd = [Input(chnl=0), Input(chnl=1)]
snd = stereoIn
crank = Sig(snd, mul=DBToA(inputgain))
comp = Compress(input=crank, thresh=compthresh, ratio=compratio, risetime=comprise, falltime=compfall, lookahead=0, knee=compknee, outputAmp=False, mul=1)
gate = Gate(input=comp , thresh=gatethresh, risetime=gateslope, falltime=gateslope, lookahead=0.00, outputAmp=False, mul=1)
out = gate*DBToA(outputgain)*env
out.out(chnl=[0,1])