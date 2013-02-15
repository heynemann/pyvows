#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''PyVows similarity assertions.  For use with `expect()` (see `pyvows.core`).

The imprecise nature of "like" comparisons is much more complicated
than most assertions.  All support code lives in this module
alongside the assertions.

'''


# pyVows testing engine
# https://github.com/heynemann/pyvows

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 Bernardo Heynemann heynemann@gmail.com

import numbers

from pyvows import Vows


@Vows.create_assertions
def to_be_like(topic, expected):
    '''Asserts that `topic` is like (similar to) `expected`. Allows
    some leeway.

    '''
    return match_alike(expected, topic)


def compare_alike(expected, topic, modifier, message):
    '''Asserts that `topic` is like `expected`, as specified by
    `modifier`.

    '''
    assert modifier(match_alike(expected, topic)), message % (topic, expected)


def match_alike(expected, topic):
    '''Asserts the "like"-ness of `topic` and `expected` according
    to their types.

    '''
    if topic is None:
        return expected is None
    if isinstance(topic, basestring):
        return compare_strings(expected, topic)
    elif isinstance(topic, numbers.Number):
        return compare_numbers(expected, topic)
    elif isinstance(topic, (list, tuple)):
        return compare_lists(expected, topic)
    elif isinstance(topic, dict):
        return compare_dicts(expected, topic)
    else:
        raise RuntimeError('Could not compare {expected} and {topic}'.format(expected=expected, topic=topic))


def compare_strings(expected, topic):
    '''Asserts the "like"-ness of `topic` and `expected` as strings.
    Allows some leeway.  (Strings don't have to exactly match.)

    '''
    replaced_topic = topic.lower().replace(' ', '').replace('\n', '')
    replaced_expected = expected.lower().replace(' ', '').replace('\n', '')
    return replaced_expected.lower() == replaced_topic.lower()


def compare_numbers(expected, topic):
    '''Asserts the "like"-ness of `topic` and `expected` as Numbers.'''
    if not isinstance(topic, numbers.Number) or not isinstance(expected, numbers.Number):
        return False
    return float(expected) == float(topic)


def compare_dicts(expected, topic):
    '''Asserts the "like"-ness of `topic` and `expected` as dicts.'''
    return match_dicts(expected, topic) and match_dicts(topic, expected)


def match_dicts(expected, topic):
    '''Asserts the "like"-ness of all keys and values in `topic` and
    `expected`.
    '''
    for k, v in expected.iteritems():
        if not k in topic or not match_alike(topic[k], v):
            return False
    return True


def compare_lists(expected, topic):
    '''Asserts the "like"-ness of `topic` and `expected` as lists.'''
    return match_lists(expected, topic) and match_lists(topic, expected)


def match_lists(expected, topic):
    '''Asserts the "like"-ness each item in of `topic` and `expected`
    (as lists or tuples).

    '''
    for item in expected:
        if isinstance(item, (list, tuple)):
            found = False
            for inner_item in topic:
                if not isinstance(inner_item, (list, tuple)):
                    continue
                if compare_lists(item, inner_item):
                    found = True
                    break
            if not found:
                return False
        elif not item in topic:
            return False

    return True
