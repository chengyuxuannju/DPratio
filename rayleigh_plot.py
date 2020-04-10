# coding=utf-8
"""
Plos
"""
import numpy as np
from matplotlib import pyplot as plt
import copy
import rayleigh_utils as util


def plot_coherence_mean(Co, freq):
    plt.subplot(211)
    plt.title("Mean")
    plt.scatter(1 / freq, Co, s=2)
    plt.xlim((20, 200))
    plt.ylim((0., 1.))
    plt.ylabel('Raw coherence')
    plt.xlabel('Seconds (s)')

    plt.subplot(212)
    plt.scatter(freq, Co, s=2)
    plt.xlim((0.1, 0.3))
    plt.ylim((0., 1.))
    plt.ylabel('Raw coherence')
    plt.xlabel('Frequency (Hz)')

    plt.show()


"""
use traces to compute and plot
"""


def plot_coherence(trZ, trP, julday):
    Ad, Co, Ph, eAd, eCo, ePh = util.calculate_trfs(trZ, trP)
    dn = 0.25
    ws = 8000
    freq = np.fft.fftfreq(ws, dn)

    fig = plt.figure()

    plt.subplot(211)
    plt.title(julday)
    plt.scatter(1 / freq, Co, s=2)
    plt.xlim((20, 200))
    plt.ylim((0., 1.))
    plt.ylabel('Raw coherence')
    plt.xlabel('Seconds (s)')

    plt.subplot(212)
    plt.scatter(freq, Co, s=2)
    plt.xlim((0.1, 0.3))
    plt.ylim((0., 1.))
    plt.ylabel('Raw coherence')
    plt.xlabel('Frequency (Hz)')

    plt.show()


"""
2000s noise segament length
4 Hz noise sample rate
0-0.05Hz 
"""


def plot_coherence_low_freq(trZ, trP, julday):
    Ad, Co, Ph, eAd, eCo, ePh = util.calculate_trfs(trZ, trP)
    dn = 0.25
    ws = 2000
    freq = np.fft.fftfreq(ws, dn)
    fig = plt.figure()
    plt.scatter(1 / freq, Co, s=2)

    plt.xlim((20, 200))
    plt.ylim((0., 1.))
    plt.ylabel('Raw coherence')
    plt.xlabel('Seconds (s)')
    plt.title(julday)


"""
2000s noise segament length
4 Hz noise sample rate
0.1-0.3Hz 
"""


def plot_coherence_high_freq(trZ, trP, julday):
    Ad, Co, Ph, eAd, eCo, ePh = util.calculate_trfs(trZ, trP)
    dn = 0.25
    ws = 2000
    freq = np.fft.fftfreq(ws, dn)
    fig = plt.figure()
    plt.scatter(freq, Co, s=2)
    plt.xlim((0.1, 0.3))
    plt.ylim((0., 1.))
    plt.ylabel('Raw coherence')
    plt.xlabel('Frequency (Hz)')
    plt.title(julday)
    plt.show()


# 标准误=标准差除以样本量的平方根
def plot_time_change(freq, ratios, days, title=None):

    f = [0.175, 0.2, 0.225]  # for AXCC1
    # f = [0.125, 0.135, 0.145]  # for AXBA1
    index = [[346, 347, 348, 349, 350, 351, 352, 353, 354]]  # 0.175 for AXCC1
    # index = [[246, 247, 248, 249, 250, 251, 252, 253, 254]]  # for AXBA1
    mul = 2
    # index = [[24, 25, 26]]

    fig = plt.figure(dpi=250)
    label = []
    colors = ['b', 'g', 'y', 'c', 'm', 'r', 'tan', 'k']

    for i in range(len(f) - 1):
        last = copy.deepcopy(index[-1])
        offset = f[i + 1] - f[i]
        for j in range(len(last)):
            last[j] += (int)(1000 * offset) * mul
        index.append(last)
    # 每个子列表存放某频率的所有值
    avg = [[], [], [], [], [], [], [], []]
    # print index

    for r in ratios:
        for i in range(len(f)):
            value = np.average(np.log10(r[index[i]]))
            avg[i].append(value)


    for i in range(len(f)):
        l = plt.scatter(days,avg[i],s=5,color=colors[i])
        label.append(l)
        # plt.plot(days,avg[i],color=colors[i])

    plt.axvline(x=113, ls='--',color='red')
    plt.grid()
    plt.legend(label, f, bbox_to_anchor=(1.05, 0), loc=3, title="freq(Hz)")

    # plt.xticks(ratios)
    plt.xlabel("julday")
    plt.ylabel("log D/P-ratio (m/Pa)")
    plt.tight_layout()
    plt.title(title)
    plt.show()
    # print avg


def get_month_first(list, month):
    day = 334  # December
    for i in range(len(list)):
        if day <= list[i]:
            return i

    return -1


