# -*- coding: utf-8 -*-
'''This package contains different runtime implementations for PyVows.  PyVows will
select the fastest possible runner, using fallbacks if unavailable.
'''


class SkipTest(Exception):
    pass

from pyvows.runner.gevent import VowsParallelRunner as VowsRunner

__all__ = ('VowsRunner', 'SkipTest')
