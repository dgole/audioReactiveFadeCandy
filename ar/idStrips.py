#!/usr/bin/env python

import fastopc, time
import numpy as np
import functionLib as lib

nStrips = 8
lStrip  = 64
nLed    = nStrips*lStrip
client = fastopc.FastOPC('localhost:7890')

on = np.zeros(nLed,3)
for i in range(0, nStrips):
    base=lStrip*i
    on[base:base+i+1]  = [0,0,255]
off = np.zeros_like(on)

while True:
    client.putPixels(0, on)
    time.sleep(0.5)
    client.putPixels(0, off)
    time.sleep(0.5)
