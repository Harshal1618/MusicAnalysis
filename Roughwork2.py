# -*- coding: utf-8 -*-
"""
Created on Fri Jun 22 09:03:46 2018

@author: hsamant
"""

import numpy as np
from scipy.io import wavfile
from scipy.fftpack import fft
import matplotlib.pyplot as plt

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


top_freq = np.array([10.0,17.0,29.0])
top_freq_amp = np.array([1.0, 0.7, 0.5])
top_freq_phase = np.array([0.0, np.pi*30/180, np.pi*60/180])
soundData = createSoundData(top_freq, top_freq_amp, top_freq_phase,i_time = 2, f_amp = 50 / len(top_freq))

i_framerate = 44100
wavfile.write('createsound_Try1_20180622_v3.wav',i_framerate,soundData)

fs, data = wavfile.read('./createsound_Try1_20180622_v3.wav') # load the data
top_freq1 , top_freq_amp1, top_freq_phase1 = findFrequencies(data, i_framerate = 44100 , i_top_n = 3)

print('Frequencies: ',top_freq1)
print('Amplitudes : ',top_freq_amp1) 
print('Phase :' , top_freq_phase1)




#i_framerate = 40 # number of samples in each second
#
#i_time = 1 # duration in seconds
#i_frq1 = 2 # freq of signal
#i_phs1 = np.pi * 0 / 180 # phase of signal
#
#x = np.linspace(0,i_framerate * i_time -1, i_framerate * i_time)
#y1 = np.cos( 2 * np.pi* x * i_frq1 / i_framerate + i_phs1)
#
#plt.plot(x,y1)
#plt.plot(x[10],y1[10],'r.')
#
#ft = fft(y1)
#xf = np.linspace(0,int(i_framerate/2.0),int((i_framerate/2.0))+1) /2 # Need to find out this last /2 part
#yf = ft[:int((i_framerate//2.0))+1]
#
#yf_top_n = np.argsort(np.abs(yf))[-1:][::-1]
#amp_top_n =  np.abs(yf)[yf_top_n] #/ np.max(np.abs(yf)[yf_top_n])
#freq_top_n = xf[yf_top_n]
#phase_top_n = np.angle(yf)[yf_top_n]
#
#print ('Frequencies: ',freq_top_n)
#print('Amplitudes : ',amp_top_n) 
#print('Phase :' , phase_top_n * 180 / np.pi)