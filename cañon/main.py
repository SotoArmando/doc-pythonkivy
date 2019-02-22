#!/usr/bin/env python
# -*- coding: utf-8 -*-
import kivy
from kivy.app import App

from interface import InterfaceManager
from pyobjs.players import Player

class MyApp(App):
    def build(self):
        x = InterfaceManager()
        return x
    

if __name__ in ('__main__', '__android__'):
    MyApp().run()

    
    
    
    
    