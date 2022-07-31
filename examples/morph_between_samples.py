#!/usr/bin/env python3

# This example creates a wave table by interpolating between two or more user-defined
# (single-cycle) samples. Result is written to an output WAV file.

import sys
import argparse
from osc_gen import wavetable
from osc_gen import sig
from osc_gen import visualize
import soundfile as sf


def parseCommandLine():
    """Parse command line arguments"""

    # Create PARSER
    PARSER = argparse.ArgumentParser(
        description="Interpolate 2 or more single-cycle samples to wave table, " \
                    "and write result to WAV file.")

    # Add arguments
    PARSER.add_argument('slots',
                        action="store",
                        type=int,
                        help="number of slots")
    PARSER.add_argument('fileOut',
                        action="store",
                        type=str,
                        help="output WAV file")
    PARSER.add_argument('samplesIn',
                        action="store",
                        type=str,
                        nargs='+',
                        help="input samples")

    # Parse arguments
    args = PARSER.parse_args()

    return args


def main():

    # Parse command line arguments
    args = parseCommandLine()

    slots = args.slots
    fileOut = args.fileOut
    samples = args.samplesIn

    if len(samples) < 2:
        sys.stderr.write("Error: number of input samples must be 2 or more\n")
        sys.exit()

    # Establish wave length from first sample
    sampleData, sampleRate = sf.read(samples[0])
    waveLength = len(sampleData)

    # Create signal generator instance
    sg = sig.SigGen(num_points=waveLength)

    # Create wave table instance
    wt = wavetable.WaveTable(slots)

    # In the following block we create a list that contains the data from
    # all input samples

    wavesIn = []

    for sample in samples:
        # Read sample data
        try:
            sampleData, sampleRate = sf.read(sample)
        except:
            sys.stderr.write("Error: cannot read file " + sample + "\n")
            sys.exit()
        # Create arbitrary wave instance from sample data
        waveIn = sg.arb(sampleData)
        # Append to list of input waves
        wavesIn.append(waveIn)

    # Fill all wave table slots by interpolating between input waves 
    wt.waves = sig.morph(wavesIn, slots)

    # Plot resulting wave table
    visualize.plot_wavetable(wt)

    # Write to wav file
    wt.to_wav(fileOut)


if __name__ == "__main__":
    main()
