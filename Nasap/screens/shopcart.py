#!/usr/bin/env python
# -*- coding: latin-1 -*-

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
class CartItem(GridLayout):
    def __init__(self, **kwargs):
        super(CartItem, self).__init__(**kwargs)
        self.size_hint_y = None
        self.height = dp(156)
        self.cols = 1
        
        pariente = GridLayout(cols = 3,padding = [0,dp(18),0,0])
        CartItem_img = Image(size_hint_x = None, width = dp(124),source = color + '5.png')
        CartItem_desc_Descripcion = Button(markup = True,background_normal = color + "16.png",text = C4+"Articulo\n\nArticulo perfecto\npara el hogar\n\n500.00 RD$")
        CartItem_desc2_cuanty = RelativeLayout(size_hint_x = None, width = dp(64))
        CartItem_desc2_cuanty.add_widget(Button(size_hint = (None,None),background_normal = color + "10.png", size = (dp(50),dp(50)),markup = True, text = C4 + "0", pos_hint = {'center_x':.5,'center_y':.5}))
        pariente.add_widget(CartItem_img)
        pariente.add_widget(CartItem_desc_Descripcion)
        pariente.add_widget(CartItem_desc2_cuanty)
        self.add_widget(pariente)
        
        parienteb = GridLayout(rows = 1 , size_hint_y = None, height = '35dp')
        parienteb.add_widget(Label())
        parienteb.add_widget(MyButton(markup = True,background_normal = color + "16.png",text = C4+'   Remover',font_size = '13sp'))
        parienteb.add_widget(MyButton(markup = True,background_normal = color + "16.png",text = C4+'    Guardar   ',font_size = '13sp'))
        self.add_widget(parienteb)
        
        
        
        
        
        

class ShopCart(Screen):
    def __init__(self, **kwargs):
        super(ShopCart, self).__init__(**kwargs)
        self.parent_height = Window.height - dp(79)
        self.add_widget(Image(source = color + "16.png",keep_ratio = False, allow_stretch = True))
        pariente_scroll = ScrollView(size_hint_y = None, height = Window.height - dp(79))
        pariente = GridLayout(y = dp(0),cols = 1, spacing = 0, size_hint_y = None, height = dp(2000))
        pariente.add_widget(CartItem())
        pariente.add_widget(Image(opacity = .24,size_hint_y = None, height = 1 , source = color + "2.png", keep_ratio = False, allow_stretch = True))
        pariente.add_widget(CartItem())
        pariente.add_widget(Image(opacity = .24,size_hint_y = None, height = 1 , source = color + "2.png", keep_ratio = False, allow_stretch = True))
        pariente.add_widget(CartItem())
        pariente.add_widget(Image(opacity = .24,size_hint_y = None, height = 1 , source = color + "2.png", keep_ratio = False, allow_stretch = True))

        pariente_scroll.add_widget(pariente)
        self.add_widget(pariente_scroll)
        bottomtitles = GridLayout(size_hint_y = None, height = dp(56),cols = 3)
        bottomtitles.add_widget(Image(opacity = .24,size_hint_y = None, height = 1 , source = color + "2.png", keep_ratio = False, allow_stretch = True))
        bottomtitles.add_widget(Image(opacity = .24,size_hint_y = None, height = 1 , source = color + "2.png", keep_ratio = False, allow_stretch = True))
        bottomtitles.add_widget(Image(opacity = .24,size_hint_y = None, height = 1 , source = color + "2.png", keep_ratio = False, allow_stretch = True))       
        bottomtitles.add_widget(Button(markup = True,background_normal = color + "16.png",text = C4+'Total de\n10 Items',font_size = '13sp'))
        bottomtitles.add_widget(Button(markup = True,background_normal = color + "16.png",text = C4+'500,000 RD$',font_size = '13sp'))
        bottomtitles.add_widget(Button(markup = True,background_normal = color + "16.png",text = C4+'Confirmar',font_size = '16sp'))
        
        self.add_widget(bottomtitles)

        

    


class MyApp(App):
    def build(self):
        return ShopCart()
 

if __name__ in ('__main__', '__android__'):
    MyApp().run()

    
    
    
    
    