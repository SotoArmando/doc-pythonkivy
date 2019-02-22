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



class GridButton(RelativeLayout):
    def __init__(self, **kwargs):
        super(GridButton, self).__init__(**kwargs)
        self.size_hint_y = None
        self.height = dp(68)
        anim_parent = GridLayout(rows = 1)
        self.pariente = GridLayout(rows = 1,padding = [16,30,16,16])
        pariente_dim = GridLayout(cols = 1, size_hint_y = 1 )
        pariente_dim_sublabel = GridLayout(rows = 1,size_hint_y = None , height = dp(24))
        self.eliminar_pop = GridLayout(opacity = .0,rows = 1, size_hint_x = None, width = 0)
        
        self.pariente.add_widget(pariente_dim)
        self.pariente.add_widget(ImageButton(on_release = lambda x: self.eliminar(),source = asset + "ic_expand_close.png",size_hint_x = None, width = dp(24)))
        
        pariente_dim.add_widget(Label(halign = 'left',valign = 'top',text_size = (Window.width - dp(24+32),dp(42)),font_size = '16sp',text = "Presentacion de Google"))
        pariente_dim.add_widget(pariente_dim_sublabel)
        self.Img = Image(source = asset + "ic_schedule_black_-1.png",size_hint_x = None, width = dp(24))
        pariente_dim_sublabel.add_widget(self.Img)
        pariente_dim_sublabel.add_widget(Label(halign = 'left',valign = 'middle',text_size = (Window.width - dp(24+44+24),dp(50)),font_size = '16sp',text = "3 Mayo, 2:00 PM - 4:00 PM"))
        
        
        
        
        self.add_widget(Image(keep_ratio = False, allow_stretch = True, source = color + "3.png"))
        self.add_widget(anim_parent)
        anim_parent.add_widget(self.pariente)
        anim_parent.add_widget(self.eliminar_pop)
        
        
        
        self.eliminar_pop.add_widget(Button(on_release = lambda x: self.eliminar(),text = "CANCEL", background_normal = color + "3.png", background_down = color + "3.png"))
        self.eliminar_pop.add_widget(Button(on_release = lambda x: self.eliminar(),text = "OK", background_normal = color + "3.png", background_down = color + "3.png"))
        
        
    def eliminar(self):
        if self.eliminar_pop.width == Window.width:
            eliminar_anim = Animation(width = 0, d = .5, t = 'in_out_quart')
            eliminar_anim1 = Animation(opacity = 0, d = .5, t = 'in_out_quart')
            eliminar_anim2 = Animation(opacity = 1, d = .5, t = 'in_out_quart')
            eliminar_anim.start(self.eliminar_pop)
            eliminar_anim1.start(self.eliminar_pop)
            eliminar_anim2.start(self.pariente)
        elif self.eliminar_pop.width == 0:
            eliminar_anim = Animation(width = Window.width, d = .5, t = 'in_out_quart')
            eliminar_anim1 = Animation(opacity = 1, d = .5, t = 'in_out_quart')
            eliminar_anim2 = Animation(opacity = 0, d = .5, t = 'in_out_quart')
            eliminar_anim.start(self.eliminar_pop)
            eliminar_anim1.start(self.eliminar_pop)
            eliminar_anim2.start(self.pariente)
 
class MyApp(App):
    def build(self):
        return GridButton()
 

if __name__ in ('__main__', '__android__'):
    MyApp().run()

    
    
    
    
    