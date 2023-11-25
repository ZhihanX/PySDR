import numpy as np
import adi
import matplotlib.pyplot as plt
from scipy import signal
import time
#this file for Sensor (transmitter power is 5977)
def process_rx(rx_samples,h):
    rx_samples.real = rx_samples.real*rx_samples.real
    rx_samples.imag = rx_samples.imag*(-rx_samples.imag)
    
    match_filter = np.flip(h)
    rx_samples = np.convolve(rx_samples,match_filter)
    max_index = np.argmax(rx_samples)

    ######windows for peak values###########
    rx_samples_mid = []
    # print("max axis:", max_index)
    if(max_index<10000):
   
        rx_samples_mid = rx_samples[max_index+4500:max_index+15500]

    elif(max_index>10000):
        
        rx_samples_mid = rx_samples[max_index-16500:max_index-5500]
    
    else:
        
        rx_samples_mid = rx_samples[max_index-5500:max_index+5500]
   
    peaks, _ = signal.find_peaks(rx_samples_mid,distance=1700)
    widths = signal.peak_widths(rx_samples_mid,peaks,rel_height = 0.15)
    
    
    avg_p = 0
    width = 5 # loop times
    print(widths[2])
    print(widths[3])
    print(len(widths[2]))
    if(len(widths[2])!=5 or np.max(rx_samples)>50000):
        count = 1
        return avg_p,count
    
    for i in range(width):
        avg_p += np.average(rx_samples_mid[int(widths[2][i]):int(widths[3][i])])
    avg_p = np.sqrt(avg_p/width)
    count = 0
    plt.figure(13)
    plt.plot(rx_samples_mid)
    plt.hlines(*widths[1:],color="C3")
    # plt.show()
    return avg_p,count

sample_rate = 1e6 
center_freq = 2450e6 
center_freq_rx = center_freq 
num_samps_tx = 10000 
num_samps_rx = 10000  

######server parameter#########
# sdr_server = adi.Pluto("ip:192.168.4.1")
# sdr_server.sample_rate = int(sample_rate)
# sdr_server.tx_buffer_size = num_samps
# sdr_server.tx_rf_bandwidth = int(sample_rate) 
# sdr_server.tx_lo = int(center_freq)
# sdr_server.tx_hardwaregain_chan0 = 0
# sdr_server.rx_hardwaregain_chan0 = 70.0 
# sdr_server.rx_lo = int(center_freq)
# sdr_server.rx_rf_bandwidth = int(sample_rate) 
# sdr_server.rx_buffer_size = num_samps
#############################################
N = 10000 
t = np.arange(N/10)/sample_rate
T = np.arange(N)/sample_rate

samples0 = 0.05*np.exp(0*t) 
samples1 = 0.2*np.exp(0*t) 
samples2 = 0.4*np.exp(0*t)
samples3 = 0.6*np.exp(0*t)
samples4 = 0.4*np.exp(0*t)
samples5 = 0.2*np.exp(0*t)

samples = np.concatenate((samples0,samples1,samples0, samples2,samples0,samples3,samples0,samples4,samples0,samples5))

samples *= 2**14
# sdr_server.tx_cyclic_buffer = True 
#filter
#lo,hi = 80e3,120e3 
#b,a = signal.butter(6, [2*lo/sample_rate], btype='high')
#sensor setting
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
# sdr_sensor.tx_cyclic_buffer = True 

#####sensor pulse shaping#####
x1 = samples
num_taps = 1001
beta = 0.35
Ts = 300 #change this
t = np.arange(num_taps) - (num_taps-1)//2
h_sensor = 1/Ts*np.sinc(t/Ts) * np.cos(np.pi*beta*t/Ts) / (1 - (2*beta*t/Ts)**2)
x_shaped = np.convolve(x1,h_sensor)
#####raised-cosine filter#####


ratio = np.zeros(5)
#  