# 把多天的计算结果放到一起，看计算的可靠性
def plot_dots(events, e_f, f1=0.02, f2=0.2, title=None):
    index = np.where((e_f >= f1) & (e_f <= f2))
    fig = plt.figure()
    e_f = e_f[index]

    for event in events:
        event = event[index]
        plt.scatter(e_f, np.log10(event), s=2)

    if title:
        plt.title(title)
    plt.xlim(f1, f2)
    plt.ylim(-4, 0)
    plt.ylabel('log D/P-ratio (m/Pa)')
    plt.xlabel('frequency (Hz)')
    return fig


def rayleigh_compare4(d_b, d_a, e_b, e_a, d_f, e_f, f1=0.0001, f2=0.2):
    fig = plt.figure()

    d_b = d_b[np.where((d_f >= f1) & (d_f <= f2))]
    d_a = d_a[np.where((d_f >= f1) & (d_f <= f2))]
    d_f = d_f[np.where((d_f >= f1) & (d_f <= f2))]
    e_b = e_b[np.where((e_f >= f1) & (e_f <= f2))]
    e_a = e_a[np.where((e_f >= f1) & (e_f <= f2))]
    e_f = e_f[np.where((e_f >= f1) & (e_f <= f2))]

    # fit1 = np.polyfit(e_f, np.log10(e_b), 2)
    # fit2 = np.polyfit(e_f, np.log10(e_a), 2)
    # fit3 = np.polyfit(d_f, np.log10(d_b), 2)
    # fit4 = np.polyfit(d_f, np.log10(d_a), 2)
    #
    # fity1 = np.polyval(fit1, e_f)
    # fity2 = np.polyval(fit2, e_f)
    # fity3 = np.polyval(fit3, d_f)
    # fity4 = np.polyval(fit4, d_f)

    # l1, = plt.plot(e_f, fity1, c='r')
    # l2, = plt.plot(e_f, fity2, c='g')
    # l3, = plt.plot(d_f, fity3, c='b')
    # l4, = plt.plot(d_f, fity4, c='k')

    l3 = plt.scatter(d_f, np.log10(d_b), s=2, c='b')
    l4 = plt.scatter(d_f, np.log10(d_a), s=2, c='k')
    l1 = plt.scatter(e_f, np.log10(e_b), s=2, c='r')
    l2 = plt.scatter(e_f, np.log10(e_a), s=2, c='g')
    plt.xlim(f1, f2)
    plt.ylim(-4, 0)

    plt.ylabel('log D/P-ratio (m/Pa)')
    plt.xlabel('frequency (Hz)')
    plt.legend([l1, l2, l3, l4], ['Event Before', 'Event After', 'Daily Before', 'Daily After'], loc='best')
    # plt.legend([l1,l3], ['Event Before', 'Daily Before'], loc='best')
    # plt.legend([l2,l4], ['Event After','Daily After'], loc='best')
    # plt.legend([l3,l4], ['Daily Before','Daily After'], loc='best')
    # plt.legend([l1, l2], ['Event Before', 'Event After'], loc='best')
    fig.show()

    return fig


def rayleigh_compare_ab(event, daily, efrq, dfrq, f1=0.1, f2=0.2, title=None, lab1="event", lab2="daily"):
    fig = plt.figure()

    l1 = plt.scatter(efrq, np.log10(event), s=2, c='b')
    l2 = plt.scatter(dfrq, np.log10(daily), s=2, c='r')
    plt.xlim(f1, f2)
    plt.ylim(-4, 0)  # TODO -4
    plt.ylabel('log D/P-ratio (m/Pa)')
    plt.xlabel('frequency (Hz)')
    plt.legend([l1, l2], [lab1, lab2], loc='best')

    if title:
        plt.title(title)

    plt.show()

    return fig


def rayleigh_compare2(r1, r2, freq, f1=0.1, f2=0.2, title=None):
    fig = plt.figure()

    l1 = plt.scatter(freq, np.log10(r1), s=2, c='b')
    l2 = plt.scatter(freq, np.log10(r2), s=2, c='r')
    plt.xlim(f1, f2)
    plt.ylim(-4, -1.5)
    plt.ylabel('log D/P-ratio (m/Pa)')
    plt.xlabel('frequency (Hz)')
    plt.legend([l1, l2], ['before', 'after'], loc='best')

    if title:
        plt.title(title)

    plt.show()

    return fig


def rayleigh_plot_DP_ratio(ratio, freq, f1=0.1, f2=0.2, title=None):
    fig = plt.figure()

    plt.scatter(freq, np.log10(ratio), s=2, c='g')
    plt.xlim(f1, f2)
    if f1 == 0.1:
        plt.ylim(-5, -2)
    plt.ylabel('log D/P-ratio (m/Pa)')
    plt.xlabel('frequency (Hz)')

    if title:
        plt.title(title)

    plt.show()

    return fig


