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
from kivy.uix.togglebutton import ToggleButton
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
C1 = "[color=#13C0C7]"
C4 = "[color=#000000]"
C2 = "[color=#404040]"
C3 = "[color=#ff3333]"
C5 = "[color=#f2f2f2]"
C6 = "[color=#95989A]"
EC = "[/color]"
class ImageButton(ButtonBehavior, Image): pass



class SearchItem(RelativeLayout):
    def __init__(self, **kwargs):
        super(SearchItem, self).__init__(**kwargs)
        self.size_hint_y = None
        self.height = dp(64)
        #self.add_widget(Image(source = color + "16.png", keep_ratio = False, allow_stretch = True))
        self.pariente = GridLayout(rows = 1, padding = [8,0,16,0])
        self.pariente2 = GridLayout(rows = 1, padding = [8,0,16,0],size_hint_y = None, height = 0 , opacity = 0.)
        anim_pariente = GridLayout(cols = 1)
        
        
        self.pariente.add_widget(Button(size_hint_y = 1 , height = dp(64),opacity = 1,size_hint_x = None ,background_normal = asset + "Ellipse 2.png", width = dp(64),font_name = font + "Roboto-Medium.ttf",markup = True ,font_size = '13sp',text = "INS\n203"))
        self.pariente.add_widget(Label(size_hint_x = None , width = dp(8)))
        self.pariente.add_widget(Label(opacity = .91,font_name = font + "Roboto-Medium.ttf",markup = True ,text = C4 + "Introduccion a la Programacion\n[size=12sp]Hirujo"))
        Imgbutton_parent_parent = RelativeLayout(size_hint_x = None , width = 48)
        Imgbutton_parent = Scatter()
        Imgbutton = ImageButton(on_release = lambda x: self.anim_parent(x.parent.parent),on_press = lambda x: self.anim_parent1(), markup = True ,text = C4 + "+", source = asset + "ic_code_black_24px.png")
        
        
        Imgbutton_parent.add_widget(Imgbutton)
        Imgbutton_parent_parent.add_widget(Imgbutton_parent)
        self.pariente.add_widget(Imgbutton_parent_parent)
        anim_pariente.add_widget(self.pariente)
        anim_pariente.add_widget(self.pariente2)
        
        text = ["L","M","MX","J","V","S"]
        for i in text:
            self.pariente2.add_widget(ToggleButton(background_normal = color + "16.png",background_down = color + "16b.png",markup = True,text = C4+i))
        self.pariente2.add_widget(ImageButton(on_press = lambda x: self.anim_parent1(),source = asset + "ic_done_black_24px.png",markup = True,text = C4+"Ok"))
        
        self.add_widget(anim_pariente)
        
        
    def anim_parent(self,x):
        parent_anim = Animation(scale = .5, d = .25, t = "in_circ")
        parent_anim1 = Animation(scale = 1., d = .25, t = "out_circ")
        parent_anim.bind(on_complete = lambda t,p: parent_anim1.start(x))
        parent_anim.start(x)
        
    def anim_parent1(self):
        if self.pariente2.height == dp(64):
            parent_anim = Animation(height = dp(0),d = .25 , t = "out_circ")
            parent_anim1 = Animation(opacity = 0.,d = .25 , t = "out_circ")
            parent_anim2 = Animation(opacity = 1.,d = .25 , t = "out_circ")
            parent_anim.start(self.pariente2)
            parent_anim1.start(self.pariente2)
            parent_anim2.start(self.pariente)
        elif self.pariente2.height == dp(0):
            parent_anim = Animation(height = dp(64),d = .25 , t = "out_circ")
            parent_anim1 = Animation(opacity = 1.,d = .25 , t = "out_circ")
            parent_anim2 = Animation(opacity = 0.,d = .25 , t = "out_circ")
            parent_anim.start(self.pariente2)
            parent_anim1.start(self.pariente2)
            parent_anim2.start(self.pariente)
            
class MyApp(App):
    def build(self):
        return SearchItem()
 

if __name__ in ('__main__', '__android__'):
    MyApp().run()

    
    
    
    
    