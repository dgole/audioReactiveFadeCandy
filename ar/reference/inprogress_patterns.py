# functioning_patterns
#
import sys
from classes import Pixel
import numpy as np
import time
from functioning_patterns  import PanelPattern
sys.path.insert(0, '../audioReactive/')
import micStream
import music
import patternHelpers

# randwalk pattern
class RandwalkPattern(PanelPattern):
    def __init__(self, m, n, numwalkers):
        PanelPattern.__init__( self, m, n )
        self.call_name = 'randwalk';

# audioReactive spectrum
class AudioReactiveBassPattern(PanelPattern):
    def __init__(self, m, n):
        PanelPattern.__init__(self, m, n)
        self.call_name = 'arBass';
        self.frameCount = 0
        self.frame_sleep_time = 0.0
        self.pix_np = np.zeros([3,self.m,self.n])
        self.stream = micStream.Stream(fps=40,nBuffers=8)
        self.volumeFilter   = music.ExpFilter(0.1, alpha_rise=0.1, alpha_decay=0.1)
        self.spectrumFilter = music.ExpFilter(np.zeros_like(self.stream.notes), alpha_rise=0.5, alpha_decay=0.25)
        self.colorWheel = patternHelpers.getColorWheel(3000)
        print(self.colorWheel)
    def update_pixel_arr(self):
        # update and change the pixel array
        success = self.stream.readAndCalc()
        if success:
            self.volumeFilter.update(np.mean(self.stream.noteSpectrum))
            self.spectrumFilter.update(self.stream.noteSpectrum)
            bassPower = np.mean(self.spectrumFilter.value[0:10])
            frameNumEff = self.frameCount%3000
            bassPower /= self.volumeFilter.value
            bassPower*=10
            print(bassPower)
            self.pix_np[0,0,:] = np.max([bassPower,10])*self.colorWheel[0, frameNumEff]
            self.pix_np[1,0,:] = np.max([bassPower,10])*self.colorWheel[1, frameNumEff]
            self.pix_np[2,0,:] = np.max([bassPower,10])*self.colorWheel[2, frameNumEff]
            midIndex = self.n//2
            temp = 10 + np.sqrt(bassPower)
            print(temp) 
            self.pix_np[0,0,midIndex-temp:midIndex+temp] = np.max([bassPower,10]) * self.colorWheel[0, frameNumEff-1000]
            self.pix_np[1,0,midIndex-temp:midIndex+temp] = np.max([bassPower,10]) * self.colorWheel[1, frameNumEff-1000]
            self.pix_np[2,0,midIndex-temp:midIndex+temp] = np.max([bassPower,10]) * self.colorWheel[2, frameNumEff-1000]            
            #self.pix_np = np.clip(self.pix_np, 0, 255)
            self.pixel_arr = [ [Pixel(self.pix_np[0,j,i],self.pix_np[1,j,i],self.pix_np[2,j,i]) for i in range(self.n) ] for j in range(self.m) ]
            self.frameCount+=1
        
        
    
# audioReactive spectrum
class AudioReactiveSpectrumPattern(PanelPattern):
    def __init__(self, m, n):
        PanelPattern.__init__(self, m, n)
        self.call_name = 'arSpectrum';
        self.frameCount = 0
        self.frame_sleep_time = 0.0
        self.pix_np = np.zeros([3,self.m,self.n])
        self.volThresh = 0.1
        self.stream = micStream.Stream(fps=40,nBuffers=8)
        self.volumeFilter   = music.ExpFilter(0.01, alpha_rise=0.1, alpha_decay=0.1)
        self.spectrumFilter = music.ExpFilter(np.zeros_like(self.stream.notes), alpha_rise=0.3, alpha_decay=0.3)
        #print(self.stream.freqs[0:10])
        #print(self.stream.freqs[-10:])
    def update_pixel_arr(self):
        # update and change the pixel array
        success = self.stream.readAndCalc()
        if success:
            self.volumeFilter.update(np.mean(self.stream.noteSpectrum))
            self.spectrumFilter.update(self.stream.noteSpectrum)
            if self.volumeFilter.value > self.volThresh:
                self.pix_np[0,0,:] = 1.0 * self.spectrumFilter.value / self.volumeFilter.value
            else:
                self.pix_np[0,0,:] = 0.0 
            self.pixel_arr = [ [Pixel(self.pix_np[0,j,i],self.pix_np[1,j,i],self.pix_np[2,j,i]) for i in range(self.n) ] for j in range(self.m) ]
            self.frameCount+=1
        if self.frameCount%10==0:
            print(self.volumeFilter.value)
            print(np.amax(5.0 * self.spectrumFilter.value / self.volumeFilter.value ))
            print(' ')
		
