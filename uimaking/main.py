#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import os.path
import sys
import threading
import time
from threading import *
from threading import Timer

import kivy
from kivy.uix.carousel import Carousel
from kivy.uix.effectwidget import EffectWidget
from kivy.uix.effectwidget import HorizontalBlurEffect,VerticalBlurEffect
from kivy.adapters.listadapter import ListAdapter
from kivy.adapters.models import SelectableDataItem
from kivy.adapters.simplelistadapter import SimpleListAdapter
from kivy.animation import Animation
from kivy.app import App
from kivy.base import runTouchApp
from kivy.clock import Clock, mainthread
from kivy.core.window import Window
from kivy.effects.opacityscroll import OpacityScrollEffect
from kivy.effects.scroll import ScrollEffect
from kivy.graphics import *
from kivy.graphics.instructions import InstructionGroup
from kivy.metrics import MetricsBase, dp,sp
from kivy.parser import parse_color
from kivy.properties import (BooleanProperty, ListProperty, NumericProperty,
                             ObjectProperty, OptionProperty, StringProperty)
from kivy.resources import resource_add_path
from kivy.uix.accordion import Accordion, AccordionItem
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.bubble import Bubble
from kivy.uix.button import Button
from kivy.uix.checkbox import CheckBox
from kivy.uix.dropdown import DropDown
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import AsyncImage, Image
from kivy.uix.label import Label
from kivy.uix.listview import (CompositeListItem, ListItemButton,
                               ListItemLabel, ListView)
from kivy.uix.popup import Popup
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.scatter import Scatter
from kivy.uix.screenmanager import (FadeTransition, FallOutTransition,
                                    NoTransition, RiseInTransition, Screen,
                                    ScreenManager, SlideTransition,
                                    SwapTransition, WipeTransition)
from kivy.uix.scrollview import ScrollView
from kivy.uix.stencilview import StencilView
from kivy.uix.textinput import TextInput
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.widget import Widget
from kivy.utils import get_color_from_hex, get_hex_from_color, platform
from kivy.core.audio import SoundLoader,Sound

from utils import NavigationDrawer
from time import gmtime, strftime




patch = os.path.dirname(os.path.abspath(__file__))
asset = patch + '/assets/drawable-mdpi/'
color = patch + '/colors/'
font = patch + '/fonts/'


Hola = "Hola a todos"

Window.clearcolor = (1,1,1,1)
 
Window.size = (360,640)
C1 = "[color=#13C0C7]"
C2 = "[color=#404040]"
C3 = "[color=#ff3333]"
C4 = "[color=#000000]"
def globaly(size):
    x = Window.height - dp(size)
    return x
def padding(size):
    x = Window.width - (dp(size)*2)
    return x
