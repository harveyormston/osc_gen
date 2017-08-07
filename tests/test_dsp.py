""" unit tests for dsp module """

import numpy as np

from osc_gen import dsp
from osc_gen import sig


def test_normalize():
    """ test normalize """
    a = np.array([0.0, 1.0, 2.0])
    e = np.array([-1.0, 0.0, 1.0])
    assert np.all(dsp.normalize(a) == e)


def test_normalize_zero():
    """ test normalize with amplitude zero """
    a = np.array([0.0, 0.0])
    assert np.amax(dsp.normalize(a)) == 0.0


def test_normalize_neg():
    """ test normalize with negative input """
    a = np.array([-1.0, 0.0])
    assert np.amax(dsp.normalize(a)) == 1.0
    assert np.amin(dsp.normalize(a)) == -1.0


def test_normalize_dc():
    """ test normalize with negative input """
    a = np.array([0.123, 0.123])
    e = np.array([0.0, 0.0])
    assert np.all(dsp.normalize(a) == e)


def test_clip():
    """ test clip """
    a = np.array([0.0, 1.0, 2.0])
    o = dsp.clip(a, 0)
    e = np.array([-1.0, 1.0, 1.0])
    assert np.allclose(o, e)


def test_clip_amount():
    """ test clip amount """
    a = np.array([-0.1, 0.5, 5.0])
    o = dsp.clip(a, 1)
    e = np.array([-1.0, 1.0, 1.0])
    assert np.allclose(o, e)


def test_clip_bias():
    """ test clip bias """
    a = np.array([-1.0, 0.5, 5.0])
    o = dsp.clip(a, 0, bias=0.5)
    e = np.array([-1.0, 1.0, 1.0])
    assert np.allclose(o, e)


def test_tube():
    """ test tube """
    a = np.array([-1.0, -0.1, 0.1, 1.0])
    o = dsp.tube(a, 0)
    e = np.array([-1.0, -0.1081076, 0.1081076, 1.0])
    assert np.allclose(o, e)


def test_tube_bypass():
    """ test tube bypass """
    a = np.array([-1.0, 0.0, 1.0])
    o = dsp.tube(a, 0)
    e = np.array([-1.0, 0.0, 1.0])
    assert np.allclose(o, e)


def test_fold():
    """ test fold to """
    a = np.array([-0.5, -0.7, 0.0, 0.6, 0.5])
    o = dsp.fold(a, 1)
    e = np.array([-1.0, -0.6, 0.0, 0.8, 1.0])
    assert np.allclose(o, e)


def test_fold_to_zero():
    """ test fold to zero """
    a = np.array([-1.0, 0.0, 1.0])
    o = dsp.fold(a, 1)
    e = np.array([0.0, 0.0, 0.0])
    assert np.allclose(o, e)


def test_shape():
    """ test shape """
    a = np.array([-1.0, -0.5, 0.0, 0.5, 1.0])
    o = dsp.shape(a)
    e = np.array([-1.0, -0.125, 0.0, 0.125, 1.0])
    assert np.allclose(o, e)


def test_shape_two():
    """ test shape power two """
    a = np.array([-1.0, -0.5, 0.0, 0.5, 1.0])
    o = dsp.shape(a, power=2)
    e = np.array([-1.0, -0.25, 0.0, 0.25, 1.0])
    assert np.allclose(o, e)


def test_shape_bias():
    """ test shape bias """
    a = np.array([-1.0, -0.5, 0.0, 0.5, 1.0])
    o = dsp.shape(a, bias=0.5)
    e = np.array([-0.625, -0.5, -0.375, 0.5, 2.875])
    dsp.normalize(e)
    assert np.allclose(o, e)


def test_slew():
    """ test slew """
    a = np.ones(100)
    a[:50] *= -1
    o = dsp.slew(a, 0.1)
    assert np.all(o[:8] == -o[50:58])
    assert o[0] > o[1]


def test_downsample():
    """ test downsample """
    a = np.linspace(-1, 1, 10)
    e = np.empty_like(a)
    for i in range(10):
        if i % 2 == 0:
            e[i] = a[i]
        else:
            e[i] = a[i - 1]
    dsp.normalize(e)
    dsp.downsample(a, 2)
    assert np.all(a == e)


def test_quantize():
    """ test quantize """
    a = np.array([-1.0, -0.5, 0.0, 0.5, 1.0])
    dsp.quantize(a, 2)
    assert a[1] == -2 / 3
    assert a[-2] == 2 / 3


def test_fundamental():
    """ test fundamental """
    a = np.array([-1.0, 0.0, 1.0, 0.0])
    f = dsp.fundamental(a, 2)
    assert f == 0.5


def test_harmonic_series():
    """ test harmonic_series """
    n = 64 * 501
    a = np.sin(16 * np.pi * np.linspace(0, 1, n))
    a += (0.5 * np.sin(32 * np.pi * np.linspace(0, 1, n)))
    a += (0.25 * np.sin(48 * np.pi * np.linspace(0, 1, n)))
    h = np.absolute(dsp.harmonic_series(a))
    e = np.zeros_like(h)
    e[0] = 1.
    e[1] = 0.5
    e[2] = 0.25
    assert np.allclose(h, e, rtol=5e-3, atol=5e-3)


def test_slice_cycles():
    """ test slice_cycles """
    a = np.array([0.0, 1.0, 0.0, -1.0])
    e = a
    a = np.tile(a, 501)
    o = dsp.slice_cycles(a, 2, 2)
    assert np.all(o[1] == e)


def test_resynthesize():
    """ test resynthesize """
    a = np.array([-1.0, 1.0, 1.0, -1.0])
    e = a
    a = np.tile(a, 1024)
    s = sig.SigGen()
    s.num_points = 4
    o = dsp.resynthesize(a, s)
    assert np.allclose(o, e)
