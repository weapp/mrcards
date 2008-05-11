import sys
import socket
from comprobar import comprobar_error

"""
Servidor para MRcard
 * servidor:
    you: ID 
    player:nombre,ID,numero_cartas
    cards: n,p;n,p;n,p;... Nuestras cartas -> split(';') -> split(',')
    turn: # directo a un jugador
    ack: confirmacion
    nack:msg
    start: Empieza el juego
    win:
    lose:
    thrown:j,n;p,n;p...

 * cliente:
    syn:autenticacion
    name: nombre del jugador
    pass: paso de turno
    throw:n;p,n;p ...
    exit:
"""
class Server:
    def __init__(self, puerto = 12345):
        """
        abre un puerto en la maquina local, y espera cn conexiones
        """
        self.ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.ss.bind(("",puerto))
        except:
            puerto = puerto + 1
            print "error al conectar en localhost, probando con puerto 12346"
            try:
                self.ss.bind(("",puerto))
            except:
                print "error tambien conectando al puert 12346"
                sys.exit(-1)
        self.ss.listen(10)
        self.cn = 0 #numero de jugadores
        self.sock = {} #cada jugador escribira en un socket
        self.addr = {} #direccion de cada jugador

    def lanzar(self):
        print "Esperando conexion"
        self.player1, self.player1_addr = self.ss.accept()


        #Mensaje para conectar
        syn_m = self.player1.recv(1024)
        comprobar_error(syn_m,"SYN")
        print "usuario conectado", self.player1_addr

        #Lo aceptamos
        self.player1.send("ACK:\r\n")

        #Recibimos algo para que no envie dos cosas en un mismo mensaje
        self.player1.recv(1024)

        # ID del jugador
        self.player1.send("YOU:2\r\n")

        name_m=self.player1.recv(1024)
        comprobar_error(name_m,"NAME")
        name=name_m.split(":")[1]
        print "Nombre del jugador ",name

        self.player1.send("CARDS:2,3;12,0;1,1;2,1")

        #Recivimos algo para que no envie dos cosas en un mismo mensaje
        self.player1.recv(1024)

        # los demas jugadores y su numero de cartas inicial
        self.player1.send("PLAYER:unidob,0,3\r\n")
        #Recibimos algo para que no envie dos cosas en un mismo mensaje
        self.player1.recv(1024)

        self.player1.send("PLAYER:weapp,1,3\r\n")
        #Recibimos algo para que no envie dos cosas en un mismo mensaje
        self.player1.recv(1024)

        self.player1.send("PLAYER:bolera_net,3,3\r\n")
        #Recibimos algo para que no envie dos cosas en un mismo mensaje
        self.player1.recv(1024)

        self.player1.send("START:\r\n")
        #Recibimos algo para que no envie dos cosas en un mismo mensaje
        self.player1.recv(1024)
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
            print ci

        #self.player1.send("ACK:\r\n")

        self.player1.close()
        self.ss.close()

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
