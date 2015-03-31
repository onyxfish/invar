#!/usr/bin/env python

from distutils.core import setup

setup(
    name = "invar",
    version = "0.1.1",
    description = "Scripts for generating images from Mapnik configuration and storing them on S3.",
    author='Christopher Groskopf',
    author_email='staringmonkey@gmail.com',
    url='http://invar.readthedocs.org/',
    license = "MIT",
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Scientific/Engineering :: GIS',
        'Topic :: Utilities'
    ],
    packages = [
        'invar',
    ],
    scripts = [
        'ivtile',
        'ivframe',
        'ivs3'
    ],
    install_requires = [
        'argparse>=1.3.0',
        'eventlet>=0.17.1',
        'boto>=2.36.0'
    ]
)
