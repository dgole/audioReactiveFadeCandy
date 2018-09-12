#!/usr/bin/env python

import numpy as np
import sys
sys.path.append("../ar/")
import fastopc, time
import functionLib as lib
import micStream

lNeck  = 18
lBody  = 40
lStrap = 36

def basic(brightnessFactor):
    print('brightness factor is ' + str(brightnessFactor))
    global lNeck, lBody, lStrap
    client = fastopc.FastOPC('localhost:7890')

    pixels    = lib.BassPixels(lNeck, lBody, lStrap, 0)
    theoNeck  = np.zeros([lNeck,  3])
    theoBody  = np.zeros([lBody,  3])
    theoStrap = np.zeros([lStrap, 3])

    stream = micStream.Stream(fps=30, nBuffers=4)

    powerSmooth = lib.ExpFilter(val=0.05, alpha_rise=0.05, alpha_decay=0.05)
    nColorWheel = 600
    colorWheel = lib.getColorWheel(nColorWheel)
    frameCount = 0

    while True:
        success = stream.readAndCalc()
        if success:
            frameNumEff = np.mod(frameCount, nColorWheel)
            power = np.sum(stream.freqSpectrum[20//7:250//7])
            powerSmooth.update(power)
            displayPower = int(122*power/powerSmooth.value)
            width = int(5 + np.sqrt(float(displayPower)))
            theoBody          = displayPower * colorWheel[np.mod(frameNumEff+200, nColorWheel)]
            theoNeck[0:width] = 255          * colorWheel[np.mod(frameNumEff,     nColorWheel)]
            pixels.updateBody(theoBody, 0.7, 0.1)
            pixels.updateNeck(theoNeck, 0.7, 0.1)
            client.putPixels(0, brightnessFactor*pixels.getArrayForDisplay())
            frameCount+=1

def scroll(brightnessFactor):
    global lNeck, lBody, lStrap
    client = fastopc.FastOPC('localhost:7890')

    pixels    = lib.BassPixels(lNeck, lBody, lStrap, 0)
    theoNeck  = np.zeros([lNeck,  3])
    theoBody  = np.zeros([lBody,  3])
    theoStrap = np.zeros([lStrap, 3])

    stream = micStream.Stream(fps=30, nBuffers=4)

    powerSmooth = lib.ExpFilter(val=0.05, alpha_rise=0.05, alpha_decay=0.05)
    nColorWheel = 600
    colorWheel = lib.getColorWheel(nColorWheel)
    frameCount = 0

    while True:
        success = stream.readAndCalc()
        if success:
            frameNumEff = np.mod(frameCount, nColorWheel)
            power = np.sum(stream.freqSpectrum[20//7:250//7])
            powerSmooth.update(power)
            displayPower = int(122*np.power(power/powerSmooth.value, 1.5))
            theoNeck     = np.roll(theoNeck, 1, axis=0)
            theoNeck[0]  = displayPower * colorWheel[frameNumEff]
            theoBody     = displayPower * colorWheel[np.mod(frameNumEff+200, nColorWheel)]
            pixels.updateBody(theoBody, 0.5, 0.5)
            pixels.updateNeck(theoNeck, 0.5, 0.5)
            client.putPixels(0, brightnessFactor*pixels.getArrayForDisplay())
            frameCount+=1
