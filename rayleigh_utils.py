# coding=utf-8
'''

Set of utility functions to calculate the transfer functions and perform
related operations

---
Pascal Audet
pascal.audet@uottawa.ca

Last updated: 17 November 2015

'''

import numpy as np
import rayleigh_plot as plt




def rayleigh_DP_ratio(trZ, trP, ws):
    # ws, ss is only needed by Noise Trace, so set it here
    # ws = int(trZ.stats.sac.user8)
    # ss = int(trZ.stats.sac.user9)
    ss = ws

    tx, nd = sliding_window(trZ.data, ws, ss)
    ty, nd = sliding_window(trP.data, ws, ss)

    uz = np.fft.fft(tx)
    p = np.fft.fft(ty)

    numerator = uz * np.conj(p)
    denominator = p * np.conj(p)

    ratio = np.abs(np.mean(numerator, axis=0) / np.mean(denominator, axis=0))

    return ratio



def get_trZ_p(tr, pAd, pPh, f1, f2):
    """
    Calculates predicted trace from transfer
    functions

    """
    # Copy trace to predicted vertical (for consistency)
    tr_p = tr.copy()

    # Fourier transform trace
    ftr = np.fft.fft(tr.data)

    nt = tr.stats.npts
    dt = tr.stats.delta
    ff = np.fft.fftfreq(nt, dt)

    Ad = np.zeros((nt,))
    Ph = np.zeros((nt,))
    ind1 = np.where((ff > f1) & (ff < f2))
    ind2 = np.where((ff < -f1) & (ff > -f2))

    # Define analytical transfer functions
    # Careful: phase of negative frequencies is negative
    Ad[ind1] = pAd[0] * ff[ind1] ** 2 + pAd[1] * ff[ind1] + pAd[2]
    Ad[ind2] = pAd[0] * ff[ind2] ** 2 + pAd[1] * ff[ind2] + pAd[2]
    Ph[ind1] = pPh[0] * ff[ind1] ** 2 + pPh[1] * ff[ind1] + pPh[2]
    Ph[ind2] = -(pPh[0] * ff[ind2] ** 2 + pPh[1] * ff[ind2] + pPh[2])

    # Define complex transfer function in frequency
    trf = Ad * np.exp(1j * Ph)

    # Convolve in Fourier domain
    ftr_p = trf * ftr

    # Inverse Fourier transform
    tr_p.data = np.real(np.fft.ifft(ftr_p))

    return tr_p


def calculate_trfs(trX, trY):
    """
    Calculates transfer functions from
    cross-spectral quantities

    """
    # Get spectral quantities
    Gxy, Gxx, Gyy, Cxy, Qxy, nd = calculate_specs(trX, trY)

    # Get transfer functions
    Ad = admittance(Gxy, Gxx)
    Co = coherence(Gxy, Gxx, Gyy)
    Ph = phase(Gxy)

    eAd, eCo, ePh = trfs_error(Ad, Co, Ph, nd)

    return Ad, Co, Ph, eAd, eCo, ePh


def calculate_specs(trX, trY):
    """
    Calculates cross-spectral quantities

    ws: window size
    ss: step size (number of samples until next window)

    """
    ws = int(trX.stats.sac.user8)
    ss = int(trX.stats.sac.user9)

    tx, nd = sliding_window(trX.data, ws, ss)
    ty, nd = sliding_window(trY.data, ws, ss)

    ftx = np.fft.fft(tx)  # fft returns a complex ndarray Oct 29
    fty = np.fft.fft(ty)
    # ndarray * means each element multiplies its counterpart Nov 6
    # 19 windows average Nov 20
    Gxx = np.abs(np.mean(np.conj(ftx) * ftx, axis=0))
    Gyy = np.abs(np.mean(np.conj(fty) * fty, axis=0))
    Gxy = np.mean(np.conj(ftx) * fty, axis=0)

    Cxy = np.mean(np.real(ftx) * np.real(fty) +
                  np.imag(ftx) * np.imag(fty), axis=0)
    Qxy = np.mean(np.real(ftx) * np.imag(fty) -
                  np.imag(ftx) * np.real(fty), axis=0)

    return Gxy, Gxx, Gyy, Cxy, Qxy, nd


def get_trfs_lsqfit(Ad, Co, Ph, eAd, eCo, ePh, freq, f1, f2):
    """
    Get best-fit analytical admittance and phase from observed
    admittance and phase data within a given frequency range

    """

    ind = np.where((freq > f1) & (freq < f2))
    cond = np.where((Co > 0.5) & (freq > f1) & (freq < f2))
    if not cond:
        print 'no coherence above 0.5 within ', f1, f2, 'Hz'
        return [0., 0., 0.], [0., 0., 0.], None
    mcoh = np.mean(Co[ind])
    if mcoh < 0.5:
        print 'mean coherence too low', mcoh
        return [0., 0., 0.], [0., 0., 0.], None

    pAd = np.polyfit(freq[cond], Ad[cond], 2, w=1. / eAd[cond])
    pPh = np.polyfit(freq[cond], Ph[cond], 2, w=1. / ePh[cond])

    aAd = pAd[0] * freq ** 2 + pAd[1] * freq + pAd[2]
    aPh = pPh[0] * freq ** 2 + pPh[1] * freq + pPh[2]

    figure = plt.obs_plot_trf_analytic(Ad, Ph, eAd, ePh, aAd, aPh, freq, ind)

    return pAd, pPh, figure


def admittance(Gxy, Gxx):
    return np.abs(Gxy) / Gxx


def coherence(Gxy, Gxx, Gyy):
    return np.abs(Gxy) ** 2 / (Gxx * Gyy)


def phase(Gxy):
    return np.angle(Gxy)


def trfs_error(Ad, Co, Ph, nd):
    """
    Errors on transfer functions

    """

    eps = np.sqrt((1. - Co) / (2. * Co * nd))

    eAd = Ad * eps
    eCo = Co * eps
    ePh = eps

    return eAd, eCo, ePh


def sliding_window(a, ws, ss=None):
    '''
    Parameters
        a  - a 1D array
        ws - the window size, in samples
        ss - the step size, in samples. If not provided, window and step size
             are equal.

    """ PA: This is not my function """

    '''

    if None is ss:
        # no step size was provided. Return non-overlapping windows
        ss = ws

    # Calculate the number of windows to return, ignoring leftover samples, and
    # allocate memory to contain the samples
    valid = len(a) - ws  # how long the window can move Oct 29
    nd = (valid) // ss + 1 # step size means how long one step can move Oct 29
    # Origin nd = (valid) // ss, add one Dec 21
    out = np.ndarray((nd, ws), dtype=a.dtype)

    for i in xrange(nd):  # 20 samples
        # an object slightly faster than range() which returns a list Oct 29
        # "slide" the window along the samples
        start = i * ss
        stop = start + ws
        out[i] = a[start: stop] * np.hanning(ws)
        # TODO change to Gaussian?
        # Return the Hanning window with the maximum value normalized to one Oct 29

    return out[2:], nd # 开始的时候会有一个taper，舍弃第一个窗户
