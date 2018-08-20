from __future__ import print_function
from __future__ import division
import time
import sys
import numpy as np
from numpy import *



class Runner:
    def __init__(self, n, speed, color, startLoc, nPixels):
        self.n = n
        self.speed = speed
        self.color = color
        self.locInt = startLoc
	self.nPixels = nPixels
        self.locFloat = float(self.locInt)
        self.outArray = np.zeros(nPixels)
        self.outZeros = np.zeros_like(self.outArray)
        for i in range(self.locInt-self.n, self.locInt+self.n+1):
            if i == self.locInt:
                self.outArray[i] = 1.0
            else:
                self.outArray[i] = np.power(1.0 - (np.abs(self.locInt-i)/n) + 0.1,2)
    def update(self):
        self.locFloat = self.locFloat + self.speed
        if int(self.locFloat) != self.locInt:
            self.locInt = int(self.locFloat)
            self.outArray = np.roll(self.outArray, int(np.sign(self.speed)))
        if self.locInt == self.n or self.locInt == self.nPixels-1-self.n:
            self.speed = -self.speed            
    def getFullOutArray(self):
        if self.color=='r':
            r = self.outArray
            g = self.outZeros
            b = self.outZeros
        elif self.color=='g':
            r = self.outZeros
            g = self.outArray
            b = self.outZeros
        elif self.color=='b':
            r = self.outZeros
            g = self.outZeros
            b = self.outArray
        elif self.color=='p':
            r = self.outArray
            g = self.outZeros
            b = self.outArray
	returnArray = np.array([r,g,b])*255
        return returnArray.astype(int)

def getColorWheel(nTot):
    colorWheel = np.zeros([3, nTot])
    nTot3 = nTot//3
    for n in range(nTot):
        if n < nTot3:
            colorWheel[0,n] = 1.0 - float(n)/float(nTot3)
            colorWheel[1,n] = 0.0 + float(n)/float(nTot3)
            colorWheel[2,n] = 0.0
        elif nTot3 < n < 2*nTot3:
            colorWheel[0,n] = 0.0
            colorWheel[1,n] = 1.0 - float(n-nTot3)/float(nTot3)
            colorWheel[2,n] = 0.0 + float(n-nTot3)/float(nTot3)
        elif 2*nTot3 < n < nTot:
            colorWheel[0,n] = 0.0 + float(n-2*nTot3)/float(nTot3)
            colorWheel[1,n] = 0.0
            colorWheel[2,n] = 1.0 - float(n-2*nTot3)/float(nTot3)
    return colorWheel

        
    
	







