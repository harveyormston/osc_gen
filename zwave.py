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


class WaveTableSlot():
    """ One wave cycle slot within the wavetable """

    min_index = 1
    max_index = 16

    def __init__(self, index, wave):
        """ Init

            @param index int : The slot number
            @param wave Wave() : The wave cycle
        """

        if not self.min_index <= index <= self.max_index:
            m = "Wavetable index {0} outside valid range {1} to {2}"
            raise ValueError(m.format(index, self.min_index, self.max_index))

        self.index = index
        self.wave = wave

    def set_wave(self, wave):
        """ Set the wave in this slot

            @param wave Wave() : The wave
        """

        self.wave = wave

    def set_index(self, index):
        """ Set the index of this slot

            @param index int : The index
        """

        self.index = index


class WaveTable():
    """ A 16-slot wavetable """

    max_slots = 16

    def __init__(self, waves=None):
        """ Init

            @param waves sequence : A sequence of Wave() objects which make up
                                    the wavetable
        """

        self.slots = []
        self.zero_empty_slots()

    def clear(self):
        """ Clear the wavetable so that all slots contain zero """

        self.slots = []
        self.zero_empty_slots()

    def get_sorted_slots(self):
        """ Get the slots which are not empty in order of index """

        for index in range(1, self.max_slots + 1):
            yield self.get_item_in_slot(index)

    def get_item_in_slot(self, slot):
        """ Get the wave at a specific slot index

            @param index int : The slot index to get the wave from
        """

        for w in self.slots:
            if w.index is slot:
                return w

    def set_waves(self, waves):
        """ Set the wavetable itmes from a seuqnce of Waves. If not enough waves
            are provided to fill the table, the remaining older items will
            remain.

            @param waves sequence : A sequence of Wave() objects which make up
                                    the wavetable
        """

        for i, w in enumerate(waves):
            self.set_wave_in_slot(i + 1, w)

    def set_wave_in_slot(self, slot, wave):
        """ Set the wave cycle at a specific slot index

            @param slot int : The slot index
            @param wave Wave() : The wave cycle
        """

        s = self.get_item_in_slot(slot)

        if s is None:
            self.slots.append(WaveTableSlot(slot, wave))
        else:
            s.set_wave(wave)

    def zero_empty_slots(self):
        """ Set the wave cycle to an empty wave cycle (all zeros)
            in all empty slots.
        """

        for i, s in enumerate(self.get_sorted_slots()):
            if s is None:
                self.set_wave_in_slot(i + 1, Wave())
