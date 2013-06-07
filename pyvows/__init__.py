# -*- coding: utf-8 -*-
'''PyVows is a Behavior-Driven Development framework for Python.  (And and it
is **fast**!)

---

PyVows runs tests asynchronously.  This makes tests which target I/O
run much faster, by running them concurrently. A faster test suite gets
run more often, thus improving the feedback cycle.

PyVows is inspired by Vows, a BDD framework for Node.js.

----

You typically shouldn't need to import any specific modules from the `pyvows`
package.  Normal use is:

    from pyvows import Vows, expect

----

To learn more, check out:   http://pyvows.org

'''


# pyVows testing engine
# https://github.com/heynemann/pyvows
#
# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 Bernardo Heynemann heynemann@gmail.com

# flake8: noqa

#-------------------------------------------------------------------------------------------------

try:
    from preggy import expect
except:
    pass

try:
    from pyvows.core import Vows, expect
except ImportError:
    pass
