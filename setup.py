#!/usr/bin/env python
# -*- coding: utf-8 -*-

# pyVows testing engine
# https://github.com/heynemann/pyvows

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 Bernardo Heynemann heynemann@gmail.com

# stdlib
import sys
from textwrap import dedent
# external
from setuptools import setup, find_packages
# local
from pyvows import version


_test_requires = [
    'argparse>=1.4.0',
    'colorama>=0.3.7',
    'coverage>=4.1.1'

]
_install_requires = [
    'gevent>=1.2.2',
    'preggy>=1.3.0',
]
if sys.version_info < (2, 7):
    _install_requires.append('argparse >= 1.1')


setup(
    ### OVERVIEW
    name='pyVows',
    description='pyVows is a BDD test engine based on Vows.js <http://vowsjs.org>.',
    long_description_content_type='text/x-rst',
    long_description=dedent(
        '''pyVows is a test engine based on Vows.js. It features topic-based testing,
        (*fast*) parallel running of tests, code coverage reports, test profiling, and
        more:

        http://pyvows.org

        '''),


    ### URLs
    url='http://pyvows.org',


    ### TECHNICAL INFO
    version=version.to_str(),
    install_requires=_install_requires,
    extras_require={
        'tests': _test_requires,
    },
    packages=find_packages(exclude=['tests', 'tests.*']),
    package_dir={'pyvows': 'pyvows'},
    entry_points={
        'console_scripts': [
            'pyvows = pyvows.cli:main'
        ],
        'distutils.commands': [
            ' vows = pyvows.commands:VowsCommand',
        ],
    },


    ### PEOPLE & LICENSE
    author='Bernardo Heynemann',
    author_email='heynemann@gmail.com',
    #maintainer = 'Rafael Carício',
    #maintainer_email = 'rafael@caricio.com',
    maintainer='Zearin',
    license='MIT',


    ### CATEGORIZATION
    keywords='test testing vows tdd bdd development coverage profile profiling',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: MacOS',
        'Operating System :: POSIX',
        'Operating System :: Unix',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Testing'
    ],
)
