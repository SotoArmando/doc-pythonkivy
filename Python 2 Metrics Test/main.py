#!/usr/bin/env python
# -*- coding: utf-8 -*-

import kivy
from kivy.config import Config
Config.set('graphics','borderless', 1)
Config.set('graphics','position','custom')
Config.set('graphics','window_state','visible')
Config.set('graphics','resizable',0)
Config.set('graphics','left',1000)
Config.set('graphics','top',35)
import threading 
from threading import *
from kivy.effects.opacityscroll import OpacityScrollEffect
from kivy.effects.scroll import ScrollEffect
from kivy.garden.mapview import MapView, MapMarker, MarkerMapLayer, MapSource
from kivy.uix.bubble import Bubble
from kivy.uix.checkbox import CheckBox
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.scatter import Scatter
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.anchorlayout import AnchorLayout
from kivy.properties import ListProperty, StringProperty
from kivy.adapters.simplelistadapter import SimpleListAdapter
from kivy.adapters.listadapter import ListAdapter
from kivy.uix.listview import ListItemButton, ListView, ListItemLabel,CompositeListItem
from kivy.adapters.models import SelectableDataItem
from kivy.graphics import *
from kivy.core.window import Window
from kivy.utils import get_hex_from_color, get_color_from_hex
from kivy.parser import parse_color
from kivy.graphics.instructions import InstructionGroup
from kivy.uix.accordion import Accordion, AccordionItem
from kivy.base import runTouchApp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.popup import Popup
from kivy.uix.image import Image
from kivy.uix.image import AsyncImage
from kivy.core.window import Window
from kivy.uix.dropdown import DropDown
from kivy.animation import Animation
from kivy.uix.widget import Widget
from kivy.uix.stencilview import StencilView
from kivy.metrics import dp
from kivy.clock import Clock
from kivy.properties import (ObjectProperty, NumericProperty, OptionProperty, BooleanProperty, StringProperty)
from kivy.resources import resource_add_path
from kivy.uix.screenmanager import ScreenManager, Screen,SwapTransition, NoTransition,SlideTransition,FadeTransition,WipeTransition,FallOutTransition,RiseInTransition 
from kivy.uix.behaviors import ButtonBehavior
from kivy.lang import Builder
from kivy.garden.mapview import MapView, MapMarker, MarkerMapLayer,MapSource
from kivy.uix.button import Button
from kivy.clock import Clock, mainthread
from kivy.uix.relativelayout import RelativeLayout
from kivy.app import App
from kivy.utils import platform
from kivy.metrics import dp, sp

import requests
import os   
import os.path
import time
import sys
import urllib2
import json, requests
import math
from openpyxl import Workbook
from openpyxl.compat import range
from openpyxl.utils import get_column_letter
from openpyxl import load_workbook
from plyer import gps
from threading import Timer

from submain import NavigationDrawer

reload(sys)
resource_add_path(os.path.dirname(__file__))

Window.size = (dp(360),dp(640))
Window.clearcolor = (1, 1, 1, 1)
#Window.size = (426,100)




C1 = "[color=#000000]"
C2 = "[color=#404040]"
C3 = "[color=#ff3333]"
C4 = "[color=#13C0C7]"

def_textsize = (Window.width-50,50)
patch = os.path.dirname(os.path.abspath(__file__))
hud = patch + '/hud/'
icon = patch + '/icons/'
textb = patch + '/textbox/'
database = patch + '/database/'
color = patch + '/hud/color/'
barra = patch + '/hud/barras/'
fonts = patch + '/fonts/'
medx = Window.width/2
medy = 200/2
wmedy = Window.height/2
wmedx = Window.width/2
if Window.width > Window.height:
    unidad = Window.width/10
else:
    unidad = Window.height/10
    
if platform == "android":

    from jnius import cast
    from jnius import autoclass
    MediaPlayer = autoclass('android.media.MediaPlayer')

else:
    print(platform)
class ImageButton(ButtonBehavior, AsyncImage):
    pass
