#!/usr/bin/env python
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
import re
import traceback

from xml.etree import ElementTree as etree

from pyvows.color import *
from pyvows.core import VowsAssertionError

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
        self.result=result
        self.verbosity=verbosity
    
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

        return green('{0}{ruler}{0}{msg}{0}{ruler}{0}'.format(
            '\n',
            ruler = ruler,
            msg   = msg))
    
    def indent_msg(self, msg, indentation=None):
        '''Returns `msg` with the indentation specified by `indentation`.
        '''
        msg = msg.capitalize()
        msg = self.format_python_constants(msg)
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
        sys.stdout.write(cls.honored)
    
    @classmethod
    def handle_error(cls, vow):
        #   FIXME: Add Docstring / Comment description
        #   
        #       *   Why is `vow` unused?
        sys.stdout.write(cls.broken)
    
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
                broken = self.BROKEN,
            )
            return

        if self.verbosity >= V_VERBOSE or self.result.errored_tests:
            print '' * 2

        for context in self.result.contexts:
            self.print_context(context['name'], context)

        print '{0}{1} OK » {honored:d} honored • {broken:d} broken ({time:.6f}s)'.format(
            self.TAB * self.indent,
            self.HONORED if self.result.successful else self.BROKEN,
            honored=self.result.successful_tests,
            broken=self.result.errored_tests,
            time=self.result.elapsed_time)
        
        print

    def print_context(self, name, context):
        #   FIXME: Add Docstring
        #
        #       *   Is this only used in certain cases?  
        #           *   If so, which?
        self.indent += 1
        indentation2 = self.TAB * (self.indent + 2)

        if self.verbosity >= V_VERBOSE or not self.result.eval_context(context):
            self.humanized_print(name)

        for test in context['tests']:
            if test['succeeded']:
                honored, topic, name = map(
                    ensure_encoded,
                    (VowsDefaultReporter.HONORED, test['topic'], test['name']))
                
                if self.verbosity == V_VERBOSE:
                    self.humanized_print('{0} {1}'.format(honored, name))
                elif self.verbosity >= V_EXTRA_VERBOSE:
                    if test['enumerated']:
                        self.humanized_print('{0} {1} - {2}'.format(honored, topic, name))
                    else:
                        self.humanized_print('{0} {1}'.format(honored, name))
            else:
                ctx = test['context_instance']

                self.humanized_print('{0} {1}'.format(
                    VowsDefaultReporter.BROKEN,
                    test['name']))

                if ctx.generated_topic:
                    value = yellow(self.max_length(test['topic'], 250))
                    
                    self.humanized_print('')
                    self.humanized_print('\tTopic value:')
                    self.humanized_print('\t{value}'.format(value = value))
                    self.humanized_print('\n' * 2)

                if hasattr(test, 'topic') and\
                   hasattr(test['topic'], 'error') and\
                   test['topic']['error'] is not None:
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


