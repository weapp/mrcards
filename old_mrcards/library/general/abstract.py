class AbstractClass(object) :
    def __init__(self) :
        if type(self) is AbstractClass :
            raise AbstractClassException
        else:
            self.i=1
            #constructor por defecto de las subclases

class SubClass(AbstractClass) :
    def __init__(self):
        AbstractClass.__init__(self):
        #constructor de la subclase que no dara errores
        
class AbstractClassException(Exception) :
    def __str__(self):
        return 'Esta clase es abstracta'
