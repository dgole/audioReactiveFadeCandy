#!/usr/bin/env python

import fastopc, time
import numpy as np
#import functionLib as lib
import micStream

stream = micStream.Stream(fps=2, nBuffers=1)
print(stream.fps)
print(stream.framesPerBuffer)

print("marker0")
stream.readNewData()
print("marker1")
stream.readNewData()
print("marker2")

stream.stopStream()

#print("marker0")
#while True:
#    print("marker1")
#    stream.readNewData()
#    print("marker2")





