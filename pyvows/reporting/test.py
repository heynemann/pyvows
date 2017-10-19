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
try:
    from StringIO import StringIO
except:
    from io import StringIO

from pyvows.color import yellow, red, blue
from pyvows.reporting.common import (
    ensure_encoded,
    V_EXTRA_VERBOSE,
    V_VERBOSE,
    VowsReporter,)
from pyvows.result import VowsResult


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
    def pretty_print(self, file=sys.stdout):
        '''Prints PyVows test results.'''
        print(self.header('Vows Results'), file=file)

        if not self.result.contexts:
            # FIXME:
            #   If no vows are found, how could any be broken?
            summary = '{indent}{broken} No vows found! » 0 honored • 0 broken • 0 skipped (0.0s)'.format(
                indent=self.TAB * self.indent,
                broken=VowsReporter.BROKEN)
            print(summary, file=file)
            return

        if self.verbosity >= V_VERBOSE or self.result.errored_tests:
            print(file=file)

        for context in self.result.contexts:
            self.print_context(context['name'], context, file=file)

        summary = '{0}{1} OK » {honored:d} honored • {broken:d} broken • {skipped:d} skipped ({time:.6f}s)'.format(
            self.TAB * self.indent,
            self.status_symbol,
            honored=self.result.successful_tests,
            broken=self.result.errored_tests,
            skipped=self.result.skipped_tests,
            time=self.result.elapsed_time
        )
        print(summary, file=file)
        print(file=file)

    def print_context(self, name, context, file=sys.stdout):
        #   FIXME: Add Docstring
        #
        #       *   Is this only used in certain cases?
        #           *   If so, which?
        self.indent += 1

        if (self.verbosity >= V_VERBOSE or not self.result.eval_context(context)):
            contextName = StringIO()
            self.humanized_print(name, file=contextName)
            contextName = contextName.getvalue().replace('\n', '')
            if context.get('skip', None):
                contextName += ' (SKIPPED: {0})'.format(str(context['skip']))
            print(contextName, file=file)

        def _print_successful_test():
            honored = ensure_encoded(VowsReporter.HONORED)
            topic = ensure_encoded(test['topic'])
            name = ensure_encoded(test['name'])

            if self.verbosity == V_VERBOSE:
                self.humanized_print('{0} {1}'.format(honored, name), file=file)
            elif self.verbosity >= V_EXTRA_VERBOSE:
                if test['enumerated']:
                    self.humanized_print('{0} {1} - {2}'.format(honored, topic, name), file=file)
                else:
                    self.humanized_print('{0} {1}'.format(honored, name), file=file)

        def _print_skipped_test():
            if self.verbosity >= V_VERBOSE:
                message = StringIO()
                self.humanized_print('{0} {1}'.format(VowsReporter.SKIPPED, test['name']), file=message)
                message = message.getvalue().replace('\n', '')
                if test['skip'] != context['skip']:
                    message = '{0} (SKIPPED: {1})'.format(message, str(test['skip']))
                print(message, file=file)

        def _print_failed_test():
            ctx = test['context_instance']

            def _print_traceback():
                self.indent += 2

                ### NOTE:
                ###     Commented out try/except; potential debugging hinderance

                #try:

                traceback_args = (test['error']['type'],
                                  test['error']['value'],
                                  test['error']['traceback'])
                self.print_traceback(*traceback_args, file=file)

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
                    print('\n', self.indent_msg(red(file_msg)), '\n', file=file)

                self.indent -= 2

            self.humanized_print('{0} {test}'.format(VowsReporter.BROKEN, test=test['name']), file=file)

            # print generated topic (if applicable)
            if ctx.generated_topic:
                value = yellow(test['topic'])
                self.humanized_print('', file=file)
                self.humanized_print('\tTopic value:', file=file)
                self.humanized_print('\t{value}'.format(value=value), file=file)
                self.humanized_print('\n' * 2, file=file)

            # print traceback
            _print_traceback()

        # Show any error raised by the setup, topic or teardown functions
        if context.get('error', None):
            e = context['error']
            print('\n', self.indent_msg(blue("Error in {0!s}:".format(e.source))), file=file)
            self.print_traceback(*e.exc_info, file=file)

        else:
            for test in context['tests']:
                if VowsResult.test_is_successful(test):
                    _print_successful_test()
                elif test['skip']:
                    _print_skipped_test()
                else:
                    _print_failed_test()

        # I hereby (re)curse you...!
        for context in context['contexts']:
            self.print_context(context['name'], context, file=file)

        self.indent -= 1
