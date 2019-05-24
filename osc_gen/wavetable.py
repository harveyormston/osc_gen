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

        @returns np.ndarray : Wave at given index
        """

        if index >= len(self.waves):
            return np.zeros(self.wave_len)

        return self.waves[index]

    def get_waves(self):
        """ Get all of the waves in the table """

        for i in range(self.num_waves):
            yield self.get_wave_at_index(i)

    def from_wav(self, filename, sig_gen=None, resynthesize=False):
        """
        Populate the wavetable from a wav file by filling all slots with
        cycles from a wav file.

        @param filename str : Wav file name.
        @param sig_gen SigGen : SigGen to use for regenerating the signal.
        @param resynthesize : If True, the signal is resynthesised using the
            harmonic series of the original signal - works best on signals with
            a low findamental frequency (< 200 Hz). If False, n evenly spaced
            single cycles are extracted from the input (default False).

        @returns WaveTable : self, populated by content from the wav file
        settings as this one
        """

        data, fs = wavfile.read(filename, with_sample_rate=True)

        if sig_gen is None:
            sig_gen = sig.SigGen()

        if resynthesize:

            num_sections = self.num_waves

            while True:
                data = data[:data.size - (data.size % num_sections)]
                sections = np.split(data, num_sections)
                try:
                    self.waves = [dsp.resynthesize(s, sig_gen) for s in sections]
                    break
                except dsp.NotEnoughSamplesError as exc:
                    num_sections -= 1
                    if num_sections <= 0:
                        raise exc

            if num_sections < self.num_waves:
                self.waves = sig.morph(self.waves, self.num_waves)

        else:
            cycles = dsp.slice_cycles(data, self.num_waves, fs)
            self.waves = [sig_gen.arb(c) for c in cycles]

        return self
