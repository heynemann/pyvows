# -*- coding: utf-8 -*-

from pyvows import Vows, expect, VowsAssertionError

from pyvows import (
    __init__ as pyvows_init,
    __main__,
    async_topic,
    color,
    console,
    core,
    reporting,
    runner,
    version,
    xunit)

from pyvows.assertions import (
    __init__ as assertion_init,
    boolean,
    classes,
    emptiness,
    equality,
    errors,
    function,
    inclusion,
    length,
    like,
    nullable,
    numeric,
    regexp)

PYVOWS_MODULES = (
    # general modules
    pyvows_init,
    __main__,
    async_topic,
    color,
    console,
    core,
    reporting,
    runner,
    version,
    xunit,
    
    # assertion modules
    assertion_init,
    boolean,
    classes,
    emptiness,
    equality,
    errors,
    function,
    inclusion,
    length,
    like,
    nullable,
    numeric,
    regexp)

@Vows.assertion
def to_have_a_docstring(topic):
    '''Custom assertion.  Raises a VowsAssertionError if the topic has no docstring.'''
    
    if not hasattr(topic, '__doc__'):
        raise VowsAssertionError('Expected topic(%s) to have a docstring', topic)
    

@Vows.batch
class EachPyvowsModule(Vows.Context):
    def topic(self):
        for mod in PYVOWS_MODULES:
            yield mod
        
    def should_have_a_docstring(self, topic):
        expect(topic).to_have_a_docstring()