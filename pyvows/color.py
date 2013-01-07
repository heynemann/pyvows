# -*- coding: utf-8 -*-
'''PyVows' support for color-printing to the terminal.

Currently, just a thin wrapper around the (3rd-party) `colorama` module.
'''


# pyvows testing engine
# https://github.com/heynemann/pyvows

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 Bernardo Heynemann heynemann@gmail.com

try:
    from colorama import init, Fore, Style
    init(autoreset = True)
except ImportError:
    class NoColor(object):
        '''When Python can't import `colorama`, this stand-in class prevents
        other parts of PyVows from throwing errors when attempting to print
        in color.
        '''
        def __getattr__(self, *args, **kwargs):
            return ""

    Fore  = NoColor()
    Style = NoColor()


__all__ = [
    'Fore', 'Style',
    'BLACK', 'BLUE', 'CYAN', 'GREEN', 'RED', 'YELLOW', 'WHITE', 'RESET',
    'black', 'blue', 'cyan', 'green', 'red', 'yellow', 'white'
]


#
#   Color convenience vars
#
BLACK  = Fore.BLACK
BLUE   = Fore.BLUE   + Style.BRIGHT
CYAN   = Fore.CYAN   + Style.BRIGHT
GREEN  = Fore.GREEN  + Style.BRIGHT
RED    = Fore.RED    + Style.BRIGHT
YELLOW = Fore.YELLOW + Style.BRIGHT
WHITE  = Fore.WHITE  + Style.BRIGHT
#
RESET  = Fore.RESET  + Style.RESET_ALL


#
#   Functions
#
def _colorize(msg, color, reset=True):
    reset = RESET if reset else ''
    return '{COLOR}{0!s}{RESET}'.format(msg, COLOR=color, RESET=reset)

black  = lambda msg: _colorize(msg, BLACK)
blue   = lambda msg: _colorize(msg, BLUE)
cyan   = lambda msg: _colorize(msg, CYAN)
green  = lambda msg: _colorize(msg, GREEN)
red    = lambda msg: _colorize(msg, RED)
yellow = lambda msg: _colorize(msg, YELLOW)
white  = lambda msg: _colorize(msg, WHITE)

