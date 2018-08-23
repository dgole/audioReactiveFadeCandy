#!/usr/bin/env python

import fastopc, time
import numpy as np
#import functionLib as lib
import micStream

stream = micStream.Stream(fps=10, nBuffers=1)
print(stream.fps)
print(stream.framesPerBuffer)

for i in range(0,10):
    print("i=" + str(i))
    stream.readNewData()
    print("marker1")

#print("marker0")
#while True:
#    print("marker1")
#    stream.readNewData()
#    print("marker2")






