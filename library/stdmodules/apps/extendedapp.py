#!/usr/bin/env python
#-*- coding:utf-8 -*-

import basicapp
from library.stdmodules import scenemanager
from library.stdmodules.controller import bindingmanager

class ExtendedApp(basicapp.BasicApp):
    def __init__(self, factory):
        basicapp.BasicApp.__init__(self)
        self['General'] = basicapp.BasicApp()
        self['SceneManager'] = scenemanager.SceneManager(factory)
        self['BindingManager'] = bindingmanager.BindingManager()
	