def obs_plot_2traces(tr1, tr2, f1=0.01, f2=0.05, title=None):
    # Get parameters from traces
    nt = tr1.stats.npts
    dt = tr1.stats.delta

    # Time axis
    time = np.arange(nt) * dt

    fig = plt.figure()

    tt = tr1.copy()
    tt.filter('bandpass', freqmin=f1, freqmax=f2, zerophase=True)
    plt.subplot(211)
    plt.plot(time, tt.data, c='k')

    tt = tr2.copy()
    tt.filter('bandpass', freqmin=f1, freqmax=f2, zerophase=True)
    plt.subplot(212)
    plt.plot(time, tt.data, c='k')

    if title:
        plt.suptitle(title)

    # plt.tight_layout()
    ##plt.show()
    plt.close()

    return fig


def obs_plot_3traces(tr1, tr2, tr3, f1=0.01, f2=0.05, title=None):
    # Get parameters from traces
    nt = tr1.stats.npts
    dt = tr1.stats.delta

    # Time axis
    time = np.arange(nt) * dt

    fig = plt.figure()

    tt = tr1.copy()
    tt.filter('bandpass', freqmin=f1, freqmax=f2, zerophase=True)
    plt.subplot(311)
    plt.plot(time, tt.data, c='k')

    tt = tr2.copy()
    tt.filter('bandpass', freqmin=f1, freqmax=f2, zerophase=True)
    plt.subplot(312)
    plt.plot(time, tt.data, c='k')

    tt = tr3.copy()
    tt.filter('bandpass', freqmin=f1, freqmax=f2, zerophase=True)
    plt.subplot(313)
    plt.plot(time, tt.data, c='k')

    if title:
        plt.suptitle(title)

    # plt.tight_layout()
    # plt.show()
    plt.close()

    return fig


def obs_plot_trf_compliance(Ad, Co, Ph, eAd, eCo, ePh, freq):
    fig = plt.figure()

    freq = freq[1:len(freq) / 2]
    Co = Co[1:len(freq) + 1]
    Ad = Ad[1:len(freq) + 1]
    Ph = Ph[1:len(freq) + 1]
    eAd = eAd[1:len(freq) + 1]
    ePh = ePh[1:len(freq) + 1]

    plt.subplot(311)
    # plt.scatter(np.log10(freq), Co, s=2)
    plt.scatter(freq, Co, s=2)
    # plt.xscale('log')

    plt.xlim((0.005, 0.3))
    # plt.xlim(-8.,1.)
    plt.ylim(0., 1.)
    plt.ylabel('Raw coherence')
    plt.xlabel('log Frequency (Hz)')

    plt.subplot(312)
    plt.scatter(freq, np.log10(Ad), s=2)
    plt.errorbar(freq, Ad, yerr=eAd, fmt='.', c='k', ecolor='r')
    plt.yscale('log')
    # plt.xlim((0.005, 0.1))
    plt.xlim((0.005, 0.3))
    # plt.ylim((-9., -5.))
    plt.ylabel('log10(Admittance)')
    plt.xlabel('Frequency (Hz)')

    plt.subplot(313)
    # plt.scatter(freq,Ph,s=2)
    plt.errorbar(freq, Ph, yerr=ePh, fmt='.', c='k', ecolor='r')
    # plt.xlim((0.005, 0.1))
    plt.xlim((0.005, 0.3))
    plt.ylim((-np.pi, np.pi))
    plt.ylabel('Phase shift (radians)')
    plt.xlabel('Frequency (Hz)')

    plt.suptitle('Transfer functions for compliance')

    # plt.tight_layout()
    # #plt.show()
    plt.close()

    return fig


def obs_plot_trf_analytic(Ad, Ph, eAd, ePh, aAd, aPh, freq, ind):
    fig = plt.figure()

    plt.subplot(211)
    plt.errorbar(freq[ind], Ad[ind], yerr=eAd[ind], fmt='k.')
    plt.plot(freq[ind], aAd[ind], 'r')
    # plt.ylim((0.0044,0.0086))
    plt.ylabel('Admittance')
    plt.xlabel('Frequency (Hz)')

    plt.subplot(212)
    plt.errorbar(freq[ind], Ph[ind], yerr=ePh[ind], fmt='k.')
    plt.plot(freq[ind], aPh[ind], 'r')
    plt.ylim((-np.pi / 10., np.pi / 10.))
    plt.ylabel('Phase shift (radians)')
    plt.xlabel('Frequency (Hz)')

    plt.suptitle("Analytical transfer functions")  # added by Cheng Oct 30

    # plt.tight_layout()
    # plt.show()
    plt.close()

    return fig