# audioReactive spectrum
class AudioReactiveScrollingPattern(PanelPattern):
    def __init__(self, m, n):
        PanelPattern.__init__(self, m, n)
        self.call_name = 'arScroll';
        self.frameCount = 0
        self.frame_sleep_time = 0.0
        self.pix_np = np.zeros([3,self.m,self.n])
        self.stream = micStream.Stream(fps=40,nBuffers=8)
        self.volumeFilter   = music.ExpFilter(0.01, alpha_rise=0.1, alpha_decay=0.1)
        self.spectrumFilter = music.ExpFilter(np.zeros_like(self.stream.notes), alpha_rise=0.5, alpha_decay=0.5)
        self.colorWheel = patternHelpers.getColorWheel(300)
    def update_pixel_arr(self):
        # update and change the pixel array
        success = self.stream.readAndCalc()
        if success:
            frameNumEff = self.frameCount%300
            self.volumeFilter.update(np.mean(self.stream.noteSpectrum))
            self.spectrumFilter.update(self.stream.noteSpectrum)
            bassPower = np.mean(self.spectrumFilter.value[0:10])
            bassPower /= self.volumeFilter.value
            bassPower = bassPower*bassPower
            print(bassPower)
            #print(self.volumeFilter.value)
            self.pix_np[0,0,:] = np.roll(self.pix_np[0,0,:], 1)
            self.pix_np[1,0,:] = np.roll(self.pix_np[1,0,:], 1)
            self.pix_np[2,0,:] = np.roll(self.pix_np[2,0,:], 1)
            self.pix_np[0,0,0] = bassPower*self.colorWheel[0, frameNumEff]
            self.pix_np[1,0,0] = bassPower*self.colorWheel[1, frameNumEff]
            self.pix_np[2,0,0] = bassPower*self.colorWheel[2, frameNumEff]
            self.pixel_arr = [ [Pixel(self.pix_np[0,j,i],self.pix_np[1,j,i],self.pix_np[2,j,i]) for i in range(self.n) ] for j in range(self.m) ]
            self.frameCount+=1
		
        
            
            
            
class AudioReactiveTheoryDemo(PanelPattern):
    def __init__(self, m, n):
        PanelPattern.__init__(self, m, n)
        self.call_name = 'arTheoryDemo';
        self.frameCount = 0
        self.frame_sleep_time = 0.0
        self.pix_np = np.zeros([3,self.m,self.n])
        self.stream = micStream.Stream()
        self.volume = music.ExpFilter(0.0, alpha_rise=0.8, alpha_decay=0.3)
        self.keyObj = music.Key(self.stream.notes)
        self.noteSumsObj = music.NoteSums(self.stream.notes)
        self.chordObj = music.Chord(self.stream.notes)
    def update_pixel_arr(self):
        # update and change the pixel array
        success = self.stream.readAndCalc()
        if success:
            self.volume.update(np.mean(self.stream.noteSpectrum))
            self.keyObj.update(self.stream.noteSpectrum)
            self.noteSumsObj.update(self.stream.noteSpectrum)
            self.chordObj.update(self.stream.noteSpectrum, self.keyObj.currentKeyNum)
            if self.frameCount%10==0:
                print(self.volume.value)
                self.keyObj.printKey()
                self.chordObj.printChord()
                self.noteSumsObj.printNoteSums()
            self.pix_np[:,:,:] = 0
            self.pix_np[0, 0, 0 :6 ] = 30
            self.pix_np[0, 0, 18:24] = 30
            self.pix_np[0, 0, 36:42] = 30
            self.pix_np[0, 0, 54:60] = 30
            self.pix_np[2, 0, 6+self.keyObj.currentKeyNum] = 100
            self.pix_np[2, 0, 24+self.chordObj.currentChordNum] = 100
            self.pix_np[2, 0, 42+np.argmax(self.noteSumsObj.newNoteSums)] = 100
            self.pixel_arr = [ [Pixel(self.pix_np[0,j,i],self.pix_np[1,j,i],self.pix_np[2,j,i]) for i in range(self.n) ] for j in range(self.m) ]
            self.frameCount+=1
 

class AudioReactiveBeat(PanelPattern):
    def __init__(self, m, n):
        PanelPattern.__init__(self, m, n)
        self.call_name = 'arBeat';
        self.frameCount = 0
        self.frame_sleep_time = 0.0
        self.pix_np = np.zeros([3,self.m,self.n])
        self.stream = micStream.Stream(fps=60,nBuffers=6)
        self.beat = music.Beat(self.stream.freqs)
    def update_pixel_arr(self):
        success = self.stream.readAndCalc()
        if success:
            self.beat.update(self.stream.freqSpectrum)
            if self.beat.beatRightNow():
                self.pix_np[2, 0, :] = 50
            else:
                self.pix_np[2, 0, :] = 0
            self.pixel_arr = [ [Pixel(self.pix_np[0,j,i],self.pix_np[1,j,i],self.pix_np[2,j,i]) for i in range(self.n) ] for j in range(self.m) ]
            self.frameCount+=1


