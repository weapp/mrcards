game.caption = "Culo"
game.descruption = "Game of Culo"
game.playzone = 1

game.deckdraws = {
    {
        name = "Mazo para robar",
        numbers = {"As", 2, 3, 4, 5, 6, 7, "J", "Q", "K"},
        suits = {"spades", "diamonds", "clubs", "hearts"}
    }
}

game.keys_descriptions="\
F5:Reload  Esc:Exit  Down:Toggle Fullscreen  D:Draw a card \
[1-10]:Add to/Rem from Selection  Z:Clear Selection  T,Return:Throws \
E:End Turn  S:Sort P:Pass Turn F1-4:Choose User  F12:None User"

game.down_func={
    K_DOWN   =   {"pygame.display.toggle_fullscreen()","local"} ,
    K_ESCAPE =   {"self.exit()","local"}, 
    K_F5     =   {"self.show()","local"}, 
    K_UP     =   {"self.showalt()","local"}, 
    K_z      =   {"self.clear_selection","global"}, 
    K_t      =   {"self.throw_cards","global"}, 
    K_RETURN =   {"self.throw_cards","global"}, 
    K_e      =   {"self.end_turn()","global"}, 
    K_s      =   {"self.sort('points')","local"}, 
    K_d      =   {"self.draw_a_card","global"}, 
    K_p      =   {"self.pass_turn","global"}, 

    K_1       =   prueba1, 
    K_2       =   prueba2, 

    K_F1      =   F1, 
    K_F2      =   F2, 
    K_F3      =   F3, 
    K_F4      =   F4, 
    K_F12     =   F12, 
}
 
function game:points(number,suit)
    if number=="As" then
        r=14
    elseif number=="J" then
        r=11
    elseif number=="Q" then
        r=12
    elseif number=="K" then
        r=13
    else
        r=number
    end
    return r
end
        
function game:init()
    getattr(deckdraws[0], 'shuffle')()
    deal(60) --repartir cartas    
end
    
function game:pass_turn()
    if self.gamezone.pass_turns_counter==len(self.gamezone.players)-1 then
        --dar el turno al jugador que tiro la ultima carta, no hace falta porque casualmente es el siguiente
        --#self.gamezone.players.index( self.throws[len(self.throws)-1][0].previous_owner)
        
        self.clear_playzone()
        --del self.throws[:]
        for k in self.throws do table.remove(self.throws,k) end
        
        self.throws = {}
    end
end

function game:throw_cards(selection)
    ending_turn()
    table.insert(self.throws, selection)
end

function game:throwable_selection(selection)
    --tiene que haber algo seleccionado
    if len(selection)==0 then return false end
    
    --obtenemos el numero y todos han de ser iguales
    
    number=selection[1].number

    --for card in selection
    --    if not card.number==number then return false end
    
    for k,card in pairs(selection) do 
        if not card.number == number then return false end
    end
    
    --si se cumple lo anterior y no ha habido tiradas, cualquiera es valida
    if len(self.throws) == 0 then
        return true
    --si ya hay tiradas entonces tendran que comprobarse mas parametros 
    else
        last_throw=self.throws[len(self.throws)]
        if len(selection)==len(last_throw) then
            if selection[1].points > last_throw[1].points then
                return true
            end
        end
        return false
    end
end


