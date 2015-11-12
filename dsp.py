from numpy import floor
from numpy import ceil


class Processor():

    def __init__(self):

        self.amp = 1.0
        self.offset = 0.0
        self.slew_rate = 0.0
        self.downsample_factor = 1
        self.bit_depth = 16

    def scale(self, amp, offset):

        for sample in self.signal:
            yield sample * amp + offset

    def normalise(self, inp):

        a = list(inp)
        p = max(a)
        p = max(p, abs(min(a)))
        g = 1. / p

        for x in a:
            yield g * x

    def slew(self, inp, inv=False):

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

        m = 2 ** self.bit_depth - 1

        for s in inp:
            if s > 0:
                yield ceil(s * m) / m
            elif s < 0:
                yield floor(s * m) / m
            else:
                yield floor(-1e-15 * m) / m
