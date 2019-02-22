#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __init__ import *

#CARPETAS DEL PROYECTO
patch = os.path.dirname(os.path.abspath(__file__))
asset = patch + '/assets/drawable-mdpi/'
color = patch + '/colors/'
font = patch + '/fonts/'

#VARIABLES GLOBALES
Hola = "Hola a todos"



Config.set('graphics', 'fullscreen', 'fake')
Config.set('graphics', 'position', 'custom')
Config.set('graphics', 'top', '300')
Config.set('graphics', 'left', '300')

class InterfaceManager(RelativeLayout):#COMPLEMENTO 'PARENT' EL PROYECTO
    def __init__(self, **kwargs):
        super(InterfaceManager, self).__init__(**kwargs)
        #INTERFACE
        button0 = Button()
        self.add_widget(button0)
        #ANIDAR FUNCION A EVENTO
        button0.bind(on_release = lambda x: self.funcion())
        

    def funcion(self):
        print("hola")

class MyApp(App):
    def build(self):
        #Window.borderless = True
        return InterfaceManager()
 

if __name__ in ('__main__', '__android__'):
    MyApp().run()

import win32gui
import win32con
win32gui.SetWindowPos(hWnd, win32con.HWND_TOPMOST, 0,0,0,0,
win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)
    
    
    
    