#!/usr/bin/python
# Nombre : xml5.py
import xml.dom.minidom

def crea_element(node):
    for elem in node.childNodes:
        if not elem.hasChildNodes():
            return False
        else:
            return True
    
    

class Element(dict):
    def __init__(self,node):
        self.node=node
        for elem in node.childNodes:
            #print repr(elem.hasChildNodes()) + "  " + str(elem)
            if elem.hasChildNodes():
                key = str(elem.tagName)
                if key not in self:
                    self[key]=lista()
                self[key].append(Element(elem))
            else:
                self['value']=elem.nodeValue
                
    def __str__(self):
        return self.__repr__()
    
    def __repr__(self):
        r=""
        for key in self:
            r+="<"+ str(key) +"> "+ str(self[key])+" </"+ str(key) +"> "
        return r 
    
class lista(list):
    def __repr__(self):
        return self.__str__()
    def __str__(self):
        r=""
        for value in self:
            r+=repr(value) + " "
        return r
  

def parse_xml(name_file):
    return Element(xml.dom.minidom.parse(name_file))

def main():
    e=parse_xml('./xml1.xml')
    print e['agenda'][0]['contacto'][0]['nombre'][0]['value']
    print e

        
if __name__ == "__main__": main()
