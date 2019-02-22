#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys  
reload(sys)  
sys.setdefaultencoding('latin-1')



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
from kivy.graphics import Color, Line, Rectangle, Ellipse
import os   
import os.path
import datetime



from utils import GridButton,TwoLineItem,SearchItem,MateriaTitle,TopNavigationS,Datingscreen,BottomNavigation

resource_add_path(os.path.dirname(__file__))

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
import os.path
from utils import CustTextInput



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
    size_hint: None, 1
    size: self.texture_size
'''
Builder.load_string(kv)
#Window.clearcolor =(1,1,1,1)
class MYCircle(Widget):
    def __init__(self, **kwargs):
        super(MYCircle, self).__init__(**kwargs)
        self.bind(pos = self.update_canvas)
        self.bind(size = self.update_canvas)
        self.update_canvas()
        
    def update_canvas(self, *args):
        self.canvas.clear()
        with self.canvas:
            Color(1,1,1,1)
            Ellipse(pos = self.pos , size = self.size)
            
class Loading(RelativeLayout):
    def __init__(self, **kwargs):
        super(Loading, self).__init__(**kwargs)

        self.size_hint_x = None
        self.width = dp(50)
        self.circles = []
        #self.add_widget(Image(source = color + '16.png', keep_ratio = False, allow_stretch = True))
        for i in range(4):
            r = 1/5.
            object = Image(pos_hint = {'center_y':.5,'center_x':(r*(i+1))},size_hint = (None,None), size = (dp(7.5),dp(7.5)),source = asset + 'Ellipse 4'+str(4+i)+'.png', keep_ratio = True, allow_stretch = False)
            self.add_widget(object)
            self.circles.append(object)
        self.animate(1,2)
            
    def animate(self,a,b):
        for i in self.circles:
            r = 1/5.
            if i.pos_hint['center_x'] >= r*4:
                anim = Animation(pos_hint = {'center_x': r} , d = .250 , t = 'out_expo')
            else:
                anim = Animation(pos_hint = {'center_x': i.pos_hint['center_x'] + r }, d = .250 , t = 'out_expo')

            if i == self.circles[-1]:
                anim.bind(on_complete = self.animate)
            anim.start(i)
        
            
class MyApp(App):
    def build(self):
        return Loading()
 

if __name__ in ('__main__', '__android__'):
    MyApp().run()

    
    
    
    
    