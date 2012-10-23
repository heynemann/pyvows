#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''PyVows' version number.
'''


# pyVows testing engine
# https://github.com/heynemann/pyvows

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 Bernardo Heynemann heynemann@gmail.com

__version__ = (1, 1, 0)

def to_str():
    return '.'.join([str(item) for item in __version__])
