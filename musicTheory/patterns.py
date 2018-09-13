#!/usr/bin/env python

import numpy as np
import sys
sys.path.append("../ar/")
import fastopc, time
import functionLib as lib
import micStream

def beatDetection():
    stream = micStream.Stream(fps=30, nBuffers=4)
    #powerSmooth = lib.ExpFilter(val=1.0, alpha_rise=0.05, alpha_decay=0.05)
    powerSmooth = lib.ExpFilter(val=1.0, alpha_rise=0.05, alpha_decay=0.05)
    print(stream.freqs.shape)
    print(stream.freqs)
    print(stream.notes)
    for i in range(0,10): print(stream.freqsToMelMatrix[0, i*10:(i+1)*10])
    powerMinFreqIndex = int(0  / stream.dFreq)
    powerMaxFreqIndex = int(250 / stream.dFreq)
    thresh = 1.3
    recentBeat = 0
    powerNorm = np.asarray([0.,0.,0.])
    while True:
        success = stream.readAndCalc()
        if success:
            power = np.sum(stream.freqSpectrum[powerMinFreqIndex:powerMaxFreqIndex])
            powerSmooth.update(power)
            powerNorm[2] = powerNorm[1]
            powerNorm[1] = powerNorm[0]
            powerNorm[0] = power/powerSmooth.value
            lib.clDisplay(powerNorm[0])
            if powerNorm[2]<powerNorm[1] and powerNorm[1]>powerNorm[0] and powerNorm[1] > thresh and recentBeat<=0:
                recentBeat = 4
                print('BEAT '*21)
            recentBeat-=1
