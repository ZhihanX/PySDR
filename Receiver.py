import numpy as np
import adi
import matplotlib.pyplot as plt
from scipy import signal

sample_rate = 1000e3 # Hz
center_freq = 2450e6 # Hz
num_samps = 10000 # number of samples returned per call to rx()
FsStop1 = 1e3
FsStop2 = 20e3


sdr = adi.Pluto('ip:192.168.4.1')
sdr.gain_control_mode_chan0 = 'manual'
sdr.rx_hardwaregain_chan0 = 70.0 # dB
sdr.rx_lo = int(center_freq)
sdr.sample_rate = int(sample_rate)
sdr.rx_rf_bandwidth = int(sample_rate) # filter width, just set it to the same as sample rate for now
sdr.rx_buffer_size = num_samps

b,a = signal.butter(8,[2.0*FsStop1/sample_rate,2.0*FsStop2/sample_rate],'bandpass')

rx_samples = sdr.rx() # receive samples off Pluto
#rx_samples = signal.filtfilt(b,a,rx_samples)
psd = np.abs(np.fft.fftshift(np.fft.fft(rx_samples)))**2/(sample_rate* num_samps)
psd_dB = 10*np.log10(psd)
f = np.linspace(sample_rate/-2, sample_rate/2, len(psd))
# Plot time domain
plt.figure(0)
plt.plot(rx_samples[1000:3500])
plt.xlabel("Time")
# plt.figure(3)
# plt.plot(rx_samples[1000:1100])
# plt.xlabel("Time")
# plt.figure(4)
# plt.plot(rx_samples)
# plt.xlabel("Time")
# plt.figure(2)
# plt.scatter(np.real(rx_samples[1000:1500]),np.imag(rx_samples[1000:1500]))
# plt.xlabel("Real")
# plt.ylabel("Imagine")
# Plot freq domain
# psd = np.abs(np.fft.fftshift(np.fft.fft(rx_samples)))**2
# psd_dB = 10*np.log10(psd)
# f = np.linspace(sample_rate/-2, sample_rate/2, len(psd))

# print(np.real(rx_samples[1000:10000])+np.imag(rx_samples[1000:10000]))
# Plot time domain
# plt.figure(0)
# plt.plot(np.real(rx_samples[0:10000]))
# plt.plot(np.imag(rx_samples[0:10000]),"yellow")
# plt.xlabel("Time")

# plt.figure(2)
# plt.scatter(np.real(rx_samples[1000:10000]),np.imag(rx_samples[1000:10000]))
# plt.xlabel("Real")
# plt.ylabel("Imagine")
# # plt.plot(np.imag(rx_samples[0:20000])
# plt.figure(3)
# plt.plot(np.sqrt(np.real(rx_samples[1000:10000])**2+(np.imag(rx_samples[1000:10000]))**2))
# plt.xlabel("Mag")
# plt.figure(4)

# plt.plot(abs(np.real(rx_samples[1000:10000])/2**14)+abs(np.imag(rx_samples[1000:10000]/2**14)))
# plt.xlabel("Distance")
# plt.figure(5)
# plt.scatter(np.real(rx_samples[2000:3000]),np.imag(rx_samples[2000:3000]))
# print(rx_samples[2000:2010])
# plt.figure(6)
# plt.plot(np.sqrt(np.real(rx_samples[2000:2010])**2+(np.imag(rx_samples[2000:2010]))**2))
# print()
# plt.figure(1)
# plt.plot(f/1e6, psd_dB)
# plt.xlabel("Frequency [MHz]")
# plt.ylabel("PSD")
# plt.show()
plt.figure(1)
plt.plot(f/1e6, psd_dB)
plt.xlabel("Frequency [MHz]")
plt.ylabel("PSD")
plt.show()
