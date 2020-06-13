# osc_gen

[![CircleCI](https://circleci.com/gh/harveyormston/osc_gen.svg?style=shield)](https://circleci.com/gh/harveyormston/osc_gen)
[![PyPI version](https://badge.fury.io/py/osc-gen.svg)](https://badge.fury.io/py/osc-gen)

# Table of Contents

<!-- vim-markdown-toc GFM -->

* [About](#about)
* [Installation](#installation)
* [Development](#development)
* [Getting Started](#getting-started)
  * [Morphing Between Waveforms](#morphing-between-waveforms)
  * [Generating Your Own Waves](#generating-your-own-waves)
  * [Pulse-width Modulation](#pulse-width-modulation)
  * [Other Wave Shapes](#other-wave-shapes)
  * [Processing Waveforms](#processing-waveforms)
* [Using Samples](#using-samples)

<!-- vim-markdown-toc -->

# About

osc_gen is a Python library for creating and managing oscillator wavetables.

Functionality includes:

* Generating common waveforms (sine, saw, square, etc.)
* Oscillator effects (waveshaping, distortion, downsampling, etc.)
* Resynthesising or slicing audio from wav files or other sources
* Saving wavetables to a wav file for use in samplers
* Saving wavetables in .h2p format for use in the u-he Zebra2 synthesiser


# Installation

osc_gen is [available on PyPI](https://pypi.org/project/osc-gen/#description) and can be installed using pip:

```sh
$ pip install osc_gen
```

# Development

Development requirements can be installed using the provided `requirements.txt`:

```sh
$ pip install -r requirements.txt
```

# Getting Started

These examples show how to:

- Use the sig module to generate oscillator shapes.
- Use the wavetable module to create a 16 slot wavetable.
- Store a wavetable as a zebra oscillator file.
- Store a wavetable as a wav file.

```python
import wavetable
import sig
import dsp


# Create a signal generator.
sg = sig.SigGen()

# Create a wave table with 16 slots to store the waves.
wt = wavetable.WaveTable(16)

# Generate a sine wave using our signal generator.
m = sg.sin()

# Put the sine wave into our wave table.
# As we're only adding one wave to the wave table, only the first slot of the
# resulting wavetable will contain the sine wave. The remaining slots will
# be empty, because we haven't added anything to those yet.
wt.waves = [m]

# Write the resulting oscillator to a Zebra2 h2p file.
wt.to_h2p('osc_gen_sine.h2p')

# Write the resulting oscillator to a wav file.
wt.to_wav('osc_gen_sine.wav')

# To fill all 16 slots, repeat the sine wave 16 times in the wavetable.
wt.waves = [m] * 16
wt.to_wav('osc_gen_saw16.wav')
```

## Morphing Between Waveforms

We can use up all 16 slots in the wavetable, even with fewer than 16
starting waveforms, if we use morph() to morph from one waveform to the
other and fill in the in-between slots.

```python
# Morph from sine to triangle over 16 slots.
wt.waves = sig.morph((sg.sin(), sg.tri()), 16)
wt.to_wav('osc_gen_sin_tri.wav')

# Morph from sine to triangle over 5 slots.
wt.waves = sig.morph((sg.sin(), sg.tri()), 5)
wt.to_wav('osc_gen_sin_tri5.wav')

# Morph between sine, triangle, saw and square over 16 slots:
wt.waves = sig.morph((sg.sin(), sg.tri(), sg.saw(), sg.sqr()), 16)
wt.to_wav('osc_gen_sin_tri_saw_sqr.wav')

# Morph between two wavetables using the morph_with() method
wt_1 = WaveTable(16, waves=[sg.sin()] * 16)
wt_2 = WaveTable(16, waves=[sg.pls(i / 16) for i in range(16)])
wt_m = wt_1.morph_with(wt_2)
```

## Generating Your Own Waves

You can create a custom signal yourself to use as an oscillator.
In this example, one slot is filled with random data, but you could
use any data you've generated or, say, read in from a wav file using the
wavfile module.

```python
# Generate some random data.
from random import uniform
random_wave = (uniform(-1, 1) for _ in range(128))

# Write to file.
wt.waves = [sg.arb(random_wave)]
wt.to_wav('osc_gen_random.wav')
```

The `arb()` method automatically normalises, scales and resamples any
data you throw at it to fit it into the `SigGen`'s parameters, so the input can
be any amplitude and any number of samples.

## Pulse-width Modulation

SigGen has a pulse wave generator too. Let's use that to make a pwm wavetable.


Pulse widths are between 0 and 1 (0 to 100%).
0 and 1 are silent as the pulse is a flat line.

So, we want to have 16 different, equally spaced pulse widths, increasing in
duration, but also avoid any silence:

```python
pulse_widths = (i / 17. for i in range(1, 17))
wt.waves = [sg.pls(p) for p in pulse_widths]
wt.to_wav('osc_gen_pwm.wav')
```

## Other Wave Shapes

Other wave shapes are supported by SigGen, including:

* Noise
* Exponential Saw
* Exponential Sin
* Square Saw
* Shark Fin

```python
wt.waves = [sgen.noise(0, 0.01),
            sgen.exp_saw(),
            sgen.exp_sin(3),
            sgen.sqr_saw(0.75),
            sgen.sharkfin(0.04)]

wt.to_wav('osc_gen_other.wav')
```

![](https://raw.githubusercontent.com/harveyormston/osc_gen/main/examples/images/fin_exp_sqrsaw.png)

## Processing Waveforms

The dsp module can be used to process waves in various ways.

These examples use the plotting functions in the visualize module to plot the resulting processed wavetable.

```python
# clip() applies hard clipping
waves = [dsp.clip(sgen.sin(), x / 10) for x in range(16)]
wtab = wavetable.WaveTable(16, waves)
visualize.plot_wavetable(wtab)
```

![](https://raw.githubusercontent.com/harveyormston/osc_gen/main/examples/images/clip.png)

```python
# tube() applies tube saturation
waves = [dsp.tube(sgen.sin(), x) for x in range(1, 17)]
wtab = wavetable.WaveTable(16, waves)
visualize.plot_wavetable(wtab)
```

![](https://raw.githubusercontent.com/harveyormston/osc_gen/main/examples/images/tube.png)

```python
# fold() applies wave folding
waves = [dsp.fold(sgen.sin(), x / 10) for x in range(16)]
wtab = wavetable.WaveTable(16, waves)
visualize.plot_wavetable(wtab)
```

![](https://raw.githubusercontent.com/harveyormston/osc_gen/main/examples/images/fold.png)

```python
# shape applies polynomial wave-shaping
waves = [dsp.shape(sgen.sin(), 1.0, power=x) for x in range(1, 17)]
wtab = wavetable.WaveTable(16, waves)
visualize.plot_wavetable(wtab)
```

![](https://raw.githubusercontent.com/harveyormston/osc_gen/main/examples/images/shape.png)

```python
# slew() smooths or sharpens the gradient of a waveform
from numpy import linspace
waves = [dsp.slew(sgen.pls(x), x) for x in linspace(-0.5, 0.5, 16)]
wtab = wavetable.WaveTable(16, waves)
visualize.plot_wavetable(wtab)
```

![](https://raw.githubusercontent.com/harveyormston/osc_gen/main/examples/images/slew.png)

```python
# downsample() lowers the sample-rate for aliasing effects
waves = [dsp.downsample(sgen.sin(), x + 1) for x in range(8)]
wtab = wavetable.WaveTable(8, waves)
visualize.plot_wavetable(wtab)
```

![](https://raw.githubusercontent.com/harveyormston/osc_gen/main/examples/images/downsample.png)

```python
# quantize() lowers the bit-depth for bit-crushing effects
waves = [dsp.quantize(sgen.sin(), (4 - x) * 2) for x in range(4)]
wtab = wavetable.WaveTable(4, waves)
visualize.plot_wavetable(wtab)
```

![](https://raw.githubusercontent.com/harveyormston/osc_gen/main/examples/images/quantize.png)


# Using Samples

Samples can be used to populate a wavetable using one of two methods: slicing
and resynthesis. Both methods involve finding the fundamental frequency of the
audio in the wav file and generating wavetable slots containing multiple
single cycles of the waveform.

Slicing is relatively simple: the input audio is sliced at regular intervals
to extract individual cycles of the tone.

Resynthesis, on the other hand, uses Fourier analysis to reconstruct cycles of
the waveform based on the harmonic series observed in the input.

Slicing gives results which will match the original audio exactly, but small
errors may result in unwanted harmonic content. Resynthesis gives more
predictable harmonic content but may discard information from the original
audio.

```python
# resynthesize
wt = wavetable.WaveTable(16, wave_len=128).from_wav('mywavefile.wav', resynthesize=True)

# slice
wt = wavetable.WaveTable(16, wave_len=128).from_wav('mywavefile.wav', resynthesize=False)
```

To extract a specific number of samples in each cycle, there are two options:

1. Set the `wave_len` property in the `WaveTable` instance e.g.:

```python
wt = wavetable.WaveTable(16, wave_len=2048).from_wav('mywavefile.wav', resynthesize=True)

```

2. create a `SigGen` object and pass that into `from_wav()` e.g.:


```python
sg = SigGen(num_points=2048)
wt = wavetable.WaveTable(16).from_wav('mywavefile.wav', sig_gen=sg, resynthesize=True)
```
