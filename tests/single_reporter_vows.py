#!/usr/bin/env python
# -*- coding: utf-8 -*-

# pyvows testing engine
# https://github.com/heynemann/pyvows

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2013 Nathan Dotz nathan.dotz@gmail.com

from pyvows import Vows, expect
from pyvows import console
#from pyvows.reporting import VowsDefaultReporter


@Vows.batch
class SingleVowFromCommandLine(Vows.Context):

    def topic(self):
        return console

    def should_be_not_error_when_called_with_5_args(self, topic):
        try:
            topic.run(None, None, None, None, None)
        except Exception as e:
            expect(e).Not.to_be_instance_of(TypeError)

    # TODO: add vow checking that there is a message about vow matching

    class Core(Vows.Context):

        def topic(self):
            return Vows

        def should_have_prune_method(self, topic):
            expect(topic.prune).to_be_a_function()
