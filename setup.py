#!/usr/bin/env python
# -*- coding: utf-8 -*-

# pyVows testing engine
# https://github.com/heynemann/pyvows

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 Bernardo Heynemann heynemann@gmail.com

from setuptools import setup
from pyvows import __version__

setup(
    name = 'pyVows',
    version = '.'.join([str(item) for item in __version__]),
    description = "pyVows is a test engine based in VowsJS(http://vowsjs.org/).",
    long_description = """
pyVows is a test engine based in Vows JS and features topic-based testing as well as parallel running of tests.
""",    
    keywords = 'testing vows test tdd',
    author = 'Bernardo Heynemann',
    author_email = 'heynemann@gmail.com',
    url = 'https://github.com/heynemann/pyvows',
    license = 'MIT',
    classifiers = ['Development Status :: 4 - Beta',
                   'Intended Audience :: Developers',
                   'License :: OSI Approved :: MIT License',
                   'Natural Language :: English',
                   'Operating System :: MacOS',
                   'Operating System :: POSIX :: Linux',
                   'Programming Language :: Python :: 2.6'
    ],
    packages = ['pyvows'],
    package_dir = {"pyvows": "pyvows"},

    entry_points = {
        'console_scripts': [
            'vows = pyvows.console:main'
        ],
    },

)


