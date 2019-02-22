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
        
class Configuracion(RelativeLayout):
    def __init__(self, **kwargs):
        super(Configuracion, self).__init__(**kwargs)
        manager_parent = RelativeLayout(y = -71)
        self.manager = ScreenManager()
        screen0 = Screen(name = 'conf0'); self.manager.add_widget(screen0)
        screen1 = Screen(name = 'conf1'); self.manager.add_widget(screen1)
        
        screen0_pariente = GridLayout(cols = 1)
        screen0.add_widget(screen0_pariente)
        screen0_pariente.add_widget(Label(markup = True,text = C4+"[b]Configuracion", text_size = (Window.width - dp(50), dp(46)), size_hint_y = None, height = dp(46),font_size = '16sp', valign = 'middle', halign = 'left'))
        screen0_pariente.add_widget(Button(on_release = lambda x: self.next(),background_normal = color + "16.png",background_down = color + "16b.png",markup = True,text = C4+"Cambiar Contraseña", text_size = (Window.width - dp(50), dp(46)), size_hint_y = None, height = dp(46),font_size = '14sp', valign = 'middle', halign = 'left'))
        
        screen1_pariente = GridLayout(cols = 1)
        screen1.add_widget(screen1_pariente)
        screen1_pariente.add_widget(Label(markup = True,text = C4+"[b]Cambiar Contraseña", text_size = (Window.width - dp(50), dp(46)), size_hint_y = None, height = dp(46),font_size = '16sp', valign = 'middle', halign = 'left'))
        self.text0 = TextInput(padding = [dp(25),dp(10),0,0],hint_text = "Contraseña Actual" ,on_release = lambda x: self.next(),background_normal = color + "16.png",background_down = color + "16b.png",markup = True, text_size = (Window.width - dp(50), dp(46)), size_hint_y = None, height = dp(46),font_size = '14sp', valign = 'middle', halign = 'left')
        self.text1 = TextInput(padding = [dp(25),dp(10),0,0],hint_text = "Confirme Actual" ,on_release = lambda x: self.next(),background_normal = color + "16.png",background_down = color + "16b.png",markup = True, text_size = (Window.width - dp(50), dp(46)), size_hint_y = None, height = dp(46),font_size = '14sp', valign = 'middle', halign = 'left')
        self.text2 = TextInput(padding = [dp(25),dp(10),0,0],hint_text = "Nueva Contraseña" ,on_release = lambda x: self.next(),background_normal = color + "16.png",background_down = color + "16b.png",markup = True, text_size = (Window.width - dp(50), dp(46)), size_hint_y = None, height = dp(46),font_size = '14sp', valign = 'middle', halign = 'left')
        screen1_pariente.add_widget(self.text0)
        screen1_pariente.add_widget(self.text1)
        screen1_pariente.add_widget(self.text2)
        self.button0 = Button(on_release = lambda x: self.next(),background_normal = color + "16.png",background_down = color + "16b.png",markup = True,text = C4+"Aceptar", text_size = (Window.width - dp(50), dp(46)), size_hint_y = None, height = dp(46),font_size = '14sp', valign = 'middle', halign = 'left')
        screen1_pariente.add_widget(self.button0)
        
        
        manager_parent.add_widget(self.manager)
        self.add_widget(manager_parent)
    def next(self): self.manager.current = self.manager.next()
    def previous(self): self.manager.current = self.manager.previous()
class MyApp(App):
    def build(self):
        return Configuracion()
 

if __name__ in ('__main__', '__android__'):
    MyApp().run()

    
    
    
    
    