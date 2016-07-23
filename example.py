import os
import platform

import numpy as np
import visualise
import zwave
import zosc
import sig
import dsp

# these examples show how to:

# - use the sig module to generate oscillator shapes.
# - use the zwave module to create an (up to) 16 slot wavetable for zebra out
#   of oscillator waveforms.
# - use the zosc module to store wavetables as a zebra oscillator file

# _____________________________________________________________________________
# first, let's set up a location to store the resulting oscillator files
# on OSX, this is the standard u-he area in Application Support.
# on other platfroms, a local directory is used.

STORE_FILES = False

if platform.system() == 'Darwin':
    home = os.path.expanduser('~')
    osc_path = 'Library/Application Support/u-he/Zebra2/Modules/Oscillator'
else:
    d = 'oscillator_pack'
    if not os.path.exists(d):
        os.mkdir(d)
    osc_path = d

# _____________________________________________________________________________
# example setup: initial setup of the objects we'll need in order to create and
# store oscillators

# create a signal generator
sg = sig.SigGen()

# create a wave table to store the waves
wt = zwave.WaveTable()

# create a zebra oscillator to store the final wave table
zo = zosc.Osc(wt)

# _____________________________________________________________________________
# example 1: generate and save a simple saw wave

# generate a saw using our signal generator and store it in a new Wave object.
m = zwave.Wave(sg.saw())

# put the saw wave into our wave table.
wt.set_waves((m,))
# as we're only adding one wave to the wave table, only the first slot of the
# resulting oscillator in zebra will contain the saw. the remaining slots will
# be empty, because we haven't added anything to those yet.

if STORE_FILES:
    # write the resulting oscillator to a file
    f = os.path.join(home, osc_path, 'osc_gen_saw.h2p')
    zo.write_to_file(f)
else:
    visualise.plot_wavetable(wt)

# you could fill all 16 slots with the same saw, by repeating it 16 times when
# calling set_waves() on the wave table, if you wanted:

# we do need to generate the saw again. sig tends to return Python generators
# where possible, which means they can become empty once they've been used
# once, unless you store them as a list yourself.
m = zwave.Wave(sg.saw())

# repeat the saw 16 times in the wavetable
wt.set_waves((m for _ in range(16)))

if STORE_FILES:
    # write the resulting oscillator to a file
    f = os.path.join(home, osc_path, 'osc_gen_saw16.h2p')
    zo.write_to_file(f)
else:
    visualise.plot_wavetable(wt)

# _____________________________________________________________________________
# example 2: morphing between two waveforms
# we can use up all 16 slots in the zebra oscillator, even with fewer than 16
# starting waveforms, if we use morph() to morph from one waveform to the
# other, to fill in the in-between slots.

# morph from sine to triangle over 16 slots
ws = (zwave.Wave(s) for s in sig.morph((sg.sin(), sg.tri()), 16))

# set the wavetable and store it as an oscillator
wt.set_waves(ws)

if STORE_FILES:
    f = os.path.join(home, osc_path, 'osc_gen_sin_tri.h2p')
    zo.write_to_file(f)
else:
    visualise.plot_wavetable(wt)

# of course, we don't have to use all 16 slots. we could use only the first 5,
# for example.
# but first, we should clear the wavetable, so that the slots above 5 don't
# end up containing any older data.
wt.clear()

# morph from sine to triangle over 5 slots
ws = (zwave.Wave(s) for s in sig.morph((sg.sin(), sg.tri()), 5))

# set the wavetable and store it as an oscillator
wt.set_waves(ws)

if STORE_FILES:
    f = os.path.join(home, osc_path, 'osc_gen_sin_tri5.h2p')
    zo.write_to_file(f)
else:
    visualise.plot_wavetable(wt)

# _____________________________________________________________________________
# example 3: morphing between many waveforms
# we can morph between any number of waveforms, with a couple of conditions:
# - we can't morph between more than 16 waves, because the zebra wavetable only
#   contains 16 slots.
# - we can't morph a number of waves over smaller number of slots. e.g. we
#   can't morph 5 waves into 3 slots. if you want to do that, you'd need to use
#   morph to compress your 5 waves into 3 'in-between' waves first, and the
#   the decision over which waves to keep and which to compress isn't a
#   decision morph should make for you.

# morph between sine, triangle, saw and square over 16 slots
ws = (zwave.Wave(s) for s in
      sig.morph((sg.sin(), sg.tri(), sg.saw(), sg.sqr()), 16))

# set the wavetable and store it as an oscillator
wt.set_waves(ws)

if STORE_FILES:
    f = os.path.join(home, osc_path, 'osc_gen_sin_tri_saw_sqr.h2p')
    zo.write_to_file(f)
else:
    visualise.plot_wavetable(wt)

# _____________________________________________________________________________
# example 4: generting your own waves
# you can create a custom signal yourself to use as an oscillator.
# in this example, one slot is filled with random data, but you could
# use any data you've generated or, say, read in from a wav file.

# generate some random data
random_wave = np.random.uniform(low=-1, high=1, size=128)

# the custom signal generator function automatically normaises and scales any
# data you throw at it to the right ranges, which is useful.
r = zwave.Wave(sg.custom(random_wave))

# clear the wavetable, so that the slots above 1 don't contain any older data.
wt.clear()

# set the wavetable and store it as an oscillator
wt.set_waves((r,))

if STORE_FILES:
    f = os.path.join(home, osc_path, 'osc_gen_random.h2p')
    zo.write_to_file(f)
else:
    visualise.plot_wavetable(wt)

# _____________________________________________________________________________
# example 5: pulse-width modulation
# SigGen has a pulse wave generator too.
# let's use that to make a pwm wavetable.

# pulse widths are between 0 and 1 (0 to 100%).
# 0 and 1 are silent as the pulse is a flat line.
# so, we want to have 16 different, equally spaced pulse widths, increasing in
# duration, but also avoid any silence:
pws = (i / 17. for i in range(1, 17))

# generate the 16 pulse waves
ws = (zwave.Wave(sg.pls(p)) for p in pws)

# set the wavetable and store it as an oscillator
wt.set_waves(ws)

if STORE_FILES:
    f = os.path.join(home, osc_path, 'osc_gen_pwm.h2p')
    zo.write_to_file(f)
else:
    visualise.plot_wavetable(wt)

# _____________________________________________________________________________
# example 6: processing wave forms
# the dsp module can be used to process waves in various ways

# let's try downsampling a sine
ds = dsp.downsample(sg.sin(), 16)

# that downsampled sine from probably sounds pretty edgy
# let's try that again with some slew this time, to smooth it out a bit
sw = dsp.slew(dsp.downsample(sg.sin(), 16), 0.8)

# generate a triangle wave and quantise (bit crush) it
qt = dsp.quantise(sg.tri(), 3)

# applying inverse slew, or overshoot, to a square wave
ss = dsp.slew(sg.sqr(), 0.8, inv=True)

# overshoot might make the wave quieter, so let's normalise it
dsp.normalise(ss)

# morph between the waves over 16 slots
ws = (zwave.Wave(s) for s in sig.morph((ds, sw, qt, ss), 16))

# set the wavetable and store it as an oscillator
wt.set_waves(ws)

if STORE_FILES:
    f = os.path.join(home, osc_path, 'osc_gen_dsp.h2p')
    zo.write_to_file(f)
else:
    visualise.plot_wavetable(wt)
