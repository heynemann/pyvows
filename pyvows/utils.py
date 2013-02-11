# -*- coding: utf-8 -*-
'''This module is the foundation that allows users to write PyVows-style tests.
'''

# pyVows testing engine
# https://github.com/heynemann/pyvows

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 Bernardo Heynemann heynemann@gmail.com

import fnmatch
import glob
import os

from pyvows.errors  import _AssertionNotFoundError, VowsAssertionError


def locate(pattern, root=os.curdir, recursive=True):
    '''Recursively locates test files when `pyvows` is run from the
    command line.
    
    '''
    root_path = os.path.abspath(root)

    if recursive:
        return_files = []
        for path, dirs, files in os.walk(root_path):
            for filename in fnmatch.filter(files, pattern):
                return_files.append(os.path.join(path, filename))
        return return_files
    else:
        return glob(os.path.join(root_path, pattern))


class VowsAssertion(object):
    '''Used by the `Vows` class for various assertion-related functionality.'''

    AssertionNotFoundError = _AssertionNotFoundError
    '''Raised when a `VowsAssertion` cannot be found.'''
    
    def __getattr__(self, name):
        if not hasattr(self, name):
            raise VowsAssertion.AssertionNotFoundError(name)
        return super(VowsAssertion, self).__getattr__(name)
