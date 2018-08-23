#!/usr/bin/env python

import fastopc, time
import numpy as np
#import functionLib as lib
import micStream

stream = micStream.Stream(fps=10, nBuffers=1)
print(stream.fps)
print(stream.framesPerBuffer)

time.sleep(10)

stream.stopStream()

#print("marker0")
#while True:
#    print("marker1")
#    stream.readNewData()
#    print("marker2")






