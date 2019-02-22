#!/usr/bin/env python55555533yyyyyyyyyyyyyyyyyyyyy555555
# -*- coding: utf-8 -*-
from kivy.config import Config
Config = None
import kivy
import requests
from kivy.garden.mapview import MapView, MapMarker, MarkerMapLayer,MapSource
from kivy3dgui.layout3d import Layout3D 
from kivy3dgui.layout3d import Node
from kivy.uix.bubble import Bubble
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
import time
import json
import urllib2
import os   
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
from kivy.uix.behaviors import ButtonBehavior
import math
    
from kivy.lang import Builder
import os.path
import time
import sys


reload(sys)
sys.setdefaultencoding('latin1')
resource_add_path(os.path.dirname(__file__))


from kivy.garden.mapview import MapView, MapMarker, MarkerMapLayer,MapSource
import json, requests
from kivy.uix.button import Button
from plyer import gps
from kivy.properties import StringProperty
from kivy.clock import Clock, mainthread
from kivy.uix.screenmanager import ScreenManager, Screen,SwapTransition, NoTransition,SlideTransition,FadeTransition,WipeTransition,FallOutTransition,RiseInTransition 

from kivy.uix.relativelayout import RelativeLayout
from kivy.app import App
Builder.load_string('''
<RotatedImage>:
    canvas.before:
        PushMatrix
        Rotate:
            angle: root.angle
            axis: 0, 0, 1
            origin: root.center
    canvas.after:
        PopMatrix
''')
patch = os.path.dirname(os.path.abspath(__file__))
hud = patch + '/hud/'
icons = patch + '/icons/'
textb = patch + '/textbox/'
database = patch + '/database/'
color = patch + '/hud/color/'
class RotatedImage(MapView):
    angle = NumericProperty()

class InterfaceManager(Layout3D):
    def __init__(self, **kwargs):
        super(InterfaceManager, self).__init__(**kwargs)
        
        self.size_hint = (1,1.2)
        self.canvas_size = Window.size
        self.post_processing = True
        
        self.Main_Node1 = Node(rotate = (105, 1, 0, 0), scale = (1, 1, .01), translate = (0, 0, -50), effects = True, meshes = ("./data/obj/2dbox.obj",))
        self.Main_Node2 = Node(rotate = (0, 0, 1, 0),size_hint = (None,None), size = (100,100), scale = (.01, .01, .01), translate = (0, 0, -25), effects = True, meshes = ("./data/obj/2dbox.obj",))
        self.GridLayout1 = GridLayout(cols = 1, size_hint = (1,1))
 
        
        self.Main_Node1Layout1 = RelativeLayout(cols = 1, size_hint = (None,None),size = Window.size)
        self.Main_Node1Layout1a = GridLayout(cols = 1, size_hint = (1,None) , height =100)
        self.add_widget(self.Main_Node1)
        self.add_widget(self.Main_Node2)
        self.Main_Node1.add_widget(self.Main_Node1Layout1)
        self.Main_Node2.add_widget(Button(size_hint = (1,1), size = (100,100), background_normal = color+"5.png"))
        accesstoken = "pk.eyJ1IjoiYXJtYW5kbzI5IiwiYSI6ImNpd282ZHJ3azAwMWoydHFuZmJudnNzYzEifQ.12vIF51BCThjrut4Q56sGg"
        sourcex = MapSource(url="https://api.mapbox.com/styles/v1/mapbox/streets-v10/tiles/256/{z}/{x}/{y}?access_token=pk.eyJ1IjoibWFjYXR1cyIsImEiOiJjaXlubGRkdXAwMDJ1MzNwZjdwanhkdnd6In0.eYV9WVlCsI44Ku0HSup7Pg",
        cache_key="custom_map1s",tile_size=256,
        image_ext="jpg", attribution="@Armando Jose Soto Melo")
        self.mv = MapView(zoom = 15, lat = 18.454651 , lon = -69.971119, map_source = sourcex)
        self.Main_Node1Layout1.add_widget(self.mv)
        self.Main_Node1Layout1.add_widget(self.Main_Node1Layout1a)  
        m1 = MapMarker(lat = 18.454651 , lon = -69.971119)  # Lille
        self.mv.add_marker(m1)
        
 

        
        
class MyApp(App):
    def build(self):
        return InterfaceManager()
 

if __name__ in ('__main__', '__android__'):
    MyApp().run()

    
    
    
    
    