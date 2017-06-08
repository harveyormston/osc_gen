#!/usr/bin/env python
""" Zebra oscillator waves """

import numpy as np

from osc_gen import wavfile
from osc_gen import dsp
from osc_gen import sig


class WaveTable(object):
    """ An n-slot wavetable """

    def __init__(self, waves=None, num_waves=16, wave_len=128):
        """ Init

            @param waves sequence : A sequence of numpy arrays containing wave
                data to form the wavetable
        """

        self.waves = []
        self.num_waves = num_waves
        self.wave_len = wave_len
        self.waves = waves

    def clear(self):
        """ Clear the wavetable so that all slots contain zero """

        self.waves = []

    def get_wave_at_index(self, index):
        """ Get the wave at a specific slot index

            @param index int : The slot index to get the wave from
        """

        if index >= len(self.waves):
            return np.zeros(self.wave_len)
        else:
            return self.waves[index]

    def get_waves(self):
        """ Get all of the waves in the table """

        for i in range(self.num_waves):
            yield self.get_wave_at_index(i)

    def populate_from_wav(self, filename):
        """
        Populate the wavetable from a wav file by filling all slots with evenly-spaced
        single cycles from the wav file.
        """

        sg = sig.SigGen()
        a, fs = wavfile.read(filename, with_sample_rate=True)

        freq = dsp.fundamental(a, fs)
        cycle_length = fs / freq
        end = len(a) - cycle_length
        slots = np.arange(0, end, cycle_length)
        slots = np.around(slots).astype(int)

        self.waves = [sg.arb(a[x:x + int(cycle_length)]) for x in slots]
