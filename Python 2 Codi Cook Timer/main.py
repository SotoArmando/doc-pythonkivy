#!/usr/bin/env python
# -*- coding: utf-8 -*-

import kivy

from comp.__init__ import *
from kivy.app import App
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.button import Button
import os


#CARPETAS DEL PROYECTO
patch = os.path.dirname(os.path.abspath(__file__))
asset = patch + '/comp/assets/drawable-mdpi/'
color = patch + '/comp/colors/'
font = patch + '/comp/fonts/'

#VARIABLES GLOBALES
Hola = "Hola a todos"
Window.size = (360,640)
from comp.behavior import CloseBehavior

class InterfaceManager(RelativeLayout):#COMPLEMENTO 'PARENT' EL PROYECTO
    def __init__(self, **kwargs):
        super(InterfaceManager, self).__init__(**kwargs)
        from comp.comp0 import Comp0
        from comp.comp1 import Comp1
        from comp.comp2 import Comp2
        from comp.comp3 import Comp3
        from comp.comp4 import Comp4
        parent = GridLayout(cols = 1, spacing = dp(24)); self.add_widget(parent)
        c0 = Comp0(size_hint_y = None, height = dp(100)); parent.add_widget(c0)
        c1 = Comp1(); parent.add_widget(c1)
        c2 = Comp2(); parent.add_widget(c2)
        c3 = Comp3(); parent.add_widget(c3)
        c4 = Comp4(size_hint_y = 1); self.add_widget(c4)
        self.add_widget(CloseBehavior(R = self, object = c4))
    def funcion(self):
        print("hola")

class MyApp(App):
    def build(self):
        return InterfaceManager()
 

if __name__ in ('__main__', '__android__'):
    MyApp().run()

    
    
    
    
    