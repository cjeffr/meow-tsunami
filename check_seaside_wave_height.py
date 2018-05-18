import numpy as np
import os
import h5py
import matplotlib.pyplot as plt


path = '/Users/jeffriesc/Desktop/GF'
subfault_number = [7, 18, #10, 11, 12,
                   31, 45]#,# 30, 31, 32,
                   #48, 49] #50, 51, 52,
                   #68, 69, 70, 71, 72]

data= np.loadtxt(os.path.join(path, '007_00035.txt'))
time_array = data[:,0]
seaside_greens_functions = np.zeros(shape=(len(time_array), len(subfault_number)))
slip = 4


for index, subfault in enumerate(subfault_number):
    gf = np.loadtxt(os.path.join(path, '{:03}_00035.txt').format(subfault))
    seaside_greens_functions[:,index] = gf[:,1]


print(seaside_greens_functions[-1])
waves_scaled_for_slip = slip * seaside_greens_functions
print(np.array_equal(seaside_greens_functions, waves_scaled_for_slip))

new_gf = np.sum(waves_scaled_for_slip, axis=1)
plt.figure(1, figsize=(8,8))
additional_increments = 1
units_per_tick = 30
seconds_per_increment = 30. * 60
num_ticks = int(np.floor(max(time_array) / seconds_per_increment) + additional_increments)

plt.plot(0, 0, 'k')
plt.xlabel("Time (minutes)", fontsize=16)
plt.ylabel("Wave Height (m)", fontsize=16)
plt.xticks([seconds_per_increment * i for i in range(num_ticks)],
           ['%d' % (i * units_per_tick) for i in range(num_ticks)])
plt.tick_params(labelsize=16)

plt.plot(time_array, new_gf,'b', label='Convolve Subfaults 7, 18, 31, 45')
plt.ylim(-.4, .5)
plt.axhline(y=0.00, xmin=0, xmax=14400, c='black', linewidth=.5, zorder=0)
plt.interactive(False)
plt.legend(loc='upper right')
plt.title("Convolution of Green's Functions for subfaults", fontsize=16)
plt.show()
plt.savefig('/Users/jeffriesc/Desktop/convolve.png')
print(np.max(new_gf, axis=0))

