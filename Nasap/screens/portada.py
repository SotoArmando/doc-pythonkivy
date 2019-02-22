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


class ImageButton(ButtonBehavior, Image): pass

class Slidecircles(RelativeLayout):
    def __init__(self, **kwargs):
        super(Slidecircles, self).__init__(**kwargs)
        self.size_hint_y = None
        self.height = dp(12)
        pariente = RelativeLayout()
        self.ellipse = ImageButton(size_hint_x = None, width = dp(12), x = (Window.width/2)-dp(6)-dp(40),source = asset + "Ellipse 10.png")
        pariente.add_widget(self.ellipse)
        pariente.add_widget(ImageButton(source = asset + "Group 2.png"))
        self.add_widget(pariente)
        self.i_pos = 0 
        self.x_pos = (Window.width/2)-dp(6)-dp(40)
        
        self.add_widget(Button(on_release = lambda x: self.animate_l(),y = 300))
    def animate_l(self):
        if self.i_pos <= 0:
            self.i_pos = 4
            x_anim = Animation(x = self.x_pos + dp(20)*self.i_pos, d = .255, t = 'out_quart')
            x_anim.start(self.ellipse)
        else:
            self.i_pos -= 1
            x_anim = Animation(x = self.x_pos + dp(20)*self.i_pos, d = .255, t = 'out_quart')
            x_anim.start(self.ellipse)
    def animate_r(self):
        if self.i_pos >= 4:
            self.i_pos = 0
            x_anim = Animation(x = self.x_pos + dp(20)*self.i_pos, d = .255, t = 'out_quart')
            x_anim.start(self.ellipse)
        else:
            self.i_pos += 1
            x_anim = Animation(x = self.x_pos + dp(20)*self.i_pos, d = .255, t = 'out_quart')
            x_anim.start(self.ellipse)
