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



class TwoLineItem(RelativeLayout):
    def __init__(self,i_text,sub_text, **kwargs):
        super(TwoLineItem, self).__init__(**kwargs)
        self.add_widget(Image(keep_ratio = False, allow_stretch = True , source = color + "16.png"))
        self.size_hint_y = None
        self.height = dp(70)
        anim_parent = GridLayout(cols = 1)
        pariente_p = RelativeLayout(size_hint_y = None, height = dp(68))
        pariente = GridLayout(rows = 1, padding = [16,8,16,0], spacing = [8,])
        pariente.add_widget(Image(source = asset + "Group 571.png", keep_ratio = False, allow_stretch = True, size_hint = (None,1), size = (dp(64),dp(64))))
        dim = GridLayout(cols = 1)
        dim.add_widget(Label(halign = 'left', valign = 'bottom',text_size = (dp(200),dp(40)),markup = True,text = C4+i_text,font_size = '16sp'))
        dim.add_widget(Label(opacity =.74,halign = 'left', valign = 'middle',text_size = (dp(200),dp(20)),markup = True,text = C4+sub_text,font_size = '14sp'))
        pariente.add_widget(dim)
        pariente.add_widget(ImageButton(on_release = lambda x: self.openme(),opacity = .54,source = asset + "ic_info_black_24px.png", keep_ratio = True, allow_stretch = False, size_hint = (None,1), size = (dp(24),dp(64))))
        
        button_anim = RelativeLayout()
        self.new_asset_parent = RelativeLayout()
        self.new_asset = Scatter(opacity = 0)
        self.new_asset_parent.add_widget(self.new_asset)
        self.img = Image(source = asset + "Group 571.png")
        self.new_asset.add_widget(self.img)
        button_anim.add_widget(self.new_asset_parent)
        self.btn = Button(background_normal = color + "10.png",on_release = lambda x: self.animbutton(),opacity = .0)
        button_anim.add_widget(self.btn)
        pariente_p.add_widget(button_anim)
        
        
        
        
        pariente_p.add_widget(pariente)
        anim_parent.add_widget(pariente_p)
        self.add_widget(anim_parent)
        
        self.secondbutton = GridLayout(opacity = 0.,height = 0,rows = 1, size_hint_y = 1, padding = [0,0,0,0])
        self.secondbutton.add_widget(Label())
        self.secondbutton.add_widget(ImageButton(size_hint_x= None ,allow_stretch = True, width = dp(100), source = asset + "Group 572.png"))
        anim_parent.add_widget(self.secondbutton)
        
    def animbutton(self):
        d = .225
        animbutton_anim = Animation(d = d,opacity =.24, t = 'out_circ', scale = 5.)
        animbutton_anim1 = Animation(d = d,opacity =.0, scale = 1., t = 'in_circ')
        animbutton_anim.bind(on_complete = lambda x,y: animbutton_anim1.start(self.new_asset))
        animbutton_anim.start(self.new_asset)
        animbutton_anim2 = Animation(d = d,opacity =.34, t = 'out_circ')
        animbutton_anim3 = Animation(d = d,opacity =.0, t = 'in_circ')
        animbutton_anim4 = animbutton_anim2 + animbutton_anim3
        animbutton_anim4.start(self.btn)

        
    def openme(self):
        if self.height == dp(70):
            openme_anim = Animation(height = dp(110), d = .3 ,t = "out_circ")
            openme_anim1 = Animation(opacity = 1., d = .3 ,t = "out_circ")
            openme_anim.start(self)
            openme_anim1.start(self.secondbutton)
        if self.height == dp(110):
            openme_anim = Animation(height = dp(70), d = .3 ,t = "out_circ")
            openme_anim1 = Animation(opacity = 0., d = .3 ,t = "out_circ")
            openme_anim.start(self)
            openme_anim1.start(self.secondbutton)
            
class MyApp(App):
    def build(self):
        return TwoLineItem("self_text","sub_text")
 

if __name__ in ('__main__', '__android__'):
    MyApp().run()

    
    
    
    
    