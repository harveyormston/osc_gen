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

import matplotlib.pyplot as plt
import numpy as np


def plot_wave(wave):
    """ Plot a single wave """

    plt.plot(wave)
    plt.show()
    plt.gcf().clear()


def plot_wavetable(wavetable, subplots=True, title=''):
    """ Plot all waves in a wavetable """

    cmap = plt.get_cmap("winter")
    colors = [cmap(i) for i in np.linspace(0, 1, wavetable.num_slots)]

    if subplots:
        _, axs = plt.subplots(wavetable.num_slots, 1, sharex=True)
        axs[0].set_title(title)
        for i, wave in enumerate(wavetable.waves):
            axs[i].plot(wave, color=colors[i])
            axs[i].set_ylabel("slot {}".format(i), rotation=0)
            axs[i].grid(True)
    else:
        plt.title(title)
        for i, wave in enumerate(wavetable.waves):
            plt.plot(wave, color=colors[i], label="slot {}".format(i))
        plt.legend()

    plt.grid(True)
    plt.show()
    plt.gcf().clear()
