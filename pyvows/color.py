#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''PyVows' thin wrapper around the (3rd-party) `colorama` module.
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
        #   FIXME: Add Docstring
        def __getattr__(self, *args, **kwargs):
            return ""

    Fore  = NoColor()
    Style = NoColor()
