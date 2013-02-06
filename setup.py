#!/usr/bin/env python
# -*- coding: utf-8 -*-

# pyVows testing engine
# https://github.com/heynemann/pyvows

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 Bernardo Heynemann heynemann@gmail.com

from setuptools import setup
from pyvows import version

setup(
    name = 'pyVows',
    version = version.to_str(),
    description = 'pyVows is a BDD test engine based on Vows.js(http://vowsjs.org).',
    long_description = '''
pyVows is a test engine based on Vows.js. It features topic-based testing, 
(*fast*) parallel running of tests, code coverage reports, test profiling, and 
more(http://pyvows.org).
''',
    keywords = 'test testing vows tdd bdd development coverage profile profiling',
    author = 'Bernardo Heynemann',
    author_email = 'heynemann@gmail.com',
    #Contributors
    #contributor = 'Rafael Carício',
    #contributor_email = 'rafael@caricio.com',
    url = 'http://heynemann.github.com/pyvows/',
    license = 'MIT',
    classifiers = ['Development Status :: 4 - Beta',
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
    packages = ['pyvows', 'pyvows.assertions', 'pyvows.assertions.types','pyvows.reporting'],
    package_dir = {'pyvows': 'pyvows'},

    install_requires=[
        'gevent>=0.13.6',
        'argparse'
    ],

    entry_points = {
        'console_scripts': [
            'pyvows = pyvows.console:main'
        ],
    },

)


