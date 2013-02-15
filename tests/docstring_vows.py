# -*- coding: utf-8 -*-

import types

from pyvows         import Vows, expect


from pyvows import (
    __init__ as pyvows_init,
    __main__,
    async_topic,
    color,
    cli,
    core,
    runner,
    version)
from pyvows.assertions import (
    __init__    as assertions_init,
    emptiness   as assertions_emptiness,
    equality    as assertions_equality,
    inclusion   as assertions_inclusion,
    length      as assertions_length,
    like        as assertions_like)
from pyvows.assertions.types import (
    __init__    as assertions_types_init,
    boolean     as assertions_types_boolean,
    classes     as assertions_types_classes,
    errors      as assertions_types_errors,
    function    as assertions_types_function,
    nullable    as assertions_types_nullable,
    numeric     as assertions_types_numeric,
    regexp      as assertions_types_regexp)
from pyvows.errors  import (
    VowsAssertionError,)
from pyvows.reporting import (
    __init__    as reporting_init,
    common      as reporting_common,
    coverage    as reporting_coverage,
    profile     as reporting_profile,
    test        as reporting_test,
    xunit       as reporting_xunit)

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
    # assertion modules (general) 
    assertions_init,
    assertions_emptiness,
    assertions_equality,
    assertions_inclusion,
    assertions_length,
    assertions_like,
    # assertion modules (types)
    assertions_types_init,
    assertions_types_boolean,
    assertions_types_classes,
    assertions_types_errors,
    assertions_types_function,
    assertions_types_nullable,
    assertions_types_numeric,
    assertions_types_regexp,
    # errors
    VowsAssertionError,
    # reporting
    reporting_init,
    reporting_common,
    reporting_coverage,
    reporting_profile,
    reporting_test,
    reporting_xunit,)

@Vows.assertion
def to_have_a_docstring(topic):
    '''Custom assertion.  Raises a VowsAssertionError if `topic` has no 
    docstring.
    
    '''
    if not hasattr(topic, '__doc__'):
        raise VowsAssertionError('Expected topic({0}) to have a docstring', topic)
    

@Vows.batch
class EachPyvowsModule(Vows.Context):
    def topic(self):
        for mod in PYVOWS_MODULES:
            if isinstance(mod, types.ModuleType):
                yield mod
        
    def should_have_a_docstring(self, topic):
        expect(topic).to_have_a_docstring()