rules.caption = "Culo"
rules.description = "Game of Culo"
rules.playzone = 1
rules.throws = {}
rules.players = {}
rules.winers = {}

rules.deckdraws = list {
    {
        name = "Mazo para robar",
        numbers = list {"As", 2, 3, 4, 5, 6, 7, "J", "Q", "K"},
        --numbers = list {"2","4"},
        suits = list {"spades", "diamonds", "clubs", "hearts"}
        --suits = list {"spades"}
    },  
}

--[[rules.keys_descriptions="\
F5:Reload  Esc:Exit  Down:Toggle Fullscreen  D:Draw a card \
[1-10]:Add to/Rem from Selection  Z:Clear Selection  T,Return:Throws \
E:End Turn  S:Sort P:Pass Turn F1-4:Choose User  F12:None User"]]

rules.keys_descriptions="\
F5:Reload  Esc:Exit  Down:Toggle Fullscreen  D:Draw a card \
Z:Clear Selection  T,Return:Throws 1:prueba1  2:prueba2\
S:Sort P:Pass Turn F1-4:Choose User  F12:None User  UP:showalt"

rules.down_func= dict {
    s      =  list {"sort('points')", "local"},
    z      =  list {"clear_selection", "global"}, 
    t      =  list {"throw_cards", "global"}, 
    ret    =  list {"throw_cards", "global"}, 
    e      =  list {"end_turn", "global"}, 
    d      =  list {"draw_a_card", "global"}, 
    p      =  list {"pass_turn", "global"}, 
    down   =  game.toggle_fullscreen ,
    F5     =  game.show, 
    UP     =  game.showalt, 
    esc    =  game.exit, 
    [1]    =  game.prueba1,
    [2]    =  game.prueba2, 
    F1     =  game.F1, 
    F2     =  game.F2, 
    F3     =  game.F3, 
    F4     =  game.F4, 
    F12    =  game.F12,
}
 
function rules:points(number,suit)
    if number=="As" then
        r = 14
    elseif number=="J" then
        r = 11
    elseif number=="Q" then
        r = 12
    elseif number=="K" then
        r = 13
    else
        r = number
    end
    return r
end
        
function rules:new_round()
    self.throws = {}
    self.players = {}
    game.deckdraws[0].shuffle()
    game.deal(60) --repartir cartas 
end
    
function rules:pass_turn()
    if game.pass_turns_counter == len(game.players)-1 then
        --dar el turno al jugador que tiro la ultima carta, no hace falta porque casualmente es el siguiente
        --#self.gamezone.players.index( self.throws[len(self.throws)-1][0].previous_owner)
        game.clear_playzone()
        self.throws = {}
    end
end

function rules:throw_cards(selection)
    table.insert(self.throws, selection)
    game.ending_turn()
end

function rules:throwable_selection(selection)
    --tiene que haber algo seleccionado
    if #selection==0 then return false end
    
    --obtenemos el numero y todos han de ser iguales
    number=selection[1].number

    for k,card in pairs(selection) do 
        if card.number ~= number then return false end
    end
    
    --si se cumple lo anterior y no ha habido tiradas, cualquiera es valida
    if #self.throws == 0 then
        return true
    --si ya hay tiradas entonces tendran que comprobarse mas parametros 
    else
        last_throw = self.throws[#self.throws]
        --print ("...::...")
        --for k, v in pairs(last_throw) do print (k, v) end
        --print ("...::...")
        if #selection == #last_throw then
            if selection[1].points > last_throw[1].points then
                return true
            end
        end
        return false
    end
end

function index(table,elem)
    local r = nil
    for k,v in pairs(table) do
        if v == elem then
            r = k
            break
        end
    end
    return r
end

function rules:is_round_finished()
    local r = true
    for p, player in enumerate(game.players) do 
        if len(player) ~= 0 then
             r = false
        else
            if not index(self.players, p) then
                table.insert(self.players, p)
            end
        end
    end
    return r
end


function rules:end_of_round()
    print()
    print ("end of round " .. game.round)
    for pos, player in pairs(self.players) do print(pos, game.players[player].id) end
    table.insert(self.winers, self.players)
    print()
end

function rules:is_game_finished() 
    if game.round == 3 then
        return true
    else
        return false
    end
end


function rules:end_game()

    for round, players in pairs(self.winers) do
        for pos, player in pairs(players) do print(round, pos, game.players[player].id) end
        print()
    end

    exit()
end

function rules:new_turn()
    if len(game.player) == 0 then
        game.pass_turn()
    end
end
