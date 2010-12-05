import functools
import pygame
from lupa import LuaRuntime

def load(filename, pyvars, objs, lua):
    lua.execute("""\
rules = {
    select = function() end,
    clear_selection = function() end,
    throw_cards = function(selection) end,
    throwable_selection = function(selection) return true end,
    draw_a_card = function() end,
    deal = function() end,
    pass_turn = function() end,
    end_turn = function() end,
    ending_turn = function() end,
    is_round_finished = function() return false end,
    end_of_round = function() end,
    new_round = function() end,
    new_turn = function() end,
    terminable_turn = function() return true end,
    points = function() return 1 end,
    init = function() end,
    deckdraws = {},
    caption = "Sin Nombre",
    descruption = "Sin Descripcion",
    playzone = 1,
    keys_descriptions="",
    down_func={},
    throws = {}
}
py = {}
""")
    lua.globals()["list"] = lambda elem: list(elem.values())
    lua.globals()["keys"] = lambda elem: dict((getattr(pygame, key), strfunc) \
                            for key,strfunc in elem.items() )
    lua.globals()["list2table"] = lambda elem: lua.table(*elem)
    for key, value in pyvars.items():
       lua.globals()[key] = value
    for key, value in objs.items():
       lua.globals()['py'][key] = value
    lua.globals()["list"] = lambda elem: list(elem.values())
    #print [a for a in lua.globals().items() if a[0] == "python"]
    f = file('rules/' + filename + '.lua')
    code = f.read()
    f.close()
    lua.execute(code)
    lua.execute("""\
irules = {
    caption = rules.caption,
    description = rules.description,
    playzone = rules.playzone,
    deckdraws = rules.deckdraws,
    keys_descriptions = rules.keys_descriptions,
    down_func = rules.down_func,
    throwable_selection = function(selection) return rules:throwable_selection(list2table(selection)) end,
    throw_cards = function(selection) return rules:throw_cards(list2table(selection)) end,
    new_round = function() return rules:new_round() end,
    select = function() return rules:select() end,
    clear_selection = function() return rules:clear_selection() end,
    draw_a_card = function() return rules:draw_a_card() end,
    deal = function() return rules:deal() end,
    pass_turn = function() return rules:pass_turn() end,
    end_turn = function() return rules:end_turn() end,
    ending_turn = function() return rules:ending_turn() end,
    is_round_finished = function() return rules:is_round_finished() end,
    end_of_round_roun = function() return rules:end_of_round() end,
    new_turn = function() return rules:new_turn() end,
    terminable_turn = function() return rules:terminable_turn() end,
    points = function(number,suit) return rules:points(number,suit) end,
    init = function() return rules:init() end
}    """)

    return lua.eval("irules")
    

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
