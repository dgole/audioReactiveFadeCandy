#!/usr/bin/env python

# Light each LED in sequence, and repeat.

import fastopc, time
import numpy as np
import functionLib as lib

nStrips = 16
lStrip  = 64

#client = fastopc.FastOPC('localhost:7890')

class Bouncer :
    def __init__(self, n, speed, color, nPixels):
        self.n = n
        self.speed = speed
        self.color=color/np.amax(color)
        self.color=int(self.color*255)
        print(np.amax(self.color))
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

nBouncers = 32
pixels = lib.Pixels(nStrips, lStrip, 20)
theoStrip = np.zeros([nStrips*lStrip, 3])

bouncerList = []
for i in range(32): 
    bouncerList.append(Bouncer(np.random.randint(1,high=8), np.random.rand()*0.3+0.05, np.random.randint(0, 255, size=3), 64))
    print(bouncerList[i].color)


'''
while True:
    for i in range(0,nBouncers):
        stripNum = np.mod(i, nStrips)
        base = stripNum*lStrip
        theoStrip[base:base+lStrip] = bouncerList[i].getFullOutArray()
        bouncerList[i].update()
    pixels.update(theoStrip, 0.5, 0.5)
    print((pixels.getArrayForDisplay())[0:64])
    #client.putPixels(0, pixels.getArrayForDisplay())
    #time.sleep(0.01)
'''

