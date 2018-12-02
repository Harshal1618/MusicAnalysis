# -*- coding: utf-8 -*-
"""
Created on Fri Jun 22 09:51:17 2018

@author: hsamant
"""

import numpy as np
import pylab as pl

num_t = 100000
t = np.linspace(0,1,num_t)
dt = 1.0/num_t
w = 2.0*np.pi*30.0
phase = np.pi/2.0

amp = np.fft.rfft(np.cos(w*t+phase))
freqs = np.fft.rfftfreq(t.shape[-1],dt)

print (np.arctan2(amp.imag,amp.real))[30]

pl.subplot(211)
pl.plot(freqs[:60],np.sqrt(amp.real**2+amp.imag**2)[:60])
pl.subplot(212)
pl.plot(freqs[:60],(np.arctan2(amp.imag,amp.real))[:60])
pl.show()