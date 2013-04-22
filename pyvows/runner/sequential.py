# -*- coding: utf-8 -*-
'''This is the slowest of PyVows' runner implementations.  But it's also dependency-free; thus, 
it's a universal fallback.  

'''

from pyvows.runner.utils import get_code_for, get_file_info_for, get_topics_for

class VowsSequentialRunner(object):
    pass