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

import os
import sys

from setuptools import setup
from setuptools.command.install import install

VERSION = "1.3.0"

LONG_DESCRIPTION = (
    """osc_gen is a Python library for creating and managing oscillator wavetables.

Functionality includes:

* Generating common waveforms (sine, saw, square, etc.)
* Oscillator effects (waveshaping, distortion, downsampling, etc.)
* Resynthesising or slicing audio from wav files or other sources
* Saving wavetables to a wav file for use in samplers
* Saving wavetables in .h2p format for use in the u-he Zebra2 synthesiser"""
)


class VerifyVersionCommand(install):
    """ Custom command to verify that the git tag matches our version """
    description = 'verify that the git tag matches our version'

    def run(self):
        tag = os.getenv('CIRCLE_TAG')

        if tag != VERSION:
            info = "Git tag: {0} does not match the version of this app: {1}".format(
                tag, VERSION
            )
            sys.exit(info)


setup(
    name='osc_gen',
    version=VERSION,
    description='Generate oscilator wavetoables',
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/x-rst',
    author='Harvey Ormston',
    author_email='harveyormston@me.com',
    url='https://github.com/harveyormston/osc_gen',
    license='GPL3',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Multimedia :: Sound/Audio',
        'Topic :: Multimedia :: Sound/Audio :: Analysis',
        'Topic :: Multimedia :: Sound/Audio :: Sound Synthesis',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6'],
    keywords='audio dsp synthsis',
    project_urls={
        'Source': 'https://github.com/harveyormston/osc_gen',
    },
    packages=['osc_gen'],
    install_requires=[
        "numpy>=1.11.3",
        "scipy>=0.18.1",
        "pysoundfile"],
    python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, <4',
    cmdclass={'verify': VerifyVersionCommand}
)
