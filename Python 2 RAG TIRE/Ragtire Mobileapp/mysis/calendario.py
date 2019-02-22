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
        
class Calendar(RelativeLayout):
    def __init__(self, **kwargs):
        super(Calendar, self).__init__(**kwargs)
        self.size_hint_y = None
        self.height = dp(56)
        self.add_widget(Image(source = color + "16.png", keep_ratio = False ,allow_stretch = True))
        pariente0 = GridLayout(cols = 1, padding = [dp(25),0,dp(25),0], opacity = 0)
        anim_parent = GridLayout(cols = 1, size_hint_y = None, height = dp(56))
        anim_parent.add_widget(Button(on_release = lambda x: self.open(x),markup = True, text = C4+"[b]Calendario",font_size = dp(18), background_normal = color + '16.png', background_down = color + '16.png',valign = 'middle',text_size = (Window.width - dp(25),dp(56)), size_hint_y = None, height = dp(56)))
        anim_parent.add_widget(pariente0)
        
        
        self.date0 = (0,0)
        self.date1 = (0,0)
        
        pariente = ScreenManager()
        self.meses = ['Enero','Febrero','Marzo','Abril','Mayo','Junio','Julio','Agosto','Septiembre','Octubre','Noviembre','Diciembre']
        self.day = 1
        self.month = 1
        def seleccionar_dia(string): 
            self.day = string[len(C4):]
            print self.day
        def seleccionar_mes(): 
            self.month = self.meses.index(pariente.current) + 1
            print self.month
        def pariente_next(): 
            pariente.transition.direction = 'left'
            self.mes_actual.text = C4 + pariente.next()
            pariente.current = pariente.next()
            seleccionar_mes()
        def pariente_back(): 
            pariente.transition.direction = 'right'
            self.mes_actual.text = C4 + pariente.previous()
            pariente.current = pariente.previous()
            seleccionar_mes()

            
        for i in range(12):
            mes = Screen(name = self.meses[i])
            mes_pariente = GridLayout(cols = 7)
            days = ['D','L','M','MC','J','V','S']
            for day in days: mes_pariente.add_widget(Label(opacity = .44,text = C4+day,markup = True ))
            for i in range(6): mes_pariente.add_widget(Label())
            for i in range(31): 
                mes_pariente.add_widget(ToggleButton(on_release = lambda x: seleccionar_dia(x.text),background_normal = color + '16.png', background_down = color+'16b.png',group = "Dia del mes",text = C4+str(i+1),markup = True))
            
            
            mes.add_widget(mes_pariente)
            pariente.add_widget(mes)
        dim = GridLayout(rows = 1, size_hint_y = None, height = '46dp')
        dim.add_widget(Label())
        dim.add_widget(Button(background_normal = color + "16.png",background_down = color + "7.png",text = C4+"OK",size_hint_x = None, width=  dp(100), markup = True))
        dim.add_widget(Button(background_normal = color + "16.png",background_down = color + "7.png",text = C4+"Cancel",size_hint_x = None, width=  dp(100), markup = True))
        dim0 = GridLayout(rows = 1, size_hint_y = None, height = '35dp')
        dim0.add_widget(Button(on_release = lambda x: pariente_back(),background_normal = color + "16.png",background_down = color + "16.png",text = C4+"[b]<",halign = 'left', valign = 'middle',text_size = (Window.width/3 -dp(50),dp(35)),font_size = dp(20),markup = True))
        self.mes_actual = Label(text =C4+"Enero",markup = True)
        dim0.add_widget(self.mes_actual)
        dim0.add_widget(Button(on_release = lambda x: pariente_next(),halign = 'right', valign = 'middle',text_size = (Window.width/3 -dp(50),dp(35)),background_normal = color + "16.png",background_down = color + "16.png",text = C4+"[b]>",font_size = dp(20),markup = True))
        
        dim1 = GridLayout(rows =1 , size_hint_y = None, height = '46dp')
        self.espace0 = Button(background_normal = color + '16.png',background_down = color + '16b.png',on_release = lambda x: self.setdate(x, b = 0),text = '', markup = True)
        self.espace1 = Button(background_normal = color + '16.png',background_down = color + '16b.png',on_release = lambda x: self.setdate(x, b = 1),text = '', markup = True)
        dim1.add_widget(self.espace0)
        dim1.add_widget(self.espace1)
        self.canc = Button(on_release = lambda x: self.afterset(),opacity = 0,size_hint_x = None, width = 0,background_normal = color + '16.png',background_down = color + '16b.png',text = C4+'Cancelar', markup = True)
        self.conf = Button(on_release = lambda x: self.afterset(),opacity = 0,size_hint_x = None, width = 0,background_normal = color + '16.png',background_down = color + '16b.png',text = C4+'Confirmar', markup = True)
        dim1.add_widget(self.conf)
        dim1.add_widget(self.canc)
        pariente0.add_widget(dim0)
        pariente0.add_widget(pariente)
        #pariente0.add_widget(dim)
        pariente0.add_widget(dim1)
        
        self.add_widget(anim_parent)
    def open(self,wid):
        parent = wid.parent
        if wid.parent.height == dp(56):
            animat = Animation(height = dp(406), d = .5 , t = 'out_expo')
            animat1 = Animation(opacity = 1 , d = .5 , t = 'out_expo')
            animat.start(self)
            animat.start(parent)
            animat1.start(parent.children[0])
        elif wid.parent.height == dp(406):
            animat = Animation(height = dp(56), d = .5 , t = 'out_expo')
            animat1 = Animation(opacity = 0 , d = .5 , t = 'out_expo')
            animat.start(self)
            animat.start(parent)
            animat1.start(parent.children[0])
        
    def setdate(self,wid,**kwargs):
        wid.text = C4+ str(self.day)+ ' de ' + self.meses[self.month-1] 
        if kwargs['b'] == 0:self.date0 = (self.month,int(self.day))
        if kwargs['b'] == 1:self.date1 = (self.month,int(self.day))
        print self.date0 , self.date1
        if (self.date0 != (0,0)) and (self.date1 != (0,0)):
            animation = Animation(opacity = 1,width = Window.width/2 -  dp(25), d = .5 , t = 'out_expo')
            animation1 = Animation(opacity = 0 , d = .5 , t = 'out_expo')
            animation.start(self.conf)
            animation.start(self.canc)
            animation1.start(self.espace0)
            animation1.start(self.espace1)
    def afterset(self):
        animation = Animation(opacity = 0,width = 0 -  dp(25), d = .5 , t = 'out_expo')
        animation1 = Animation(opacity = 1 , d = .5 , t = 'out_expo')
        animation.start(self.conf)
        animation.start(self.canc)
        animation1.start(self.espace0)
        animation1.start(self.espace1)
class MyApp(App):
    def build(self):
        return Calendar()
 

if __name__ in ('__main__', '__android__'):
    MyApp().run()

    
    
    
    
    