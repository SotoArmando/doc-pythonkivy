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
class Shopitem(RelativeLayout):
    def __init__(self, **kwargs):
        super(Shopitem, self).__init__(**kwargs)
        self.size_hint_y  = None
        self.height = dp(256)
        self.add_widget(Image(source = color + "16.png",keep_ratio = False, allow_stretch = True))
        
        pariente = GridLayout(cols = 1)
        pariente.add_widget(Image(source = color + '5.png', size_hint_y = None, height = dp(124)))
        pariente.add_widget(Button(markup = True,text = C4+"[b]Articulo\nGigante[/b][size=13sp]\nBueno para la casa[/size]\n\n[b]500 RD$\nDisponible[/b]\n5.0 Estrellas", background_normal = color + 'None.png'))
        
        self.add_widget(pariente)
class Shopitem1(RelativeLayout):
    def __init__(self, **kwargs):
        super(Shopitem1, self).__init__(**kwargs)
        self.size_hint_y  = None
        self.height = dp(156)
        self.add_widget(Image(source = color + "16.png",keep_ratio = False, allow_stretch = True))
        
        pariente = GridLayout(rows = 1)
        pariente.add_widget(Image(source = color + '5.png'))
        pariente.add_widget(Button(markup = True,text = C4+"[b]Articulo\nGigante[/b][size=13sp]\nBueno para la casa[/size]\n\n[b]500 RD$\nDisponible[/b]\n5.0 Estrellas", background_normal = color + 'None.png'))
        
        self.add_widget(pariente)
        
class Shop(Screen):
    def __init__(self, **kwargs):
        super(Shop, self).__init__(**kwargs)
        self.parent_height = Window.height - dp(79)
        self.add_widget(Image(source = color + "16.png",keep_ratio = False, allow_stretch = True))
        pariente_root = RelativeLayout(size_hint_y = None, height = dp(2000))
        pariente_root.add_widget(Image(opacity = .14,y = dp(-56),source = color + "2.png",keep_ratio = False, allow_stretch = True))
        pariente = GridLayout(cols = 1, spacing = 1)
        
        
        
        pariente_scroll = ScrollView( size_hint_y = None , height = self.parent_height)
        pariente_sortgrid = GridLayout(rows = 1, size_hint_y = None, height = dp(56))
        pariente_sortgrid.add_widget(Button(background_normal = color + "16.png"))
        pariente_sortgrid.add_widget(ImageButton(on_release = lambda x: self.setview(1),source = asset + "ic_view_module_black_24px.png",size_hint_x = None, width = dp(56)))
        pariente_sortgrid.add_widget(ImageButton(on_release = lambda x: self.setview(2),source = asset + "ic_view_list_black_24px.png",size_hint_x = None, width = dp(56)))
        pariente.add_widget(pariente_sortgrid)
        self.items_parent = GridLayout(cols = 2, spacing = 1)
        self.setview(2)
        pariente.add_widget(self.items_parent)

        
        pariente_root.add_widget(pariente)
        pariente_scroll.add_widget(pariente_root)
        self.add_widget(pariente_scroll)
        

    def setview(self,view):
        try:
            self.items_parent.clear_widgets()
        except:
            pass
        if view == 1:
            self.items_parent.cols = 2
            self.items_parent.add_widget(Shopitem())
            self.items_parent.add_widget(Shopitem())
            self.items_parent.add_widget(Shopitem())
            self.items_parent.add_widget(Shopitem())
            self.items_parent.add_widget(Shopitem())
            self.items_parent.add_widget(Shopitem())
        elif view == 2:
            self.items_parent.cols = 1
            self.items_parent.add_widget(Shopitem1())
            self.items_parent.add_widget(Shopitem1())
            self.items_parent.add_widget(Shopitem1())
            self.items_parent.add_widget(Shopitem1())
            self.items_parent.add_widget(Shopitem1())
            self.items_parent.add_widget(Shopitem1())

    


class MyApp(App):
    def build(self):
        return Shop()
 

if __name__ in ('__main__', '__android__'):
    MyApp().run()

    
    
    
    
    