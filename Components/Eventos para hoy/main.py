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



class Datingscreen(RelativeLayout):
    def __init__(self, **kwargs):
        super(Datingscreen, self).__init__(**kwargs)
        self.size_hint_y = None
        self.height = dp(48)
        self.add_widget(Image(source = color+"2.png", keep_ratio = False, allow_stretch = True))
        self.pariente_grid = GridLayout(spacing = [64,0],rows = 1, size_hint_x = None, width = dp(0), padding = [32,0,16,0])
        pariente = RelativeLayout()
        
        pariente.add_widget(self.pariente_grid)
        pariente.add_widget(ImageButton(opacity = .54,on_release = lambda x: self.move_left(),source = asset + "ic_keyboard_arrow_right_black.png",x = Window.width - dp(64)+16,size_hint_x = None , width = dp(64)))
        pariente.add_widget(ImageButton(opacity = .54,on_release = lambda x: self.move_right(),source = asset + "ic_keyboard_arrow_left_black_.png",x = -16,size_hint_x = None , width = dp(64)))
        self.add_line("Logica de Programacion")
        self.add_line("Fundamentos de Programacion")
        self.add_line("Calculo Integral")
        self.add_line("Lengua Espanola")
 


        self.add_widget(pariente)
    def move_left(self):
        move_anim = Animation(x = self.pariente_grid.x - Window.width/2, d = .65 , t = 'out_circ' )
        move_anim.start(self.pariente_grid)
        
    def move_right(self):
        move_anim = Animation(x = 0, d = .65 , t = 'in_out_back' )
        move_anim.start(self.pariente_grid)
        
    
    def add_line(self,text):
        i_width = (dp(8.5) * len(text)) + dp(48)

        children = RelativeLayout(size_hint_x = None)
        children.add_widget(Image(pos_hint = {'center_y':.5},x = 1,size_hint = (None,1), size = (dp(40),dp(38)) , height = '38dp',source = asset + "Ellipse 3.png", keep_ratio = False, allow_stretch = True))
        children.add_widget(Image(pos_hint = {'center_y':.5},x = i_width-1,size_hint = (None,1) , size = (dp(40),dp(38)),source = asset + "Ellipse 3.png", keep_ratio = False, allow_stretch = True))
        children.add_widget(Image(pos_hint = {'center_y':.5},x = dp(20),size_hint_y = 1 , height = '38dp',source = asset + "Rectangle 68.png", keep_ratio = False, allow_stretch = True))
        img0 = ImageButton(on_release = lambda x: self.anim_parent(x.parent.parent),opacity = .84,source = asset + "ic_assignment_late_black_24px.png", keep_ratio = True, allow_stretch = False)
        img0parent = Scatter()
        img0_parent_parent = RelativeLayout(cols = 1,pos_hint = {'center_y':.5},x = dp(15),size_hint_x = None , width = '24dp',size_hint_y = None , height = '38dp')
        
        img1 = ImageButton(on_release = lambda x: self.anim_parent(x.parent.parent),opacity = .84,source = asset + "ic_delete_black_24px.png", keep_ratio = True, allow_stretch = False)       
        img1parent = Scatter()
        img1_parent_parent = RelativeLayout(cols = 1,pos_hint = {'center_y':.5},x = i_width+4,size_hint_x = None , width = '24dp',size_hint_y = None , height = '38dp')
        
        
        img0parent.add_widget(img0)
        img0_parent_parent.add_widget(img0parent)
        img1parent.add_widget(img1)
        img1_parent_parent.add_widget(img1parent)
        
        
        children.add_widget(img0_parent_parent)
        children.add_widget(img1_parent_parent)
        children.add_widget(Label(pos_hint = {'center_y':.5},x = dp(30),text_size = (i_width - dp(36),dp(24)),valign = 'middle',halign = "left",markup = True, opacity = .84,text = C4+text))
        children.width = i_width
        self.pariente_grid.add_widget(children)
        self.pariente_grid.width += i_width+dp(75)
        
    def anim_parent(self,x):
        print x
        dur = .225
        parent_anim = Animation(scale = .75, d = dur/2, t = "in_circ")
        parent_anim1 = Animation(scale = 1., d = dur/2, t = "out_circ")
        parent_anim.bind(on_complete = lambda t,p: parent_anim1.start(x))
        parent_anim.start(x)
        
class MyApp(App):
    def build(self):
        return Datingscreen()
 

if __name__ in ('__main__', '__android__'):
    MyApp().run()

    
    
    
    
    