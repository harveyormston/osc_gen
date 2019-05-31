""" unit tests for sig module """

from __future__ import division
import pytest
import numpy as np

from osc_gen import sig


@pytest.fixture(scope="module")
def fxsg():
    """ SigGen fixture """
    return sig.SigGen()


def test_saw_two(fxsg):  # pylint: disable=redefined-outer-name
    """ test saw wave length two """

    fxsg.num_points = 2
    saw = fxsg.saw()
    assert saw[0] == -1
    assert saw[1] == 1


def test_saw_three(fxsg):  # pylint: disable=redefined-outer-name
    """ test saw wave length three """

    fxsg.num_points = 3
    saw = fxsg.saw()
    assert saw[0] == -1
    assert saw[1] == 0
    assert saw[2] == 1


def test_tri_long(fxsg):  # pylint: disable=redefined-outer-name
    """ test tri wave """

    fxsg.num_points = 1 << 16
    tri = fxsg.tri()
    assert tri[0] == -1
    assert tri[fxsg.num_points // 2] == 1
    assert abs(tri[-1] + 1) < 0.01


def test_sqr_three(fxsg):  # pylint: disable=redefined-outer-name
    """ test sqr wave length three """

    fxsg.num_points = 3
    sqr = fxsg.sqr()
    assert sqr[0] == -1
    assert sqr[1] == 1
    assert sqr[2] == 1


def test_sin_long(fxsg):  # pylint: disable=redefined-outer-name
    """ test sin wave """

    fxsg.num_points = 1 << 16
    sin = fxsg.sin()
    assert sin[0] == -1
    assert sin[fxsg.num_points // 2] == 1
    assert abs(sin[-1] + 1) < 0.01


def test_pls_width(fxsg):  # pylint: disable=redefined-outer-name
    """ test pls wave width """

    fxsg.num_points = 10
    for w in range(10):
        width = (w / 5) - 1
        pls = fxsg.pls(width)
        for i, v in enumerate(pls):
            if i >= w:
                assert v == 1
            else:
                assert v == -1


def test_arb(fxsg):  # pylint: disable=redefined-outer-name
    """ test arb wave """

    fxsg.num_points = 10
    saw = fxsg.saw()
    fxsg.num_points = 19
    arb = fxsg.arb(saw)
    assert np.allclose(arb[::2], saw)


def test_morph_same(fxsg):  # pylint: disable=redefined-outer-name
    """ test morphing same signal """

    fxsg.num_points = 10
    saw = fxsg.saw()
    inp = [saw for _ in range(2)]
    exp = [saw for _ in range(3)]
    assert all(all(sig.morph(inp, 3)[i] == exp[i]) for i in range(3))


def test_morph(fxsg):  # pylint: disable=redefined-outer-name
    """ test morph """

    fxsg.num_points = 3
    saw = fxsg.saw()
    tri = fxsg.tri()
    inp = [saw, tri]
    exp = [saw, (saw + tri) / 2, tri]
    assert all(all(sig.morph(inp, 3)[i] == exp[i]) for i in range(3))
