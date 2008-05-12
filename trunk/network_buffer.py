
import socket
import threading

class Receiver(threading.Thread):
    '''
    Recibe del socket, y va escribiendo los mensajes en la cola fifo
    del network_buffer.
    '''
    def __init__(self, my_network_buffer):
        self.nb = my_network_buffer
        threading.Thread.__init__(self)
        self.buffer = ''
        self.end = False

    def run(self):
        while not self.end:
            sep = self.nb.separator
            try:
                self.buffer += self.nb.sock.recv(1024)
            except:
                pass
            index = self.buffer.find(self.nb.separator)
            while index >= 0:
                print index
                print "antes", buffer
                self.nb.fifo.append(self.buffer[0:index])
                self.buffer = self.buffer[index + len(sep):]
                print "dps", buffer
                index = self.buffer.find(sep)

    def stop(self):
        self.end = True

class NetworkBuffer:
    '''
    Clase que facilita la comunicacion en red separando los mensajes,
    recibiendolos y enviandolos uno a uno.
    '''
    NO_CONNECT = -1
    def __init__(self, port, server=''):
        self.separator = '\r\n'
        self.timeout=1
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.sock.connect((server, port))
        except:
            raise Exception(str(NetworkBuffer.NO_CONNECT))

        self.sock.settimeout(self.timeout)
        self.fifo = []
        self.receiver_thread = Receiver(self)
        self.receiver_thread.start()

    def __del__(self):
        print "destructor"
        self.receiver_thread.end = True

    def send_msg(self, msg):
        '''
        Envia un mensaje por el socket
        '''
        counter = 6
        to_send = msg + self.separator
        length = self.sock.send(to_send)
        while length < len(to_send):
            length += self.sock.send(to_send[length+1:])
            counter -= 1
            if counter == 0:
                return False, length

        return True, 0

    def number_msg(self):
        '''
        Devuelve el numero de mensajes en la cola
        '''
        return len(self.fifo)

    def received_msg(self):
        '''
        Devuelve el primer elemento de la cola, si existe. Si no hay
        mensajes en la cola lanza la excepcion 
        '''

        if len(self.fifo) > 0:
            return self.fifo.pop()
        else:
            return ''

    def clear_msg(self):
        '''
        Borra toda la cola fifo
        '''

        self.fifo = []
