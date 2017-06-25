""" convert a wav file to a wavetable """
from __future__ import print_function
import os
import sys

from osc_gen import wavetable
from osc_gen import zosc

if len(sys.argv) < 2:
    print("Usage: {0} WAV_FILE_PREFIX".format(sys.argv[0]))
    print("e.g., to convert sine.wav: {0} sine".format(sys.argv[0]))
    exit()

lib_path = os.path.join(
    os.path.expanduser("~"),
    "Library",
    "Application Support",
    "u-he",
    "Zebra2",
    "Modules",
    "Oscillator")

name = sys.argv[1]

# resynthesize
wt = wavetable.WaveTable().from_wav('{0}.wav'.format(name), resynthesize=True)
out = os.path.join(lib_path, '{0}_resynth.h2p'.format(name))
print("write {}".format(out))
zosc.write_wavetable(wt, out)

# slice
wt = wavetable.WaveTable().from_wav('{0}.wav'.format(name))
out = os.path.join(lib_path, '{0}_slice.h2p'.format(name))
print("write {}".format(out))
zosc.write_wavetable(wt, out)
