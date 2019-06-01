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


def write_wavetable(wavetable, filename):
    """ Write wavetable to an h2p oscillator file

        @param wavetable zwave.WaveTable : Wavetable
        @param filename str : File name to write to
    """

    table_size = wavetable.wave_len

    if table_size is None:
        return

    with open(filename, 'w') as osc_file:

        osc_file.write("#defaults=no\n")
        osc_file.write("#cm=OSC\n")
        osc_file.write("Wave=2\n")
        osc_file.write("<?\n")
        osc_file.write("\n")

        osc_file.write("float Wave[")
        osc_file.write(str(table_size))
        osc_file.write("];\n")
        osc_file.write("\n")

        for i, wave in enumerate(wavetable.get_waves()):

            if wave is None:
                continue

            wave_num = i + 1
            # scale to avoid overflow resulting from finite precision
            scaled_wave = wave * 0.999969
            osc_file.write("//table ")
            osc_file.write(str(wave_num))
            osc_file.write("\n")

            for index, value in enumerate(scaled_wave):
                osc_file.write("Wave[")
                osc_file.write(str(index))
                osc_file.write("] = ")
                osc_file.write('{0:.10f}'.format(value))
                osc_file.write(";\n")

            osc_file.write("Selected.WaveTable.set(")
            osc_file.write(str(wave_num))
            osc_file.write(", Wave);\n")
            osc_file.write("\n")

        osc_file.write("?>")
