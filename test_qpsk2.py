import numpy as np
import matplotlib.pyplot as plt
import adi
import time
import signal

sample_rate = 2.5e6 # Hz
center_freq = 2450e6 # Hz
num_symbols = 10000

x_int = np.random.randint(0, 4, num_symbols) # 0 to 3
x_degrees = x_int*360/4.0 + 45 # 45, 135, 225, 315 degrees
x_radians = x_degrees*np.pi/180.0 # sin() and cos() takes in radians
x_symbols = np.cos(x_radians) + 1j*np.sin(x_radians) # this produces our QPSK complex symbols
plt.figure(0)
plt.plot(np.real(x_symbols), np.imag(x_symbols), '.')
plt.grid(True)
plt.show()

n = (np.random.randn(num_symbols) + 1j*np.random.randn(num_symbols))/np.sqrt(2) # AWGN with unity power
noise_power = 0.01
r = x_symbols + n * np.sqrt(noise_power)
plt.figure(1)
plt.plot(np.real(r), np.imag(r), '.')
plt.grid(True)
plt.show()