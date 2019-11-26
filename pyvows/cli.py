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
from __future__ import division, print_function

import argparse
import inspect
import os
from os.path import isfile, split
import sys
import tempfile

try:
    from coverage import coverage
    COVERAGE_AVAILABLE = True
except ImportError:
    COVERAGE_AVAILABLE = False

from pyvows.color import yellow, Style, Fore
from pyvows.reporting import VowsDefaultReporter
from pyvows.reporting.xunit import XUnitReporter
from pyvows import version

#-------------------------------------------------------------------------------------------------


class Messages(object):  # pragma: no cover
    '''A simple container for command-line interface strings.'''

    summary = 'Run PyVows tests.'

    path = 'Directory to look for vows recursively. If a file is passed,' + \
        'the file will be the target for vows. (default: %(default)r).'

    pattern = 'Pattern of vows files. (default: %(default)r)'
    verbosity = 'Verbosity. May be specified many times to increase verbosity (default: -vv)'
    cover = 'Show the code coverage of tests. (default: %(default)s)'
    cover_package = 'Verify coverage of %(metavar)s. May be specified many times. (default: all packages)'
    cover_omit = 'Exclude %(metavar)s from coverage. May be specified many times. (default: no files)'
    cover_threshold = 'Coverage below %(metavar)s is considered a failure. (default: %(default)s)'
    cover_report = 'Store coverage report as %(metavar)s. (default: %(default)r)'
    xunit_output = 'Enable XUnit output. (default: %(default)s)'
    xunit_file = 'Store XUnit output as %(metavar)s. (default: %(default)r)'
    exclude = 'Exclude tests and contexts that match regex-pattern %(metavar)s [Mutually exclusive with --include]'
    include = 'Include only tests and contexts that match regex-pattern %(metavar)s [Mutually exclusive with --exclude]'
    profile = 'Prints the 10 slowest topics. (default: %(default)s)'
    profile_threshold = 'Tests taking longer than %(metavar)s seconds are considered slow. (default: %(default)s)'
    no_color = 'Turn off colorized output. (default: %(default)s)'
    progress = 'Show progress ticks during testing. (default: %(default)s)'
    template = 'Print a PyVows test file template. (Disables testing)'
    capture_output = 'Capture stdout and stderr during test execution (default: %(default)s)'


class Parser(argparse.ArgumentParser):
    def __init__(self, description=Messages.summary, **kwargs):
        super(Parser, self).__init__(
            description=description,
            **kwargs)

        #Easy underlining, if we ever need it in the future
        #uline   = lambda text: '\033[4m{0}\033[24m'.format(text)
        metavar = lambda metavar: '{0}{metavar}{0}'.format(Style.RESET_ALL, metavar=metavar.upper())

        self.add_argument('-p', '--pattern', default='*_vows.py', help=Messages.pattern, metavar=metavar('pattern'))

        ### Filtering
        self.add_argument('-e', '--exclude', action='append', default=[], help=Messages.exclude, metavar=metavar('exclude'))
        self.add_argument('-i', '--include', action='append', default=[], help=Messages.include, metavar=metavar('include'))

        ### Coverage
        cover_group = self.add_argument_group('Test Coverage')
        cover_group.add_argument('-c', '--cover', action='store_true', default=False, help=Messages.cover)
        cover_group.add_argument(
            '-l', '--cover-package', action='append', default=[],
            help=Messages.cover_package, metavar=metavar('package')
        )
        cover_group.add_argument(
            '-o', '--cover-omit', action='append', default=[],
            help=Messages.cover_omit, metavar=metavar('file')
        )
        cover_group.add_argument(
            '-t', '--cover-threshold', type=float, default=80.0,
            help=Messages.cover_threshold, metavar=metavar('number')
        )
        cover_group.add_argument(
            '-r', '--cover-report', action='store', default=None,
            help=Messages.cover_report, metavar=metavar('file')
        )

        ### XUnit
        xunit_group = self.add_argument_group('XUnit')
        xunit_group.add_argument('-x', '--xunit-output', action='store_true', default=False, help=Messages.xunit_output)
        xunit_group.add_argument(
            '-f', '--xunit-file', action='store', default='pyvows.xml',
            help=Messages.xunit_file, metavar=metavar('file')
        )

        ### Profiling
        profile_group = self.add_argument_group('Profiling')
        profile_group.add_argument('--profile', action='store_true', dest='profile', default=False, help=Messages.profile)
        profile_group.add_argument(
            '--profile-threshold', type=float, default=0.1,
            help=Messages.profile_threshold, metavar=metavar('num')
        )

        ### Aux/Unconventional
        aux_group = self.add_argument_group('Utility')
        aux_group.add_argument('--template', action='store_true', dest='template', default=False, help=Messages.template)

        ### Misc
        self.add_argument('--no-color', action='store_true', default=False, help=Messages.no_color)
        self.add_argument('--progress', action='store_true', dest='progress', default=False, help=Messages.progress)
        self.add_argument('--version', action='version', version='%(prog)s {0}'.format(version.to_str()))
        self.add_argument('--capture-output', action='store_true', default=False, help=Messages.capture_output)
        self.add_argument('-v', action='append_const', dest='verbosity', const=1, help=Messages.verbosity)

        self.add_argument('path', nargs='?', default=os.curdir, help=Messages.path)


