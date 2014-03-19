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

from xml.etree import ElementTree as etree

from pyvows.color import yellow, blue, dim, white, bold
from pyvows.reporting.common import (
    PROGRESS_SIZE,
    VowsReporter,)


class VowsCoverageReporter(VowsReporter):
    '''A VowsReporter which prints the code coverage of tests.'''

    def get_uncovered_lines(self, uncovered_lines, max_num=3):
        '''Searches for untested lines of code.  Returns a string
        listing the line numbers.

        If the number of uncovered lines is greater than `max_num`, this will
        only explicitly list the first `max_num` uncovered lines, followed
        by ' and ## more' (where '##' is the total number of additional
        uncovered lines.

        '''
        if len(uncovered_lines) > max_num:
            template_str = []
            for i in range(max_num):
                line_num = uncovered_lines[i]
                template_str.append(line_num)
                if i is not (max_num - 1):
                    template_str.append(', ')

            template_str.append(
                ', and {num_more_uncovered:d} more'.format(
                    num_more_uncovered=len(uncovered_lines) - max_num
                ))

            return yellow(''.join(template_str))

        return yellow(', '.join(uncovered_lines))

    def parse_coverage_xml(self, xml):
        '''Reads `xml` for code coverage statistics, and returns the
        dict `result`.
        '''
        _coverage = lambda x: float(x.attrib['line-rate'])

        result = {}
        root = etree.fromstring(xml)
        result['overall'] = _coverage(root)
        result['classes'] = []

        for package in root.findall('.//package'):
            package_name = package.attrib['name']
            for klass in package.findall('.//class'):
                result['classes'].append({
                    'name': '.'.join([package_name, klass.attrib['name']]),
                    'line_rate': _coverage(klass),
                    'uncovered_lines': [line.attrib['number']
                                        for line in klass.find('lines')
                                        if line.attrib['hits'] == '0']
                })

        return result

    #-------------------------------------------------------------------------
    #   Printing (Coverage)
    #-------------------------------------------------------------------------
    def print_coverage(self, xml, cover_threshold):
        '''Prints code coverage statistics for your tests.'''
        print(self.header('Code Coverage'))

        root = self.parse_coverage_xml(xml)
        klasses = sorted(root['classes'], key=lambda klass: klass['line_rate'])
        max_length = max([len(klass['name']) for klass in root['classes']])
        max_coverage = 0

        for klass in klasses:
            coverage = klass['line_rate']

            if coverage < cover_threshold:
                cover_character = VowsReporter.BROKEN
            else:
                cover_character = VowsReporter.HONORED

            if 100.0 < max_coverage < coverage:
                max_coverage = coverage
                if max_coverage == 100.0:
                    print()

            coverage = coverage
            progress = int(coverage * PROGRESS_SIZE)
            offset = None

            if coverage == 0.000:
                offset = 2
            elif 0.000 < coverage < 0.1000:
                offset = 1
            else:
                offset = 0

            if coverage == 0.000 and not klass['uncovered_lines']:
                continue

            print(self.format_class_coverage(
                cover_character=cover_character,
                klass=klass['name'],
                space1=' ' * (max_length - len(klass['name'])),
                progress=progress,
                coverage=coverage,
                space2=' ' * (PROGRESS_SIZE - progress + offset),
                lines=self.get_uncovered_lines(klass['uncovered_lines']),
                cover_threshold=cover_threshold))

        print()

        total_coverage = root['overall']
        cover_character = VowsReporter.HONORED if (total_coverage >= cover_threshold) else VowsReporter.BROKEN
        progress = int(total_coverage * PROGRESS_SIZE)

        print(self.format_overall_coverage(cover_character, max_length, progress, total_coverage))
        print()

    def format_class_coverage(self, cover_character, klass, space1, progress, coverage, space2, lines, cover_threshold):
        '''Accepts coverage data for a class and returns a formatted string (intended for
        humans).
        '''
        #   FIXME:
        #       Doesn't this *actually* print coverage for a module, and not a class?

        # preprocess raw data...
        klass = klass.lstrip('.')
        klass = blue(klass)

        MET_THRESHOLD = coverage >= cover_threshold

        coverage = '{prefix}{coverage:.1%}'.format(
            prefix=' ' if (coverage > 0.000) else '',
            coverage=coverage
        )

        if MET_THRESHOLD:
            coverage = bold(coverage)

        coverage = white(coverage)

        # ...then format
        return ' {0} {klass}{space1}\t{progress}{coverage}{space2} {lines}'.format(
            # TODO:
            #   * remove manual spacing, use .format() alignment
            cover_character,
            klass=klass,
            space1=space1,
            progress=dim('•' * progress),
            coverage=coverage,
            space2=space2,
            lines=lines
        )

    def format_overall_coverage(self, cover_character, max_length, progress, total_coverage):
        '''Accepts overall coverage data and returns a formatted string (intended for
        humans).
        '''

        # preprocess raw data
        overall = blue('OVERALL')
        overall = bold(overall)
        space = ' ' * (max_length - len('OVERALL'))
        total = '{total_coverage:.1%}'.format(total_coverage=total_coverage)
        total = white(bold(total))

        # then format
        return ' {0} {overall}{space}\t{progress} {total}'.format(
            cover_character,
            overall=overall,
            space=space,
            progress='•' * progress,
            total=total)
