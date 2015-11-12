""" Extend wavfile to read data as normalised float """

import soundfile as sf
import numpy as np


def read(filename):
    """ Read wav file and convert to normalised float """

    data, _ = sf.read(filename)
    # take only the first channel of the audio
    if len(data.shape) > 1:
        data = np.swapaxes(data, 0, 1)[0]
    # center on 0
    data = data.astype(float)
    data -= np.mean(data)
    # normalise to +/- 1.0
    dm = max(abs(data))
    return data / dm


def write(data, filename, samplerate):
    """ Write wav file """

    sf.write(data, filename, samplerate=samplerate)
