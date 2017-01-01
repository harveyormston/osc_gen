""" Plot waveforms """
import matplotlib.pyplot as plt


def plot_wave(wave):
    """ Plot a single wave """

    plt.plot(wave)
    plt.show()
    plt.gcf().clear()


def plot_wavetable(wavetable, title=''):
    """ Plot all waves in a wavetable """

    for wave in wavetable.waves:
        plt.plot(wave)

    plt.title(title)
    plt.show()
    plt.gcf().clear()
