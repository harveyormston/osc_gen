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

from __future__ import division
import pytest
import numpy as np

from osc_gen import sig


@pytest.fixture(scope="module")
def fxsg():
    """ SigGen fixture """
    return sig.SigGen()


def test_saw(fxsg):  # pylint: disable=redefined-outer-name
    """ test saw wave """

    fxsg.num_points = 1 << 16

    saw = fxsg.saw()
    pre_mid = saw[-1 + fxsg.num_points // 2]
    mid = saw[fxsg.num_points // 2]

    assert saw[0] == 0
    assert np.isclose(pre_mid, 1, rtol=0.01)
    assert np.isclose(mid, -1, rtol=0.01)
    assert saw[-1] == 0


def test_tri(fxsg):  # pylint: disable=redefined-outer-name
    """ test tri wave """

    fxsg.num_points = 1 << 16

    tri = fxsg.tri()
    quarter = tri[fxsg.num_points // 4]
    half = tri[fxsg.num_points // 2]
    three_quarters = tri[3 * fxsg.num_points // 4]

    assert tri[0] < 0.01
    assert np.isclose(quarter, 1, rtol=0.01)
    assert np.isclose(half, 0, atol=np.inf, rtol=0.01)
    assert np.isclose(three_quarters, -1, rtol=0.01)
    assert np.isclose(tri[-1], 0, atol=np.inf, rtol=0.01)


def test_sqr(fxsg):  # pylint: disable=redefined-outer-name
    """ test sqr wave """

    fxsg.num_points = 1 << 16

    sqr = fxsg.sqr()
    pre_mid = sqr[fxsg.num_points // 2 - 1]
    mid = sqr[fxsg.num_points // 2]

    assert (sqr[0] - 1) < 0.01
    assert np.isclose(pre_mid, 1, rtol=0.01)
    assert np.isclose(mid, -1, rtol=0.01)
    assert sqr[-1] == 1


def test_sin(fxsg):  # pylint: disable=redefined-outer-name
    """ test sin wave """

    fxsg.num_points = 1 << 16
    sin = fxsg.sin()

    start = sin[0]
    quarter = sin[fxsg.num_points // 4]
    half = sin[fxsg.num_points // 2]
    three_quarters = sin[3 * fxsg.num_points // 4]
    end = sin[-1]

    assert start == 0
    assert np.isclose(quarter, 1, rtol=np.inf, atol=0.01)
    assert np.isclose(half, 0, atol=0.01)
    assert np.isclose(three_quarters, -1, rtol=np.inf, atol=0.01)
    assert np.isclose(end, 0, atol=0.01)


def test_pls_width(fxsg):  # pylint: disable=redefined-outer-name
    """ test pls wave width """

    fxsg.num_points = 11
    assert np.all(fxsg.pls(-1) == np.ones(fxsg.num_points))
    assert np.all(fxsg.pls(0) == fxsg.sqr())
    width_one_exp = -1 * np.ones(fxsg.num_points)
    width_one_exp[fxsg.num_points // 2] = 1
    assert np.all(fxsg.pls(1) == width_one_exp)


def test_arb(fxsg):  # pylint: disable=redefined-outer-name
    """ test arb wave """

    fxsg.num_points = 10
    sin = fxsg.sin()
    fxsg.num_points = 20
    arb = fxsg.arb(sin)
    assert np.allclose(arb[::2], sin, rtol=np.inf, atol=0.001)


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
