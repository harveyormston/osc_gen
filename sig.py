""" Tools for generating and interpolating between waeform cycles. """

from scipy.interpolate import interp1d
import numpy as np


class SigGen():
    """ Signal Generator """

    def __init__(self):
        """ Init """

        self.num_points = 128
        self.amp = 1.0
        self.offset = 0.0

    def __base(self):
        """ Generate the base waveform cycle, a sawtooth or ramp from -1 to 1
        """

        rmax = self.num_points / 2
        rmin = -rmax

        for v in range(rmin, rmax):
            x = v / float(rmax)
            yield x

    def __scale(self, value):
        """ Scale a value so that it has the required amplitude and offset
            applied.
        """

        return value * self.amp + self.offset

    def saw(self):
        """ Generate a sawtooth wave cycle """

        for s in self.__base():
            yield self.__scale(s)

    def tri(self):
        """ Generate a triangle wave cycle """

        for s in self.__base():
            yield self.__scale(s * 2 + 1 if s < 0 else s * -2 + 1)

    def pls(self, pw):
        """ Generate a pulse wave cycle

            @param pw float : Pulse width or duty cycle, between 0 and 1
        """

        t = pw * 2 - 1
        for s in self.__base():
            yield self.__scale(-1.0 if s < t else 1.0)

    def sqr(self):
        """ Generate a square wave cycle """

        return self.pls(0.5)

    def sin(self):
        """ Generate a sine wave cycle """

        for x in (np.sin(np.pi * (a + 0.5)) for a in self.__base()):
            yield self.__scale(x)

    def custom(self, data):
        """ Generate a custom wave cycle. The provided data will be interpolated
            to occupy the correct number of samples for a single cycle at our
            reference frequency and then normalised and scaled as appropriate.

            @param data seq : A sequence of samples representing a single cycle
                              of a wave
        """

        y = list(data)
        x = range(len(y))
        f = interp1d(x, y)
        xx = np.linspace(x[0], x[-1], self.num_points)
        for x in normalise(f(xx)):
            yield self.__scale(x)


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

    # TODO: return a generator instead of an iterator
    morphed = []
    a = None
    b = None
    i = 0
    for ss in s:
        b = list(ss)
        if a is not None:
            if i is 0:
                o = 0
            else:
                o = 1

            n = list(list(x) for x in __morph_two(a, b, r[i]))[o:]
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

    alphas = (s * 1. / (n - 1) for s in range(n))

    # must transform to iterators as a generator would be exhausted
    # on the first iteration of the zip operation
    a = list(a)
    b = list(b)

    return ((x * (1 - m) + y * m for x, y in zip(a, b)) for m in alphas)


def normalise(s):
    """ Normalise a wave cycle to within the range +/- 1

        @param s sequence : A wave cycle
    """

    a = list(s)
    p = max(a)
    p = max(p, abs(min(a)))
    g = 1. / p
    for x in s:
        yield g * x
