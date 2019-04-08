#!/usr/bin/env python3

import os.path
from setuptools import setup, find_packages

from hideezlib import __version__ as VERSION


CWD = os.path.dirname(os.path.realpath(__file__))


def read(name):
    filename = os.path.join(CWD, name)
    with open(filename, 'r') as f:
        return f.read()


with open('requirements.txt') as f:
    install_requires = f.read().splitlines()


setup(
    name='hideez',
    version=VERSION,
    author='Hideez Group Inc',
    author_email='info@hideez.com',
    license='LGPLv3',
    description='Python library for communicating with Hideez Hardware Wallet',
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    url='https://github.com/HideezGroup/python-hideez',
    packages=find_packages(),
    package_data={
        'hideezlib': ['coins.json'],
    },
    scripts=['hideezctl'],
    install_requires=install_requires,
    extras_require={
        ':python_version < "3.5"': ['typing>=3.0.0'],
    },
    python_requires='>=3.3',
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
        'Operating System :: POSIX :: Linux',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: MacOS :: MacOS X',
        'Programming Language :: Python :: 3 :: Only',
    ],
)
