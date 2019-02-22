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

#CARPETAS DEL PROYECTO
patch = os.path.dirname(os.path.abspath(__file__))
asset = patch + '/assets/drawable-mdpi/'
color = patch + '/colors/'
font = patch + '/fonts/'
C1 = "[color=#13C0C7]"
C4 = "[color=#000000]"
C2 = "[color=#404040]"
C3 = "[color=#ff3333]"
C5 = "[color=#f2f2f2]"
C6 = "[color=#95989A]"
EC = "[/color]"
kv = '''
<MyButton>:
    size_hint: None, None
    size: self.texture_size
'''
Builder.load_string(kv)
class ImageButton(ButtonBehavior, Image): pass
class MyButton(Button):
    pass


class CleanButton(RelativeLayout):
    def __init__(self, **kwargs):
        super(CleanButton, self).__init__(**kwargs)
        self.add_widget(Image(source = color + '16.png', keep_ratio = False, allow_stretch = True))
        self.size_hint_y = None
        self.height = '51dp'
        mywid = GridLayout(cols = 4,padding = [dp(16),0,dp(16),0])
        mywid.add_widget(ImageButton(source = color + "10.png",size_hint_x = None, width = '52dp'))
        mywid.add_widget(MyButton(background_normal = color+'16.png',markup = True,text = C4+"Cleanbutton"))
        mywid.add_widget(Label())
        mywid.add_widget(CheckBox())
        
        self.add_widget(mywid)


class MyApp(App):
    def build(self):
        return CleanButton()
 

if __name__ in ('__main__', '__android__'):
    MyApp().run()

    
    
    
    
    