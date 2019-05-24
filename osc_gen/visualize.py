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

    plt.figure(num=None, figsize=(2, 6), dpi=80, facecolor='w', edgecolor='k')

    for i, wave in enumerate(wavetable.waves):
        plt.plot(wave + (i * 2.01))

    plt.title(title)
    plt.show()
    plt.gcf().clear()
