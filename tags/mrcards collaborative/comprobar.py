import sys

def comprobar_error(mensaje,clave):
    if mensaje.split(":")[0]!=clave:
        print "Error no ha llegado el mensaje ", clave
        print mensaje
        sys.exit(-1)
