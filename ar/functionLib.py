#!/usr/bin/env python

# Light each LED in sequence, and repeat.

#import fastopc, time
import numpy as np

class Pixels():
    def __init__(self, nStrips, lStrip, minDisplay):
        self.nStrips    = nStrips
        self.lStrip     = lStrip
		self.nLed       = nStrips*lStrip
		self.minDisplay = minDisplay
		self.array      = np.zeros([self.nLed, 3])
	def update(self, arrayNew, alphaRise, alphaDecay):
        if   arrayNew.shape == (self.lStrip, 3):
            arrayNew = np.tile(arrayNew, (self.nStrips, 1))
            alpha = arrayNew - self.array
            alpha[alpha > 0.0 ] = alphaRise
		    alpha[alpha <= 0.0] = alphaDecay
            self.array = alpha*arrayNew + (1.0-alpha)*self.array
	def getArrayForDisplay(self):
        elif arrayNew.shape == (self.nLed,   3):
            alpha = arrayNew - self.array
            alpha[alpha > 0.0 ] = alphaRise
		    alpha[alpha <= 0.0] = alphaDecay
            self.array = alpha*arrayNew + (1.0-alpha)*self.array
	def getArrayForDisplay(self):
		returnArray = self.array
		returnArray[returnArray < minDisplay] = 0
		return returnArray
