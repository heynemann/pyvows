# -*- coding: utf-8 -*-
'''PyVows is a test engine based on Vows.js. It features topic-based testing,
(fast!) parallel running of tests, code coverage reports, test profiling, and
more.

PyVows is inspired by Vows.js, a BDD framework for Node.js.

---

PyVows runs tests asynchronously.  This makes tests which target I/O run much 
faster, by executing them concurrently. 

A faster test suite gets run more often, thus improving the feedback cycle.

Learn more:
http://pyvows.org

'''


# pyVows testing engine
# https://github.com/heynemann/pyvows
#
# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 Bernardo Heynemann heynemann@gmail.com

# flake8: noqa

#-------------------------------------------------------------------------------------------------


#   PEOPLE
__author__ = 'Bernardo Heynemann'
__author_email__ = 'heynemann@gmail.com'

__maintainer__ = 'Zearin'
#__maintainer__ = 'Rafael Carício'
#__maintainer_email__ = 'rafael@caricio.com'


#   MISC
__url__ = 'http://pyvows.org'
__keywords__ = 'test testing vows tdd bdd development coverage profile profiling'
__description__ = 'pyvows is a BDD test engine (inspired by Vows.js)'
__license__ = 'MIT'
__classifiers__ = [
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
]

#-------------------------------------------------------------------------------------------------

try:
    from preggy import expect
except:
    pass

try:
    from pyvows.core import Vows, expect
except ImportError:
    pass
