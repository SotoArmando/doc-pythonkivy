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
from kivy.graphics import Color, Line, Rectangle, Ellipse
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
C7 = "[color=#ff0000]"
EC = "[/color]"

Window.clearcolor = (1,1,1,1)

class ImageButton(ButtonBehavior, Image): pass

def Dp(*args):
    tuple = []
    for i in args:
        tuple.append(dp(i))
    return tuple
        

class CustTextInput(RelativeLayout):
    cleansize_x = NumericProperty(0)
    added = False
    def __init__(self,i_text,sub_text,ihint_text, **kwargs):
        super(CustTextInput, self).__init__(**kwargs)
        self.size_hint_y = None
        self.height = '69dp'
        self.add_widget(Image(source = color + "16.png", keep_ratio = False, allow_stretch = True))
        pariente = GridLayout(cols = 1,spacing = [0,0],padding = [dp(25),0,dp(25),dp(8)])
        left = 49
        self.label0 = Label(font_size = '19sp',text_size = (Window.width-dp(left),dp(75)),valign = 'bottom',size_hint_y = None, height = dp(25),markup = True,text = C4+i_text)
        pariente.add_widget(self.label0)
        self.input0 = TextInput(on_text_validate = lambda x: self.on_click_onit(),font_size = '16sp',cursor_color = (0,0,0,1),padding = [dp(-2),dp(5),dp(8),0],multiline = False,size_hint_y = None, height = dp(29),background_normal = color + "None.png",background_active = color + "None.png",markup = True)
        self.input0.bind(focus = self.on_focus)
        pariente.add_widget(self.input0)
        self.errortxt= Label(font_size = '12sp',opacity = 0,valign = 'top',text_size = (Window.width-dp(left),dp(20)),size_hint_y = None, height = dp(25),markup = True,text = C7+"error: usuario no disponible.")
        self.imageparent = RelativeLayout(size_hint_y = None, height = dp(2))
        self.image_animated1 =Image(opacity = .54,source = color + "2.png",keep_ratio = False, allow_stretch = True)
        self.image_animated2 =Image(opacity = 0.,source = color + "10.png",keep_ratio = False, allow_stretch = True)
        self.image_animated3=Image(opacity = 0.,source = color + "1.png",keep_ratio = False, allow_stretch = True)
        self.imageparent.add_widget(self.image_animated1)
        self.imageparent.add_widget(self.image_animated2)
        self.imageparent.add_widget(self.image_animated3)
        pariente.add_widget(self.imageparent)
        pariente.add_widget(self.errortxt)
        self.add_widget(pariente)
        self.onit = Button(background_normal = color + "None.png",background_down = color + "None.png",disabled = False, on_release = lambda x: self.on_click_onit())
        self.add_widget(self.onit)
        
        self.cleanbuttonpiz = RelativeLayout(size_hint = (None,None) ,size = Dp(32,32), pos_hint = {'center_x':.9 , 'center_y':.6} )
        self.cleanbutton = Button(background_normal = '' , background_down = '',on_release = lambda x: self.cleansizeactive(), background_color = (0,0,0,1))
        self.cleanbuttonpiz.add_widget(self.cleanbutton)
        with self.cleanbuttonpiz.canvas:
            Color(0,0,0,.5)
            Ellipse(size = Dp(self.cleansize_x,self.cleansize_x), pos = (dp(32)/2 - self.cleansize_x/2,dp(32)/2 - self.cleansize_x/2))
            
        #self.error("No jodas") 
    def on_cleansize_x(self,*args):
        self.cleanbuttonpiz.canvas.clear()
        with self.cleanbuttonpiz.canvas:
            Color(0,0,0,.24)
            Ellipse(size = Dp(self.cleansize_x,self.cleansize_x), pos = (dp(32)/2 - self.cleansize_x/2,dp(32)/2 - self.cleansize_x/2))
            Color(1,1,1,1)
            Rectangle(source = "cancel.png", size = Dp(self.cleansize_x/2.0,self.cleansize_x/2.0), pos = (dp(32)/2 - self.cleansize_x/4.0,dp(32)/2 - self.cleansize_x/4.0))
            
    def cleansizeactive(self,*args):
        self.input0.text = ""
        self.sizing()
        x = Animation(cleansize_x = dp(0), t = 'out_back', d = .5)
        x.start(self)
        
    def add_cleanbutton(self):
        if self.added == False: self.add_widget(self.cleanbuttonpiz) ; self.added = True
        x = Animation(cleansize_x = dp(32), t = 'out_back', d = .5)
        x.start(self)
        
    def sizing(self):
        left = 49
        if self.input0.text == "":
            sizing_animate = Animation(font_size = sp(19),text_size = (Window.width-dp(left),dp(75)), d = .255 , t = 'out_cubic')
            sizing_animate.start(self.label0)
        else:
            self.add_cleanbutton()
        sizing_animate1 = Animation(opacity = 0, d = .255 , t = 'in_out_cubic')
        sizing_animate1.start(self.image_animated2)
    def sizing1(self):
        left = 49
        sizing_animate = Animation(font_size = sp(13),text_size = (Window.width-dp(left),dp(20)), d = .255 , t = 'out_cubic')
        sizing_animate1 = Animation(opacity = 1., d = .255 , t = 'in_out_cubic')
        sizing_animate.start(self.label0)
        sizing_animate1.start(self.image_animated2)
        
    def error(self):self.errortxt.opacity = 1.
    def returninput(self): return self.input0
    def on_focus(self,instance, value):
        if value:
            print('User focused', instance)
            self.sizing1()
        else:
            print('User defocused', instance)
            self.sizing()

    def on_click_onit(self):
        try:
            self.add_widget(self.onit)
            anim_x = Animation(opacity = 0., d = .225 , t = 'out_circ')
            anim_x.start(self.image_animated2)
            anim_x.start(self.image_animated3)
            anim_x.start(self.errortxt)
        except:
            self.remove_widget(self.onit)
            self.input0.focus = True
            anim_x = Animation(opacity = 1., d = .225 , t = 'in_circ')
            anim_x.start(self.image_animated2)
            
    def error(self,text):
        try:
            self.add_widget(self.onit)
            anim_x = Animation(opacity = 0., d = .225 , t = 'out_circ')
            anim_x.start(self.image_animated3)
        except:
            self.remove_widget(self.onit)
            self.input0.focus = True
            anim_x = Animation(opacity = 1., d = .225 , t = 'in_circ')
            self.errortxt.text = C7+"text"
            anim_x.start(self.image_animated3)
            anim_x.start(self.errortxt)
            


class MyApp(App):
    def build(self):
        gridlayout = GridLayout(cols = 1)
        gridlayout.add_widget(Label(text = C4+"Cual es tu color preferido??",size_hint_y = None, height = dp(24), font_size = dp(17), markup = True))
        gridlayout.add_widget(CustTextInput("Respuesta","sub_text","hin_text"))
        gridlayout.add_widget(Label(text = C4+"Cual es tu color preferido??",size_hint_y = None, height = dp(24), font_size = dp(17), markup = True))
        gridlayout.add_widget(CustTextInput("Respuesta","sub_text","hin_text"))
        gridlayout.add_widget(Label(text = C4+"@@[b]Credenciales",size_hint_y = None, height = dp(24), font_size = dp(17), markup = True))
        gridlayout.add_widget(CustTextInput("Usuario","sub_text","hin_text"))
        gridlayout.add_widget(CustTextInput("Contraseña","sub_text","hin_text"))
        return gridlayout
 

if __name__ in ('__main__', '__android__'):
    MyApp().run()

    
    
    
    
    