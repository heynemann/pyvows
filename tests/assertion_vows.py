#!/usr/bin/env python
# -*- coding: utf-8 -*-

# pyvows testing engine
# https://github.com/heynemann/pyvows

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 Bernardo Heynemann heynemann@gmail.com

from pyvows import Vows

class SomeClass(object): pass
class OtherClass(object): pass

Assert = Vows.Assert

@Vows.batch
class Assertion(Vows.Context):

    class Equal(Vows.Context):

        def topic(self):
            return "test"

        def we_get_test(self, topic):
            Assert.are_equal('test', topic)

        def we_do_not_get_else(self, topic):
            Assert.not_are_equal('else', topic)

    class IsInstance(Vows.Context):
        def topic(self):
            return SomeClass()

        def we_get_an_instance_of_someclass(self, topic):
            Assert.is_instance_of(SomeClass, topic)

        def we_do_not_get_an_instance_of_otherclass(self, topic):
            Assert.not_is_instance_of(OtherClass, topic)

    class IsEmpty(Vows.Context):
        class WhenEmpty(Vows.Context):
            class WhenString(Vows.Context):
                def topic(self):
                    return ''

                def we_get_an_empty_string(self, topic):
                    Assert.is_empty(topic)

            class WhenList(Vows.Context):
                def topic(self):
                    return []

                def we_get_an_empty_list(self, topic):
                    Assert.is_empty(topic)

            class WhenTuple(Vows.Context):
                def topic(self):
                    return tuple([])

                def we_get_an_empty_tuple(self, topic):
                    Assert.is_empty(topic)

            class WhenDict(Vows.Context):
                def topic(self):
                    return {}

                def we_get_an_empty_dict(self, topic):
                    Assert.is_empty(topic)

        class WhenNotEmpty(Vows.Context):
            class WhenString(Vows.Context):
                def topic(self):
                    return 'whatever'

                def we_get_a_not_empty_string(self, topic):
                    Assert.is_not_empty(topic)

            class WhenList(Vows.Context):
                def topic(self):
                    return ['something']

                def we_get_a_not_empty_list(self, topic):
                    Assert.is_not_empty(topic)

            class WhenTuple(Vows.Context):
                def topic(self):
                    return tuple(['something'])

                def we_get_a_not_empty_tuple(self, topic):
                    Assert.is_not_empty(topic)

            class WhenDict(Vows.Context):
                def topic(self):
                    return {"key": "value"}

                def we_get_a_not_empty_dict(self, topic):
                    Assert.is_not_empty(topic)

    class IsNull(Vows.Context):

        class WhenItIsNull(Vows.Context):
            def topic(self):
                return None

            def we_get_to_check_for_nullability_in_None(self, topic):
                Assert.is_null(topic)

        class WhenItIsNotNull(Vows.Context):
            def topic(self):
                return "something"

            def we_see_string_is_not_null(self, topic):
                Assert.is_not_null(topic)

    class IsTrue(Vows.Context):

        def topic(self):
            return True

        def we_can_assert_it_is_true(self, topic):
            Assert.is_true(topic)

        def we_can_assert_number_is_true(self, topic):
            Assert.is_true(1)

        def we_can_assert_string_is_true(self, topic):
            Assert.is_true('some')

        def we_can_assert_list_is_true(self, topic):
            Assert.is_true(['some'])

        def we_can_assert_empty_dict_is_true(self, topic):
            Assert.is_true({'some': 'key'})

    class IsFalse(Vows.Context):

        def topic(self):
            return False

        def we_can_assert_it_is_false(self, topic):
            Assert.is_false(topic)

        def we_can_assert_zero_is_false(self, topic):
            Assert.is_false(0)

        def we_can_assert_none_is_false(self, topic):
            Assert.is_false(None)

        def we_can_assert_empty_string_is_false(self, topic):
            Assert.is_false('')

        def we_can_assert_empty_list_is_false(self, topic):
            Assert.is_false('')

        def we_can_assert_empty_dict_is_false(self, topic):
            Assert.is_false({})

    class IsNumeric(Vows.Context):

        class WhenItIsANumber(Vows.Context):
            def topic(self):
                return 42

            def we_assert_it_is_numeric(self, topic):
                Assert.is_numeric(topic)

        class WhenItIsNotANumber(Vows.Context):
            def topic(self):
                return 'test'

            def we_assert_it_is_not_numeric(self, topic):
                Assert.not_is_numeric(topic)

    class IsFunction(Vows.Context):

        class WhenItIsAFunction(Vows.Context):
            def topic(self):
                def my_func():
                    pass
                return my_func

            def we_assert_it_is_a_function(self, topic):
                Assert.is_function(topic)

        class WhenItIsANumber(Vows.Context):
            def topic(self):
                return 42

            def we_assert_it_is_not_a_function(self, topic):
                Assert.not_is_function(topic)

    class Regexp(Vows.Context):
        def topic(self):
            return "some string"

        def we_assert_it_matches_regexp(self, topic):
            Assert.match(r'^some.+$', topic)

        def we_assert_it_does_not_match_regexp(self, topic):
            Assert.not_match(r'^other.+$', topic)

    class HasThrown(Vows.Context):
        def topic(self):
            raise ValueError("some bogus error")

        def we_can_see_it_was_a_value_error(self, topic):
            Assert.has_errored_with(ValueError, topic)

        def we_can_see_that_is_has_error_message_of(self, topic):
            Assert.has_error_message_of("some bogus error", topic)

    class Length(Vows.Context):
        class WithString(Vows.Context):
            def topic(self):
                return "some string"

            def we_can_see_it_has_11_characters(self, topic):
                Assert.length(11, topic)

        class WithList(Vows.Context):
            def topic(self):
                return ["some", "list"]

            def we_can_see_it_has_2_items(self, topic):
                Assert.length(2, topic)

        class WithTuple(Vows.Context):
            def topic(self):
                return tuple(["some", "list"])

            def we_can_see_it_has_2_items(self, topic):
                Assert.length(2, topic)
        class WithDict(Vows.Context):
            def topic(self):
                return { "some": "item", "other": "item" }

            def we_can_see_it_has_2_items(self, topic):
                Assert.length(2, topic)
 
    class Include(Vows.Context):

        class WhenItIsAString(Vows.Context):
            def topic(self):
                return "some big string"

            def we_can_find_some(self, topic):
                Assert.include('some', topic)

            def we_can_find_big(self, topic):
                Assert.include('big', topic)

            def we_can_find_string(self, topic):
                Assert.include('string', topic)

            def we_cant_find_else(self, topic):
                Assert.not_include('else', topic)

        class WhenItIsAList(Vows.Context):
            def topic(self):
                return ["some", "big", "string"]

            def we_can_find_some(self, topic):
                Assert.include('some', topic)

            def we_can_find_big(self, topic):
                Assert.include('big', topic)

            def we_can_find_string(self, topic):
                Assert.include('string', topic)

            def we_cant_find_else(self, topic):
                Assert.not_include('else', topic)

        class WhenItIsATuple(Vows.Context):
            def topic(self):
                return tuple(["some", "big", "string"])

            def we_can_find_some(self, topic):
                Assert.include('some', topic)

            def we_can_find_big(self, topic):
                Assert.include('big', topic)

            def we_can_find_string(self, topic):
                Assert.include('string', topic)

            def we_cant_find_else(self, topic):
                Assert.not_include('else', topic)

        class WhenItIsADict(Vows.Context):
            def topic(self):
                return {"some": 1, "big": 2, "string": 3}

            def we_can_find_some(self, topic):
                Assert.include('some', topic)

            def we_can_find_big(self, topic):
                Assert.include('big', topic)

            def we_can_find_string(self, topic):
                Assert.include('string', topic)

            def we_cant_find_else(self, topic):
                Assert.not_include('else', topic)

    class IsLike(Vows.Context):

        class WhenItIsAString(Vows.Context):
            def topic(self):
                return " some StRinG with RanDoM CaSe And  Weird   SpACING   "

            def we_assert_it_is_like_other_string(self, topic):
                Assert.are_alike('some string with random case and weird spacing', topic)

            def we_assert_it_is_not_like_other_string(self, topic):
                Assert.not_are_alike('some other string', topic)

        class WhenItIsANumber(Vows.Context):
            def topic(self):
                return 42

            def we_assert_it_is_not_like_a_string(self, topic):
                Assert.not_are_alike('42', topic)

            def we_assert_it_is_like_42(self, topic):
                Assert.are_alike(42, topic)

            def we_assert_it_is_like_42_float(self, topic):
                Assert.are_alike(42.0, topic)

            def we_assert_it_is_like_42_long(self, topic):
                Assert.are_alike(long(42), topic)

            def we_assert_it_is_not_like_41(self, topic):
                Assert.not_are_alike(41, topic)

        class WhenItIsAList(Vows.Context):

            class OfNumbers(Vows.Context):
                def topic(self):
                    return [1, 2, 3]

                def we_can_compare_to_other_list(self, topic):
                    Assert.are_alike([1, 2, 3], topic)

                def we_can_compare_to_a_list_in_different_order(self, topic):
                    Assert.are_alike([3, 2, 1], topic)

                def we_can_compare_to_a_tuple_in_different_order(self, topic):
                    Assert.are_alike((3, 2, 1), topic)

            class OfStrings(Vows.Context):
                def topic(self):
                    return ["some", "string", "list"]

                def we_can_compare_to_other_list_in_different_order(self, topic):
                    Assert.are_alike(["list", "some", "string"], topic)

            class OfLists(Vows.Context):

                class WithinList(Vows.Context):
                    def topic(self):
                        return [["my", "list"], ["of", "lists"]]

                    def we_can_compare_to_other_list_of_lists(self, topic):
                        Assert.are_alike((['lists', 'of'], ['list', 'my']), topic)

                class WithinTuple(Vows.Context):
                    def topic(self):
                        return (["my", "list"], ["of", "lists"])

                    def we_can_compare_to_other_list_of_lists(self, topic):
                        Assert.are_alike((['lists', 'of'], ['list', 'my']), topic)

            class OfDicts(Vows.Context):

                def topic(self):
                    return [{'some': 'key', 'other': 'key'}]

                def we_can_compare_to_other_list_of_dicts(self, topic):
                    Assert.are_alike([{'some': 'key', 'other': 'key'}], topic)

                def we_can_compare_to_other_list_of_dicts_out_of_order(self, topic):
                    Assert.are_alike([{'other': 'key', 'some': 'key'}], topic)

        class WhenItIsATuple(Vows.Context):

            class OfNumbers(Vows.Context):
                def topic(self):
                    return (1, 2, 3)

                def we_can_compare_to_other_tuple(self, topic):
                    Assert.are_alike((1, 2, 3), topic)

                def we_can_compare_to_a_tuple_in_different_order(self, topic):
                    Assert.are_alike((3, 2, 1), topic)

                def we_can_compare_to_a_list_in_different_order(self, topic):
                    Assert.are_alike([3, 2, 1], topic)
        
        class WhenItIsADict(Vows.Context):

            def topic(self):
                return { 'some': 'key', 'other': 'value' }

            def we_can_compare_to_other_dict(self, topic):
                Assert.are_alike({ 'some': 'key', 'other': 'value' }, topic)

            def we_can_compare_to_a_dict_in_other_order(self, topic):
                Assert.are_alike({ 'other': 'value', 'some': 'key' }, topic)

            class OfDicts(Vows.Context):

                def topic(self):
                    return {
                        'some': {
                            'key': 'value',
                            'key2': 'value2'
                        }
                    }

                def we_can_compare_to_nested_dicts(self, topic):
                    Assert.are_alike({
                        'some': {
                            'key2': 'value2',
                            'key': 'value'
                        }
                    }, topic)

