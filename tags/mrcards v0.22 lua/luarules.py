import functools
import pygame
from lupa import LuaRuntime

def load(filename, pyvars, objs, lua):
    lua.execute("""\
game = {}
py = {}
function game:select() end
function game:clear_selection() end
function game:throw_cards(selection) end
function game:throwable_selection(selection) return true end
function game:draw_a_card() end
function game:deal() end
function game:pass_turn() end
function game:end_turn() end
function game:ending_turn() end
function game:is_round_finished() return false end
function game:end_of_round_roun() end
function game:new_turn() end
function game:terminable_turn() return true end
function game:points() return 1 end
function game:init() end
game.deckdraws = {}
game.caption = "Sin Nombre"
game.descruption = "Sin Descripcion"
game.playzone = 1
game.keys_descriptions=""
game.down_func={}
game.throws = {}
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
            if attr in ["throwable_selection", "throw_cards"]:
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
    
    rules =  lua.eval("game")
    
    
    """
    rulesthrowable_selection = rules.throwable_selection
    def throwable_selection (self, selection):
        table = lua.table(*selection)
        return rulesthrowable_selection(self, table)
    rules.throwable_selection = throwable_selection

    rulesthrow_cards = rules.throw_cards
    def throw_cards (self, selection):
        table = lua.table(*selection)
        return rulesthrow_cards(self, table)
    rules.throw_cards = throw_cards
    """
    
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
