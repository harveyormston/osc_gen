#!/usr/bin/env python
""" Zebra oscillator waves """

from __future__ import division
from __future__ import print_function
import numpy as np

from osc_gen import wavfile
from osc_gen import dsp
from osc_gen import sig


class WaveTable(object):
    """ An n-slot wavetable """

    def __init__(self, waves=None, num_waves=16, wave_len=128):
        """
        Init

        @param waves sequence : A sequence of numpy arrays containing wave
            data to form the wavetable
        """

        self.num_waves = num_waves
        self.wave_len = wave_len

        if waves is None:
            self.waves = []
        else:
            self.waves = waves

    def clear(self):
        """ Clear the wavetable so that all slots contain zero """

        self.waves = []

    def get_wave_at_index(self, index):
        """
        Get the wave at a specific slot index

        @param index int : The slot index to get the wave from

        @returns np.ndarray : Wavefore at given index
        """

        if index >= len(self.waves):
            return np.zeros(self.wave_len)
        else:
            return self.waves[index]

    def get_waves(self):
        """ Get all of the waves in the table """

        for i in range(self.num_waves):
            yield self.get_wave_at_index(i)

    def from_wav(self, filename):
        """
        Populate the wavetable from a wav file by filling all slots with
        evenly-spaced single cycles from a wav file.

        @param filename str : Wav file name.

        @returns WaveTable : self, populated by content from the wav file
        settings as this one
        """

        def nearest(arr, val):
            """ find the nearest value in an array to a given value """
            return arr[np.argmin(np.absolute(arr - val))]

        a, fs = wavfile.read(filename, with_sample_rate=True)

        zero_crossings = np.where(np.diff(np.sign(a)) > 0)[0] + 1

        if len(zero_crossings) < 1:
            raise ValueError("No zero crossings found.")

        freq = dsp.fundamental(a, fs)
        samples_per_cycle = fs / freq
        end = len(a) - samples_per_cycle

        # Split the input into a number of indivdual cycles, evenly spaced
        # throughout the signal.
        # The number of cycles will be, at most, self.num_waves (less for a
        # input so short that there are not that many complete cycles)
        # The start of each cycle occurs at a zero crossing.
        slots = np.linspace(0, end, self.num_waves)
        slots = np.around(slots).astype(int)
        slots = np.unique([nearest(zero_crossings, slot) for slot in slots])
        cycles = [a[x:x + int(samples_per_cycle)] for x in slots]

        sg = sig.SigGen()
        self.waves = [sg.arb(c) for c in cycles]

        return self
