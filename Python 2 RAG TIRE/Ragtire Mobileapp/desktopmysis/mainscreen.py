#!/usr/bin/env python
# -*- coding: latin-1 -*-

from __init__ import *

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



from administrarinventario import Administrar_Inventario
from administrarentregas import Administrar_Entregas
from agregarvendedor import Agregar_Vendedor
from toppanel import TopPanel            

                    
class MainScreen(RelativeLayout):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        pariente = GridLayout(cols = 1)
        self.sc = ScreenManager()
        self.sc.transition = NoTransition()
        self.Armando = Asistente()
        self.Armando.seturl("http://127.0.0.1:8000/Router")
        self.temp = self.Armando.returntablesdata()
        sc_screen2 = Screen(name = "Administrar Inventario");self.sc.add_widget(sc_screen2)     ;invadmin = Administrar_Inventario(root = self,temp = self.temp)         ;sc_screen2.add_widget(invadmin)
        sc_screen1 = Screen(name = "Agregar Vendedor")      ;self.sc.add_widget(sc_screen1)     ;agregvend = Agregar_Vendedor(root = self,temp = self.temp)              ;sc_screen1.add_widget(agregvend)
        sc_screen3 = Screen(name = "Administrar Entregas")    ;self.sc.add_widget(sc_screen3)   ;entadmin = Administrar_Entregas(root = self,temp = self.temp)           ;sc_screen3.add_widget(entadmin)
        sc_screen4 = Screen(name = "Entregas Completadas")    ;self.sc.add_widget(sc_screen4)

        self.toppanel0 = TopPanel(wsize = kwargs["wsize"], root =self)
        pariente.add_widget(self.toppanel0)
        pariente.add_widget(Image(size_hint_y= None, height = 1,source = color + "3.png", keep_ratio = False , allow_stretch = True))
        pariente.add_widget(self.sc)
        self.add_widget(pariente)
        
    def simplycurrent(self,newcurrent):  self.sc.current = newcurrent
    def data_base_connecttions(self,**kwargs):
        data_connect = self.Armando
        print kwargs["jsondata"]
        data_connect.insertar(kwargs["tableid"],kwargs["jsondata"])
            
class MyApp(App):
    def build(self):
        return Main_Screen()
 

if __name__ in ('__main__', '__android__'):
    MyApp().run()

    
    
    
    
    