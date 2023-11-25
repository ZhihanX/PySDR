
import numpy as np
import adi
import matplotlib.pyplot as plt
from scipy import signal
import time

sample_rate = 1e6 
center_freq = 2450e6 
center_freq_rx = center_freq + 25000
num_samps = 10000 
# sdr_server = adi.Pluto("ip:192.168.4.1")
# sdr_server.sample_rate = int(sample_rate)
# sdr_server.tx_buffer_size = num_samps
# sdr_server.tx_rf_bandwidth = int(sample_rate) 
# sdr_server.tx_lo = int(center_freq)
# sdr_server.tx_hardwaregain_chan0 = 0
# sdr_server.rx_hardwaregain_chan0 = 70.0 
# sdr_server.rx_lo = int(center_freq_rx)
# sdr_server.rx_rf_bandwidth = int(sample_rate) 
# sdr_server.rx_buffer_size = num_samps
N = 10000 
t = np.arange(N/10)/sample_rate

samples = np.exp(2.0j*np.pi*100e3*t) 
samples0 = 0.05*np.exp(0*t) 
samples1 = 0.2*np.exp(0*t) 
samples2 = 0.4*np.exp(0*t)
samples3 = 0.6*np.exp(0*t)
samples4 = 0.4*np.exp(0*t)
samples5 = 0.2*np.exp(0*t)
samples = np.concatenate((samples0,samples1,samples0, samples2,samples0,samples3,samples0,samples4,samples0,samples5))

# for i in range(4):
#     samples = np.concatenate((samples,samples1, samples2))

samples *= 2**14
# psd = np.abs(np.fft.fftshift(np.fft.fft(samples)))**2/(sample_rate* num_samps)
# psd_dB = 10*np.log10(psd)
# f = np.linspace(sample_rate/-2, sample_rate/2, len(psd))
# plt.figure(4)
# plt.plot(f/1e6, psd_dB)
# plt.xlabel("Frequency [MHz]") 
# plt.ylabel("PSD")
# plt.figure(0)
# plt.plot(samples)

# sdr_server.tx_cyclic_buffer = True 
# print(np.average(np.sqrt(np.real(samples)**2+(np.imag(samples))**2)))
#filter
lo,hi = 3000,120e3
b,a = signal.butter(6, [2*lo/sample_rate], btype='low')
#sensor setting
sdr_sensor = adi.Pluto("ip:192.168.2.1")
sdr_sensor.gain_control_mode_chan0 = 'manual'
sdr_sensor.sample_rate = int(sample_rate)
sdr_sensor.tx_buffer_size = num_samps
sdr_sensor.tx_rf_bandwidth = int(sample_rate) 
sdr_sensor.tx_lo = int(center_freq)
sdr_sensor.tx_hardwaregain_chan0 = 0
sdr_sensor.tx_cyclic_buffer = True 
sdr_sensor.rx_hardwaregain_chan0 = 70.0 
sdr_sensor.rx_lo = int(center_freq_rx)
sdr_sensor.rx_rf_bandwidth = int(sample_rate) 
sdr_sensor.rx_buffer_size = num_samps*3

#####pulse shaping#####
x = samples
num_taps = 1001
beta = 0.35
Ts = 300 #change this
t = np.arange(num_taps) - (num_taps-1)//2
h = 1/Ts*np.sinc(t/Ts) * np.cos(np.pi*beta*t/Ts) / (1 - (2*beta*t/Ts)**2)
x_shaped = np.convolve(x,h)
# plt.figure(5)
# plt.plot(h)
# plt.xlabel("time")
# plt.figure(2)
# plt.plot(x_shaped)
# plt.xlabel("time")
# plt.xlabel("time")
# plt.figure(2)
# plt.plot(x_shaped)
# plt.xlabel("time")
# plt.ylabel("Shaped Signal")
# plt.ylabel("Shaped Signal")
#####raised-cosine filter#####

# sdr_server.tx_destroy_buffer()
# sdr_server.tx(x_shaped)
# time.sleep(0.1)
for i in range(10):
    raw_data = sdr_sensor.rx()
#Wait for the server
raw_data.real = raw_data.real*raw_data.real
raw_data.imag = raw_data.imag*(-raw_data.imag)
print(np.median( raw_data.real ))
if(np.median( raw_data.real )>800):
    print("Got the signal")
    for i in range(10):
        raw_data = sdr_sensor.rx()
else :
    print("Wrong")
###
rx_samples = sdr_sensor.rx()  #receive signal

plt.figure(6)
plt.plot(rx_samples)
rx_samples.real = rx_samples.real*rx_samples.real
rx_samples.imag = rx_samples.imag*match_filter#######
rx_samples_mid = []
print("max axis:", max_index)
if(max_index<10000):
   
    rx_samples_mid = rx_samples[max_index+4500:max_index+15500]

elif(max_index>20000):
    
    rx_samples_mid = rx_samples[max_index-16500:max_index-5500]
   
else:
    
    rx_samples_mid = rx_samples[max_index-5500:max_index+5500]
    
peaks, _ = signal.find_peaks(rx_samples_mid,distance=1700)
widths = signal.peak_widths(rx_samples_mid,peaks,rel_height = 0.15)
avg_p = 0
for i in range(5):
    avg_p += np.average(rx_samples_mid.real[int(widths[2][i]):int(widths[3][i])])
avg_p = np.sqrt(avg_p/5)
print("avg:",avg_p)
plt.figure(11)
plt.plot(rx_samples_mid)
plt.hlines(*widths[1:],color="C3")
print(len(rx_samples_mid))
##################################


# rx_samples =  signal.lfilter(b,a,rx_samples) 
# psd = np.abs(np.fft.fftshift(np.fft.fft(rx_samples)))**2/(sample_rate* num_samps)
# psd_dB = 10*np.log10(psd)
# f = np.linspace(sample_rate/-2, sample_rate/2, len(psd))
# plt.figure(3)
# plt.plot(f/1e6, psd_dB)
# plt.xlabel("Frequency [MHz]")
# plt.ylabel("PSD")
plt.figure(1)
plt.plot(rx_samples[0:40000])


# raw_data.real = raw_data.real*raw_data.real
# raw_data.imag = raw_data.imag*(-raw_data.imag)
print("raw_data",np.average(raw_data.real))
# plt.figure(5)
# plt.plot(raw_data)

plt.show()