""" Zebra oscillator waves """

import numpy as np

class Wave():
    """ Single-cycle wave """

    smp_max = (2 ** 15 - 1.) / (2 ** 15)
    smp_min = -smp_max

    def __init__(self, data=None, length=128):
        """ Init

            @param data sequence : a single cycle's worth of
                                   samples between +/- 1
        """

        if data is None:
            self.values = np.zeros(length)
            self.wave_len = length
        else:
            self.wave_len = len(data)
            self.values = np.zeros(self.wave_len)
            self.set_wave(data)

    def set_sample(self, index, value, sat=True):
        """ Set a sample value within the wave cycle

            @param index int : Index of the sample
            @param value number : Value of the sample
            @param sat bool : If True, saturate at the upper/lower
                              limits (default=True)
        """

        if not 0 <= index < self.wave_len:
            m = "Waveform index {0} outside valid range {1} to {2}"
            raise ValueError(m.format(index, 0, self.wave_len - 1))

        if not self.smp_min <= value <= self.smp_max:
            if sat:
                if value > self.smp_max:
                    value = self.smp_max
                elif value < self.smp_min:
                    value = self.smp_min
            else:
                m = "Sample {0} outside valid range {1} to {2}"
                raise ValueError(m.format(value, self.smp_min, self.smp_max))

        self.values[index] = float(value)

    def set_wave(self, values):
        """ Set the values of the wave

            @param values sequence : a single cycle's worth of
                                     samples between +/- 1
        """

        for i, v in enumerate(values):
            self.set_sample(i, v)

        if i < self.wave_len - 1:
            m = "Not enough samples for a wave ({0})"
            raise ValueError(m.format(i + 1))


class WaveTable():
    """ An n-slot wavetable """


    def __init__(self, waves=None, num_waves=None):
        """ Init

            @param waves sequence : A sequence of Wave() objects which make up
                                    the wavetable
        """

        self.waves = []
        self.num_waves = 0
        self.set_waves(waves, num_waves)

    def clear(self):
        """ Clear the wavetable so that all slots contain zero """

        self.waves = []

    def get_wave_at_index(self, index):
        """ Get the wave at a specific slot index

            @param index int : The slot index to get the wave from
        """
        
        if index >= len(self.waves):
            return Wave()
        else:
            return self.waves[index]

    def set_waves(self, waves=None, num_waves=None):
        """ Set the wavetable items from a seuqnce of Waves. If not enough waves
            are provided to fill the table, the remaining older items will
            remain.

            @param waves sequence : A sequence of Wave() objects which make up
                                    the wavetable
        """

        if waves is None:
            self.waves = []
        else:
            self.waves = list(waves)
            if len(self.waves) <= self.num_waves:
                return

        if num_waves is None:
            if waves is None:
                self.num_waves = 0
            else:
                self.num_waves = len(self.waves)
        else:
            self.num_waves = num_waves
        
    def get_waves(self):

        for i in range(self.num_waves):
            yield self.get_wave_at_index(i)
