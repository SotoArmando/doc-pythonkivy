#!/usr/bin/env python
# -*- coding: utf-8 -*-

from kivy.core.window import Window
from kivy.animation import Animation
from kivy.metrics import dp,sp, MetricsBase
from kivy.resources import resource_add_path
from kivy.uix.screenmanager import ScreenManager, Screen,CardTransition,SwapTransition, NoTransition,SlideTransition,FadeTransition,WipeTransition,FallOutTransition,NoTransition ,RiseInTransition 
from kivy.uix.button import Button
from kivy.uix.relativelayout import RelativeLayout
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.image import Image,AsyncImage
from kivy.uix.scrollview import ScrollView
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.checkbox import CheckBox
from kivy.uix.scatterlayout import ScatterLayout as Scatter
from kivy.uix.textinput import TextInput
from kivy.graphics import Color, Line, Rectangle
from kivy.uix.behaviors import ButtonBehavior
from kivy.animation import Animation
from kivy.uix.widget import Widget
from kivy.uix.stencilview import StencilView
from kivy.metrics import dp
from kivy.clock import Clock
from kivy.properties import (ObjectProperty, NumericProperty, OptionProperty,
                             BooleanProperty, StringProperty)
from kivy.resources import resource_add_path
from kivy.lang import Builder
import os   
import os.path
Window.size = (360,640)
Window.clearcolor = (1,1,1,1)
#CARPETAS DEL PROYECTO
patch = os.path.dirname(os.path.abspath(__file__))
asset = patch + '/assets/drawable-mdpi/'
color = patch + '/colors/'
font = patch + '/fonts/'
from kivy.graphics import *
C1 = "[color=#13C0C7]"
C4 = "[color=#000000]"
C2 = "[color=#404040]"
C3 = "[color=#ff3333]"
C5 = "[color=#f2f2f2]"
C6 = "[color=#95989A]"
EC = "[/color]"
class ImageButton(ButtonBehavior, Image): pass



class AlarmarPop(RelativeLayout):
    def __init__(self, **kwargs):
        super(AlarmarPop, self).__init__(**kwargs)
        self.json = {}
        self.pariente1 = GridLayout(opacity = 0,cols = 2, size_hint = (.6,.3), pos_hint = {'center_x':.5,'center_y':.5}, disabled = True)
        x = Button(text = "[b]USAR MI POSICION",text_size = (Window.width/4, dp(50)), background_normal = color + "2.png",background_down = color + "3.png", halign = 'center', valign = 'middle', markup = True, on_release = lambda x: self.end())
        x.bind(on_release = lambda x: self.setjson(field = "POSICIONRELATIVA",data = "POSICION DE USUARIO"))
        
        self.pariente1.add_widget(x)
        y = Button(text = "[b]MARCAR EN EL MAPA",text_size = (Window.width/4, dp(50)), background_normal = color + "2.png",background_down = color + "3.png", halign = 'center', valign = 'middle', markup = True, on_release = lambda x: self.end())
        self.pariente1.add_widget(y)
        y.bind(on_release = lambda x: self.setjson(field = "POSICIONRELATIVA",data = "POSICION DEL MAPA"))
        y.bind(on_release = lambda x: self.animatex(kwargs["root"].indicador))
        y.bind(on_release = lambda x: self.animatex(kwargs["root"].alarmapos))
        self.add_widget(self.pariente1)
        
        
        self.pariente = GridLayout(opacity = 0,cols = 2, size_hint = (.6,.6), pos_hint = {'center_x':.5,'center_y':.5}, disabled = True)
        
        self.pariente.add_widget(Button(text = "[b]TRAFICO OBSTRUIDO",text_size = (Window.width/4, dp(50)),on_press = lambda x: self.setjson(field = "GRAVEDAD",data = "TRAFICO"), background_normal = color + "2.png",background_down = color + "3.png", halign = 'center', valign = 'middle', markup = True, on_release = lambda x: self.animate(), ))
        
        self.pariente.add_widget(Button(text = "[b]CRIMEN",text_size = (Window.width/4, dp(50)), background_normal = color + "2.png",on_press = lambda x: self.setjson(field = "GRAVEDAD",data = "CRIMEN"),background_down = color + "3.png", halign = 'center', valign = 'middle', markup = True, on_release = lambda x: self.animate()))
        
        self.pariente.add_widget(Button(text = "[b]ACCIDENTE",text_size = (Window.width/4, dp(50)),on_press = lambda x: self.setjson(field = "GRAVEDAD",data = "ACCIDENTE"), background_normal = color + "2.png",background_down = color + "3.png", halign = 'center', valign = 'middle', markup = True, on_release = lambda x: self.animate()))
        
        self.pariente.add_widget(Button(text = "[b]DELITO",text_size = (Window.width/4, dp(50)),on_press = lambda x: self.setjson(field = "GRAVEDAD",data = "DELITO"), background_normal = color + "2.png",background_down = color + "3.png", halign = 'center', valign = 'middle', markup = True, on_release = lambda x: self.animate()))
        self.add_widget(self.pariente)
        
    def setjson(self,**kwargs): self.json[kwargs["field"]] = kwargs["data"]
    def animatex(self,x):
        print x
        a = Animation(opacity = 1, d = .225 , t = 'out_back')
        a.start(x)
    def animate(self):
        if self.pariente.opacity == 0:
            a = Animation(opacity = .74, d = .225 , t = 'out_quart')
            a.start(self.pariente)
            self.pariente1.disabled = True
            self.pariente.disabled = False
        else:
            a = Animation(opacity = 0, d = .225 , t = 'out_quart')
            #a.bind(on_complete = lambda x,y: self.parent.remove_widget(self))
            a.start(self.pariente)
            b = Animation(opacity = .74 , d = .225, t = 'out_quart')
            self.pariente1.disabled = False
            self.pariente.parent.remove_widget(self.pariente)
            b.start(self.pariente1)
    
    def end(self): self.parent.remove_widget(self)
            
class MyApp(App):
    def build(self):
        return AlarmarPop()
 

if __name__ in ('__main__', '__android__'):
    MyApp().run()

    
    
    
    
    