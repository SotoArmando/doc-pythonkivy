#!/usr/bin/env python
# -*- coding: utf-8 -*-


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

from time import gmtime, strftime

#CARPETAS DEL PROYECTO
patch = os.path.dirname(os.path.abspath(__file__))
asset = patch + '/assets/drawable-mdpi/'
color = patch + '/colors/'
font = patch + '/fonts/'

#VARIABLES GLOBALES
Hola = "Hola a todos"
Window.clearcolor = (0,0,0,1.)
Window.size = (360,640)

class Playscreen(Screen):
    def __init__(self, **kwargs):
        super(Playscreen, self).__init__(**kwargs)
        self.lives = 3
        self.score = Label(font_name = font + "ARCADECLASSIC.ttf",pos_hint = {'center_x':.5, 'center_y':.9},size_hint = (None,None),font_size = '24sp', size = (dp(250),dp(50)), text = "000000")
        self.score1 = Label(markup = True,pos_hint = {'center_x':.5, 'center_y':.84},size_hint = (None,None),font_size = '24sp', size = (dp(250),dp(50)), text = "[font="+font+"ARCADECLASSIC.ttf"+"]"+ "3 lives[/font]" )
        self.button0 = Image(size_hint = (None,None), size = (dp(50),dp(50)), y = Window.height - 100, x = Window.width - 100)
        self.button1 = Image(size_hint = (None,None), size = (dp(50),dp(50)), y = Window.height - 50, x = Window.width - 50)
        self.b = Button(pos_hint = {'center_y':.5,'center_x':.5},size_hint = (None,None), size = (dp(50),dp(50)))
        self.botones = [.225,.5,.775]
        
        self.add_widget(self.score)
        self.add_widget(self.score1)
        self.add_widget(self.b)
        self.add_widget(self.button0)
                
  
        
        
        self.points = 0
        self.moves = 1
        self.state = 1
        self.state1 = 1
        self.state2 = -1 #MOVERSE
        Clock.schedule_interval(self.update, 1.0/60.0)
        

       
    def on_touch_down(self, touch):
        if (self.state2 == 1) and (touch.y > 50):
            if touch.y >= Window.height/2:
                self.moves = (self.moves % 3)+1
            else:
                if (self.moves % 3) == 2:
                    self.moves = (self.moves % 3)-1
                else:
                    self.moves = (self.moves % 3)+2

            for i in range(3):
                if i == self.moves-1:
                    self.b.background_normal = color + "6.png"
                    self.b.background_disabled_normal = color + "6.png"
                    self.b.disabled = False
                    x_anim = Animation(pos_hint = {'center_y': self.botones[i]}, t = 'in_out_circ', d = .20)
                    x_anim.start(self.b)
            self.points += 1
            self.score.text = str(self.points)
        else:
            pass
    def pause(self):
        self.state2 *= -1
        
    def update(self,x):
        if self.state2 == 1: 
            if (self.button0.y <= 0) or (self.button0.y + dp(50) >= Window.height - self.button0.height):
                self.state *= -1 
            if (self.button0.x <= 0) or (self.button0.x + dp(50) >= Window.width):
                self.state1 *= -1 

            
     
            if self.b.collide_widget(self.button0):
                self.b.background_normal = color + "10.png"
                self.lives -= 1
                if str(self.lives)[0] == '-':
                    self.score1.text = str(self.lives)[0]+"[font="+font+"ARCADECLASSIC.ttf"+"]"+str(self.lives)[1:] + "lives[/font]" 
                else:
                    self.score1.text = "[font="+font+"ARCADECLASSIC.ttf"+"]"+str(self.lives) + "  lives[/font]"
                if self.b.disabled == True:
                    pass
                else:
                    self.state *= -1
                    self.state1 *= -1
            else:
                self.b.background_normal = color + "6.png"
        
                    

        
            self.button0.y -=  self.state*( 1  + (self.button0.y/25))
            self.button0.x +=  self.state1*( 1  + (self.button0.x/25))
            print self.button0.x


            
