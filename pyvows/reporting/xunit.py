# -*- coding: utf-8 -*-
'''Provides the `XUnitReporter` class, which creates XML reports after testing.
'''


# pyVows testing engine
# https://github.com/{heynemann,truemped}/pyvows

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 Daniel Truemper truemped@googlemail.com
import codecs
from datetime import datetime
import socket
import traceback
from xml.dom.minidom import Document
import re

INVALID_CHARACTERS = re.compile(r"[\000-\010\013\014\016-\037]")
INVALID_CHARACTERS = re.compile(r"[\000]")


class XUnitReporter(object):
    '''Turns `VowsResult` objects into XUnit-style reports.'''

    def __init__(self, result):
        self.result_summary = self.summarize_results(result)

    def write_report(self, filename, encoding=None):
        #   FIXME: Add Docstring
        with codecs.open(filename, 'w', encoding, 'replace') as output_file:
            output_file.write(self.to_xml(encoding))

    def to_xml(self, encoding='utf-8'):
        #   FIXME: Add Docstring
        document = self.create_report_document()
        return document.toxml(encoding=encoding)

    def summarize_results(self, result):
        #   FIXME: Add Docstring
        result_summary = {
            'total': result.total_test_count,
            'errors': 0,
            'skip': result.skipped_tests,
            'failures': result.errored_tests,
            'ts': datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
            'hostname': socket.gethostname(),
            'elapsed': result.elapsed_time,
            'contexts': result.contexts
        }
        return result_summary

    def create_report_document(self):
        #   FIXME: Add Docstring
        result_summary = self.result_summary

        document = Document()
        testsuite_node = document.createElement('testsuite')
        testsuite_node.setAttribute('name', 'pyvows')
        testsuite_node.setAttribute('tests', str(result_summary['total']))
        testsuite_node.setAttribute('errors', str(result_summary['errors']))
        testsuite_node.setAttribute('failures', str(result_summary['failures']))
        testsuite_node.setAttribute('skip', str(result_summary['skip']))
        testsuite_node.setAttribute('timestamp', str(result_summary['ts']))
        testsuite_node.setAttribute('hostname', str(result_summary['hostname']))
        testsuite_node.setAttribute('time', '{elapsed:.3f}'.format(elapsed=result_summary['elapsed']))

        document.appendChild(testsuite_node)

        for context in result_summary['contexts']:
            self.create_test_case_elements(document, testsuite_node, context)

        return document

    def _safe_cdata(self, str):
        return INVALID_CHARACTERS.sub('', str)

    def create_test_case_elements(self, document, parent_node, context):
        #   FIXME: Add Docstring

        topic_node = document.createElement('testcase')
        topic_node.setAttribute('classname', context['name'])
        topic_node.setAttribute('name', 'topic')
        topic_node.setAttribute('time', '0.0')
        stdOutNode = document.createElement('system-out')
        stdOutText = document.createCDATASection(self._safe_cdata(context['stdout']))
        stdOutNode.appendChild(stdOutText)
        stdErrNode = document.createElement('system-err')
        stdErrText = document.createCDATASection(self._safe_cdata(context['stderr']))
        stdErrNode.appendChild(stdErrText)

        topic_node.appendChild(stdOutNode)
        topic_node.appendChild(stdErrNode)
        if context.get('error', None):
            e = context['error']
            error_msg = 'Error in {0!s}: {1!s}'.format(e.source, e.exc_info[1])
            error_tb = traceback.format_exception(*e.exc_info)

            failure_node = document.createElement('failure')
            failure_node.setAttribute('type', e.exc_info[0].__name__)
            failure_node.setAttribute('message', error_msg)
            failure_text = document.createTextNode(''.join(error_tb))
            failure_node.appendChild(failure_text)
            topic_node.appendChild(failure_node)
        if context.get('skip', None):
            skip_node = document.createElement('skipped')
            skip_node.setAttribute('message', str(context['skip']))
            topic_node.appendChild(skip_node)

        parent_node.appendChild(topic_node)

        for test in context['tests']:
            test_stats = {
                'context': context['name'],
                'name': test['name'],
                'taken': 0.0
            }

            testcase_node = document.createElement('testcase')
            testcase_node.setAttribute('classname', str(test_stats['context']))
            testcase_node.setAttribute('name', str(test_stats['name']))
            testcase_node.setAttribute('time', '{time:.3f}'.format(time=test_stats['taken']))

            stdOutNode = document.createElement('system-out')
            stdOutText = document.createCDATASection(self._safe_cdata(test['stdout']))
            stdOutNode.appendChild(stdOutText)
            stdErrNode = document.createElement('system-err')
            stdErrText = document.createCDATASection(self._safe_cdata(test['stderr']))
            stdErrNode.appendChild(stdErrText)

            testcase_node.appendChild(stdOutNode)
            testcase_node.appendChild(stdErrNode)
            parent_node.appendChild(testcase_node)

            if test.get('error', None):
                error = test['error']
                error_msg = traceback.format_exception(
                    error['type'],
                    error['value'],
                    error['traceback']
                )

                error_data = {
                    'errtype': error['type'].__name__,
                    'msg': error['value'],
                    'tb': ''.join(error_msg)
                }

                failure_node = document.createElement('failure')
                failure_node.setAttribute('type', str(error_data['errtype']))
                failure_node.setAttribute('message', str(error_data['msg']))
                failure_text = document.createTextNode(str(error_data['tb']))
                failure_node.appendChild(failure_text)
                testcase_node.appendChild(failure_node)
            if test.get('skip', None):
                skip_node = document.createElement('skipped')
                skip_node.setAttribute('message', str(test['skip']))
                testcase_node.appendChild(skip_node)

        for ctx in context['contexts']:
            self.create_test_case_elements(document, parent_node, ctx)
