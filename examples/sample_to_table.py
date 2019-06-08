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

from __future__ import print_function
import os
import sys

from osc_gen import wavetable
from osc_gen import zosc
from osc_gen import sig

def main():
    """ convert wav file to wavetable using slicing and resynthesis """

    if len(sys.argv) < 3:
        print("Usage: {0} WAV_FILE CYCLES".format(sys.argv[0]))
        exit()

    lib_path = '.'

    name = os.path.splitext(sys.argv[1])[0]
    sig_gen = sig.SigGen(num_points=int(sys.argv[2]))

    # resynthesize
    wt = wavetable.WaveTable(128)
    wt.from_wav('{0}.wav'.format(name), sig_gen=sig_gen, resynthesize=True)
    out = os.path.join(lib_path, '{0}_resynth.h2p'.format(name))
    print("write {}".format(out))
    zosc.write_wavetable(wt, out)

    # slice
    wt = wavetable.WaveTable(128)
    wt.from_wav('{0}.wav'.format(name), sig_gen=sig_gen)
    out = os.path.join(lib_path, '{0}_slice.h2p'.format(name))
    print("write {}".format(out))
    zosc.write_wavetable(wt, out)


if __name__ == '__main__':
    main()
