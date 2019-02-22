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
        self.size_hint_y = None ; self.height = dp(56)
        self.add_widget(Image(source = color + "16b.png", allow_stretch = True, keep_ratio = False))
        pariente = GridLayout(rows = 3)
        titles = GridLayout(rows = 1 , size_hint_y = None, height = dp(56))
        titles.add_widget(Image(source = color + '15.png', allow_stretch = True, keep_ratio = False,size_hint_x = None, width = dp(56)))
        titles.add_widget(Button(text_size = (Window.width - dp(56*2) - dp(25), dp(56)),valign = 'middle',markup = True,text = C4+"[b]Cliente[/b]\nsubdato", background_normal = color + '16.png'))
        #----------------------animated
        scatter0_parent = GridLayout(cols = 1, size_hint_x = None, width = dp(56))
        scatter0_parent_child = RelativeLayout()
        scatter0 = Scatter()
        scatter0_child = ImageButton(size_hint = (None,None), size = (dp(56),dp(56)), source = color + '15.png',allow_stretch = True , keep_ratio = False, on_release = lambda x: self.animate(x))
        scatter0_child.bind(on_release = lambda x: self.open())
        scatter0_parent.add_widget(scatter0_parent_child)
        scatter0_parent_child.add_widget(scatter0)
        scatter0.add_widget(scatter0_child)
        
        titles.add_widget(scatter0_parent)
        pariente.add_widget(titles)
        #--------------------------------------
        self.titles_data = GridLayout(cols = 2,opacity = 0.)
        for i in range(10):self.titles_data.add_widget(Label(valign = 'middle',text_size = (Window.width/2,dp(200/5)),markup = True,text = C4+"[b][campo]: [/b] Base de datos no conectada."))
        
        shadow_parent = GridLayout(cols = 1,size_hint_y = None, height = dp(0))
        shadow_parent.add_widget(Image(source = "Repeat Grid 20.png",allow_stretch = True, keep_ratio = False, height = dp(25)))
        pariente.add_widget(shadow_parent)
        pariente.add_widget(self.titles_data)
        
        self.add_widget(pariente)
        
    def open(self):
        if self.titles_data.opacity == 0.:
            anim = Animation(height = dp(256), d = .255, t = 'out_expo')
            anim1 = Animation(opacity = 1., d = .255, t = 'out_expo')
            anim.start(self)
            anim1.start(self.titles_data)
        elif self.titles_data.opacity == 1.:
            anim = Animation(height = dp(56), d = .255, t = 'out_expo')
            anim1 = Animation(opacity = 0.,  d = .255, t = 'out_expo')
            anim.start(self)
            anim1.start(self.titles_data)
            
    def animate(self,object):
        anim = Animation(size = (dp(50),dp(50)),x = object.x + 3, y = object.y + 3, d = .225/2 , t = 'out_quart') + Animation(size = (dp(56),dp(56)),x = object.x, y = object.y, d = .225/2 , t = 'in_quart')
        anim.start(object)

class MyApp(App):
    def build(self):
        return CleanButton()
 

if __name__ in ('__main__', '__android__'):
    MyApp().run()

    
    
    
    
    