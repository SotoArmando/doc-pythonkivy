#!/usr/bin/env python55555533yyyyyyyyyyyyyyyyyyyyy555555
# -*- coding: utf-8 -*-

import kivy
from kivy.config import Config
Config.set('graphics','borderless', 1)
Config.set('graphics','position','custom')
Config.set('graphics','window_state','visible')
Config.set('graphics','resizable',0)
Config.set('graphics','left',1000)
Config.set('graphics','top',35)
import threading 
from threading import *
from kivy.effects.opacityscroll import OpacityScrollEffect
from kivy.effects.scroll import ScrollEffect
from kivy.garden.mapview import MapView, MapMarker, MarkerMapLayer, MapSource
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
from submain import NavigationDrawerException,ImageButton,NavigationDrawer
import requests
import os   
import os.path
import time
import sys
import urllib2
import json, requests
import math
from openpyxl import Workbook
from openpyxl.compat import range
from openpyxl.utils import get_column_letter
from openpyxl import load_workbook
from plyer import gps
from threading import Timer



reload(sys)
resource_add_path(os.path.dirname(__file__))

Window.size = (426,950)

Builder.load_string('''
<NavigationDrawer>:
    size_hint: (1,1)
    _side_panel: sidepanel
    _main_panel: mainpanel
    _join_image: joinimage
    side_panel_width: min(0.5*self.width, 0.5*self.width)
    BoxLayout:
        id: sidepanel
        y: root.y
        x: root.x - \
           (1-root._anim_progress)* \
           root.side_panel_init_offset*root.side_panel_width
        height: root.height
        width: root.side_panel_width
        opacity: root.side_panel_opacity + \
                 (1-root.side_panel_opacity)*root._anim_progress
        canvas:
            Color:
                rgba: (0,0,0,.80)
            Rectangle:
                pos: self.pos
                size: self.size
        canvas.after:
            Color:
                rgba: (1,1,1,(1-root._anim_progress)*root.side_panel_darkness)
            Rectangle:
                size: self.size
                pos: self.pos
    BoxLayout:
        id: mainpanel
        x: root.x + \
           root._anim_progress * \
           root.side_panel_width * \
           root.main_panel_final_offset
        y: root.y
        size: root.size
        canvas:
            Color:
                rgba: (0,0,0,1)
            Rectangle:
                pos: self.pos
                size: self.size
        canvas.after:
            Color:
                rgba: (0,0,0,root._anim_progress*root.main_panel_darkness)
            Rectangle:
                size: self.size
                pos: self.pos
    Image:
        id: joinimage
        opacity: min(sidepanel.opacity, 0 if root._anim_progress < 0.00001 \
                 else min(root._anim_progress*40,1))
        source: root._choose_image(root._main_above, root.separator_image)
        mipmap: False
        width: 1
        height: root._side_panel.height
        x: (mainpanel.x - self.width + 1) if root._main_above \
           else (sidepanel.x + sidepanel.width - 1)
        y: root.y
        allow_stretch: True
        keep_ratio: False
''')

C1 = "[color=#13C0C7]"
C4 = "[color=#000000]"
C2 = "[color=#404040]"
C3 = "[color=#ff3333]"

def_textsize = (Window.width-50,50)
patch = os.path.dirname(os.path.abspath(__file__))
hud = patch + '/hud/'
icon = patch + '/icons/'
font = patch + '/fonts/'
textb = patch + '/textbox/'
database = patch + '/database/'
color = patch + '/hud/colors/'
barra = patch + '/hud/barras/'
Wwi = Window.width
Whe = Window.height
b = font + "Roboto-Medium.ttf"
class DefaultButton(Button):
    Button.font_name = font + "Roboto-Regular.ttf"
class InterfaceManager(RelativeLayout):
    def __init__(self, **kwargs):
        super(InterfaceManager, self).__init__(**kwargs)
        self.maingrid = GridLayout(cols  = 1)
        self.add_widget(self.maingrid)
        View1Mainimage = Image(size_hint = (1,None),height = 200,source = "recipe.png",keep_ratio = True, allow_stretch = False)
        
        for i in range(5):
            if i == 0:
                self.maingrid.add_widget(View1Mainimage)
                self.maingrid.add_widget(Button(height = 100, size_hint_y = None,size_hint_x = .8,text_size = ((Wwi)-50, 100),valign = "middle",font_size = 19,background_normal = color + "16.png",text = C2+"Nombre receta",markup = True))
            View1item = self.Alarmacocina_Objeto1(i+1)
            View1Subitem = self.Alarmacocina_Objeto2(View1item.children[1])
            self.maingrid.add_widget(View1item)
            self.maingrid.add_widget(View1Subitem)

        
        
    def Alarmacocina_Objeto1(self,N):
        Objeto = GridLayout(cols = 3,size_hint = (1,None), height = 100)
        Objeto.add_widget(Button(size_hint_x = None, width = 100,text_size = (50, 100),halign = "center",valign = "middle",font_size = 36,background_disabled_normal = color + "16.png",text = C4+str(N),markup = True,disabled = True))
        Objeto.add_widget(Button(size_hint_x = .8,text_size = ((Wwi-200)-50, 100),valign = "middle",font_size = 17,background_normal = color + "16.png",text = C2+"[b]Paso "+str(N)+"[/b]\nDescripcion",markup = True))
        Objeto.add_widget(Image(size_hint = (None, None), size = (100,100), source = "checked.png",text_size = ((Wwi*0.30)-50, 100),halign = "center",valign = "middle",font_size = 32,background_normal = color + "16.png",text = C4+">",markup = True))
        return Objeto
        
    def Alarmacocina_Objeto2(self,Y):
        def Animate(X):
            if X.height == 100:
                Anim = Animation(height = 0)
                Anim.start(X)
                X.font_size = 0
            else:
                Anim = Animation(height = 100)
                Anim.start(X)
                X.font_size = 17
                
        Objeto = Button(border = [0,0,0,0],font_size = 0,markup = True,text = C1+"Para ser preciso\nme siento muy bien.",size_hint_y = None, height = 0, background_normal = color + "16.png")
        Y.bind(on_release = lambda x: Animate(Objeto))
        return Objeto



class MyApp(App):
    def build(self):
        return InterfaceManager()
 

if __name__ in ('__main__', '__android__'):
    MyApp().run()

    
    
    
    
    