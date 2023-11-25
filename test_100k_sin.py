import matplotlib.pyplot as plt
import numpy as np
import adi
import time

sample_rate = 2.084e6 # Hz
center_freq = 2450e6 # Hz
num_samps = 10000

sdr_server = adi.Pluto("ip:192.168.4.1")
sdr_server.sample_rate = int(sample_rate)
sdr_server.tx_buffer_size = num_samps
sdr_server.tx_rf_bandwidth = int(sample_rate) 
sdr_server.tx_lo = int(center_freq)
sdr_server.tx_hardwaregain_chan0 = 0

N = 10000 
t = np.arange(N)/sample_rate
samples = 0.5*np.exp(2.0j*np.pi*100e3*t) 
samples *= 2**14
sdr_server.tx_cyclic_buffer = True 
sdr_server.tx_destroy_buffer()
sdr_server.tx(samples)
time.sleep(1000)