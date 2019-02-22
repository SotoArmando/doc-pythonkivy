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



class Slidecircles(RelativeLayout):
    def __init__(self, **kwargs):
        super(Slidecircles, self).__init__(**kwargs)
        self.size_hint_y = None
        #self.height = dp(12)
        pariente = RelativeLayout()
        self.ellipse = ImageButton(size_hint_x = None, width = dp(12), x = (Window.width/2)-dp(6)-dp(40),source = asset + "circle.png")
        pariente.add_widget(self.ellipse)
        pariente.add_widget(ImageButton(source = asset + "circles.png"))
        self.add_widget(pariente)
        self.i_pos = 0 
        self.x_pos = (Window.width/2)-dp(6)-dp(40)
        
        self.add_widget(Button(on_release = lambda x: self.animate_l() , opacity = .5))
    def animate_l(self):
        if self.i_pos <= 0:
            self.i_pos = 4
            x_anim = Animation(x = self.x_pos + dp(20)*self.i_pos, d = .255, t = 'out_circ')
            x_anim.start(self.ellipse)
        else:
            self.i_pos -= 1
            x_anim = Animation(x = self.x_pos + dp(20)*self.i_pos, d = .255, t = 'out_circ')
            x_anim.start(self.ellipse)
    def animate_r(self):
        if self.i_pos >= 4:
            self.i_pos = 0
            x_anim = Animation(x = self.x_pos + dp(20)*self.i_pos, d = .255, t = 'out_circ')
            x_anim.start(self.ellipse)
        else:
            self.i_pos += 1
            x_anim = Animation(x = self.x_pos + dp(20)*self.i_pos, d = .255, t = 'out_circ')
            x_anim.start(self.ellipse)


class MyApp(App):
    def build(self):
        return Slidecircles()
 

if __name__ in ('__main__', '__android__'):
    MyApp().run()

    
    
    
    
    