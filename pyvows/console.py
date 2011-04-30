#!/usr/bin/env python
# -*- coding: utf-8 -*-

# pyVows testing engine
# https://github.com/heynemann/pyvows

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 Bernardo Heynemann heynemann@gmail.com

import os
from os.path import isfile, split

try:
    import argparse
    ARGPARSE = True
except ImportError:
    ARGPARSE = False
    from optparse import OptionParser

from pyvows.reporting import VowsDefaultReporter
from pyvows.core import Vows

def __get_arguments():
    current_dir = os.curdir

    if ARGPARSE:
        parser = argparse.ArgumentParser(description='Runs pyVows.')

        parser.add_argument('-p', '--pattern', default='*_vows.py', help='Pattern of vows files. Defaults to *_vows.py.')

        parser.add_argument('path', default=current_dir, nargs='?', help='Directory to look for vows recursively. If a file is passed, the file will be the target for vows. Defaults to current dir.')

        arguments = parser.parse_args()
    else:
        parser = OptionParser()
        parser.add_option("-p", "--pattern", dest="pattern", default='*_vows.py', help='Pattern of vows files. Defaults to *_vows.py.')

        (options, args) = parser.parse_args()

        class Args(object):
            def __init__(self, pattern, path):
                self.pattern = pattern
                self.path = path

        arguments = Args(options.pattern, args[0] if args else None)

    return arguments

def run(path, pattern):
    Vows.gather(path, pattern)

    result = Vows.ensure(VowsDefaultReporter.handle_success, VowsDefaultReporter.handle_error)

    reporter = VowsDefaultReporter(result)

    reporter.pretty_print()

def main():
    arguments = __get_arguments()

    path = arguments.path
    pattern = arguments.pattern

    if path and isfile(path):
        path, pattern = split(path)
    if not path:
        path = os.curdir

    run(path, pattern)

if __name__ == '__main__':
    main()
