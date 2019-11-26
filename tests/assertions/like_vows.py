#!/usr/bin/env python
# -*- coding: utf-8 -*-

# pyvows testing engine
# https://github.com/heynemann/pyvows

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 Bernardo Heynemann heynemann@gmail.com

from pyvows import Vows, expect


@Vows.batch
class AssertionIsLike(Vows.Context):

    class WhenItIsAString(Vows.Context):
        def topic(self):
            return " some StRinG with RanDoM CaSe And  Weird   SpACING   "

        def we_assert_it_is_like_other_string(self, topic):
            expect(topic).to_be_like('some string with random case and weird spacing')

        def we_assert_it_is_not_like_other_string(self, topic):
            expect(topic).Not.to_be_like('some other string')

    class WhenItIsAMultilineString(Vows.Context):
        def topic(self):
            return " some StRinG \nwith RanDoM \nCaSe And  \nWeird   \nSpACING   "

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
            return {'some': 'key', 'other': 'value'}

        def we_can_compare_to_other_dict(self, topic):
            expect(topic).to_be_like({'some': 'key', 'other': 'value'})

        def we_can_compare_to_a_dict_in_other_order(self, topic):
            expect(topic).to_be_like({'other': 'value', 'some': 'key'})

        def we_can_compare_to_a_dict_with_a_key_that_has_value_none(self, topic):
            expect(topic).not_to_be_like({'other': 'value', 'some': None})

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
        @Vows.capture_error
        def topic(self, last):
            expect('a').to_be_like('b')

        def we_get_an_understandable_message(self, topic):
            expect(topic).to_have_an_error_message_of("Expected topic('a') to be like 'b'")

    class WhenWeGetAnErrorOnNot(Vows.Context):
        @Vows.capture_error
        def topic(self, last):
            expect('a').not_to_be_like('a')

        def we_get_an_understandable_message(self, topic):
            expect(topic).to_have_an_error_message_of("Expected topic('a') not to be like 'a'")
