#!/usr/bin/env python
# -*- coding: utf-8 -*-

# pyVows testing engine
# https://github.com/{heynemann,truemped}/pyvows

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 Daniel Truemper truemped@googlemail.com
import codecs
from datetime import datetime
import socket
import traceback


class XUnitReporter(object):

    def __init__(self, result, filename, encoding='UTF-8'):
        self.result = result
        self.filename = filename
        self.encoding = encoding

    def write_report(self):
        output_file = codecs.open(self.filename, 'w', self.encoding, 'replace')

        stats = {'encoding': self.encoding,
            'total': self.result.successful_tests + self.result.errored_tests,
            'errors': 0,
            'failures': self.result.errored_tests,
            'ts': datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
            'hostname': socket.gethostname(),
            'elapsed': self.result.ellapsed_time,
        }

        output_file.write(
            u'<?xml version="1.0" encoding="%(encoding)s"?>\n'
            u'<testsuite name="pyvows" tests="%(total)d" '
            u'errors="%(errors)d" failures="%(failures)d" '
            u'timestamp="%(ts)s" hostname="%(hostname)s" '
            u'time="%(elapsed).3f">\n' % (stats)
        )

        for context in self.result.contexts:
            self.write_context(output_file, context)

        output_file.write(u'</testsuite>')

    def write_context(self, output_file, context):

        for test in context['tests']:
            nice_name = '%s.%s' % (context['name'], test['name'])

            if test['succeeded']:
                test_stats = {'context': context['name'],
                    'name': test['name'],
                    'taken': 0.0
                }

                output_file.write(u'<testcase classname="%(context)s" '
                        u'name="%(name)s" time="%(taken).3f" />\n' % test_stats)

            else:
                test_stats = {'context': context['name'],
                    'name': test['name'],
                    'taken': 0.0
                }
                output_file.write(u'<testcase classname="%(context)s" '
                        u'name="%(name)s" time="%(taken).3f">\n' % test_stats)

                error = test['error']
                error_msg = traceback.format_exception(error['type'],
                        error['value'], error['traceback'])

                if isinstance(test['topic'], Exception):
                    exc_type, exc_value, exc_traceback = test['context_instance'].topic_error
                    error_msg += traceback.format_exception(exc_type, exc_value, exc_traceback)

                error_data = {'errtype': error['type'].__name__,
                    'msg': error['value'],
                    'tb': ''.join(error_msg)
                }

                output_file.write(u'<failure type="%(errtype)s" '
                        u'message="%(msg)s"><![CDATA[%(tb)s]]>' % error_data)
                output_file.write(u'</failure>\n</testcase>\n')

        for ctx in context['contexts']:
            self.write_context(output_file, ctx)
