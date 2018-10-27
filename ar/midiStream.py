import fastopc, time
import numpy as np
import mido
import time

####################################################
inputNames = mido.get_input_names()
print(inputNames)
inport     = mido.open_input(inputNames[0])
sleepTime  = 1.e-4
####################################################

class Board:
    def __init__(self):
        self.knobs      = np.zeros(8)
        self.pitchwheel = 0.0
        self.notes       = np.zeros(128)
    def update(self, msg):
        if msg.type == 'note_on':
            self.notes[msg.note] = 1
        elif msg.type == 'note_off':
            self.notes[msg.note] = 0
        elif msg.type == 'pitchwheel':
            self.pitchwheel = msg.pitch
        elif msg.type == 'control_change':
            self.knobs[msg.control] = msg.value

board = Board()
while True:
    for msg in inport.iter_pending():
        print(msg)
        board.update(msg)
        print('-'*80)
    time.sleep(sleepTime)










































#
