#!/usr/bin/env python
# -*- coding: utf-8 -*-

# pyVows testing engine
# https://github.com/heynemann/pyvows

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 Bernardo Heynemann heynemann@gmail.com

import sys
import os
from os.path import isfile, split
import tempfile
import inspect

import argparse
from colorama import init, Fore

try:
    from coverage import coverage
    from lxml import etree
    COVERAGE_AVAILABLE = True
except ImportError:
    COVERAGE_AVAILABLE = False

from pyvows.xunit import XUnitReporter
from pyvows import version


class Messages(object):
    pattern = 'Pattern of vows files. Defaults to *_vows.py.'
    cover = 'Indicates that coverage of code should be shown. Defaults to True.'
    path = 'Directory to look for vows recursively. If a file is passed, the file will be the target for vows. Defaults to current dir.'
    xunit_output = 'Enable XUnit output.'
    xunit_file = 'Filename of the XUnit output (default: pyvows.xml).'
    cover_package = 'Package to verify coverage. May be specified many times. Defaults to all packages.'
    cover_omit = 'Path of file to exclude from coverage. May be specified many times. Defaults to no files.'
    cover_threshold = 'Coverage number below which coverage is considered failing. Defaults to 80.0.'
    cover_report = 'Store the coverage report as the specified file.'
    no_color = 'Does not colorize the output.'

def __get_arguments():
    current_dir = os.curdir

    parser = argparse.ArgumentParser(description='Runs pyVows.')

    parser.add_argument('-p', '--pattern', default='*_vows.py', help=Messages.pattern)
    parser.add_argument('-c', '--cover', action="store_true", default=False, help=Messages.cover)
    parser.add_argument('-l', '--cover_package', action="append", default=[], help=Messages.cover_package)
    parser.add_argument('-o', '--cover_omit', action="append", default=[], help=Messages.cover_omit)
    parser.add_argument('-t', '--cover_threshold', default=80.0, type=float, help=Messages.cover_threshold)
    parser.add_argument('-r', '--cover_report', action="store", default=None, help=Messages.cover_report)
    parser.add_argument('-x', '--xunit_output', action="store_true", default=False, help=Messages.xunit_output)
    parser.add_argument('-f', '--xunit_file', action="store", default="pyvows.xml", help=Messages.xunit_file)
    parser.add_argument('--no_color', action="store_true", default=False, help=Messages.no_color)
    parser.add_argument('--version', action='version', version='%(prog)s ' + version.to_str())

    parser.add_argument('path', default=current_dir, nargs='?', help=Messages.path)

    arguments = parser.parse_args()

    return arguments

def run(path, pattern):
    from pyvows.core import Vows
    from pyvows.reporting import VowsDefaultReporter

    Vows.gather(path, pattern)

    result = Vows.ensure(VowsDefaultReporter.handle_success, VowsDefaultReporter.handle_error)

    reporter = VowsDefaultReporter(result)

    reporter.pretty_print()

    return result, reporter

def main():
    arguments = __get_arguments()

    path = arguments.path
    pattern = arguments.pattern

    if path and isfile(path):
        path, pattern = split(path)
    if not path:
        path = os.curdir

    if arguments.no_color:
        for color_name, value in inspect.getmembers(Fore):
            if not color_name.startswith('_'):
                setattr(Fore, color_name, '')


    if arguments.cover and COVERAGE_AVAILABLE:
        cov = coverage(source=arguments.cover_package, omit=arguments.cover_omit)
        cov.erase()
        cov.start()

    result, reporter = run(path, pattern)

    if arguments.cover:
        if COVERAGE_AVAILABLE:
            cov.stop()

            print
            print

            xml = ''
            with tempfile.NamedTemporaryFile() as tmp:
                cov.xml_report(outfile=tmp.name)
                tmp.seek(0)
                xml = tmp.read()

            if arguments.cover_report:
                with open(arguments.cover_report, 'w') as report:
                    report.write(xml)

            reporter.print_coverage(xml, arguments.cover_threshold)

        else:

            init(autoreset=True)
            print
            print Fore.YELLOW + "WARNING: Cover disabled because coverage or lxml could not be found."
            print Fore.YELLOW + "Make sure both are installed and accessible"
            print

    if arguments.xunit_output:
        xunit = XUnitReporter(result, arguments.xunit_file)
        xunit.write_report()

    sys.exit(result.errored_tests)

if __name__ == '__main__':
    main()
