import functools
import pygame
from lupa import LuaRuntime

def load(filename, pyvars, objs, lua):
    lua.execute("""game = {}""")
    lua.execute("""py = {}""")

    for key, value in objs.items():
       lua.globals()['py'][key] = value
       
    for key, value in pyvars.items():
       lua.globals()[key] = value

    
    #print [a for a in lua.globals().items() if a[0] == "python"]
    f = file('rules/' + filename + '.lua')
    code = f.read()
    f.close()
    lua.execute(code)
    
    rules =  lua.eval("game")
    
    
    
    
    #down_func...
    t = {}
    
    def fun(tup):
        tup = list(tup)
        tup[0] = getattr(pygame, tup[0])
        if hasattr(tup[1],'values'):
            tup[1] = list(tup[1].values())
        return tup
    
    t.update(map(fun,rules.down_func.items()))
    rules.down_func = t
    del t
    #...down_func
    
    #deck_draws...
    
    for k, ideck in rules.deckdraws.items():
        t = {
            "name" : ideck.name,
            "numbers" : list(ideck.numbers.values()),
            "suits" : list(ideck.suits.values()),
        }
        rules.deckdraws[k] = t

    rules.deckdraws = list(rules.deckdraws.values())

    #...deck_draws
    
    
    return rules
    

lua = LuaRuntime()
lua.execute("""python = nil""")


load = functools.partial(load, lua=lua)


"""
import sys
orig_dlflags = sys.getdlopenflags()
sys.setdlopenflags(258)
import lupa
sys.setdlopenflags(orig_dlflags)
"""
