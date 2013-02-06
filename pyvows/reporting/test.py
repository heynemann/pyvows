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

import sys

from pyvows.color import *
from pyvows.reporting.common import (
    ensure_encoded,
    PROGRESS_SIZE,
    V_EXTRA_VERBOSE,
    V_VERBOSE,
    V_NORMAL,
    V_SILENT,
    VowsReporter,)


class VowsTestReporter(VowsReporter):
    '''A VowsReporter which prints test results.'''

    def __init__(self, result, verbosity):
        super(VowsTestReporter, self).__init__(result, verbosity)
        self.indent    = 1

    #-------------------------------------------------------------------------
    #   Class Methods
    #-------------------------------------------------------------------------
    @classmethod
    def handle_success(cls, vow):
        #   FIXME: Add Docstring / Comment description
        #
        #       *   Why is `vow` unused?
        sys.stdout.write(VowsReporter.HONORED)

    @classmethod
    def handle_error(cls, vow):
        #   FIXME: Add Docstring / Comment description
        #
        #       *   Why is `vow` unused?
        sys.stdout.write(VowsReporter.BROKEN)

    #-------------------------------------------------------------------------
    #   Printing Methods
    #-------------------------------------------------------------------------
    def pretty_print(self):
        '''Prints PyVows test results.'''
        print self.header('Vows Results')

        if not self.result.contexts:
            # FIXME:
            #   If no vows are found, how could any be broken?
            print '{indent}{broken} No vows found! » 0 honored • 0 broken (0.0s)'.format(
                indent = self.TAB * self.indent,
                broken = VowsReporter.BROKEN,
            )
            return

        if self.verbosity >= V_VERBOSE or self.result.errored_tests:
            print '' * 2

        for context in self.result.contexts:
            self.print_context(context['name'], context)

        print '{0}{1} OK » {honored:d} honored • {broken:d} broken ({time:.6f}s)'.format(
            self.TAB * self.indent,
            VowsReporter.HONORED if self.result.successful else VowsReporter.BROKEN,
            honored = self.result.successful_tests,
            broken  = self.result.errored_tests,
            time    = self.result.elapsed_time)

        print

    def print_context(self, name, context):
        #   FIXME: Add Docstring
        #
        #       *   Is this only used in certain cases?
        #           *   If so, which?
        self.indent += 1
        indentation2 = self.TAB * (self.indent + 2)

        if (self.verbosity >= V_VERBOSE or
            not self.result.eval_context(context)):
            self.humanized_print(name)

        for test in context['tests']:
            if test['succeeded']:
                honored, topic, name = map(
                    ensure_encoded,
                    (VowsReporter.HONORED, test['topic'], test['name']))

                if self.verbosity == V_VERBOSE:
                    self.humanized_print('{0} {1}'.format(honored, name))
                elif self.verbosity >= V_EXTRA_VERBOSE:
                    if test['enumerated']:
                        self.humanized_print('{0} {1} - {2}'.format(honored, topic, name))
                    else:
                        self.humanized_print('{0} {1}'.format(honored, name))
            else:
                ctx = test['context_instance']

                self.humanized_print('{0} {test}'.format(
                    VowsReporter.BROKEN,
                    test = test['name']))

                if ctx.generated_topic:
                    value = yellow(test['topic'])

                    self.humanized_print('')
                    self.humanized_print('\tTopic value:')
                    self.humanized_print('\t{value}'.format(value = value))
                    self.humanized_print('\n' * 2)

                if hasattr(test, 'topic')               \
                   and hasattr(test['topic'], 'error')  \
                   and test['topic']['error'] is not None:
                    print self.indent_msg('')
                    print blue(self.indent_msg('Topic Error:'))
                    exc_type, exc_value, exc_traceback = test['topic'].error
                    self.print_traceback(exc_type, exc_value, exc_traceback, indentation2)
                else:
                    error = test['error']
                    exc_type, exc_value, exc_traceback = error['type'], error['value'], error['traceback']

                    self.print_traceback(exc_type, exc_value, exc_traceback, indentation2)

                if 'file' in test:
                    print
                    print red('{indent}found in {test[file]} at line {test[lineno]}'.format(
                        indent= indentation2,
                        test  = test))
                    print

        for context in context['contexts']:
            self.print_context(context['name'], context)

        self.indent -= 1
