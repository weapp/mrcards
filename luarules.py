import functools
import pygame
from lupa import LuaRuntime

def load(filename, pyvars, objs, lua):
    lua.execute("""\
rules = {}
py = {}
function rules:select() end
function rules:clear_selection() end
function rules:throw_cards(selection) end
function rules:throwable_selection(selection) return true end
function rules:draw_a_card() end
function rules:deal() end
function rules:pass_turn() end
function rules:end_turn() end
function rules:ending_turn() end
function rules:is_round_finished() return false end
function rules:end_of_round() end
function rules:new_round() end
function rules:new_turn() end
function rules:terminable_turn() return true end
function rules:points() return 1 end
function rules:init() end
rules.deckdraws = {}
rules.caption = "Sin Nombre"
rules.descruption = "Sin Descripcion"
rules.playzone = 1
rules.keys_descriptions=""
rules.down_func={}
rules.throws = {}
""")

    for key, value in objs.items():
       lua.globals()['py'][key] = value
       
    for key, value in pyvars.items():
       lua.globals()[key] = value

    
    #print [a for a in lua.globals().items() if a[0] == "python"]
    f = file('rules/' + filename + '.lua')
    code = f.read()
    f.close()
    lua.execute(code)
    
    class rules_prox:
        def __init__(self, rules):
            self.rules = rules

        def __getattr__(self, attr):
            if attr == "down_func":
                return dict((getattr(pygame, key), list(strfunc.values()) if \
                             hasattr(strfunc,'values') else strfunc) \
                            for key,strfunc in self.rules.down_func.items() )
            elif attr in ["throwable_selection", "throw_cards"]:
                f = getattr(self.rules, attr)
                def colons(selection):
                    return f(self.rules, lua.table(*selection))
                return colons
            elif attr in ["select", "clear_selection", "draw_a_card", "deal", "pass_turn", "end_turn", "ending_turn", "is_round_finished", "end_of_round_roun", "new_turn", "terminable_turn", "points", "init"]:
                f = getattr(self.rules, attr)
                def colons(*args, **kws):
                    return f(self.rules, *args, **kws)
                return colons
            else:
                return getattr(self.rules, attr)
    
    rules =  lua.eval("rules")
    
    
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
    
    rules = rules_prox(rules)
    
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
