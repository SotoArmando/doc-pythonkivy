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
Window.clearcolor =  (1,1,1,1)
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
from kivy.uix.effectwidget import HorizontalBlurEffect,VerticalBlurEffect,FXAAEffect,EffectWidget,InvertEffect
class ImageButton(ButtonBehavior, Image): pass



class Combine(RelativeLayout):
    def __init__(self, **kwargs):
        super(Combine, self).__init__(**kwargs)
        self.size_hint_y = None 
        self.height = 64
        object_parent = GridLayout(cols = 1)
        self.bttn = ImageButton(source = kwargs["source"], keep_ratio = True, allow_stretch = True)
        self.bttntext = Label(text_size = (dp(100),dp(45)),halign = 'center', valign = 'middle',size_hint_y = None , text = kwargs["text"], markup = True, height = 30)
        
        object_parent.add_widget(self.bttn)
        object_parent.add_widget(self.bttntext)
        self.add_widget(object_parent)
        
class LateralMenu(RelativeLayout):
    def __init__(self, **kwargs):
        super(LateralMenu, self).__init__(**kwargs)
        self.add_widget(Image(opacity = .54,source = color + "3.png", keep_ratio = False , allow_stretch = True))
        
        
        self.poses = []
        self.pictures = []
        self.stats = [1,1,1,1,1,1]
        self.stats1 = [1,1,1,1,1,1]
        self.buttons = []
        pngs = ["Configuracion","Inicio","Posicion Actual","Archivo","Inspeccion","chat"]
        grid = GridLayout(cols = 1,size_hint = (None,1), width = '94dp',spacing = 24,pos_hint = {'center_x':.5,'center_y':.5})
        self.x1 = Label(font_size = 20,markup = True)
        Window.bind(mouse_pos=lambda w, p: setattr(self.x1, 'text', "[color=#000000]"+str(p)))
        for i in range(1):
            grid.add_widget(Label())
            for i in range(len(pngs)):
                a = Combine(source = pngs[i] + ".png", text = "[b]"+pngs[i])
                a.bttn.bind(on_release = lambda x:self.animate1(x))
                self.buttons.append(a.bttn)
                self.pictures.append(a.bttntext)
                grid.add_widget(a)
            grid.add_widget(Label(size_hint_y = None, height = 24))
            

        w = EffectWidget()
        w.add_widget(grid)
        
        self.add_widget(w)
        #self.add_widget(self.x1)
        Clock.schedule_interval(self.update, 1.0/60.0)
        #self.add_widget(Image(source = color + "3.png",size_hint_x = None, width =1 ,opacity = .24, x = 127, keep_ratio = False , allow_stretch = True))
 
    def update(self,x):
        x = len("[color=#000000]")
        val = self.x1.text[x:]
        
        val = val.replace(" ","")
        val = val.replace(".0","")
        val = val.replace("(","")
        val = val.replace(")","")
        if len(val) < 3: 
            pass
        else:
            nums = [float(n) for n in val.split(',')]
            #print nums
            for i in self.pictures:       
                if len(self.poses) >= 6:
                    pass
                else:
                    self.poses.append(i.parent.parent.pos)
                    print self.poses

        for i in self.poses:
            if (nums[1] > i[1]) and (nums[1] < i[1]+64):
                #print "hola", i
                if (nums[0] > i[0]) and (nums[0] < i[0]+64):
                    index = self.poses.index(i)
                    obj =  self.pictures[index]
                    self.animate(obj)

  

                

    def animate(self,object):
        index = self.pictures.index(object)
        if (self.stats[index] == 1) and (self.stats1[index] == 1):
            self.stats[index] *= -1
            def terminar(a,b):
                self.stats[index] *= -1
            
            animation = Animation(height = 10 ,opacity = 0, d = .225 , t = 'out_quad')
            animation.bind(on_complete = terminar)
            animation.start(object.parent.children[0])
                
                
            for x in self.pictures:
                if x == object.parent.children[0]:
                    pass
                else:
                    animation = Animation(height = dp(30) ,opacity = 1, d = .225 , t = 'out_quad')
                    animation.start(x)
                    
    def animate1(self,object):
        index = self.pictures.index(object.parent.children[0])
        if self.stats1[index] == 1:
            self.stats1[index] *= -1
            def terminar(a,b):
                self.stats1[index] *= -1
            animation = Animation(height = 0 ,opacity = 0, d = .225/2 , t = 'out_quad') + Animation(height = 10 ,opacity = 0, d = .225/2 , t = 'out_quad')
            animation.bind(on_complete = terminar)
            animation.start(object.parent.children[0])
                

                    
class MyApp(App):
    def build(self):
        return LateralMenu()
 

if __name__ in ('__main__', '__android__'):
    MyApp().run()

    
    
    
    
    