""" Extend wavfile to read data as normalised float """

try:
    import soundfile as sf
    HAS_SOUNDFILE = True
except ImportError:
    HAS_SOUNDFILE = False

import array
import wave
import struct
import numpy as np


def _float_to_ibytes(floats):
    """ Convert a sequence of floats to 16-bit bytes """

    a = np.array(floats)
    a = (a * 32768).astype('int')
    np.clip(a, -32768, 32767, out=a)
    return array.array('i', a).tostring()


def _ibytes_to_float(bytes):

    n = len(bytes)
    n = int(n / 4)
    a = struct.unpack('<{0}i'.format(n), bytes)
    a = np.array(a).astype(float)
    a /= 32768.
    return a.astype(float)


def _read_using_wave(filename):

    w = wave.open(filename, 'r')
    if w.getnchannels() != 1:
        raise ValueError("only mono supported")
    if w.getsampwidth() != 2:
        raise ValueError("only 16 bit supported")
    n = w.getnframes()
    return _ibytes_to_float(w.readframes(n))


def read(filename):
    """ Read wav file and convert to normalised float """

    if HAS_SOUNDFILE:
        data, _ = sf.read(filename)
        # take only the first channel of the audio
        if len(data.shape) > 1:
            data = np.swapaxes(data, 0, 1)[0]
    else:
        data = _read_using_wave(filename)

    # center on 0
    data = data.astype(float)
    data -= np.mean(data)
    # normalise to +/- 1.0
    dm = max(abs(data))
    return data / dm


def write(data, filename, samplerate=44100):
    """ Write wav file """

    with wave.open(filename, 'w') as w:
        w.setframerate(samplerate)
        w.setnchannels(1)
        w.setsampwidth(2)
        w.writeframes(_float_to_ibytes(data))


def write_wavetable(wavetable, filename, samplerate=44100):

    with wave.open(filename, 'w') as w:
        w.setframerate(samplerate)
        w.setnchannels(1)
        w.setsampwidth(2)
        for wv in wavetable.get_waves():
            w.writeframes(_float_to_ibytes(wv.values))
