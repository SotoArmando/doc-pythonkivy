#!/usr/bin/env python
# -*- coding: utf-8 -*-

import kivy
from kivy.config import Config

import threading 
from threading import *

from kivy.graphics import Color, Line
from kivy.graphics.transformation import Matrix
from kivy.graphics.context_instructions import Translate, Scale
from kivy.effects.opacityscroll import OpacityScrollEffect
from kivy.effects.scroll import ScrollEffect
from kivy.garden.mapview import MapView, MapMarker, MarkerMapLayer, MapSource, MapLayer,MapMarkerPopup
from kivy.uix.bubble import Bubble
from kivy.uix.checkbox import CheckBox
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.scatter import Scatter
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.anchorlayout import AnchorLayout
from kivy.properties import ListProperty, StringProperty
from kivy.adapters.simplelistadapter import SimpleListAdapter
from kivy.adapters.listadapter import ListAdapter
from kivy.uix.listview import ListItemButton, ListView, ListItemLabel,CompositeListItem
from kivy.adapters.models import SelectableDataItem
from kivy.graphics import *
from kivy.core.window import Window
from kivy.utils import get_hex_from_color, get_color_from_hex
from kivy.parser import parse_color
from kivy.graphics.instructions import InstructionGroup
from kivy.uix.accordion import Accordion, AccordionItem
from kivy.base import runTouchApp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.popup import Popup
from kivy.uix.image import Image
from kivy.uix.image import AsyncImage
from kivy.core.window import Window
from kivy.uix.dropdown import DropDown
from kivy.animation import Animation
from kivy.uix.widget import Widget
from kivy.uix.stencilview import StencilView
from kivy.metrics import dp
from kivy.clock import Clock
from kivy.properties import (ObjectProperty, NumericProperty, OptionProperty, BooleanProperty, StringProperty)
from kivy.resources import resource_add_path
from kivy.uix.screenmanager import ScreenManager, Screen,SwapTransition, NoTransition,SlideTransition,FadeTransition,WipeTransition,FallOutTransition,RiseInTransition 
from kivy.uix.behaviors import ButtonBehavior
from kivy.lang import Builder
from kivy.garden.mapview import MapView, MapMarker, MarkerMapLayer,MapSource
from kivy.uix.button import Button
from kivy.clock import Clock, mainthread
from kivy.uix.relativelayout import RelativeLayout
from kivy.app import App

import requests
import os   
import os.path
import time
import sys
import urllib2
import json, requests
import math
import urllib
from openpyxl import Workbook
from openpyxl.compat import range
from openpyxl.utils import get_column_letter
from openpyxl import load_workbook
from plyer import gps
from threading import Timer

from mysis.mdata import Asistente
from mysis.mdata2 import Asistente2
from mysis.mdata3 import LineMapLayer


#CARPETAS DEL PROYECTO
patch = os.path.dirname(os.path.abspath(__file__))
hud = patch + '/hud/'
asset = patch + '/mysis/assets/drawable-mdpi/'
icon = patch + '/icons/'
textb = patch + '/textbox/'
database = patch + '/database/'
color = patch + '/mysis/colors/'
fonts = patch + '/mysis/fonts/'
barra = patch + '/hud/barras/'
            
C1 = "[color=#13C0C7]"
C4 = "[color=#000000]"
C2 = "[color=#404040]"
C3 = "[color=#ff3333]"
C5 = "[color=#FF0000]"
C6 = "[color=#C0C0C0]"
ENDC = "[/color]"
#VARIABLES GLOBALES
Hola = "Hola a todos"

# class Label(Label):
    # def __init__(self,**kwargs):
        # super(Label, self).__init__(**kwargs)
        # self.font_name = fonts + "PTS55F.TTF"
# class Button(Button):
    # def __init__(self,**kwargs):
        # super(Button, self).__init__(**kwargs)
        # self.font_name = fonts + "PTS55F.TTF"   
# class TextInput(TextInput):
    # def __init__(self,**kwargs):
        # super(TextInput, self).__init__(**kwargs)
        # self.font_name = fonts + "PTS55F.TTF"   
        
