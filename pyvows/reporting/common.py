# -*- coding: utf-8 -*-
'''Contains the `VowsDefaultReporter` class, which handles output after tests
have been run.
'''

# pyvows testing engine
# https://github.com/heynemann/pyvows

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 Bernardo Heynemann heynemann@gmail.com
from __future__ import division, print_function

import re
import traceback
import sys

from pyvows.color import yellow, green, red, bold

__all__ = [
    'PROGRESS_SIZE',
    'V_EXTRA_VERBOSE',
    'V_VERBOSE',
    'V_NORMAL',
    'V_SILENT',
    'ensure_encoded',
    'VowsReporter',
]

PROGRESS_SIZE = 50

# verbosity levels
V_EXTRA_VERBOSE = 4
V_VERBOSE = 3
V_NORMAL = 2
V_SILENT = 1


def ensure_encoded(thing, encoding='utf-8'):
    '''Ensures proper encoding for unicode characters.

    Currently used only for characters `✓` and `✗`.

    '''
    if isinstance(thing, bytes) or not isinstance(thing, str):
        return thing
    else:
        return thing.encode(encoding)


class VowsReporter(object):
    '''Base class for other Reporters to extend.  Contains common attributes
    and methods.
    '''
    #   Should *only* contain attributes and methods that aren't specific
    #   to a particular type of report.

    HONORED = green('✓')
    BROKEN = red('✗')
    SKIPPED = '?'
    TAB = '  '

    def __init__(self, result, verbosity):
        self.result = result
        self.verbosity = verbosity
        self.indent = 1

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

    def format_traceback(self, traceback_list):
        '''Adds the current level of indentation to a traceback (so it matches
        the current context's indentation).

        '''

        # TODO:
        #   ...Is this a decorator?  If so, please add a comment or docstring
        #   to make it explicit.
        def _indent(msg):
            if msg.strip().startswith('File'):
                return self.indent_msg(msg)
            return msg

        tb_list = [_indent(tb) for tb in traceback_list]
        return ''.join(tb_list)

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

        msg = ' {0}'.format(msg)
        msg = '{0}{ruler}{0}{msg}{0}{ruler}{0}'.format(
            '\n',
            ruler=ruler,
            msg=msg)

        msg = green(bold(msg))

        return msg

    def indent_msg(self, msg, indentation=None):
        '''Returns `msg` with the indentation specified by `indentation`.

        '''
        if indentation is not None:
            indent = self.TAB * indentation
        else:
            indent = self.TAB * self.indent

        return '{indent}{msg}'.format(
            indent=indent,
            msg=msg
        )

    #-------------------------------------------------------------------------
    #   Printing Methods
    #-------------------------------------------------------------------------
    def humanized_print(self, msg, indentation=None, file=sys.stdout):
        '''Passes `msg` through multiple text filters to make the output
        appear more like normal text, then prints it (indented by
        `indentation`).

        '''
        msg = self.under_split(msg)
        msg = self.camel_split(msg)
        msg = msg.replace('  ', ' ')  # normalize spaces if inserted by
                                      # both of the above
        msg = msg.capitalize()
        msg = self.format_python_constants(msg)

        print(self.indent_msg(msg, indentation), file=file)

    def print_traceback(self, err_type, err_obj, err_traceback, file=sys.stdout):
        '''Prints a color-formatted traceback with appropriate indentation.'''
        if isinstance(err_obj, AssertionError):
            error_msg = err_obj
        elif isinstance(err_obj, bytes):
            error_msg = err_obj.decode('utf8')
        else:
            error_msg = err_obj

        print(self.indent_msg(red(error_msg)), file=file)

        if self.verbosity >= V_NORMAL:
            traceback_msg = traceback.format_exception(err_type, err_obj, err_traceback)
            traceback_msg = self.format_traceback(traceback_msg)
            traceback_msg = '\n{traceback}'.format(traceback=traceback_msg)
            traceback_msg = self.indent_msg(yellow(traceback_msg))
            print(traceback_msg, file=file)
