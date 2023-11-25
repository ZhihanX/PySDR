import numpy as np
import adi
import matplotlib.pyplot as plt
from scipy import signal
import time

sample_rate = 1e6 
center_freq = 2450e6 
center_freq_rx = center_freq 
num_samps_tx = 10000 
num_samps_rx = 10000  

N = 10000 
t = np.arange(N/10)/sample_rate
samples0 = 0.05*np.exp(0*t) 
samples1 = 0.2*np.exp(0*t) 
samples2 = 0.4*np.exp(0*t)
samples3 = 0.6*np.exp(0*t)
samples4 = 0.4*np.exp(0*t)
samples5 = 0.2*np.exp(0*t)
samples = np.concatenate((samples0,samples1,samples0, samples2,samples0,samples3,samples0,samples4,samples0,samples5))
samples *= 2**14

sdr_sensor = adi.Pluto("ip:192.168.2.1")
sdr_sensor.gain_control_mode_chan0 = 'manual'
sdr_sensor.sample_rate = int(sample_rate)
sdr_sensor.tx_buffer_size = num_samps_tx
sdr_sensor.tx_rf_bandwidth = int(sample_rate) 
sdr_sensor.tx_lo = int(center_freq)
sdr_sensor.tx_hardwaregain_chan0 = 0
sdr_sensor.rx_hardwaregain_chan0 = 70.0 
sdr_sensor.rx_lo = int(center_freq_rx)
sdr_sensor.rx_rf_bandwidth = int(sample_rate) 
sdr_sensor.rx_buffer_size = num_samps_rx

#####sensor pulse shaping#####
x1 = samples
num_taps = 1001
beta = 0.35
Ts = 300 #change this
t = np.arange(num_taps) - (num_taps-1)//2
h_sensor = 1/Ts*np.sinc(t/Ts) * np.cos(np.pi*beta*t/Ts) / (1 - (2*beta*t/Ts)**2)
x_shaped = np.convolve(x1,h_sensor)
#####raised-cosine filter#####

print("wait for the broadcast")
psd = 0
while(1):  ##wait for the signal
    raw_data = np.zeros((10,10000))
    for i in range (0, 10):
        raw_data[i] = sdr_sensor.rx()
    psd = np.abs(np.fft.fftshift(np.fft.fft(raw_data[1])))**2/(sample_rate* 10000)
    print(len(raw_data[1]))
    plt.figure(1)
    plt.plot(psd) 
    # plt.show()
    thres = 4880
    for i in range(100):
        if(psd[thres]>5):
            print("Got the signal 1")
            break
        else:
            thres += 1
    if(psd[thres]>5):
            break
    print("Wrong")
    print(len(raw_data))
    continue


rx_samples = np.zeros(100000)
for i in range(0,9):
    for j in range(10000):
        rx_samples[i*10000+j] = raw_data[i][j]
plt.figure(2)
plt.plot(rx_samples) 
plt.show()
print("done")