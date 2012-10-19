#!/usr/bin/env python

from distutils.core import setup

setup(
    name = "invar",
    version = "0.0.16",
    description = "Scripts for generating tiles from Mapnik configuration and storing them on S3.",
    author='Christopher Groskopf',
    author_email='staringmonkey@gmail.com',
    url='http://blog.apps.chicagotribune.com/',
    license = "MIT",
    packages = [
        'invar',
    ],
    scripts = [
        'ivtile',
        'ivframe',
        'ivs3'
    ],
    install_requires = [
        'argparse',
        'eventlet',
        'boto'
    ]
)

