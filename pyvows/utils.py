# -*- coding: utf-8 -*-
'''This module is the foundation that allows users to write PyVows-style tests.
'''

# pyVows testing engine
# https://github.com/heynemann/pyvows

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 Bernardo Heynemann heynemann@gmail.com


from pyvows.errors  import _AssertionNotFoundError, VowsAssertionError


class VowsAssertion(object):
    '''Used by the `Vows` class for various assertion-related functionality.'''

    AssertionNotFoundError = _AssertionNotFoundError
    '''Raised when a `VowsAssertion` cannot be found.'''
    
    def __getattr__(self, name):
        if not hasattr(self, name):
            raise VowsAssertion.AssertionNotFoundError(name)
        return super(VowsAssertion, self).__getattr__(name)
