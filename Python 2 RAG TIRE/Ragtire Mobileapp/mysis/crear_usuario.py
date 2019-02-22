#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys  
reload(sys)  
sys.setdefaultencoding('latin-1')


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


class CrearUsuario(Screen):
    def __init__(self, **kwargs):
        super(CrearUsuario, self).__init__(**kwargs)
        pariente = GridLayout(cols = 1,opacity = 1)
        self.temp = kwargs["data"]
        self.connect = kwargs["connect"]
        pw = CustTextInput("Contraseña","***","***")
        cpw = CustTextInput("Confimar Contraseña","***","***")
        pw.selfTextInput().password = True
        cpw.selfTextInput().password = True
        dim = GridLayout(rows = 1,size_hint_y = None, height = '55dp')
        self.accept = Button(on_release = lambda x : self.send_usuario(),background_normal = color +'16.png',background_down = color +'16bb.png',markup = True,font_name = font + 'Roboto-Regular.ttf', text = C4+'Aceptar', font_size = '16sp')
        self.cancelar = Button(background_normal = color+ '16.png',background_down = color +'16bb.png',markup = True,font_name = font + 'Roboto-Regular.ttf', text = C4+'Cancelar', font_size = '16sp')
        dim.add_widget(self.accept)
        dim.add_widget(Image(size_hint_x = None, width = dp(1), keep_ratio = False, allow_stretch = True, source = color+'3.png', opacity = .14))
        dim.add_widget(self.cancelar)
        self.screenmanager = ScreenManager(size_hint_y = 1)
        screen1 = Screen(name = '1'); self.screenmanager.add_widget(screen1)
        screen2 = Screen(name = '2'); self.screenmanager.add_widget(screen2)
        scroll = ScrollView()
        screen1_parent = GridLayout(cols = 1,size_hint_y = None, height = dp(1200))
        scroll.add_widget(screen1_parent)
        screen1.add_widget(scroll)
        screen2_parent = GridLayout(cols = 1); screen2.add_widget(screen2_parent)
        
        pariente.add_widget(Label(size_hint_y = None, height = dp(71)))
        pariente.add_widget(Label(text = C4+"Añadir Cliente",text_size = (Window.width - 50 , dp(50)),valign = 'middle', halign = 'left',size_hint_y = None , height = '50dp', markup = True, font_size = '24sp'))
        pariente.add_widget(Image(size_hint_y = None, height = dp(1), keep_ratio = False, allow_stretch = True, source = color+'3.png', opacity = .14))
        #pariente.add_widget(Image(size_hint_y = None, height = dp(6), keep_ratio = False, allow_stretch = True, source = asset+'shaddown.png', opacity = 1))
        pariente.add_widget(self.screenmanager)
        
        
        screen1_parent.add_widget(Label(size_hint_y = None, height = dp(71)))
        screen1_parent.add_widget(Label(markup = True,text = C4+"Datos Personales", font_size = sp(20), size_hint_y = None, height = dp(40)))
        
        self.input1 = CustTextInput("Nombres","Nombres","Credencial")
        self.input1b = CustTextInput("Apellidos","Apellidos","Credencial")
        self.input2 = CustTextInput("identificacion","identificacion","cedula/pasaporte")
        self.input3 = CustTextInput("contacto","contacto","contacto")
        self.input4 = CustTextInput("telefono1","telefono1","telefono1")
        self.input5 = CustTextInput("telefono2","telefono2","telefono2")
        self.input12 = CustTextInput("Correo","Mail","@mail.com")
        self.input6 = CustTextInput("direccion1","direccion1","direccion1")
        self.input7 = CustTextInput("sector1","sector1","sector1")
        self.input8 = CustTextInput("ciudad1","ciudad1","ciudad1")
        self.input9 = CustTextInput("direccion2","direccion2","direccion2")
        self.input10 = CustTextInput("sector2","sector2","sector2")
        self.input11 = CustTextInput("ciudad2","ciudad2","ciudad2")
        self.input13 = CustTextInput("Posicion del Mapa","Posicion del Mapa","Posicion del Mapa")



        screen1_parent.add_widget(self.input1)
        screen1_parent.add_widget(self.input1b)
        screen1_parent.add_widget(self.input2)
        screen1_parent.add_widget(self.input3)
        screen1_parent.add_widget(self.input4)
        screen1_parent.add_widget(self.input5)
        screen1_parent.add_widget(self.input12)
        screen1_parent.add_widget(self.input13)
        screen1_parent.add_widget(Label(markup = True,text = C4+"Direcciones 1", font_size = sp(20), size_hint_y = None, height = dp(40)))
        screen1_parent.add_widget(self.input6)
        screen1_parent.add_widget(self.input7)
        screen1_parent.add_widget(self.input8)
        screen1_parent.add_widget(Label(markup = True,text = C4+"Direcciones 2", font_size = sp(20), size_hint_y = None, height = dp(40)))
        screen1_parent.add_widget(self.input9)
        screen1_parent.add_widget(self.input10)
        screen1_parent.add_widget(self.input11)
        

        
        
        pariente.add_widget(Image(source = color + '16.png', keep_ratio= False, allow_stretch = True,size_hint_y = None, height = '15dp'))
        pariente.add_widget(dim)
        #pariente.add_widget(Label(text_size = (Window.width, None),halign = 'center', valign = 'middle',text = "Ya tienes una cuenta?\n[b]Inicia Sesión", markup = True))
        
        
        self.add_widget(Image(source = color + '16.png', keep_ratio= False, allow_stretch = True))
        self.add_widget(pariente)
    def send_usuario(self):
        import datetime
        x = datetime.datetime.now()
        y = str(x).replace(" ", "T")
        y += "Z"
        i_jsondata =     {
            "direcciones_recientes": self.input1.input0.text,
            "telefono1": self.input4.input0.text,
            "sector2": self.input10.input0.text,
            "telefono2": self.input5.input0.text,
            "direccion2": self.input9.input0.text,
            "direccion1": self.input6.input0.text,
            "ciudad1": self.input8.input0.text,
            "sector1": self.input7.input0.text,
            "cliente": self.input1.input0.text + self.input1b.input0.text,
            "correo": self.input12.input0.text,
            "ciudad2": self.input11.input0.text,
            "identificacion": self.input2.input0.text,
            "contacto": self.input3.input0.text,
            "id": len(self.temp[3][0]) + 1
        }
        self.connect(tableid = 3 , jsondata = i_jsondata)


    def aceptarbtn(self): return self.accept
    def cancelarbtn(self): return self.cancelar
    def nextscreen(self):self.screenmanager.current = self.screenmanager.next()
        
class MyApp(App):
    def build(self):
        return CrearUsuario()
 

if __name__ in ('__main__', '__android__'):
    MyApp().run()

    
    
    
    
    