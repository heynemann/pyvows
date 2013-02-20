# -*- coding: utf-8 -*-
'''This module is the foundation that allows users to write PyVows-style tests.
'''

# pyVows testing engine
# https://github.com/heynemann/pyvows

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 Bernardo Heynemann heynemann@gmail.com


class _AssertionNotFoundError(AttributeError):
    #   This is underscore-prefixed because it is not intended to be accessed
    #   directly. Instead, it should be accessed as
    #   `VowsAssertion.AssertionNotFoundError`. (See `pyvows.core`)

    def __init__(self, name):
        super(_AssertionNotFoundError, self).__init__(
            'Assertion "{name!s}" was not found!'.format(name=name))


class VowsAssertionError(AssertionError):
    '''Raised when a VowsAssertion returns `False`.'''

    def __init__(self, *args):
        if not isinstance(args[0], str):
            raise TypeError('VowsAssertionError instances must be created with a string as their first argument')
        if not len(args) >= 2:
            raise IndexError('VowsAssertionError must receive at least 2 arguments')

        self.raw_msg = args[0]

        if not self.raw_msg.endswith('.'):
            self.raw_msg += '.'

        self.args = tuple([repr(i) for i in args[1:]])

    def __repr__(self):
        return "VowsAssertionError('{0!s}',)".format(self)

    def __str__(self):
        return self.raw_msg.format(*self.args)

    def __unicode__(self):
        return self.__str__()


class VowsInternalError(Exception):
    '''Raised whenever PyVows internal code does something unexpected.'''

    def __init__(self, *args):
        if not isinstance(args[0], str):
            raise TypeError('VowsInternalError must be instantiated with a string as the first argument')
        if not len(args) >= 2:
            raise IndexError('VowsInternalError must receive at least 2 arguments')

    def __repr__(self):
        return "VowsInternalError('{0!s}',)".format(self)

    def __str__(self):
        msg = self.raw_msg.format(*self.args)
        msg += '''

        Help PyVows fix this issue!  Tell us what happened:

        https://github.com/heynemann/pyvows/issues/new

        '''
        return msg


    def __unicode__(self):
        return self.__str__()


