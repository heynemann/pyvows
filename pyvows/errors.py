# -*- coding: utf-8 -*-
'''This module is the foundation that allows users to write PyVows-style tests.
'''

# pyVows testing engine
# https://github.com/heynemann/pyvows

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 Bernardo Heynemann heynemann@gmail.com


class VowsInternalError(Exception):
    '''Raised whenever PyVows internal code does something unexpected.'''

    def __init__(self, *args):
        if not isinstance(args[0], str):
            raise TypeError('VowsInternalError must be instantiated with a string as the first argument')
        if not len(args) >= 2:
            raise IndexError('VowsInternalError must receive at least 2 arguments')
        self.raw_msg = args[0]
        self.args = args[1:]

    def __str__(self):
        msg = self.raw_msg.format(*self.args)
        msg += '''

        Help PyVows fix this issue!  Tell us what happened:

        https://github.com/heynemann/pyvows/issues/new

        '''
        return msg
