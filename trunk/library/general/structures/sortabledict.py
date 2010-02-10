#!/usr/bin/env python
#-*- coding:utf-8 -*-
import sortablelist
import UserDict

class SortableDict(UserDict.UserDict):
    new_always_in_top=False
    def __init__(self):
        UserDict.UserDict.__init__(self)
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
        if SortableDict.new_always_in_top:
            if key in self.__keys: self.__keys.remove(key)
            self.__keys.append(key)
        else:
            if not key in self:
                self.__keys.append(key)
        UserDict.UserDict.__setitem__(self,key,value)

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
        UserDict.UserDict.__delitem__(self,x)
        self.__keys.remove(x)

    def clear(self):
        UserDict.UserDict.clear(self)
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
        return UserDict.UserDict.pop(self,x)

    def popitem(self):
        return UserDict.UserDict.pop(self,self.__keys.pop())

    def update(self,*args,**kw):
        UserDict.UserDict.update(self,*args,**kw)
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
        a.update(UserDict.UserDict.copy(self))
        return a
    
    def reverse(self):
        self.__keys.reverse()

    update_items=update

if __name__ == '__main__':
    pass
