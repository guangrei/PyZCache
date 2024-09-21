#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md')) as f:
    long_description = f.read()

setup(
    name='zcache',
    version='v1.0.5',
    packages=['zcache',],
    license='MIT',
    author="guangrei",
    author_email="myawn@pm.me",
    description="Key Value Database/Cache with abstract storage and plugins",
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords="cache key value file json",
    url="https://github.com/guangrei/zcache",
)
