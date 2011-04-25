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

        def we_get_test(self, topic):
            Vows.Assert.are_equal('test', topic)

        def we_do_not_get_else(self, topic):
            Vows.Assert.not_are_equal('else', topic)

    class IsNumeric(Vows.Context):

        class WhenItIsANumber(Vows.Context):
            def topic(self):
                return 42

            def we_assert_it_is_numeric(self, topic):
                Vows.Assert.is_numeric(topic)

        class WhenItIsNotANumber(Vows.Context):
            def topic(self):
                return 'test'

            def we_assert_it_is_not_numeric(self, topic):
                Vows.Assert.not_is_numeric(topic)

    class IsFunction(Vows.Context):

        class WhenItIsAFunction(Vows.Context):
            def topic(self):
                def my_func():
                    pass
                return my_func

            def we_assert_it_is_a_function(self, topic):
                Vows.Assert.is_function(topic)

        class WhenItIsANumber(Vows.Context):
            def topic(self):
                return 42

            def we_assert_it_is_not_a_function(self, topic):
                Vows.Assert.not_is_function(topic)

    class IsLike(Vows.Context):

        class WhenItIsAString(Vows.Context):
            def topic(self):
                return " some StRinG with RanDoM CaSe And  Weird   SpACING   "

            def we_assert_it_is_like_other_string(self, topic):
                Vows.Assert.are_alike('some string with random case and weird spacing', topic)

            def we_assert_it_is_not_like_other_string(self, topic):
                Vows.Assert.not_are_alike('some other string', topic)

        class WhenItIsANumber(Vows.Context):
            def topic(self):
                return 42

            def we_assert_it_is_not_like_a_string(self, topic):
                Vows.Assert.not_are_alike('42', topic)

            def we_assert_it_is_like_42(self, topic):
                Vows.Assert.are_alike(42, topic)

            def we_assert_it_is_like_42_float(self, topic):
                Vows.Assert.are_alike(42.0, topic)

            def we_assert_it_is_like_42_long(self, topic):
                Vows.Assert.are_alike(long(42), topic)

            def we_assert_it_is_not_like_41(self, topic):
                Vows.Assert.not_are_alike(41, topic)

        class WhenItIsAList(Vows.Context):

            class OfNumbers(Vows.Context):
                def topic(self):
                    return [1, 2, 3]

                def we_can_compare_to_other_list(self, topic):
                    Vows.Assert.are_alike([1, 2, 3], topic)

                def we_can_compare_to_a_list_in_different_order(self, topic):
                    Vows.Assert.are_alike([3, 2, 1], topic)

                def we_can_compare_to_a_tuple_in_different_order(self, topic):
                    Vows.Assert.are_alike((3, 2, 1), topic)

            class OfStrings(Vows.Context):
                def topic(self):
                    return ["some", "string", "list"]

                def we_can_compare_to_other_list_in_different_order(self, topic):
                    Vows.Assert.are_alike(["list", "some", "string"], topic)

            class OfLists(Vows.Context):

                class WithinList(Vows.Context):
                    def topic(self):
                        return [["my", "list"], ["of", "lists"]]

                    def we_can_compare_to_other_list_of_lists(self, topic):
                        Vows.Assert.are_alike((['lists', 'of'], ['list', 'my']), topic)

                class WithinTuple(Vows.Context):
                    def topic(self):
                        return (["my", "list"], ["of", "lists"])

                    def we_can_compare_to_other_list_of_lists(self, topic):
                        Vows.Assert.are_alike((['lists', 'of'], ['list', 'my']), topic)

        class WhenItIsATuple(Vows.Context):

            class OfNumbers(Vows.Context):
                def topic(self):
                    return (1, 2, 3)

                def we_can_compare_to_other_tuple(self, topic):
                    Vows.Assert.are_alike((1, 2, 3), topic)

                def we_can_compare_to_a_tuple_in_different_order(self, topic):
                    Vows.Assert.are_alike((3, 2, 1), topic)

                def we_can_compare_to_a_list_in_different_order(self, topic):
                    Vows.Assert.are_alike([3, 2, 1], topic)

