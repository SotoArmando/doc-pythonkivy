#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys  
reload(sys)  
sys.setdefaultencoding('latin-1')

from kivy.config import Config
Config.set('graphics','borderless', 1)
Config.set('graphics','position','custom')
Config.set('graphics','window_state','visible')
Config.set('graphics','resizable',0)
Config.set('graphics','left',500)
Config.set('graphics','top',35)

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
kv = '''
<MyButton>:
    size_hint: None, 1
    size: self.texture_size
'''
Builder.load_string(kv)
class ImageButton(ButtonBehavior, Image): pass
class MyButton(Button):
    pass
class CleanButton(RelativeLayout):
    def __init__(self,i_img,i_text, **kwargs):
        super(CleanButton, self).__init__(**kwargs)
        self.add_widget(Image(source = color + '16.png', keep_ratio = False, allow_stretch = True))
        self.size_hint_y = None
        self.height = '51dp'
        mywid = GridLayout(cols = 5,padding = [dp(8),0,dp(0),0])
        mywid.add_widget(ImageButton(source = asset + i_img +".png",size_hint_x = None, width = '52dp'))
        mywid.add_widget(Label(size_hint_x = None , width = '8dp'))
        mywid.add_widget(MyButton(valign = 'middle',background_normal = color+'16.png',markup = True,font_size = '16sp',text = C4+i_text))
        mywid.add_widget(Label())
        mywid.add_widget(CheckBox(background_checkbox_normal = asset + "ic_check_box_outline_blank_bl.png",background_checkbox_down = asset + "ic_check_box_black_24px.png",))
        
        self.add_widget(mywid)

class MenuLateral(RelativeLayout):
    def __init__(self, **kwargs):
        super(MenuLateral, self).__init__(**kwargs)
        self.parent_height = Window.height - dp(79)
        self.add_widget(Image(source = color + "16.png",keep_ratio = False, allow_stretch = True))
        pariente = GridLayout(y = dp(-79),cols = 1, spacing = 0)
        self.index_data = []
        text = ["My Shop","My Vehicles","My Personal Resources"]
        text1 = ["About us","Contact us","Schedule\nAppointment","Find my shop"]
        for i in range(3):
            widget_parent = GridLayout(cols = 1, size_hint_y = None, height = dp(45))
            widget_parent.add_widget(Button(markup = True,font_size = '16sp',text = C4+text[i],background_normal = color + "5.png",background_down = color + "5.png",on_release = lambda x: self.openmenu(x.parent.children[0]),size_hint_y = None,  height = dp(45)))
            sub_parent = GridLayout(opacity = 0.,cols = 1)


            sub_parent.add_widget(CleanButton("ic_people_black_36px",text1[0]))
            sub_parent.add_widget(CleanButton("ic_schedule_black_36px",text1[1]))
            sub_parent.add_widget(CleanButton("ic_find_in_page_black_36px",text1[2]))
            sub_parent.add_widget(CleanButton("ic_contact_mail_black_36px",text1[3]))
            widget_parent.add_widget(sub_parent)
            
            pariente.add_widget(widget_parent)
            self.index_data.append(widget_parent.children[0])
            
        
        self.add_widget(pariente)
            
    def openmenu(self,x):
        if x.opacity == 0:
            animate_x = Animation(opacity = 1,height = self.parent_height-dp(135), d = .5, t = 'in_quart')
            animate_x1 = Animation(height = self.parent_height-dp(90), d = .275, t = 'in_quart')
            animate_x.start(x)
            animate_x1.start(x.parent)
        else:
            animate_x = Animation(opacity = .0, d = .225)
            animate_x2 = Animation(height = dp(45), d = .275, t = 'out_quart')
            animate_x1 = Animation(height = dp(45), d = .275, t = 'out_quart')
            animate_x.start(x)
            animate_x2.start(x)
            animate_x1.start(x.parent)
        for i in self.index_data:
            if i == x:pass
            else:
                animate_x = Animation(opacity = .0, d = .225)
                animate_x2 = Animation(height = dp(45), d = .275, t = 'out_quart')
                animate_x1 = Animation(height = dp(45), d = .275, t = 'out_quart')
                animate_x.start(i)
                animate_x2.start(i)
                animate_x1.start(i.parent)
            
        
        

    


class MyApp(App):
    def build(self):
        return MenuLateral()
 

if __name__ in ('__main__', '__android__'):
    MyApp().run()

    
    
    
    
    