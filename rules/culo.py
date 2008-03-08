game=False
throws=[]

def register_gamezone(gz):
    global game
    game=gz
    
caption="Culo"
playzone=True
deckdraws=[{"name":"Mazo para robar","numbers":["As",2,3,4,5,6,7,"J","Q","K"],"suits":["espadas","oros","bastos","copas"]}]

def points(number,suit):
    if number=="As":
        r=14
    elif number=="J":
        r=11
    elif number=="Q":
        r=12
    elif number=="K":
        r=13
    else:
        r=number
    return r
    
def init():
    game.deckdraws[0].shuffle()
    game.deal(60) #repartir cartas    
    
down_func='''{
    pygame.K_DOWN   :   [pygame.display.toggle_fullscreen,[]] , \
    pygame.K_ESCAPE :   sys.exit, \
    pygame.K_F5     :   game.show, \
    pygame.K_1      :   [game.select,0], \
    pygame.K_2      :   [game.select,1], \
    pygame.K_3      :   [game.select,2], \
    pygame.K_4      :   [game.select,3], \
    pygame.K_5      :   [game.select,4], \
    pygame.K_6      :   [game.select,5], \
    pygame.K_7      :   [game.select,6], \
    pygame.K_8      :   [game.select,7], \
    pygame.K_9      :   [game.select,8], \
    pygame.K_0      :   [game.select,9], \
    pygame.K_z      :   game.clear_selection, \
    pygame.K_t      :   game.throw_cards, \
    pygame.K_RETURN :   game.throw_cards, \
    pygame.K_e      :   game.end_turn, \
    pygame.K_s      :   game.sort_by_points, \
    pygame.K_d      :   game.draw_a_card, \
    pygame.K_p      :   game.pass_turn
}'''

#    pygame.K_p      :   game.sort_by_points, \

#

def pass_turn():
    if game.pass_turns_counter==len(game.players)-1:
        print "han pasado todos"
        #dar el turno al jugador que tiro la ultima carta
        print game.players.index( throws[len(throws)-1][0].previous_owner)
        del game.playzone[0].cards[:]
        del throws[:]
        print "<-----"


def throw_cards(selection):
    game.ending_turn()
    throws.append(selection)
        
def throwable_selection(selection):
    #tiene que haber algo seleccionado
    if len(selection)==0:return False
    
    #obtenemos el numero y todos han de ser iguales
    number=selection[0].number
    for card in selection:
        if not card.number==number: return False
    
    #si se cumple lo anterior y no ha habido tiradas, cualquiera es valida
    if len(throws)==0:
        return True
    
    #si ya hay tiradas entonces tendran que comprobarse mas parametros 
    else:
        last_throw=throws[len(throws)-1]
        if len(selection)==len(last_throw):
            if selection[0].points>last_throw[0].points:
                return True
        return False
        

