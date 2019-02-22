#!/usr/bin/env python
# -*- coding: utf-8 -*-
from kivy.config import Config
Config.set('graphics','borderless', 1)
Config.set('graphics','position','custom')
Config.set('graphics','window_state','visible')
Config.set('graphics','resizable',0)
Config.set('graphics','left',1000)
Config.set('graphics','top',35)
import kivy
from kivy.app import App
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.button import Button
import os
import os.path
import sys
import threading
import time
from threading import *
from threading import Timer
import datetime
import pytz
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
from kivy.uix.pagelayout import PageLayout
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
from kivy.clock import Clock
#CARPETAS DEL PROYECTO
patch = os.path.dirname(os.path.abspath(__file__))
asset = patch + '/assets/drawable-mdpi/'
color = patch + '/colors/'
font = patch + '/fonts/'
from random import randint

#VARIABLES GLOBALES
Hola = "Hola a todos"
Window.size = (360,640)

class Brick(RelativeLayout):
    def __init__(self, **kwargs):
        super(Brick, self).__init__(**kwargs)
        self.peso = 20
        self.color = kwargs["color"]
        self.add_widget(Image(source = color  + kwargs["color"]+ ".png", keep_ratio = False , allow_stretch = True))
        self.size_hint = (.1,None)
        self.height = Window.width * 0.1
        self.y = Window.height - self.height
        if kwargs["column"] > 4:
            self.column = kwargs["column"] % 10
            print self.column
        else:
            self.column = kwargs["column"]
        
        self.x = self.height * self.column
        self.pariente_x = None
        
class Figura(GridLayout):
    def __init__(self, **kwargs):
        super(Figura, self).__init__(**kwargs)
        self.cols = 3
        self.rows = 3
        self.color = "Hola"
        self.size_hint = (.3,None)
        self.height = Window.width * 0.3
        self.add_widget(Brick(color = 'None',column = 0))
        self.add_widget(Brick(color = 'None',column = 0))
        self.add_widget(Brick(color = 'None',column = 0))
        self.add_widget(Brick(color = '5',column = 0))
        self.add_widget(Brick(color = '5',column = 0))
        self.add_widget(Brick(color = '5',column = 0))
        self.add_widget(Brick(color = 'None',column = 0))
        self.add_widget(Brick(color = 'None',column = 0))
        self.add_widget(Brick(color = '5',column = 0))
        if kwargs["column"] > 7:
            self.column = kwargs["column"] % 7
            print self.column
        else:
            self.column = kwargs["column"]
        self.y = Window.height - self.height
        self.pixeles = []
        for a in range(1):
            self.pixeles.append([])
            for b in range(1):
                base = a * 3
                base = base + b
                self.pixeles[a].append(self.children[base])
            
            self.pixeles[a] = self.pixeles[a][::-1]
        self.pixeles = self.pixeles[::-1]
        self.x = (Window.width * 0.1) * self.column
        print "self.pixeles",self.pixeles
class Brick2(RelativeLayout):
    def __init__(self, **kwargs):
        super(Brick2, self).__init__(**kwargs)
        self.peso = 20
        self.add_widget(Image(source = color + "None.png", keep_ratio = False , allow_stretch = True))
        self.size_hint = (.1,None)
        self.height = Window.width * 0.1 
        self.color = "3"
        if kwargs["column"] > 9:
            self.column = kwargs["column"] % 10
            print self.column
        else:
            self.column = kwargs["column"]
        self.x = self.height * (self.column)         
        
class InterfaceManager(RelativeLayout):#COMPLEMENTO 'PARENT' EL PROYECTO
    def __init__(self, **kwargs):
        super(InterfaceManager, self).__init__(**kwargs)
        cuadrados = 10
        self.figurassize = Window.width / cuadrados
        self.casillas = []
        self.lineas_posibles = Window.height / self.figurassize
        self.pariente = RelativeLayout()
        
        #self.pariente.add_widget(Brick(color = '6',x = four))
        #self.pariente.add_widget(Brick(color = '7',x = four * 2))
        #self.pariente.add_widget(Brick(color = '8',x = four * 3))
        #self.pariente.add_widget(Brick(color = '9',x = four * 4))
        self.add_widget(self.pariente)
        for i in range(cuadrados):#(Window.width * 0.1)*-1
            x = Brick2(y = 0, column = i, color = '5')
            self.pariente.add_widget(x)
            self.casillas.append([x])
        Clock.schedule_interval(self.get_others, 1.0/60.0)
        self.pariente.add_widget(Figura(color = '5',column = 3))
        
    def funcion(self):
        print("hola")
        
        
        
    def get_others(self,*args):
        elementos = []
        try:
            i = self.pariente.children[0]
            x = []
            y = []
            x1 = i.column
            
            for m in range(3):
                if i.pixeles[2][m] == 'None':
                    x.append(0)
                else:
                    x.append(1)
                
                if self.casillas[x1 + m -1][-1].color == 'None':
                    y.append(0)
                else:
                    y.append(1)
            for i in self.casillas:
                print i
            c = 0
            print x,y
            for i in range(3):
                if x[i] != y[i]:
                    c += 1
           
            if c == 3:  
                print "ES 3"
                if i.y > self.casillas[i.column][-1].y + 0: 
                    if (i.y - (self.casillas[i.column][-1].y + 0)) <= 5:
                        i.y -= (i.y - (self.casillas[i.column][-1].y + 0))
                    else:
                        i.y -= 5
                else:
                    print "hola"
                    a = Animation(opacity = 1, d = .5, t = 'out_quad')
                    
                    brick = Figura(opacity = 0,color = str(randint(1, 16)),column = self.pariente.children[0].column + 1)
                    self.pariente.add_widget(brick)
                    a.start(brick)
                    
                    if str(type(i)) == "<class '__main__.Figura'>":
                        for line in i.pixeles:
                            for element in line:
                                if element.color == "None":
                                    pass
                                else:
                                    print element.color , "AGREGADO"
                                    self.casillas[i.column + line.index(element)].append(i)
                                #print element.color
                                
                    elif str(type(i)) == "<class '__main__.Brick'>":
                        self.casillas[i.column].append(i)
            else:
                i = self.pariente.children[0]
                if i.y > self.casillas[i.column][-1].y + self.casillas[i.column][-1].width: 
                    if (i.y - (self.casillas[i.column][-1].y + self.casillas[i.column][-1].width)) <= 5:
                        i.y -= (i.y - (self.casillas[i.column][-1].y + self.casillas[i.column][-1].width))
                    else:
                        i.y -= 5
                else:
                    print "hola"
                    a = Animation(opacity = 1, d = .5, t = 'out_quad')
                    
                    brick = Figura(opacity = 0,color = str(randint(1, 16)),column = self.pariente.children[0].column + 1)
                    self.pariente.add_widget(brick)
                    a.start(brick)
                    
                    if str(type(i)) == "<class '__main__.Figura'>":
                        for line in i.pixeles:
                            for element in line:
                                if element.color == "None":
                                    pass
                                else:
                                    print element.color , "AGREGADO"
                                    self.casillas[i.column + line.index(element)].append(i)
                                #print element.color
                                
                    elif str(type(i)) == "<class '__main__.Brick'>":
                        self.casillas[i.column].append(i)
            
  
                
                    
                
                        
                    

                
                
        except:
            import traceback
            traceback.print_exc()
			
class MyApp(App):
    def build(self):
        return InterfaceManager()
 

if __name__ in ('__main__', '__android__'):
    MyApp().run()

    
    
    
    
    