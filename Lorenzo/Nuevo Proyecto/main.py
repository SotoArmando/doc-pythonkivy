#!/usr/bin/env python
# -*- coding: utf-8 -*-

from kivy.uix.stencilview import StencilView
from kivy.properties import (ObjectProperty, NumericProperty, OptionProperty, BooleanProperty, StringProperty)
from kivy.lang import Builder

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
from kivy.metrics import dp
from kivy.clock import Clock
from kivy.resources import resource_add_path
import os
C1 = "[color=#13C0C7]"
C4 = "[color=#000000]"
C2 = "[color=#404040]"
C3 = "[color=#ff3333]"
C5 = "[color=#f2f2f2]"
C6 = "[color=#95989A]"
EC = "[/color]"
#CARPETAS DEL PROYECTO
patch = os.path.dirname(os.path.abspath(__file__))
asset = patch + '/assets/drawable-mdpi/'
color = patch + '/colors/'
font = patch + '/fonts/'

#VARIABLES GLOBALES
Hola = "Hola a todos"
from utils import NavigationDrawer,BottomNavigation,TopNavigationS
Window.size = (360,640)

class ImageButton(ButtonBehavior,Image):pass
Window.clearcolor = (1,1,1,1)

class InterfaceManager(RelativeLayout):#COMPLEMENTO 'PARENT' EL PROYECTO
    def __init__(self, **kwargs):
        super(InterfaceManager, self).__init__(**kwargs)
        self.a1 = TopNavigationS(opacity = .74)
        a2 = BottomNavigation()
        a3 = NavigationDrawer()
        self.a4 = ScreenManager()
        self.a1.y = Window.height - self.a1.height
        
        #self.topnavbar.y = Window.height - self.topnavbar.height
        interface = RelativeLayout()

        self.add_widget(a3)
        interface.add_widget(self.a4)
        interface.add_widget(self.a1)
        interface.add_widget(a2)
        
        a3.add_widget(Button())
        a3.add_widget(interface)
        
        self.a1.leftbutton().bind(on_release = lambda x: a3.toggle_state())
        self.a1.rightbutton().bind(on_release = lambda x: self.choose("busqueda"))
        self.a1.textinput().bind(on_text_validate = lambda x: self.buscarmaterias())
        
        self.screen5()
        self.screen1()
        self.busquedascreen()
        
    def agregarmateria(self):   
        BC1 = '[color=#0090FF]'
        BC2 = '[color=#F45D5D]'
        try:
            self.label0.parent.remove_widget(self.label0)
        except:
            pass
        
        pariente = GridLayout(rows = 2, size_hint_y = None, height = dp(35))
        pariente_titulo_dim = RelativeLayout(size_hint_y = None, height = dp(35))
        pariente_titulo = GridLayout(rows = 1, size_hint_y = None, height = dp(35))
        pariente_hijos = GridLayout(opacity = 0.,cols = 1,size_hint_y = None , height = 0)
        
        pariente_titulo_dim.add_widget(Image(source = color + '10.png',keep_ratio = False, allow_stretch = True))
        pariente_titulo_dim.add_widget(pariente_titulo)
        
        pariente.add_widget(pariente_titulo_dim)
        pariente.add_widget(pariente_hijos)
        
        def open(x):
            print "hola"
            print x
            if pariente_hijos.height == 0:
                x_height = (len(pariente_hijos.children)/2 *dp(71))
                x_anim1 = Animation(opacity = 1.,height = x_height ,d = .3, t = 'out_circ')
                x_anim2 = Animation(height = x_height+dp(35), d = .3, t = 'out_circ')
                x_anim1.start(x)
                x_anim2.start(x.parent)
            else:
                x_anim1 = Animation(opacity = 0.,height = 0, d = .3, t = 'in_circ')
                x_anim2 = Animation(height = dp(35), d = .3, t = 'in_circ')
                x_anim1.start(x)
                x_anim2.start(x.parent)
                

                
        
        pariente_titulo.add_widget(ImageButton(on_release = lambda x: open(x.parent.parent.parent.children[0]),size_hint_x = None ,width = dp(50), source = asset + "Group 126.png"))
        pariente_titulo.add_widget(Label(halign = 'center',text_size = (dp(200),None),markup = True ,font_name = font + 'Roboto-Light.ttf',font_size = '14sp', text = "Logica de Programacion", size_hint_x = None, width = '180dp'))
        pariente_titulo.add_widget(Label(halign = 'center',text_size = (dp(65),None),markup = True ,font_name = font + 'Roboto-Medium.ttf',font_size = '14sp', text = BC1 + "@Lorenzo", size_hint_x = None, width = '50dp'))
        pariente_titulo.add_widget(Label())
        pariente_titulo.add_widget(Button(size_hint_x = None ,width = dp(35),background_normal = asset + "Group 127.png"))
        
        #DOCUMENTOS DE LA MATERIA
        def documento():
            pariente2 = GridLayout(cols = 3, size_hint_y = 1)
            pariente2.add_widget(Label(opacity = .54,text_size = (dp(71),dp(50)),valign = 'bottom',halign = 'left',text = C4+'1m', markup = True))
            pariente2_hijo = GridLayout(cols = 1)
            pariente2_hijo.add_widget(Label(opacity = .54,text_size = (dp(200),dp(25)),valign = 'bottom',halign = 'left',text = C4+'@Lorenzo', markup = True))
            pariente2_hijo.add_widget(Label(opacity = .54,text_size = (dp(200),dp(25)),valign = 'bottom',halign = 'left',text = C4+'Archivo Importante', markup = True))
            pariente2_hijo_botones = GridLayout(opacity = .54,rows = 1)
            pariente2_hijo_botones.add_widget(ImageButton(source = asset + 'like.png'))
            pariente2_hijo_botones.add_widget(ImageButton(source = asset + 'retweet.png', markup = True))
            pariente2_hijo_botones.add_widget(Label())
            pariente2.add_widget(pariente2_hijo);pariente2_hijo.add_widget(pariente2_hijo_botones)
            pariente2.add_widget(Label(opacity = .54,text_size = (dp(71),dp(50)),valign = 'bottom',halign = 'center',text = C4+'.Doc', markup = True))
            return pariente2
            
        pariente_hijos.add_widget(documento())
        pariente_hijos.add_widget(Image(opacity = .21,size_hint_y = None , height = dp(1) , source = color + '3.png', keep_ratio = False, allow_stretch = True))
        pariente_hijos.add_widget(documento())
        pariente_hijos.add_widget(Image(opacity = .21,size_hint_y = None , height = dp(1) , source = color + '3.png', keep_ratio = False, allow_stretch = True))
        pariente_hijos.add_widget(documento())
        pariente_hijos.add_widget(Image(opacity = .21,size_hint_y = None , height = dp(1) , source = color + '3.png', keep_ratio = False, allow_stretch = True))


        
        self.screen1_parent.add_widget(pariente)
        self.choose('1')
        self.a1.search_animate()
        
    def choose(self,string): 
        self.a4.current = string
    def buscarmaterias(self):
        BC1 = '[color=#0090FF]'
        BC2 = '[color=#F45D5D]'
        self.busqueda_pariente_hijo.clear_widgets()
        self.busqueda_pariente_hijo.add_widget(Label(size_hint_y = None , height = dp(100)))
        for i in range(10): 
            self.busqueda_pariente_hijo.add_widget(self.searchitem())
            self.busqueda_pariente_hijo.add_widget(Image(opacity = .14,source = color + '3.png', keep_ratio = False, allow_stretch = True, size_hint_y = None, height = dp(1)))
    def searchitem(self):
        BC1 = '[color=#0090FF]'
        BC2 = '[color=#F45D5D]'
        pariente =  GridLayout(opacity = .91,padding = [10,0,0,0],rows = 1,size_hint_y = None , height = dp(50))
        pariente.add_widget(Label(halign = 'center',text_size = (dp(60),None),markup = True ,font_name = font + 'Roboto-Medium.ttf',font_size = '13sp', text = BC2 + "INS203", size_hint_x = None, width = '60dp'))
        pariente.add_widget(Label(halign = 'center',text_size = (dp(200),None),markup = True ,font_name = font + 'Arial_Italic.ttf',font_size = '13sp', text = BC2 + "Logica de Programacion", size_hint_x = None, width = '180dp'))
        pariente.add_widget(Label(halign = 'center',text_size = (dp(65),None),markup = True ,font_name = font + 'Roboto-Medium.ttf',font_size = '13sp', text = BC1 + "@Lorenzo", size_hint_x = None, width = '50dp'))
        pariente.add_widget(Button(on_release = lambda x: self.agregarmateria(),background_normal = asset + 'Group 119.png',background_down = asset + 'Group 119.png', size_hint_x = None, width = '50dp'))
        return pariente
        
    def papeleraitem(self):
        BC1 = '[color=#0090FF]'
        BC2 = '[color=#F45D5D]'
        pariente =  GridLayout(opacity = .54,padding = [10,0,0,0],rows = 1,size_hint_y = None , height = dp(50))
        pariente.add_widget(Label(halign = 'center',text_size = (dp(60),None),markup = True ,font_name = font + 'Roboto-Medium.ttf',font_size = '13sp', text = C4 + "INS203", size_hint_x = None, width = '60dp'))
        pariente.add_widget(Label(halign = 'center',text_size = (dp(200),None),markup = True ,font_name = font + 'Arial_Italic.ttf',font_size = '13sp', text = C4 + "Logica de Programacion", size_hint_x = None, width = '180dp'))
        pariente.add_widget(Label(halign = 'center',text_size = (dp(65),None),markup = True ,font_name = font + 'Roboto-Medium.ttf',font_size = '13sp', text = C4 + "@Lorenzo", size_hint_x = None, width = '50dp'))
        pariente.add_widget(Button(on_release = lambda x: self.agregarmateria(),background_normal = asset + 'Group 132.png',background_down = asset + 'Group 132.png', size_hint_x = None, width = '50dp'))
        return pariente
    def busquedascreen(self):
        busqueda_screen = Screen(name = 'busqueda')
        busqueda_screen.add_widget(Image(source = color + "16.png", keep_ratio= False, allow_stretch = True))
        self.a4.add_widget(busqueda_screen)
        self.busqueda_pariente = ScrollView()
        busqueda_screen.add_widget(self.busqueda_pariente)
        self.busqueda_pariente_hijo = GridLayout(cols = 1, size_hint_y = None, height = dp(1000), spacing = 4)
        self.busqueda_pariente.add_widget(self.busqueda_pariente_hijo)
        self.busqueda_pariente_hijo.add_widget(Label(size_hint_y = None , height = dp(100)))
        
    def screen1(self):
        screen1 = Screen(name = '1'); self.a4.add_widget(screen1)
        screen1_background = Image(source = color + "16.png", keep_ratio = False, allow_stretch = True,size_hint_y = 1 )
        self.screen1_scroll = ScrollView()
        self.screen1_parent = GridLayout(cols = 1, size_hint_y = None ,height = dp(1000))
        
        self.screen1_scroll.add_widget(self.screen1_parent)
        self.screen1_parent.add_widget(Image(source = color + "10.png", size_hint_y = None , height = '200dp', keep_ratio = False, allow_stretch = True))
        self.screen1_parent.add_widget(Label(font_size = "24sp",size_hint_y = None, height = 0 ,text_size = (dp(Window.width - 50), dp(125)),halign = 'left', valign = 'top',markup = True, text =  "Armando Jose Soto Melo"))
        self.screen1_parent.add_widget(Label(font_size = "20sp",size_hint_y = None, height = 0 ,text_size = (dp(Window.width - 50), dp(65)),halign = 'left', valign = 'top',markup = True, text =  "1066320"))
        self.screen1_parent.add_widget(Image(opacity = .14,source = color + "2.png", size_hint_y = None , height = '1dp', keep_ratio = False, allow_stretch = True))
        
        button_rel = RelativeLayout(size_hint_y = 1 )
        button_rel_button1 = Button(size_hint = (None,None),text = "+",markup = True,background_down = color + "10.png",background_normal = color + "10.png", size = (dp(55),dp(55)), pos_hint = {'center_x':.5, 'center_y':.5})
        button_rel.add_widget(button_rel_button1)

        #self.screen1_parent.add_widget(button_rel)
        screen1.add_widget(screen1_background)
        screen1.add_widget(self.screen1_scroll)
        
    def screen5(self):
        screen5 = Screen(name = '5'); self.a4.add_widget(screen5)
        screen5_background = Image(source = asset + "Rectangle 11.png", size_hint = (None,None), size = (dp(501),dp(940)) ,y = dp(-940) + Window.height, pos_hint = {'center_x':.5})
        screen5_background2 = Image(opacity = .94,source = asset + "Rectangle 8.png",background_down = asset + "Rectangle 8.png", size_hint = (.95,.95), pos_hint = {'center_x':.5, 'center_y' : .5})
        screen5.add_widget(screen5_background)
        #screen5.add_widget(screen5_background2)
        
        screen5_layout = GridLayout(cols = 1, padding = [20,0,20,0]);screen5.add_widget(screen5_layout)
        screen5_layout.add_widget(Label())
        screen5_layout.add_widget(Label(size_hint_y = None, height = '50dp',markup = True,text = C4+"Codi",font_name = font+'segoescb.ttf', font_size = '40sp', opacity = .64))
        
        screen5_layout.add_widget(Label(size_hint_y = None , height = '25dp'))
        
        dim1 = RelativeLayout(size_hint_y = None, height = '50dp')
        dim2 = RelativeLayout(size_hint_y = None, height = '50dp')
        
        dim1.add_widget(Button(opacity = .54,pos_hint = {'center_x':.5},background_normal = asset + 'Group 94.png', size = ('268dp','50dp'), size_hint = (None,None) , background_down = asset + 'Group 94.png'))
        dim1.add_widget(TextInput(cursor_color = [0,0,0,.54],cursor_width = '2sp',pos_hint = {'center_x':.5},padding = [30,19,0,0],hint_text_color = [0,0,0,.54],hint_text = "Usuario",size_hint = (None,None) ,width = '267dp', height = '50dp', background_normal = color + 'None.png', background_active = color + 'None.png'))
        
        dim2.add_widget(Button(opacity = .54,pos_hint = {'center_x':.5},background_normal = asset + 'Group 94.png', size = ('268dp','50dp'), size_hint = (None,None) , background_down = asset + 'Group 94.png'))
        dim2.add_widget(TextInput(cursor_color = [0,0,0,.54],cursor_width = '2sp',password = True,pos_hint = {'center_x':.5},padding = [30,19,0,0],hint_text_color = [0,0,0,.54],hint_text = "Contraseña",size_hint = (None,None) ,width = '267dp', height = '50dp', background_normal = color + 'None.png', background_active = color + 'None.png'))
        dim2.add_widget(Button(password = True,pos_hint = {'center_x':.8},hint_text_color = [0,0,0,.54],hint_text = "Contraseña",size_hint = (None,None) ,width = '50dp', height = '50dp', background_normal = asset + 'Group 93.png', background_down = asset + 'Group 93.png'))

        
        
        screen5_layout.add_widget(dim1)
        screen5_layout.add_widget(Label(size_hint_y = None , height = '20dp'))
        screen5_layout.add_widget(dim2)
        
        
        
        dim3 = RelativeLayout(opacity = .54,size_hint_y = None, height = '50dp')
        dim3.add_widget(Button(on_release = lambda x: self.choose('1'),border = [20,20,20,20],markup = True,font_name = font + 'Roboto-Medium.ttf',font_size = '16sp', text = C4 + "Iniciar Session",pos_hint = {'center_x':.5, 'center_y':.5},size_hint_x = None, width = '219dp', background_normal = asset+'NuevoR.png', background_down = asset+'NuevoR.png'))
        dim4 = RelativeLayout(opacity = .54,size_hint_y = None, height = '50dp')
        dim4.add_widget(Button(on_release = lambda x: self.choose('7'),border = [20,20,20,20],markup = True,font_name = font + 'Roboto-Medium.ttf',font_size = '16sp', text = C4 + "Crear Cuenta",pos_hint = {'center_x':.5, 'center_y':.5},size_hint_x = None, width = '219dp', background_normal = asset+'NuevoR.png', background_down = asset+'NuevoR.png'))
        dim5 = GridLayout(rows = 1, size_hint_y = None, height = '50dp')
        dim5.add_widget(Label())
        dim5.add_widget(CheckBox(size_hint_x = None ,width = '50dp'))
        dim5.add_widget(Label(markup = True,opacity = .64,text = C4+'Recordar contraseña.',size_hint_x = None ,width = '150dp'))
        dim5.add_widget(Label())
        
        #screen5_layout.add_widget(dim5)
        screen5_layout.add_widget(Label(size_hint_y = None , height = '25dp'))
        
        
        screen5_layout.add_widget(dim3)
        screen5_layout.add_widget(Label(size_hint_y = None , height = '10dp'))
        screen5_layout.add_widget(dim4)
        screen5_layout.add_widget(Label(size_hint_y = None , height = '25dp'))
        screen5_layout.add_widget(Button(opacity = .64,size_hint_y = None, height = '35dp', text = C4+'Has olvidado tu contraseña?', markup = True, background_normal = color + 'None.png', background_down = color + 'None.png' ))
        screen5_layout.add_widget(Label())

        
class MyApp(App):
    def build(self):
        return InterfaceManager()
 

if __name__ in ('__main__', '__android__'):
    MyApp().run()

    
    
    
    
    