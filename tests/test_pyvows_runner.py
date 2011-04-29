#!/usr/bin/env python
# -*- coding: utf-8 -*-

# pyVows testing engine
# https://github.com/heynemann/pyvows

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 Bernardo Heynemann heynemann@gmail.com

from pyvows.runner import VowsRunner

def assert_it(expected, returned):
    assert expected == returned, 'Expected: %s and returned %s' % (str(expected), str(returned))


def test_when_not_have_olders_topics():
    r = VowsRunner(None, None)
    assert_it([], r.pop_topics([]))

def test_when_have_a_old_topic():
    r = VowsRunner(None, None)
    assert_it([1], r.pop_topics([1]))

def test_when_have_2_old_topics():
    r = VowsRunner(None, None)
    assert_it([2], r.pop_topics([1, 2]))

def test_when_the_last_topic_is_none_return_the_parent_value():
    r = VowsRunner(None, None)
    assert_it([1], r.pop_topics([1, None, None, None]))

def test_when_should_get_a_specifc_num_of_topics():
    r = VowsRunner(None, None)
    assert_it([5, 4, 3], r.pop_topics([1, 2, 3, 4, 5], num=3))

def test_when_get_topics_form_contexts_that_not_have_topic():
    r = VowsRunner(None, None)
    assert_it([5, 3, 2], r.pop_topics([1, 2, 3, None, 5, None], num=3))
