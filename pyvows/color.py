#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''PyVows' support for color-printing to the terminal.

Currently, just a thin wrapper around the (3rd-party) `colorama` module.
'''


# pyvows testing engine
# https://github.com/heynemann/pyvows

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 Bernardo Heynemann heynemann@gmail.com

try:
    from colorama import init, Fore, Style
    init(autoreset=True)
except ImportError:
    class NoColor(object):
        '''When Python can't import `colorama`, this stand-in class prevents
        other parts of PyVows from throwing errors when attempting to print
        in color.
        '''
        def __getattr__(self, *args, **kwargs):
            return ""

    Fore  = NoColor()
    Style = NoColor()
