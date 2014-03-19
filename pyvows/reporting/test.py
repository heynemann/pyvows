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

import sys

from pyvows.color import yellow, red, blue
from pyvows.errors import VowsInternalError
from pyvows.reporting.common import (
    ensure_encoded,
    V_EXTRA_VERBOSE,
    V_VERBOSE,
    VowsReporter,)


class VowsTestReporter(VowsReporter):
    '''A VowsReporter which prints test results.'''

    def __init__(self, result, verbosity):
        super(VowsTestReporter, self).__init__(result, verbosity)

    @property
    def status_symbol(self):
        '''Returns the symbol indicating whether all tests passed.'''
        if self.result.successful:
            return VowsReporter.HONORED
        else:
            return VowsReporter.BROKEN

    #-------------------------------------------------------------------------
    #   Class Methods
    #-------------------------------------------------------------------------
    @classmethod
    def on_vow_success(cls, vow):
        #   FIXME: Add Docstring / Comment description
        #
        #       *   Why is `vow` unused?
        sys.stdout.write(VowsReporter.HONORED)

    @classmethod
    def on_vow_error(cls, vow):
        #   FIXME: Add Docstring / Comment description
        #
        #       *   Why is `vow` unused?
        sys.stdout.write(VowsReporter.BROKEN)

    #-------------------------------------------------------------------------
    #   Printing Methods
    #-------------------------------------------------------------------------
    def pretty_print(self):
        '''Prints PyVows test results.'''
        print(self.header('Vows Results'))

        if not self.result.contexts:
            # FIXME:
            #   If no vows are found, how could any be broken?
            print(
                '{indent}{broken} No vows found! » 0 honored • 0 broken (0.0s)'.format(
                    indent=self.TAB * self.indent,
                    broken=VowsReporter.BROKEN)
                )
            return

        if self.verbosity >= V_VERBOSE or self.result.errored_tests:
            print()

        for context in self.result.contexts:
            self.print_context(context['name'], context)

        print('{0}{1} OK » {honored:d} honored • {broken:d} broken ({time:.6f}s)'.format(
            self.TAB * self.indent,
            self.status_symbol,
            honored=self.result.successful_tests,
            broken=self.result.errored_tests,
            time=self.result.elapsed_time))

        print()

    def print_context(self, name, context):
        #   FIXME: Add Docstring
        #
        #       *   Is this only used in certain cases?
        #           *   If so, which?
        self.indent += 1

        if (self.verbosity >= V_VERBOSE or
                not self.result.eval_context(context)):
            self.humanized_print(name)

        def _print_successful_context():
            honored = ensure_encoded(VowsReporter.HONORED)
            topic = ensure_encoded(test['topic'])
            name = ensure_encoded(test['name'])

            if self.verbosity == V_VERBOSE:
                self.humanized_print('{0} {1}'.format(honored, name))
            elif self.verbosity >= V_EXTRA_VERBOSE:
                if test['enumerated']:
                    self.humanized_print('{0} {1} - {2}'.format(honored, topic, name))
                else:
                    self.humanized_print('{0} {1}'.format(honored, name))

        def _print_failed_context():
            ctx = test['context_instance']

            def _print_traceback():
                self.indent += 2
                
                ### NOTE:
                ###     Commented out try/except; potential debugging hinderance
                
                #try:

                traceback_args = (test['error']['type'],
                                  test['error']['value'],
                                  test['error']['traceback'])
                self.print_traceback(*traceback_args)
                
                # except Exception:
                #     # should never occur!
                #     err_msg = '''Unexpected error in PyVows!
                #                  PyVows error occurred in: ({0!s})
                #                  Context was: {1!r}
                # 
                #               '''
                #     # from os.path import abspath
                #     raise VowsInternalError(err_msg, 'pyvows.reporting.test', ctx)

                # print file and line number
                if 'file' in test:
                    file_msg = 'found in {test[file]} at line {test[lineno]}'.format(test=test)
                    print('\n', 
                          self.indent_msg(red(file_msg)), 
                          '\n')

                self.indent -= 2

            self.humanized_print('{0} {test}'.format(
                VowsReporter.BROKEN,
                test=test['name']))

            # print generated topic (if applicable)
            if ctx.generated_topic:
                value = yellow(test['topic'])
                self.humanized_print('')
                self.humanized_print('\tTopic value:')
                self.humanized_print('\t{value}'.format(value=value))
                self.humanized_print('\n' * 2)

            # print traceback
            _print_traceback()

        # Show any error raised by the setup, topic or teardown functions
        if context.get('error', None):
            e = context['error']
            print('\n', self.indent_msg(blue("Error in {0!s}:".format(e.source))))
            self.print_traceback(*e.exc_info)
            print(self.indent_msg(red("Nested tests following this error have not been run.")))

        else:
            for test in context['tests']:
                if test['succeeded']:
                    _print_successful_context()
                else:
                    _print_failed_context()

        # I hereby (re)curse you...!
        for context in context['contexts']:
            self.print_context(context['name'], context)

        self.indent -= 1