# sdr_server.tx_destroy_buffer()
# sdr_server.tx(samples)
# time.sleep(0.1)



gk = np.zeros(10)
for i in range (0, 10):
    raw_data = sdr_sensor.rx()

#first round: server broadcast
print("wait for the broadcast")
count = 0

######## wait for the signal #######
while(1):  ##wait for the signal
    for i in range (0, 10):
        raw_data = sdr_sensor.rx()
    raw_data = sdr_sensor.rx() 
    
    psd = np.abs(np.fft.fftshift(np.fft.fft(raw_data)))**2/(sample_rate* 30000)
    # plt.figure(55)
    # plt.plot(psd)
   
    # plt.show()
    # raw_data = np.abs(raw_data)
    thres = 14700
    count = 0
    
    power = np.mean(raw_data.real)
    for i in range(100):
        if(psd[thres]>10):
            count += 1
            print("Got the signal 1")
            break
        else:
            thres += 1
    if(count == 0):
            print("Wrong")
            continue
    else: 
        break
    # plt.figure(7)
    # plt.plot(raw_data)

##################################

rx_samples = np.zeros(100000)   
for i in range(10): #clear the buffer
    raw_data = sdr_sensor.rx()
time.sleep(2)
count_array = np.zeros(20)

for k in range(10):
    count = 0
    outlier = 0
    for i in range (10):
        rx_samples[i] = sdr_sensor.rx() 
        # plt.figure(5)
        # plt.plot(rx_samples)
        # avg_p,flag = process_rx(rx_samples,h_sensor)
        # if(flag == 1):
        #     outlier += 1
        # print("avg_p:",avg_p)
    rx_samples.real = rx_samples.real*rx_samples.real
    rx_samples.imag = rx_samples.imag*(-rx_samples.imag)
    count_array[i] = rx_samples
    count += avg_p

    max = np.max(count_array)
    min = np.min(count_array)
    # print(int((count-max-min)/8))
    gk[k] = (count-max-min)/(18-outlier)/6000 #device get gk from server
plt.figure(0)
x_target = np.linspace(0, 10, len(gk))
# plt.plot(x_target,gk,label= j)
plt.plot(x_target,gk)
plt.legend()
plt.ylabel("gk head")
plt.xlabel("time/s")
gk = np.average(gk)
print("gk:",gk)
plt.show()
sdr_sensor.tx_destroy_buffer()
print("send pilot to server")
sdr_sensor.tx(samples)
time.sleep(20)
# sdr_sensor.tx_destroy_buffer()
# sdr_sensor.tx(samples_finish)

# try:
#     while True:
#         z=1
# except KeyboardInterrupt:
#     print("done")
sdr_sensor.tx_destroy_buffer()

#Second round: sensor send pilot, server get hk
print("wait for the server")
######## wait for the signal #######
while(1):  ##wait for the signal
    for i in range (0, 10):
        raw_data = sdr_sensor.rx()
    raw_data = sdr_sensor.rx() 
    psd = np.abs(np.fft.fftshift(np.fft.fft(raw_data)))**2/(sample_rate* 30000)
    psd_dB = psd
    
    plt.figure(55)
    plt.plot(psd)
    # f = np.linspace(sample_rate/-2, sample_rate/2, len(psd))
    # plt.figure(1)
    # plt.plot(f/1e6, psd_dB)
    # plt.xlabel("Frequency [MHz]")
    # plt.ylabel("PSD")
    # plt.figure(7)
    # plt.plot(raw_data)
    # plt.figure(55)
    # plt.plot(psd)   
    # plt.show()
    plt.show()
    # raw_data = np.abs(raw_data)
    thres = 14700
    count = 0
    
    power = np.mean(raw_data.real)
    for i in range(100):
        if(psd[thres]>10):
            count += 1
            print("Got the signal hk*pilot")
            break
        else:
            thres += 1
    if(count == 0):
            print("Wrong")
            continue
    else: 
        break
    # plt.figure(7)
    # plt.plot(raw_data)