class VowsCoverageReporter(VowsReporter):
    '''A VowsReporter which prints the code coverage of tests.'''

    def get_uncovered_lines(self, uncovered_lines, number_of=3):
        '''Searches for untested lines of code.  Returns a string
        listing the line numbers.
        
        If the number of uncovered lines is greater than `number_of`, this will
        only explicitly list the first `number_of` uncovered lines, followed
        by ' and ## more' (where '##' is the total number of additional 
        uncovered lines.
        '''
        if len(uncovered_lines) > number_of:
            template_str = []
            for i in range(number_of):
                template_str.append(uncovered_lines[i])
                if i is not (number_of - 1):
                    template_str.append(', ')

            template_str.append(', and {num_more_uncovered:d} more'.format(
                num_more_uncovered = len(uncovered_lines) - number_of)
                )

            return ''.join(template_str)

        return ', '.join(uncovered_lines)

    def parse_coverage_xml(self, xml):
        '''Reads `xml` for code coverage statistics, and returns the
        dict `result`.
        '''
        result = {}
        root   = etree.fromstring(xml)
        result['overall'] = float(root.attrib['line-rate']) * 100
        result['classes'] = []

        for package in root.findall('.//package'):
            package_name = package.attrib['name']
            for klass in package.findall('.//class'):
                result['classes'].append({
                    'name': '.'.join([package_name, klass.attrib['name']]),
                    'line_rate': float(klass.attrib['line-rate']) * 100,
                    'uncovered_lines': [line.attrib['number']
                                        for line in klass.find('lines')
                                        if  line.attrib['hits'] == '0']
                })
        return result

    #-------------------------------------------------------------------------
    #   Printing (Coverage)
    #-------------------------------------------------------------------------
    def print_coverage(self, xml, cover_threshold):
        '''Prints code coverage statistics for your tests.'''
        print self.header('Code Coverage')

        root         = self.parse_coverage_xml(xml)
        klasses      = sorted(root['classes'], key=lambda klass: klass['line_rate'])
        max_length   = max([ len(klass['name']) for klass in root['classes'] ])
        max_coverage = 0

        for klass in klasses:
            coverage = klass['line_rate']

            if coverage < cover_threshold:
                cover_character = self.BROKEN
            else:
                cover_character = self.HONORED

            if 100.0 < max_coverage < coverage:
                max_coverage = coverage
                if max_coverage == 100.0:
                    print

            coverage = int(round(coverage, 0))
            progress = int(round(coverage / 100.0 * PROGRESS_SIZE, 0))
            offset   = coverage == 0 and 2 or (coverage < 10 and 1 or 0)
            #   FIXME: explain the `offset` line please?  :)
                        
            if coverage == 0 and not klass['uncovered_lines']:
                continue

            print self.format_class_coverage(
                cover_character = cover_character,
                klass           = klass['name'],
                space1          = ' ' * (max_length - len(klass['name'])),
                progress        = progress,
                cover_pct       = (coverage > 0 and ' ' or '') + '{coverage:.2f}'.format(coverage=coverage),
                space2          = ' ' * (PROGRESS_SIZE - progress + offset),
                lines           = self.get_uncovered_lines(klass['uncovered_lines']))

        print

        total_coverage  = root['overall']
        cover_character = self.HONORED if (total_coverage >= cover_threshold) else self.BROKEN
        progress        = int(round(total_coverage / 100.0 * PROGRESS_SIZE, 0))

        print self.format_overall_coverage(cover_character, max_length, progress, total_coverage)

        print
            
    def format_class_coverage(self, cover_character, klass, space1, progress, cover_pct, space2, lines):
        '''Accepts coverage data for a class and returns a formatted string (intended for 
        humans).
        '''
        #   FIXME:
        #       Doesn't this *actually* print coverage for a module, and not a class?
        
        # preprocess raw data...
        klass       = blue( klass )
        cover_pct   = white( cover_pct )
        
        # ...then format
        return ' {0} {klass}{space1}\t{progress}{cover_pct}%{space2} {lines}'.format(
            # TODO:
            #   * remove manual spacing, use .format() alignment
            cover_character,
            klass     = klass,
            space1    = space1,
            progress  = '•' * progress,
            cover_pct = cover_pct,
            space2    = space2,
            lines     = lines
        )
        
    def format_overall_coverage(self, cover_character, max_length, progress, total_coverage):
        '''Accepts overall coverage data and returns a formatted string (intended for 
        humans).
        '''

        # preprocess raw data
        overall = blue('OVERALL')
        space   = ' ' * (max_length - len('OVERALL'))
        total   = white('{total_coverage:.2%}'.format(total_coverage=total_coverage/100))
        # then format
        return ' {0} {overall}{space}\t{progress} {total}%'.format(
            cover_character,
            overall  = overall,
            space    = space,
            progress = '•' * progress,
            total    = total)


class VowsProfileReporter(VowsReporter):
    '''A VowsReporter which prints a profile of the 10 slowest topics.'''

    def print_profile(self, threshold):
        '''Prints the 10 slowest topics that took longer than `threshold`
        to test.
        '''

        MAX_PATH_SIZE = 30
        topics = self.result.get_worst_topics(number=10, threshold=threshold)

        if topics:
            print self.header('Slowest Topics')

            print yellow('       elapsed     Context File Path                 Context Name')
            for index, topic in enumerate(topics):
                name = self.under_split(topic['context'])
                name = self.camel_split(name)

                print Style.BRIGHT + ("%s#%02d%s    %.05fs    %s%s%" + str(MAX_PATH_SIZE) + "s%s%s    %s") % (
                        Fore.BLUE,
                        index + 1,
                        Fore.RESET,
                        topic['elapsed'],
                        Style.DIM,
                        Fore.WHITE,
                        topic['path'][-MAX_PATH_SIZE:],
                        Fore.RESET,
                        Style.BRIGHT,
                        name
                ) + Style.RESET_ALL

            print


class VowsDefaultReporter(VowsTestReporter,
                          VowsCoverageReporter,
                          VowsProfileReporter):
    '''The all-in-one reporter used by other parts of PyVows.'''
    pass
