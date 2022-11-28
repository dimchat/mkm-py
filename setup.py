#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Ming-Ke-Ming
    ~~~~~~~~~~~~

    Common Identity Module for decentralized user identity authentication
"""

import io

from setuptools import setup, find_packages

__version__ = '0.12.3'
__author__ = 'Albert Moky'
__contact__ = 'albert.moky@gmail.com'

with io.open('README.md', 'r', encoding='utf-8') as fh:
    readme = fh.read()

setup(
    name='mkm',
    version=__version__,
    url='https://github.com/dimchat/mkm-py',
    license='MIT',
    author=__author__,
    author_email=__contact__,
    description='A common identity module',
    long_description=readme,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    install_requires=[
    ]
)
