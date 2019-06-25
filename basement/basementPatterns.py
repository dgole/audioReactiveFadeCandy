#!/usr/bin/env python
import numpy as np
import sys
sys.path.append("../ar/")
import fastopc, time
import functionLib as lib
import micStream
import music
import mido

nStrips = 1
lStrip  = 64

'''
TEMPLATE
def temp(brightnessFactor):
    # always here
    global nStrips, lStrip
    client    = fastopc.FastOPC('localhost:7890')
    # setup
    pixels = lib.Pixels(nStrips, lStrip, 20)
    theoStrip = np.zeros([lStrip*nStrips,3])
    # loop
    while True:
'''
def chase(brightnessFactor):
    # always here
    global nStrips, lStrip
    client    = fastopc.FastOPC('localhost:7890')
    # setup
    n = 1
    dir = 1
    pixels = lib.Pixels(nStrips, lStrip, 20)
    theoStrip = np.zeros([lStrip*nStrips,3])
    color=2
    theoStrip[n,color] = 255
    # loop
    while True:
        if n == (nStrips*lStrip-1):
            dir *=-1
        elif n == 0:
            dir*=-1
            theoStrip=np.roll(theoStrip, 1, axis=1)
        theoStrip = np.roll(theoStrip, dir, axis=0)
        pixels.update(theoStrip, 1.0, 1.0)
        client.putPixels(0, brightnessFactor*pixels.getArrayForDisplay())
        n+=dir
        time.sleep(0.003)

