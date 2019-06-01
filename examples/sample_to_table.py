""" convert a wav file to a wavetable """
from __future__ import print_function
import os
import sys

from osc_gen import wavetable
from osc_gen import zosc

if len(sys.argv) < 2:
    print("Usage: {0} WAV_FILE".format(sys.argv[0]))
    exit()

lib_path = '.'

name = os.path.splitext(sys.argv[1])[0]

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
