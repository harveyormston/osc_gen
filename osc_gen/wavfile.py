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

try:
    import soundfile as sf
    HAS_SOUNDFILE = True
except ImportError:
    HAS_SOUNDFILE = False

import wave
import struct
import numpy as np


def _float_to_ibytes(vals):
    """ Convert a sequence of vals to 16-bit bytes """

    num = len(vals)
    afloats = np.array(vals)
    afloats = (afloats * 32768).astype('int')
    np.clip(afloats, -32768, 32767, out=afloats)
    return struct.pack('<{0}h'.format(num), *(aval for aval in afloats))


def _ibytes_to_float(vals):

    num = len(vals)
    num = int(num / 4)
    afloats = struct.unpack('<{0}h'.format(num), vals)
    afloats = np.array(afloats).astype(float)
    afloats /= 32768.0
    return afloats


def _read_using_wave(filename):

    wave_file = wave.open(filename, 'r')

    if wave_file.getnchannels() != 1:
        raise ValueError("only mono supported")

    if wave_file.getsampwidth() != 2:
        raise ValueError("only 16 bit supported")

    num_frames = wave_file.getnframes()
    data = _ibytes_to_float(wave_file.readframes(num_frames))
    fs = wave_file.getframerate()

    return data, fs


def read(filename, with_sample_rate=False):
    """ Read wav file and convert to normalized float """

    if HAS_SOUNDFILE:
        data, fs = sf.read(filename)
        # take only the first channel of the audio
        if len(data.shape) > 1:
            data = np.swapaxes(data, 0, 1)[0]
    else:
        data, fs = _read_using_wave(filename)

    # center on 0
    data = data.astype(float)
    data -= np.mean(data)

    # normalize to +/- 1.0
    data_max = max(abs(data))
    data /= data_max

    if with_sample_rate:
        return data, fs

    return data


def write(data, filename, samplerate=44100):
    """ Write wav file """

    wave_file = wave.open(filename, 'w')
    wave_file.setframerate(samplerate)
    wave_file.setnchannels(1)
    wave_file.setsampwidth(2)
    wave_file.writeframes(_float_to_ibytes(data))
    wave_file.close()


def write_wavetable(wavetable, filename, samplerate=44100):
    """ Write wavetable to file """

    wave_file = wave.open(filename, 'w')
    wave_file.setframerate(samplerate)
    wave_file.setnchannels(1)
    wave_file.setsampwidth(2)
    for wt_wave in wavetable.get_waves():
        wave_file.writeframes(_float_to_ibytes(wt_wave))
    wave_file.close()
