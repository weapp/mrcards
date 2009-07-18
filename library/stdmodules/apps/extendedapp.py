#!/usr/bin/env python
#-*- coding:utf-8 -*-

import basicapp
import mvcapp

class ExtendedApp(basicapp.BasicApp):
    def __init__(self):
        basicapp.BasicApp.__init__(self)
        self[general]=mvc.MVCApp()
        self[SceneManager]=scenemanager.SceneManager
