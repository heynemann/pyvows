#!/usr/bin/env python
# -*- coding: utf-8 -*-

# pyvows testing engine
# https://github.com/heynemann/pyvows

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 Bernardo Heynemann heynemann@gmail.com

import sys
import os
from os.path import join, abspath, splitext
import fnmatch
import glob

from pyvows.runner import VowsRunner
from pyvows.reporting import VowsDefaultReporter

def locate(pattern, root=os.curdir, recursive=True):
    root_path = os.path.abspath(root)

    if recursive:
        return_files = []
        for path, dirs, files in os.walk(root_path):
            for filename in fnmatch.filter(files, pattern):
                return_files.append(os.path.join(path, filename))
        return return_files
    else:
        return glob(join(root_path, pattern))

class Vows(object):
    contexts = {}

    class Context(object):
        pass

    class Assert(object):
        pass

    @staticmethod
    def batch(method):
        def method_name(*args, **kw):
            method(*args, **kw)

        Vows.contexts[method.__name__] = method

        return method_name

    @classmethod
    def assertion(cls, method):
        def method_name(*args, **kw):
            method(*args, **kw)
        @classmethod
        def exec_assertion(cls, *args, **kw):
            return method_name(*args, **kw)
        setattr(Vows.Assert, method.__name__, exec_assertion)
        return method_name

    @classmethod
    def ensure(cls):
        runner = VowsRunner(Vows.contexts, Vows.Context)

        result = runner.run()

        return result

    @classmethod
    def gather(cls, path):
        path = abspath(path)

        files = locate("*_vows.py", path)
        sys.path.insert(0, path)
        for module_path in files:
            module_name = splitext(module_path.replace(path, '').replace('/', '.').lstrip('.'))[0]
            __import__(module_name)

    @classmethod
    def run(cls):
        if sys.argv:
            path = sys.argv[-1]
        else:
            path = '.'

        Vows.gather(path)

        result = Vows.ensure()

        reporter = VowsDefaultReporter(result)

        reporter.pretty_print()

