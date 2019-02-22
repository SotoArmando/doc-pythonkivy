#!/usr/bin/env python
# -*- coding: utf-8 -*-

import kivy
from kivy.uix.behaviors import FocusBehavior
from kivy.app import App
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
import os
from kivy.core.window import Window
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
#CARPETAS DEL PROYECTO
patch = os.path.dirname(os.path.abspath(__file__))
asset = patch + '/assets/drawable-mdpi/'
color = patch + '/colors/'
font = patch + '/fonts/'

#VARIABLES GLOBALES
Hola = "Hola a todos"
class CustTextInput(TextInput):
    def __init__(self,**kwargs):
        super(CustTextInput, self).__init__(**kwargs)
        self._selected = kwargs["_selected"]
    def golll(self):
        print self._selected 
        
class CustButton(Button):
    def __init__(self,**kwargs):
        super(CustButton, self).__init__(**kwargs)
        self.root = kwargs["M"]
        
    def go(self):
        self.root.selected = self
        y = self.root.selected.__class__.__dict__
        self.root.setproperties(P = y)
    
class Board(RelativeLayout):
    def __init__(self, **kwargs):
        super(Board, self).__init__(**kwargs)
        my_size = (360,640)
        self.widgets = []
        self.active = {}
        self.opened = []
        self.selected_parent = None
        x_parent = Image(source = color + "16.png", keep_ratio = False, allow_stretch = True, opacity = .04, size = (360,640), size_hint = (None,None), pos_hint = {'center_x':.5, 'center_y':.5})
        x = RelativeLayout( size = my_size, size_hint = (None,None), pos_hint = {'center_x':.5, 'center_y':.5})
        self.thex = x
        self.add_widget(x_parent)
        self.add_widget(x)

        self.widgets.append({"self":x,"size": x.size, "pos": (x.x,x.y), "children": []})
        self.active[str(self.thex)] = False
        self.active["Higlight"] = False
            
        print self.widgets
    def check(self,i):
        for x in i.children:
            str = {"self": x,"size": x.size, "pos": (i.x,i.y)}
            self.widgets[str(i)]["children"].append(str)
            
    def getparent(self,x,y):
        
        #print x,y
        for i in self.widgets:
            
            #print (i["pos"][0]), x, (i["pos"][0] + i["size"][0])
            #print (i["pos"][1]), y, (i["pos"][1] + i["size"][1])
            if ((i["self"].pos[0]) < x < (i["self"].pos[0] + i["self"].size[0])) and ((i["self"].pos[1]) < y < (i["self"].pos[1] + i["self"].size[1])): 
                print "dentro " , i["self"]
                self.selected_parent = i["self"]
                if str(i["self"])[0:20] == "<kivy.uix.relativelayout.RelativeLayout object at 0x042340D8>"[0:20]:
                    pass
                else:
                    if self.active["Higlight"] == True:
                        pass
                    else:
                        img = Image(source = color + "5.png",size_hint = (None,None), size = i["self"].size, x = i["self"].x, y = i["self"].y, keep_ratio = False ,allow_stretch = True, opacity = .24)
                        self.opened.append(img)
                        self.thex.add_widget(img)
                        self.active["Higlight"] = True
            else:  
                if self.active["Higlight"] == True:
                    for i in self.opened: i.parent.remove_widget(i)
                    self.opened[:] = []
                    self.active["Higlight"] = False

                    
                    
                
              
        
    
class Properties(RelativeLayout):
    def __init__(self, **kwargs):
        super(Properties, self).__init__(**kwargs)
        self.size_hint_x = .25
        
        pariente = GridLayout(cols = 1)
        for i in range(10): pariente.add_widget(Button())
        self.add_widget(pariente)
        
