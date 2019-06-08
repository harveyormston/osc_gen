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

from __future__ import division
from __future__ import print_function
import numpy as np

from osc_gen import wavfile
from osc_gen import dsp
from osc_gen import sig


class WaveTable(object):
    """ An n-slot wavetable """

    def __init__(self, num_slots, waves=None, wave_len=None):
        """
        Init

        @param waves sequence : A sequence of numpy arrays containing wave
            data to form the wavetable
        """

        self.num_slots = num_slots
        self.wave_len = wave_len

        self._waves = []

        if waves is not None:
            self.waves = waves

    @property
    def waves(self):
        """ wavetable waves """
        return self._waves

    @waves.setter
    def waves(self, value):

        if hasattr(value, '__iter__') and value:

            if self.wave_len is None:
                self.wave_len = len(value[0])
                self._waves = value
            else:
                self._waves = [sig.SigGen(num_points=self.wave_len).arb(x) for x in value]

        else:
            raise ValueError("Waves must be a sequence with length > 0")

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

        return sig.SigGen(num_points=self.wave_len).arb(self._waves[index])

    def get_waves(self):
        """ Get all of the waves in the table """

        for i in range(self.num_slots):
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
            sig_gen = sig.SigGen(num_points=self.wave_len)

        if resynthesize:

            num_sections = self.num_slots

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

            if num_sections < self.num_slots:
                self.waves = sig.morph(self.waves, self.num_slots)

        else:
            cycles = dsp.slice_cycles(data, self.num_slots, fs)
            self.waves = [sig_gen.arb(c) for c in cycles]

        return self

    def morph_with(self, other, in_place=False):
        """ Morph waves with contents of another wavetable

            @param other WaveTable : other wavetable

            @param in_place bool : If True, this WaveTable will be modified.
                If False, a new WaveTable will be created with the result of
                the morph
        """

        waves = [None for _ in range(self.num_slots)]

        for i in range(self.num_slots):
            wav_a = self.get_wave_at_index(i)
            wav_b = other.get_wave_at_index(i)
            # interpolate wav_b to the same length as a
            if other.wave_len != self.wave_len:
                wav_b = sig.SigGen(num_points=self.wave_len).arb(wav_b)
            waves[i] = sig.morph([wav_a, wav_b], 3)[1]

        if in_place:
            self.waves = waves
            return self

        return WaveTable(self.num_slots, waves=waves, wave_len=self.wave_len)
