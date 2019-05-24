""" Plotting examples """

from osc_gen import wavetable, dsp, sig, visualize


def main():
    """ main function """

    sgen = sig.SigGen()

    waves = [dsp.tube(sgen.sin(), x) for x in range(1, 17)]
    wtab = wavetable.WaveTable(waves)
    visualize.plot_wavetable(wtab, title='tube')

    waves = [dsp.clip(sgen.sin(), x) for x in range(1, 17)]
    wtab = wavetable.WaveTable(waves)
    visualize.plot_wavetable(wtab, title='clip')

    waves = [dsp.fold(sgen.sin(), x) for x in range(1, 17)]
    wtab = wavetable.WaveTable(waves)
    visualize.plot_wavetable(wtab, title='fold')

    waves = [dsp.shape(sgen.sin(), x) for x in range(1, 17)]
    wtab = wavetable.WaveTable(waves)
    visualize.plot_wavetable(wtab, title='shape')

    waves = [dsp.slew(sgen.sqr(), 1 / x) for x in range(1, 9)]
    waves += [dsp.slew(sgen.sqr(), 1 / x) for x in range(-8, 0)]
    wtab = wavetable.WaveTable(waves)
    visualize.plot_wavetable(wtab, title='slew')

    waves = [dsp.downsample(sgen.sin(), x) for x in range(1, 17)]
    wtab = wavetable.WaveTable(waves)
    visualize.plot_wavetable(wtab, title='downsample')

    waves = [dsp.quantize(sgen.sin(), x) for x in range(1, 17)]
    wtab = wavetable.WaveTable(waves)
    visualize.plot_wavetable(wtab, title='quantize')


if __name__ == '__main__':
    main()
