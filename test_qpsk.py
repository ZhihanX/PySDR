import numpy as np
import adi
import matplotlib.pyplot as plt
from scipy import signal
import time

num_taps = 10001
beta = 0.35
for i in range (2000,2100):
    Ts = i #change this
    t = np.arange(num_taps) - (num_taps-1)//2
    h = 1/Ts*np.sinc(t/Ts) * np.cos(np.pi*beta*t/Ts) / (1 - (2*beta*t/Ts)**2)
   
    plt.plot(h)
    plt.xlabel("time")
    plt.ylabel("Shaped Signal")
    
plt.show()