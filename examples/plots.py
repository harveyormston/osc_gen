#!/usr/bin/env python3
"""
Copyright 2019 Harvey Ormston

This file is part of osc_gen.

    osc_gen is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    osc_gen is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with osc_gen.  If not, see <https://www.gnu.org/licenses/>.
"""

import os
import numpy as np
from osc_gen import wavetable, dsp, sig, visualize


def main():
    """ main function """

    sgen = sig.SigGen()

    wave_sets = [
        [dsp.clip(sgen.sin(), x / 10) for x in range(16)],
        [dsp.tube(sgen.sin(), x) for x in range(1, 17)],
        [dsp.fold(sgen.sin(), x / 10) for x in range(16)],
        [dsp.shape(sgen.sin(), 1.0, power=x) for x in range(1, 17)],
        [dsp.slew(sgen.pls(x), x) for x in np.linspace(-0.5, 0.5, 16)],
        [dsp.downsample(sgen.sin(), x + 1) for x in range(8)],
        [dsp.quantize(sgen.sin(), (4 - x) * 2) for x in range(4)]
    ]

    titles = ('clip', 'tube', 'fold', 'shape', 'slew', 'downsample', 'quantize')

    for waves, title in zip(wave_sets, titles):
        wtab = wavetable.WaveTable(len(waves), waves)
        save = os.path.join('examples', 'images', "{}.png".format(title))
        visualize.plot_wavetable(wtab, title=title, save=save)


if __name__ == '__main__':
    main()
