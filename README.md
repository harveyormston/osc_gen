# osc_gen
Python modules to create and manage oscillator wavetables.

# Examples

These examples show how to:

- Use the sig module to generate oscillator shapes.
- Use the zwave module to create an (up to) 16 slot wavetable.
- Use the zosc module to store wavetables as a zebra oscillator file.


## Example Setup

Initial setup of the objects we'll need in order to create and store oscillators

        import zwave
        import zosc
        import sig
        import dsp

Create a signal generator:

        sg = sig.SigGen()

Create a wave table to store the waves:

        wt = zwave.WaveTable()

Create a zebra oscillator to store the final wave table:

        zo = zosc.Osc(wt)

## Generate and Save a Simple Saw Wave

Generate a saw using our signal generator and store it in a new Wave object:

        m = zwave.Wave(sg.saw())

Put the saw wave into our wave table:

        wt.set_waves((m,))

As we're only adding one wave to the wave table, only the first slot of the
resulting oscillator in zebra will contain the saw. The remaining slots will
be empty, because we haven't added anything to those yet.

Write the resulting oscillator to a file:

        zo.write_to_file('osc_gen_saw.h2p')

You could fill all 16 slots with the same saw, by repeating it 16 times when
calling `set_waves()` on the wave table, if you wanted. However, we do need to
generate the saw again. sig tends to return Python generators
where possible, which means they can become empty once they've been used
once, unless you store them as a list yourself.

        m = zwave.Wave(sg.saw())

Repeat the saw 16 times in the wavetable:

        wt.set_waves((m for _ in range(16)))

Write the resulting oscillator to a file:

        zo.write_to_file('osc_gen_saw16.h2p')

## Morphing Between Two Waveforms

We can use up all 16 slots in the zebra oscillator, even with fewer than 16
starting waveforms, if we use morph() to morph from one waveform to the
other, to fill in the in-between slots.


Morph from sine to triangle over 16 slots:

        ws = (zwave.Wave(s) for s in sig.morph((sg.sin(), sg.tri()), 16))

Set the wavetable and store it as an oscillator:

        wt.set_waves(ws)
        zo.write_to_file('osc_gen_sin_tri.h2p')

Of course, we don't have to use all 16 slots. We could use only the first 5,
for example.


But first, we should clear the wavetable, so that the slots above 5 don't
end up containing any older data:

        wt.clear()

Morph from sine to triangle over 5 slots:

        ws = (zwave.Wave(s) for s in sig.morph((sg.sin(), sg.tri()), 5))

Set the wavetable and store it as an oscillator:

        wt.set_waves(ws)
        zo.write_to_file('osc_gen_sin_tri5.h2p')

## Morphing Between Many Waveforms

We can morph between any number of waveforms, with a couple of conditions:

- We can't morph between more than 16 waves, because the zebra wavetable only
contains 16 slots.

- We can't morph a number of waves over smaller number of slots. e.g. we
can't morph 5 waves into 3 slots.


If you want to morph to a smaller number of slots, you'd need to use
morph to compress your 5 waves into 3 'in-between' waves first, and
the decision over which waves to keep and which to compress isn't a
decision morph should make for you.


Morph between sine, triangle, saw and square over 16 slots:

        ws = (zwave.Wave(s) for s in
              sig.morph((sg.sin(), sg.tri(), sg.saw(), sg.sqr()), 16))

Set the wavetable and store it as an oscillator:

        wt.set_waves(ws)
        zo.write_to_file('osc_gen_sin_tri_saw_sqr.h2p')


## Generating Your Own Waves

You can create a custom signal yourself to use as an oscillator.
In this example, one slot is filled with random data, but you could
use any data you've generated or, say, read in from a wav file using the
wavfile module.

Generate some random data:

        from random import uniform
        random_wave = (uniform(-1, 1) for _ in range(128))

The custom signal generator function automatically normaises and scales any
data you throw at it to the right ranges, which is useful.

        r = zwave.Wave(sg.custom(random_wave))

Clear the wavetable, so that the slots above 1 don't contain any older data:

        wt.clear()

Set the wavetable and store it as an oscillator:

        wt.set_waves((r,))
        f = os.path.join(home, osc_path, 'osc_gen_random.h2p')
        zo.write_to_file(f)

## Pulse-width Modulation

SigGen has a pulse wave generator too. Let's use that to make a pwm wavetable.


Pulse widths are between 0 and 1 (0 to 100%).
0 and 1 are silent as the pulse is a flat line.


So, we want to have 16 different, equally spaced pulse widths, increasing in
duration, but also avoid any silence:

        pws = (i / 17. for i in range(1, 17))

Generate the 16 pulse waves:

        ws = (zwave.Wave(sg.pls(p)) for p in pws)

Set the wavetable and store it as an oscillator:

        wt.set_waves(ws)
        zo.write_to_file('osc_gen_pwm.h2p')

## Processing Waveforms

The dsp module can be used to process waves in various ways.

Let's try downsampling a sine:

        ds = dsp.downsample(sg.sin(), 16)

That downsampled sine from probably sounds pretty edgy.

Let's try that again with some slew this time, to smooth it out a bit:

        sw = dsp.slew(dsp.downsample(sg.sin(), 16), 0.8)

Generate a triangle wave and quantise (bit crush) it:

        qt = dsp.quantise(sg.tri(), 3)

Applying inverse slew, or overshoot, to a square wave:

        ss = dsp.slew(sg.sqr(), 0.8, inv=True)

Overshoot might make the wave quieter, so let's normalise it:

        dsp.normalise(ss)

Morph between the waves over 16 slots:

        ws = (zwave.Wave(s) for s in sig.morph((ds, sw, qt, ss), 16))

Set the wavetable and store it as an oscillator:

    wt.set_waves(ws)
    zo.write_to_file('osc_gen_dsp.h2p')
