# -*- coding: utf-8 -*-
'''This package contains different runtime implementations for PyVows.  PyVows will
select the fastest possible runner, using fallbacks if unavailable.

'''
# pragma: no cover

# Don't bother covering this file.  A failure in these statements will 
# prevent PyVows from running.  The failure will be obvious.

try:
    ##  GEvent
    from pyvows.runner.gevent import VowsParallelRunner as VowsRunner
except ImportError as e:
    ##  Sequential
    from pyvows.runner.sequential import VowsSequentialRunner as VowsRunner
finally:
    __all__ = ('VowsRunner')