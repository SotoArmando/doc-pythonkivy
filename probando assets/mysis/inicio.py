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
from autosize import MyButton as SizeButton
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


class Inicio(RelativeLayout):
    def __init__(self, **kwargs):
        super(Inicio, self).__init__(**kwargs)
        self.add_widget(Image(source = color + "3.png",opacity = .10, keep_ratio = False ,allow_stretch = True))
        programparent = RelativeLayout(size_hint_x = .95 ,size_hint_y = .75,y = Window.height-dp(79)-(Window.height*.5), pos_hint = {'center_x':.5,'center_y':.5})
        pariente = GridLayout(cols = 3,spacing = [1,1])
        self.bindings = []
        img = ['ic_info_black_36px',
        'ic_add_shopping_cart_black_36',
        'ic_build_black_36px',
        'ic_account_balance_black_36px',
        'ic_exit_to_app_black_36px',
        'ic_account_box_black_36px','ic_account_box_black_36px','ic_account_box_black_36px','ic_account_box_black_36px','ic_account_box_black_36px',
        'ic_credit_card_black_36px'
        ]
        text = ["Contact Us","Schedule\nAppointment","Find My Shop","Ask My\nTechnician","Specials","Recommended","Find My Car","Emergency\nResponder","My Vehicle\nDocuments"
        ]
        menusetx1 = [
        [3.04,"Inicio","Tocar para ir."],
        [3.04,"Pedido Actual","Tocar para abrir."],
        [3.04,"Entregas Realizadas","Tocar para abrir."],
        [3.04,"Inventario","Tocar para abrir."],
        [3.04,"Ventas","Cuentas por Cobrar"],
       #[3.04,"Clientes","Tocar para abrir"],
        [3.04,"Añadir Cliente","Tocar para abrir."],
        [3.04,"Recordatorios","Tocar para abrir."],
        [3.04,"Mostrar Ruta","Tocar para mostrar."],
        [3.04,"Configuracion","Tocar para mostrar."],
        [3.04,"Vendedores","Tocar para mostrar."],
        [3.04,"Ayuda","Tocar para mostrar."],
        ]

        for i in range(11): 
            scatter = Scatter()
            scatter_parent = GridLayout(cols = 1)
            widget_parent_background = RelativeLayout()
            scatter.add_widget(widget_parent_background)
            scatter_parent.add_widget(scatter)
            widget_parent_background.add_widget(Image(source = color + '16.png',opacity = .74, keep_ratio = False, allow_stretch = True))
            widget_parent = GridLayout(cols = 1)
            imagebutton0 = ImageButton(on_release = lambda x: self.Animation(x.parent.parent.parent.parent),size_hint_y = None , height = '60px', source = asset + img[i] + '.png')

            
            imagebutton0.bind(on_release = lambda x: self.hola())
            self.bindings.append(imagebutton0)
            widget_parent.add_widget(imagebutton0)
            widget_parent.add_widget(SizeButton(halign = 'center', valign = 'middle',text_size = ((Window.width*.95)/3.0,50 ), size_hint_y = 1,on_release = lambda x: self.Animation(x.parent.parent.parent.parent),background_normal = color + 'None.png', text = C4+menusetx1[i][1], markup = True))
            widget_parent_background.add_widget(widget_parent)
            pariente.add_widget(scatter_parent)
            
            
        buscador = TopNavigationS()
        programparent.add_widget(pariente)
        self.add_widget(programparent)
        #self.add_widget(buscador)
    def hola(self):
        print "hola"
    def Animation(self, x):
        
        dur = .225
        x_anim = Animation(scale = .85, d = dur/2 , t = 'out_circ' )
        x_anim1 = Animation(scale = 1, d = dur/2 , t = 'out_circ' )
        x_anim.bind(on_complete = lambda x,y: x_anim1.start(y))
        x_anim.start(x)


class MyApp(App):
    def build(self):
        return Inicio()
 

if __name__ in ('__main__', '__android__'):
    MyApp().run()

    
    
    
    
    