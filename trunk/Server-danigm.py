import sys
import socket

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
                return None
        self.ss.listen(10)
        self.cn = 0 #numero de jugadores
        self.sock = {} #cada jugador escribira en un socket
        self.addr = {} #direccion de cada jugador

    def lanzar(self):
        print "Esperando conexion"
        self.player1, self.player1_addr = self.ss.accept()
        syn = self.player1.recv(1024)
        if syn.split(':')[0] == 'SYN':
            print "usuario conectado", self.player1_addr, syn
        else: sys.exit(-1)
        self.player1.send("ACK:\r\n")

        # las cartas del jugador y su id
        self.player1.send("START:2,3;0,12;1,9;3\r\n")

        # los demas jugadores y su numero de cartas inicial
        self.player1.send("PLAYER:0,3\r\n")
        self.player1.send("PLAYER:1,3\r\n")
        self.player1.send("PLAYER:3,3\r\n")

        self.player1.send("GO:\r\n")
        self.player1.send("TURN:\r\n")
        
        # Esperar que el cliente diga algo
        comando = self.player1.recv(1024)
        
        c1 = comando.split(':')
        
        if c1[0] == "THROW":
            print "Carta enviada ", c1
        elif c1[0] == "PASS":
            print "Pasando ", c1

        self.player1.send("ACK:\r\n")
        
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
