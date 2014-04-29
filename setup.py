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
        
    'setup': [],

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
#   CUSTOM COMMANDS
#--------------------------------------------------------------------------------
class test(setuptools.Command):
    description = "(pyvows) Test pyvows using itself"
    user_options = list(tuple())
    
    _cli_args = ['export', r'PYTHONPATH=".:${PYTHONPATH}"', '&&', 'python', '-B', './pyvows']
    _pyvows_args = ['--cover','--cover-package=pyvows','--cover-threshold=80.0','--profile']
    
    
    def initialize_options(self): pass
    def finalize_options(self):   pass
    
    def _prepare_run(self):
        _cli_input = self.__class__._cli_args + self.__class__._pyvows_args
        return _cli_input
    
    def run(self):
        import subprocess
        _cli_input = self._prepare_run()
        _cli_input = ' '.join(_cli_input)
        subprocess.call( 
            _cli_input, 
            stdin=sys.stdin, 
            stdout=sys.stdout, 
            stderr=sys.stderr, 
            shell=True
        )


vows = test  # alias 'test' command


#--------------------------------------------------------------------------------
#   SETUP
#--------------------------------------------------------------------------------
setuptools.setup(
    #--------------------------------------------------------------------------------
    #   CUSTOM COMMANDS
    #--------------------------------------------------------------------------------
    cmdclass={
        'test': test,
        'vows': test,
    },
    
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