class ClassicTexInput(RelativeLayout):#COMPLEMENTO 'PARENT' EL PROYECTO
    def __init__(self, **kwargs):
        super(ClassicTexInput, self).__init__(**kwargs)
        self.size_hint_y = None
        self.height = 45
        pariente = GridLayout(rows = 1)
        pariente.add_widget(Label(size_hint_x = None, width = 150,markup = True, text = C4 + kwargs["campo"] + ":"))
        pariente.add_widget(TextInput(padding = [0,14,0,0], password = kwargs["passw"],hint_text = kwargs["campo"],background_normal = color + "None.png", background_active = color + "None.png"))
        self.add_widget(pariente)
class Dualbutton(RelativeLayout):
    def __init__(self, **kwargs):
        super(Dualbutton, self).__init__(**kwargs)
        self.size_hint_y = 1
        self.height = 120
        pariente = GridLayout(rows = 1)
        self.b1 = Button(markup = True,text = C4+"[b]Iniciar",background_normal = color + "None.png", background_down = color + "10.png")
        self.b2 = Button(markup = True,text = C4+"Salir",background_normal = color + "None.png", background_down = color + "10.png")
        pariente.add_widget(self.b1)
        pariente.add_widget(self.b2)
        self.add_widget(pariente)
        
class InterfaceManager(RelativeLayout):#COMPLEMENTO 'PARENT' EL PROYECTO
    def __init__(self, **kwargs):
        super(InterfaceManager, self).__init__(**kwargs)
        
        Window.size = (1000,600)
        from desktopmysis.mainscreen import MainScreen
        x = Window.size
        Window.bind(size = lambda x,y: self.hola(x,y))
        self.ventana0 = MainScreen(wsize = Window.size)
        self.add_widget(self.ventana0)
        
        
        
        
        
        
        
        
        #--------------------------------------------------------
        self.log_back = Button(background_down = color + "3.png",background_normal = color + "3.png", opacity = .50, keep_ratio = False, allow_stretch = True)
        self.log_pariente_parent = RelativeLayout(size_hint = (None,None), size = (350,200), pos_hint = {'center_x':.5 , 'center_y':.5})
        log_pariente = GridLayout(cols = 1)
        log_pariente.add_widget(Label(text_size = (350,50), valign = 'middle', halign = 'center',size_hint_y = None, height = 50,markup = True, text = C4+"[b]Inicio de Sesion\nRAG TIRE & AUTO CENTER, SRL"))
        log_pariente.add_widget(ClassicTexInput(campo = "Usuario", passw = False))
        log_pariente.add_widget(ClassicTexInput(campo = "Password", passw = True))
        self.log_pariente_parent.add_widget(Image(opacity = .84,source = color + "16bb.png", allow_stretch = True , keep_ratio = False))
        self.log_pariente_parent.add_widget(log_pariente)
        dualbutton = Dualbutton()
        dualbutton.b1.bind(on_release = lambda x: self.ANIMlog_pariente())
        log_pariente.add_widget(dualbutton)
        self.add_widget(self.log_back)
        self.add_widget(self.log_pariente_parent)
    def hola(self,a,b): 
        print a,b
        self.ventana0.toppanel0.close()
        self.ventana0.toppanel0.x_size = Window.size
        print "hola"
    def ANIMlog_pariente(self):
        anim = Animation(opacity = 0 , d = .5 , t = 'out_expo')
        def endit():
            try:
                self.log_back.parent.remove_widget(self.log_back)
                self.log_pariente_parent.parent.remove_widget(self.log_pariente_parent)
            except:
                pass
        anim.bind(on_complete = lambda x,y: endit())
        anim.start(self.log_back)
        anim.start(self.log_pariente_parent)
        
 
    
    

class MyApp(App):
    def build(self):
        self.title = 'RAG TIRE & AUTO CENTER SRL'
        return InterfaceManager()
        
 

if __name__ in ('__main__', '__android__'):
    MyApp().run()
    

    
    
    
    
    