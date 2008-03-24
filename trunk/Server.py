import socket
import threading
import pdb

"""
Servidor para MRcard
XIT: salir
NGP: nombre del juego, numero de jugadores
ACK: confirmacion afirmativa
NAC: confirmacion negativa
MSG: Lo que sigue a los dos puntos es el mensaje
WHO: quien eres
FUN: nombre_funcion,arg1,arg2,...,userid
OUT: el jugador se ha salido del juego
"""

class ControlCliente(threading.Thread):
    def __init__(self, server, index, nick):
        self.server = server
        self.index = index
        self.nick = nick
        self.finish = None
        threading.Thread.__init__(self)
    def run(self):
        resp = self.server.sock[self.index].recv(1024)
        while resp[0:3] != "XIT":
            try:
                if resp.find("\r\n")>0:
                    if resp[0:3]=="FUN":
                        self.server.send_all_minus(str(self.index)+","+resp[0:resp.find("\r\n")+3], self.index)
                        resp = resp[resp.find("\r\n")+2:]
                        if resp != "":
                            continue
                    else:
                        resp = resp[resp.find("\r\n")+2:]
                        if resp != "":
                            continue

                #TODO separar cadenas recibidas
                resp += self.server.sock[self.index].recv(1024)

            except:
                print str(self.nick[0:-2])+" : se ha desconectado inesperadamente"
                break
        #self.server.send_to("600: hasta luego\r\n", self.index)
        self.server.send_all_minus("OUT:"+str(self.index)+":LOG_OUT\r\n", self.index)
        self.server.remove(self.index)

class BroadCast(threading.Thread):
    def __init__(self, server):
        self.server = server
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        threading.Thread.__init__(self)
    def run(self):
        self.s.bind(("",8080))
        while True:
            buf, addr = self.s.recvfrom(1024)
            self.s.sendto("MRCards server\r\n", addr)
        
class Server:
    #tengo que pasar un parametro para controlar si se crea en el cliente, que no se vuelva
    #a llamar
    def __init__(self, puerto = 12345, parametro=None):
        """
        abre un puerto en la maquina local, y espera cn conexiones
        """
        self.parametro = parametro
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
        self.ready = []
        self.laps = []
        self.winners = []
        self.players = []
        self.max2 = 0
        self.first = 0
        BroadCast(self).start()
        self.esperandoMaster()

    def esperandoMaster(self):
        #esperamos al Master
        self.cn = 0 #numero de jugadores
        self.sock = {} #cada jugador escribira en un socket
        self.addr = {} #direccion de cada jugador
        self.ready = []
        self.laps = []
        self.winners = []
        self.players = []
        self.max2 = 0

        print "Esperando al Master"
        self.master, self.master_addr = self.ss.accept()
        self.master.send("NGP: Master conectado, nombre del juego:jugadores\r\n")
        print "Master conectado", self.master_addr
        print "Esperando juego"
        #recivimos parametros de la partida
        self.game = self.master.recv(1024)
        self.game, self.cn = self.game.split(':')
        self.cn = int(self.cn)
        self.master.send("ACK: juego:jugadores ok\r\n")
        print "juego ok:", self.game
        print "numero de jugadores ok:", self.cn
        #esperamos a que todos se conecten
        self.conecta()
        
    def conecta(self):
        self.sock[0] = self.master
        self.addr[0] = self.master_addr
        for i in range(1, self.cn):
            print "Esperando "+str(self.cn - i)+" jugadores"
            self.sock[i], self.addr[i] = self.ss.accept()
            self.sock[i].send("MSG:"+self.game+':'+str(self.cn)+':'+str(i)+"\r\n")
            self.sock[i].recv(1024) #esperamos a que lea el circuito y los jugadores

        print self.cn, "conexiones"
        #peticion de datos de los clientes
        #tengo que crear cn objetos de la clase cliente
        #con los datos de cada jugador
        jugadores = ""
        for i in self.sock.keys():
            self.sock[i].send("WHO: todos conectados, quien eres\r\n")
            resp = self.sock[i].recv(1024)
            print resp[0:-2], "Conectado"
            self.players.append(resp[0:-2])
            jugadores = jugadores + ":"+resp[0:-2]
        self.send_all(jugadores+":\r\n")

        for i in self.sock.keys():
            resp = self.sock[i].recv(1024)
            print self.players[i], "Listo"
            self.add_player_ready(i)

        for i in self.sock.keys():
            ControlCliente(self, i, self.players[i]).start()

        #self.send_all("READY!\r\n")

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

    def add_player_ready(self, index):
        """
        anade el player index a los que estan listos para empezar
        """
        self.ready.append(index)
        if(len(self.ready) >= self.cn):
            self.send_all("READY!\r\n")
            print "READY enviado"
            for i in self.ready:
                self.laps.append(0)

    def max(self):
        for i in self.laps:
            if i > self.laps[self.max2]:
                self.max2 = self.laps.index(i)
        return self.max2

if __name__ == '__main__':
    ss = Server()
