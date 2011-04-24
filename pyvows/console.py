#!/usr/bin/env python
# -*- coding: utf-8 -*-

# pyvows testing engine
# https://github.com/heynemann/pyvows

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 Bernardo Heynemann heynemann@gmail.com

import os
from os.path import isfile, split
import argparse

from pyvows.reporting import VowsDefaultReporter
from pyvows.core import Vows

def __get_arguments():
    current_dir = os.curdir
    parser = argparse.ArgumentParser(description='Runs PyVows.')

    parser.add_argument('-p', '--pattern', default='*_vows.py', help='Pattern of vows files. Defaults to *_vows.py.')

    parser.add_argument('path', default=current_dir, nargs='?', help='Directory to look for vows recursively. If a file is passed, the file will be the target for vows. Defaults to current dir.')

    arguments = parser.parse_args()

    return arguments

def run(path, pattern):
    Vows.gather(path, pattern)

    result = Vows.ensure()

    reporter = VowsDefaultReporter(result)

    reporter.pretty_print()

def main():
    arguments = __get_arguments()

    path = arguments.path
    pattern = arguments.pattern

    if isfile(path):
        path, pattern = split(path)

    run(path, pattern)

if __name__ == '__main__':
    main()
