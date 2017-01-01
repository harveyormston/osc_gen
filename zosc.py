""" Zebra2 Oscillator wavetable """


def write_wavetable(wavetable, filename):
    """ Write wavetable to an h2p oscillator file

        @param wavetable zwave.WaveTable : Wavetable
        @param filename str : File name to write to
    """

    table_size = None
    for wave in wavetable.waves:
        if wave is not None:
            table_size = len(wave)
            break

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

        for i, wave in enumerate(wavetable.waves):

            if wave is None:
                continue

            osc_file.write("//table ")
            osc_file.write(str(i))
            osc_file.write("\n")

            for index, value in enumerate(wave):
                osc_file.write("Wave[")
                osc_file.write(str(index))
                osc_file.write("] = ")
                osc_file.write('{0:.10f}'.format(value))
                osc_file.write(";\n")

            osc_file.write("Selected.WaveTable.set(")
            osc_file.write(str(i))
            osc_file.write(", Wave);\n")
            osc_file.write("\n")

        osc_file.write("?>")
