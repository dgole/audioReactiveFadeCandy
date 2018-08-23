#!/usr/bin/env python

import fastopc, time
import numpy as np
#import functionLib as lib
import micStream
import pyaudio


stream = micStream.Stream(fps=1, nBuffers=1)
#print(stream.fps)
#print(stream.framesPerBuffer)

for i in range(0,10):
    print("i=" + str(i))
    #stream.readNewData()
    stream.stream.read(2*stream.framesPerBuffer)
    print("marker1")


'''
# audio setup
CHUNK = 8192    # input buffer size in frames
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATES = [96000, 88200, 48000, 44100, 32000, 24000]
RATES = [44100]
# open sound card data stream
npoints = 1000000
for rate in RATES:
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
        channels=CHANNELS,
        rate=rate,
        input=True,
        frames_per_buffer=CHUNK)
    try:
        print "RATE %d" % rate,
        x = stream.read(npoints)
        print "OK"
    except IOError:
        print "FAIL"
    stream.stop_stream()
    stream.close()
p.terminate()
'''






