import sys
import socket
import network_buffer
from comprobar import comprobar_error

"""
Protocolo para MRcard
    #Conexion
    SYN:version #C
    ACK:        #S

    #Vemos los jugadores y montones que hay
    YOU:ID      #S
    NAME:nombre #C
    PLAYER:nombre,ID #S
    ...
    SET:nombre,ID   #S
    ...

    #Se reparten las cartas donde ID=O es el mazo inicial
    START:  #S
    MOVE:0,ID_a_donde_se_manda,numero_cartas    #S
    ...
    VMOVE:0,ID_a_donde_se_manda,n-p,n-p,n-p...  #S

    #Los jugadores no tienen turno, si intentas tirar cartas
    #cuando no es tu turno te da mensaje de error
    #Sin embargo se mandan mensajes con quien es el turno
    MSG:Turn ID     #S

    THROW:ID,n-p,n-p,n-p   #C
    MOVE:ID,ID,numero_cartas    #S
    VMOVE:ID,ID,n-p,n-p,n-p...  #S

    WIN:    #S
    LOSE:   #S
"""

class Client:
    def __init__(self, port = 12345):
        """
            Se conecta al puerto del servidor
        """
        #Creamos socket y se inicaliza
        self.nb=network_buffer.NetworkBuffer(port)

    def lanzar(self):
        #Mandamos mensaje de conectar SYN
        self.nb.send_msg("SYN:")

        #Esperamos a que nos llegue algun mensaje
        while self.nb.number_msg() == 0:
            pass
        received_m=self.nb.recv_msg()
        comprobar_error(received_m,"ACK")

        print "Nos conectamos al servidor"

        #Vemos que jugador somos y le mandamos nuestro nombre
        received_m= self.nb.recv_msg()
        comprobar_error(received_m,"YOU")

        self.ID=received_m.split(":")[1]
        print "Somos el jugador numero: ", self.ID
        self.nb.send_msg("NAME:danigm")

        #Recibimos las cartas
        while self.nb.number_msg() == 0:
            pass
        received_m= self.nb.recv_msg()

        comprobar_error(received_m,"CARDS")

        mazo=received_m.split(":")[1]
        print "Nuestras Cartas son"
        for card in mazo.split(";"):
            numero,palo=card.split(",")
            print numero, palo

        while self.nb.number_msg() == 0:
            pass
        received_m=self.nb.recv_msg()
        while received_m.split(":")[0]=="PLAYER":
            jugador=received_m.split(":")[1]
            print "Jugador de nombre:", jugador.split(",")[0]
            print "ID:", jugador.split(",")[1], "cartas:", jugador.split(",")[2]
            while self.nb.number_msg() == 0:
                pass
            received_m=self.nb.recv_msg()

        comprobar_error(received_m,"START")
        print "Empieza el juego"

        while self.nb.number_msg() == 0:
            pass
        received_m=self.nb.recv_msg()
        comprobar_error(received_m,"TURN")
        print "Es nuestro turno escribe THROW: o PASS:"

        data = raw_input('>')
        self.nb.send_msg(data)
        self.nb.__del__()


if __name__ == '__main__':
    print "Iniciando"
    cs = Client()
    cs.lanzar()
    print "Finalizado"