class InterfaceManager(RelativeLayout):
    def __init__(self, **kwargs):
        
        super(InterfaceManager, self).__init__(**kwargs)
        
        self.dimstate1 = False
        self.Contador_state = -1
        self.Tiempo = float(0)
        self.Grado = float(0.0083333333333333)
        self.Grado1 = float(6)
        self.TimeState = float(0)
        
        self.maingrid = GridLayout(cols = 1)
        self.add_widget(self.maingrid)
        self.maingrid.add_widget(Label(size_hint_y = None))
        self.maingrid.add_widget(self.Topmenu())#.14
        self.maingrid.add_widget(self.Marcador())#.1
        self.maingrid.add_widget(self.MarcadorLetras())#.1
        self.maingrid.add_widget(Label(size_hint_y = .05))#.1
        #self.maingriddim
        self.maingriddim = GridLayout(rows = 1, size_hint_y = .1, height = unidad)#
        x = self.MarcadorBotones()
        
        self.maingriddim.add_widget(Label())
        for i in x:
            self.maingriddim.add_widget(i)
        self.maingriddim.add_widget(Label())
        
        self.maingrid.add_widget(self.maingriddim)#.06
        self.maingrid.add_widget(self.Marcadores())
        #self.ControlesScreen
        x = self.ControlesScreen()
        self.add_widget(x[0])
        self.add_widget(x[1])
        self.maingrid.add_widget(Label(size_hint_y = None))
        
        
        
        
    def Topmenu(self):
        
        image_size = unidad 
        choose = ScrollView(bar_margin = 0,size_hint_y = None,height = '100dp' ,do_scroll_y = False, do_scroll_x = True ,scroll_x = 0.5,bar_color = [0,0,0,.6],bar_inactive_color = [.7,.7,.7,.2],bar_width = 3, bar_pos_x = "top")
        chooseroot_root = RelativeLayout(size_hint_y = 1, size_hint_x = None, width = (unidad * 15) + ((wmedx-unidad)*2)+45)
        chooseroot = GridLayout(rows = 1, size_hint_y = 1, size_hint_x = 1, spacing = 5)
        chooseroot_root.add_widget(chooseroot)
        choose.add_widget(chooseroot_root)
        self.medio = Image(source = icon + "clock.png", size_hint = (None,None), size = ('24dp','24dp'), pos = (0,100-30))
        chooseroot_root.add_widget(self.medio)
    
        imgset = ["bacon","bread","coffeex","fried-egg","meat","toaster","tea","teapot","pizza","shrimp"]
        
        for i in range(10):  
            if i == 0:
                chooseroot.add_widget(Image(source = hud+"None.png",allow_stretch = True, keep_ratio = False,size_hint_x = None, width = (wmedx-unidad)))
                

            
            self.container = GridLayout(cols = 1, size_hint = (1,1))
            size1 = (Window.height * .2) /2
            size2 = (Window.height * .1) /2
            
            image = ImageButton(source = icon +imgset[i]+".png",size_hint = (None,None),width = '64dp', allow_stretch = True,  keep_ratio = True)
            
            self.imagescatter = Scatter(scale = 1,do_translation_y=False,do_translation_x=False,source = icon +imgset[i],size_hint = (1,1) , allow_stretch = True,  keep_ratio = True)
            
            image.bind(on_press =lambda x: self.Animatesize(x.parent))
            self.imagescatter.add_widget(image)
            self.container.add_widget(self.imagescatter)
            chooseroot.add_widget(self.container)
            
            if i == 9:
                chooseroot.add_widget(Image(source = hud+"None.png",allow_stretch = True, keep_ratio = False,size_hint_x = None, width = '64dp'))
                
        return choose 
        
    def MarcadorLetras(self):
        self.TiempoTxt = Button(markup = True,font_size = '20sp',halign = "center",text = C1+"Comienza a Cocinar :D !",background_normal = hud+"None.png",background_down = hud+"None.png", allow_stretch = True, keep_ratio = False,size_hint_y = .1)
        
        return self.TiempoTxt
        
    def Marcador(self):
        self.Diseno_Text = GridLayout(cols = 10, size_hint_y = .2 )
        Letras = ["0","0",":","0","0",":","0","0"]
        self.Diseno_Text.add_widget(Label())
        
        self.Botones = []
        for i in Letras:  
            ButtonX = Button(size_hint_x = 1,font_size = '65dp',markup = True,text = C1+i,background_normal = hud +"None2.png")
            self.Diseno_Text.add_widget(ButtonX)
            self.Botones.append(ButtonX)
        self.Diseno_Text.add_widget(Label())

        return self.Diseno_Text

        
    def MarcadorBotones(self):
        
        Button5 = Button(background_normal = hud+"hud15.png",background_down = hud+"hud15.png", size_hint = (1,1) , height = sp(sp(64)),width = sp(sp(64)))
        Button6 = Button(background_normal = hud+"hud14.png",background_down = hud+"hud14.png", size_hint = (1,1), height = sp(sp(64)), width = sp(sp(64)))
        Button7 = Button(background_normal = hud+"hud16.png",background_down = hud+"hud16.png", size_hint = (1,1) , height = sp(sp(64)), width = sp(sp(64)))
        
        Button5.bind(on_release = lambda x: self.activar_state())
        Button6.bind(on_release = lambda x: self.ReiniciarTiempo(x))
        Button7.bind(on_release = lambda x: self.ReducirTiempo(self.Tiempo))
        
        Button5_container = GridLayout(cols = 1 , size_hint = (1,1))
        Button6_container = GridLayout(cols = 1 , size_hint = (1,1))
        Button7_container = GridLayout(cols = 1 , size_hint = (1,1))
        
        Button5_Scatter = Scatter(background_normal = hud+"hud15.png",background_down = hud+"hud15.png", size_hint = (1,1))
        Button6_Scatter = Scatter(background_normal = hud+"hud14.png",background_down = hud+"hud14.png", size_hint = (1,1))
        Button7_Scatter = Scatter(background_normal = hud+"hud16.png",background_down = hud+"hud16.png", size_hint = (1,1))
        
        Button5_Scatter.add_widget(Button5)
        Button6_Scatter.add_widget(Button6)
        Button7_Scatter.add_widget(Button7)
        
        Button5_container.add_widget(Button5_Scatter)
        Button6_container.add_widget(Button6_Scatter)
        Button7_container.add_widget(Button7_Scatter)
 
        trio = [Button5_container,Button6_container,Button7_container] 
        
        Button5.bind(on_press =lambda x: self.Animatesize(x.parent))
        Button6.bind(on_press =lambda x: self.Animatesize(x.parent))
        Button7.bind(on_press =lambda x: self.Animatesize(x.parent))
        return trio
       
       
    def CalcularTiempo(self,In):

        hud = patch + '/hud/'
        icon = patch + '/icon/'
        fonts = patch + '/fonts/'
        
        C1 = "[color=#000000]"
        #In = [2,30,59]
        #tiempo = float((In[0]*216000)+(In[1]*3600)+(In[2]*60))
        
        segundos = (((self.Tiempo/60))%1)*60
        minutos = ((((self.Tiempo/60))/60)%1)*60
        horas = (((((self.Tiempo/60))/60)/60)%1)*60

        print ("Calculando" + str(self.Tiempo) + " segundos...")
        if self.dimstate1 == True:
            self.dimstate1 = False
            pass
        else:
            if self.Tiempo == 0: self.Activar()

            
        
        if segundos< 10:
            segundos = "0"+ str(segundos)[:-2]
        else:
            segundos = str(segundos)[:-2]
            
        if minutos< 10:
            minutos = "0"+ str(int(minutos))
        else:
            minutos = str(int(minutos))

        if horas < 10:
            horas = "0"+ str(int(horas))
        else:
            horas = str(int(horas))
            
        a = -1*(self.Grado*self.Tiempo)
        b = -1*(self.Grado1*self.Tiempo)
        TimeVar = (str(horas)+":"+str(minutos)+":"+str(segundos))

        #self.Tiempo_text2.text= (C1+str(horas)+":"+str(minutos)+":"+str(segundos))
        self.TiempoTxt.text = (C1+str(horas)+" Horas "+str(minutos)+" Minutos y "+str(segundos))+" segundos"
        print TimeVar
        cc = 0
        for i in TimeVar: 
            self.Botones[cc].text = C1+i
            cc += 1
        print horas
        print minutos
        print segundos
        
                
    def AumentarTiempo(self,Plus,button):
        self.Animatesize(button.parent)
        self.Tiempo += Plus
        self.CalcularTiempo(1)
        self.TimeState = self.Tiempo
        
      
    def ReiniciarTiempo(self,button):
        #self.Animatesize(button.parent)
        self.Tiempo = self.TimeState
        self.CalcularTiempo(1)
        if self.Contador_state == 1: self.Contador_state *= -1
        
        
    def Animatesize(self,button):

        print button.parent.pos

        
        anim3 = Animation(x = button.parent.pos[0], d = .75, t = "in_out_back")
        anim3.start(self.medio)
        button.scale = 1.0
        anim1 = Animation(scale = 1.5, d = .05,t = "in_circ")
        anim2 = Animation(scale = 1.0, d = .15,t = "out_circ")
        anim = anim1 + anim2
        anim.start(button)

        
    def ReducirTiempo(self,Plus):
    
        C1 = "[color=#000000]"
        if Plus == self.Tiempo:
            self.dimstate1 = True
        self.Tiempo -= Plus
        self.CalcularTiempo(1)
        if self.Contador_state == 1: self.Contador_state *= -1
        
        threading.Timer(1, self.activar_contar).cancel()
        Letras = ["0","0",":","0","0",":","0","0"]
        for i in self.Botones:
            i.text = C1+Letras[self.Botones.index(i)]
    
    
    def activar_contar(self):
        
        if self.Tiempo == 0:
            pass
            if self.Contador_state == -1: threading.Timer(1, self.activar_contar).cancel()
        else:
            if self.Contador_state == 1: 
                threading.Timer(1, self.activar_contar).start()
                self.contar()
                self.CalcularTiempo(1)
                
           
    def activar_state(self):
        if self.Contador_state == 1:
            pass
        else:
            self.Contador_state *= -1
            self.activar_contar()
            print self.Contador_state
  
  
    def contar(self):  
        self.Tiempo -= 1
        self.CalcularTiempo(1)


    def Activar(self):
        C1 = "[color=#000000]"  
        mPlayer = MediaPlayer()
        mPlayer.setDataSource(self.patch + '\sounds\default.wav')
        mPlayer.prepare()
        self.mPlayer.start()
      

    def Marcadores(self):
    
        pantalla1_grid1 = GridLayout(cols = 1)
        pantalla1_relat1 = RelativeLayout(cols = 1, size_hint = (1,1))
        pantalla1_grid1_dim1 = GridLayout(cols = 7, size_hint = (1,1))
        pantalla1_grid1_dim2 = GridLayout(cols = 7, size_hint = (1,1))
        pantalla1_grid1_dim3 = GridLayout(cols = 7, size_hint = (1,1))
        self.pantalla1_grid1_dim1_root = Screen(name = "a",cols = 7, size_hint = (1,1))
        self.pantalla1_grid1_dim1_root2 = Screen(name = "b",cols = 7, size_hint = (1,1))
        self.pantalla1_grid1_dim1_root3 = Screen(name = "c",cols = 7, size_hint = (1,1))
        self.pantalla1_grid1_dim1_root_screen = ScreenManager(cols = 7, size_hint = (1,.2))
        self.pantalla1_grid1_dim1_root_screen.add_widget(self.pantalla1_grid1_dim1_root)
        self.pantalla1_grid1_dim1_root_screen.add_widget(self.pantalla1_grid1_dim1_root2)
        self.pantalla1_grid1_dim1_root_screen.add_widget(self.pantalla1_grid1_dim1_root3)
        
        self.pantalla1_grid1_dim1_root.add_widget(pantalla1_grid1_dim1)
        self.pantalla1_grid1_dim1_root2.add_widget(pantalla1_grid1_dim2)
        self.pantalla1_grid1_dim1_root3.add_widget(pantalla1_grid1_dim3)
        for i in range(2):
            img = ["b3","b3","b3"]
            if i == 1:
                T1="30 S"
                T2="1 M"
                T3="3 M"
            else:
                T1=""
                T2=""
                T3=""
            if i == 0:    
                pantalla1_grid1_dim1.add_widget(Image(source = hud+"None.png",allow_stretch = True,keep_ratio = False))
                Button5 = Button(size_hint = (1,1), size = (sp(64),sp(20.0)),background_normal = hud+img[i]+".png", text = C1+T1,markup = True, font_size = sp(23))
                Button5.bind(on_release = lambda x: self.AumentarTiempo(float(30.0),x))
                pantalla1_grid1_dim1.add_widget(Button5)
                
                pantalla1_grid1_dim1.add_widget(Image(source = hud+"None.png",allow_stretch = True,keep_ratio = False))
                Button6 = Button(size_hint = (1,1), size = (sp(64),sp(20.0)),background_normal = hud+img[i]+".png", text = C1+T2,markup = True, font_size = sp(23))
                Button6.bind(on_release = lambda x: self.AumentarTiempo(float(60.0),x))
                pantalla1_grid1_dim1.add_widget(Button6)
                
                pantalla1_grid1_dim1.add_widget(Image(source = hud+"None.png",allow_stretch = True,keep_ratio = False))
                Button7 =  Button(size_hint = (1,1), size = (sp(64),sp(20.0)),background_normal = hud+img[i]+".png", text = C1+T3,markup = True, font_size = sp(23))
                Button7.bind(on_release = lambda x: self.AumentarTiempo(float(180.0),x))
                pantalla1_grid1_dim1.add_widget(Button7)
                
                pantalla1_grid1_dim1.add_widget(Image(source = hud+"None.png",allow_stretch = True,keep_ratio = False))
            else:
                print i
                pantalla1_grid1_dim1.add_widget(ImageButton(source = hud+"None.png",allow_stretch = True,keep_ratio = False))
                Button5 = Button(size_hint = (1,1), size = (sp(64),sp(64)),background_normal = hud+img[i]+".png",background_down = hud+img[i]+".png", text = C1+T1,markup = True, font_size = 30)
                Button5_Scatter = Scatter(size_hint = (1,1), size = (sp(64),sp(64)),background_normal = hud+img[i]+".png",background_down = hud+img[i]+".png", text = C1+T1,markup = True, font_size = 30)
                Button5_Grid = GridLayout(cols = 1 , size_hint = (1,1), size = (sp(64),sp(64)),background_normal = hud+img[i]+".png",background_down = hud+img[i]+".png", text = C1+T1,markup = True, font_size = 30)
                Button5_Scatter.add_widget(Button5)
                Button5_Grid.add_widget(Button5_Scatter)
                Button5.bind(on_release = lambda x: self.AumentarTiempo(float(30.0),x))
                pantalla1_grid1_dim1.add_widget(Button5_Grid)
                
                pantalla1_grid1_dim1.add_widget(Image(source = hud+"None.png",allow_stretch = True,keep_ratio = False))
                Button6 = Button(size_hint = (1,1), size = (sp(64),sp(64)),background_normal = hud+img[i]+".png",background_down = hud+img[i]+".png", text =  C1+T2,markup = True, font_size = 30)
                Button6_Scatter = Scatter(size_hint = (1,1), size = (sp(64),sp(64)),background_normal = hud+img[i]+".png",background_down = hud+img[i]+".png", text =  C1+T2,markup = True, font_size = 30)
                Button6_Grid = GridLayout(cols = 1,size_hint = (1,1), size = (sp(64),sp(64)),background_normal = hud+img[i]+".png",background_down = hud+img[i]+".png", text =  C1+T2,markup = True, font_size = 30)
                Button6_Scatter.add_widget(Button6)
                Button6_Grid.add_widget(Button6_Scatter)
                Button6.bind(on_release = lambda x: self.AumentarTiempo(float(60.0),x))
                pantalla1_grid1_dim1.add_widget(Button6_Grid)
                
                pantalla1_grid1_dim1.add_widget(Image(source = hud+"None.png",allow_stretch = True,keep_ratio = False))
                Button7 =  Button(size_hint = (1,1), size = (sp(64),sp(64)),background_normal = hud+img[i]+".png",background_down = hud+img[i]+".png", text = C1+T3,markup = True, font_size = 30)
                Button7_Scatter = Scatter(size_hint = (1,1), size = (sp(64),sp(64)),background_normal = hud+img[i]+".png",background_down = hud+img[i]+".png", text = C1+T1,markup = True, font_size = 30)
                Button7_Grid = GridLayout(cols = 1 , size_hint = (1,1), size = (sp(64),sp(64)),background_normal = hud+img[i]+".png",background_down = hud+img[i]+".png", text = C1+T3,markup = True, font_size = 30)
                Button7_Scatter.add_widget(Button7)
                Button7_Grid.add_widget(Button7_Scatter)
                Button7.bind(on_release = lambda x: self.AumentarTiempo(float(180.0),x))
                pantalla1_grid1_dim1.add_widget(Button7_Grid)
                
                pantalla1_grid1_dim1.add_widget(ImageButton(source = hud+"None.png",allow_stretch = True,keep_ratio = True))

        for i in range(2):
            img = ["b3","b3","b3"]
            if i == 1:
                T1="3 M"
                T2="5 M"
                T3="15 M"
            else:
                T1=""
                T2=""
                T3=""
            if i == 0:    
                pantalla1_grid1_dim2.add_widget(Image(source = hud+"None.png",allow_stretch = True,keep_ratio = False))
                Button5 = Button(size_hint = (1,1), size = (sp(64),sp(20.0)),background_normal = hud+img[i]+".png", text = C1+T1,markup = True, font_size = sp(23))
                Button5.bind(on_release = lambda x: self.AumentarTiempo(float(180.0),x))
                pantalla1_grid1_dim2.add_widget(Button5)
                
                pantalla1_grid1_dim2.add_widget(Image(source = hud+"None.png",allow_stretch = True,keep_ratio = False))
                Button6 = Button(size_hint = (1,1), size = (sp(64),sp(20.0)),background_normal = hud+img[i]+".png", text = C1+T2,markup = True, font_size = sp(23))
                Button6.bind(on_release = lambda x: self.AumentarTiempo(float(300.0),x))
                pantalla1_grid1_dim2.add_widget(Button6)
                
                pantalla1_grid1_dim2.add_widget(Image(source = hud+"None.png",allow_stretch = True,keep_ratio = False))
                Button7 =  Button(size_hint = (1,1), size = (sp(64),sp(20.0)),background_normal = hud+img[i]+".png", text = C1+T3,markup = True, font_size = sp(23))
                Button7.bind(on_release = lambda x: self.AumentarTiempo(float(900.0),x))
                pantalla1_grid1_dim2.add_widget(Button7)
                
                pantalla1_grid1_dim2.add_widget(Image(source = hud+"None.png",allow_stretch = True,keep_ratio = False))
            else:
                print i
                pantalla1_grid1_dim2.add_widget(ImageButton(source = hud+"None.png",allow_stretch = True,keep_ratio = False))
                Button5 = Button(size_hint = (1,1), size = (sp(64),sp(64)),background_normal = hud+img[i]+".png",background_down = hud+img[i]+".png", text = C1+T1,markup = True, font_size = 30)
                Button5_Scatter = Scatter(size_hint = (1,1), size = (sp(64),sp(64)),background_normal = hud+img[i]+".png",background_down = hud+img[i]+".png", text = C1+T1,markup = True, font_size = 30)
                Button5_Grid = GridLayout(cols = 1 , size_hint = (1,1), size = (sp(64),sp(64)),background_normal = hud+img[i]+".png",background_down = hud+img[i]+".png", text = C1+T1,markup = True, font_size = 30)
                Button5_Scatter.add_widget(Button5)
                Button5_Grid.add_widget(Button5_Scatter)
                Button5.bind(on_release = lambda x: self.AumentarTiempo(float(180.0),x))
                pantalla1_grid1_dim2.add_widget(Button5_Grid)
                
                pantalla1_grid1_dim2.add_widget(Image(source = hud+"None.png",allow_stretch = True,keep_ratio = False))
                Button6 = Button(size_hint = (1,1), size = (sp(64),sp(64)),background_normal = hud+img[i]+".png",background_down = hud+img[i]+".png", text =  C1+T2,markup = True, font_size = 30)
                Button6_Scatter = Scatter(size_hint = (1,1), size = (sp(64),sp(64)),background_normal = hud+img[i]+".png",background_down = hud+img[i]+".png", text =  C1+T2,markup = True, font_size = 30)
                Button6_Grid = GridLayout(cols = 1,size_hint = (1,1), size = (sp(64),sp(64)),background_normal = hud+img[i]+".png",background_down = hud+img[i]+".png", text =  C1+T2,markup = True, font_size = 30)
                Button6_Scatter.add_widget(Button6)
                Button6_Grid.add_widget(Button6_Scatter)
                Button6.bind(on_release = lambda x: self.AumentarTiempo(float(300.0),x))
                pantalla1_grid1_dim2.add_widget(Button6_Grid)
                
                pantalla1_grid1_dim2.add_widget(Image(source = hud+"None.png",allow_stretch = True,keep_ratio = False))
                Button7 =  Button(size_hint = (1,1), size = (sp(64),sp(64)),background_normal = hud+img[i]+".png",background_down = hud+img[i]+".png", text = C1+T3,markup = True, font_size = 30)
                Button7_Scatter = Scatter(size_hint = (1,1), size = (sp(64),sp(64)),background_normal = hud+img[i]+".png",background_down = hud+img[i]+".png", text = C1+T1,markup = True, font_size = 30)
                Button7_Grid = GridLayout(cols = 1 , size_hint = (1,1), size = (sp(64),sp(64)),background_normal = hud+img[i]+".png",background_down = hud+img[i]+".png", text = C1+T3,markup = True, font_size = 30)
                Button7_Scatter.add_widget(Button7)
                Button7_Grid.add_widget(Button7_Scatter)
                Button7.bind(on_release = lambda x: self.AumentarTiempo(float(900.0),x))
                pantalla1_grid1_dim2.add_widget(Button7_Grid)
                
                pantalla1_grid1_dim2.add_widget(ImageButton(source = hud+"None.png",allow_stretch = True,keep_ratio = True))

        for i in range(2):
            img = ["b3","b3","b3"]
            if i == 1:
                T1="15 M"
                T2="30 M"
                T3="1 H"
            else:
                T1=""
                T2=""
                T3=""
            if i == 0:    
                pantalla1_grid1_dim3.add_widget(Image(source = hud+"None.png",allow_stretch = True,keep_ratio = False))
                Button5 = Button(size_hint = (1,1), size = (sp(sp(64)),sp(20.0)),background_normal = hud+img[i]+".png", text = C1+T1,markup = True, font_size = sp(23))
                Button5.bind(on_release = lambda x: self.AumentarTiempo(float(900.0),x))
                pantalla1_grid1_dim3.add_widget(Button5)
                
                pantalla1_grid1_dim3.add_widget(Image(source = hud+"None.png",allow_stretch = True,keep_ratio = False))
                Button6 = Button(size_hint = (1,1), size = (sp(sp(64)),sp(20.0)),background_normal = hud+img[i]+".png", text = C1+T2,markup = True, font_size = sp(23))
                Button6.bind(on_release = lambda x: self.AumentarTiempo(float(1800.0),x))
                pantalla1_grid1_dim3.add_widget(Button6)
                
                pantalla1_grid1_dim3.add_widget(Image(source = hud+"None.png",allow_stretch = True,keep_ratio = False))
                Button7 =  Button(size_hint = (1,1), size = (sp(sp(64)),sp(20.0)),background_normal = hud+img[i]+".png", text = C1+T3,markup = True, font_size = sp(23))
                Button7.bind(on_release = lambda x: self.AumentarTiempo(float(3600.0),x))
                pantalla1_grid1_dim3.add_widget(Button7)
                
                pantalla1_grid1_dim3.add_widget(Image(source = hud+"None.png",allow_stretch = True,keep_ratio = False))
            else:
                print i
                pantalla1_grid1_dim3.add_widget(ImageButton(source = hud+"None.png",allow_stretch = True,keep_ratio = False))
                Button5 = Button(size_hint = (1,1), size = (sp(sp(64)),sp(sp(64))),background_normal = hud+img[i]+".png",background_down = hud+img[i]+".png", text = C1+T1,markup = True, font_size = sp(30))
                Button5_Scatter = Scatter(size_hint = (1,1), size = (sp(sp(64)),sp(sp(64))),background_normal = hud+img[i]+".png",background_down = hud+img[i]+".png", text = C1+T1,markup = True, font_size = 30)
                Button5_Grid = GridLayout(cols = 1 , size_hint = (1,1), size = (sp(sp(64)),sp(sp(64))),background_normal = hud+img[i]+".png",background_down = hud+img[i]+".png", text = C1+T1,markup = True, font_size = sp(30))
                Button5_Scatter.add_widget(Button5)
                Button5_Grid.add_widget(Button5_Scatter)
                Button5.bind(on_release = lambda x: self.AumentarTiempo(float(900.0),x))
                pantalla1_grid1_dim3.add_widget(Button5_Grid)
                
                pantalla1_grid1_dim3.add_widget(Image(source = hud+"None.png",allow_stretch = True,keep_ratio = False))
                Button6 = Button(size_hint = (1,1), size = (sp(sp(64)),sp(sp(64))),background_normal = hud+img[i]+".png",background_down = hud+img[i]+".png", text =  C1+T2,markup = True, font_size = sp(30))
                Button6_Scatter = Scatter(size_hint = (1,1), size = (sp(sp(64)),sp(sp(64))),background_normal = hud+img[i]+".png",background_down = hud+img[i]+".png", text =  C1+T2,markup = True, font_size = sp(30))
                Button6_Grid = GridLayout(cols = 1,size_hint = (1,1), size = (sp(sp(64)),sp(sp(64))),background_normal = hud+img[i]+".png",background_down = hud+img[i]+".png", text =  C1+T2,markup = True, font_size = sp(30))
                Button6_Scatter.add_widget(Button6)
                Button6_Grid.add_widget(Button6_Scatter)
                Button6.bind(on_release = lambda x: self.AumentarTiempo(float(1800.0),x))
                pantalla1_grid1_dim3.add_widget(Button6_Grid)
                
                pantalla1_grid1_dim3.add_widget(Image(source = hud+"None.png",allow_stretch = True,keep_ratio = False))
                Button7 =  Button(size_hint = (1,1), size = (sp(sp(64)),sp(sp(64))),background_normal = hud+img[i]+".png",background_down = hud+img[i]+".png", text = C1+T3,markup = True, font_size = 30)
                Button7_Scatter = Scatter(size_hint = (1,1), size = (sp(sp(64)),sp(sp(64))),background_normal = hud+img[i]+".png",background_down = hud+img[i]+".png", text = C1+T1,markup = True, font_size = sp(30))
                Button7_Grid = GridLayout(cols = 1 , size_hint = (1,1), size = (sp(sp(64)),sp(sp(64))),background_normal = hud+img[i]+".png",background_down = hud+img[i]+".png", text = C1+T3,markup = True, font_size = 30)
                Button7_Scatter.add_widget(Button7)
                Button7_Grid.add_widget(Button7_Scatter)
                Button7.bind(on_release = lambda x: self.AumentarTiempo(float(3600.0),x))
                pantalla1_grid1_dim3.add_widget(Button7_Grid)
                
                pantalla1_grid1_dim3.add_widget(ImageButton(source = hud+"None.png",allow_stretch = True,keep_ratio = True))
        return self.pantalla1_grid1_dim1_root_screen

        
    def next(self,button):
        print (self.pantalla1_grid1_dim1_root_screen.next())
        self.pantalla1_grid1_dim1_root_screen.transition = transition = SlideTransition(direction ="left")
        self.pantalla1_grid1_dim1_root_screen.current = self.pantalla1_grid1_dim1_root_screen.next()
        
        
    def previous(self,button):
        print (self.pantalla1_grid1_dim1_root_screen.previous())
        self.pantalla1_grid1_dim1_root_screen.transition = transition = SlideTransition(direction ="right")
        self.pantalla1_grid1_dim1_root_screen.current = self.pantalla1_grid1_dim1_root_screen.previous()
        
        
    def ControlesScreen(self):
        self.Button1 = Button(size_hint = (None,None), size = ('64sp','64sp'), pos = (0,wmedy-32-60), background_normal = hud+"hud11.png", background_down = hud+"hud11.png",markup = True , text = C1+"",font_size = 72 , font_name = fonts+"FiraSans-Light")
        self.Button2 = Button(size_hint = (None,None), size = ('64sp','64sp'), pos = (Window.width-64,wmedy-32-60), background_normal = hud+"hud12.png", background_down = hud+"hud12.png",markup = True , text = C1+"",font_size = 72, font_name = fonts+"FiraSans-Light")
        self.Button2.bind(on_release  = lambda x: self.next("Lobby2"))
        self.Button1.bind(on_release  = lambda x: self.previous("Lobby"))
        duo = [self.Button1,self.Button2]
        return duo
        
class MyApp(App):
    def build(self):
        return InterfaceManager()
 

if __name__ in ('__main__', '__android__'):
    MyApp().run()

    
    
    
    
    