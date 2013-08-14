# -*- coding: utf-8 -*-
'''Utility functions for all implementations of pyvows.runner.

'''
import inspect
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
    filename, lineno = code.co_filename, code.co_firstlineno
    return filename, lineno

def get_topics_for(topic_function, ctx_obj):
    #   FIXME: Add Docstring
    if not ctx_obj.parent:
        return []

    # check for async topic
    if hasattr(topic_function, '_original'):
        topic_function = topic_function._original
        async = True
    else:
        async = False

    code = get_code_for(topic_function)

    if not code:
        raise RuntimeError('Function %s does not have a code property')

    expected_args = code.co_argcount - 1

    # taking the callback argument into consideration
    if async:
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

def get_vows_and_subcontexts(ctx_obj, exclusion_patterns):
    '''Returns a (vows, subcontexts) tuple of the contents of `ctx_obj`. Any 
    vows or subcontexts whose name matches any `exclusion_patterns` will
    not be included.  

    `exclusion_patterns` should be a set of compiled regular expression objects.

    '''

    def _is_excluded(name, exclusion_patterns):
        '''Return whether `name` is in `self.exclusion_patterns`.'''
        for pattern in exclusion_patterns:
            if pattern.search(name):
                return True
        return False

    # removes any special methods from ctx_members
    filterfunc = lambda member: not any((
        member[0] in ctx_obj.ignored_members,
        member[0].startswith('_'),
        _is_excluded(member[0], exclusion_patterns)
    ))

    ctx_members = filter(filterfunc, inspect.getmembers(type(ctx_obj)))

    # now separate out the two types we're concerned with
    vows = frozenset(vow for vow_name, vow in ctx_members if inspect.ismethod(vow))
    subcontexts = frozenset(subctx for subctx_name, subctx in ctx_members if inspect.isclass(subctx))

    return vows, subcontexts
