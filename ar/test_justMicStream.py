#!/usr/bin/env python

import fastopc, time
import numpy as np
#import functionLib as lib
import micStream

stream = micStream.Stream(fps=40, nBuffers=1)
print(stream.fps)
print(stream.framesPerBuffer)

for i in range(0,10):
    print("i=" + str(i))
    #stream.readNewData()
    stream.stream.read(stream.framesPerBuffer)
    print("marker1")

#print("marker0")
#while True:
#    print("marker1")
#    stream.readNewData()
#    print("marker2")






