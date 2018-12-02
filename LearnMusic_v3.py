#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 20 23:00:04 2018

@author: harshal
"""

## read a musical note
import numpy as np
from scipy.io import wavfile
from scipy.fftpack import fft
import matplotlib.pyplot as plt

i_framerate = 44100
fs, data = wavfile.read('./Flute.nonvib.ff.A4.stereo.wav') # load the data

def findFrequencies(arr_data, i_framerate = 44100, i_top_n =5):
    a = arr_data.T[0] # this is a two channel soundtrack, I get the first track
#    b=[(ele/2**8.)*2-1 for ele in a] # this is 8-bit track, b is now normalized on [-1,1)
    y = fft(a) # calculate fourier transform (complex numbers list)
    
    xf = np.linspace(0,int(i_framerate/2.0),int((i_framerate/2.0))+1) /2 # Need to find out this last /2 part
    yf = y[:int((i_framerate//2.0))+1]
    
    plt.plot(xf,np.abs(yf))
    
    yf_top_n = np.argsort(np.abs(yf))[-i_top_n:][::-1]
    amp_top_n =  np.abs(yf)[yf_top_n] / np.max(np.abs(yf)[yf_top_n])
    freq_top_n = xf[yf_top_n]
    phase_top_n = np.angle(yf)[yf_top_n]
    
    return freq_top_n, amp_top_n, phase_top_n

def createSoundData(a_freq, a_amp,a_phase, i_framerate=44100, i_time = 1, f_amp = 1.0):
    n_samples = i_time * i_framerate
    
    x = np.linspace(0,n_samples -1, n_samples)
    y = np.zeros(n_samples)
    for i in range(len(a_freq)):
        y += np.cos(2 * np.pi *x *a_freq[i] / i_framerate + a_phase[i])* f_amp * a_amp[i]
    data2 = np.c_[y,y] # 2 Channel sound
    return data2
    
top_freq , top_freq_amp, top_freq_phase = findFrequencies(data, i_framerate = 44100 , i_top_n = 150)

print('Frequencies: ',top_freq)
print('Amplitudes : ',top_freq_amp) 
print('Phase :' , top_freq_phase)

soundData = createSoundData(top_freq, top_freq_amp, top_freq_phase,i_time = 2, f_amp = 10 / len(top_freq))
wavfile.write('createsound_A4_20180622_v3.wav',i_framerate,soundData)
