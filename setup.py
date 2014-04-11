#!/usr/bin/env python
# -*- coding: utf-8 -*-

# pyVows testing engine
# https://github.com/heynemann/pyvows

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 Bernardo Heynemann heynemann@gmail.com

# stdlib
import sys

# external
import setuptools

# local
import pyvows
import pyvows.version


#--------------------------------------------------------------------------------
#   REQUIREMENTS
#--------------------------------------------------------------------------------
REQUIREMENTS = {
    'install': [
        'gevent>=0.13.6',
        'preggy>=0.11.1',
        ],

    'test': [
        'argparse',
        'colorama',
        'coverage',
        ],
}

if sys.version_info < (2, 7):
    REQUIREMENTS['install'].append('argparse >= 1.1')

REQUIREMENTS.update(
    {
        'extras': {'tests': REQUIREMENTS['test']}
    })



#--------------------------------------------------------------------------------
#   SETUP
#--------------------------------------------------------------------------------
setuptools.setup(
    #--------------------------------------------------------------------------------
    #   OVERVIEW
    #--------------------------------------------------------------------------------
    name='pyvows',
    description=pyvows.__description__,
    long_description=pyvows.__doc__,

    #--------------------------------------------------------------------------------
    #   URLs
    #--------------------------------------------------------------------------------
    url=pyvows.__url__,

    #--------------------------------------------------------------------------------
    #   TECHNICAL INFO
    #--------------------------------------------------------------------------------
    version=pyvows.version.to_str(),
    install_requires=REQUIREMENTS['install'],
    extras_require=REQUIREMENTS['extras'],
    packages=setuptools.find_packages(),
    package_dir={'pyvows': 'pyvows'},
    entry_points={
        'console_scripts': [
            'pyvows = pyvows.cli:main'
        ]
    },

    #--------------------------------------------------------------------------------
    #   PEOPLE & LICENSE
    #--------------------------------------------------------------------------------
    author=pyvows.__author__,
    author_email=pyvows.__author_email__,
    maintainer=pyvows.__maintainer__,
    license=pyvows.__license__,

    #--------------------------------------------------------------------------------
    #   CATEGORIZATION
    #--------------------------------------------------------------------------------
    keywords=pyvows.__keywords__,
    classifiers=pyvows.__classifiers__,
)
