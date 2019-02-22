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
class ImageButton(ButtonBehavior, Image): pass



class MateriaTitle(RelativeLayout):
    def __init__(self, **kwargs):
        super(MateriaTitle, self).__init__(**kwargs)
        self.add_widget(Image(keep_ratio = False, allow_stretch = True , source = color + "16.png"))
        self.size_hint_y = None
        self.height = dp(68)
        self.add_widget(Image(source = color + "16.png", keep_ratio = False, allow_stretch = True))
        
        anim_p = GridLayout(cols = 1)
        self.pariente = GridLayout(rows = 1)
        self.ImgB1 = ImageButton(on_release = lambda x: self.anim_parent(x.parent.parent),source = asset + "ic_expand_more_black_24px.png")
        self.ImgB2 = ImageButton(on_release = lambda x: self.anim_parent(x.parent.parent),opacity = .54,source = asset + "ic_delete_black_24px.png" )
        self.Imgp1 = Scatter()
        self.Imgp1_parent = GridLayout(cols =1,size_hint_x = None , width = dp(64))
        self.Imgp2 = Scatter()
        self.Imgp2_parent = GridLayout(cols =1,size_hint_x = None , width = dp(64))
        
        self.Imgp1_parent.add_widget(self.Imgp1)
        self.Imgp1.add_widget(self.ImgB1)
        self.Imgp2_parent.add_widget(self.Imgp2)
        self.Imgp2.add_widget(self.ImgB2)
        
        self.pariente.add_widget(self.Imgp1_parent)
        self.pariente.add_widget(Label(markup = True,font_name = font + "Roboto-Medium.ttf",font_size = '14sp', text = C4+"Logica de Programacion\n[size=12sp]Lorenzo[/size]\nL MX V 2:00 PM - 4:00 PM"))
        self.pariente.add_widget(self.Imgp2_parent)
        
        
        anim_p.add_widget(self.pariente)
        self.add_widget(anim_p)
    def leftbutton(self): return self.ImgB1
    def righbutton(self): return self.ImgB2
    def anim_parent(self,x):
        dur = .225
        parent_anim = Animation(scale = .75, d = dur/2, t = "in_circ")
        parent_anim1 = Animation(scale = 1., d = dur/2, t = "out_circ")
        parent_anim.bind(on_complete = lambda t,p: parent_anim1.start(x))
        parent_anim.start(x)
            
class MyApp(App):
    def build(self):
        return MateriaTitle()
 

if __name__ in ('__main__', '__android__'):
    MyApp().run()

    
    
    
    
    