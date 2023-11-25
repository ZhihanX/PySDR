import numpy as np
import adi
import matplotlib.pyplot as plt
sample_rate = 2500e3 # Hz
center_freq = 2450e6 # Hz 

sdr = adi.Pluto("ip:192.168.2.1")
sdr.sample_rate = int(sample_rate)
sdr.tx_rf_bandwidth = int(sample_rate) # filter cutoff, just set it to the same as sample rate
sdr.tx_lo = int(center_freq)
sdr.tx_hardwaregain_chan0 = -4 # Increase to increase tx power, valid range is -90 to 0 dB

N = 10000 # number of samples to transmit at once
t = np.arange(N)/sample_rate
samples = 0.5*np.exp(2.0j*np.pi*100e3*t) # Simulate a sinusoid of 100 kHz, so it should show up at 915.1 MHz at the receiver
print(samples)
print(len(samples))
samples *= 2**14 # The PlutoSDR expects samples to be between -2^14 and +2^14, not -1 and +1 like some SDRs
# plt.plot(np.real(samples[0:500]))
# plt.show()

for i in range(10000):

    sdr.tx(samples) # transmit the batch of samples once

#plt.plot(np.real(samples[i:i+500]))
#plt.show()