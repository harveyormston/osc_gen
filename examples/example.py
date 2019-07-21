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

# These examples show how to:
#
#     - use the sig module to generate oscillator shapes.
#     - use the wavetable module to create multi-slot wavetables out of
#       oscillator waveforms.
#     - use the zosc module to store wavetables as a zebra oscillator file
#     - use the wavfile module to store wavetables as a wav file



import os

import numpy as np
from osc_gen import visualize
from osc_gen import wavetable
from osc_gen import wavfile
from osc_gen import zosc
from osc_gen import sig
from osc_gen import dsp

STORE_FILES = True
SHOW_PLOTS = True


def make_osc_path():
    """ Create or derive the path in which to store generated oscillator files.
    """

    home = '.'
    osc_path = 'example_files'
    if not os.path.exists(osc_path):
        os.mkdir(osc_path)

    return os.path.join(home, osc_path)


def render(zwt, name):
    """ Write to file or plot a wavetable """

    if STORE_FILES:
        osc_path = make_osc_path()
        fname = name + '.h2p'
        zosc.write_wavetable(zwt, os.path.join(osc_path, fname))
        fname = name + '.wav'
        wavfile.write_wavetable(zwt, os.path.join(osc_path, fname))
    if SHOW_PLOTS:
        visualize.plot_wavetable(zwt, title=name)


def main():
    """ main """

    # create a signal generator
    sig_gen = sig.SigGen()

    # create a wave table to store the waves
    zwt = wavetable.WaveTable(16)

    # example 1: generate and save a simple saw wave

    # generate a saw using our signal generator and store it in a new Wave
    # object.
    saw_wave = sig_gen.saw()

    # put the saw wave into our wave table.
    zwt.waves = [saw_wave]
    # as we're only adding one wave to the wave table, only the first slot of
    # the resulting oscillator in zebra will contain the saw. the remaining
    # slots will be empty, because we haven't added anything to those yet.

    render(zwt, 'osc_gen_saw')

    # you could fill all 16 slots with the same saw, by repeating it 16 times
    zwt.waves = [saw_wave for _ in range(16)]

    render(zwt, 'osc_gen_saw_16')

    # example 2: morphing between two waveforms we can use up all 16 slots in
    # the zebra oscillator, even with fewer than 16 starting waveforms, if we
    # use morph() to morph from one waveform to the other, to fill in the
    # in-between slots.

    # morph from sine to triangle over 16 slots
    zwt.waves = sig.morph((sig_gen.sin(), sig_gen.tri()), 16)

    render(zwt, 'osc_gen_sin_tri')

    # of course, we don't have to use all 16 slots. we could use only the first
    # 5, for example.
    # morph from sine to triangle over 5 slots
    zwt.waves = sig.morph((sig_gen.sin(), sig_gen.tri()), 5)

    render(zwt, 'osc_gen_sin_tri_5')

    # example 3: morphing between many waveforms
    # it is possible to morph between any number of waveforms, to produce
    # interpolated waves between the given waves.

    # morph between sine, triangle, saw and square over 16 slots
    zwt.waves = sig.morph((sig_gen.sin(),
                           sig_gen.tri(),
                           sig_gen.saw(),
                           sig_gen.sqr()), 16)

    render(zwt, 'osc_gen_sin_tri_saw_sqr')

    # example 4: generting arbitrary waves
    # a custom signal can be used as an oscillator.
    # in this example, one slot is filled with random data, but any data,
    # generated or, say, read in from a wav file, can be used.

    # the custom signal generator function automatically normaises and scales
    # any data you throw at it to the right ranges, which is useful.
    zwt.waves = [sig_gen.arb(np.random.uniform(low=-1, high=1, size=128))
                 for _ in range(16)]

    render(zwt, 'osc_gen_random')

    # example 5: pulse-width modulation
    # SigGen has a pulse wave generator too.
    # let's use that to make a pwm wavetable.

    # pulse widths are between 0 and 1 (0 to 100%).  0 and 1 are silent as the
    # pulse is a flat line.  so, we want to have 16 different, equally spaced
    # pulse widths, increasing in duration, but also avoid any silence:
    pws = (i / 17. for i in range(1, 17))

    # generate the 16 pulse waves
    zwt.waves = [sig_gen.pls(p) for p in pws]

    render(zwt, 'osc_gen_pwm')

    # example 6: other wave shapes
    # Other wave shapes are supported by the SigGen class, including:
    # - Shark Fin
    # - Exponential Saw
    # - Square Saw

    zwt.waves = [sig_gen.sharkfin(), sig_gen.exp_saw(), sig_gen.sqr_saw()]

    render(zwt, 'shark_exp_sqrsaw')

    # example 7: processing wave forms
    # the dsp module can be used to process waves in various ways

    # let's try downsampling a sine
    downsampled = dsp.downsample(sig_gen.sin(), 16)

    # that downsampled sine from probably sounds pretty edgy
    # let's try that again with some slew this time, to smooth it out a bit
    slewed = dsp.slew(dsp.downsample(sig_gen.sin(), 16), 0.8)

    # generate a triangle wave and quantize (bit crush) it
    quantized = dsp.quantize(sig_gen.tri(), 3)

    # applying inverse slew, or overshoot, to a square wave
    slewed_square = dsp.slew(sig_gen.sqr(), 0.8, inv=True)

    # overshoot might make the wave quieter, so let's normalize it
    dsp.normalize(slewed_square)

    # morph between the waves over 16 slots
    zwt.waves = sig.morph((downsampled,
                           slewed,
                           quantized,
                           slewed_square), 16)

    render(zwt, 'osc_gen_dsp')

    # example 8: longer wavetables, more processing and writing a wav file

    # wavetables can have any number of slots, this one has 120 slots
    lwt = wavetable.WaveTable(120)

    # similarly, a signal generator can generate any number of samples
    # a waveform coresponding to the frequency of C3 at 44.1 kHz would
    # have approx. 337 samples.
    mc_sig_gen = sig.SigGen()
    mc_sig_gen.num_points = 337

    # create ever-decreasing wave folding distortion over the wavetable
    lwt.waves = [dsp.fold(mc_sig_gen.sin(), (lwt.num_slots - i) / 50.)
                 for i in range(lwt.num_slots)]

    wavfile.write_wavetable(lwt, os.path.join(make_osc_path(), 'folding.wav'))

    # create ever-increasing wave shaping distortion over the wavetable
    lwt.waves = [dsp.shape(mc_sig_gen.sin(), power=i + 1)
                 for i in range(lwt.num_slots)]

    wavfile.write_wavetable(lwt, os.path.join(make_osc_path(), 'shaping.wav'))


if __name__ == "__main__":
    main()
