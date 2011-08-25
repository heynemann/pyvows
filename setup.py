#!/usr/bin/env python
# -*- coding: utf-8 -*-

# pyVows testing engine
# https://github.com/heynemann/pyvows

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 Bernardo Heynemann heynemann@gmail.com

from setuptools import setup
from pyvows.version import __version__

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
    #Contributors
    #contributor = 'Rafael Carício',
    #contributor_email = 'rafael@caricio.com',
    url = 'http://heynemann.github.com/pyvows/',
    license = 'MIT',
    classifiers = ['Development Status :: 3 - Alpha',
                   'Intended Audience :: Developers',
                   'License :: OSI Approved :: MIT License',
                   'Natural Language :: English',
                   'Operating System :: MacOS',
                   'Operating System :: POSIX :: Linux',
                   'Programming Language :: Python :: 2.6',
                   'Topic :: Software Development :: Testing'
    ],
    packages = ['pyvows', 'pyvows.assertions'],
    package_dir = {"pyvows": "pyvows"},

    install_requires=[
        "eventlet",
        "colorama",
        "lxml"
    ],

    entry_points = {
        'console_scripts': [
            'pyvows = pyvows.console:main'
        ],
    },

)


