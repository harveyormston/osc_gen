#!/usr/bin/env python
""" Process waveforms """

import math
from copy import deepcopy

import numpy as np


class NotEnoughSamplesError(Exception):
    """ Not Enough Samples """
    pass


def normalize(inp):
    """ Normalize a signal to the range +/- 1

        @param inp seq : A sequence of samples
    """

    inp -= (np.amax(inp) + np.amin(inp)) / 2
    amp = np.amax(np.absolute(inp))

    if amp > 0:
        inp /= np.amax(abs(inp))

    return inp


def clip(inp, amount, bias=0):
    """ Hard-clip a signal

        @param inp seq : A sequence of samples
        @param amount number : Amount of clipping
        @param bias number : Pre-distortion DC bias
    """

    gain = 1 + amount

    inp += bias
    inp *= gain
    np.clip(inp, -1., 1., out=inp)

    return normalize(inp)


def tube(inp, amount, bias=0):
    """ Tube saturate a signal

        @param inp seq : A sequence of samples
        @param amount number : Amount of distortion
        @param bias number : Pre-distortion DC bias
    """

    gain = 1 + amount
    inp += bias
    inp *= gain
    for i, val in enumerate(inp):
        inp[i] = math.exp(-np.logaddexp(0, -val))

    inp *= 2
    inp -= 1

    return normalize(inp)


def fold(inp, amount, bias=0):
    """ Perform wave folding

        @param inp seq : A sequence of samples
        @param amount number : Amount of distortion
        @param bias number : Pre-distortion DC bias
    """

    gain = 1 + amount
    inp += bias
    inp *= gain
    while (max(abs(inp))) > 1:
        for i, val in enumerate(inp):
            if val > 1:
                inp[i] = 2 - val
            if val < -1:
                inp[i] = -2 - val

    return normalize(inp)


def shape(inp, amount=1, bias=0, power=3):
    """ Perform polynomial waveshaping

        @param inp seq : A sequence of samples
        @param amount number : Amount of shaping
            (1: maximum shaping, 0: no shaping)
        @param bias number : Pre-distortion DC bias
        @param power number : Polynomial power
    """

    biased = inp + bias

    # make another copy to apply polynomial shaping to the biased input
    shaped = np.empty_like(biased)
    # shape positive and negative halves of the signal symmetrically
    shaped[biased >= 0] = np.power(biased[biased >= 0], power) * amount
    shaped[biased < 0] = -np.power(-biased[biased < 0], power) * amount
    # de-bais
    shaped -= bias
    normalize(shaped)

    inp *= (1 - amount)
    inp += shaped * amount

    return normalize(inp)


def slew(inp, rate, inv=False):
    """ Apply slew or overhoot to a signal. Slew smooths steep transients in
        the signal while overshoot results in a sharper transient with
        ringing.

        @param rate float : Slew rate, between 0 and 1
        @param inp seq : A sequence of samples
        @param inv bool : If True, overshoot will be applied. if False,
                          slew will be applied. (default=False).
    """

    prev = 0.
    # process twice in order to allow for settling
    for num in range(2):
        for i, val in enumerate(inp):
            if inv:
                curr = prev * (rate - 1.) + (val * rate)
            else:
                curr = val * (1. - rate) + (prev * rate)
            prev = curr
            if num > 0:
                inp[i] = curr

    return normalize(inp)


def downsample(inp, factor):
    """ Reduce the effective sample rate of a signal, resulting in aliasing.

        @param inp seq : A sequence of samples
        @param factor int : Downsampling factor
    """

    if factor < 1:
        raise ValueError(
            "Downsampling factor ({0}) cannot be < 1".format(factor))

    if factor == 1:
        return inp
    else:
        # the aliasing is deliberate!
        for i, val in enumerate(inp):
            if i % factor == 0:
                last = val
            else:
                inp[i] = last

    return normalize(inp)


def quantize(inp, depth):
    """ Reduce the bit depth of a signal.

        @param inp seq : A sequence of samples
        @param depth number : New bit depth in bits
    """

    scale = 2 ** depth - 1

    for i, val in enumerate(inp):
        if val > 0:
            inp[i] = np.ceil(val * scale) / scale
        elif val < 0:
            inp[i] = np.floor(val * scale) / scale

    return normalize(inp)


def fundamental(inp, fs):
    """ Find the fundamental frequency in Hz of a given input """

    h = np.hamming(len(inp))
    w = np.fft.fft(inp * h)
    f = np.fft.fftfreq(len(w))
    i = np.argmax(np.abs(w))

    return abs(f[i] * fs)


def harmonic_series(inp):
    """ Find the harmonic series of a periodic input """

    L = min(64, len(inp) // 501)
    M = 501 * L
    if len(inp) < M:
        raise NotEnoughSamplesError("Got {0} samples, need at least {1}.".format(len(inp), M))

    # produce symmetrical, windowed fft
    hM1 = int(np.floor((M + 1) / 2))
    hM2 = int(np.floor(M / 2))
    x1 = inp[:M] * np.hamming(M)
    N = 1024 * L
    buf = np.zeros(N)
    buf[:hM1] = x1[hM2:]
    buf[N - hM2:] = x1[:hM2]
    fft = np.fft.fft(buf)[:N // 2]

    # peak amplitude assumed to be fundamental frequency
    i_fund = np.argmax(np.abs(fft))

    # get fft components from only the harmonics, harmonics are picked by
    # taking the value with the highest amplitude around each harmonic
    # frequency
    ws = i_fund // 4
    hs = np.array(
        [fft[i - ws:i + ws][np.abs(fft[i - ws:i + ws]).argmax()]
         for i in range(i_fund, N // 2, i_fund)])

    # normalize magnitude and phase
    hs_amp = np.abs(hs)
    hs_ang = np.angle(hs)
    hs = hs_amp * np.exp(1j * (hs_ang - hs_ang[0])) / hs_amp[0]

    return hs


def slice_cycles(inp, n, fs):
    """ Extact n single-cycle slices from a signal """

    def nearest(arr, val):
        """ find the nearest value in an array to a given value """
        return arr[np.argmin(np.abs(arr - val))]

    zero_crossings = np.where(np.diff(np.sign(inp)) > 0)[0] + 1

    if len(zero_crossings) < 1:
        raise ValueError("No zero crossings found.")

    freq = fundamental(inp, fs)
    samples_per_cycle = fs / freq
    end = len(inp) - samples_per_cycle

    slots = np.linspace(0, end, n)
    slots = np.around(slots).astype(int)
    slots = np.unique([nearest(zero_crossings, slot) for slot in slots])

    return [inp[x:x + int(samples_per_cycle)] for x in slots]


def resynthesize(inp, sig_gen):
    """
    Resynthesize a signal from its harmonic series

    @param sig_gen SigGen : SigGen to use for regenerating the signal.
    """

    sg = deepcopy(sig_gen)
    max_harmonic = sig_gen.num_points // 2
    hs = harmonic_series(inp)
    s = np.zeros(sg.num_points)

    for i, h in enumerate(hs):

        sg.harmonic = i
        sg.amp = np.abs(h)
        sg.phase = np.angle(h)

        s += sg.sin()

        if i >= max_harmonic:
            break

    normalize(s)

    return s