def run(path, pattern, verbosity, show_progress, exclusion_patterns=None, inclusion_patterns=None, capture_output=False):
    #   FIXME: Add Docstring

    # This calls Vows.run(), which then calls VowsRunner.run()

    # needs to be imported here, else the no-color option won't work
    from pyvows.core import Vows

    if exclusion_patterns:
        Vows.exclude(exclusion_patterns)
    if inclusion_patterns:
        Vows.include(inclusion_patterns)

    Vows.collect(path, pattern)

    on_success = show_progress and VowsDefaultReporter.on_vow_success or None
    on_error = show_progress and VowsDefaultReporter.on_vow_error or None
    result = Vows.run(on_success, on_error, capture_output)

    return result


def main():
    '''PyVows' runtime implementation.
    '''
    # needs to be imported here, else the no-color option won't work
    from pyvows.reporting import VowsDefaultReporter

    arguments = Parser().parse_args()

    if arguments.template:
        from pyvows.utils import template
        template()
        sys.exit()  # Exit after printing template, since it's
                    # supposed to be redirected from STDOUT by the user

    path, pattern = arguments.path, arguments.pattern
    if path and isfile(path):
        path, pattern = split(path)
    if not path:
        path = os.curdir

    if arguments.no_color:
        for color_name, value in inspect.getmembers(Fore):
            if not color_name.startswith('_'):
                setattr(Fore, color_name, '')

    if arguments.cover and COVERAGE_AVAILABLE:
        cov = coverage(source=arguments.cover_package,
                       omit=arguments.cover_omit)
        cov.erase()
        cov.start()

    verbosity = len(arguments.verbosity) if arguments.verbosity else 2
    result = run(
        path,
        pattern,
        verbosity,
        arguments.progress,
        exclusion_patterns=arguments.exclude,
        inclusion_patterns=arguments.include,
        capture_output=arguments.capture_output
    )
    reporter = VowsDefaultReporter(result, verbosity)

    # Print test results first
    reporter.pretty_print()

    # Print profile if necessary
    if arguments.profile:
        reporter.print_profile(arguments.profile_threshold)

    # Print coverage if necessary
    if result.successful and arguments.cover:
        # if coverage was requested, but unavailable, warn the user
        if not COVERAGE_AVAILABLE:
            print()
            print(yellow('WARNING: Cover disabled because coverage could not be found.'))
            print(yellow('Make sure it is installed and accessible.'))
            print()

        # otherwise, we're good
        else:
            cov.stop()
            xml = ''

            try:
                with tempfile.NamedTemporaryFile() as tmp:
                    cov.xml_report(outfile=tmp.name)
                    tmp.seek(0)
                    xml = tmp.read()
            except Exception:
                err = sys.exc_info()[1]
                print("Could not run coverage. Error: %s" % err)

            if xml:
                if arguments.cover_report:
                    with open(arguments.cover_report, 'wb') as report:
                        report.write(xml)

                arguments.cover_threshold /= 100.0
                reporter.print_coverage(xml, arguments.cover_threshold)

    # Write XUnit if necessary
    if arguments.xunit_output:
        xunit = XUnitReporter(result)
        xunit.write_report(arguments.xunit_file)

    sys.exit(result.errored_tests)

if __name__ == '__main__':
    main()
