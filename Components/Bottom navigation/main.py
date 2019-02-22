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



class BottomNavigation(RelativeLayout):
    def __init__(self, **kwargs):
        super(BottomNavigation, self).__init__(**kwargs)
        
        self.size_hint_y = None
        self.height = '56dp'
        self.background = Image(source = color + "3.png", keep_ratio = False, allow_stretch = True)
        self.add_widget(self.background)
        self.colors = ScreenManager()
        self.parent = GridLayout(rows = 1)
        self.colors.transition = FadeTransition(duration = .25)
     
        #eTransition,FadeTransition,WipeTransition,FallOutTransition,NoTransition ,RiseInTransition 
  
        colors = ["3","2","15","10"]
        text =  ["Movies & TV", "Music", "Books", "Newsstand"]
        img =  ["ic_alarm_black_24px", "ic_bookmark_border_black_24px", "ic_class_black_24px", "ic_copyright_black_24px"]
        for i in range(4):
            color_screen = Screen(name = str(i))
            color_screen.add_widget(Image(source = color + colors[i] + ".png", keep_ratio = False, allow_stretch = True))
            self.colors.add_widget(color_screen)
            
        for i in range(4):
            if i == 1:
                button_parent = GridLayout(size_hint_x = None, width = '96dp',cols = 1, padding = [12,6,12,10])
                button_label = Label(size_hint_y = None, height = '14sp',font = font + "Roboto-Regular.ttf",font_size = '14sp',text = text[i], markup = True, halign = 'center', valign = 'bottom')
                
                button_parent.add_widget(Label())
                button_parent.add_widget(ImageButton(on_release = lambda x: self.animate(x.parent.children[0]),size_hint = (1,None), size = (dp(24),dp(24)), source = asset + img[i] +".png", keep_ratio = False, allow_stretch = False))
                button_parent.add_widget(button_label)
                self.parent.add_widget(button_parent)
            else:
                button_parent = GridLayout(size_hint_x = None, width = '96dp',cols = 1, padding = [12,6,12,10])
                button_label = Label(opacity = 0.,size_hint_y = None,height= 0, font = font + "Roboto-Regular.ttf",font_size = '14sp',text = text[i], markup = True, halign = 'center', valign = 'bottom')
                
                button_parent.add_widget(Label())
                button_parent.add_widget(ImageButton(on_release = lambda x: self.animate(x.parent.children[0]),size_hint = (1,None), size = (dp(24),dp(24)), source = asset + img[i] +".png", keep_ratio = False, allow_stretch = False))
                button_parent.add_widget(button_label)
                self.parent.add_widget(button_parent)
        
        
        self.add_widget(self.colors)
        self.add_widget(self.parent)
        
    def animate(self,x):
        animate_anim = Animation(opacity = 1.,height = sp(14), d = .25, t = 'in_out_circ')
        animate_anim1 = Animation(width = dp(Window.width/4 + 36),d = .25, t = 'in_out_circ')
        animate_anim2 = Animation(opacity = .91,d = .25, t = 'in_out_circ')
        animate_anim.start(x)
        animate_anim1.start(x.parent)
        animate_anim2.start(x.parent.children[1])
        otros = x.parent.parent.children
        count = 0
        for i in otros:
            if (count == 9) or (count == 9) :
                pass
            else:
                if i == x.parent: pass
                else:
                    animate_anim = Animation(opacity = 0.,height = sp(0), d = .20, t = 'in_out_circ')
                    animate_anim1 = Animation(width = dp(Window.width/4 - 12),d = .25, t = 'in_out_circ')
                    animate_anim2 = Animation(opacity = .54,d = .25, t = 'in_out_circ')
                    animate_anim.start(i.children[0])
                    animate_anim2.start(i.children[1])
                    animate_anim1.start(i)
            count += 1
            
        self.colors.current = self.colors.next()

                
    
    def funcion(self):
        print("hola")

class MyApp(App):
    def build(self):
        
        return BottomNavigation(y = Window.height - dp(56))
 

if __name__ in ('__main__', '__android__'):
    MyApp().run()

    
    
    
    
    