class Portada(Screen):
    def __init__(self, **kwargs):
        super(Portada, self).__init__(**kwargs)
        pariente = GridLayout(cols = 1)
        
        dim = GridLayout(rows = 1, size_hint_y = None, height = dp(55))
        titles = ["MY VEHICLE","MY STORE"] 
        img1 = ["ic_directions_car_black_24px","ic_store_mall_directory_black"] 
        for i in range(2):
            sub_dim = GridLayout(cols = 2)
            sub_dim_labels = GridLayout(cols = 1, padding = [0,dp(8),0,dp(8)])
            leftimg = Image(source = asset + img1[i]+".png", size_hint_x = None, width = dp(50))
            rightlabel = Label(markup = True,valign = 'middle',text_size = ((Window.width/2) - dp(50),dp(40)), text = C4 + titles[i])
            rightsublabel = Label(markup = True,valign = 'middle',text_size = ((Window.width/2) - dp(50),dp(40)),font_size = '14sp', text = C4 + "[b]Select option")
            
            sub_dim_labels.add_widget(rightlabel)
            sub_dim_labels.add_widget(rightsublabel)
            sub_dim.add_widget(leftimg)
            sub_dim.add_widget(sub_dim_labels)
            dim.add_widget(sub_dim)
        
        self.screenmanager = ScreenManager()
        screenmanager_parent = RelativeLayout(size_hint_y = None , height = dp(200))
        img = ['15','14','13'] 
        for i in range(3):
            x = Screen(name = str(i))
            pantalla = Image(source = color +  img[i]+".png", keep_ratio = False, allow_stretch = True)
            x.add_widget(pantalla)
            self.screenmanager.add_widget(x)
        
        screenmanager_left = ImageButton(on_release = lambda x: self.screenmanager_previous(),pos_hint = {'center_y':.2 , 'center_x':.1},source = asset + "ic_navigate_before_black_24px.png", size_hint = (None,None), size = (dp(50),dp(50)))
        screenmanager_right = ImageButton(on_release = lambda x: self.screenmanager_next(),pos_hint = {'center_y':.2 , 'center_x':.9},source = asset + "ic_navigate_next_black_24px.png", size_hint = (None,None), size = (dp(50),dp(50)))
        screenmanager_circles = ImageButton(pos_hint = {'center_y':.9 , 'center_x':.5},source = asset + "24x24.png", size_hint = (None,None), size = (dp(50),dp(50)))
        screenmanager_chapa = Button(text = "populares",font_size = '19sp',font_name = font + "Roboto-Medium.ttf",pos_hint = {'center_y':1, 'center_x': .5},background_normal = color + "3.png", size_hint = (None,None), size = (dp(200),dp(35)))
        
        self.screenmanager1 = ScreenManager()
        screenmanager1_parent = RelativeLayout(size_hint_y = None , height = dp(200))
        for i in range(3):
            x = Screen(name = str(i))
            grid0 = GridLayout(rows = 1,spacing = (4,0), size_hint_y = .75, pos_hint = {'center_y': .4})
            grid0.add_widget(Label())
            def objeto0():
                objeto0_pariente = GridLayout(cols = 1,size_hint_x = None, width = '100dp')
                objeto0_imagen = ImageButton(keep_ratio = False, allow_stretch = True,source = color + "3.png",size_hint_y = None, height = '100dp')
                objeto0_titulo = Button(markup = True,font_name = font + 'Roboto-Medium.ttf',font_size = '17sp',text = C4+"titulo",background_normal = color + "None.png")
                
                objeto0_pariente.add_widget(objeto0_imagen)
                objeto0_pariente.add_widget(objeto0_titulo)
                return objeto0_pariente
            
            grid0.add_widget(objeto0())
            grid0.add_widget(objeto0())
            grid0.add_widget(objeto0())
            grid0.add_widget(Label())
            x.add_widget(grid0)
            self.screenmanager1.add_widget(x)
            
            
        screenmanager1_left = ImageButton(on_release = lambda x: self.screenmanager1_previous(),pos_hint = {'center_y':.5 , 'center_x':.05},source = asset + "ic_navigate_before_white_24px.png", size_hint = (None,None), size = (dp(50),dp(50)))
        screenmanager1_right = ImageButton(on_release = lambda x: self.screenmanager1_next(),pos_hint = {'center_y':.5 , 'center_x':.95},source = asset + "ic_navigate_next_white_24px.png", size_hint = (None,None), size = (dp(50),dp(50)))
        self.slider0 = Slidecircles(pos_hint = {'center_y':.2 , 'center_x':.5})
        screenmanager_parent.add_widget(self.screenmanager)
        screenmanager_parent.add_widget(screenmanager_left)
        screenmanager_parent.add_widget(screenmanager_right)
        screenmanager_parent.add_widget(self.slider0)
        
        screenmanager1_parent.add_widget(Image(opacity = .56,source = color + '2.png', keep_ratio = False, allow_stretch = True))
        screenmanager1_parent.add_widget(self.screenmanager1)
        screenmanager1_parent.add_widget(screenmanager1_left)
        screenmanager1_parent.add_widget(screenmanager1_right)
        screenmanager1_parent.add_widget(screenmanager_chapa)
        pariente.add_widget(Label(size_hint_y = None, height = '90dp'))
        pariente.add_widget(dim)
        pariente.add_widget(screenmanager_parent)
        pariente.add_widget(screenmanager1_parent)
        self.add_widget(pariente)
        
    def screenmanager1_next(self): self.screenmanager1.current = self.screenmanager1.next()
    def screenmanager1_previous(self): self.screenmanager1.current = self.screenmanager1.previous()
    def screenmanager_next(self): 
        self.slider0.animate_r()
        self.screenmanager.current = self.screenmanager.next()
    def screenmanager_previous(self): 
        self.slider0.animate_l()
        self.screenmanager.current = self.screenmanager.previous()
            
        

class MyApp(App):
    def build(self):
        return Portada()
 

if __name__ in ('__main__', '__android__'):
    MyApp().run()

    
    
    
    
    