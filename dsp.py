""" Process waveforms """

import math

import numpy as np


def normalise(inp):
    """ Normalise a signal to the range +/- 1

        @param inp seq : A sequence of samples
    """

    inp /= max(abs(inp))
    
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
    
    return normalise(inp)
    

def tube(inp, amount, bias=0):
    """ Tube saturate a signal

        @param inp seq : A sequence of samples
        @param amount number : Amount of distortion
        @param bias number : Pre-distortion DC bias
    """
    
    gain = 1 + amount
    inp += bias
    inp *= gain
    for i, s in enumerate(inp):
        inp[i] = math.exp(-np.logaddexp(0, -s))
    
    inp *= 2
    inp -= 1
    
    return normalise(inp)


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
        for i, s in enumerate(inp):
            if s > 1:
                inp[i] = 2 - s
            if s < -1:
                inp[i] = -2 -s

    return normalise(inp)


def shape(inp, amount, bias=0, power=3):
    """ Perform polynomial waveshaping
    
        @param inp seq : A sequence of samples
        @param amount number : Amount of shaping
        @param bias number : Pre-distortion DC bias
        @param power : Polynomial power
    """
    
    shaped = np.power(inp, power) * amount
    inp *= (1 - amount)
    inp += shaped
    
    return normalise(inp)


def slew(inp, rate, inv=False):
    """ Apply slew or overhoot to a signal. Slew smooths steep transients in
        the signal while overshoot results in a sharper transient with
        ringing.
        
        @param rate float : Slew rate, between 0 and 1
        @param inp seq : A sequence of samples
        @param inv bool : If True, overshoot will be applied. if False,
                          slew will be applied. (default=False).
    """

    a = rate
    p = 0.
    # process twice in order to allow for settling
    for m in range(2):
        for i, s in enumerate(inp):
            if inv:
                c = p * (a - 1.) + (s * a)
            else:
                c = s * (1. - a) + (p * a)
            p = c
            if m > 0:
                inp[i] = c

    return normalise(inp)
    

def downsample(inp, factor):
    """ Reduce the effective sample rate of a signal, resulting in aliasing.

        @param inp seq : A sequence of samples
        @param factor int : Downsampling factor
    """

    if factor < 1:
        m = "Downsampling factor ({0}) cannot be < 1"
        raise ValueError(m.format(self.downsample_factor))

    if factor == 1:
        return inp
    else:
        # the aliasing is deliberate!
        ns = 0
        f = factor

        for i, s in enumerate(inp):
            if i % f == 0:
                last = s
            else:
                inp[i] = last
                
    return normalise(inp)


def quantise(inp, depth):
    """ Reduce the bit depth of a signal.

        @param inp seq : A sequence of samples
        @param depth number : New bit depth in bits
    """

    m = 2 ** depth - 1

    for i, s in enumerate(inp):
        if s > 0:
            inp[i] = np.ceil(s * m) / m
        elif s < 0:
            inp[i] = np.floor(s * m) / m
            
    return normalise(inp)