def bouncers(brightnessFactor):
    # always here
    global nStrips, lStrip
    client    = fastopc.FastOPC('localhost:7890')
    # setup
    nBouncers = 16
    pixels = lib.Pixels(nStrips, lStrip, 0)
    theoStrip = np.zeros([nStrips*lStrip, 3])
    bouncerList = []
    for i in range(nBouncers):
        bouncerList.append(lib.Bouncer(np.random.randint(1,high=8), np.random.rand()*0.3+0.05, np.random.rand(3), lStrip))
    # loop
    while True:
        for i in range(0,nBouncers): bouncerList[i].update()
        for i in range(0,nBouncers//2):
            stripNum = i
            base = stripNum*lStrip
            theoStrip[base:base+lStrip] = bouncerList[i].getFullOutArray() + bouncerList[i+nBouncers//2].getFullOutArray()
        pixels.update(theoStrip, 0.5, 0.5)
        client.putPixels(0, brightnessFactor*pixels.getArrayForDisplay())
        time.sleep(0.01)

def stars(brightnessFactor):
    # always here
    global nStrips, lStrip
    client    = fastopc.FastOPC('localhost:7890')
    # setup
    waitTime = 0.1
    #fade stars in over 10 frames at 0.1 s/frame is 1s per star
    nStars = 50
    pixels = lib.Pixels(nStrips, lStrip, 0)
    theoStrips = np.zeros([nStars, nStrips*lStrip, 3])
    zeroStrip = np.zeros_like(pixels.getArrayForDisplay())
    client.putPixels(0, zeroStrip)
    colorOption="all"
    # loop
    while True:
        # select new values
        positions = np.random.randint(0, high=nStrips*lStrip-1, size=nStars)
        colors    = np.random.randint(0, 255, size=[nStars,3])
        for n in range(nStars):
            maxColor  = np.amax(colors[n])
            if colorOption == "all":
                colors[n]    = 255*colors[n]/maxColor
            elif colorOption=="red":
                colors[n] = [255,0,0]
            elif colorOption=="blue":
                colors[n] = [0,0,255]
            elif colorOption=="green":
                colors[n] = [0,255,0]
            elif colorOption=="purple":
                colors[n] = [200,0,150]
        for n in range(nStars): theoStrips[n, positions[n]] = colors[n]
        # bring in new stars
        for i in range(0,nStars*10):
            starNum = int(np.floor(i/10))
            pixels.update(theoStrips[starNum], 0.2, 0.0)
            client.putPixels(0, brightnessFactor*pixels.getArrayForDisplay())
            time.sleep(waitTime)
        # clear old stars
        for i in range(0,int(10/waitTime)):
            pixels.update(zeroStrip, 0.0, 0.02)
            client.putPixels(0, brightnessFactor*pixels.getArrayForDisplay())
            time.sleep(waitTime)
        # fully zero out strip
        pixels.update(zeroStrip, 1.0, 1.0)
        theoStrips = np.zeros([nStars, nStrips*lStrip, 3])

def bassWiden(brightnessFactor):
    # always here
    global nStrips, lStrip
    client    = fastopc.FastOPC('localhost:7890')
    # setup
    pixels = lib.Pixels(nStrips, lStrip, 20)
    theoStrip = np.zeros([lStrip//2, 3])
    stream = micStream.Stream(fps=30, nBuffers=4)
    powerMinFreqIndex1 = int(0   / stream.dFreq)
    powerMaxFreqIndex1 = int(200 / stream.dFreq)
    powerSmooth = lib.ExpFilter(val=1.0, alpha_rise=0.01, alpha_decay=0.01)
    nColorWheel = 600
    colorWheel = lib.getColorWheel(nColorWheel)
    frameCount = 0
    # loop
    while True:
        success = stream.readAndCalc()
        if success:
            frameNumEff = np.mod(frameCount, nColorWheel)
            power = np.sum(stream.freqSpectrum[powerMinFreqIndex1:powerMaxFreqIndex1])
            powerSmooth.update(power)
            displayPower = max(int(122*power/powerSmooth.value),50)
            width = int(2 + 0.5*np.sqrt(float(displayPower)))
            theoStrip[width:] = displayPower * colorWheel[np.mod(frameNumEff+200,nColorWheel)]
            theoStrip[0:width] =  255 * colorWheel[np.mod(frameNumEff,nColorWheel)]
            #pixels.update(theoStrip, 0.7, 0.2)
            pixels.update(theoStrip, 1.0, 1.0)
            client.putPixels(0, brightnessFactor*pixels.getArrayForDisplay())
            frameCount+=1

def bassScrollMiddle(brightnessFactor):
    # always here
    global nStrips, lStrip
    client    = fastopc.FastOPC('localhost:7890')
    # setup
    pixels = lib.Pixels(nStrips, lStrip, 0)
    theoStrip = np.zeros([lStrip//2, 3])
    stream = micStream.Stream(fps=30, nBuffers=4)
    powerSmooth = lib.ExpFilter(val=0.05, alpha_rise=0.05, alpha_decay=0.05)
    nColorWheel = 300
    colorWheel = lib.getColorWheel(nColorWheel)
    frameCount = 0
    # loop
    while True:
        success = stream.readAndCalc()
        if success:
            frameNumEff = np.mod(frameCount, nColorWheel)
            power = np.sum(stream.freqSpectrum[20//7:250//7])
            powerSmooth.update(power)
            displayPower = int(122*np.power(power/powerSmooth.value, 1.5))
            theoStrip = np.roll(theoStrip, 1, axis=0)
            theoStrip[1] = displayPower * colorWheel[frameNumEff]
            theoStrip[0] = 1000*colorWheel[frameNumEff]
            pixels.update(theoStrip, 0.5, 0.5)
            client.putPixels(0, brightnessFactor*pixels.getArrayForDisplay())
            frameCount+=1

def kickDrum(brightnessFactor):
    # always here
    global nStrips, lStrip
    client    = fastopc.FastOPC('localhost:7890')
    # setup
    pixels = lib.Pixels(nStrips, lStrip, 0)
    theoStrip = np.zeros([lStrip//2, 3])
    stream = micStream.Stream(fps=60, nBuffers=4)
    powerSmooth = lib.ExpFilter(val=0.05, alpha_rise=0.1, alpha_decay=0.1)
    nColorWheel = 300
    colorWheel = lib.getColorWheel(nColorWheel)
    frameCount = 0
    # loop
    while True:
        success = stream.readAndCalc()
        if success:
            frameNumEff = np.mod(frameCount, nColorWheel)
            #power = np.sum(stream.freqSpectrum[20//7:250//7])
            power = np.sum(stream.freqSpectrum[:20])
            powerSmooth.update(power)
            if power > 1.e4:
                displayPower = int(122*np.power(power/powerSmooth.value, 1.5))
                theoStrip[:] = displayPower * colorWheel[frameNumEff]
                #theoStrip[0] = 1000*colorWheel[frameNumEff]
                pixels.update(theoStrip, 1.0, 0.4)
                client.putPixels(0, brightnessFactor*pixels.getArrayForDisplay())
                frameCount+=1
            else:
                theoStrip[:] = np.zeros_like(theoStrip[:])
                #theoStrip[0] = 1000*colorWheel[frameNumEff]
                pixels.update(theoStrip, 1.0, 0.4)
                client.putPixels(0, brightnessFactor*pixels.getArrayForDisplay())


def bassScrollTop(brightnessFactor):
    # always here
    global nStrips, lStrip
    client    = fastopc.FastOPC('localhost:7890')
    # setup
    pixels = lib.Pixels(nStrips, lStrip, 0)
    theoStrip = np.zeros([lStrip, 3])
    stream = micStream.Stream(fps=30, nBuffers=4)
    powerSmooth = lib.ExpFilter(val=1.0, alpha_rise=0.01, alpha_decay=0.01)
    nColorWheel = 300
    colorWheel = lib.getColorWheel(nColorWheel)
    frameCount = 0
    powerMinFreqIndex = int(0   / stream.dFreq)
    powerMaxFreqIndex = int(120 / stream.dFreq)
    # loop
    while True:
        success = stream.readAndCalc()
        if success:
            frameNumEff = np.mod(frameCount, nColorWheel)
            power = np.sum(stream.freqSpectrum[powerMinFreqIndex:powerMaxFreqIndex])
            powerSmooth.update(power)
            displayPower = int(122*np.power(power/powerSmooth.value, 1.5))
            theoStrip = np.roll(theoStrip, -1, axis=0)
            theoStrip[-2] = displayPower * colorWheel[frameNumEff]
            theoStrip[-1] = 1000*colorWheel[frameNumEff]
            pixels.update(theoStrip, 0.7, 0.5)
            client.putPixels(0, brightnessFactor*pixels.getArrayForDisplay())
            frameCount+=1

def beatDetection(brightnessFactor):
    # always here
    client    = fastopc.FastOPC('localhost:7890')
    pixels    = lib.Pixels(nStrips, lStrip, 0)
    theo      = np.zeros([lStrip,3])
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

            theo[0,:] = 0
            theo       = np.roll(theo, -1, axis=0)
            if beatObj1.getBeatStatus() == True:
                theo[-1,0]=255
                print('BEAT '*21)
            if beatObj2.getBeatStatus() == True:
                theo[-1, 2]=255
                #print('BEAT '*21)
            lib.clDisplay(powerNorm2)
            pixels.update(theo, 1.0, 0.3)
            client.putPixels(0, brightnessFactor*pixels.getArrayForDisplay())

def bouncers_ar(brightnessFactor):
    # always here
    global nStrips, lStrip
    client    = fastopc.FastOPC('localhost:7890')
    # setup
    stream = micStream.Stream(fps=30, nBuffers=4)
    powerSmooth = lib.ExpFilter(val=0.05, alpha_rise=0.05, alpha_decay=0.05)
    powerMinFreqIndex = int(0   / stream.dFreq)
    powerMaxFreqIndex = int(250 / stream.dFreq)
    nBouncers = 16
    pixels = lib.Pixels(nStrips, lStrip, 0)
    theoStrip = np.zeros([nStrips*lStrip, 3])
    bouncerList = []
    for i in range(nBouncers):
        bouncerList.append(lib.Bouncer(np.random.randint(1,high=8), np.random.rand()*0.3+0.05, np.random.rand(3), lStrip))
    # loop
    while True:
        success = stream.readAndCalc()
        if success:
            power = np.sum(stream.freqSpectrum[powerMinFreqIndex:powerMaxFreqIndex])
            powerSmooth.update(power)
            displayPower = int(122*np.power(power/powerSmooth.value, 1.5))
            for i in range(0,nBouncers): bouncerList[i].update()
            for i in range(0,nBouncers//2):
                stripNum = i
                base = stripNum*lStrip
                theoStrip[base:base+lStrip] = (0.5+(float(displayPower)/255.0)) * ( bouncerList[i].getFullOutArray() + bouncerList[i+nBouncers//2].getFullOutArray() )
            pixels.update(theoStrip, 0.5, 0.5)
            client.putPixels(0, brightnessFactor*pixels.getArrayForDisplay())
            #time.sleep(0.01)

def chase_beatDetection(brightnessFactor):
    # always here
    global nStrips, lStrip
    client    = fastopc.FastOPC('localhost:7890')
    # setup
    stream    = micStream.Stream(fps=30, nBuffers=4)

    powerSmooth1 = lib.ExpFilter(val=1.0, alpha_rise=0.05, alpha_decay=0.05)
    powerMinFreqIndex1 = int(0   / stream.dFreq)
    powerMaxFreqIndex1 = int(120 / stream.dFreq)
    beatObj1 = music.Beat(thresh=1.5, waitFrames = 5)

    powerSmooth2 = lib.ExpFilter(val=1.0, alpha_rise=0.1, alpha_decay=0.1)
    powerMinFreqIndex2 = int(9000 / stream.dFreq)
    powerMaxFreqIndex2 = int(10000 / stream.dFreq)
    beatObj2 = music.Beat(thresh=2.5, waitFrames = 2)

    dir = 1
    pixels = lib.Pixels(nStrips, lStrip, 20)
    theoStrip = np.zeros([lStrip*nStrips,3])
    color=2
    for n in range(0,lStrip*nStrips, lStrip//2+2 ): theoStrip[n,color] = 255
    # loop
    while True:
        success = stream.readAndCalc()
        if success:
            power1 = np.sum(stream.freqSpectrum[powerMinFreqIndex1:powerMaxFreqIndex1])
            powerSmooth1.update(power1)
            #powerTot = np.sum(stream.freqSpectrum)
            powerSmooth1.update(power1)
            powerNorm1 = power1/powerSmooth1.value
            beatObj1.update(powerNorm1)

            power2 = np.sum(stream.freqSpectrum[powerMinFreqIndex2:powerMaxFreqIndex2])
            powerSmooth2.update(power2)
            powerNorm2 = power2/powerSmooth2.value
            beatObj2.update(powerNorm2)
            if beatObj1.getBeatStatus() == True:
                dir *=-1
                theoStrip = np.roll(theoStrip, 1, axis=1)
            lib.clDisplay(powerNorm1)
            theoStrip = np.roll(theoStrip, dir, axis=0)
            pixels.update(theoStrip, 1.0, 0.05)
            client.putPixels(0, brightnessFactor*pixels.getArrayForDisplay())
            n+=dir
            time.sleep(0.003)

def rain1(brightnessFactor):
    # always here
    global nStrips, lStrip
    client = fastopc.FastOPC('localhost:7890')
    # setup
    nColorWheel = 100
    colorWheel = lib.getColorWheel(nColorWheel)
    pixels  = lib.Pixels(nStrips, lStrip, 0)
    theoAll = np.zeros([lStrip*nStrips,3])
    frameCount = 0
    # loop
    while True:
        for i in range(nStrips): theoAll[i*lStrip,:]=0
        frameNumEff = np.mod(frameCount, nColorWheel)
        theoAll = 0.99*np.roll(theoAll, -1, axis=0)
        if np.random.rand()<0.75:
            stripNum = np.random.randint(0, high=nStrips)
            theoAll[(stripNum*lStrip)+lStrip-1]=255*colorWheel[frameNumEff]
        pixels.update(theoAll, 1.0, 0.4)
        client.putPixels(0, brightnessFactor*pixels.getArrayForDisplay())
        time.sleep(0.05)
        frameCount+=1

def rain2(brightnessFactor):
    # always here
    global nStrips, lStrip
    client = fastopc.FastOPC('localhost:7890')
    # setup
    nColorWheel = nStrips
    colorWheel  = lib.getColorWheelRedBlue(nColorWheel)
    pixels      = lib.Pixels(nStrips, lStrip, 0)
    theoAll     = np.zeros([lStrip*nStrips,3])
    frameCount  = 0
    stripNum    = 0
    dir         = 1
    updateEvery = 50
    sleepTime   = 0.03 / updateEvery
    chance      = 0.5
    alpha       = float(2.0/updateEvery)
    # loop
    while True:
        if np.mod(frameCount, updateEvery) == 0:
            for i in range(nStrips): theoAll[i*lStrip,:]=0
            theoAll = np.roll(theoAll, -1, axis=0)
            if np.random.rand()<chance:
                if stripNum==0:
                    dir=1
                elif stripNum==nStrips-1:
                    dir=-1
                theoAll[(stripNum*lStrip)+lStrip-1]=255*colorWheel[stripNum]
                stripNum += dir
        pixels.update(theoAll, alpha, alpha/10.0)
        client.putPixels(0, brightnessFactor*pixels.getArrayForDisplay())
        frameCount+=1
        time.sleep(sleepTime)

def rain1_midi(brightnessFactor):
    # always here
    global nStrips, lStrip
    client = fastopc.FastOPC('localhost:7890')
    # setup
    pixels     = lib.Pixels(nStrips, lStrip, 0)
    theoAll    = np.zeros([lStrip*nStrips,3])
    inputNames = mido.get_input_names()
    inport     = mido.open_input(inputNames[0])
    board      = lib.Board()
    speedCut   = 100
    frameNum   = 0
    midiNotes  = []
    while len(midiNotes) < nStrips:
        for msg in inport.iter_pending():
            if msg.type == 'note_on':
                midiNotes.append(msg.note)
                print(midiNotes)
    # loop
    while True:
        for msg in inport.iter_pending():
            board.update(msg)
        color = 2*board.knobs[48:51]
        overallFactor = float(board.knobs[51]+1)/(128.0)
        if np.mod(frameNum, speedCut) == 0:
            for n in range(nStrips): theoAll[n*lStrip,:]=0
            theoAll     = np.roll(theoAll, -1, axis=0)
            for n in range(nStrips):
                midiNoteNum = midiNotes[n]
                if board.notes[midiNoteNum] == 1:
                    theoAll[(n*lStrip)+lStrip-1] = color*(board.velocities[midiNoteNum]/128.0)
                    #theoAll[(n*lStrip)+lStrip-1] = stripColors[n]
            pixels.update(theoAll, 1.0, 0.4)
            client.putPixels(0, overallFactor*brightnessFactor*pixels.getArrayForDisplay())
        time.sleep(2.e-4)
        frameNum+=1

def rain2_midi(brightnessFactor):
    # always here
    global nStrips, lStrip
    client = fastopc.FastOPC('localhost:7890')
    # setup
    pixels     = lib.Pixels(nStrips, lStrip, 0)
    theoAll    = np.zeros([lStrip*nStrips,3])
    inputNames = mido.get_input_names()
    inport     = mido.open_input(inputNames[0])
    board      = lib.Board()
    speedCut   = 100
    frameNum   = 0
    stripColors = np.zeros([nStrips, 3])
    n=0
    while n < nStrips:
        for msg in inport.iter_pending():
            board.update(msg)
            if msg.type == 'note_on':
                stripColors[n] = 2*board.knobs[48:51]
        n+=1
    # loop
    while True:
        for msg in inport.iter_pending():
            board.update(msg)
        overallFactor = float(board.knobs[51]+1)/(128.0)
        if np.mod(frameNum, speedCut) == 0:
            for n in range(nStrips): theoAll[n*lStrip,:]=0
            theoAll     = np.roll(theoAll, -1, axis=0)
            for n in range(nStrips):
                iNotes[n]
                if board.notes[midiNoteNum] == 1:
                    theoAll[(n*lStrip)+lStrip-1] = stripColors[n]
            pixels.update(theoAll, 1.0, 0.4)
            client.putPixels(0, overallFactor*brightnessFactor*pixels.getArrayForDisplay())
        time.sleep(2.e-4)
        frameNum+=1

def drums_midi(brightnessFactor):
    # always here
    global nStrips, lStrip
    client = fastopc.FastOPC('localhost:7890')
    # setup
    pixels     = lib.Pixels(nStrips, lStrip, 0)
    theoAll    = np.zeros([lStrip*nStrips,3])
    inputNames = mido.get_input_names()
    inport     = mido.open_input(inputNames[1])
    board      = lib.Board()
    speedCut   = 100
    frameNum   = 0
    nColorWheel = nStrips
    colorWheel  = lib.getColorWheel(nColorWheel)
    stripColors = np.zeros([nStrips, 3])
    n=0
    while n < nStrips:
        stripColors[n]=colorWheel[n]*255
    	n+=1
    midiNotes=[]
    while len(midiNotes) < nStrips:
        for msg in inport.iter_pending():
            if msg.type == 'note_on':
                midiNotes.append(msg.note)
                print(midiNotes)
	justTurnedOn = np.zeros(nStrips)
    # loop
    while True:
        for msg in inport.iter_pending():
            board.update(msg)
        #overallFactor = float(board.knobs[51]+1)/(128.0)
        #if np.mod(frameNum, speedCut) == 0:
        for n in range(nStrips): theoAll[n*lStrip,:]=0
        theoAll = np.roll(theoAll, -1, axis=0)
        for n in range(nStrips):
            if board.notes[midiNotes[n]] == 1:
                theoAll[(n*lStrip)+lStrip-1] = stripColors[n]
        pixels.update(theoAll, 1.0, 0.4)
        client.putPixels(0, brightnessFactor*pixels.getArrayForDisplay())
        time.sleep(2.e-2)
        frameNum+=1


def bpm(brightnessFactor):
    # always here
    global nStrips, lStrip
    #client    = fastopc.FastOPC('localhost:7890')
    # setup
    #pixels = lib.Pixels(nStrips, lStrip, 20)
    #theoStrip = np.zeros([lStrip//2, 3])
    stream = micStream.Stream(fps=30, nBuffers=4)
    powerMinFreqIndex1 = int(0   / stream.dFreq)
    powerMaxFreqIndex1 = int(200 / stream.dFreq)
    powerSmooth = lib.ExpFilter(val=1.0, alpha_rise=0.01, alpha_decay=0.01)
    #frameCount = 0
    bpm = music.BPM()
    # loop
    while True:
        success = stream.readAndCalc()
        if success:
            power = np.sum(stream.freqSpectrum[powerMinFreqIndex1:powerMaxFreqIndex1])
            powerSmooth.update(power)
            bpm.update(power)


            #displayPower = max(int(122*power/powerSmooth.value),50)
            #pixels.update(theoStrip, 0.7, 0.2)
            #client.putPixels(0, brightnessFactor*pixels.getArrayForDisplay())
            #frameCount+=1


def joystick(brightnessFactor):
    # always here
    global nStrips, lStrip
    client = fastopc.FastOPC('localhost:7890')
    # setup
    pixels     = lib.Pixels(nStrips, lStrip, 0)
    theoAll    = np.zeros([lStrip*nStrips,3])
    inputNames = mido.get_input_names()
    inport     = mido.open_input(inputNames[0])
    board      = lib.Board()
    # loop
    while True:
        for msg in inport.iter_pending():
            board.update(msg)
        for n in range(nStrips): theoAll[n*lStrip,:]=0
        theoAll      = np.roll(theoAll, -1, axis=0)
        currentStrip = np.floor((board.pitchwheel+8192)//(8192*2//nStrips))
        for n in range(nStrips):
            if n == currentStrip:
                theoAll[(n*lStrip)+lStrip-1] = [200, 100, 250]
        pixels.update(theoAll, 1.0, 0.4)
        client.putPixels(0, brightnessFactor*pixels.getArrayForDisplay())
        time.sleep(2.e-2)


def loopTest(brightnessFactor):
    # always here
    global nStrips, lStrip
    #client = fastopc.FastOPC('localhost:7890')
    # setup
    pixels     = lib.Pixels(nStrips, lStrip, 0)
    theoAll    = np.zeros([lStrip*nStrips,3])
    inputNames = mido.get_input_names()
    inport     = mido.open_input(inputNames[0])
    board      = lib.Board()
    mseqList   = []
    n1         = 0
    # loop
    while True:
        n=0
        mseqList.append(lib.midiSequence())
        while n < 10000:
            n+=1
            for msg in inport.iter_pending():
                mseq.update(msg)
            pixels.update(theoAll, 1.0, 0.4)
            #client.putPixels(0, brightnessFactor*pixels.getArrayForDisplay())
            time.sleep(2.e-4)
        n1+=1
























##
