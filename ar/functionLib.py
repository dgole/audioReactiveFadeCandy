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
    
    
