# -*- coding: utf-8 -*-
'''Utility functions for all implementations of pyvows.runner.
 
'''
import os.path as path

#-------------------------------------------------------------------------------------------------

def get_code_for(obj):
    #   FIXME: Add Comment description
    code = None
    if hasattr(obj, '__code__'):
        code = obj.__code__
    elif hasattr(obj, '__func__'):
        code = obj.__func__.__code__
    return code
 
 
def get_file_info_for(member):
    #   FIXME: Add Docstring
    code = get_code_for(member)
 
    filename = code.co_filename
    lineno = code.co_firstlineno
 
    return filename, lineno
 
 
def get_topics_for(topic_function, ctx_obj):
    #   FIXME: Add Docstring
    if not ctx_obj.parent:
        return []
 
    # check for decorated topic function
    if hasattr(topic_function, '_original'):
        # _wrapper_type is 'async_topic' or 'capture_error'
        _async = (getattr(topic_function, '_wrapper_type', None) == 'async_topic')
        topic_function = topic_function._original
    else:
        _async = False
 
    code = get_code_for(topic_function)
 
    if not code:
        raise RuntimeError(
            'Function %s does not have a code property' % topic_function)
 
    expected_args = code.co_argcount - 1
 
    # taking the callback argument into consideration
    if _async:
        expected_args -= 1
 
    # prepare to create `topics` list
    topics = []
    child = ctx_obj
    context = ctx_obj.parent
 
    # populate `topics` list
    for i in range(expected_args):
        topic = context.topic_value
 
        if context.generated_topic:
            topic = topic[child.index]
 
        topics.append(topic)
 
        if not context.parent:
            break
 
        context = context.parent
        child = child.parent
 
    return topics
