#!/usr/bin/env python
# -*- coding: utf-8 -*-

# pyvows testing engine
# https://github.com/heynemann/pyvows

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 Bernardo Heynemann heynemann@gmail.com

import sys
import re
import traceback

from lxml import etree
from colorama import init, Fore, Style

from pyvows.core import VowsAssertionError

PROGRESS_SIZE = 50

# verbosity levels
V_VERBOSE = 3
V_NORMAL = 2
V_SILENT = 1

class VowsDefaultReporter(object):
    honored = Fore.GREEN + Style.BRIGHT + '✓' + Fore.RESET + Style.RESET_ALL
    broken = Fore.RED + Style.BRIGHT + '✗' + Fore.RESET + Style.RESET_ALL

    def __init__(self, result, verbosity):
        init(autoreset=True)
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
        if not self.result.contexts:
            print '%s%s No vows found! » 0 honored • 0 broken (0.0s)' % (
                self.tab * self.indent,
                self.broken,
            )
            return

        if self.verbosity >= V_VERBOSE or self.result.errored_tests:
            print
            print

        for context in self.result.contexts:
            self.print_context(context['name'], context)

        print
        print '%s%s OK » %d honored • %d broken (%.6fs)' % (
            self.tab * self.indent,
            self.honored if self.result.successful else self.broken,
            self.result.successful_tests,
            self.result.errored_tests,
            self.result.ellapsed_time
        )

    def humanized_print(self, msg, indentation=None):
        msg = self.under_split(msg)
        msg = self.camel_split(msg)
        print (indentation or (self.tab * self.indent)) + msg.capitalize()

    def format_traceback(self, traceback_list, indentation):
        def indent(msg):
            if msg.startswith('  File'):
                return msg.replace('\n ', '\n %s' % indentation)
            return msg

        return indentation.join(map(indent, traceback_list))

    def print_traceback(self, exc_type, exc_value, exc_traceback, indentation):
        if isinstance(exc_value, VowsAssertionError):
            exc_values_args = tuple(map(lambda arg: Fore.RESET + arg + Fore.RED, exc_value.args))
            error_msg = exc_value.msg % exc_values_args
        else:
            error_msg = unicode(exc_value)

        print indentation + Fore.RED + error_msg + Fore.RESET

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
                if self.verbosity >= V_VERBOSE:
                    self.humanized_print(VowsDefaultReporter.honored + ' ' + test['name'])
            else:
                self.humanized_print(VowsDefaultReporter.broken + ' ' + test['name'])

                if isinstance(test['topic'], Exception) and \
                   hasattr(test['context_instance'], 'topic_error'):
                    exc_type, exc_value, exc_traceback = test['context_instance'].topic_error
                    self.print_traceback(exc_type, exc_value, exc_traceback, indentation2)

                error = test['error']
                exc_type, exc_value, exc_traceback = error['type'], error['value'], error['traceback']

                self.print_traceback(exc_type, exc_value, exc_traceback, indentation2)

                if 'file' in test:
                    print indentation2 + Fore.RED + 'found in %s at line %s' % (test['file'], test['lineno']) + Fore.RESET
                    print

        for context in context['contexts']:
            self.print_context(context['name'], context)

        self.indent -= 1

    def print_profile(self):
        MAX_PATH_SIZE = 30
        topics = self.result.get_worst_topics(10)

        msg = "Slowest Topics"
        print ' ' + '=' * len(msg)
        print Fore.GREEN + Style.BRIGHT + ' ' + msg + Style.RESET_ALL + Fore.RESET
        print ' ' + '=' * len(msg)
        print

        print "       Ellapsed    Context File Path                 Context Name"
        for index, topic in enumerate(topics):
            name = self.under_split(topic['context'])
            name = self.camel_split(name)

            print Style.BRIGHT + ("%s#%02d%s    %.05fs    %s%s%" + str(MAX_PATH_SIZE) + "s%s%s    %s") % (
                    Fore.BLUE, 
                    index + 1, 
                    Fore.RESET, 
                    topic['ellapsed'], 
                    Style.DIM,
                    Fore.WHITE,
                    topic['path'][-MAX_PATH_SIZE:], 
                    Fore.RESET,
                    Style.BRIGHT,
                    name
            ) + Style.RESET_ALL

        print

    def print_coverage(self, xml, cover_threshold):
        write_blue = lambda msg: Fore.BLUE + Style.BRIGHT + str(msg) + Style.RESET_ALL + Fore.RESET
        write_white = lambda msg: Fore.WHITE + Style.BRIGHT + str(msg) + Style.RESET_ALL + Fore.RESET

        root = etree.fromstring(xml)

        klasses = root.xpath('//class')
        names = ['.'.join([klass.getparent().getparent().attrib['name'], klass.attrib['name']]) for klass in klasses]
        max_length = max([len(klass_name) for klass_name in names])

        print ' ' + '=' * len('Code Coverage')
        print Fore.GREEN + Style.BRIGHT + ' Code Coverage' + Style.RESET_ALL + Fore.RESET
        print ' ' + '=' * len('Code Coverage')
        print

        klasses = sorted(klasses, key=lambda klass: float(klass.attrib['line-rate']))

        max_coverage = 0
        for klass in klasses:
            package_name = klass.getparent().getparent().attrib['name']
            klass_name = '.'.join([package_name, klass.attrib['name']])
            coverage = float(klass.attrib['line-rate']) * 100
            if coverage < cover_threshold:
                cover_character = self.broken
            else:
                cover_character = self.honored

            if coverage > max_coverage and max_coverage < 100.0:
                max_coverage = coverage
                if max_coverage == 100.0:
                    print

            uncovered_lines = [line.attrib['number'] for line in klass.find('lines') if line.attrib['hits'] == '0']

            coverage = int(round(coverage, 0))
            progress = int(round(coverage / 100.0 * PROGRESS_SIZE, 0))
            offset = coverage == 0 and 2 or (coverage < 10 and 1 or 0)

            if coverage == 0 and not uncovered_lines:
                continue

            print ' %s %s%s\t%s%s%%%s %s' % (cover_character,
                                        write_blue(klass_name),
                                        ' ' * (max_length - len(klass_name)),
                                        '•' * progress,
                                        write_white((coverage > 0 and ' ' or '') + '%.2f' % coverage),
                                        ' ' * (PROGRESS_SIZE - progress + offset),
                                        self.get_uncovered_lines(uncovered_lines))

        print
        total_coverage = float(root.xpath('//coverage')[0].attrib['line-rate']) * 100
        progress = int(round(total_coverage / 100.0 * PROGRESS_SIZE, 0))
        print ' %s %s%s\t%s %s%%' % ((total_coverage >= cover_threshold) and self.honored or self.broken,
                                    write_blue('OVERALL'),
                                    ' ' * (max_length - len('OVERALL')),
                                    '•' * progress,
                                    write_white('%.2f' % total_coverage))

        print

    def get_uncovered_lines(self, uncovered_lines, number_of=3):
        if len(uncovered_lines) > number_of:
            template_str = []
            for i in range(number_of):
                template_str.append(uncovered_lines[i])
                if not i == number_of - 1:
                    template_str += ' ,'

            template_str.append(' and %d more' % (len(uncovered_lines) - number_of))

            return ''.join(template_str)

        return ', '.join(uncovered_lines)

