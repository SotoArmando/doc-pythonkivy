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
from utils import CustTextInput

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

class CrearUsuario(RelativeLayout):
    def __init__(self, **kwargs):
        super(CrearUsuario, self).__init__(**kwargs)
        pariente = GridLayout(cols = 1,opacity = 1)
        pw = CustTextInput("Contraseña","***","***")
        cpw = CustTextInput("Confimar Contraseña","***","***")
        pw.selfTextInput().password = True
        cpw.selfTextInput().password = True
        dim = GridLayout(rows = 1,size_hint_y = None, height = '55dp')
        dim.add_widget(Button(background_normal = color +'16.png',background_down = color +'16.png',markup = True,font_name = font + 'Roboto-Regular.ttf', text = C4+'Siguiente',on_release = lambda x: self.nextscreen(), font_size = '16sp'))
        dim.add_widget(Image(size_hint_x = None, width = dp(1), keep_ratio = False, allow_stretch = True, source = color+'3.png', opacity = .14))
        dim.add_widget(Button(background_normal = '10.png',markup = True,font_name = font + 'Roboto-Regular.ttf', text = C4+'Cancelar', font_size = '16sp'))
        self.screenmanager = ScreenManager(size_hint_y = None, height = dp(71*3))
        screen1 = Screen(name = '1'); self.screenmanager.add_widget(screen1)
        screen2 = Screen(name = '2'); self.screenmanager.add_widget(screen2)
        screen1_parent = GridLayout(cols = 1); screen1.add_widget(screen1_parent)
        screen2_parent = GridLayout(cols = 1); screen2.add_widget(screen2_parent)
        
        pariente.add_widget(Label(size_hint_y = None, height = dp(71)))
        pariente.add_widget(Label(text = "Creacion de Usuario",text_size = (Window.width - 50 , dp(50)),valign = 'middle', halign = 'left',size_hint_y = None , height = '50dp', markup = True, font_size = '24sp'))
        pariente.add_widget(Image(size_hint_y = None, height = dp(1), keep_ratio = False, allow_stretch = True, source = color+'3.png', opacity = .14))
        pariente.add_widget(self.screenmanager)
        
        screen1_parent.add_widget(CustTextInput("Nombre Completo","Nombre Completo","Nombre Completo"))
        screen1_parent.add_widget(CustTextInput("E-Mail","E-Mail","@mail.com"))
        screen1_parent.add_widget(CustTextInput("Fecha de Nacimiento","dd/mm/yyyy","dd/mm/yyyy"))
        screen2_parent.add_widget(CustTextInput("Usuario","Usuario","User001"))
        screen2_parent.add_widget(pw)
        screen2_parent.add_widget(cpw)
        
        
        pariente.add_widget(Image(source = color + '16.png', keep_ratio= False, allow_stretch = True,size_hint_y = None, height = '15dp'))
        pariente.add_widget(dim)
        pariente.add_widget(Label(text_size = (Window.width, None),halign = 'center', valign = 'middle',text = "Ya tienes una cuenta?\n[b]Inicia Sesión", markup = True))
        
        
        self.add_widget(Image(source = color + '10.png', keep_ratio= False, allow_stretch = True))
        self.add_widget(pariente)

    def nextscreen(self):self.screenmanager.current = self.screenmanager.next()
        
class MyApp(App):
    def build(self):
        return CrearUsuario()
 

if __name__ in ('__main__', '__android__'):
    MyApp().run()

    
    
    
    
    