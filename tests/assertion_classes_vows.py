#!/usr/bin/env python
# -*- coding: utf-8 -*-

# pyvows testing engine
# https://github.com/heynemann/pyvows

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 Bernardo Heynemann heynemann@gmail.com

from pyvows import Vows, expect


class SomeClass(object): pass
class OtherClass(object): pass

@Vows.batch
class AssertionIsInstance(Vows.Context):
    def topic(self):
        return SomeClass()

    class WhenIsInstance(Vows.Context):

        def we_get_an_instance_of_someclass(self, topic):
            expect(topic).to_be_instance_of(SomeClass)

        class WhenWeGetAnError(Vows.Context):

            def topic(self, last):
                expect(2).to_be_instance_of(str)

            def we_get_an_understandable_message(self, topic):
                expect(topic).to_have_an_error_message_of(
                        "Expected topic(2) to be an instance of %s, but it was a %s." % (str(str), str(int)))

    class WhenIsNotInstance(Vows.Context):

        def we_do_not_get_an_instance_of_otherclass(self, topic):
            expect(topic).Not.to_be_instance_of(OtherClass)

        class WhenWeGetAnError(Vows.Context):

            def topic(self, last):
                expect(2).not_to_be_instance_of(int)

            def we_get_an_understandable_message(self, topic):
                expect(topic).to_have_an_error_message_of(
                        "Expected topic(2) not to be an instance of %s." % str(int))


