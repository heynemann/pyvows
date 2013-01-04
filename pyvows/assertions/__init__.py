#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''PyVows features an extensible assertion model with many useful functions, 
as well as error reporting.

It’s always best to use the most specific assertion functions when testing a 
value. You’ll get much better error reporting, because your intention is clearer.

This package contains all the code for PyVows assertions.  

Aren't they convenient?

'''


# pyVows testing engine
# https://github.com/heynemann/pyvows

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 Bernardo Heynemann heynemann@gmail.com

import pyvows.assertions.equality
import pyvows.assertions.numeric
import pyvows.assertions.function
import pyvows.assertions.like
import pyvows.assertions.boolean
import pyvows.assertions.classes
import pyvows.assertions.nullable
import pyvows.assertions.emptiness
import pyvows.assertions.inclusion
import pyvows.assertions.regexp
import pyvows.assertions.errors
import pyvows.assertions.length

