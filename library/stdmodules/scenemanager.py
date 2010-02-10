#!/usr/bin/env python
#-*- coding:utf-8 -*-

from library.stdmodules import module
from library.general.structures import sdwak
from apps import sceneapp
from library.general import xmlconfig
class SceneManager (module.Module, object):

    def __init__(self, factory):
        module.Module.__init__(self)
        self.scenes = sdwak.SDWAK()
        self.__scene = sceneapp.SceneApp()
        
        self.next_scene = None
        self.factory = factory
    
    def get_scene(self):
        return self.__scene
          
    def set_scene(self, scene):
        if self.__scene:
            self.__scene.end_scene()
            self.del_child(self.__scene)
        self.__scene = scene
        self.add_child(scene)
          
    def del_scene(self):
        del self.__scene
    
    scene = property(get_scene, set_scene, del_scene, "I'm the 'scene' property.")
    
    def charge_scene(self, name_scene, xmlfilename):
        self.scenes[name_scene] = xmlfilename
        
    def charge_scenes(self, path):
        raise NotImplementedError()
        pass
                    
    def change_scene(self, name_scene):
        self.next_scene = name_scene
        
    def __change_scene(self):
        self.scene = sceneapp.SceneApp()
        self.add_child(self.scene)
        xmlconfig.cargar_estado(self.scenes[self.next_scene], self.scene.add, self.factory)
        self.scene.start_scene()
        self.next_scene = None
                        
    def charge_and_change_scene(self,name_scene, xmlfilename):
        self.charge_scene(name_scene, xmlfilename)
        self.change_scene(name_scene)
        
    def new_event(self, event):
        return self.scene.new_event(event)
        
    def update(self):
        if not self.next_scene is None:
            self.__change_scene()
        self.scene.update()
        
    def draw(self):
        self.scene.draw()
        
    def updated(self):
        return True