##################################
time.sleep(2)
count_array = np.zeros(20)
gkhk = np.zeros(10)
for k in range(10):
    count = 0
    outlier = 0
    for i in range (20):
        rx_samples = sdr_sensor.rx() 
        # plt.figure(5)
        # plt.plot(rx_samples)
        avg_p,flag = process_rx(rx_samples,h_sensor )
        if(flag == 1):
            outlier += 1
        # print("avg_p:",avg_p)
        count_array[i] =avg_p
        count += avg_p

    max = np.max(count_array)
    min = np.min(count_array)
    # print(int((count-max-min)/8))
    gkhk[k] = (count-max-min)/(18-outlier)/6000/gk/100 #device get gk from server
plt.figure(0)
x_target = np.linspace(0, 10, len(gkhk))
# plt.plot(x_target,gk,label= j)
plt.plot(x_target,gkhk)
plt.legend()
plt.ylabel("gkhk head")
plt.xlabel("time/s")
hk = np.average(gkhk)
print("hk:",hk)
# plt.show()


#     #third round: server send hk*pilot
#     print("step3 begin")
#     count = 0
#     sdr_server.tx_destroy_buffer()
#     sdr_server.tx(samples*hk*eta)

#     for i in range (0, 20):
#         raw_data = sdr_sensor.rx()
#     hk_sensor = np.zeros(100)
#     for k in range(100):
#         count = 0
#         for i in range (10):
#             rx_samples = sdr_sensor.rx() 
#             rx_samples = signal.lfilter(b,a,rx_samples)  
#             # rx_samples = (rx_samples/gk/8192)
#             print(np.average(np.sqrt(np.real(rx_samples)**2+(np.imag(rx_samples))**2)))
#             count_array[i] = np.average(np.sqrt(np.real(rx_samples)**2+(np.imag(rx_samples))**2))
#             count += count_array[i]
#         max = np.max(count_array)
#         min = np.min(count_array)
#         print((count-max-min)/8)
#         hk_sensor[k] = (count-max-min)/8/gk/eta/16384 #sensor get hk from server
#     print(hk_sensor)
#     plt.figure(2)
#     x_target = np.linspace(0, 4, len(hk_sensor))
#     plt.plot(x_target,hk_sensor,label= j)
#     plt.legend()
#     plt.ylabel("hk_sensor")
#     plt.xlabel("time/s")

#     #reset buffer
#     sdr_server.tx_destroy_buffer()
#     for i in range (0, 10):
#         raw_data = sdr_sensor.rx()
#     hk_sensor = np.average(hk_sensor)
#     #fourth round: test round
#     # print("test:divice to server with 1/hk")
#     # count = 0hk_sensor
#     # sdr_sensor.tx_destroy_buffer()
#     # sdr_sensor.tx(samples/hk_sensor)
#     # # print(np.average(np.sqrt(np.real(samples/hk_sensor)**2+(np.imag(samples/hk_sensor))**2)))

#     # for i in range (0, 20):
#     #     raw_data = sdr_server.rx()
#     # for i in range (10):
#     #     rx_samples = sdr_server.rx() 
#     #     rx_samples = signal.lfilter(b,a,rx_samples)  
#     #     rx_samples = rx_samples
#     #     print(np.average(np.sqrt(np.real(rx_samples)**2+(np.imag(rx_samples))**2)))
#     #     count_array[i] = np.average(np.sqrt(np.real(rx_samples)**2+(np.imag(rx_samples))**2))
#     #     count += count_array[i]
#     # max = np.max(count_array)
#     # min = np.min(count_array)   
#     # print((count-max-min)/8)
#     # ratio[j]= gk/hk_sensor
# print(ratio)
# plt.figure(3)
# plt.plot(ratio)
# plt.ylabel("ratio")
# plt.show()
        # raw_data = np.abs(raw_data)