class Menu(RelativeLayout):
    def __init__(self, **kwargs):
        super(Menu, self).__init__(**kwargs)
        self.size_hint_x = .25
        self.root = kwargs["M"]
        pariente = GridLayout(cols = 1)
        
        comp = [Label, Button, CheckBox, Image]# Slider, ProgressBar, TextInput, Togglebutton, Switch, Video,Anchor Layout, BoxLayout, FloatLayout, GridLayout, PageLayout, RelativeLayout, ScatterLayout, StackLayout,Bubble, DropDownList, FileChooser, Popup, Spinner, List View, TabbedPanel, Video player, VKeyboard,Scatter, Stencil View,ScreenManager]
        
        for i in comp:
            pariente.add_widget(Button(text = str(i), on_release = lambda x: self.transfer(me = i),size_hint_y = None , height = dp(34), always_release = True))
        if i == 9:
            pariente.add_widget(Label())
            
        self.add_widget(pariente)
        
        

 
        
    def cc00(self,x): 
        x.go()
        self.root.selected = x
        
    def transfer(self, **kwargs): 
        
        wid = CustButton(on_release = lambda x: self.cc00(x), M = self.root,size_hint = (None,None), size = (50,50))
        self.root.bb.selected_parent.add_widget(wid)
        self.root.bb.widgets.append({"self":wid,"size": wid.size, "pos": (wid.x,wid.y), "children": []})
        self.root.bb.active[str(wid)] = False
        
      

        self.root.selected = wid
        y = self.root.selected.__class__.__dict__
        for z in y: print z

        self.root.setproperties(P = y)
        
class InterfaceManager(RelativeLayout):#COMPLEMENTO 'PARENT' EL PROYECTO
    def __init__(self, **kwargs):
        super(InterfaceManager, self).__init__(**kwargs)
        self.selected = None
        
        
        
        self.pariente = GridLayout(cols = 1)
        
        self.boards = GridLayout(rows = 1)
        self.pariente.add_widget(self.boards)
        self.boards.add_widget(Menu(M = self))
        self.bb = Board(M = self)
        self.boards.add_widget(self.bb)
        self.pp = Properties(M = self)
        self.boards.add_widget(self.pp)
        
        self.add_widget(self.pariente)
        
        
        from kivy.core.window import Window
        Window.bind(mouse_pos = lambda w, p: self.getpos(p))
        
    def getpos(self,*args):
        #print args[0]
        #print self.bb.thex.to_widget(args[0][0], args[0][1], relative=True)
        x = self.bb.thex.to_widget(args[0][0], args[0][1], relative=True)
        self.bb.getparent(x[0], x[1])
        
    def setproperties(self,**kwargs):
        self.pp.children[0].clear_widgets()
        other = ["x","y","size_hint_x","size_hint_y","pos_hint","height","width"]
        
        for i in other:
            print i
            selected = self.selected
            dim = GridLayout(rows = 1,size_hint_y = None , height = dp(56))
            dim.add_widget(Label(text_size = (100,56-16), halign = 'left', valign = 'middle',text = i))
            print self.bb.thex.children[0]
            textr = CustTextInput(_selected = self.selected, multiline = False,padding = [8,16,0,0],background_normal = color + "3.png",hint_text = i)
            def hola(x):
                print x._selected
                print "hola"

            print 


                
            
            exec("textr.text = str(self.selected."+i+")")
            exec("textr.bind(on_text_validate = lambda x: setattr(x._selected, '"+i+"', x.text))")

            dim.add_widget(textr)
            self.pp.children[0].add_widget(dim)
            
        for i in kwargs["P"]:
                                
            dim = GridLayout(rows = 1,size_hint_y = None , height = dp(56))
            dim.add_widget(Label(text_size = (100,56-16), halign = 'left', valign = 'middle',text = i))
            textr = CustTextInput(_selected = self.selected,multiline = False,padding = [8,16,0,0],background_normal = color + "3.png",hint_text = i)
            exec("textr.text = str(self.selected."+i+")")
            exec("textr.bind(on_text_validate = lambda x: setattr(x._selected, '"+i+"', x.text))")
            dim.add_widget(textr)
            self.pp.children[0].add_widget(dim)

                
        self.pp.children[0].add_widget(Label())
    def contain(self,x,i):
        exec("self.selected."+i+" = x.text")
    def funcion(self):
        print("hola")
		
class MyApp(App):
    def build(self):
        return InterfaceManager()
 

if __name__ in ('__main__', '__android__'):
    MyApp().run()

    

    
    
    