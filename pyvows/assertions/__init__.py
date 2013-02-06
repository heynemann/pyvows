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

from pyvows.assertions.emptiness import *
from pyvows.assertions.equality import *
from pyvows.assertions.inclusion import *
from pyvows.assertions.length import *
from pyvows.assertions.like import *

from pyvows.assertions.types.numeric import *
from pyvows.assertions.types.function import *
from pyvows.assertions.types.boolean import *
from pyvows.assertions.types.classes import *
from pyvows.assertions.types.file import *
from pyvows.assertions.types.nullable import *
from pyvows.assertions.types.regexp import *
from pyvows.assertions.types.errors import *

