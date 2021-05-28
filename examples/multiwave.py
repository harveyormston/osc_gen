#!/usr/bin/env python3
"""
Copyright 2021 Harvey Ormston

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

# This example combines multiple single-cycle wav files into a WaveTable.

import os
import argparse

import numpy as np
import soundfile as sf

from osc_gen import visualize
from osc_gen import wavetable
from osc_gen import wavfile
from osc_gen import zosc

STORE_FILES = True
SHOW_PLOTS = True

DESCRIPTION = (
    'Convert single-cycle wav files in a directory ' +
    'into a wavetable. Assumes that the direcory contains ' +
    'wav files at the root level. Does not look in subdirectories.'
)

HELP_CYCLE_DIR = 'Directory to look for wav files.'
HELP_NUM_SLOTS = 'Number of slots in output wavetable (default=16).'
HELP_WAVE_LEN = 'Length of the output waves (default=128).'

HELP_SELECT = (
    'How to select files (first, last, even, default=first). ' +
    'first: chose the first X files from a list of Y files, ' +
    'last: chose the last X files from a list of Y files, ' +
    'even: chose X files evenly spaced from a list of Y files.')

HELP_SORT = (
    'How to sort files (alpha, random, reverse, default=alpha): ' +
    'alpha: alphabetical sort, ' +
    'random: random sort, ' +
    'reverse: reverse alphabetical sort.'
)

HELP_NAME = 'Name of the output file.'


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
        fname = os.path.join(osc_path, name + '.h2p')
        print("Saving to {}".format(fname))
        zosc.write_wavetable(zwt, fname)
        fname = os.path.join(osc_path, name + '.wav')
        print("Saving to {}".format(fname))
        wavfile.write_wavetable(zwt, fname)
    if SHOW_PLOTS:
        visualize.plot_wavetable(zwt, title=name)


def check_args(args, parser):
    """ Validate arguments """

    if args.num_slots < 1:
        parser.error('Minimum num_slots is 1')

    if args.wave_len < 2:
        parser.error('Minimum wave_len is 2')

    if not os.path.exists(args.cycle_dir):
        parser.error("error: Directory {} does not exist.".format(args.cycle_dir))

    if not os.path.isdir(args.cycle_dir):
        parser.error("error: {} is not a directory.".format(args.cycle_dir))

    if args.sort not in ('alpha', 'reverse', 'random'):
        parser.error("{} is not a valid sort option.".format(args.sort))

    if args.select not in ('first', 'last', 'even'):
        parser.error("{} is not a valid select option.".format(args.select))


def main():
    """ main """

    parser = argparse.ArgumentParser( description=DESCRIPTION)
    parser.add_argument('cycle_dir', help=HELP_CYCLE_DIR)
    parser.add_argument('--num_slots', default=16, type=int, help=HELP_NUM_SLOTS)
    parser.add_argument('--wave_len', default=128, type=int, help=HELP_WAVE_LEN)
    parser.add_argument('--select', default='first', help=HELP_SELECT)
    parser.add_argument('--sort', default='alpha', help=HELP_SORT)
    parser.add_argument('--name', default=None, help=HELP_NAME)
    args = parser.parse_args()

    check_args(args, parser)

    zwt = wavetable.WaveTable(args.num_slots, wave_len=args.wave_len)

    wavfiles = []

    print("Looking in directory {}".format(args.cycle_dir))

    for x in os.listdir(args.cycle_dir):
        if x.lower().endswith('.wav'):
            wavfiles.append(os.path.join(args.cycle_dir, x))

    print("Found {} wav files.".format(len(wavfiles)))

    if len(wavfiles) < zwt.num_slots:
        print("error: {} .wav files found in {}. Expected at least {}".format(
            len(wavfiles), args.cycle_dir, zwt.num_slots))
        exit()

    print("Sorting wav files using {}.".format(args.sort))

    if args.sort == 'alpha':
        wavfiles.sort()
    elif args.sort == 'reverse':
        wavfiles.sort(reverse=True)
    elif args.sort == 'random':
        np.random.shuffle(wavfiles)

    print("Selecting wav files using {}.".format(args.select))

    if args.select == 'first':
        wavfiles = wavfiles[:zwt.num_slots]
    elif args.select == 'last':
        wavfiles = wavfiles[-zwt.num_slots:]
    elif args.select == 'even':
        idx = np.round(np.linspace(0, len(wavfiles) - 1, args.num_slots)).astype(int)
        wavfiles = np.array(wavfiles)[idx].tolist()

    print("Selected these files:\n")

    for fname in wavfiles:
        print("\t", fname)
    print()

    zwt.waves = [sf.read(x)[0] for x in wavfiles]

    if args.name is None:
        name = os.path.basename(args.cycle_dir)
    else:
        name = args.name

    render(zwt, name)

    print("Done!")

if __name__ == '__main__':
    main()
