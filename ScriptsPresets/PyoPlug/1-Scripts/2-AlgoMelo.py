freqs = [midiToHz(m+7) for m in [60,62,63.93,65,67.01,69,71,72]]
chx = Choice(choice=freqs, freq=[1,2,3,3,4])
port = Port(chx, risetime=.001, falltime=.001)
sines = SineLoop(port, feedback=[.06,.057,.033,.035,.016], mul=[.15,.15,.1,.1,.06])
out = SPan(sines, pan=[0, 1, .2, .8, .5]).out()

# pOut = Print(stereoIn)
#inP = stereoIn
#pIn = Print(inP)
#rec = Record(inP, filename="/recInPyo.aif", fileformat=1, sampletype=1)
#clean = Clean_objects(2.5, rec)
#clean.start()

#pout = Print(dawQuartetPos);