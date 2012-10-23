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

import sys
import re
import traceback

from xml.etree import ElementTree as etree

from pyvows.color import Fore, Style
from pyvows.core import VowsAssertionError

PROGRESS_SIZE = 50

# verbosity levels
V_EXTRA_VERBOSE = 4
V_VERBOSE = 3
V_NORMAL = 2
V_SILENT = 1


def ensure_encoded(thing, encoding='utf-8'):
    if isinstance(thing, unicode):
        return thing.encode(encoding)
    else:
        return thing


class VowsDefaultReporter(object):
    honored = '{0}✓{1}'.format(Fore.GREEN + Style.BRIGHT, Fore.RESET + Style.RESET_ALL)
    broken = '{0}✗{1}'.format(Fore.RED + Style.BRIGHT, Fore.RESET + Style.RESET_ALL)

    def __init__(self, result, verbosity):
        self.verbosity = verbosity
        self.result = result
        self.tab = ' ' * 2
        self.indent = 1

    def camel_split(self, string):
        return re.sub('((?=[A-Z][a-z])|(?<=[a-z])(?=[A-Z])|(?=[0-9]\b))', ' ', string).strip()

    def under_split(self, string):
        return ' '.join(string.split('_'))

    @classmethod
    def handle_success(cls, vow):
        sys.stdout.write(cls.honored)

    @classmethod
    def handle_error(cls, vow):
        sys.stdout.write(cls.broken)

    def pretty_print(self):
        self.print_header('Vows Results')

        if not self.result.contexts:
            print '{indent}{broken} No vows found! » 0 honored • 0 broken (0.0s)'.format(
                indent=self.tab * self.indent,
                broken=self.broken,
            )
            return

        if self.verbosity >= V_VERBOSE or self.result.errored_tests:
            print
            print

        for context in self.result.contexts:
            self.print_context(context['name'], context)

        print '{0}{1} OK » {honored:d} honored • {broken:d} broken ({time:.6f}s)'.format(
            self.tab * self.indent,
            self.honored if self.result.successful else self.broken,
            honored=self.result.successful_tests,
            broken=self.result.errored_tests,
            time=self.result.elapsed_time
        )

        print

    def humanized_print(self, msg, indentation=None):
        msg = self.under_split(msg)
        msg = self.camel_split(msg)
        print (indentation or (self.tab * self.indent)) + msg.capitalize()

    def format_traceback(self, traceback_list, indentation):
        def indent(msg):
            if msg.startswith('  File'):
                return msg.replace('\n ', '\n {0}'.format(indentation))
            return msg

        return indentation.join(map(indent, traceback_list))

    def print_traceback(self, exc_type, exc_value, exc_traceback, indentation):
        if isinstance(exc_value, VowsAssertionError):
            exc_values_args = tuple(map(lambda arg: '{0.RESET}{1}{0.RED}{2}'.format(Fore, arg, exc_value.args)))
            error_msg = exc_value.msg % exc_values_args
        else:
            error_msg = unicode(exc_value)

        print '{indent}{F.RED}{error}{F.RESET}'.format(
            F=Fore,
            indent=indentation,
            error=error_msg)

        if self.verbosity >= V_NORMAL:
            traceback_msg = traceback.format_exception(exc_type, exc_value, exc_traceback)
            traceback_msg = self.format_traceback(traceback_msg, indentation)
            print
            print indentation + traceback_msg

    def print_context(self, name, context):

        self.indent += 1
        indentation2 = self.tab * (self.indent + 2)

        if self.verbosity >= V_VERBOSE or not self.result.eval_context(context):
            self.humanized_print(name)

        for test in context['tests']:
            if test['succeeded']:
                honored, topic, name = map(
                    ensure_encoded,
                    (VowsDefaultReporter.honored, test['topic'], test['name']))
                if self.verbosity == V_VERBOSE:
                    self.humanized_print('{0} {1}'.format(honored, name))
                elif self.verbosity >= V_EXTRA_VERBOSE:
                    if test['enumerated']:
                        self.humanized_print('{0} {1} - {2}'.format(honored, topic, name))
                    else:
                        self.humanized_print('{0} {1}'.format(honored, name))
            else:
                self.humanized_print('{0} {1}'.format(
                    VowsDefaultReporter.broken,
                    test['name']))

                if isinstance(test['topic'], Exception) and \
                   hasattr(test['context_instance'], 'topic_error'):
                    exc_type, exc_value, exc_traceback = test['context_instance'].topic_error
                    self.print_traceback(exc_type, exc_value, exc_traceback, indentation2)

                error = test['error']
                exc_type, exc_value, exc_traceback = error['type'], error['value'], error['traceback']

                self.print_traceback(exc_type, exc_value, exc_traceback, indentation2)

                if 'file' in test:
                    print
                    print '{0}found in {test["file"]} at line {test["lineno"]}{1}'.format(
                        (indentation2 + Fore.RED),
                        Fore.RESET,
                        test=test)
                    print

        for context in context['contexts']:
            self.print_context(context['name'], context)

        self.indent -= 1

    def print_profile(self, threshold):
        MAX_PATH_SIZE = 30
        topics = self.result.get_worst_topics(number=10, threshold=threshold)

        if topics:
            self.print_header('Slowest Topics')

            print "       elapsed    Context File Path                 Context Name"
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

    def parse_coverage_xml(self, xml):
        result = {}
        root = etree.fromstring(xml)
        result['overall'] = float(root.attrib['line-rate']) * 100
        result['classes'] = []
        for package in root.findall('.//package'):
            package_name = package.attrib['name']
            for klass in package.findall('.//class'):
                result['classes'].append({
                    'name': '.'.join([package_name, klass.attrib['name']]),
                    'line_rate': float(klass.attrib['line-rate']) * 100,
                    'uncovered_lines': [line.attrib['number'] for line in klass.find('lines') if line.attrib['hits'] == '0']
                })
        return result

    def print_header(self, msg):
        ruler = ' {0}'.format('=' * len(msg))

        prefix = ''.join((Fore.GREEN, Style.BRIGHT))
        suffix = ''.join((Style.RESET_ALL, Fore.RESET))

        msg = '{prefix} {msg}{suffix}'.format(
            prefix=prefix,
            msg=msg,
            suffix=suffix
        )
        print
        print ruler
        print msg
        print ruler
        print

    def print_coverage(self, xml, cover_threshold):
        write_blue = lambda msg: Fore.BLUE + Style.BRIGHT + str(msg) + Style.RESET_ALL + Fore.RESET
        write_white = lambda msg: Fore.WHITE + Style.BRIGHT + str(msg) + Style.RESET_ALL + Fore.RESET

        root = self.parse_coverage_xml(xml)

        max_length = max([len(klass['name']) for klass in root['classes']])

        self.print_header('Code Coverage')

        klasses = sorted(root['classes'], key=lambda klass: klass['line_rate'])

        max_coverage = 0
        for klass in klasses:
            coverage = klass['line_rate']
            if coverage < cover_threshold:
                cover_character = self.broken
            else:
                cover_character = self.honored

            if coverage > max_coverage and max_coverage < 100.0:
                max_coverage = coverage
                if max_coverage == 100.0:
                    print

            coverage = int(round(coverage, 0))
            progress = int(round(coverage / 100.0 * PROGRESS_SIZE, 0))
            offset = coverage == 0 and 2 or (coverage < 10 and 1 or 0)

            if coverage == 0 and not klass['uncovered_lines']:
                continue

            print ' %s %s%s\t%s%s%%%s %s' % (cover_character,
                                        write_blue(klass['name']),
                                        ' ' * (max_length - len(klass['name'])),
                                        '•' * progress,
                                        write_white((coverage > 0 and ' ' or '') + '{0:.2f}'.format(coverage)),
                                        ' ' * (PROGRESS_SIZE - progress + offset),
                                        self.get_uncovered_lines(klass['uncovered_lines']))

        print
        total_coverage = root['overall']
        progress = int(round(total_coverage / 100.0 * PROGRESS_SIZE, 0))
        print ' %s %s%s\t%s %s%%' % ((total_coverage >= cover_threshold) and self.honored or self.broken,
                                    write_blue('OVERALL'),
                                    ' ' * (max_length - len('OVERALL')),
                                    '•' * progress,
                                    write_white('{0:.2f}'.format(total_coverage)))

        print

    def get_uncovered_lines(self, uncovered_lines, number_of=3):
        if len(uncovered_lines) > number_of:
            template_str = []
            for i in range(number_of):
                template_str.append(uncovered_lines[i])
                if not i == number_of - 1:
                    template_str += ', '

            template_str.append(' and {0:d} more'.format(len(uncovered_lines) - number_of))

            return ''.join(template_str)

        return ', '.join(uncovered_lines)

