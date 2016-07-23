import os
import platform
from itertools import product

import visualise
import zwave
import zosc
import sig
import dsp

# CAUTION! RUNNING THIS CREATES FILES IN YOUR USER LIBRARY!
# IF THERE ARE EXISTING FILES IN THE ZEBRA OSCILLATOR USER LIBRARY THAT HAPPEN
# TO HAVE THE SAME NAMES AS THE ONES CREATED HERE, THEY WILL BE OVERWRITTEN!

# these examples show how to:

# - use the sig module to generate oscillator shapes.
# - use the zwave module to create an (up to) 16 slot wavetable for zebra out
#   of oscillator waveforms.
# - use the zosc module to store wavetables as a zebra oscillator file

# _____________________________________________________________________________
# first, let's set up a location to store the resulting oscillator files
# on OSX, this is the standard u-he area in Application Support.
# on other platform, a local directory is used.

STORE_FILES = False

if platform.system() == 'Darwin':
    home = os.path.expanduser('~')
    osc_path = 'Library/Application Support/u-he/Zebra2/Modules/Oscillator'
else:
    d = 'oscillator_pack'
    if not os.path.exists(d):
        os.mkdir(d)
    osc_path = d
    

# create a signal generator
sg = sig.SigGen()
# create a wave table to hold the waves
wt = zwave.WaveTable()
# create a zebra oscillator to store the final wave table
zo = zosc.Osc(wt)

bit_depths = (16, 6, 3)
dowsample_factors = (1, 4, 8, 16)
slew_rates = (0.1, 0.5, 0.8)
slew_invert = (False, True)

params = product(
    bit_depths,
    dowsample_factors,
    slew_rates,
    slew_invert)

for p in params:

    bd = p[0]
    ds = p[1]
    sr = p[2]
    si = p[3]

    fn = 'og_stsp_{0}{1}{2}{3}'
    fn = fn.format(bd, ds, sr, si)
    fn = fn.replace('.', '')
    fn = fn.replace('False', 's')
    fn = fn.replace('True', 'o')
    fn += '.h2p'

    ws = []
    raw = (
        sg.sin(),
        sg.tri(),
        sg.saw(),
        sg.pls(1./14),
        sg.pls(2./14),
        sg.pls(3./14),
        sg.pls(4./14),
        sg.pls(5./14),
        sg.pls(6./14),
        sg.pls(7./14),
        sg.pls(8./14),
        sg.pls(9./14),
        sg.pls(10./14),
        sg.pls(11./14),
        sg.pls(12./14),
        sg.pls(13./14),
    )

    for w in raw:
        dsp.downsample(w, ds)
        dsp.quantise(w, bd)
        dsp.slew(w, sr, si)
        ws.append(w)

    # set the wavetable and store it as an oscillator
    wt.set_waves(zwave.Wave(s) for s in ws)
    f = os.path.join(home, osc_path, fn)
    if STORE_FILES:
        zo.write_to_file(f)
    else:
        visualise.plot_wavetable(wt)