class ImageButton(ButtonBehavior, Image): pass
class InterfaceManager(RelativeLayout):#COMPLEMENTO 'PARENT' EL PROYECTO
    def __init__(self, **kwargs):
        super(InterfaceManager, self).__init__(**kwargs)
        self.state3 = -1
        self.main = ScreenManager();self.add_widget(self.main)
        self.main_screen = Screen();self.main.add_widget(self.main_screen)
        
        self.screenparent = RelativeLayout();self.main_screen.add_widget(self.screenparent)
        self.parent_child = GridLayout(cols = 1);self.screenparent.add_widget(self.parent_child)
        
        bluetitle = FloatLayout(rows = 1,size_hint = (1,None), height = '144dp', size_hint_x = None , width = dp(432))
        bluetitle.add_widget(Button(background_normal = asset + "Repeat Grid 7.png" ,y = globaly(dp(135)),x = dp(-360)))
        bluetitle.add_widget(Button(background_normal = asset + "Repeat Grid 7.png" ,y = globaly(dp(135)),x = dp(360)))
        bluetitle.add_widget(Button(background_normal = asset + "Repeat Grid 7.png" ,y = globaly(dp(135)) ))
        bluetitle.add_widget(Button(halign = 'center',text_size = (padding(50), dp(60)),font_size = '24sp',background_normal = color + "None.png",background_down = color + "None.png",font_name = font + "Millennial Solstice.ttf",text = "Codi", width = Window.width,  y = globaly(dp(120)),size_hint_y = None, height = dp(120)))   
        bluetitle.add_widget(Image(pos_hint = {'center_x':.9 },y = globaly(dp(100)),size_hint = (None,None), size = ('70dp','66dp'), source = asset + 'chef.png'))   
        bluetitle.add_widget(Button(pos_hint = {'x': 0. },y = globaly(dp(95)),size_hint = (None,None), size = ('50dp','50dp'), background_normal = asset + 'Group 61.png', background_down = asset + 'Group 61.png'))   
        
        b_parentsearcherparent = RelativeLayout(opacity = 0.,size_hint_y = None, height = 0)
        b_parentsearcherparent_dim1 = GridLayout(rows = 1, pos = (0,-20))
        b_parentsearcherparent_dim1.add_widget(Label(size_hint_x = None , width = '25dp'))
        b_parentsearcherparent_dim1.add_widget(Image(size_hint_x = None , width = '47dp' , source = asset+"ic_search_white.png"))
        b_parentsearcherparent_dim1.add_widget(TextInput(hint_text = "buscas una receta?",cursor_color = (0,0,0,.5),font_name = font + "Roboto-Regular.ttf",padding = [dp(20),dp(40),0,0],multiline = False,font_size = '16dp',  background_normal = color + "None.png", background_active = color + "None.png"))
        #b_parentsearcherparent_dim1.add_widget(Image(size_hint_x = None , width = '1dp' ,keep_ratio = False, allow_stretch = True, source = color+"17b.png"))
        b_parentsearcherparent_dim1.add_widget(Label(size_hint_x = None , width = '25dp'))
        b_parentsearcherparent.add_widget(b_parentsearcherparent_dim1)
        
        screen_scroll = ScrollView()
        self.screenparent.add_widget(screen_scroll)
        self.screenparent.add_widget(bluetitle)
        
        scrollparent = GridLayout(cols = 1, size_hint_y = None, height = dp(1500))
        screen_scroll.add_widget(scrollparent)
        def objeto():
            x = GridLayout(cols = 1, size_hint_y = None , height = '321dp')
            dim = GridLayout(rows = 1, size_hint_y = None , height = '79dp')
            dim.add_widget(Button(line_height = 1.25,halign = 'left', valign = 'middle',text_size = ((Window.width-dp(75)) - dp(54),dp(79)),font_name = font + 'Roboto-Medium.ttf',font_size = '20sp',size_hint_y = None, height = '79dp', text = C4+'Filtro[i]\n[font='+font+'Roboto-Regular.ttf'+'][size=16sp]    Descripcion',background_normal = color + "16.png",markup = True))
            dim.add_widget(Image(source = asset+"Path 102.png", keep_ratio = True , allow_stretch = False, size_hint_x = None , width = '75dp'))
            x.add_widget(dim)
            
            dim2 = RelativeLayout(size_hint_y = None , height= '205dp')
            dim2.add_widget(Button(y = dp(34),size_hint_y = None , height = '171dp',background_normal = asset + 'Repeat Grid 12.png'))
            x.add_widget(dim2)
            
            dim1 = GridLayout(rows = 1, size_hint_y = None , height = '50dp', y = 0)
            dim1.add_widget(Label())
            dim1.add_widget(Button(background_normal = asset+"Group 64.png" , size_hint_x = None , width = '50dp'))
            dim1.add_widget(Button(background_normal = asset+"Group 65.png" , size_hint_x = None , width = '50dp'))
            dim1.add_widget(Button(background_normal = asset+"Group 63.png" , size_hint_x = None , width = '50dp'))
            dim1.add_widget(Label())
            dim2.add_widget(dim1)
            
            
            #x.add_widget(Image(source = color + "16.png", size_hint_y = None , height = dp(50) , keep_ratio = False, allow_stretch = True))
            return x
        scrollparent.add_widget(Button(size_hint_y = None, height = dp(125), background_normal = color + "16.png"))
        
        def saludar(): 
            if b_parentsearcherparent.opacity == 1.:
                x_anim2 = Animation(height = dp(0), d = .15)
                x_anim1 = Animation(opacity = 0., d = .5)
                x_anim = x_anim2 + x_anim1 
            else:
                x_anim2 = Animation(height = dp(100), d = .15)
                x_anim1 = Animation(opacity = 1., d = .5)
                x_anim = x_anim2 + x_anim1
            if (screen_scroll.scroll_y > 1.1) and (self.state3 == -1): 
                self.state3 *= -1
                def desactivar(): self.state3 *= -1;print self.state3
                x_anim.bind(on_complete = lambda x,y:desactivar())
                x_anim.start(b_parentsearcherparent)
        
        screen_scroll.bind(on_scroll_stop = lambda x,y: saludar())
        scrollparent.add_widget(b_parentsearcherparent)
        scrollparent.add_widget(Image(size_hint_y = None, height = dp(1), source = color+"16bb.png", keep_ratio = False, allow_stretch = True))
        scrollparent.add_widget(objeto())
        scrollparent.add_widget(objeto())
        scrollparent.add_widget(objeto())

    def funcion(self):
        print("hola")

class MyApp(App):
    def build(self):
        return InterfaceManager()
 

if __name__ in ('__main__', '__android__'):
    MyApp().run()

    
    
    
    
    