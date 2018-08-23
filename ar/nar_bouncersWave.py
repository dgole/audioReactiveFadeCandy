#!/usr/bin/env python

# Light each LED in sequence, and repeat.

import fastopc, time
import numpy as np
import functionLib as lib

nStrips = 16
lStrip  = 64

client = fastopc.FastOPC('localhost:7890')

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

pixels = lib.Pixels(nStrips, lStrip, 20)
theoStrip = np.zeros([nStrips*lStrip, 3])

bouncerList = []
bouncerList.append(Bouncer(5, 0.1,   (10,0,0), 64))
bouncerList.append(Bouncer(5, 0.101, (10,0,5), 64))
bouncerList.append(Bouncer(5, 0.102, (10,0,8), 64))
bouncerList.append(Bouncer(5, 0.103, (10,0,10), 64))
bouncerList.append(Bouncer(5, 0.104, (10,0,10), 64))
bouncerList.append(Bouncer(5, 0.105, (8,0,10), 64))
bouncerList.append(Bouncer(5, 0.106, (5,0,10), 64))
bouncerList.append(Bouncer(5, 0.107, (0,0,10), 64))


while True:
    for i in range(0,8):
        stripNum = i
        base = stripNum*lStrip*2
        theoStrip[base:base+lStrip] = bouncerList[i].getFullOutArray()
        base = stripNum*lStrip*2+lStrip
        theoStrip[base:base+lStrip] = bouncerList[i].getFullOutArray()
        bouncerList[i].update()
    pixels.update(theoStrip, 0.5, 0.5)
    #print((pixels.getArrayForDisplay())[0:64,0])
    client.putPixels(0, pixels.getArrayForDisplay())
    #time.sleep(0.01)


