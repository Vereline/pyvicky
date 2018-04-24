#!/usr/bin/env python
import sys

if sys.version_info < (3, 5):
    raise ImportError("some things require python >= 3.5, test this for correct version")

import io
import os
from pip.req import parse_requirements
from pip.download import PipSession
from setuptools import setup, find_packages

install_requirements = parse_requirements('requirements-freeze.txt', session=PipSession())
requirements = [str(ir.req) for ir in install_requirements]


def read(filename):
    return io.open(os.path.join(os.path.dirname(__file__), filename), encoding='utf-8').read()


setup(
    name='pyvicky',
    version='0.1',
    description='Simple text editor for python projects',
    long_description=read('Readme.md'),
    author='Viktoryia Stanko',
    author_email='vstanko1998@inbox.ru',
    packages=find_packages(),
    install_requires=requirements
)
