# -*- coding: utf-8 -*-
'''Contains the `VowsDefaultReporter` class, which handles output after tests
have been run.
'''
# pyvows testing engine
# https://github.com/heynemann/pyvows

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 Bernardo Heynemann heynemann@gmail.com
from __future__ import division

from pyvows.color import *
from pyvows.reporting.common import (
    VowsReporter,)



class VowsProfileReporter(VowsReporter):
    '''A VowsReporter which prints a profile of the 10 slowest topics.'''

    def print_profile(self, threshold):
        '''Prints the 10 slowest topics that took longer than `threshold`
        to test.
        '''

        MAX_PATH_SIZE = 30
        topics = self.result.get_worst_topics(number=10, threshold=threshold)

        if topics:
            print self.header('Slowest Topics')

            print yellow('       elapsed     Context File Path                 Context Name')
            for index, topic in enumerate(topics):
                name = self.under_split(topic['context'])
                name = self.camel_split(name)

                print Style.BRIGHT + ("%s#%02d%s    %.05fs    %s%s%" + str(MAX_PATH_SIZE) + "s%s%s    %s") % (
                        Fore.BLUE,
                        index + 1,
                        Fore.RESET,
                        topic['elapsed'],
                        Style.DIM,
                        Fore.WHITE,
                        topic['path'][-MAX_PATH_SIZE:],
                        Fore.RESET,
                        Style.BRIGHT,
                        name
                ) + Style.RESET_ALL

            print