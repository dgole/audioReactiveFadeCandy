#!/usr/bin/env python

import numpy as np
import sys
sys.path.append("../ar/")
import fastopc, time
import functionLib as lib
import micStream
import music

#lNeck  = 18
lNeck  = 64
lBody  = 40
lStrap = 36

def basic(brightnessFactor):
    print('brightness factor is ' + str(brightnessFactor))
    global lNeck, lBody, lStrap
    client    = fastopc.FastOPC('localhost:7890')
    pixels    = lib.BassPixels(lNeck, lBody, lStrap, 0)
    theoNeck  = np.zeros([lNeck,  3])
    theoBody  = np.zeros([lBody,  3])
    theoStrap = np.zeros([lStrap, 3])
    stream    = micStream.Stream(fps=30, nBuffers=4)

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
    client    = fastopc.FastOPC('localhost:7890')
    pixels    = lib.BassPixels(lNeck, lBody, lStrap, 0)
    theoNeck  = np.zeros([lNeck,  3])
    theoBody  = np.zeros([lBody,  3])
    theoStrap = np.zeros([lStrap, 3])
    stream    = micStream.Stream(fps=30, nBuffers=4)

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

def beatDetectionBounce(brightnessFactor):
    global lNeck, lBody, lStrap
    client    = fastopc.FastOPC('localhost:7890')
    pixels    = lib.BassPixels(lNeck, lBody, lStrap, 0)
    theoNeck  = np.zeros([lNeck,  3])
    theoBody  = np.zeros([lBody,  3])
    theoStrap = np.zeros([lStrap, 3])
    stream    = micStream.Stream(fps=30, nBuffers=4)

    powerSmooth1 = lib.ExpFilter(val=1.0, alpha_rise=0.05, alpha_decay=0.05)
    powerMinFreqIndex1 = int(0   / stream.dFreq)
    powerMaxFreqIndex1 = int(250 / stream.dFreq)
    beatObj1 = music.Beat()

    powerSmooth2 = lib.ExpFilter(val=1.0, alpha_rise=0.1, alpha_decay=0.1)
    powerMinFreqIndex2 = int(9000 / stream.dFreq)
    powerMaxFreqIndex2 = int(10000 / stream.dFreq)
    beatObj2 = music.Beat(thresh=2.5, waitFrames = 2)

    while True:
        success = stream.readAndCalc()
        if success:
            power1 = np.sum(stream.freqSpectrum[powerMinFreqIndex1:powerMaxFreqIndex1])
            powerSmooth1.update(power1)
            powerNorm1 = power1/powerSmooth1.value
            beatObj1.update(powerNorm1)

            power2 = np.sum(stream.freqSpectrum[powerMinFreqIndex2:powerMaxFreqIndex2])
            powerSmooth2.update(power2)
            powerNorm2 = power2/powerSmooth2.value
            beatObj2.update(powerNorm2)

            theoNeck = np.roll(theoNeck, 1, axis=0)
            theoNeck[0] = 0
            if beatObj1.getBeatStatus() == True:
                theoNeck[0,0]=255
            lib.clDisplay(powerNorm2)
            if beatObj2.getBeatStatus() == True:
                theoNeck[0,2]=255
                print('BEAT '*21)
            pixels.updateNeck(theoNeck, 1.0, 0.3)
            client.putPixels(0, brightnessFactor*pixels.getArrayForDisplay())


def oneNote(brightnessFactor):
    global lNeck, lBody, lStrap
    #client    = fastopc.FastOPC('localhost:7890')
    #pixels    = lib.BassPixels(lNeck, lBody, lStrap, 0)
    #theoNeck  = np.zeros([lNeck,  3])
    #theoBody  = np.zeros([lBody,  3])
    #theoStrap = np.zeros([lStrap, 3])
    stream     = micStream.Stream(fps=30, nBuffers=4)

    keyObj       = music.Key(stream.notes)
    noteSumsObj  = music.NoteSums(stream.notes)
    noteSumsObj2 = music.NoteSums(stream.notes, alpha=0.5)
    #chordObj    = music.Chord(stream.notes)

    while True:
        success = stream.readAndCalc()
        if success:
            keyObj      .update(stream.noteSpectrum)
            noteSumsObj .update(stream.noteSpectrum)
            noteSumsObj2.update(stream.noteSpectrum)
            #chordObj    .update(stream.noteSpectrum, keyObj.currentKeyNum)

            #keyObj.printKey()
            #chordObj.printChord()
            noteSumsObj2.printNoteSums()


            #client.putPixels(0, brightnessFactor*pixels.getArrayForDisplay())

























##
