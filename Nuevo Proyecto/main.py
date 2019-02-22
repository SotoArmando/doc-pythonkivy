#!/usr/bin/env python
# -*- coding: utf-8 -*-

import kivy
from kivy.app import App
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.button import Button
import os

#CARPETAS DEL PROYECTO
patch = os.path.dirname(os.path.abspath(__file__))
asset = patch + '/assets/drawable-mdpi/'
color = patch + '/colors/'
font = patch + '/fonts/'

#VARIABLES GLOBALES
Hola = "Hola a todos"



class InterfaceManager(RelativeLayout):#COMPLEMENTO 'PARENT' EL PROYECTO
    def __init__(self, **kwargs):
        super(InterfaceManager, self).__init__(**kwargs)
        #INTERFACE
        button0 = Button()
        self.add_widget(button0)
        #ANIDAR FUNCION A EVENTO
        button0.bind(on_release = lambda x: self.funcion())
        
        '''Toda la documentacion es ta en https://kivy.org/docs/api-kivy.html
        *** Se puede dar el caso de que este desactualizada. para resolver esos problemas
        se puede ir a la carpeta del modulo de kivy y leer las clases de los complementos para
        verificar exactamente que hacen.
        
        --------------------------------------------------------------------------------------
        
        Todos los elementos de los Layout necesariamente no tienen que ser llamados por sus nombres
        pueden ser llamados a travez del mismo Layout dado que son child de este.
        
        Layout.children[0] --> el primer elemento del Layout
        Layout.children[1] --> el segundo elemento del Layout
        Layout.children[2] --> el tercero elemento del Layout
        
        Asimismo se puede llamar a un pariente por su hijo.
        
        Layout.parent                  --> el primer parent del hijo
        Layout.parent.parent           --> el segundo parent del hijo
        Layout.parent.parent.parent    --> el segundo parent del hijo
        
        Yo uso personalmente Experience design para hacer los assets y el prototipo de la aplicacion
        para el frontend.
        
        Kivy no tiene muchos tutoriales que expliquen como trabaja apropiadamente, la comunidad no es muy grande;
        en cualquier caso no dude en enviarme un mail.     ArmandoJoseSoto@Hotmail.com
        '''
      



    #FUNCIONES
    '''todas las funciones alojadas en un evento siempre envian el argumento (self)
    ,las funciones del projecto siempre deben tenerla en el primer parametro.
    '''
    def funcion(self):
        print("hola")

class MyApp(App):
    def build(self):
        return InterfaceManager()
 

if __name__ in ('__main__', '__android__'):
    MyApp().run()

    
    
    
    
    