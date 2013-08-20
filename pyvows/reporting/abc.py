# -*- coding: utf-8 -*-
'''Contains the `VowsDefaultReporter` class, which handles output after tests
have been run.
'''

# pyvows testing engine
# https://github.com/heynemann/pyvows

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 Bernardo Heynemann heynemann@gmail.com

__all__ = ('VowsReporterABC')


class VowsReporterABC(object):
    '''Base class for other Reporters to extend.  Contains common attributes
    and methods.
    '''
    #   Should *only* contain attributes and methods that aren't specific
    #   to a particular type of report.

    def __init__(self, result, verbosity):
        self.result = result
        self.verbosity = verbosity
