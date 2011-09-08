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

class VowsDefaultReporter(object):
    honored = Fore.GREEN + Style.BRIGHT + '✓' + Fore.RESET + Style.RESET_ALL
    broken = Fore.RED + Style.BRIGHT + '✗' + Fore.RESET + Style.RESET_ALL

    def __init__(self, result):
        init(autoreset=True)
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
        print
        print
        if not self.result:
            print ' %s No vows found! » 0 honored • 0 broken (0.0s)' % self.broken
            return

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

    def humanized_print(self, msg):
        msg = self.under_split(msg)
        msg = self.camel_split(msg)
        print (self.tab * self.indent) + msg.capitalize()

    def format_traceback(self, traceback_list, indentation):
        def indent(msg):
            if msg.startswith('  File'):
                return msg.replace('\n ', '\n %s' % indentation)
            return msg

        return map(indent, traceback_list)

    def print_context(self, name, context):
        self.humanized_print(name)
        self.indent += 1

        indentation2 = self.tab * (self.indent + 2)

        for test in context['tests']:
            if test['succeeded']:
                self.humanized_print(VowsDefaultReporter.honored + ' ' + test['name'])
            else:
                self.humanized_print(VowsDefaultReporter.broken + ' ' + test['name'])

                if isinstance(test['topic'], Exception) and \
                   'context_instance' in test and \
                   hasattr(test['context_instance'], 'topic_error') and \
                   not isinstance(test['context_instance'].topic_error[1], AssertionError):
                    exc_type, exc_value, exc_traceback = test['context_instance'].topic_error
                else:
                    error = test['error']
                    exc_type, exc_value, exc_traceback = error['type'], error['value'], error['traceback']

                if isinstance(exc_value, VowsAssertionError):
                    exc_values_args = tuple(map(lambda arg: Fore.RESET + arg + Fore.RED, exc_value.args))
                    error_msg = exc_value.msg % exc_values_args
                else:
                    error_msg = unicode(exc_value)

                traceback_msg = traceback.format_exception(exc_type, exc_value, exc_traceback)
                traceback_msg = self.format_traceback(traceback_msg, indentation2)
                traceback_msg = indentation2.join(traceback_msg)

                print indentation2 + Fore.RED + error_msg + Fore.RESET
                print
                print indentation2 + traceback_msg

                if 'file' in test:
                    print indentation2 + Fore.RED + '(found in %s at line %s)' % (test['file'], test['lineno']) + Fore.RESET
                    print

        for context in context['contexts']:
            self.print_context(context['name'], context)

        self.indent -= 1

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

