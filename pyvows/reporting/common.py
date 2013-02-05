# -*- coding: utf-8 -*-
'''Contains the `VowsDefaultReporter` class, which handles output after tests
have been run.
'''

# pyvows testing engine
# https://github.com/heynemann/pyvows

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 Bernardo Heynemann heynemann@gmail.com
from __future__ import division

import re
import traceback

from pyvows.color import *
from pyvows.core  import VowsAssertionError

__all__ = [ 'PROGRESS_SIZE',
            'V_EXTRA_VERBOSE',
            'V_VERBOSE',
            'V_NORMAL',
            'V_SILENT',
            'ensure_encoded',
            'VowsReporter',]

PROGRESS_SIZE   = 50

# verbosity levels
V_EXTRA_VERBOSE = 4
V_VERBOSE       = 3
V_NORMAL        = 2
V_SILENT        = 1


def ensure_encoded(thing, encoding='utf-8'):
    '''Ensures proper encoding for unicode characters.

    Currently used only for characters `✓` and `✗`.
    '''
    if isinstance(thing, unicode):
        return thing.encode(encoding)
    else:
        return thing


class VowsReporter(object):
    '''Base class for other Reporters to extend.  Contains common attributes
    and methods.
    '''
    #   Should *only* contain attributes and methods that aren't specific
    #   to a particular type of report.

    def __init__(self, result, verbosity):
        self.result = result
        self.verbosity = verbosity

    HONORED = green('✓')
    BROKEN  = red('✗')
    TAB     = '  '

    #-------------------------------------------------------------------------
    #   String Formatting
    #-------------------------------------------------------------------------
    def camel_split(self, string):
        '''Splits camel-case `string` into separate words.

        Example:

            self.camel_split('SomeCamelCaseString')

        Returns:

            'Some camel case string'

        '''
        return re.sub('((?=[A-Z][a-z])|(?<=[a-z])(?=[A-Z])|(?=[0-9]\b))', ' ', string).strip()

    def under_split(self, string):
        '''Replaces all underscores in `string` with spaces.'''
        return ' '.join(string.split('_'))

    def format_traceback(self, traceback_list, indentation):
        '''Adds the current level of indentation to a traceback (so it matches
        the current context's indentation).

        '''

        # TODO:
        #   ...Is this a decorator?  If so, please add a comment or docstring
        #   to make it explicit.
        def indent(msg):
            if msg.startswith('  File'):
                return msg.replace('\n ', '\n {indentation}'.format(indentation=indentation))
            return msg

        return indentation.join(map(indent, traceback_list))

    def format_python_constants(self, msg):
        '''Fixes capitalization of Python constants.

        Since developers are used to reading `True`, `False`, and `None`
        as capitalized words, it makes sense to match that capitalization
        in reports.

        '''
        msg = msg.replace('true', 'True')
        msg = msg.replace('false', 'False')
        msg = msg.replace('none', 'None')
        return msg

    def header(self, msg, ruler_character='='):
        '''Returns the string `msg` with a text "ruler".  Also colorizes as
        bright green (when color is available).

        '''
        ruler = ' {0}'.format(len(msg) * ruler_character)
        
        msg   = ' {0}'.format(msg)
        msg   = '{0}{ruler}{0}{msg}{0}{ruler}{0}'.format(
            '\n',
            ruler = ruler,
            msg   = msg)
             
        msg   = green(bold(msg))
        
        return msg

    def indent_msg(self, msg, indentation=None):
        '''Returns `msg` with the indentation specified by `indentation`.

        '''
        return '{indent}{msg}'.format(
            indent = indentation or (self.TAB * self.indent),
            msg    = msg)


    #-------------------------------------------------------------------------
    #   Printing Methods
    #-------------------------------------------------------------------------
    def humanized_print(self, msg, indentation=None):
        '''Passes `msg` through multiple text filters to make the output
        appear more like normal text, then prints it (indented by
        `indentation`).

        '''
        msg = self.under_split(msg)
        msg = self.camel_split(msg)
        msg = msg.replace('  ',' ') # normalize spaces if inserted by
                                    # both of the above
        msg = msg.capitalize()
        msg = self.format_python_constants(msg)
        
        print self.indent_msg(msg, indentation)

    def print_traceback(self, exc_type, exc_value, exc_traceback, indentation):
        '''Prints a color-formatted traceback with appropriate indentation.'''
        if isinstance(exc_value, VowsAssertionError):
            exc_values_args = tuple(map(lambda arg: red(arg), exc_value.args))
            error_msg = exc_value.msg % exc_values_args
        else:
            error_msg = unicode(exc_value)

        print red('{indent}{error}'.format(
            indent = indentation,
            error  = error_msg))

        if self.verbosity >= V_NORMAL:
            traceback_msg = traceback.format_exception(exc_type, exc_value, exc_traceback)
            traceback_msg = self.format_traceback(traceback_msg, indentation)
            print yellow('\n{indent}{traceback}'.format(
                indent      = indentation,
                traceback   = traceback_msg))

