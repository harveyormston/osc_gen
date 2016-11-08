""" Zebra2 Oscillator wavetable """


class Osc():
    """ Zebra2 Oscillator wavetable """

    def __init__(self, wavetable):
        """ Init

            @param wavetable zwvae.WaveTable() : wavetable
        """

        self.wavetable = wavetable

    def write_to_file(self, filename):
        """ Write wavetable to an h2p oscillator file

            @param filename str : File name to write to
        """

        table_size = None
        for s in [wave.values for wave in self.wavetable.waves]:
            if s is not None:
                table_size = len(s)
                break

        if table_size is None:
            return

        with open(filename, 'w') as f:

            f.write("#defaults=no\n")
            f.write("#cm=OSC\n")
            f.write("Wave=2\n")
            f.write("<?\n")
            f.write("\n")

            f.write("float Wave[")
            f.write(str(table_size))
            f.write("];\n")
            f.write("\n")

            for i, s in enumerate([wave.values for wave in self.wavetable.waves]):

                if s is None:
                    continue

                f.write("//table ")
                f.write(str(i))
                f.write("\n")

                for index, value in enumerate(s):
                    f.write("Wave[")
                    f.write(str(index))
                    f.write("] = ")
                    f.write('{0:.10f}'.format(value))
                    f.write(";\n")

                f.write("Selected.WaveTable.set(")
                f.write(str(i))
                f.write(", Wave);\n")
                f.write("\n")

            f.write("?>")
