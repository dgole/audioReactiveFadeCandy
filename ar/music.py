from __future__ import print_function
from __future__ import division
import time
import sys
import numpy as np
from numpy import *
from scipy.ndimage.filters import gaussian_filter1d
#import config
import functionLib as lib


def getNotesToKeyMatrix(noteList, weights):
    matrix = np.zeros([12, len(noteList)])
    for i in range(12):
        for note in noteList:
            scaleDegree = ((note-i%12)%12)-1
            matrix[i,note-noteList[0]] = weights[scaleDegree]
    return matrix

class Key:
    def __init__(self, noteList,
                 #          1      2      3  4      5      6      7
                 weights = [3.,-1.,1.,-1.,1.,2.,-5.,3.,-1.,2.,-5.,1.],
                 alpha   = 0.00025):
        self.keySums = lib.ExpFilter(np.ones(12), alpha_rise=alpha, alpha_decay=alpha)
        self.matrix = getNotesToKeyMatrix(noteList, weights)
        self.keyStringList = ['c  ', 'cs ', 'd  ', 'ef ',
                              'e  ', 'f  ', 'fs ', 'g  ',
                              'af ', 'a  ', 'bf ', 'b  ' ]
        self.currentKeyNum = 0
    def update(self, newNoteSpectrum):
        newKeySums = np.dot(self.matrix, newNoteSpectrum)
        self.keySums.update(newKeySums)
        self.currentKeyNum = np.argmax(self.keySums.value)
    def printKey(self):
        sortedValues = np.sort(self.keySums.value)
        sortedNames = list(self.keyStringList[i] for i in np.argsort(self.keySums.value))
        surety = np.round(100 * (sortedValues[-1]/sortedValues[-2] - 1.),1)
        print("most likely key is: " + self.keyStringList[self.currentKeyNum] + " " + str(surety) + "%")
        print(np.fliplr([sortedNames])[0][0:7])
        print(np.round(np.fliplr([sortedValues])[0],0)[0:7])


class NoteSums:
    def __init__(self, noteList, alpha=0.001):
        self.noteSums = lib.ExpFilter(np.ones(12), alpha_rise=alpha, alpha_decay=alpha)
        self.matrix   = getNotesToKeyMatrix(noteList, [1.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.])
        self.newNoteSums = np.zeros(12)
        self.noteStringList = ['c  ', 'cs ', 'd  ', 'ef ',
                              'e  ', 'f  ', 'fs ', 'g  ',
                              'af ', 'a  ', 'bf ', 'b  ' ]
    def update(self, newNoteSpectrum):
        self.newNoteSums = np.dot(self.matrix, newNoteSpectrum)
        self.noteSums.update(self.newNoteSums)
    def printNoteSums(self):
        print("most used notes are: ")
        sortedValues = np.sort(self.noteSums.value)
        sortedNames = list(self.noteStringList[i] for i in np.argsort(self.noteSums.value))
        print(np.fliplr([sortedNames])[0][0:7])
        print(np.round(np.fliplr([sortedValues])[0],0)[0:7])

'''
class Chord:
    def __init__(self, noteList):
        # define the 7 x notes matrix for each of 12 possible keys.
        #                           c     d     e  f     g     a       b
        chordRefMatrix = np.array([[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11] for i in range(6)])
        weights        = np.array([[1 ,0 ,0 ,0 ,1 ,0 ,0, 1 ,0 ,0 ,0 , 0 ],
                                   [0 ,0 ,1 ,0 ,0 ,1 ,0, 0 ,0 ,1 ,0 , 0 ],
                                   [0 ,0 ,0 ,0 ,1 ,0 ,0, 1 ,0 ,0 ,0 , 1 ],
                                   [1 ,0 ,0 ,0 ,0 ,1 ,0, 0 ,0 ,1 ,0 , 0 ],
                                   [0 ,0 ,1 ,0 ,0 ,0 ,0, 1 ,0 ,0 ,0 , 1 ],
                                   [1 ,0 ,0 ,0 ,1 ,0 ,0, 0 ,0 ,1 ,0 , 0 ]])
        self.chordMatrixList = []
        for i in range(12):
            self.chordMatrixList.append(np.zeros([7,len(noteList)]))
        for keyNum in range(12):
            for chordNum in range(6):
                for note in noteList:
                    scaleDegree = (note-keyNum%12)%12 -1
                    if scaleDegree in chordRefMatrix[chordNum]:
                        arg = np.argmin(np.abs(chordRefMatrix[chordNum]-scaleDegree))
                        self.chordMatrixList[keyNum][chordNum, note-noteList[0]] = weights[chordNum, arg]
                    else:
                        self.chordMatrixList[keyNum][chordNum, note-noteList[0]] = 0.0
        self.chordSums = ExpFilter(np.zeros(7), alpha_rise=0.01, alpha_decay=0.01)
        self.chordStringList = ['I', 'ii', 'iii', 'IV', 'V', 'vi', 'vii']
        self.currentChordNum = 0
    def update(self, newNoteSpectrum, currentKeyNum):
        newChordSums = np.dot(self.chordMatrixList[currentKeyNum], newNoteSpectrum)
        self.chordSums.update(newChordSums)
        self.currentChordNum = np.argmax(self.chordSums.value)
    def printChord(self):
        print("most likely chord is " + self.chordStringList[self.currentChordNum])
        print(np.round(self.chordSums.value,0))
'''

class Beat:
    def __init__(self, thresh=1.3, waitFrames=4):
        self.thresh = thresh
        self.waitFrames = waitFrames
        self.recentBeat = 0
        self.powerNorm = np.asarray([0.,0.,0.])
        self.beatNow = False
    def update(self, powerNorm):
        self.beatNow = False
        self.powerNorm[2] = self.powerNorm[1]
        self.powerNorm[1] = self.powerNorm[0]
        self.powerNorm[0] = powerNorm
        if self.powerNorm[2]<self.powerNorm[1] and self.powerNorm[1]>self.powerNorm[0] and self.powerNorm[1] > self.thresh and self.recentBeat<=0:
            self.recentBeat = self.waitFrames
            self.beatNow = True
        self.recentBeat-=1
    def getBeatStatus(self):
        return self.beatNow
