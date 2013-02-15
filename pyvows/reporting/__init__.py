# -*- coding: utf-8 -*-

# pyvows testing engine
# https://github.com/heynemann/pyvows

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 Bernardo Heynemann heynemann@gmail.com


from pyvows.reporting.common import VowsReporter
from pyvows.reporting.coverage import VowsCoverageReporter
from pyvows.reporting.profile import VowsProfileReporter
from pyvows.reporting.test import VowsTestReporter


__all__ = [
    'VowsDefaultReporter',
    'VowsTestReporter',
    'VowsProfileReporter',
    'VowsCoverageReporter',
    'VowsReporter',
]


class VowsDefaultReporter(VowsTestReporter,
                          VowsCoverageReporter,
                          VowsProfileReporter):
    '''The all-in-one reporter used by other parts of PyVows.'''
    pass
