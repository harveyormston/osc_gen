""" Process waveformas """

from numpy import floor
from numpy import ceil


class Processor():
    """ Processor """

    def __init__(self):
        """ Init """

        self.amp = 1.0
        self.offset = 0.0
        self.slew_rate = 0.0
        self.downsample_factor = 1
        self.bit_depth = 16

    def normalise(self, inp):
        """ Normalise a signal to the range +/- 1

            @param inp seq : A sequence of samples

            @returns seq : The processed samples
        """

        a = list(inp)
        p = max(a)
        p = max(p, abs(min(a)))
        g = 1. / p

        for x in a:
            yield g * x

    def slew(self, inp, inv=False):
        """ Apply slew or overhoot to a signal. Slew smooths steep transients in
            the signal while overshoot results in a sharper transient with
            ringing.

            @param inp seq : A sequence of samples
            @param inv bool : If True, overshoot will be applied. if False,
                              slew will be applied. (default=False).

            @returns seq : The processed samples
        """

        a = self.slew_rate

        # process 2 cycles and return the last, in order to allow for
        # settling
        il = list(inp)
        l = len(il)
        il.extend(il)
        p = 0
        for i, s in enumerate(il):
            if inv:
                c = p * (a - 1) + (s * a)
            else:
                c = s * (1 - a) + (p * a)
            p = c
            if i >= l:
                yield c

    def downsample(self, inp):
        """ Reduce the effective sample rate of a signal, resulting in aliasing.

            @param inp seq : A sequence of samples

            @returns seq : The processed samples
        """

        if self.downsample_factor < 1:
            m = "Downsampling factor ({0}) cannot be < 1"
            raise ValueError(m.format(self.downsample_factor))

        if self.downsample_factor == 1:
            for sample in inp:
                yield sample
        else:
            # the aliasing is deliberate!
            ns = 0
            f = self.downsample_factor

            for sample in inp:
                ns += 1
                if ns is 1:
                    last = sample
                    yield sample
                else:
                    if ns >= f:
                        ns -= f
                    yield last

    def quantise(self, inp):
        """ Reduce the bit depth of a signal.

            @param inp seq : A sequence of samples

            @returns seq : The processed samples
        """

        m = 2 ** self.bit_depth - 1

        for s in inp:
            if s > 0:
                yield ceil(s * m) / m
            elif s < 0:
                yield floor(s * m) / m
            else:
                yield floor(-1e-15 * m) / m
