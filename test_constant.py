import numpy as np
import adi
import time
import matplotlib.pyplot as plt
sample_rate = 2.5e6 # Hz
center_freq = 2450e6 # Hz


sdr = adi.Pluto("ip:192.168.3.1")
sdr.sample_rate = int(sample_rate)
sdr.tx_rf_bandwidth = int(sample_rate) # filter cutoff, just set it to the same as sample rate
sdr.tx_lo = int(center_freq)
sdr.tx_hardwaregain_chan0 = 0 # Increase to increase tx power, valid range is -90 to 0 dB
sdr.tx_cyclic_buffer = True

N = 10000 # number of samples to transmit at once
t = constant_array = np.full((N, ), 1)
samples = (0.5 + 0j)*t # Simulate a sinusoid of 100 kHz, so it should show up at 915.1 MHz at the receiver
print(samples)
samples *= 2**14 # The PlutoSDR expects samples to be between -2^14 and +2^14, not -1 and +1 like some SDRs
# plt.figure(0)
# plt.plot(np.real(samples[0:1000]))
# plt.xlabel("Time")
# plt.figure(3)
# plt.plot((np.real(samples[9000:9500])**2+(np.imag(samples[9000:9500]))**2))
# plt.xlabel("Mag")
# plt.show()
# Transmit our batch of samples 100 times, so it should be 1 second worth of samples total, if USB can keep up
sdr.tx_destroy_buffer()
sdr.tx(samples)

time.sleep(100)  