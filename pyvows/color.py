# -*- coding: utf-8 -*-
'''PyVows' support for color-printing to the terminal.

Currently, just a thin wrapper around the (3rd-party) `colorama`
module.

'''

# pyvows testing engine
# https://github.com/heynemann/pyvows

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 Bernardo Heynemann heynemann@gmail.com

try:
    from colorama import init, Fore, Style
    init(autoreset=True)
except ImportError:
    class NoColor(object):
        '''When Python can't import `colorama`, this stand-in class prevents
        other parts of PyVows from throwing errors when attempting to print
        in color.

        '''
        def __getattr__(self, *args, **kwargs):
            return ''

    Fore = NoColor()
    Style = NoColor()

#-------------------------------------------------------------------------------------------------

__all__ = [
    'Fore', 'Style',
    'BLACK', 'BLUE', 'CYAN', 'GREEN', 'RED', 'YELLOW', 'WHITE', 'RESET', 'RESET_ALL',
    'black', 'blue', 'cyan', 'green', 'red', 'yellow', 'white', 'bold', 'dim'
]


#-------------------------------------------------------------------------------------------------
#   Color Constants
#-------------------------------------------------------------------------------------------------
BLACK = Fore.BLACK
BLUE = Fore.BLUE
CYAN = Fore.CYAN
GREEN = Fore.GREEN
RED = Fore.RED
YELLOW = Fore.YELLOW
WHITE = Fore.WHITE
#
BOLD = Style.BRIGHT
DIM = Style.DIM
#
RESET = Fore.RESET
RESET_ALL = Style.RESET_ALL

#-------------------------------------------------------------------------------------------------
#   Functions
#-------------------------------------------------------------------------------------------------
def _colorize(msg, color, reset=True):
    reset = RESET if reset else ''
    return '{COLOR}{0!s}{RESET}'.format(msg, COLOR=color, RESET=reset)


def _bold(msg):
    return '{BOLD}{0!s}{RESET_ALL}'.format(msg, BOLD=BOLD, RESET_ALL=RESET_ALL)


def _dim(msg):
    return '{DIM}{0!s}{RESET_ALL}'.format(msg, DIM=DIM, RESET_ALL=RESET_ALL)


black = lambda msg: _colorize(msg, BLACK)
blue = lambda msg: _colorize(msg, BLUE)
cyan = lambda msg: _colorize(msg, CYAN)
green = lambda msg: _colorize(msg, GREEN)
red = lambda msg: _colorize(msg, RED)
yellow = lambda msg: _colorize(msg, YELLOW)
white = lambda msg: _colorize(msg, WHITE)

bold = lambda msg: _bold(msg)
dim = lambda msg: _dim(msg)
