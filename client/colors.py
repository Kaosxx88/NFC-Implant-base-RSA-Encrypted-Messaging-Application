#!/usr/bin/env python3
# Autor @kaosxx88
# function and class for color output on the command line interface

# import colorama 
from colorama import Fore, Style, init

init()
# debug options
class D():
    ''' Debug class, set active to False to hide '''
    active = True
    def d(x):
        if D.active == True: print(f'{C.debug}{x}')
        
# System message
class I():
    ''' Info class '''

    def i(x):
        print(f'{C.info}{x}')

class E():
    ''' Error class '''

    def e(x):
        print(f'{C.error}{x}')

# color class project
class C:
    ''' color setting '''
    # colors
    #
    r = Fore.RED
    g = Fore.GREEN
    c = Fore.CYAN
    y = Fore.YELLOW
    m = Fore.MAGENTA
    #
    # reset
    #
    x = Style.RESET_ALL
    #
    # tags
    #
    info        = f'{c}[ INFO   ]{x} '
    input_name  = f'{y}[INPUT]{x} '
    mex         = f'{g}[  MEX  ]{x} '
    arrow       = f'{g}  --->{x} '
    arrow_cyan  = f'{c}  --->{x} '
    error       = f'{r}[ ERROR  ]{x} '
    system      = f'{r}[{y}SYSTEM{r}]{x} '
    chat        = f'{y}[ CHAT ] {x}'
    debug       = f'{y}[ DEBUG  ]{x} '


    #
    # functions
    #
    def cyan(x): return C.c+'['+x+']'+C.x        
    def yellow(x): return C.y+'['+x+']'+C.x 
    def green(x): return C.g+'['+x+']'+C.x 
    def red(x): return C.r+'['+x+']'+C.x 
    def magenta(x): return C.m+'['+x+']'+C.x 
    def green_clean(x): return f'{C.g}{x}{C.x}' 
    def magenta_clean(x): return f'{C.m}{x}{C.x}' 
    def cyan_clean(x): return f'{C.c}{x}{C.x}' 
    def red_clean(x): return f'{C.r}{x}{C.x}' 
    def yellow_clean(x): return f'{C.y}{x}{C.x}' 



def name_tag_modder(n1ckname):
    size = 8
    ''' format the name as max len 10'''
    if len(n1ckname) >= size:  return f'[{n1ckname[:size]}]'

    for i in range(size - len(n1ckname)):
        if i % 2 == 0 : n1ckname = f'{n1ckname} '
        else: n1ckname = f' {n1ckname}'
    return f'[{n1ckname}]'