# coding=utf-8
import numpy as np
import rayleigh_plot as plt
import DP_daily as dp

dp.run()


file_days = open("AXCC1/days")
days = []
for i in file_days:
    year = int(i[0:4])
    day = int(i[5:-1])

    days.append(365*(year-2015) + day)

print days

ratios = np.loadtxt("AXCC1/ratio")

ws = len(ratios[0])
sample_rate = 4
freq = np.fft.fftfreq(ws, 1.0 / sample_rate)

plt.plot_time_change(freq, ratios, days, title="May")
