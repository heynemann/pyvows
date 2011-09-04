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
def a_function(): pass

Assert = Vows.Assert

@Vows.batch
class Assertion(Vows.Context):

    class WhenUTF8Topic(Vows.Context):
        def topic(self):
            return u"some á é í ó ç"

        def should_not_fail(self, topic):
            expect(topic).to_equal(u'some á é í ó ç')

    class NonErrorContext(Vows.NotErrorContext):
        def topic(self):
            return 42

    class NotEmptyContext(Vows.NotEmptyContext):
        def topic(self):
            return "harmless"

    class WhenNotHaveTopic(Vows.Context):
        def we_can_see_topic_as_none(self, topic):
            expect(topic).to_be_null()

    class Equal(Vows.Context):
        def topic(self):
            return "test"

        class WhenIsEqual(Vows.Context):

            def we_get_test(self, topic):
                expect(topic).to_equal('test')

            class WhenWeGetAnError(Vows.Context):

                def topic(self, last):
                    expect(1).to_equal(2)

                def we_get_an_understandable_message(self, topic):
                    expect(topic).to_have_an_error_message_of("Expected topic(1) to equal 2")

        class WhenIsNotEqual(Vows.Context):

            def we_do_not_get_else(self, topic):
                expect(topic).Not.to_equal('else')

            class WhenWeGetAnError(Vows.Context):

                def topic(self, last):
                    expect(1).not_to_equal(1)

                def we_get_an_understandable_message(self, topic):
                    expect(topic).to_have_an_error_message_of("Expected topic(1) not to equal 1")

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

        class WhenIsInstance(Vows.Context):

            def we_get_an_instance_of_someclass(self, topic):
                expect(topic).to_be_instance_of(SomeClass)

            class WhenWeGetAnError(Vows.Context):

                def topic(self, last):
                    expect(2).to_be_instance_of(str)

                def we_get_an_understandable_message(self, topic):
                    expect(topic).to_have_an_error_message_of(
                            "Expected topic(2) to be an instance of %s, but it was a %s" % (str(str), str(int)))

        class WhenIsNotInstance(Vows.Context):

            def we_do_not_get_an_instance_of_otherclass(self, topic):
                expect(topic).Not.to_be_instance_of(OtherClass)

            class WhenWeGetAnError(Vows.Context):

                def topic(self, last):
                    expect(2).not_to_be_instance_of(int)

                def we_get_an_understandable_message(self, topic):
                    expect(topic).to_have_an_error_message_of(
                            "Expected topic(2) not to be an instance of %s" % str(int))


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

            class WhenWeGetAnError(Vows.Context):

                def topic(self, last):
                    expect([1]).to_be_empty()

                def we_get_an_understandable_message(self, topic):
                    expect(topic).to_have_an_error_message_of("Expected topic([1]) to be empty")

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

            class WhenWeGetAnError(Vows.Context):

                def topic(self, last):
                    expect([]).not_to_be_empty()

                def we_get_an_understandable_message(self, topic):
                    expect(topic).to_have_an_error_message_of("Expected topic([]) not to be empty")

    class IsNull(Vows.Context):

        class WhenItIsNull(Vows.Context):
            def topic(self):
                return None

            def we_get_to_check_for_nullability_in_None(self, topic):
                expect(topic).to_be_null()

            class WhenWeGetAnError(Vows.Context):
                def topic(self, last):
                    expect(1).to_be_null()

                def we_get_an_understandable_message(self, topic):
                    expect(topic).to_have_an_error_message_of("Expected topic(1) to be None")

        class WhenItIsNotNull(Vows.Context):
            def topic(self):
                return "something"

            def we_see_string_is_not_null(self, topic):
                expect(topic).not_to_be_null()

            class WhenWeGetAnError(Vows.Context):
                def topic(self, last):
                    expect(None).not_to_be_null()

                def we_get_an_understandable_message(self, topic):
                    expect(topic).to_have_an_error_message_of("Expected topic(None) not to be None")


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

        class WhenWeGetAnError(Vows.Context):

            def topic(self, last):
                expect(False).to_be_true()

            def we_get_an_understandable_message(self, topic):
                expect(topic).to_have_an_error_message_of("Expected topic(False) to be truthy")


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

        class WhenWeGetAnError(Vows.Context):

            def topic(self):
                expect(True).to_be_false()

            def we_get_an_understandable_message(self, topic):
                expect(topic).to_have_an_error_message_of("Expected topic(True) to be falsy")


    class IsNumeric(Vows.Context):

        class WhenItIsANumber(Vows.Context):
            def topic(self):
                return 42

            def we_assert_it_is_numeric(self, topic):
                expect(topic).to_be_numeric()

            class WhenWeGetAnError(Vows.Context):

                def topic(self):
                    expect('s').to_be_numeric()

                def we_get_an_understandable_message(self, topic):
                    expect(topic).to_have_an_error_message_of("Expected topic(s) to be numeric")


        class WhenItIsNotANumber(Vows.Context):
            def topic(self):
                return 'test'

            def we_assert_it_is_not_numeric(self, topic):
                expect(topic).Not.to_be_numeric()

            class WhenWeGetAnError(Vows.Context):

                def topic(self):
                    expect(2).not_to_be_numeric()

                def we_get_an_understandable_message(self, topic):
                    expect(topic).to_have_an_error_message_of("Expected topic(2) not to be numeric")


    class IsFunction(Vows.Context):

        class WhenItIsAFunction(Vows.Context):
            def topic(self):
                def my_func():
                    pass
                return my_func

            def we_assert_it_is_a_function(self, topic):
                expect(topic).to_be_a_function()

            class WhenWeGetAnError(Vows.Context):

                def topic(self):
                    expect(4).to_be_a_function()

                def we_get_an_understandable_message(self, topic):
                    expect(topic).to_have_an_error_message_of(
                            "Expected topic(4) to be a function or a method, but it was a %s" % str(int))


        class WhenItNotAFunction(Vows.Context):
            def topic(self):
                return 42

            def we_assert_it_is_not_a_function(self, topic):
                expect(topic).Not.to_be_a_function()

            class WhenWeGetAnError(Vows.Context):

                def topic(self):
                    expect(a_function).not_to_be_a_function()

                def we_get_an_understandable_message(self, topic):
                    expect(topic).to_have_an_error_message_of(
                            "Expected topic(%s) not to be a function or a method" % str(a_function))


    class Regexp(Vows.Context):
        def topic(self):
            return "some string"

        class WhenItMatches(Vows.Context):

            def we_assert_it_matches_regexp(self, topic):
                expect(topic).to_match(r'^some.+$')

            class WhenWeGetAnError(Vows.Context):

                def topic(self, last):
                    expect(last).to_match(r'^other.+$')

                def we_get_an_understandable_message(self, topic):
                    expect(topic).to_have_an_error_message_of(
                            "Expected topic(some string) to match the regular expression ^other.+$")

        class WhenItDoesntMatches(Vows.Context):

            def we_assert_it_does_not_match_regexp(self, topic):
                expect(topic).Not.to_match(r'^other.+$')

            class WhenWeGetAnError(Vows.Context):

                def topic(self, last):
                    expect(last).not_to_match(r'^some.+$')

                def we_get_an_understandable_message(self, topic):
                    expect(topic).to_have_an_error_message_of(
                            "Expected topic(some string) not to match the regular expression ^some.+$")


    class Errors(Vows.Context):
        class WhenRaises(Vows.Context):
            def topic(self):
                raise ValueError("some bogus error")

            class BeAnErrorLike(Vows.Context):

                def we_can_see_it_was_a_value_error(self, topic):
                    expect(topic).to_be_an_error_like(ValueError)

                class WhenWeGetAnError(Vows.Context):

                    def topic(self, last):
                        expect(NotImplementedError('no')).to_be_an_error_like(OSError)

                    def we_get_an_understandable_message(self, topic):
                        expect(topic).to_have_an_error_message_of(
                                "Expected topic(%s) to be an error of type %s, but it was a %s" % (
                                    NotImplementedError('no'), OSError, NotImplementedError))

            class HaveErrorMessageOf(Vows.Context):

                def we_can_see_that_is_has_error_message_of(self, topic):
                    expect(topic).to_have_an_error_message_of("some bogus error")

                class WhenWeGetAnError(Vows.Context):

                    def topic(self, last):
                        expect(last).to_have_an_error_message_of('some bogus')

                    def we_get_an_understandable_message(self, topic):
                        expect(topic).to_have_an_error_message_of(
                                "Expected topic(%s) to be an error with message '%s'" % (
                                    'some bogus error', 'some bogus'))

            class ToBeAnError(Vows.Context):

                def we_can_see_that_is_an_error_instance(self, topic):
                    expect(topic).to_be_an_error()

                class WhenWeGetAnError(Vows.Context):

                    def topic(self, last):
                        expect(2).to_be_an_error()

                    def we_get_an_understandable_message(self, topic):
                        expect(topic).to_have_an_error_message_of("Expected topic(2) to be an error")

            class NotToBeAnError(Vows.Context):
                def topic(self):
                    return 2

                def we_can_see_that_is_not_an_error_instance(self, topic):
                    expect(topic).not_to_be_an_error()

                class WhenWeGetAnError(Vows.Context):

                    def topic(self, last):
                        expect(ValueError).not_to_be_an_error()

                    def we_get_an_understandable_message(self, topic):
                        expect(topic).to_have_an_error_message_of("Expected topic(%s) not to be an error" % str(ValueError))
            class TheExceptionClass(Vows.Context):
                def topic(self, error):
                    return ValueError

                def we_can_see_that_is_an_error_class(self, topic):
                    expect(topic).to_be_an_error()


        class WhenDontRaise(Vows.Context):
            def topic(self):
                return 0

            def we_can_see_that_is_not_an_error(self, topic):
                expect(topic).Not.to_be_an_error()

    class Length(Vows.Context):
        class ToLength(Vows.Context):
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

            class WhenWeGetAnError(Vows.Context):

                def topic(self, last):
                    expect('a').to_length(2)

                def we_get_an_understandable_message(self, topic):
                    expect(topic).to_have_an_error_message_of("Expected topic(a) to have 2 of length, but it has 1")

        class NotToLength(Vows.Context):
            class WhenWeGetAnError(Vows.Context):
                def topic(self, last):
                    expect('a').not_to_length(1)

                def we_get_an_understandable_message(self, topic):
                    expect(topic).to_have_an_error_message_of("Expected topic(a) not to have 1 of length")


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

        class WhenWeGetAnError(Vows.Context):
            def topic(self, last):
                expect('a').to_include('b')

            def we_get_an_understandable_message(self, topic):
                expect(topic).to_have_an_error_message_of("Expected topic(a) to include b")

        class WhenWeGetAnErrorOnNot(Vows.Context):
            def topic(self, last):
                expect('a').not_to_include('a')

            def we_get_an_understandable_message(self, topic):
                expect(topic).to_have_an_error_message_of("Expected topic(a) not to include a")

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

            def we_can_compare_to_a_dict_with_a_key_that_has_value_none(self, topic):
                expect(topic).not_to_be_like({ 'other': 'value', 'some': None })

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

        class WhenWeGetAnError(Vows.Context):
            def topic(self, last):
                expect('a').to_be_like('b')

            def we_get_an_understandable_message(self, topic):
                expect(topic).to_have_an_error_message_of("Expected topic(a) to be like b")

        class WhenWeGetAnErrorOnNot(Vows.Context):
            def topic(self, last):
                expect('a').not_to_be_like('a')

            def we_get_an_understandable_message(self, topic):
                expect(topic).to_have_an_error_message_of("Expected topic(a) not to be like a")

