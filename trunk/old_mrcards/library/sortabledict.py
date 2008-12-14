#!/usr/bin/env python
#-*- coding:utf-8 -*-
import sortablelist

class SortableDict(dict):

    def __init__(self):
        self.__keys=sortablelist.SortableList()

    def top(self,x):
        self.__keys.top_elem(x)

    def bottom(self,x):
        self.__keys.bottom_elem(x)

    def up(self,x):
        self.__keys.up_elem(x)

    def down(self,x):
        self.__keys.down_elem(x)

    def __setitem__(self,key,value):
        if key in self.__keys: self.__keys.remove(key)
        self.__keys.append(key)
        dict.__setitem__(self,key,value)

    def __iter__(self):
        return self.__keys.__iter__()

    def items(self):
        for key in self.__keys:
            yield key, self[key]

    def keys(self):
        return self.__keys[:]
        
    def values(self):
        return map(lambda key:self[key],self.__keys[:])

    def __delitem__(self,x):
        dict.__delitem__(self,x)
        self.__keys.remove(x)

    def clear(self):
        dict.clear(self)
        self.__keys=sortable_list.Sortable_list()

    def iterkeys(self):
        self.__iter__()

    def iteritems(self):
        for key in self.__keys:
            yield key, self[key]

    def itervalues(self):
        for key in self.__keys:
            yield self[key]

    def pop(self,x):
        self.__keys.remove(x)
        return dict.pop(self,x)

    def popitem(self):
        return dict.pop(self,self.__keys.pop())

    def update(self,*args,**kw):
        dict.update(self,*args,**kw)
        if args:
            if type(args[0]) == dict:
                for key in args[0]:
                    if key in self.__keys: self.__keys.remove(key)
                    self.__keys.append(key)
            else:
                for lists in args[0]:
                    print lists
                    key=lists[0]
                    if key in self.__keys: self.__keys.remove(key)
                    self.__keys.append(key)
        for key in kw:
            if key in self.__keys: self.__keys.remove(key)
            self.__keys.append(key)

    def copy(self):
        a = Sortable_dict()
        a.update(dict.copy(self))
        return a

if __name__ == '__main__':
    pass
