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



class Personal_Pos(RelativeLayout):
    def __init__(self, **kwargs):
        super(Personal_Pos, self).__init__(**kwargs)
        self.size_hint = (None,None)
        self.size = (dp(64),dp(64))
        self.img = Image(opacity = 0,source = "circle.png", keep_ratio = False, allow_stretch = True, size_hint = (None,None), size = (dp(0),dp(0)), pos_hint = {'center_x':.5, 'center_y':.5})
        self.img1 = Image(opacity = 0,source = "circle2.png", keep_ratio = False, allow_stretch = True, size_hint = (None,None), size = (dp(16),dp(16)), pos_hint = {'center_x':.5, 'center_y':.5})
        self.add_widget(self.img)
        self.add_widget(self.img1)
        #self.pos_hint = {'center_x':.5, 'center_y':.5}
        self.animate()
    def animate(self):
        a = Animation(opacity = 1,size = (dp(64),dp(64)), d = .5 , t = 'out_quart')
        b = Animation(opacity = 1, d = .5 , t = 'out_quart')
        b.bind(on_complete = lambda x,y: a.start(self.img))
        b.start(self.img1)
class MyApp(App):
    def build(self):
        return Personal_Pos()
 

if __name__ in ('__main__', '__android__'):
    MyApp().run()

    
    
    
    
    