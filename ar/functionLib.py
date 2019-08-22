#!/usr/bin/env python

# Light each LED in sequence, and repeat.

#import fastopc, time
import numpy as np
import mido
import time

class Board:
    def __init__(self):
        self.knobs      = np.zeros(128)
        self.pitchwheel = 0.0
        self.notes      = np.zeros(128)
        self.velocities = np.zeros(128)
    def update(self, msg):
        print(msg)
        if msg.type == 'note_on':
            self.notes[msg.note] = 1
            self.velocities[msg.note] = msg.velocity
        elif msg.type == 'note_off':
            self.notes[msg.note] = 0
        elif msg.type == 'pitchwheel':
            self.pitchwheel = msg.pitch
        elif msg.type == 'control_change':
            self.knobs[msg.control] = msg.value

class midiSequence:
    def __init__(self):
        self.msgList = []
        self.tList   = []
    def update(self, msg):
        if self.tList == 0: self.t0 = time.time
        self.tList.append(time.time()-self.t0)
        self.msgList.append(msg)
    def getMsgs(self, msg):
        msgReturnList = []
        t = time.time()
        for n in range(len(self.tList)):
            if t<tList[n]:
                msgReturnList.append(msgList[n])



class Pixels():
    def __init__(self, nStrips, lStrip, minDisplay, upSampleFactor=1):
        self.upSampleFactor=upSampleFactor
        self.nStrips    = nStrips
        self.lStrip     = lStrip
        self.nLed       = nStrips*lStrip
        self.minDisplay = minDisplay
        self.array      = np.zeros([self.nLed, 3])
    def update(self, arrayNew, alphaRise, alphaDecay):
        if arrayNew.shape == (self.lStrip, 3):
            arrayNew = np.tile(arrayNew, (self.nStrips, 1))
            alpha = arrayNew - self.array
            alpha[alpha > 0.0 ] = alphaRise
            alpha[alpha <= 0.0] = alphaDecay
            self.array = alpha*arrayNew + (1.0-alpha)*self.array
        elif arrayNew.shape == (self.nLed,   3):
            alpha = arrayNew - self.array
            alpha[alpha > 0.0 ] = alphaRise
            alpha[alpha <= 0.0] = alphaDecay
            self.array = alpha*arrayNew + (1.0-alpha)*self.array
        elif arrayNew.shape == (self.nStrips, self.lStrip, 3):
            arrayNew = arrayNew.reshape(self.nLed, 3) 
            alpha    = arrayNew - self.array
            alpha[alpha > 0.0 ] = alphaRise
            alpha[alpha <= 0.0] = alphaDecay
            self.array = alpha*arrayNew + (1.0-alpha)*self.array
        elif arrayNew.shape == (self.lStrip//2,   3):
            arrayNewFlip = np.flip(arrayNew, axis=0)
            arrayNewDouble = np.concatenate((arrayNewFlip,arrayNew), axis=0)
            arrayNew = np.tile(arrayNewDouble, (self.nStrips, 1))
            alpha = arrayNew - self.array
            alpha[alpha > 0.0 ] = alphaRise
            alpha[alpha <= 0.0] = alphaDecay
            self.array = alpha*arrayNew + (1.0-alpha)*self.array
        elif arrayNew.shape == (self.nLed//2,   3):
            arrayNewFull = np.zeros_like(self.array)
            for i in range(self.nStrips):
                arrayNewFlip = np.flip(arrayNew, axis=0)
                arrayNewDouble = np.concatenate((arrayNewFlip,arrayNew), axis=0)
                arrayNewFull[(i-1)*self.lStrip:(i)*self.lStrip] = arrayNewDouble
            alpha = arrayNew - self.array
            alpha[alpha > 0.0 ] = alphaRise
            alpha[alpha <= 0.0] = alphaDecay
            self.array = alpha*arrayNewFull + (1.0-alpha)*self.array
    def updateSimple(self, arrayNew):
        if arrayNew.shape == (self.lStrip, 3):
            arrayNew = np.tile(arrayNew, (self.nStrips, 1))
            self.array = arrayNew
        elif arrayNew.shape == (self.nLed,   3):
            self.array = arrayNew
    def getArrayForDisplay(self):
        if self.upSampleFactor==1:
            returnArray = self.array
        else:
            returnArray = np.mean(self.array.reshape(-1,self.upSampleFactor), axis=0)
        if self.minDisplay != 0: returnArray[returnArray < self.minDisplay] = 0
        return returnArray

class PixelsHalfStrips():
    def __init__(self, nStrips, lStrip, minDisplay):
        self.nStrips    = nStrips
        self.lStrip     = lStrip
        self.nLed       = nStrips*lStrip
        self.minDisplay = minDisplay
        self.array      = np.zeros([self.nLed, 3])
    def update(self, arrayNew, alphaRise, alphaDecay):
        if arrayNew.shape == (self.lStrip, 3):
            arrayNew = np.tile(arrayNew, (self.nStrips, 1))
            alpha = arrayNew - self.array
            alpha[alpha > 0.0 ] = alphaRise
            alpha[alpha <= 0.0] = alphaDecay
            self.array = alpha*arrayNew + (1.0-alpha)*self.array
        elif arrayNew.shape == (self.nLed,   3):
            alpha = arrayNew - self.array
            alpha[alpha > 0.0 ] = alphaRise
            alpha[alpha <= 0.0] = alphaDecay
            self.array = alpha*arrayNew + (1.0-alpha)*self.array
        elif arrayNew.shape == (self.lStrip//2,   3):
            arrayNewFlip = np.flip(arrayNew, axis=0)
            arrayNewDouble = np.concatenate((arrayNewFlip,arrayNew), axis=0)
            arrayNew = np.tile(arrayNewDouble, (self.nStrips, 1))
            alpha = arrayNew - self.array
            alpha[alpha > 0.0 ] = alphaRise
            alpha[alpha <= 0.0] = alphaDecay
            self.array = alpha*arrayNew + (1.0-alpha)*self.array
        elif arrayNew.shape == (self.nLed//2,   3):
            arrayNewFull = np.zeros_like(self.array)
            for i in range(self.nStrips):
                arrayNewFlip = np.flip(arrayNew, axis=0)
                arrayNewDouble = np.concatenate((arrayNewFlip,arrayNew), axis=0)
                arrayNewFull[(i-1)*self.lStrip:(i)*self.lStrip] = arrayNewDouble
            alpha = arrayNew - self.array
            alpha[alpha > 0.0 ] = alphaRise
            alpha[alpha <= 0.0] = alphaDecay
            self.array = alpha*arrayNewFull + (1.0-alpha)*self.array
    def updateSimple(self, arrayNew):
        if arrayNew.shape == (self.lStrip, 3):
            arrayNew = np.tile(arrayNew, (self.nStrips, 1))
            self.array = arrayNew
        elif arrayNew.shape == (self.nLed,   3):
            self.array = arrayNew
    def getArrayForDisplay(self):
        returnArray = self.array
        if self.minDisplay != 0: returnArray[returnArray < self.minDisplay] = 0
        return returnArray






#
class BassPixels():
    'neck then body then strap'
    def __init__(self, lNeck,lBody, lStrap, minDisplay):
        self.lNeck  = lNeck
        self.lBody  = lBody
        self.lStrap = lStrap
        self.nLed = lNeck*2 + lBody + lStrap
        self.minDisplay = minDisplay
        self.array      = np.zeros([self.nLed, 3])
    def updateNeck(self, arrayNew, alphaRise, alphaDecay):
        alpha = arrayNew - self.array[0:self.lNeck]
        alpha[alpha > 0.0 ] = alphaRise
        alpha[alpha <= 0.0] = alphaDecay
        self.array[0:self.lNeck] = alpha*arrayNew + (1.0-alpha)*self.array[0:self.lNeck]
        self.array[self.lNeck:2*self.lNeck] = alpha*arrayNew + (1.0-alpha)*self.array[self.lNeck:2*self.lNeck]
    def updateNeck1(self, arrayNew, alphaRise, alphaDecay):
        alpha = arrayNew - self.array[0:self.lNeck]
        alpha[alpha > 0.0 ] = alphaRise
        alpha[alpha <= 0.0] = alphaDecay
        self.array[0:self.lNeck] = alpha*arrayNew + (1.0-alpha)*self.array[0:self.lNeck]
    def updateNeck2(self, arrayNew, alphaRise, alphaDecay):
        alpha = arrayNew - self.array[self.lNeck:2*self.lNeck]
        alpha[alpha > 0.0 ] = alphaRise
        alpha[alpha <= 0.0] = alphaDecay
        self.array[self.lNeck:2*self.lNeck] = alpha*arrayNew + (1.0-alpha)*self.array[self.lNeck:2*self.lNeck]
    def updateBody(self, arrayNew, alphaRise, alphaDecay):
        alpha = arrayNew - self.array[self.lNeck*2:self.lNeck*2+self.lBody]
        alpha[alpha > 0.0 ] = alphaRise
        alpha[alpha <= 0.0] = alphaDecay
        self.array[self.lNeck*2:self.lNeck*2+self.lBody] = alpha*arrayNew + (1.0-alpha)*self.array[self.lNeck*2:self.lNeck*2+self.lBody]
    def updateStrap(self, arrayNew, alphaRise, alphaDecay):
        alpha = arrayNew - self.array[self.lNeck*2+self.lBody:]
        alpha[alpha > 0.0 ] = alphaRise
        alpha[alpha <= 0.0] = alphaDecay
        self.array[self.lNeck*2+self.lBody:] = alpha*arrayNew + (1.0-alpha)*self.array[self.lNeck*2+self.lBody:]
    def getArrayForDisplay(self):
        returnArray = self.array
        if self.minDisplay != 0: returnArray[returnArray < self.minDisplay] = 0
        return returnArray

class ExpFilter:
    """Temporal exponential smoothing filter
    """
    def __init__(self, val=0.0, alpha_decay=0.5, alpha_rise=0.5):
        """Small rise / decay factors = more smoothing"""
        self.alpha_decay = alpha_decay
        self.alpha_rise = alpha_rise
        self.value = val
    def update(self, value):
        if isinstance(self.value, (list, np.ndarray, tuple)):
            alpha = value - self.value
            alpha[alpha > 0.0] = self.alpha_rise
            alpha[alpha <= 0.0] = self.alpha_decay
        else:
            alpha = self.alpha_rise if value > self.value else self.alpha_decay
        self.value = alpha * value + (1.0 - alpha) * self.value

class Bouncer :
    def __init__(self, n, speed, color, nPixels):
        self.n = n
        self.speed = speed
        self.color=color/np.amax(color)
        self.color=self.color*255.0
        for i in range(0,3): self.color[i]=int(self.color[i])
        self.nPixels = nPixels
        self.locInt = 10
        self.locFloat = float(self.locInt)
        self.outArray = np.zeros([nPixels, 3])
        self.outZeros = np.zeros_like(self.outArray)
        for i in range(self.locInt-self.n, self.locInt+self.n+1):
            if i == self.locInt:
                self.outArray[i] = self.color
            else:
                self.outArray[i] = self.color
    def update(self):
        self.locFloat = self.locFloat + self.speed
        if int(self.locFloat) != self.locInt:
            self.locInt = int(self.locFloat)
            self.outArray = np.roll(self.outArray, int(np.sign(self.speed)), axis=0)
        if self.locInt == self.n or self.locInt == self.nPixels-1-self.n:
            self.speed = -self.speed
    def getFullOutArray(self):
        returnArray = self.outArray
        return returnArray.astype(int)


'''
def getColorWheel(nTot):
    colorWheel = np.zeros([nTot,3])
    nTot3 = nTot//3
    for n in range(nTot):
        if n <= nTot3:
            colorWheel[n,0] = 1.0 - float(n)/float(nTot3)
            colorWheel[n,1] = 0.0 + float(n)/float(nTot3)
            colorWheel[n,2] = 0.0
        elif nTot3 < n <= 2*nTot3:
            colorWheel[n,0] = 0.0
            colorWheel[n,1] = 1.0 - float(n-nTot3)/float(nTot3)
            colorWheel[n,2] = 0.0 + float(n-nTot3)/float(nTot3)
        elif 2*nTot3 < n <= nTot:
            colorWheel[n,0] = 0.0 + float(n-2*nTot3)/float(nTot3)
            colorWheel[n,1] = 0.0
            colorWheel[n,2] = 1.0 - float(n-2*nTot3)/float(nTot3)
    return colorWheel
'''

def getColorWheel(nTot):
    colorWheel = np.zeros([nTot,3])
    nTot3 = nTot//3
    for n in range(nTot):
        if n <= nTot3:
            colorWheel[n,0] = 1.0 - np.power(float(n)/float(nTot3), 1)
            colorWheel[n,1] = 0.0 + np.power(float(n)/float(nTot3), 1)
            colorWheel[n,2] = 0.0
        elif nTot3 < n <= 2*nTot3:
            colorWheel[n,0] = 0.0
            colorWheel[n,1] = 1.0 - np.power(float(n-nTot3)/float(nTot3), 1)
            colorWheel[n,2] = 0.0 + np.power(float(n-nTot3)/float(nTot3), 1)
        elif 2*nTot3 < n <= nTot:
            colorWheel[n,0] = 0.0 + np.power(float(n-2*nTot3)/float(nTot3), 1)
            colorWheel[n,1] = 0.0
            colorWheel[n,2] = 1.0 - np.power(float(n-2*nTot3)/float(nTot3), 1)
    return colorWheel

def getColorWheelRedBlue(nTot):
    colorWheel = np.zeros([nTot,3])
    for n in range(nTot):
            colorWheel[n,0] = 0.0 + np.power(float(n)/float(nTot), 0.25)
            colorWheel[n,1] = 0.0
            colorWheel[n,2] = 1.0 - np.power(float(n)/float(nTot), 4)
    return colorWheel



def clDisplay(powerNorm1):
    maxDisplay     = 100.0
    maxOutFactor   = 5
    segLen         = int(maxDisplay / maxOutFactor)
    powerNorm      = powerNorm1 * maxDisplay/maxOutFactor
    string1        = 'O' * int(min(powerNorm, maxDisplay))
    string2        = '-' * int(max(maxDisplay-powerNorm,0))
    finalString    = string1 + string2
    charList = list(finalString+'|')
    for i in range(maxOutFactor): charList[i*segLen]='|'
    finalString = ''.join(charList)
    print(finalString)