class InterfaceManager(RelativeLayout):#COMPLEMENTO 'PARENT' EL PROYECTO
    def __init__(self, **kwargs):
        
        super(InterfaceManager, self).__init__(**kwargs)
        #INTERFACE
        self.main = ScreenManager()
        self.button1 = Button(size_hint = (None,None), size = (dp(50),dp(50)), background_normal = asset + 'Group 9.png')
        self.button2 = Button(size_hint = (None,None), size = (dp(50),dp(50)),on_release = lambda x: self.pause(), x = Window.width - 50, background_normal = asset + "Group 2.png")
        self.add_widget(self.button1)
        self.add_widget(self.button2)
        self.screen2()
        self.screen1()
        self.add_widget(self.main)
        self.lives = 3
        self.points = 0
        self.moves = 1
        self.state = 1
        self.state1 = 1

        

            
        
    def pause(self):
        try:
            self.pausescreen.parent.remove_widget(self.pausescreen)
            self.screen1.pause()
        except:
            self.pausescreen = GridLayout(pos_hint = {'center_x':.5, 'center_y':.5},cols = 1,size_hint = (None,None), size = (dp(200),dp(300)))
            self.pausescreen.add_widget(Label())
            self.pausescreen.add_widget(Label(size_hint_y = None, height = dp(50), text = "PAUSE", font_name = font + "ARCADECLASSIC.ttf", font_size = '28sp'))
            self.pausescreen.add_widget(Label())
            self.add_widget(self.pausescreen) 
            self.screen1.pause()
            
    def Animate(self,button):
        if (button.x + button.width) > (Window.width - button.width):
            x_anim = Animation(x = Window.width - button.width, y = button.y +50, d = .15 )
        else:
            x_anim = Animation(x = button.x +50, y = button.y +50, d = .15)
        x_anim.start(button)
    def screen1(self):
        self.screen1 = Playscreen(name = '1')
        self.main.add_widget(self.screen1)
        
    def choose(self,string):
    
        if string == '1':
            Clock.schedule_once(lambda x: self.screen1.pause(), 1)
        self.main.current = string
    def screen2(self):
        screen2 = Screen(name = '2')
        
        screen2_pariente = GridLayout(cols = 1)
        screen2_pariente.add_widget(Label(size_hint_y = None, height = dp(65)))
        screen2_pariente.add_widget(Label(font_size = '44sp',size_hint_y = None, height = dp(44), text = "BRILLIANT", font_name = font + 'ARCADECLASSIC.ttf'))
        screen2_pariente.add_widget(Label(font_size = '20sp',size_hint_y = None, height = dp(27), text = "MAX SCORE 000000", font_name = font + 'ARCADECLASSIC.ttf'))
        screen2_pariente.add_widget(Label(size_hint_y = None, height = '50dp'))
        screen2_pariente.add_widget(Button(on_release = lambda x: self.choose('1'),font_size = '20sp',background_normal = color + 'None.png',size_hint_y = None, height = dp(50), text = "BEGIN", font_name = font + 'ARCADECLASSIC.ttf'))
        screen2_pariente.add_widget(Button(font_size = '20sp',background_normal = color + 'None.png',size_hint_y = None, height = dp(50), text = "SCORES", font_name = font + 'ARCADECLASSIC.ttf'))
        screen2_pariente.add_widget(Button(font_size = '20sp',background_normal = color + 'None.png',size_hint_y = None, height = dp(50), text = "EXIT", font_name = font + 'ARCADECLASSIC.ttf'))
        screen2_pariente.add_widget(Label())
        self.musica = Button(size_hint = (None,None), size = (dp(50),dp(50)), background_normal = asset + 'Group 9.png')
        self.pausa = Button(size_hint = (None,None), size = (dp(50),dp(50)), x = Window.width - 50, background_normal = asset + "Group 2.png")
        
        screen2.add_widget(screen2_pariente)
        screen2.add_widget(self.musica)
        self.main.add_widget(screen2)
        


        
        
        

            

                




    def funcion(self):
        print("hola")

class MyApp(App):
    def build(self):
        return InterfaceManager()
 

if __name__ in ('__main__', '__android__'):
    MyApp().run()

    
    
    
    
    