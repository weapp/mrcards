import time
tiempos={}

def mostrar_tiempos():
    for t in tiempos:
        suma=reduce(lambda x,y: x+y, tiempos[t])
        #print "+" + t + ": "+ str(suma) + "/" + str(len(tiempos[t])) +"\n" +  str( suma / len(tiempos[t]) )
        
        mitad=tiempos[t][ int(len(tiempos[t])/2):]
        suma=reduce(lambda x,y: x+y, mitad)
        #print "++++++++++" + t + ": "+ str(suma) + "/" + str(len(mitad)) +"\n++++++++++" +  str( suma / len(mitad) )

def dec_mos_tiempos(funcion):
    def nueva(*args):
        retorno = funcion(*args)
        mostrar_tiempos()
        return retorno
    return nueva

def tiempo(funcion):
  def nueva(*lista_args):
    tiempo1 = time.time()
    valor = funcion(*lista_args)
    tiempo2 = time.time()
    delta = tiempo2 - tiempo1
    
    #print "La funcion '%s()' tardo en ejecutarse %s segundos" % (funcion.func_name, delta)
    
    if not tiempos.has_key(funcion.func_name):
        tiempos[funcion.func_name]=[]
    tiempos[funcion.func_name].append(delta)
    
    return valor  
  return nueva


cache={}

def cachear(funcion):

    def fcache(*args):
        #print "****cache de la funcion", funcion.__name__
        return cache.setdefault((funcion,tuple(map(repr,args))),funcion(*args))
        """
        if not cache.has_key((funcion,tuple(map(repr,args)))):
            cache[(funcion,tuple(map(repr,args)))]=funcion(*args)
            print "#no cacheado:",funcion,args
        return cache[(funcion,tuple(map(repr,args)))]
        """
    return fcache


def function_cache(function, args, force=False):
    if force or not cache.has_key((function,tuple(args))):
        cache[(function,tuple(args))]=function(*args)   
    return cache[(function,tuple(args))]


@tiempo 
@cachear
def a(h, s2, l):
    return 1
    
@tiempo
def b(h, s2, l):
    return 1
