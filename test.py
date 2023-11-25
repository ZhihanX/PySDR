import matplotlib.pyplot as plt
import numpy as np
import adi
import time
import argparse


sample_rate = 2.5e6 # Hz
center_freq = 2450e6 # Hz
num_samps = 10000

sdr = adi.Pluto("ip:192.168.4.1")
sdr.sample_rate = int(sample_rate)
sdr.tx_buffer_size = num_samps
sdr.tx_rf_bandwidth = int(sample_rate) # sample rate
sdr.tx_lo = int(center_freq)
sdr.tx_hardwaregain_chan0 = -10
sdr.tx_cyclic_buffer = True


def generate_pulse_sequence(num_pulses, pulse_interval, pulse_amplitudes):
    """
    生成固定间隔、不同幅度的复数脉冲序列。

    参数：
    num_pulses：int，脉冲的数量
    pulse_interval：float，脉冲之间的时间间隔
    pulse_amplitudes：list，包含每个脉冲的幅度的列表

    返回：
    complex_array：numpy.array，包含复数脉冲序列的NumPy数组
    """
    if len(pulse_amplitudes) != num_pulses:
        raise ValueError("脉冲数量与脉冲幅度列表长度不一致")

    # 生成脉冲序列    
    pulses = [amp * np.ones(int(pulse_interval)) for amp in pulse_amplitudes]
    pulse_sequence = np.concatenate(pulses)

    return pulse_sequence

# 示例
num_pulses = 5
pulse_interval = 10 # 假设脉冲之间间隔为10个单位

# Save the complex numbers to a file in binary format
complex_numbers = np.array([0.1+0j, 0.1+0j, 0.3+0j, 0.5-0j, 0.4+0j], dtype=np.complex64) #0.1+0j, 0.1+0j, 0.3+0j, 0.5-0j, 0.4+0j]

with open("pilot.txt", "wb") as file:
    complex_numbers.tofile(file)

Pilot = np.fromfile("pilot.txt",np.complex64)
# for i in range(len(Pilot)):
#     Pilot -= 11312

print(Pilot)

pulse = generate_pulse_sequence(num_pulses, pulse_interval, Pilot)


# pulse_duration = 1e-6  # 1微秒
# num_samples = int(pulse_duration * sdr.sample_rate)
# pulse = np.ones(num_samples)
print(pulse)
pulse *= 2**14
# pulse_duration = 1e-6  # 1微秒
# num_samples = int(pulse_duration * sdr.sample_rate)
# pulse = np.ones(num_samples)
# sdr.tx_cyclic_buffer = True
complex_numbers*=2**14
plt.figure(0)
plt.plot(np.real(complex_numbers[0:30]))
plt.xlabel("Time")
plt.show()
sdr.tx_destroy_buffer()
sdr.tx(complex_numbers)

time.sleep(10)       
sdr.tx_destroy_buffer()