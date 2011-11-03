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
    pattern = 'Pattern of vows files. (default: %(default)r).'
    progress = 'Indicates that progress ticks should be shown. (default: %(default)s).'
    cover = 'Indicates that coverage of code should be shown. (default: %(default)s).'
    cover_package = 'Package to verify coverage. May be specified many times. (default: all packages).'
    cover_omit = 'Path of file to exclude from coverage. May be specified many times. (default: no files).'
    cover_threshold = 'Coverage number below which coverage is considered failing. (default: %(default)s).'
    cover_report = 'Store the coverage report as the specified file. (default: %(default)s).'
    xunit_output = 'Enable XUnit output. (default: %(default)s).'
    xunit_file = 'Filename of the XUnit output (default: %(default)s).'
    no_color = 'Does not colorize the output. (default: %(default)s).'
    verbosity = 'Verbosity. Can be supplied multiple times to increase verbosity (default: -vv)'
    path = 'Directory to look for vows recursively. If a file is passed, the file will be the target for vows. (default: %(default)r).'
    profile = 'Prints the 10 slowest topics. (default: %(default)s).'

def __get_arguments():
    current_dir = os.curdir

    parser = argparse.ArgumentParser(description='Runs pyVows.')

    parser.add_argument('-p', '--pattern', default='*_vows.py', help=Messages.pattern)

    cover_group = parser.add_argument_group('coverage arguments')
    cover_group.add_argument('-c', '--cover', action="store_true", default=False, help=Messages.cover)
    cover_group.add_argument('-l', '--cover_package', action="append", default=[], help=Messages.cover_package)
    cover_group.add_argument('-o', '--cover_omit', action="append", default=[], help=Messages.cover_omit)
    cover_group.add_argument('-t', '--cover_threshold', default=80.0, type=float, help=Messages.cover_threshold)
    cover_group.add_argument('-r', '--cover_report', action="store", default=None, help=Messages.cover_report)

    xunit_group = parser.add_argument_group('xunit arguments')
    xunit_group.add_argument('-x', '--xunit_output', action="store_true", default=False, help=Messages.xunit_output)
    xunit_group.add_argument('-f', '--xunit_file', action="store", default="pyvows.xml", help=Messages.xunit_file)

    parser.add_argument('--no_color', action="store_true", default=False, help=Messages.no_color)
    parser.add_argument('--version', action='version', version='%(prog)s ' + version.to_str())
    parser.add_argument('-v', action='append_const', dest='verbosity', const=1, help=Messages.verbosity)
    parser.add_argument('--profile', action='store_true', dest='profile', default=False, help=Messages.profile)
    parser.add_argument('--progress', action='store_true', dest='progress', default=False, help=Messages.progress)

    parser.add_argument('path', default=current_dir, nargs='?', help=Messages.path)

    arguments = parser.parse_args()

    return arguments

def run(path, pattern, verbosity, progress):
    from pyvows.core import Vows
    from pyvows.reporting import VowsDefaultReporter

    Vows.gather(path, pattern)

    handle_success = progress and VowsDefaultReporter.handle_success or None
    handle_error = progress and VowsDefaultReporter.handle_error or None
    result = Vows.ensure(handle_success, handle_error)

    reporter = VowsDefaultReporter(result, verbosity)
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

    verbosity = len(arguments.verbosity) if arguments.verbosity else 2
    result, reporter = run(path, pattern, verbosity, arguments.progress)

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

    if arguments.profile:
        reporter.print_profile()

    sys.exit(result.errored_tests)

if __name__ == '__main__':
    main()
