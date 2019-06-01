#!/usr/bin/env python
""" Plot waveforms """

import matplotlib.pyplot as plt


def plot_wave(wave):
    """ Plot a single wave """

    plt.plot(wave)
    plt.show()
    plt.gcf().clear()


def plot_wavetable(wavetable, title=''):
    """ Plot all waves in a wavetable """

    _, axs = plt.subplots(wavetable.num_waves, 1, sharex=True)

    axs[0].set_title(title)

    for i, wave in enumerate(wavetable.waves):
        axs[i].plot(wave)

    plt.show()
    plt.gcf().clear()
