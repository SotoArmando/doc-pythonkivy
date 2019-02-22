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
Window.size = (1024,640)
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



class Configuracion(Screen):
    def __init__(self, **kwargs):
        super(Configuracion, self).__init__(**kwargs)
        self.add_widget(Image(source = color + "3.png", keep_ratio = False, allow_stretch = True))
        self.sc = ScreenManager()
        self.screen0 = Screen(name = "0")
        self.screen1 = Screen(name = "1")
        self.screen2 = Screen(name = "2")
        self.sc.add_widget(self.screen0)
        self.sc.add_widget(self.screen1)
        self.sc.add_widget(self.screen2)
        scrollview0 = ScrollView()
        pariente = GridLayout(cols = 1)
        pariente.add_widget(Label(size_hint_y = None , height = dp(74)))
        pariente.add_widget(Button(size_hint = (1,None), height = dp(54), text = "Configurar Unidad", on_release = lambda x: self.dummycurrent(current = "2")))
        pariente.add_widget(Button(size_hint = (1,None), height = dp(54), text = "Configurar datos por default", on_release = lambda x: self.dummycurrent(current = "1")))
        pariente.add_widget(Label(size_hint = (1,None),font_size = sp(18), height = dp(400), text = "No se ha configurado ninguna unidad."))
        scrollview0.add_widget(pariente)
        self.screen0.add_widget(scrollview0)
        self.add_widget(self.sc)
        
        
        scrollview1 = ScrollView()
        pariente1 = GridLayout(cols = 1,size_hint_y = None, height = dp(1000))
        scrollview1.add_widget(pariente1)
        self.screen1.add_widget(scrollview1)
        pariente1.add_widget(Label(size_hint_y = None, height = dp(74)))
        pariente1.add_widget(TextInput(font_size = dp(18),padding = [15,15,0,0],hint_text = "IMAGEN",background_normal = color + "3.png",background_active = color + "2.png",size_hint_y = None , height = dp(54), multiline = False, foreground_color = (1,1,1,1)))
        pariente1.add_widget(TextInput(font_size = dp(18),padding = [15,15,0,0],hint_text = "NOMBRE",background_normal = color + "3.png",background_active = color + "2.png",size_hint_y = None , height = dp(54), multiline = False, foreground_color = (1,1,1,1)))
        pariente1.add_widget(TextInput(font_size = dp(18),padding = [15,15,0,0],hint_text = "FECHA DE NACIMIENTO",background_normal = color + "3.png",background_active = color + "2.png",size_hint_y = None , height = dp(54), multiline = False, foreground_color = (1,1,1,1)))
        pariente1.add_widget(TextInput(font_size = dp(18),padding = [15,15,0,0],hint_text = "ORIGEN DE NACIMIENTO",background_normal = color + "3.png",background_active = color + "2.png",size_hint_y = None , height = dp(54), multiline = False, foreground_color = (1,1,1,1)))
        pariente1.add_widget(TextInput(font_size = dp(18),padding = [15,15,0,0],hint_text = "SEXO",background_normal = color + "3.png",background_active = color + "2.png",size_hint_y = None , height = dp(54), multiline = False, foreground_color = (1,1,1,1)))
        pariente1.add_widget(TextInput(font_size = dp(18),padding = [15,15,0,0],hint_text = "ESTADO CIVIL",background_normal = color + "3.png",background_active = color + "2.png",size_hint_y = None , height = dp(54), multiline = False, foreground_color = (1,1,1,1)))
        pariente1.add_widget(TextInput(font_size = dp(18),padding = [15,15,0,0],hint_text = "PROFESION",background_normal = color + "3.png",background_active = color + "2.png",size_hint_y = None , height = dp(54), multiline = False, foreground_color = (1,1,1,1)))
        pariente1.add_widget(TextInput(font_size = dp(18),padding = [15,15,0,0],hint_text = "DNI",background_normal = color + "3.png",background_active = color + "2.png",size_hint_y = None , height = dp(54), multiline = False, foreground_color = (1,1,1,1)))

        pariente1.add_widget(TextInput(font_size = dp(18),padding = [15,15,0,0],hint_text = "DIRECCION",background_normal = color + "3.png",background_active = color + "2.png",size_hint_y = None , height = dp(54), multiline = False, foreground_color = (1,1,1,1)))
        pariente1.add_widget(TextInput(font_size = dp(18),padding = [15,15,0,0],hint_text = "NUMERO MOVIL",background_normal = color + "3.png",background_active = color + "2.png",size_hint_y = None , height = dp(54), multiline = False, foreground_color = (1,1,1,1)))
        pariente1.add_widget(TextInput(font_size = dp(18),padding = [15,15,0,0],hint_text = "NUMERO RESIDENCIAL",background_normal = color + "3.png",background_active = color + "2.png",size_hint_y = None , height = dp(54), multiline = False, foreground_color = (1,1,1,1)))
        pariente1.add_widget(Button(background_normal = color + "2.png",size_hint_y = None , height = dp(74), text = "CONFIRMAR", font_size = sp(18)))
        pariente1.add_widget(Button(background_normal = color + "2.png",size_hint_y = None , height = dp(74), text = "CANCELAR", font_size = sp(18), on_release = lambda x: self.dummycurrent(current = "0")))
        
        self.pariente2scroll = ScrollView()
        self.pariente2 = GridLayout(cols = 1, size_hint_y = None, height = 2000) 
        self.pariente2scroll.add_widget(self.pariente2)
        self.screen2.add_widget(self.pariente2scroll)
        self.pariente2.add_widget(Label(size_hint_y = None, height = dp(74)))
        self.pariente2.add_widget(TextInput(font_size = dp(18),padding = [15,15,0,0],hint_text = "DIVISION",background_normal = color + "3.png",background_active = color + "2.png",size_hint_y = None , height = dp(54), multiline = False, foreground_color = (1,1,1,1)))
        self.pariente2.add_widget(TextInput(font_size = dp(18),padding = [15,15,0,0],hint_text = "DEPARTAMENTO",background_normal = color + "3.png",background_active = color + "2.png",size_hint_y = None , height = dp(54), multiline = False, foreground_color = (1,1,1,1)))
        self.pariente2.add_widget(TextInput(font_size = dp(18),padding = [15,15,0,0],hint_text = "CARGO",background_normal = color + "3.png",background_active = color + "2.png",size_hint_y = None , height = dp(54), multiline = False, foreground_color = (1,1,1,1)))
        self.pariente2.add_widget(Button(background_normal = color + "2.png",size_hint_y = None , height = dp(74), text = "CONFIRMAR", font_size = sp(18)))
        self.pariente2.add_widget(Button(background_normal = color + "2.png",size_hint_y = None , height = dp(74), text = "CANCELAR", font_size = sp(18), on_release = lambda x: self.dummycurrent(current = "0")))
        
    def dummycurrent(self,**kwargs): 
        self.sc.current = kwargs["current"]
        
class MyApp(App):
    def build(self):
        return Configuracion()
 

if __name__ in ('__main__', '__android__'):
    MyApp().run()

    
    
    
    
    