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

from osc_gen import wavetable, dsp, sig, visualize


def main():
    """ main function """

    sgen = sig.SigGen()

    waves = [dsp.tube(sgen.sin(), x) for x in range(1, 17)]
    wtab = wavetable.WaveTable(waves)
    visualize.plot_wavetable(wtab, title='tube')

    waves = [dsp.clip(sgen.sin(), x) for x in range(1, 17)]
    wtab = wavetable.WaveTable(waves)
    visualize.plot_wavetable(wtab, title='clip')

    waves = [dsp.fold(sgen.sin(), x) for x in range(1, 17)]
    wtab = wavetable.WaveTable(waves)
    visualize.plot_wavetable(wtab, title='fold')

    waves = [dsp.shape(sgen.sin(), x) for x in range(1, 17)]
    wtab = wavetable.WaveTable(waves)
    visualize.plot_wavetable(wtab, title='shape')

    waves = [dsp.slew(sgen.sqr(), 1 / x) for x in range(1, 9)]
    waves += [dsp.slew(sgen.sqr(), 1 / x) for x in range(-8, 0)]
    wtab = wavetable.WaveTable(waves)
    visualize.plot_wavetable(wtab, title='slew')

    waves = [dsp.downsample(sgen.sin(), x) for x in range(1, 17)]
    wtab = wavetable.WaveTable(waves)
    visualize.plot_wavetable(wtab, title='downsample')

    waves = [dsp.quantize(sgen.sin(), x) for x in range(1, 17)]
    wtab = wavetable.WaveTable(waves)
    visualize.plot_wavetable(wtab, title='quantize')


if __name__ == '__main__':
    main()
