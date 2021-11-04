#!/usr/bin/python3 
# by kaosxx88 
# Color settings for debugging and output 

import datetime
from colorama import Fore, Style, init

# colorama start functions ( for windows OS )
init()

###################################################
############### LOGS COLORS CLASS #################
###################################################

class D():
    '''
    Debug output class, (set active to False to hide the output) 
    '''
    active = True
    def d(x):        
        if D.active == True: 
            print (f'{C.debug}{x}')
        with open('nirema_log.log','a+') as f: f.write(f'[-] {datetime.datetime.now().strftime("%Y-%m-%d %H:%M")} {x}\n')
        
class I():
    '''
    Info - System output class, set active to False to hide the output
    '''
    def i(x):
        print(f'{C.info}{x}')
        with open('nirema_log.log','a+') as f: f.write(f'[+] {datetime.datetime.now().strftime("%Y-%m-%d %H:%M")} {x}\n')

class E():
    ''' 
    Errors output class
    '''    
    def e(x):
        print (f'{C.error}{x}')
        with open('nirema_log.log','a+') as f: f.write(f'[!] {datetime.datetime.now().strftime("%Y-%m-%d %H:%M")} {x}\n')

class X():
    '''
    Debug extra class, set active to False to hide output on the log file 
    '''
    active = False
    def x(x):
        message = f'{C.debug}{x}'
        if X.active == True: 
            print(message)
            with open('nirema_log.log','a+') as f: f.write(f'[-] {datetime.datetime.now().strftime("%Y-%m-%d %H:%M")} {x}\n')


###################################################
################### COLOR CLASS ###################
###################################################


# color class project
class C:
    ''' Creation of color output '''
    #
    # COLORS
    #
    r = Fore.RED
    g = Fore.GREEN
    c = Fore.CYAN
    y = Fore.YELLOW
    m = Fore.MAGENTA
    #
    # RESET
    #
    x = Style.RESET_ALL
    #
    # TAGS
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
    # FUNCTIONS TO COLOR
    #
    def cyan(x):            return C.c+'['+x+']'+C.x        
    def yellow(x):          return C.y+'['+x+']'+C.x 
    def green(x):           return C.g+'['+x+']'+C.x 
    def red(x):             return C.r+'['+x+']'+C.x 
    def green_clean(x):     return f'{C.g}{x}{C.x}' 
    def magenta_clean(x):   return f'{C.m}{x}{C.x}' 
    def cyan_clean(x):      return f'{C.c}{x}{C.x}' 
    def red_clean(x):       return f'{C.r}{x}{C.x}' 
    def yellow_clean(x):    return f'{C.y}{x}{C.x}' 

#
# RESIZE THE NAME TAG
#
def name_tag_modder(n1ckname):
    #
    # format the name as max len ($size)
    #
    size = 8
    
    if len(n1ckname) >= size:  return f'[{n1ckname[:size]}]'

    for i in range(size - len(n1ckname)):
        if i % 2 == 0 : n1ckname = f'{n1ckname} '
        else: n1ckname = f' {n1ckname}'
    return f'[{n1ckname}]'