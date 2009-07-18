import sys
import socket
import game
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
class Server:
    def __init__(self, port = 12345):
        self.create_game()
        """
        Abre un puerto en la maquina local, y espera cn conexiones
        """
        #Creamos el socket
        self.ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            #Asociamos el socket al puerto del ordenador
            self.ss.bind(("",port))
        except:
            print "error conectando al puerto 12345"
            sys.exit(-1)
        #Hacemos que escuche el socket
        self.ss.listen(10)
        #numero de jugadores
        self.n_players = 0
        #cada jugador escribira en un socket
        self.sock = {}
        #direccion de cada jugador
        self.addr = {}

    def lanzar(self):
        print "Esperando conexion"
        #Accept devuelve un socket (player1) y su direcion
        self.player1, self.player1_addr = self.ss.accept()
        print self.player1_addr


        #Mensaje para conectar
        syn_m = self.player1.recv(1024)
        #comprobamos que sea SYN y si no se sale
        comprobar_error(syn_m,"SYN")
        print "usuario conectado", self.player1_addr

        #Lo aceptamos
        self.player1.send("ACK:\r\n")

        # ID del jugador
        self.player1.send("YOU:2\r\n")

        name_m=self.player1.recv(1024)
        comprobar_error(name_m,"NAME")
        name=name_m.split(":")[1]
        print "Nombre del jugador ",name

        self.player1.send("CARDS:2,3;12,0;1,1;2,1")

        # los demas jugadores y su numero de cartas inicial
        self.player1.send("PLAYER:unidob,0,3\r\n")

        self.player1.send("PLAYER:weapp,1,3\r\n")

        self.player1.send("PLAYER:bolera_net,3,3\r\n")

        self.player1.send("START:\r\n")

        self.player1.send("TURN:\r\n")

        # Esperar que el cliente diga algo
        comando = self.player1.recv(1024)

        c1 = comando.split(':')

        if c1[0] == "THROW":
            print "Carta enviada ", c1
        elif c1[0] == "PASS":
            print "Pasando ", c1
        else:
            print "Comando equivocado"
            print c1

        #self.player1.send("ACK:\r\n")

        self.player1.close()
        self.ss.close()

    def create_game()
        self.game_name=culo
        self.mod_game=__import__(self.game_name)
        self.game=mod_game.Game()


    '''
    def close_all(self):
        """
        cierra todas las conexiones
        """
        for i in self.sock.keys():
            self.sock[i].send("XIT: adios\r\n")
            self.sock[i].close()
            self.sock.pop(i)
        self.sock = 0
        self.addr = 0
        self.cn = 0
        self.esperandoMaster()

    def send_all_minus(self, str, index):
        """
        manda la cadena str a todos los clientes conectados menos al de indice index
        """
        for i in self.sock.keys():
            if i != index:
                try:
                    self.sock[i].send(str)
                except:
                    self.remove(i)

    def send_to(self, str, index):
        """
        manda la cadena str al cliente index solamente
        """
        self.sock[index].send(str)
    
    def send_all(self, str):
        """
        manda la cadena str a todos los clientes conectados
        """
        for i in self.sock.keys():
            self.sock[i].send(str)
    
    def remove(self, index):
        """
        borra un socket de conexion con clave index
        """
        self.cn = self.cn - 1
        self.sock[index].close()
        self.sock.pop(index)
        if self.cn == 0 and self.parametro:
            self.esperandoMaster()

    '''

if __name__ == '__main__':
    print "Iniciando"
    ss = Server()
    ss.lanzar()
    print "Finalizado"
