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



class CustomPopup(RelativeLayout):
    def __init__(self, **kwargs):
        super(CustomPopup, self).__init__(**kwargs)
        self.size_hint_x = None
        self.Opened = False
        self.width = dp(48)
        self.add_widget(Image(source = color + "2.png", keep_ratio = False, allow_stretch = True))
        self.behx = ImageButton(source = kwargs["source"], on_release = lambda x: self.Open())
        self.add_widget(self.behx)
        
        self.menu = RelativeLayout(opacity = 0,size_hint = (None,None), size = (dp(150),dp(54*4)))
        self.menu.add_widget(Image(source = color + "3.png", keep_ratio = False ,allow_stretch = True))
        self.menu_grid = GridLayout(cols = 1)
        self.menu.add_widget(self.menu_grid)
        self.add_widget(self.menu)
        for i in range(4):
            self.menu_grid.add_widget(Button(text = "Opcion "+ str(i), on_release = lambda x: self.Open()))
        self.Opened = True
    def Open(self):
        if self.Opened == False:
            a = Animation(opacity = 1, d = .255, t = 'out_expo')
            a.start(self.menu)

        else:   
            a = Animation(opacity = 0 , d = .255, t = 'in_expo')
            a.start(self.menu)
            

            
class MyApp(App):
    def build(self):
        return CustomPopup(source = "attachment.png")
 

if __name__ in ('__main__', '__android__'):
    MyApp().run()

    
    
    
    
    