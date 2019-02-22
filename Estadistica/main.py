#!/usr/bin/env python55555533yyyyyyyyyyyyyyyyyyyyy555555
# -*- coding: utf-8 -*-

import json
import math
import os
import os.path
import sys
import threading
import time
import urllib2
from threading import *
from threading import Timer

import kivy
import requests
from kivy.adapters.listadapter import ListAdapter
from kivy.adapters.models import SelectableDataItem
from kivy.adapters.simplelistadapter import SimpleListAdapter
from kivy.animation import Animation
from kivy.app import App
from kivy.base import runTouchApp
from kivy.clock import Clock, mainthread
from kivy.config import Config
from kivy.core.window import Window
from kivy.effects.opacityscroll import OpacityScrollEffect
from kivy.effects.scroll import ScrollEffect
from kivy.garden.mapview import MapMarker, MapSource, MapView, MarkerMapLayer
from kivy.graphics import *
from kivy.graphics.instructions import InstructionGroup
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.parser import parse_color
from kivy.properties import (BooleanProperty, ListProperty, NumericProperty,
                             ObjectProperty, OptionProperty, StringProperty)
from kivy.resources import resource_add_path
from kivy.uix.accordion import Accordion, AccordionItem
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.bubble import Bubble
from kivy.uix.button import Button
from kivy.uix.checkbox import CheckBox
from kivy.uix.dropdown import DropDown
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import AsyncImage, Image
from kivy.uix.label import Label
from kivy.uix.listview import (CompositeListItem, ListItemButton,
                               ListItemLabel, ListView)
from kivy.uix.popup import Popup
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.scatter import Scatter
from kivy.uix.screenmanager import (FadeTransition, FallOutTransition,
                                    NoTransition, RiseInTransition, Screen,
                                    ScreenManager, SlideTransition,
                                    SwapTransition, WipeTransition)
from kivy.uix.scrollview import ScrollView
from kivy.uix.stencilview import StencilView
from kivy.uix.textinput import TextInput
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.widget import Widget
from kivy.utils import get_color_from_hex, get_hex_from_color
from openpyxl import Workbook, load_workbook
from openpyxl.compat import range
from openpyxl.utils import get_column_letter
from plyer import gps

from paint import MyPaintWidget
from smain import NavigationDrawer

Config.set('graphics','borderless', 0)
Config.set('graphics','resizable', 1)
Config.set('graphics','window_state', 'maximized')




reload(sys)
resource_add_path(os.path.dirname(__file__))




C1 = "[color=#13C0C7]"
C4 = "[color=#000000]"
C2 = "[color=#404040]"
C3 = "[color=#ff3333]"

def_textsize = (Window.width-50,50)
patch = os.path.dirname(os.path.abspath(__file__))
hud = patch + '/hud/'
icon = patch + '/icons/'
textb = patch + '/textbox/'
database = patch + '/database/'
color = patch + '/hud/colors/'
barra = patch + '/hud/barras/'
font = patch + '/fonts/'

class InterfaceManager(RelativeLayout):
    def __init__(self, **kwargs):
        super(InterfaceManager, self).__init__(**kwargs)

        
        self.lay3 = MyPaintWidget()
        
        self.Screen1()
        self.add_widget(self.lay3)
        

    def Canvaz(self):
        with self.lay3.canvas:
            Color(1., 0, 0)
            Line(points=[250, 300, 250, 700], width=1)
            Line(points=[50, 500, 700, 500], width=1)

    def Screen1(self):
        self.screen1 = GridLayout(cols = 1)
        self.menubar = GridLayout(rows = 1, size_hint_y = None, height = 50, spacing = 1)
        for i in range(1):
            clearbtn = Button(background_normal = color + "15.png")
            self.menubar.add_widget(clearbtn)
            clearbtn.bind(on_release= lambda x:self.lay3.canvas.clear())

        self.texto = TextInput(font_size = '20sp', font_name = font +"Roboto-Regular.ttf", background_active = color+"16.png", background_normal = color+"16.png")
        self.add_widget(self.screen1)        
        self.screen1.add_widget(self.menubar)
        self.screen1.add_widget(Image(keep_ratio = False, allow_strech = True, source = color + "3.png", size_hint_y = None, height = 1))
        self.screen1.add_widget(self.texto)


        
        
        
class MyApp(App):
    def build(self):
        return InterfaceManager()
 

if __name__ in ('__main__', '__android__'):
    MyApp().run()