class HoodBounce(PanelPattern):
    def __init__(self, m, n):
        PanelPattern.__init__(self, m, n)
        self.call_name = 'hoodBounce';
        self.frame_sleep_time = 0.0
        self.pix_np = np.zeros([3,self.m,self.n])
	self.filter = music.ExpFilter(np.zeros(self.n), alpha_rise=0.05, alpha_decay=0.05)
        self.runnerList = []
        self.runnerList.append(patternHelpers.Runner(np.random.randint(1,high=2), np.random.rand()*0.1+0.05, 'r', 30, self.n)) 
        self.runnerList.append(patternHelpers.Runner(np.random.randint(1,high=2), np.random.rand()*0.1+0.05, 'p', 30, self.n)) 
        self.runnerList.append(patternHelpers.Runner(np.random.randint(1,high=2), np.random.rand()*0.1+0.05, 'b', 30, self.n))
    def update_pixel_arr(self):
        for runner in self.runnerList: runner.update()
        self.pix_np[:,0,:] = 0
        for runner in self.runnerList: self.pix_np[:,0,:] += runner.getFullOutArray()
        self.pix_np /= len(self.runnerList)
        self.filter.update(self.pix_np[:,0,:])
        self.pix_np[:,0,:] = self.filter.value
        self.pixel_arr = [ [Pixel(self.pix_np[0,j,i],self.pix_np[1,j,i],self.pix_np[2,j,i]) for i in range(self.n) ] for j in range(self.m) ]


class StripBounce(PanelPattern):
    def __init__(self, m, n):
        PanelPattern.__init__(self, m, n)
        self.call_name = 'stripBounce';
        self.frame_sleep_time = 0.0
        self.pix_np = np.zeros([3,self.m,self.n])
	self.filter = music.ExpFilter(np.zeros(self.n), alpha_rise=0.05, alpha_decay=0.05)
        self.runnerList = []
        self.runnerList.append(patternHelpers.Runner(np.random.randint(1,high=8), np.random.rand()*0.3+0.05, 'r', 30, self.n)) 
        self.runnerList.append(patternHelpers.Runner(np.random.randint(1,high=8), np.random.rand()*0.3+0.05, 'p', 30, self.n)) 
        self.runnerList.append(patternHelpers.Runner(np.random.randint(1,high=8), np.random.rand()*0.3+0.05, 'b', 30, self.n))
        self.runnerList.append(patternHelpers.Runner(np.random.randint(1,high=8), np.random.rand()*0.3+0.05, 'g', 30, self.n))
        self.runnerList.append(patternHelpers.Runner(np.random.randint(1,high=8), np.random.rand()*0.3+0.05, 'r', 30, self.n))
    def update_pixel_arr(self):
        for runner in self.runnerList: runner.update()
        self.pix_np[:,0,:] = 0
        for runner in self.runnerList: self.pix_np[:,0,:] += runner.getFullOutArray()
        self.pix_np /= len(self.runnerList)
        self.filter.update(self.pix_np[:,0,:])
        self.pix_np[:,0,:] = self.filter.value
        self.pixel_arr = [ [Pixel(self.pix_np[0,j,i],self.pix_np[1,j,i],self.pix_np[2,j,i]) for i in range(self.n) ] for j in range(self.m) ]
        
        
class HoodFlash(PanelPattern):
    def __init__(self, m, n):
        PanelPattern.__init__(self, m, n)
        self.call_name = 'hoodFlash';
        self.frame_sleep_time = 0.0
        self.pix_np = np.zeros([3,self.m,self.n])
        self.sleeveL = np.zeros([3, 40])
        self.sleeveR = np.zeros([3, 40])
        self.head    = np.zeros([3, 30])
        self.colorWheel = patternHelpers.getColorWheel(300)
        self.frameNum=0
    def update_pixel_arr(self):
        frameNumEff = self.frameNum%300
        self.sleeveL[0,:] = 255.0 * self.colorWheel[0, frameNumEff - 0  ]
        self.sleeveL[1,:] = 255.0 * self.colorWheel[1, frameNumEff - 0  ]
        self.sleeveL[2,:] = 255.0 * self.colorWheel[2, frameNumEff - 0  ]
        self.sleeveR[0,:] = 255.0 * self.colorWheel[0, frameNumEff - 100]
        self.sleeveR[1,:] = 255.0 * self.colorWheel[1, frameNumEff - 100]
        self.sleeveR[2,:] = 255.0 * self.colorWheel[2, frameNumEff - 100]
        self.head   [0,:] = 255.0 * self.colorWheel[0, frameNumEff - 200]
        self.head   [1,:] = 255.0 * self.colorWheel[1, frameNumEff - 200]
        self.head   [2,:] = 255.0 * self.colorWheel[2, frameNumEff - 200]
        self.frameNum+=1
        self.pix_np[:, 0, 0 :40 ] = self.sleeveL
        self.pix_np[:, 0, 40:70 ] = self.head
        self.pix_np[:, 0, 70:110] = self.sleeveR
        self.pixel_arr = [ [Pixel(self.pix_np[0,j,i],self.pix_np[1,j,i],self.pix_np[2,j,i]) for i in range(self.n) ] for j in range(self.m) ]































