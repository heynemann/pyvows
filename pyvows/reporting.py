#!/usr/bin/env python
# -*- coding: utf-8 -*-

# pyvows testing engine
# https://github.com/heynemann/pyvows

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 Bernardo Heynemann heynemann@gmail.com

import re

from colorama import init, Fore, Style

class VowsDefaultReporter(object):
    honored = Fore.GREEN + Style.BRIGHT + '✓' + Fore.RESET + Style.RESET_ALL
    broken = Fore.RED + Style.BRIGHT + '✗' + Fore.RESET + Style.RESET_ALL

    def __init__(self, result):
        init(autoreset=True)
        self.result = result
        self.tab = " " * 2
        self.indent = 0

    def camel_split(self, string):
        return re.sub('((?=[A-Z][a-z])|(?<=[a-z])(?=[A-Z]))', ' ', string)

    def pretty_print(self):
        for name, context in self.result.contexts.iteritems():
            self.print_context(name, context)
        print
        print " %s OK » %d honored • %d errored (%.2fs)" % (
                self.result.successful and self.honored or self.errored,
                self.result.successful_tests,
                self.result.failed_tests,
                self.result.ellapsed_time
        )

    def print_context(self, name, context):
        print " %s%s" % (self.tab * self.indent, self.camel_split(name))
        self.indent += 1

        for test in context.tests:
            if test.successful:
                print " %s%s %s" % (self.tab * self.indent, self.honored, self.camel_split(test.name))

        self.indent -= 1
