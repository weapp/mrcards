class Singleton(type):
    def __init__(cls, name, bases, dct):
        cls.__instance = None
        type.__init__(cls, name, bases, dct)
 
    def __call__(cls, *args, **kw):
        if cls.__instance is None:
            cls.__instance = type.__call__(cls, *args,**kw)
        return cls.__instance
        
if __name__ == "__main__":
    class A:
        __metaclass__ = Singleton
        def __init__(self):
            self.i=1
            
        def add(self):
            self.i+=1
     
    a = A()
    b = A()

    print a.i
    print b.i

    b.add()

    print a.i
    print b.i
    
    assert a==b
    print a == b  # True, funciona!  :-)
