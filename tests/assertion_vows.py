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

Assert = Vows.Assert

@Vows.batch
class Assertion(Vows.Context):

    class Equal(Vows.Context):

        def topic(self):
            return "test"

        def we_get_test(self, topic):
            expect(topic).to_equal('test')

        def we_do_not_get_else(self, topic):
            expect(topic).Not.to_equal('else')

        class WhenHaveASubClassThatHaveAExtraParamInTopic(Vows.Context):

            def topic(self, last):
                return last

            def we_get_the_last_topic_value_without_modifications(self, topic):
                expect(topic).to_equal('test')

        class WhenSubContextNotHaveTopic(Vows.Context):

            def we_get_the_last_topic(self, topic):
                expect(topic).to_equal('test')

    class IsInstance(Vows.Context):
        def topic(self):
            return SomeClass()

        def we_get_an_instance_of_someclass(self, topic):
            expect(topic).to_be_instance_of(SomeClass)

        def we_do_not_get_an_instance_of_otherclass(self, topic):
            expect(topic).Not.to_be_instance_of(OtherClass)

        class WeCanModifyATopicValue(Vows.Context):

            def topic(self, older):
                older.coisa = 1
                return older

            def we_get_a_mod_instance_from_my_topic(self, topic):
                expect(hasattr(topic, 'coisa')).to_be_true()

        class TheOtherContext(Vows.Context):

            def topic(self, older):
                return older

            def cant_percept_the_motifications(self, topic):
                expect(hasattr(topic, 'coisa')).to_be_false()

    class IsEmpty(Vows.Context):
        class WhenEmpty(Vows.Context):
            class WhenString(Vows.Context):
                def topic(self):
                    return ''

                def we_get_an_empty_string(self, topic):
                    expect(topic).to_be_empty()

            class WhenList(Vows.Context):
                def topic(self):
                    return []

                def we_get_an_empty_list(self, topic):
                    expect(topic).to_be_empty()

            class WhenTuple(Vows.Context):
                def topic(self):
                    return tuple([])

                def we_get_an_empty_tuple(self, topic):
                    expect(topic).to_be_empty()

            class WhenDict(Vows.Context):
                def topic(self):
                    return {}

                def we_get_an_empty_dict(self, topic):
                    expect(topic).to_be_empty()

        class WhenNotEmpty(Vows.Context):
            class WhenString(Vows.Context):
                def topic(self):
                    return 'whatever'

                def we_get_a_not_empty_string(self, topic):
                    expect(topic).Not.to_be_empty()

            class WhenList(Vows.Context):
                def topic(self):
                    return ['something']

                def we_get_a_not_empty_list(self, topic):
                    expect(topic).Not.to_be_empty()

            class WhenTuple(Vows.Context):
                def topic(self):
                    return tuple(['something'])

                def we_get_a_not_empty_tuple(self, topic):
                    expect(topic).Not.to_be_empty()

            class WhenDict(Vows.Context):
                def topic(self):
                    return {"key": "value"}

                def we_get_a_not_empty_dict(self, topic):
                    expect(topic).Not.to_be_empty()

    class IsNull(Vows.Context):

        class WhenItIsNull(Vows.Context):
            def topic(self):
                return None

            def we_get_to_check_for_nullability_in_None(self, topic):
                expect(topic).to_be_null()

        class WhenItIsNotNull(Vows.Context):
            def topic(self):
                return "something"

            def we_see_string_is_not_null(self, topic):
                expect(topic).not_to_be_null()

    class IsTrue(Vows.Context):

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

    class IsFalse(Vows.Context):

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

    class IsNumeric(Vows.Context):

        class WhenItIsANumber(Vows.Context):
            def topic(self):
                return 42

            def we_assert_it_is_numeric(self, topic):
                expect(topic).to_be_numeric()

        class WhenItIsNotANumber(Vows.Context):
            def topic(self):
                return 'test'

            def we_assert_it_is_not_numeric(self, topic):
                expect(topic).Not.to_be_numeric()

    class IsFunction(Vows.Context):

        class WhenItIsAFunction(Vows.Context):
            def topic(self):
                def my_func():
                    pass
                return my_func

            def we_assert_it_is_a_function(self, topic):
                expect(topic).to_be_a_function()

        class WhenItIsANumber(Vows.Context):
            def topic(self):
                return 42

            def we_assert_it_is_not_a_function(self, topic):
                expect(topic).Not.to_be_a_function()

    class Regexp(Vows.Context):
        def topic(self):
            return "some string"

        def we_assert_it_matches_regexp(self, topic):
            expect(topic).to_match(r'^some.+$')

        def we_assert_it_does_not_match_regexp(self, topic):
            expect(topic).Not.to_match(r'^other.+$')

    class HasThrown(Vows.Context):
        def topic(self):
            raise ValueError("some bogus error")

        def we_can_see_it_was_a_value_error(self, topic):
            expect(topic).to_be_an_error_like(ValueError)

        def we_can_see_that_is_has_error_message_of(self, topic):
            expect(topic).to_have_an_error_message_of("some bogus error")

        def we_can_see_that_is_an_error_instance(self, topic):
            expect(topic).to_be_an_error()

        class TheExceptionClass(Vows.Context):
            def topic(self, error):
                return type(error)

            def we_can_see_that_is_an_error_class(self, topic):
                expect(topic).to_be_an_error()

    class NotHasThrown(Vows.Context):
        def topic(self):
            return 0

        def we_can_see_that_is_not_an_error(self, topic):
            expect(topic).Not.to_be_an_error()

    class Length(Vows.Context):
        class WithString(Vows.Context):
            def topic(self):
                return "some string"

            def we_can_see_it_has_11_characters(self, topic):
                expect(topic).to_length(11)

        class WithList(Vows.Context):
            def topic(self):
                return ["some", "list"]

            def we_can_see_it_has_2_items(self, topic):
                expect(topic).to_length(2)

        class WithTuple(Vows.Context):
            def topic(self):
                return tuple(["some", "list"])

            def we_can_see_it_has_2_items(self, topic):
                expect(topic).to_length(2)

        class WithDict(Vows.Context):
            def topic(self):
                return { "some": "item", "other": "item" }

            def we_can_see_it_has_2_items(self, topic):
                expect(topic).to_length(2)

    class Include(Vows.Context):

        class WhenItIsAString(Vows.Context):
            def topic(self):
                return "some big string"

            def we_can_find_some(self, topic):
                expect(topic).to_include('some')

            def we_can_find_big(self, topic):
                expect(topic).to_include('big')

            def we_can_find_string(self, topic):
                expect(topic).to_include('string')

            def we_cant_find_else(self, topic):
                expect(topic).Not.to_include('else')

        class WhenItIsAList(Vows.Context):
            def topic(self):
                return ["some", "big", "string"]

            def we_can_find_some(self, topic):
                expect(topic).to_include('some')

            def we_can_find_big(self, topic):
                expect(topic).to_include('big')

            def we_can_find_string(self, topic):
                expect(topic).to_include('string')

            def we_cant_find_else(self, topic):
                expect(topic).Not.to_include('else')

        class WhenItIsATuple(Vows.Context):
            def topic(self):
                return tuple(["some", "big", "string"])

            def we_can_find_some(self, topic):
                expect(topic).to_include('some')

            def we_can_find_big(self, topic):
                expect(topic).to_include('big')

            def we_can_find_string(self, topic):
                expect(topic).to_include('string')

            def we_cant_find_else(self, topic):
                expect(topic).Not.to_include('else')

        class WhenItIsADict(Vows.Context):
            def topic(self):
                return {"some": 1, "big": 2, "string": 3}

            def we_can_find_some(self, topic):
                expect(topic).to_include('some')

            def we_can_find_big(self, topic):
                expect(topic).to_include('big')

            def we_can_find_string(self, topic):
                expect(topic).to_include('string')

            def we_cant_find_else(self, topic):
                expect(topic).Not.to_include('else')

    class IsLike(Vows.Context):

        class WhenItIsAString(Vows.Context):
            def topic(self):
                return " some StRinG with RanDoM CaSe And  Weird   SpACING   "

            def we_assert_it_is_like_other_string(self, topic):
                expect(topic).to_be_like('some string with random case and weird spacing')

            def we_assert_it_is_not_like_other_string(self, topic):
                expect(topic).Not.to_be_like('some other string')

        class WhenItIsANumber(Vows.Context):
            def topic(self):
                return 42

            def we_assert_it_is_not_like_a_string(self, topic):
                expect(topic).Not.to_be_like('42')

            def we_assert_it_is_like_42(self, topic):
                expect(topic).to_be_like(42)

            def we_assert_it_is_like_42_float(self, topic):
                expect(topic).to_be_like(42.0)

            def we_assert_it_is_like_42_long(self, topic):
                expect(topic).to_be_like(long(42))

            def we_assert_it_is_not_like_41(self, topic):
                expect(topic).Not.to_be_like(41)

        class WhenItIsAList(Vows.Context):

            class OfNumbers(Vows.Context):
                def topic(self):
                    return [1, 2, 3]

                def we_can_compare_to_other_list(self, topic):
                    expect(topic).to_be_like([1, 2, 3])

                def we_can_compare_to_a_list_in_different_order(self, topic):
                    expect(topic).to_be_like([3, 2, 1])

                def we_can_compare_to_a_tuple_in_different_order(self, topic):
                    expect(topic).to_be_like((3, 2, 1))

            class OfStrings(Vows.Context):
                def topic(self):
                    return ["some", "string", "list"]

                def we_can_compare_to_other_list_in_different_order(self, topic):
                    expect(topic).to_be_like(["list", "some", "string"])

            class OfLists(Vows.Context):

                class WithinList(Vows.Context):
                    def topic(self):
                        return [["my", "list"], ["of", "lists"]]

                    def we_can_compare_to_other_list_of_lists(self, topic):
                        expect(topic).to_be_like((['lists', 'of'], ['list', 'my']))

                class WithinTuple(Vows.Context):
                    def topic(self):
                        return (["my", "list"], ["of", "lists"])

                    def we_can_compare_to_other_list_of_lists(self, topic):
                        expect(topic).to_be_like((['lists', 'of'], ['list', 'my']))

            class OfDicts(Vows.Context):

                def topic(self):
                    return [{'some': 'key', 'other': 'key'}]

                def we_can_compare_to_other_list_of_dicts(self, topic):
                    expect(topic).to_be_like([{'some': 'key', 'other': 'key'}])

                def we_can_compare_to_other_list_of_dicts_out_of_order(self, topic):
                    expect(topic).to_be_like([{'other': 'key', 'some': 'key'}])

        class WhenItIsATuple(Vows.Context):

            class OfNumbers(Vows.Context):
                def topic(self):
                    return (1, 2, 3)

                def we_can_compare_to_other_tuple(self, topic):
                    expect(topic).to_be_like((1, 2, 3))

                def we_can_compare_to_a_tuple_in_different_order(self, topic):
                    expect(topic).to_be_like((3, 2, 1))

                def we_can_compare_to_a_list_in_different_order(self, topic):
                    expect(topic).to_be_like([3, 2, 1])

        class WhenItIsADict(Vows.Context):

            def topic(self):
                return { 'some': 'key', 'other': 'value' }

            def we_can_compare_to_other_dict(self, topic):
                expect(topic).to_be_like({ 'some': 'key', 'other': 'value' })

            def we_can_compare_to_a_dict_in_other_order(self, topic):
                expect(topic).to_be_like({ 'other': 'value', 'some': 'key' })

            class OfDicts(Vows.Context):

                def topic(self):
                    return {
                        'some': {
                            'key': 'value',
                            'key2': 'value2'
                        }
                    }

                def we_can_compare_to_nested_dicts(self, topic):
                    expect(topic).to_be_like({
                        'some': {
                            'key2': 'value2',
                            'key': 'value'
                        }
                    })
