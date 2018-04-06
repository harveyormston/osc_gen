#!/usr/bin/env python
""" Setup osc_gen """

from setuptools import setup

LONG_DESCRIPTION = (
    """osc_gen is a Python library for creating and managing oscillator wavetables.

Functionality includes:

* Generating common waveforms (sine, saw, square, etc.)
* Oscillator effects (waveshaping, distortion, downsampling, etc.)
* Resynthesising or slicing audio from wav files or other sources
* Saving wavetables to a wav file for use in samplers
* Saving wavetables in .h2p format for use in the u-he Zebra2 synthesiser"""
)

setup(
    name='osc_gen',
    version='0.1.0',
    description='Generate oscilator wavetoables',
    long_descriptions=LONG_DESCRIPTION,
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
    python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, <4'
)
