import os
import platform

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
# on OSX, this is the standard u-he aread in Application Support, not sure
# where it is on other platofrms.

if platform.system() == 'Darwin':
    home = os.path.expanduser('~')
    osc_path = 'Library/Application Support/u-he/Zebra2/Modules/Oscillator'
else:
    m = ("I'm not sure where your oscillator library is. "
         "You should probably check.")
    raise Warning(m)

# let's make a processor and set some of its properties
p = dsp.Processor()
# create a signal generator
sg = sig.SigGen()
# create a wave table to hold the waves
wt = zwave.WaveTable()
# create a zebra oscillator to store the final wave table
zo = zosc.Osc(wt)

for bd in (16, 6, 3):
    for ds in (1, 4, 8, 16):
        for sr in (0.1, 0.5, 0.8):
            for si in (False, True):

                p.bit_depth = bd
                p.downsample_factor = ds
                p.slew_rate = sr
                sinv = si

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
                    pw = p.normalise(
                        p.slew(
                            p.quantise(
                                p.downsample(w)),
                            inv=sinv))

                    ws.append(pw)

                # set the wavetable and store it as an oscillator
                wt.set_waves(zwave.Wave(s) for s in ws)
                f = os.path.join(home, osc_path, fn)
                zo.write_to_file(f)
                print f
