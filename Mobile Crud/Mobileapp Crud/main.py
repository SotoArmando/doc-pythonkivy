#!/usr/bin/env python
# -*- coding: utf-8 -*-

from rutas import *
from dependencias import *
from variablesGlobales import *


class Main(RelativeLayout):#COMPLEMENTO 'PARENT' EL PROYECTO
    def __init__(self, **kwargs):
        super(Main, self).__init__(**kwargs)
        
        
        
        
        

class MainApp(App):
    def build(self):
        return Main()
 

if __name__ in ('__main__', '__android__'):
    MainApp().run()

    
    
    
    
    