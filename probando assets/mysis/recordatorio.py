#!/usr/bin/env python
# -*- coding: latin-1 -*-

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




resource_add_path(os.path.dirname(__file__))

from kivy.uix.behaviors import ButtonBehavior
from kivy.animation import Animation
from kivy.uix.widget import Widget
from kivy.uix.stencilview import StencilView
from kivy.metrics import dp
from kivy.clock import Clock
from entregas import Entregas_Item
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
kv = '''
<MyButton>:
    size_hint: None, 1
    size: self.texture_size
'''
Builder.load_string(kv)
class ImageButton(ButtonBehavior, Image): pass
from calendario import Calendar       
class Recordatorio(Screen):
    def __init__(self, **kwargs):
        super(Recordatorio, self).__init__(**kwargs)
        pariente = GridLayout(cols = 1,size_hint_y = None, height = 500)
        open_filtros = Button(on_release = lambda x: self.openfilter1(x),markup = True, text = C4+"[b]Criterios",font_size = dp(18), background_normal = color + '16.png', background_down = color + '16.png',valign = 'middle',text_size = (Window.width - dp(25),dp(56)), size_hint_y = None, height = dp(56))
        self.temp = kwargs["temp"]
        self.eroot = kwargs["e"]
        self.lay = GridLayout(cols = 1, size_hint_y = None , height = dp(56))
        self.lay_dim = GridLayout(cols = 2, opacity = 0.)
        self.lay.add_widget(open_filtros)
        self.lay.add_widget(self.lay_dim)
        self.root = kwargs["root"]
        for i in self.temp[0][1]:
            newwidget = ToggleButton(background_normal = color +"16.png",markup = True,group = "Account_Receivable", text =C4+i,valign = 'middle',text_size = (Window.width/2 -dp(25), dp(36)), font_size = 16)
            newwidget.bind(on_press = lambda x: self.root.set_FiltrarCampo(0,x.text[len(C4):]))
            self.lay_dim.add_widget(newwidget)
            
        dim1 = RelativeLayout(size_hint_y = None, height = 52)
        dim1.add_widget(Image(source = color+"16.png", allow_stretch = True , keep_ratio = False))
        
        dim1b = GridLayout(rows = 1 , size_hint_y = None , height = 50)
        dim1b.add_widget(Label(size_hint_x = None, width = ((Window.width-382)/2)))
        
        dim1b.add_widget(Button(border = [0,0,0,0],background_normal = asset+"1.png",background_down = asset+"1.png",size_hint_x = None, width = 64))
        textwidget = TextInput(multiline=False,size_hint_x = None, width =254,font_size = 16, hint_text = "Buscar Entrega",padding = [0,dp(18),0,0],background_normal = asset+"2.png",background_active = asset+"2.png")
        textwidget.bind(on_text_validate = lambda x: self.Filtrar(0,x.text))
        dim1b.add_widget(textwidget)
        dim1b.add_widget(Button(border = [0,0,0,0],background_normal = asset+"3.png",background_down = asset+"3.png",size_hint_x = None, width = 64))
        
        image1_parent = RelativeLayout(cols = 1, size_hint = (None,None), size = (50,50))
        dim1b.add_widget(image1_parent)
        dim1b.add_widget(Label(size_hint_x = None, width = ((Window.width-382)/2)))
        
        dim1.add_widget(Image(pos_hint = {'y': 1},opacity = .12,source = color + "3.png", keep_ratio = False , allow_stretch = True, size_hint_y = None, height = dp(1)))
        dim1.add_widget(dim1b)
        dim1.add_widget(Image(source = color + "3.png",opacity = .12, keep_ratio = False , allow_stretch = True, size_hint_y = None, height = dp(1)))
        
        
        pariente.add_widget(Image(size_hint_y = None, height = 71,opacity = 1, source =color+ "16.png", keep_ratio = False , allow_stretch = True))
        pariente.add_widget(Button(background_normal = color + "16.png",text = C4+"Recordatorio",text_size = (Window.width - 50 , dp(50)),valign = 'middle', halign = 'left',size_hint_y = None , height = '50dp', markup = True, font_size = '24sp')) 
        relat1 = RelativeLayout(size_hint_y = None, height = 100)
        relat1.add_widget(Image(size_hint_y = 1,opacity = 1, source =color+ "16.png", keep_ratio = False , allow_stretch = True))
        relat1.add_widget(SizeButton(background_normal = "None",text = C4+"A continuacion se muestran las diligencias restantes, puede encargarlas presionandolas y seleccionando la opcion 'Encargar Pedido'",pos_hint = {'center_x':.5, 'center_y':.5},text_size = (Window.width *.75 , 100),valign = 'middle', halign = 'center',size_hint_y = None , height = '50dp', markup = True))
        pariente.add_widget(relat1)
        pariente.add_widget(dim1)
        pariente.add_widget(self.lay)
        pariente.add_widget(Calendar())
        self.anid = GridLayout(cols = 1,  size_hint_y = None, height = 0)
        self.datos_parent = self.anid
        for i in self.temp[0][0]:
            
            if (i["estado_entrega"] == "Sin entregar") or (i["estado_entrega"] == "Vencida"):
                self.anid.add_widget(Entregas_Item(managing = ScreenManager(),temp = self.temp, item = i))
            else:
                pass

        for i in self.anid.children:
            self.anid.height += i.height
            pariente.height += i.height
        pariente.add_widget(self.anid)
        self.add_widget(Image(source = color + "16.png", keep_ratio = False, allow_stretch = True))
        scroll = ScrollView()
        scroll.add_widget(pariente)
        self.add_widget(scroll)
    def Filtrar(self, Tabla, Valor):
        def calcular_suma(val1):
            calcx = 0
            for dim in self.temp[0][0]:
                if val1 == dim["cliente"]:
                    calcx += float(dim["balance_original"])
            return str(calcx)
        try:
            print self.root.tablasfilter[Tabla]
            datos = self.root.Armando.filtrar(Tabla,self.root.tablasfilter[Tabla],Valor)

            def managinx(x,y):
                print x,y
                self.root.screen5sc.current = y
            self.datos_parent.clear_widgets() 
            for i in datos:
                if Tabla == 0:
                    if i["estado_entrega"][0] == "S":
                        item_x = Entregas_Item(opacity = 0,temp = self.temp,managing = self.eroot.set_current, item = i)
                        self.datos_parent.add_widget(item_x)
                        self.datos_parent.height += 324
                        a = Animation(opacity = 1, d = .5, t = 'out_quart')
                        a.start(item_x)
                    else:
                        item_x = Entregas_Item(opacity = 0,temp = self.temp,managing = self.eroot.set_current, item = i)
                        self.datos_parent.add_widget(item_x)
                        self.datos_parent.height += 324
                        a = Animation(opacity = 1, d = .5, t = 'out_quart')
                        a.start(item_x)

                else:
                    pass
        except:
            import traceback
            traceback.print_exc()
    
        
    def openfilter1(self,object):
        print "hola"
        print object.parent.height
        if object.parent.height == dp(56):
            anim1 = Animation(height = dp(300), d = .225 , t = 'out_expo')
            anim2 = Animation(opacity = 1, d = .225 , t = 'out_expo')
            anim1.start(object.parent)
            anim2.start(object.parent.children[0])
        elif object.parent.height == dp(300):
            anim1 = Animation(height = dp(56), d = .225 , t = 'out_expo')
            anim2 = Animation(opacity = 0, d = .225 , t = 'out_expo')
            anim1.start(object.parent)
            anim2.start(object.parent.children[0])
