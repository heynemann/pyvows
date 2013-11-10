#!/usr/bin/env python
# -*- coding: utf-8 -*-

# pyvows testing engine
# https://github.com/heynemann/pyvows

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 Bernardo Heynemann heynemann@gmail.com

from pyvows import Vows, expect


@Vows.batch
class AssertionIsTrue(Vows.Context):

    class WhenBoolean(Vows.Context):
        def topic(self):
            return True

        def we_can_assert_it_is_true(self, topic):
            expect(topic).to_be_true()

    class WhenNumber(Vows.Context):
        def topic(self):
            return 1

        def we_can_assert_number_is_true(self, topic):
            expect(topic).to_be_true()

    class WhenString(Vows.Context):
        def topic(self):
            return 'some'

        def we_can_assert_string_is_true(self, topic):
            expect(topic).to_be_true()

    class WhenList(Vows.Context):
        def topic(self):
            return ['some']

        def we_can_assert_list_is_true(self, topic):
            expect(topic).to_be_true()

    class WhenDict(Vows.Context):
        def topic(self):
            return {'some': 'key'}

        def we_can_assert_dict_is_true(self, topic):
            expect(topic).to_be_true()

    class WhenWeGetAnError(Vows.Context):

        @Vows.capture_error
        def topic(self, last):
            expect(False).to_be_true()

        def we_get_an_understandable_message(self, topic):
            expect(topic).to_have_an_error_message_of("Expected topic(False) to be truthy")


@Vows.batch
class AssertionIsFalse(Vows.Context):

    class WhenBoolean(Vows.Context):
        def topic(self):
            return False

        def we_can_assert_it_is_false(self, topic):
            expect(topic).to_be_false()

    class WhenNumber(Vows.Context):
        def topic(self):
            return 0

        def we_can_assert_zero_is_false(self, topic):
            expect(topic).to_be_false()

    class WhenNone(Vows.Context):
        def topic(self):
            return None

        def we_can_assert_none_is_false(self, topic):
            expect(topic).to_be_false()

    class WhenString(Vows.Context):
        def topic(self):
            return ''

        def we_can_assert_empty_string_is_false(self, topic):
            expect(topic).to_be_false()

    class WhenList(Vows.Context):
        def topic(self):
            return []

        def we_can_assert_empty_list_is_false(self, topic):
            expect(topic).to_be_false()

    class WhenDict(Vows.Context):
        def topic(self):
            return {}

        def we_can_assert_empty_dict_is_false(self, topic):
            expect(topic).to_be_false()

    class WhenWeGetAnError(Vows.Context):

        @Vows.capture_error
        def topic(self):
            expect(True).to_be_false()

        def we_get_an_understandable_message(self, topic):
            expect(topic).to_have_an_error_message_of("Expected topic(True) to be falsy")
