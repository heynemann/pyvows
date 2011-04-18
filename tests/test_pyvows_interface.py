#!/usr/bin/env python
# -*- coding: utf-8 -*-

# thumbor imaging service
# https://github.com/globocom/thumbor/wiki

# Licensed under the MIT license: 
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 globo.com timehome@corp.globo.com

from pyvows import Vows

import division_vows

def test_can_get_vows():
    assert Vows.__current_vows__

def test_can_get_vows_by_key():
    assert 'DivisionTests' in Vows.__current_vows__

def test_can_run_vows():
    result = Vows.ensure()

    assert result.successful