class RecordatorioItem(RelativeLayout):
    def __init__(self, **kwargs):
        super(RecordatorioItem, self).__init__(**kwargs)
        self.size_hint_y = None
        self.height = 100
        self.opened = []
        self.add_widget(Image(size_hint = (.9,.9), pos_hint = {'center_x':.5, 'center_y':.5},source = color+"16.png", keep_ratio = False, allow_stretch = True))
        self.add_widget(Image(size_hint = (.9,.9), pos_hint = {'center_x':.5, 'center_y':.5},opacity = .94,source = color+"8.png", keep_ratio = False, allow_stretch = True))
        self.add_widget(Image(size_hint = (.9,None),pos_hint = {'y':.05,'center_x':.5}, height = dp(1),opacity = .44,source = color+"3.png", keep_ratio = False, allow_stretch = True))
        pariente = GridLayout(cols = 1, size_hint = (.9,.9), pos_hint = {'center_x':.5, 'center_y':.5})
        pariente.add_widget(Label(size_hint_y = None, height = '28dp',markup = True,text_size = ((Window.width*0.9)-25,35),text = C4+"[size=18][b]Contacto"))
        pariente.add_widget(Label(size_hint_y = None, height = '28dp',opacity = .54,markup = True,valign = 'middle',text_size = ((Window.width*0.9)-25,dp(35)),text = C4+"[size=15]Asunto"))
        dim = GridLayout(cols = 2)
        
        pariente.add_widget(dim)
        dim.add_widget(Label(opacity = .74,markup = True,valign = 'middle',text_size = ((Window.width*0.9)-25 - 70,dp(35)),text = C4+"[size=15]Datos detallados"))
        dim.add_widget(Label(size_hint_x = None, width = '70dp',opacity = .74,markup = True,halign = 'center',valign = 'middle',text_size = (dp(70),dp(35)),text = C4+"[size=15]30Min"))
        
        self.add_widget(pariente)
        self.add_widget(Button(opacity = 0, on_release = lambda x:self.opciones(managing = kwargs['managing'])))
        
    def opciones(self,**kwargs):
        try:
            for i in self.opened:
                i.parent.remove_widget(i)
        except:
            pass
                
        relat = RelativeLayout()
        img = Image(opacity = .0, keep_ratio = False, allow_stretch = True, source = color + "3.png")
        pp = ['Examinar Documento','Realizar pedido', 'Estado de cuenta','Localizar en Mapa' ]
        pp1 = ['Examinar Documento','Realizar pedido', 'Estado de cuenta','Localizar en Mapa' ]
        
        opciones = GridLayout(cols = 1,opacity = .0,size_hint = (.8,None),height = 250, pos_hint = {'center_x':.5,'center_y':.5})
        for i in range(4): opciones.add_widget(Button(on_release = lambda x: kwargs["managing"](x.text[len(C4+"[size=17][b]"):]),halign = 'left', valign = 'middle',text_size = ((Window.width * 0.8)-35,400.0/7.0),background_normal = 'None',background_down = color + '16bb.png',markup = True,text = C4+"[size=17][b]"+pp[i]))
        
        def destroy(x):
            anim2 = Animation(opacity = 0 , d = .225, t = 'out_expo')
            anim2.bind(on_complete = lambda y,z: x.parent.parent.remove_widget(x.parent))
            anim2.start(x.parent)
        self.opened.append(relat)
        self.parent.parent.parent.parent.add_widget(relat)
        relat.add_widget(img)
        relat.add_widget(Button(opacity = 0,on_release = lambda x: destroy(x)))
        relat.add_widget(Image(size_hint = (.85,None), pos_hint = {'center_x':.5,'center_y':.5},height = 300 , keep_ratio = False, allow_stretch = True, source =  "Repeat Grid 3.png"))
        relat.add_widget(opciones)
        
        anim1 = Animation(opacity = .14 , d = .225/2, t = 'in_expo')
        anim2 = Animation(opacity = 1 , d = .3, t = 'out_expo')
        anim1.bind(on_complete = lambda x,y: anim2.start(opciones))
        anim1.start(img)
        
class MyApp(App):
    def build(self):
        return Recordatorio()
 

if __name__ in ('__main__', '__android__'):
    MyApp().run()

    
    
    
    
    