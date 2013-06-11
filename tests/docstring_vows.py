# -*- coding: utf-8 -*-

import types

from pyvows import Vows, expect


from pyvows import (
    __init__ as pyvows_init,
    __main__,
    async_topic,
    color,
    cli,
    core,
    runner,
    version)
from pyvows.reporting import (
    __init__ as reporting_init,
    common as reporting_common,
    coverage as reporting_coverage,
    profile as reporting_profile,
    test as reporting_test,
    xunit as reporting_xunit)

PYVOWS_MODULES = (
    # general modules
    pyvows_init,
    __main__,
    async_topic,
    color,
    cli,
    core,
    runner,
    version,
    # reporting
    reporting_init,
    reporting_common,
    reporting_coverage,
    reporting_profile,
    reporting_test,
    reporting_xunit,)


@Vows.assertion
def to_have_a_docstring(topic):
    '''Custom assertion.  Raises a AssertionError if `topic` has no
    docstring.

    '''
    if not hasattr(topic, '__doc__'):
        raise AssertionError('Expected topic({0}) to have a docstring', topic)


@Vows.batch
class EachPyvowsModule(Vows.Context):
    def topic(self):
        for mod in PYVOWS_MODULES:
            if isinstance(mod, types.ModuleType):
                yield mod

    def should_have_a_docstring(self, topic):
        expect(topic).to_have_a_docstring()
