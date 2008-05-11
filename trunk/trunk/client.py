import sys
import socket
from comprobar import comprobar_error

"""
Servidor para MRcard
 * servidor:
    start: j,n;p,n;p,n;p  -> split(',') -> split(';')
    player: j,n
    turn: # directo a un jugador
    ack: confirmacion
    nack:msg
    win:
    lose:
    thrown:j,n;p,n;p...

 * cliente:
    syn:autenticacion
    pass: paso de turno
    throw:n;p,n;p ...
    exit:
"""
class Client:
    def __init__(self, puerto = 12345):
        """
        Se conecta al puerto del servidor
        """
        self.cs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.cs.connect(("",puerto))
            print "conectado a localhost al puerto 12345"
        except:
            puerto = puerto + 1
            print "error al conectar con localhost, probando con puerto 12346"
            try:
                self.cs.connect(("",puerto))
            except:
                print "\nimposible conectar a localhost\n"
                sys.exit(-1)
        #self.ss.listen(10)
        #self.cn = 0 #numero de jugadores
        #self.sock = {} #cada jugador escribira en un socket
        #self.addr = {} #direccion de cada jugador

    def lanzar(self):
        #Mandamos mensaje de conectar SYN
        self.cs.send("SYN:\r\n")

        #Comprobamos que todo ha ido bien
        received_m= self.cs.recv(1024)
        comprobar_error(received_m,"ACK")

        print "Nos conectamos al servidor"

        self.cs.send("mando algo para partir los mensajes")

        #Vemos que jugador somos y le mandamos nuestro nombre
        received_m= self.cs.recv(1024)
        comprobar_error(received_m,"YOU")

        self.ID=received_m.split(":")[1]
        print "Somos el jugador numero: ", self.ID
        self.cs.send("NAME:danigm\r\n")

        #Recibimos las cartas
        received_m= self.cs.recv(1024)

        comprobar_error(received_m,"CARDS")

        mazo=received_m.split(":")[1]
        print "Nuestras Cartas son"
        for card in mazo.split(";"):
            numero,palo=card.split(",")
            print numero, palo

        self.cs.send("mando algo para partir los mensajes")
        received_m=self.cs.recv(1024)
        while received_m.split(":")[0]=="PLAYER":
            jugador=received_m.split(":")[1]
            print "Jugador de nombre:", jugador.split(",")[0]
            print "ID:", jugador.split(",")[1], "cartas:", jugador.split(",")[2]
            self.cs.send("mando algo para partir los mensajes")
            received_m=self.cs.recv(1024)

        comprobar_error(received_m,"START")
        print "Empieza el juego"

        self.cs.send("mando algo para partir los mensajes")

        received_m=self.cs.recv(1024)
        comprobar_error(received_m,"TURN")
        print "Es nuestro turno escribe THROW o PASS"

        data = raw_input('>')
        self.cs.send(data)
        self.cs.close()


if __name__ == '__main__':
    print "Iniciando"
    cs = Client()
    cs.lanzar()
    print "Finalizado"
