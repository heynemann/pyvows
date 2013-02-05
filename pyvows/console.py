#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''PyVows' main entry point.  Contains code for command-line I/O,
running tests, and the almighty `if __name__ == '__main__': main()`.

'''


# pyVows testing engine
# https://github.com/heynemann/pyvows

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 Bernardo Heynemann heynemann@gmail.com
from __future__ import division

import sys
import os
from os.path import isfile, split
import tempfile
import inspect

import argparse

try:
    from coverage import coverage
    COVERAGE_AVAILABLE = True
except ImportError:
    COVERAGE_AVAILABLE = False

from pyvows.color import *
from pyvows.reporting.xunit import XUnitReporter
from pyvows import version


class Messages(object):
    '''A simple container for command-line interface strings.'''

    summary   = 'Run PyVows tests.'
    path      = 'Directory to look for vows recursively. If a file is passed, the file will be the target for vows. (default: %(default)r).'
    pattern   = 'Pattern of vows files. (default: %(default)r)'
    verbosity = 'Verbosity. May be specified many times to increase verbosity (default: -vv)'
    cover           = 'Show the code coverage of tests. (default: %(default)s)'
    cover_package   = 'Verify coverage of %(metavar)s. May be specified many times. (default: all packages)'
    cover_omit      = 'Exclude %(metavar)s from coverage. May be specified many times. (default: no files)'
    cover_threshold = 'Coverage below %(metavar)s is considered a failure. (default: %(default)s)'
    cover_report    = 'Store coverage report as %(metavar)s. (default: %(default)r)'
    xunit_output    = 'Enable XUnit output. (default: %(default)s)'
    xunit_file      = 'Store XUnit output as %(metavar)s. (default: %(default)r)'
    profile           = 'Prints the 10 slowest topics. (default: %(default)s)'
    profile_threshold = 'Tests taking longer than %(metavar)s seconds are considered slow. (default: %(default)s)'
    no_color  = 'Turn off colorized output. (default: %(default)s)'
    progress  = 'Show progress ticks during testing. (default: %(default)s)'


def __get_arguments():
    '''Parses arguments from the command-line.'''

    current_dir = os.curdir

    #Easy underlining, if we ever need it in the future
    #uline   = lambda text: '\033[4m{0}\033[24m'.format(text)

    parser  = argparse.ArgumentParser(description     = Messages.summary)
    metavar = lambda metavar: '{0}{metavar}{0}'.format(Style.RESET_ALL, metavar=metavar.upper())

    parser.add_argument('-p', '--pattern', default='*_vows.py', help=Messages.pattern, metavar=metavar('pattern'))

    cover_group = parser.add_argument_group('Test Coverage')
    cover_group.add_argument('-c', '--cover',           action='store_true', default=False, help=Messages.cover)
    cover_group.add_argument('-l', '--cover_package',   action='append',     default=[],    help=Messages.cover_package, metavar=metavar('package'))
    cover_group.add_argument('-o', '--cover_omit',      action='append',     default=[],    help=Messages.cover_omit,    metavar=metavar('file'))
    cover_group.add_argument('-t', '--cover_threshold', type=float,          default=80.0,  help=Messages.cover_threshold, metavar=metavar('number'))
    cover_group.add_argument('-r', '--cover_report',    action='store',      default=None,  help=Messages.cover_report, metavar=metavar('file'))

    xunit_group = parser.add_argument_group('XUnit')
    xunit_group.add_argument('-x', '--xunit_output', action='store_true', default=False,        help=Messages.xunit_output)
    xunit_group.add_argument('-f', '--xunit_file',   action='store',      default='pyvows.xml', help=Messages.xunit_file, metavar=metavar('file'))

    profile_group = parser.add_argument_group('Profiling')
    profile_group.add_argument('--profile', action='store_true', dest='profile', default=False, help=Messages.profile)
    profile_group.add_argument('--profile_threshold', type=float,                default=0.1,   help=Messages.profile_threshold, metavar=metavar('num'))

    parser.add_argument('--no_color', action='store_true',                  default=False, help=Messages.no_color)
    parser.add_argument('--progress', action='store_true', dest='progress', default=False, help=Messages.progress)

    parser.add_argument('--version', action='version', version='%(prog)s {0}'.format(version.to_str()))
    parser.add_argument('-v',        action='append_const', dest='verbosity', const=1, help=Messages.verbosity)

    parser.add_argument('path', nargs='?', default=current_dir, help=Messages.path)

    arguments = parser.parse_args()

    return arguments

def run(path, pattern, verbosity, progress):
    #   FIXME: Add Docstring

    # they need to be imported here, else the no-color option won't work
    from pyvows.core import Vows
    from pyvows.reporting import VowsDefaultReporter

    Vows.gather(path, pattern)

    handle_success = progress and VowsDefaultReporter.handle_success or None
    handle_error = progress and VowsDefaultReporter.handle_error or None
    result = Vows.ensure(handle_success, handle_error)

    reporter = VowsDefaultReporter(result, verbosity)

    return result, reporter

def main():
    '''PyVows' runtime implementation.
    '''

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
        cov = coverage(source = arguments.cover_package,
                       omit   = arguments.cover_omit)
        cov.erase()
        cov.start()

    verbosity = len(arguments.verbosity) if arguments.verbosity else 2
    result, reporter = run(path, pattern, verbosity, arguments.progress)

    if result.successful and arguments.cover:
        if COVERAGE_AVAILABLE:
            cov.stop()

            print '\n' * 2

            xml = ''
            with tempfile.NamedTemporaryFile() as tmp:
                cov.xml_report(outfile=tmp.name)
                tmp.seek(0)
                xml = tmp.read()

            if arguments.cover_report:
                with open(arguments.cover_report, 'w') as report:
                    report.write(xml)

            arguments.cover_threshold /= 100.0
            reporter.print_coverage(xml, arguments.cover_threshold)

        else:

            print
            print yellow('WARNING: Cover disabled because coverage could not be found.')
            print yellow('Make sure it is installed and accessible.')
            print

    reporter.pretty_print()

    if arguments.xunit_output:
        xunit = XUnitReporter(result)
        xunit.write_report(arguments.xunit_file)

    if arguments.profile:
        reporter.print_profile(arguments.profile_threshold)

    sys.exit(result.errored_tests)

if __name__ == '__main__':
    main()
