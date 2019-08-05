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
from osc_gen import wavetable, dsp, sig, visualize, wavfile


def main():
    """ main function """

    sgen = sig.SigGen(1024)

    wave_sets = [
        [dsp.clip(sgen.sin(), x / 10) for x in range(16)],
        [dsp.tube(sgen.sin(), x) for x in range(1, 17)],
        [dsp.fold(sgen.sin(), x / 10) for x in range(16)],
        [dsp.shape(sgen.sin(), 1.0, power=x) for x in range(1, 17)],
        [dsp.slew(sgen.sqr(), x) for x in np.linspace(0.001, 0.1, 16)],
        [dsp.downsample(sgen.sin(), x * 4) for x in range(1, 9)],
        [dsp.quantize(sgen.sin(), x) for x in range(9, 1, -1)],
        [sgen.noise(0, 0.01),
         sgen.exp_saw(),
         sgen.exp_sin(3),
         sgen.sqr_saw(0.75),
         sgen.sharkfin(0.04)]
    ]

    titles = ('clip', 'tube', 'fold', 'shape', 'slew', 'downsample',
              'quantize', 'fin_exp_sqrsaw')

    for waves, title in zip(wave_sets, titles):
        wtab = wavetable.WaveTable(len(waves), waves)
        save = os.path.join('examples', 'images', "{}.png".format(title))
        visualize.plot_wavetable(wtab, title=title, save=save)
        wavfile.write_wavetable(wtab, "{}.wav".format(title))


if __name__ == '__main__':
    main()
