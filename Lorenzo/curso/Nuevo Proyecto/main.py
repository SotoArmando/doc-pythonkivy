#!/usr/bin/env python
# -*- coding: utf-8 -*-


import datetime 
import pytz

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.relativelayout import RelativeLayout
import threading

from kivy.core.window import Window
Window.size = (360,640)

import os
patch = os.path.dirname(os.path.abspath(__file__))
asset = patch + '/assets/drawable-mdpi/'
color = patch + '/colors/'
font = patch + '/fonts/'




class InterfaceManager(RelativeLayout):
    def __init__(self, **kwargs):
        super(InterfaceManager, self).__init__(**kwargs)
        
        self.start_date = str(datetime.datetime.now(pytz.utc))[:19];date_1 = datetime.datetime.strptime(self.start_date, "%Y-%m-%d %H:%M:%S")
        self.end_date = date_1 + datetime.timedelta(seconds=15)
        

        self.activar_contar()




        
    def activar_contar(self):
        self.start_date = str(datetime.datetime.now(pytz.utc))[:19]
        if str(self.start_date) == str(self.end_date):
            threading.Timer(.5, self.activar_contar).cancel()
            print ("LISTO")
        else:
            threading.Timer(.5, self.activar_contar).start()
            print self.start_date


class MyApp(App):
    def build(self):
        return InterfaceManager()
 

if __name__ in ('__main__', '__android__'):
    MyApp().run()

    
    
    
    
    