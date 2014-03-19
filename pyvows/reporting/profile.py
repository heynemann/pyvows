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

import os

from pyvows.color import yellow, blue, dim, green, white
from pyvows.reporting.common import (
    VowsReporter,)


class VowsProfileReporter(VowsReporter):
    '''A VowsReporter which prints a profile of the 10 slowest topics.'''

    def print_profile(self, threshold):
        '''Prints the 10 slowest topics that took longer than `threshold`
        to test.
        '''

        '''Prints the 10 slowest topics that took longer than
        `threshold` to test.

        '''

        MAX_PATH_SIZE = 40
        topics = self.result.get_worst_topics(number=10, threshold=threshold)

        if topics:
            print(self.header('Slowest Topics'))

            table_header = yellow('  {0}'.format(dim('#')))
            table_header += yellow('  Elapsed     Context File Path                         ')
            table_header += yellow('  Context Name')
            print(table_header)

            for index, topic in enumerate(topics):
                name = self.under_split(topic['context'])
                name = self.camel_split(name)

                topic['path'] = os.path.realpath(topic['path'])
                topic['path'] = '{0!s}'.format(topic['path'])
                topic['path'] = os.path.relpath(topic['path'], os.path.abspath(os.curdir))

                data = {
                    'number': '{number:#2}'.format(number=index + 1),
                    'time': '{time:.05f}s'.format(time=topic['elapsed']),
                    'path': '{path:<{width}}'.format(
                        path=topic['path'][-MAX_PATH_SIZE:],
                        width=MAX_PATH_SIZE),
                    'name': '{name}'.format(name=name),
                }

                for k, v in data.items():
                    if k == 'number':
                        colorized = blue
                    if k == 'time':
                        colorized = green
                    if k == 'path':
                        colorized = lambda x: dim(white(x))
                    if k == 'name':
                        colorized = green

                    data[k] = colorized(v)

                print(
                    ' {number}  {time}{0}{path}{0}{name}'.format(
                        4 * ' ',
                        **data)
                    )

            print()
