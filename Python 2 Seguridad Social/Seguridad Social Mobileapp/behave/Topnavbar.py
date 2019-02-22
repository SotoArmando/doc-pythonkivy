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



class TopNavigationS(RelativeLayout):
    def __init__(self, **kwargs):
        super(TopNavigationS, self).__init__(**kwargs)
        self.size_hint_y = None 
        self.height = '79dp'
        background = Image(source = color + "3.png", keep_ratio = False, allow_stretch = True)
        parent = GridLayout(rows = 1)
        self.parent_child = GridLayout(rows = 1, padding = [12,6,12,10])
        self.search_parent = RelativeLayout(size_hint_x = None, width = dp(55))
        self.search_parent_grid = GridLayout(rows = 1, padding = [0,6,0,10]);self.search_parent.add_widget(self.search_parent_grid)
        
        #self.Img = ImageButton(on_release = lambda x: self.bar_animate(),source = asset + "Group 566.png",size_hint = (None,None), size = ('55dp','55dp'))
        self.Img = ImageButton(source = asset + "Group 566.png",size_hint = (None,None), size = ('55dp','55dp'))
        self.Img_parent = Scatter(do_translation_y=False, size_hint = (None,None), size = (dp(55),dp(55)))
        self.Img_parent_parent = RelativeLayout(size_hint = (None,1), width = dp(55))
        self.Img_parent.add_widget(self.Img)
        self.Img_parent_parent.add_widget(self.Img_parent)
        
        
        self.parent_child.add_widget(self.Img_parent_parent)
        self.lbl0 = Label(halign = 'left',valign = 'bottom',text_size = (Window.width - dp(110) - 50,dp(30)),text = "Page Title",font_name = font + "Roboto-Medium.ttf" ,font_size = '20sp')
        self.parent_child.add_widget(self.lbl0)
        
        self.search_parent_grid.add_widget(ImageButton(size_hint = (None,1), size = ('55dp','55dp'),source = asset + "Group 567.png", on_release = lambda x: self.search_animate()))
        self.search_parent_grid.add_widget(TextInput(cursor_color = (1,1,1,.91),foreground_color = [1,1,1,.91],padding = [5,27,0,0],hint_text = "Buscar lugares y personas",font_size = '16sp',background_normal = color + "None.png",background_active = color + "None.png", multiline = False))
        
        parent.add_widget(self.parent_child)
        parent.add_widget(self.search_parent)
        
        
        
        self.add_widget(background)    
        self.add_widget(parent)
        
    def bar_animate(self):

        animate_d = .5
        if self.Img_parent.rotation == 360:
            animate_anim = Animation(rotation = 0, d = animate_d, t = 'in_out_quart')
            animate_anim1 = Animation(opacity = 1 , d = animate_d/2., t = 'in_out_quart')
            animate_anim2 = Animation(opacity = 1 , d = animate_d/2., t = 'in_out_quart')
            def ch(): 
                if self.Img.source == asset + "Group 565.png":
                    self.Img.source = asset + "Group 566.png"
                else:
                    self.Img.source = asset + "Group 565.png"
            animate_anim1.bind(on_complete= lambda x,y: ch())
            animate_anim2 = animate_anim1 + animate_anim2
            animate_anim.start(self.Img_parent)
            animate_anim2.start(self.Img_parent)
        elif self.Img_parent.rotation == 0:
            animate_anim = Animation(rotation = 360, d = animate_d, t = 'in_out_quart')
            animate_anim1 = Animation(opacity = 1 , d = animate_d/2., t = 'in_out_quart')
            animate_anim2 = Animation(opacity = 1 , d = animate_d/2., t = 'in_out_quart')
            def ch(): 
                if self.Img.source == asset + "Group 565.png":
                    self.Img.source = asset + "Group 566.png"
                else:
                    self.Img.source = asset + "Group 565.png"
            animate_anim1.bind(on_complete= lambda x,y: ch())
            animate_anim2 = animate_anim1 + animate_anim2
            animate_anim.start(self.Img_parent)
            animate_anim2.start(self.Img_parent)
        #animate_anim1.start(self.Img_parent)
    def search_animate(self):
        animate_d = .5
        if self.search_parent.width == dp(55):
            animate_anim = Animation(width = Window.width, d = animate_d, t = 'in_out_quart')
            animate_anim1 = Animation(opacity = 0., d = animate_d, t = 'in_out_quart')
            animate_anim2 = Animation(padding = [12,6,12,10], d = animate_d, t = 'in_out_quart')
            animate_anim1.start(self.parent_child)
            animate_anim.start(self.search_parent)
            animate_anim2.start(self.search_parent_grid)
        else:
            animate_anim = Animation(width = dp(55), d = animate_d, t = 'in_out_quart')
            animate_anim1 = Animation(opacity = 1., d = animate_d, t = 'in_out_quart')
            animate_anim2 = Animation(padding = [0,6,0,10], d = animate_d/2, t = 'in_out_quart')
            animate_anim.start(self.search_parent)
            animate_anim2.start(self.search_parent_grid)
            #animate_anim.bind(on_complete = lambda x,y:animate_anim1.start(self.parent_child))
            animate_anim1.start(self.parent_child)
        
    def funcion(self):
        print("hola")

class MyApp(App):
    def build(self):
        return TopNavigationS()
 

if __name__ in ('__main__', '__android__'):
    MyApp().run()

    
    
    
    
    