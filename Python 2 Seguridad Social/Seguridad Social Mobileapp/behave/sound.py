#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.checkbox import CheckBox
from kivy.uix.scatterlayout import ScatterLayout as Scatter
from kivy.uix.textinput import TextInput
from kivy.graphics import Color, Line, Rectangle
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
import os   
import os.path
Window.size = (360,640)
Window.clearcolor = (1,1,1,1)
#CARPETAS DEL PROYECTO
patch = os.path.dirname(os.path.abspath(__file__))
asset = patch + '/assets/drawable-mdpi/'
color = patch + '/colors/'
font = patch + '/fonts/'
from kivy.graphics import *
C1 = "[color=#13C0C7]"
C4 = "[color=#000000]"
C2 = "[color=#404040]"
C3 = "[color=#ff3333]"
C5 = "[color=#f2f2f2]"
C6 = "[color=#95989A]"
EC = "[/color]"
class ImageButton(ButtonBehavior, Image): pass



class SoundBox(RelativeLayout):
    def __init__(self, **kwargs):
        super(SoundBox, self).__init__(**kwargs)
        self.size_hint_y = None
        self.height = dp(54)
        self.duration = 3 #segundos
        self.state = False

        self.est = None
        self.add_widget(Image(source = color + "2.png", keep_ratio = False,  allow_stretch = True))
        self.th = Image(size_hint_y = 1, pos_hint = {'center_y':.5},opacity = .44,size_hint_x = 0,source = color + "16.png", keep_ratio = False,allow_stretch = True)
        self.add_widget(self.th)
        self.pariente = GridLayout(rows = 1)
        self.add_widget(self.pariente)
        self.pariente.add_widget(Image(size_hint_x = None, width = dp(64), source = asset + "ic_music_note_white_36dp.png"))
        self.parent0 = RelativeLayout()
        self.parent0.add_widget(Image(size_hint_y = .5, pos_hint = {'center_y':.5},opacity = .44,size_hint_x = 0,source = color + "16.png", keep_ratio = False,allow_stretch = True))

        self.label0 = Label(text = str(self.duration), size_hint = (None,None), size = (dp(100),dp(35)),valign = 'middle', text_size = (dp(100),dp(35)), pos_hint = {'x':.05, 'center_y':.5})
        self.parent0.add_widget(self.label0)
        self.pariente.add_widget(self.parent0)
        self.pariente.add_widget(ImageButton(on_release = lambda x:self.animate(),size_hint_x = None, width = dp(64), source = asset + "ic_play_arrow_white_36dp.png"))
        self.opacity = 0
    def animate(self):
        if self.state == False:
            from kivy.core.audio import SoundLoader,Sound
            import contextlib
            import wave
            Sonido = SoundLoader.load(patch+"\soundd.wav")
            soundx = Sonido.load()
            self.state == True
            fname = patch+"\soundd.wav"
            with contextlib.closing(wave.open(fname,'r')) as f:
                frames = f.getnframes()
                rate = f.getframerate()
                xduration = frames / float(rate)
                print(xduration)
            self.duration = int(xduration)
            self.est = self.duration
 
            def set(*args): 
                self.parent0.children[-1].size_hint_x = 0
                self.state = False
                self.duration = self.est
                self.label0.text = str(self.duration)
            a = Animation(size_hint_x = 1 , d = self.duration)
            a.bind(on_complete = lambda x,y:set())
            a.bind(on_complete = lambda x,y: Clock.unschedule(self.less))
            

            Sonido.play()
            
            a.start(self.th)
            Clock.schedule_interval(self.less, 1)
    def show(self):
        a = Animation(opacity = 1 , d = .5 , t = 'out_back')
        a.start(self)


    def less(self,x): 
        import time
        self.duration -= 1
        self.label0.text = time.strftime('%M:%S', time.gmtime(self.duration))
class MyApp(App):
    def build(self):
        return SoundBox()
 

if __name__ in ('__main__', '__android__'):
    MyApp().run()

    
    
    
    
    