""" Tools for generating and interpolating between waeform cycles. """

import dsp

import numpy as np


class SigGen():
    """ Signal Generator """

    def __init__(self, harmonic=0):
        """ Init """

        self.num_points = 128
        self.amp = 1.0
        self.offset = 0.0
        self.harmonic = harmonic

    def __base(self):
        """ Generate the base waveform cycle, a sawtooth or ramp from -1 to 1
        """

        d = 2 ** self.harmonic
        n = self.num_points / d
        cycle = np.linspace(-1., 1., num=n)
        return np.tile(cycle, d)


    def saw(self):
        """ Generate a sawtooth wave cycle """

        return self.__base()

    def tri(self):
        """ Generate a triangle wave cycle """

        return abs(self.__base()) * -2 + 1

    def pls(self, pw):
        """ Generate a pulse wave cycle

            @param pw float : Pulse width or duty cycle, between -1 and 1
        """

        def threshold(x, t):
            if x < t:
                return -1.
            else:
                return 1.

        return np.array([threshold(x, pw) for x in self.__base()])

    def sqr(self):
        """ Generate a square wave cycle """

        return self.pls(0)

    def sin(self):
        """ Generate a sine wave cycle """

        return np.sin(np.pi * (self.__base() + 0.5))

    def custom(self, data):
        """ Generate a custom wave cycle. The provided data will be
            interpolated, if possible, to occupy the correct number of samples
            for a single cycle at our reference frequency and then normalised
            and scaled as appropriate.

            @param data seq : A sequence of samples representing a single cycle
                              of a wave
        """

        y = data
        n = len(y)
        x = np.linspace(0, n, num=n)
        xx = np.linspace(0, n, num=self.num_points)
        yy = np.interp(xx, x, y)
        dsp.normalise(yy)
        return yy


def morph(s, n):
    """ Take a number of wave cycles and generate a higher number of wave cycles
        where the original waves are linearly interpolated from one to the next
        to fill in the gaps.

        @param s sequence : A sequence of wave cycles
        @param n int : The reuqired number of wave cycles in the new seuqence
    """

    inp = list(s)
    on = len(inp)

    if on >= n:
        m = "Can't morph a group into a smaller or equal group ({0} to {1})"
        raise ValueError(m.format(on, n))

    if on < 2:
        m = "Can't morph between less than 2 signals ({0})"
        raise ValueError(m.format(on))

    if on is 2:
        return __morph_two(inp[0], inp[1], n)

    ranges = __detrmine_morph_ranges(on, n)

    return __morph_many(inp, ranges)


def __detrmine_morph_ranges(n, nn):
    """ Find a set of integer gaps sizes between two set sizes

        @param n int : The original set size
        @param nn int : The new set size
    """

    bn = n - 1
    gs = int(round(float(nn) / bn, 0))
    ranges = [gs if j is 0 else gs + 1 for j in range(bn)]
    k = -1
    while sum(ranges) < nn + bn - 1:
        ranges[k] += 1
        k -= 1
    while sum(ranges) > nn + bn - 1:
        ranges[k] -= 1
        k -= 1

    return ranges


def __morph_many(s, r):
    """ Morph between more then two sequences

        @param s sequence : A sequence of wave cycles
        @param r sequence : The size of the gap between each pair of cycles
    """

    morphed = []
    a = None
    i = 0
    for b in s:
        if a is not None:
            if i is 0:
                o = 0
            else:
                o = 1

            n = [x for x in __morph_two(a, b, r[i])][o:]
            morphed.extend(n)
            i += 1

        a = b

    return morphed


def __morph_two(a, b, n):
    """ Morph between two wave cycles.

        @param a sequence : The first wave cycle
        @param b sequence : The second wave cycle
        @param n int : The reuqired number of wave cycles in the new seuqence
    """

    alphas = (s / (n - 1.0) for s in range(n))

    return [a * (1 - m) + b * m for m in alphas]
