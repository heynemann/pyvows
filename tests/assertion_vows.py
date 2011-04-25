#!/usr/bin/env python
# -*- coding: utf-8 -*-

# pyvows testing engine
# https://github.com/heynemann/pyvows

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 Bernardo Heynemann heynemann@gmail.com

from pyvows import Vows

@Vows.batch
class Assertion(Vows.Context):

    class Equal(Vows.Context):

        def topic(self):
            return "test"

        def WeGetTest(self, topic):
            Vows.Assert.are_equal('test', topic)

        def WeDoNotGetElse(self, topic):
            Vows.Assert.not_are_equal('else', topic)

    class IsNumeric(Vows.Context):

        class WhenItIsANumber(Vows.Context):
            def topic(self):
                return 42

            def WeAssertItIsNumeric(self, topic):
                Vows.Assert.is_numeric(topic)

        class WhenItIsNotANumber(Vows.Context):
            def topic(self):
                return 'test'

            def WeAssertItIsNotNumeric(self, topic):
                Vows.Assert.not_is_numeric(topic)

    class IsFunction(Vows.Context):

        class WhenItIsAFunction(Vows.Context):
            def topic(self):
                def my_func():
                    pass
                return my_func

            def WeAssertItIsAFunction(self, topic):
                Vows.Assert.is_function(topic)

        class WhenItIsANumber(Vows.Context):
            def topic(self):
                return 42

            def WeAssertItIsNotAFunction(self, topic):
                Vows.Assert.not_is_function(topic)

    class IsLike(Vows.Context):

        class WhenItIsAString(Vows.Context):
            def topic(self):
                return " some StRinG with RanDoM CaSe And  Weird   SpACING   "

            def WeAssertItIsLikeOtherString(self, topic):
                Vows.Assert.are_alike('some string with random case and weird spacing', topic)

            def WeAssertItIsNotLikeOtherString(self, topic):
                Vows.Assert.not_are_alike('some other string', topic)

        class WhenItIsANumber(Vows.Context):
            def topic(self):
                return 42

            def WeAssertItIsNotLikeAString(self, topic):
                Vows.Assert.not_are_alike('42', topic)

            def WeAssertItIsLike42(self, topic):
                Vows.Assert.are_alike(42, topic)

            def WeAssertItIsLike42Float(self, topic):
                Vows.Assert.are_alike(42.0, topic)

            def WeAssertItIsLike42Long(self, topic):
                Vows.Assert.are_alike(long(42), topic)

            def WeAssertItIsNotLike41(self, topic):
                Vows.Assert.not_are_alike(41, topic)
