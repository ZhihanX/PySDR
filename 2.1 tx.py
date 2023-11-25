import matplotlib.pyplot as plt
import numpy as np
import adi
import time

sample_rate = 2.084e6 # Hz
center_freq = 2450e6 # Hz
num_samps = 10000

sdr = adi.Pluto("ip:192.168.2.1")
sdr.sample_rate = int(sample_rate)
sdr.tx_buffer_size = num_samps
sdr.tx_rf_bandwidth = int(sample_rate) # sample rate
sdr.tx_lo = int(center_freq)
sdr.tx_hardwaregain_chan0 = -10 #valid range is -90 to 0 dB
#sdr.tx_cyclic_buffer = True #repeat transmitting
N = 10000 # number of samples to transmit at once
t = np.arange(N)/sample_rate

Pilot = np.fromfile("pilot.txt",np.int16) # get pilot from txt file and convert it to complex number
# for i in range(len(Pilot)):
#     Pilot[i] -= 11312
# pack = int(N/len(Pilot))

# for i in range(len(Pilot)):
#     print(i)
#     t = t1[int(i*pack):int((i+1)*pack)]
#     if(Pilot[i]==1):
#         print(1)
#         samples1 = 0.5*np.sign(np.exp(2.0j*np.pi*100e3*t)) 
#         samples.extend(samples1)
#         print(len(samples))
#     else:
#         print(0)
#         samples2 = 0.5*np.sign(np.exp(1.0j*np.pi*100e3*t)) 
#         samples.extend(samples2) 
#         print(len(samples))
# samples1=0.5*np.exp(2.0j*np.pi*100e3*t*(0.2)) # diff fre ofdm
# samples2=0.5*np.exp(2.0j*np.pi*100e3*t*(0.4))
# samples3=0.5*np.exp(2.0j*np.pi*100e3*t*(0.6))
# samples4=0.5*np.exp(2.0j*np.pi*100e3*t*(0.8))
# samples = samples1+samples2+samples3+samples4
# samples =0.5*np.exp(2.0j*np.pi*100e3*t*(0.1))
# print (len(samples))
# print(samples)
# times = 1
# samples = np.tile(samples,times)

# for bit in samples:
#     pulse = np.zeros(sps)
#     pulse[0] += 1
#     samples = np.concatenate((samples,pulse))


samples*= 2**14 # The PlutoSDR expects samples to be between -2^14 and +2^14, not -1 and +1 like some SDRs
plt.figure(0)
plt.plot(np.real(samples[1000:1100]))

psd = np.abs(np.fft.fftshift(np.fft.fft(samples)))**2/(sample_rate* num_samps)
psd_dB = 10*np.log10(psd)
f = np.linspace(sample_rate/-2, sample_rate/2, len(psd))
plt.figure(1)
plt.plot(f/1e6, psd_dB)
plt.xlabel("Frequency [MHz]")
plt.ylabel("PSD")
plt.show()
# Transmit our batch of samples 100 times, so it should be 1 second worth of samples total, if USB can keep up
# sdr.tx_destroy_buffer()
for i in range(100000):
  sdr.tx(samples) # transmit the batch of samples once

