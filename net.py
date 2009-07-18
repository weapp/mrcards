'''
Este modulo es el encargado de gestionar el juego en red.
'''
import socket

class Net:
    def __init__(self,options=False):
        self.buffer = ''
        self.juego = ''
        self.jugadores = 0
        self.me = 0
        self.players = []

    def init_net(self, juego='', jugadores=0):
        print "IP del servidor:"
        server = raw_input()
        print "Puerto del servidor:"
        port = int(raw_input())

        self.s = socket.socket()
        self.s.connect((server,port))
        msg = self.read_msg()
        print msg
        
        if msg[0:3] == 'NGP':
            # Master
            self.juego = juego
            self.jugadores = jugadores
            self.me = 0
            self.s.send(juego+':'+str(jugadores)+'\r\n')
            msg = self.read_msg()
            if msg[0:3] != 'ACK':
                return False
            msg = self.read_msg()
            if msg[0:3] == 'WHO':
                self.s.send('player 0\r\n')

        elif msg[0:3] == 'MSG':
            # Cliente
            all = msg.split(':')
            juego = all[1]
            jugadores = int(all[2])

            me = int(all[3])
            self.juego = juego
            self.jugadores = jugadores
            self.me = me

            self.s.send('ACK: recibido\r\n')
            msg = self.read_msg()
            if msg[0:3] == 'WHO':
                self.s.send('player '+str(me)+'\r\n')

        msg = self.read_msg()
        self.players = msg.strip()[1:-1].split(':')
        self.s.send('ACK: vamos alla\r\n')
        # Hay que esperar el READY
        self.read_msg() 

    def read_msg(self):
        '''
        Lee un mensaje completo del socket. Los mensajes completos
        finalizan con \r\n
        '''
        n = self.buffer.find('\r\n')
        if n != -1:
            to_ret = self.buffer[0:n]
            self.buffer = self.buffer[n+2:]
            return to_ret

        self.buffer += self.s.recv(1024)
        while self.buffer.find('\r\n') == -1:
            self.buffer += self.s.recv(1024)
        
        n = self.buffer.find('\r\n')
        to_ret = self.buffer[0:n]
        self.buffer = self.buffer[n+2:]
        return to_ret

    def read_non_blocking(self):
        '''
        lee un mensaje del socket, pero sin bloquear
        '''

        n = self.buffer.find('\r\n')
        if n != -1:
            to_ret = self.buffer[0:n]
            self.buffer = self.buffer[n+2:]
            return to_ret
        else:
            try:
                self.buffer += self.s.recv(1024, socket.MSG_DONTWAIT)
            except:
                return False

            n = self.buffer.find('\r\n')
            if n != -1:
                to_ret = self.buffer[0:n]
                self.buffer = self.buffer[n+2:]
                return to_ret
            else: return False




    def send(self, msg):
        '''
        Envia un mensaje al servidor
        '''
        self.s.send('FUN:'+msg+'\r\n')
