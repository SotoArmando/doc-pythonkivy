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
from kivy.uix.bubble import Bubble
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
from utils import CustTextInput
from autosize import MyButton as SizeButton


resource_add_path(os.path.dirname(__file__))

from kivy.uix.behaviors import ButtonBehavior
from kivy.animation import Animation
from kivy.uix.widget import Widget
from kivy.uix.stencilview import StencilView
from kivy.metrics import dp
from kivy.clock import Clock
from kivy.garden.mapview import MapView, MapMarker, MarkerMapLayer, MapSource, MapLayer,MapMarkerPopup
from kivy.properties import (ObjectProperty, NumericProperty, OptionProperty,
                             BooleanProperty, StringProperty)
from kivy.resources import resource_add_path
from kivy.lang import Builder
import os.path
from clientshow import ClientShow
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
EC = "[/color]"
kv = '''
<MyButton>:
    size_hint: None, 1
    size: self.texture_size
'''
Builder.load_string(kv)
class ImageButton(ButtonBehavior, Image): pass
from calendario import Calendar
class Vendedores_Item(RelativeLayout):
    def __init__(self, **kwargs):
        super(Vendedores_Item, self).__init__(**kwargs)
        self.opened= [] 
        relat0 = RelativeLayout(size_hint = (None,None), size = (dp(400), dp(154)), pos_hint = {'center_x':.5, 'center_y':.5})
        self.size_hint = (1,None)
        self.height = 184
        #self.add_widget(Image(opacity = .05,source = color + "3.png", keep_ratio = False , allow_stretch = True))
        self.add_widget(Image(source =  "Repeat Grid 3.png", keep_ratio = False , allow_stretch = True))
        relat0.add_widget(Image(source = color + "16.png", keep_ratio = False , allow_stretch = True))
        campo = [ "username:\n",
                  "first_name:\n",
                  "last_name:\n", 
                  "last_login:\n",
                  "is_staff:\n",
                  "email:\n",
                  "date_joined:\n[/color]" ]
        self.item = kwargs["item"]
        data = [kwargs["item"]["username"],
                kwargs["item"]["first_name"],
                kwargs["item"]["last_name"],
                kwargs["item"]["last_login"][:19],
                kwargs["item"]["is_staff"],
                kwargs["item"]["email"]]

        pariente = GridLayout(cols = 1, padding = [5,15,5,0])
        #Title = Label(valign = 'middle',halign = 'left',text_size = (Window.width- 50,24),markup = True,text = C4 + "[size=17][b]Factura No.: " + "[b]" + str(kwargs["item"]["no_factura"]), size_hint_y = None, height = 38)
        pariente2 = GridLayout(cols = 2, padding = [5,0,5,0])
        #pariente.add_widget(Title)
        pariente.add_widget(pariente2)
        relat0.add_widget(pariente)
        self.add_widget(relat0)
        for i in range(6): 
            if ((i+1)%2) < 1:
                if i == 7:
                   
                    pariente2.add_widget(Label(valign = 'bottom',halign = 'right',text_size = (Window.width/2 -25,40),markup = True,text = C4 + campo[i] + "[b]" + kwargs["temp"][3][0][int(data[i])-1]["cliente"], size_hint_y = None, height = 44))
                    pariente2.add_widget(Image(opacity = .14,source = color + "3.png",size_hint_y = None , height = 2, keep_ratio = False , allow_stretch = True))
                    pariente2.add_widget(Image(opacity = .14,source = color + "3.png",size_hint_y = None , height = 2, keep_ratio = False , allow_stretch = True))
                else:   
                    pariente2.add_widget(Label(valign = 'bottom',halign = 'right',text_size = (Window.width/2 -25,40),markup = True,text = C4 + campo[i] + "[b]" + str(data[i]), size_hint_y = None, height = 44))
                    pariente2.add_widget(Image(opacity = .14,source = color + "3.png",size_hint_y = None , height = 2, keep_ratio = False , allow_stretch = True))
                    pariente2.add_widget(Image(opacity = .14,source = color + "3.png",size_hint_y = None , height = 2, keep_ratio = False , allow_stretch = True))

            else:
                if i == 8:
                    #print str(data), "HELLO"
                    if (str(data[i])[0] == "S"):
                        pariente2.add_widget(Label(valign = 'bottom',halign = 'left',text_size = (Window.width/2  -25,40),markup = True,text = C4 + campo[i] + "[color=#ff0000][b]" + str(data[i]), size_hint_y = None, height = 44))
                    elif (str(data[i])[0] == "E"):
                        pariente2.add_widget(Label(valign = 'bottom',halign = 'left',text_size = (Window.width/2  -25,40),markup = True,text = C4 + campo[i] + "[color=#00ff00][b]" + str(data[i]), size_hint_y = None, height = 44))
                else:   
                    pariente2.add_widget(Label(valign = 'bottom',halign = 'left',text_size = (Window.width/2  -25,40),markup = True,text = C4  + campo[i] + "[b]" + str(data[i]), size_hint_y = None, height = 44))

        
        self.add_widget(Button(opacity = 0, on_release = lambda x: self.opciones(managing = kwargs['managing'])))
    
    def opciones(self,**kwargs):
        try:
            for i in self.opened:
                i.parent.remove_widget(i)
        except:
            pass
                
        relat = RelativeLayout()
        img = Image(opacity = .0, keep_ratio = False, allow_stretch = True, source = color + "3.png")
        pp = ['Examinar documento','Realizar pedido', 'Estado de cuenta','Localizar en Mapa' ]
        pp1 = ['Examinar documento','Realizar pedido', 'Estado de cuenta','Localizar en Mapa' ]
        
        opciones = GridLayout(cols = 1,opacity = .0,size_hint = (.8,None),height = 250, pos_hint = {'center_x':.5,'center_y':.5})
        for i in range(4): opciones.add_widget(Button(on_release = lambda x: kwargs["managing"](x.text[len(C4+"[size=17][b]"):]),halign = 'left', valign = 'middle',text_size = ((Window.width * 0.8)-35,400.0/7.0),background_normal = 'None',background_down = color + '16bb.png',markup = True,text = C4+"[size=17][b]"+pp[i]))
        
        def destroy(x):
            anim2 = Animation(opacity = 0 , d = .225, t = 'out_expo')
            anim2.bind(on_complete = lambda y,z: x.parent.parent.remove_widget(x.parent))
            anim2.start(x.parent)
        self.opened.append(relat)
        self.parent.parent.parent.add_widget(relat)
        relat.add_widget(img)
        relat.add_widget(Button(opacity = 0,on_release = lambda x: destroy(x)))
        relat.add_widget(Image(size_hint = (.85,None), pos_hint = {'center_x':.5,'center_y':.5},height = 300 , keep_ratio = False, allow_stretch = True, source =  "Repeat Grid 3.png"))
        relat.add_widget(opciones)
        
        anim1 = Animation(opacity = .14 , d = .225/2, t = 'out_expo')
        anim2 = Animation(opacity = 1 , d = .225/2, t = 'out_quart')
        anim1.bind(on_complete = lambda x,y: anim2.start(opciones))
        anim1.start(img)
class Entregas_Item(RelativeLayout):
    def __init__(self, **kwargs):
        super(Entregas_Item, self).__init__(**kwargs)
        self.opened= [] 
        relat0 = RelativeLayout(size_hint = (None,None), size = (dp(400), dp(284)), pos_hint = {'center_x':.5, 'center_y':.5})
        self.size_hint = (1,None)
        self.height = 324
        #self.add_widget(Image(opacity = .05,source = color + "3.png", keep_ratio = False , allow_stretch = True))
        self.back = Image(source =  "Repeat Grid 3.png", keep_ratio = False , allow_stretch = True)
        self.add_widget(self.back)
        relat0.add_widget(Image(source = color + "16.png", keep_ratio = False , allow_stretch = True))
        self.item = kwargs["item"]
        campo = ["Emision:\n",
                  "Vencimiento:\n",
                  "balance_original:\nRD$",
                  "balance_actual:\nRD$",
                  "dias:\n",    
                  "posicion_mapa:\n",
                  "creditos:\nRD$",
                  "Cliente:\n",
                  "Estado de entrega:\n[/color]",
        ]
        data = [kwargs["item"]["emision"],
                kwargs["item"]["vencto"],
                kwargs["item"]["balance_original"],
                kwargs["item"]["balance_actual"],
                kwargs["item"]["dias"],
                kwargs["item"]["posicion_mapa"],
                kwargs["item"]["creditos"],
                kwargs["item"]["cliente"],
                kwargs["item"]["estado_entrega"]]

        
        pariente = GridLayout(cols = 1, padding = [5,15,5,0])
        Title = Label(valign = 'middle',halign = 'left',text_size = (Window.width- 50,24),markup = True,text = C4 + "[size=17][b]Factura No.: " + "[b]" + str(kwargs["item"]["no_factura"]), size_hint_y = None, height = 38)
        pariente2 = GridLayout(cols = 2, padding = [5,0,5,0])
        
        
        pariente.add_widget(Title)
        pariente.add_widget(pariente2)
        relat0.add_widget(pariente)
        self.add_widget(relat0)
        for i in range(9): 
            if ((i+1)%2) < 1:
                if i == 7:
                   
                    pariente2.add_widget(Label(valign = 'bottom',halign = 'right',text_size = (Window.width/2 -25,40),markup = True,text = C4 + campo[i] + "[b]" + kwargs["temp"][3][0][int(data[i])-1]["cliente"], size_hint_y = None, height = 44))
                    pariente2.add_widget(Image(opacity = .14,source = color + "3.png",size_hint_y = None , height = 2, keep_ratio = False , allow_stretch = True))
                    pariente2.add_widget(Image(opacity = .14,source = color + "3.png",size_hint_y = None , height = 2, keep_ratio = False , allow_stretch = True))
                else:   
                    pariente2.add_widget(Label(valign = 'bottom',halign = 'right',text_size = (Window.width/2 -25,40),markup = True,text = C4 + campo[i] + "[b]" + str(data[i]), size_hint_y = None, height = 44))
                    pariente2.add_widget(Image(opacity = .14,source = color + "3.png",size_hint_y = None , height = 2, keep_ratio = False , allow_stretch = True))
                    pariente2.add_widget(Image(opacity = .14,source = color + "3.png",size_hint_y = None , height = 2, keep_ratio = False , allow_stretch = True))

            else:
                if i == 8:
                    #print str(data), "HELLO"
                    if (str(data[i])[0] == "S"):
                        pariente2.add_widget(Label(valign = 'bottom',halign = 'left',text_size = (Window.width/2  -25,40),markup = True,text = C4 + campo[i] + "[color=#ff0000][b]" + str(data[i]), size_hint_y = None, height = 44))
                    elif (str(data[i])[0] == "E"):
                        pariente2.add_widget(Label(valign = 'bottom',halign = 'left',text_size = (Window.width/2  -25,40),markup = True,text = C4 + campo[i] + "[color=#00ff00][b]" + str(data[i]), size_hint_y = None, height = 44))
                else:   
                    pariente2.add_widget(Label(valign = 'bottom',halign = 'left',text_size = (Window.width/2  -25,40),markup = True,text = C4  + campo[i] + "[b]" + str(data[i]), size_hint_y = None, height = 44))

        
        self.add_widget(Button(opacity = 0, on_release = lambda x: self.opciones(managing = kwargs['managing'])))
    
    def opciones(self,**kwargs):
        try:
            for i in self.opened:
                i.parent.remove_widget(i)
        except:
            pass
                
        relat = RelativeLayout()
        img = Image(opacity = .0, keep_ratio = False, allow_stretch = True, source = color + "3.png")
        pp = ['Examinar documento','Encargar pedido', 'Estado de cuenta','Localizar en Mapa' ]
        pp1 = ['Examinar documento','Encargar pedido', 'Estado de cuenta','Localizar en Mapa' ]
        
        opciones = GridLayout(cols = 1,opacity = .0,size_hint = (.8,None),height = 250, pos_hint = {'center_x':.5,'center_y':.5})
        for i in range(4): opciones.add_widget(Button(on_release = lambda x: kwargs["managing"](self.item,x.text[len(C4+"[size=17][b]"):]),halign = 'left', valign = 'middle',text_size = ((Window.width * 0.8)-35,400.0/7.0),background_normal = 'None',background_down = color + '16bb.png',markup = True,text = C4+"[size=17][b]"+pp[i]))
        
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
        
        anim1 = Animation(opacity = .14 , d = .225/2, t = 'out_expo')
        anim2 = Animation(opacity = 1 , d = .225/2, t = 'out_quart')
        anim1.bind(on_complete = lambda x,y: anim2.start(opciones))
        anim1.start(img)
        
class Entregas(Screen):
    def __init__(self, **kwargs):
        super(Entregas, self).__init__(**kwargs)
        self.root = kwargs["s"]
        self.sc = ScreenManager()
        self.factura_entregar = None
        self.vendedor = None
        self.connect = kwargs["connect"]
        self.temp = kwargs["temp"]
        self.Vendedortxt = CustTextInput("Vendedor","Vendedor","Vendedor")
        
        self.screen1 = Screen(name = 'main')
        self.screen2 = Screen(name = 'Examinar documento')
        self.screen3 = Screen(name = 'Encargar pedido')
        self.screen5 = Screen(name = 'Estado de cuenta')
        self.screen4 = Seleccionar_Vendedores(vtxt = self.Vendedortxt,sc = self.sc,name = 'Seleccionar Vendedor', temp = self.temp)
        pariente_scroll = ScrollView()
        
        pariente = GridLayout(cols = 1, size_hint_y = None, height = 500)
        open_filtros = Button(on_release = lambda x: self.openfilter1(x),markup = True, text = C4+"[b]Criterios",font_size = dp(18), background_normal = color + '16.png', background_down = color + '16.png',valign = 'middle',text_size = (Window.width - dp(25),dp(56)), size_hint_y = None, height = dp(56))
        
        
        self.lay = GridLayout(cols = 1, size_hint_y = None , height = dp(56))
        self.lay_dim = GridLayout(cols = 2, opacity = 0.)
 
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

            

 
 
        self.lay.add_widget(open_filtros)
        self.lay.add_widget(self.lay_dim)
        
        for i in self.temp[0][1]:
            newwidget = ToggleButton(background_normal = color +"16.png",markup = True,group = "Account_Receivable", text =C4+i,valign = 'middle',text_size = (Window.width/2 -dp(25), dp(36)), font_size = 16)
            newwidget.bind(on_press = lambda x: self.root.set_FiltrarCampo(0,x.text[len(C4):]))
            self.lay_dim.add_widget(newwidget)
            
            
        pariente.add_widget(Image(size_hint_y = None, height = 71,opacity = 1, source =color+ "16.png", keep_ratio = False , allow_stretch = True))
        pariente.add_widget(Button(background_normal = color + "16.png",text = C4+"Entregas",text_size = (Window.width - 50 , dp(50)),valign = 'middle', halign = 'left',size_hint_y = None , height = '50dp', markup = True, font_size = '24sp')) 
        relat1 = RelativeLayout(size_hint_y = None, height = 100)
        relat1.add_widget(Image(size_hint_y = 1,opacity = 1, source =color+ "16.png", keep_ratio = False , allow_stretch = True))
        relat1.add_widget(SizeButton(background_normal = "None",text = C4+"A continuacion se muestran las Entregas Realizadas y por Realizar, puede encargarlas presionandolas y seleccionando la opcion 'Encargar pedido'",pos_hint = {'center_x':.5, 'center_y':.5},text_size = (Window.width *.75 , 100),valign = 'middle', halign = 'center',size_hint_y = None , height = '50dp', markup = True))
        pariente.add_widget(relat1)
        
        pariente.add_widget(Image(size_hint_y = None, height = 50,opacity = 1, source =color+"16.png", keep_ratio = False , allow_stretch = True))
        pariente.add_widget(Image(source = color + "16.png", height = 25,size_hint_y = None, keep_ratio= False, allow_stretch = True))
        pariente.add_widget(dim1)
        pariente.add_widget(Image(source = color + "16.png", height = 25,size_hint_y = None, keep_ratio= False, allow_stretch = True))
        
        pariente.add_widget(self.lay)
        pariente.add_widget(Calendar())
        self.item_list = GridLayout(cols = 1,size_hint_y = 1 , height = 0)
        self.temp = kwargs['temp']
        for i in self.temp[0][0]:
            #print i
            if i["estado_entrega"][0] == "S":
                self.item_list.add_widget(Entregas_Item(temp = self.temp,managing = self.set_current, item = i))
                pariente.height += 324
            else:
                self.item_list.add_widget(Entregas_Item(temp = self.temp,managing = self.set_current, item = i))
                pariente.height += 324 
        self.datos_parent = self.item_list

        pariente.add_widget(self.item_list)
        pariente_scroll.add_widget(pariente)
        self.screen1.add_widget(pariente_scroll)
        
        
        self.sc.add_widget(self.screen1)
        self.sc.add_widget(self.screen2)
        self.sc.add_widget(self.screen3)
        self.sc.add_widget(self.screen4)
        self.sc.add_widget(self.screen5)
        self.add_widget(Image(size_hint_y = 1,opacity = 1, source =color+ "16.png", keep_ratio = False , allow_stretch = True))
        #self.add_widget(Image(size_hint_y = 1,opacity = .05, source =color+ "3.png", keep_ratio = False , allow_stretch = True))
        self.add_widget(self.sc)
        self.screen3_parent = GridLayout(cols = 1, size_hint_y = None , height = dp(1100))
        self.screen3_parent.add_widget(Label(size_hint_y = None, height = 71))
        screen3_scroll = ScrollView()
        screen3_scroll.add_widget(self.screen3_parent)
        self.screen3.add_widget(screen3_scroll)

        self.Desctxt = CustTextInput("Descripcion","Descripcion","Descripcion")
        self.FechaHtxt = CustTextInput("Fecha Hora Creada","Fecha Hora Creada","Fecha Hora Creada")
        self.Tipotxt = CustTextInput("Tipo","Tipo","Tipo")
        self.EntregFtxt = CustTextInput("Entregar Factura","Entregar Factura","Entregar Factura")
        self.FechaHAtxt = CustTextInput("Fecha Hora A","Fecha Hora A","Fecha Hora A")
        self.FechaHBtxt = CustTextInput("Fecha Hora B","Fecha Hora B","Fecha Hora B")
        self.FechaHRtxt = CustTextInput("Fecha Hora_Realizada","Fecha Hora_Realizada","Fecha Hora_Realizada")
        
        
        
        #self.Vendedortxt.input0 = self.temp[2][0][self.vendedor]
        
        import datetime
        x = datetime.datetime.now()
        y = str(x).replace(" ", "T")
        y += "Z"
        
        self.FechaHtxt.input0.text = y
        self.FechaHAtxt.input0.text = "Sin Emitir"
        self.FechaHBtxt.input0.text = "Sin Emitir"
        self.Tipotxt.input0.text = "Entrega"
        self.FechaHRtxt.input0.text = "Sin Emitir"
        
        self.FechaHtxt.on_click_onit()
        self.FechaHAtxt.on_click_onit()
        self.FechaHBtxt.on_click_onit()
        self.Tipotxt.on_click_onit()
        self.FechaHRtxt.on_click_onit()
        
        self.FechaHtxt.disabled = True
        self.FechaHAtxt.disabled = True
        self.FechaHBtxt.disabled = True
        self.Tipotxt.disabled = True
        self.FechaHRtxt.disabled = True
        
        relat1 = RelativeLayout(size_hint_y = None, height = 100)
        relat1.add_widget(SizeButton(background_normal = "None",text = C4+"A Continuacion se mostrara un formulario para soliciar un encargo. rellene los campos siguientes.",pos_hint = {'center_x':.5, 'center_y':.5},text_size = (Window.width *.75 , 100),valign = 'middle', halign = 'center',size_hint_y = None , height = '50dp', markup = True))
        self.screen3_parent.add_widget(relat1)
        
        
        
        self.screen3_parent.add_widget(self.FechaHtxt)
        self.screen3_parent.add_widget(self.Tipotxt)
        self.screen3_parent.add_widget(self.EntregFtxt)
        self.screen3_parent.add_widget(self.Desctxt)
        self.screen3_parent.add_widget(self.FechaHAtxt)
        self.screen3_parent.add_widget(self.FechaHBtxt)
        self.screen3_parent.add_widget(self.FechaHRtxt)
        self.screen3_parent.add_widget(self.Vendedortxt)
        self.screen3_parent.add_widget(Button(on_release = lambda x: self.simplycurrent('Seleccionar Vendedor'),text_size = (Window.width,41), valign = 'middle', halign = 'center',background_down = color + "16b.png",background_normal = color + "None.png",text = C4 + "[b]Seleccionar Vendedor", markup = True, size_hint_y = None, height = dp(41)))
        self.screen3_parent.add_widget(Label(size_hint_y = None, height = 24))
        
        self.screen3_parent.add_widget(Button(markup = True,on_release = lambda x: self.confirmar_data(),text = C4+"[size=17][b]Completar Encargo", size_hint_y = None, height = dp(61), background_normal = color+"16bb.png", background_down = color+"16b.png"))
        self.screen3_parent.add_widget(Button(on_release = lambda x: self.simplycurrent("main"),markup = True,text = C4+"[size=17][b]Cancelar Encargo", size_hint_y = None, height = dp(61), background_normal = color+"16bb.png", background_down = color+"16b.png"))
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
                        item_x = Entregas_Item(opacity = 0,temp = self.temp,managing = self.set_current, item = i)
                        self.datos_parent.add_widget(item_x)
                        self.datos_parent.height += 324
                        a = Animation(opacity = 1, d = .5, t = 'out_quart')
                        a.start(item_x)
                    else:
                        item_x = Entregas_Item(opacity = 0,temp = self.temp,managing = self.set_current, item = i)
                        self.datos_parent.add_widget(item_x)
                        self.datos_parent.height += 324
                        a = Animation(opacity = 1, d = .5, t = 'out_quart')
                        a.start(item_x)

                else:
                    pass
        except:
            import traceback
            traceback.print_exc()
    
    def simplycurrent(self,setting): self.sc.current = setting
    def confirmar_data(self):
        import datetime
        x = datetime.datetime.now()
        y = str(x).replace(" ", "T")
        y += "Z"
        self.vendedor = self.screen4.seleccionado
        print self.vendedor, "POROOWEQPOWJEQOPDJQWPDOJ"
        self.Schedule_item = {
            "idline": 0,
            "Tipo": "Entrega",
            "Fecha_Hora_B": y,
            "Fecha_Hora_A": y,
            "fecha_hora": y,
            "Vendedor": self.vendedor["id"],
            "descripcion": str(self.Desctxt.input0.text),
            "codigo": "000",
            "Fecha_Hora_Realizada": y,
            "id": int(len(self.temp[1][0])+1),
            "Entrega_Factura": int(self.factura_entregar)
        }
        print self.Schedule_item
        self.connect(tableid = 1, jsondata = self.Schedule_item)  
    def sendschedule(self):
    
        data = {
        "idline": null,
        "Tipo": "",
        "Fecha_Hora_B": null,
        "Fecha_Hora_A": null,
        "fecha_hora": null,
        "Vendedor": null,
        "descripcion": "",
        "codigo": "",
        "Fecha_Hora_Realizada": null,
        "id": null,
        "Entrega_Factura": null
        }
        self.connect(tableid = 1, jsondata = data)
        
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
    def add_item(self,**kwargs):
        pariente.add_widget(Entregas_Item(managing = self.set_current))
        
    def set_current(self,xo,setting): 
        try:
        
            print setting
            self.sc.current = setting
        except:
            pass
        self.factura_entregar = xo["id"]
        if setting == "Examinar documento":
            self.screen2.clear_widgets()
            #self.screen2.add_widget(Image())
            scroll = ScrollView()
            screen2_pariente = GridLayout(cols = 1, size_hint_y = None, height = 1000,padding = [0,25,0,0])
            scroll.add_widget(screen2_pariente)
            self.screen2.add_widget(Image(size_hint_y = 1,opacity = 1, source =color+ "16.png", keep_ratio = False , allow_stretch = True))
            self.screen2.add_widget(scroll)
                
            campo = ["Fecha:\n",
                      "Vencimiento:\n",
                      "Monto neto:\n",
                      "Balance:\n",
                      "Total:\n",    
                      "Monto a pagar:\n",
                      "Descuento:\n",
                      "Nuevo Balance:\n",
                      "Estado:\n[/color][color=#00FF00]",
            ]
            pariente = GridLayout(cols = 1, padding = [5,25,5,0], size_hint_y = None, height = 300)
            Title = Label(valign = 'middle',halign = 'left',text_size = (Window.width- 35,24),markup = True,text = C4 + "[size=18]Factura No.: " + "[b]01244536", size_hint_y = None, height = 38)
            pariente2 = GridLayout(cols = 2, padding = [5,0,5,0])
            

            pariente.add_widget(Title)
            pariente.add_widget(pariente2)
            
      
            for i in range(9): 
                if ((i+1)%2) < 1:
                    pariente2.add_widget(Label(valign = 'bottom',halign = 'right',text_size = (Window.width/2 -25,40),markup = True,text = C4 + campo[i] + "[b]data", size_hint_y = None, height = 44))
                    pariente2.add_widget(Image(opacity = .14,source = color + "3.png",size_hint_y = None , height = 2, keep_ratio = False , allow_stretch = True))
                    pariente2.add_widget(Image(opacity = .14,source = color + "3.png",size_hint_y = None , height = 2, keep_ratio = False , allow_stretch = True))
                else:    
                    pariente2.add_widget(Label(valign = 'bottom',halign = 'left',text_size = (Window.width/2  -25,40),markup = True,text = C4 + campo[i] + "[b]data", size_hint_y = None, height = 44))

                    
                    

            B_pariente = GridLayout(cols = 1, padding = [5,25,5,0], spacing = 5)
            B_pariente.add_widget(Label(valign = 'middle',halign = 'left',text_size = (Window.width- 35,24),markup = True,text = C4 + "[size=18][b]Detalles", size_hint_y = None, height = 38))
            try:
                idobjetos = xo["idobjetos"].split(",")
                for i in idobjetos:
                    objeto_parent = RelativeLayout(size_hint_y = None, height = 84)
                    objeto_parent.add_widget(Image(source = color + '16bb.png', keep_ratio = False, allow_stretch = True , size_hint = (.95,.95), pos_hint = {'center_x':.5, 'center_y':.5}))
                    objeto = GridLayout(cols = 2, padding = [7,7,7,7])
                    
                    objeto.add_widget(Label(valign = 'middle',halign = 'left',text_size = (Window.width/2 - 35,40),markup = True,text = C4 + "Objeto:\n[b]"+self.temp[4][0][int(i)-1]["item_name"], size_hint_y = 1, height = 38))
                    objeto.add_widget(Label(valign = 'middle',halign = 'right',text_size = (Window.width/2 - 35,40),markup = True,text = C4 + "Cantidad:\n[b]1", size_hint_y = 1, height = 38))
                    objeto.add_widget(Label(valign = 'middle',halign = 'left',text_size = (Window.width/2 - 35,40),markup = True,text = C4 + "Clasificacion:\n[b]"+self.temp[4][0][int(i)-1]["clasificacion"], size_hint_y = 1, height = 38))
                    objeto.add_widget(Label(valign = 'middle',halign = 'right',text_size = (Window.width/2 - 35,40),markup = True,text = C4 + "Precio:\n[b]RD$"+self.temp[4][0][int(i)-1]["precio_1"], size_hint_y = 1, height = 38))
                    objeto_parent.add_widget(objeto)
                    B_pariente.add_widget(objeto_parent)
            except:
                pass


            entregasitem = Entregas_Item(temp = self.temp,managing = self.set_current, item = xo)
            entregasitem.back.source = ""
            screen2_pariente.add_widget(entregasitem)#pariente

            screen2_pariente.add_widget(B_pariente)
            screen2_pariente.add_widget(Button(on_release = lambda x: self.simplycurrent("main"),size_hint_y = None,markup = True, background_normal = color + "16.png", height = 74, text = C4+"[size=17][b]volver"))

        elif setting == "Encargar pedido":
            self.EntregFtxt.input0.text = str(xo["cliente"]) + str(xo["emision"])
            self.EntregFtxt.input0.background_disabled_normal = color + "None.png"
            self.EntregFtxt.disabled = True
            self.EntregFtxt.on_click_onit()
            #screen2_pariente.add_widget(self.parent_scrollview2)
        elif setting == "Estado de cuenta":
            self.screen5.clear_widgets()
            scroll = ScrollView()
            pariente = GridLayout(cols = 1, size_hint_y = None, height = 100)
            scroll.add_widget(pariente)
            self.screen5.add_widget(scroll)
            pariente.add_widget(Label(size_hint_y = None, height = dp(50)))
            self.parent_scrollview2 = ScrollView(do_scroll_x = True, do_scroll_y = False, size_hint_y = None, height = 300)
            self.scrollview2_parent = GridLayout(rows = 4, cols = 6, size_hint_x = None, width = 700)
            self.scrollview2_parent.bind(minimum_width = self.scrollview2_parent.setter('width'))
            self.parent_scrollview2.add_widget(self.scrollview2_parent)
            i = self.temp[3][0][0]
            client = ClientShow(item = i, temp = self.temp, managing = self.simplycurrent)
            client.back.source = color + "None.png"
            
            pariente.height += 290
            rowsset1 = [
            ["M","0 30","31 60","61 90","91 120","121 +"],
            ["Balance","470,000.00","80,000.00","","","15,000.00"],
            ["Porciento","83.40%","14.00%","","","2.60%"],
            ]
            for row in rowsset1:
                for i in row:
                    settimg = color + "16bb.png" 
                    if (i == "M")or(i == "Balance")or(i=="Porciento"): 
                        b = ''
                        settimg = color + "16b.png" 
                    else:
                        b = '[b]'
                    self.scrollview2_parent.add_widget(Button(background_normal = settimg,text = C4+b+i,markup= True,font_size = 16))
            cliente = self.temp[3][0][xo["cliente"]-1]
            client = ClientShow(item = cliente, temp = self.temp, managing = self.simplycurrent)
            client.back.source = color + "None.png"
            pariente.add_widget(client)
            pariente.height += 290
            pariente.add_widget(self.parent_scrollview2)
            
            for i in self.temp[0][0]:
                if xo["cliente"] == i["cliente"]:
                    pariente.add_widget(Entregas_Item(temp = self.temp,managing = self.simplycurrent, item = i))
                    pariente.height += 324
            
        elif setting == "Localizar en Mapa":
            self.root.anim_hstate_root()
            self.root.current("b")
            pos = xo["posicion_mapa"].replace(" ","")
            pos = pos.split(",")
            
            self.root.x_mapview.center_on(float(pos[0]),float(pos[1]))
            bubble = Bubble()
            marcador = MapMarkerPopup(lat=float(pos[0]),lon=float(pos[1]), source = asset + "Group 5.png")
            dim = GridLayout(cols = 1)
            dim.add_widget(Button(on_release = lambda x: self.root.searcherm.toggleinfor(),opacity = .74,background_normal  = color + '16.png', markup = True,text =C4+"[b]Buscar Direcciones", size_hint = (None,None), size = (dp(250),dp(56))))
            dim.add_widget(Button(on_release = lambda x: self.root.searcherm.toggleinfor(),opacity = .74,background_normal  = color + '16.png', markup = True,text =C4+"[b]Datos", size_hint = (None,None), size = (dp(250),dp(56))))
            #dim.add_widget(Button(on_release = lambda x: self.searcherm.toggleinfor(),opacity = .74,background_normal  = color + '16.png', markup = True,text =C4+"[b]Boton2", size_hint = (None,None), size = (dp(100),dp(56))))
            marcador.add_widget(dim)
            self.root.x_mapview.add_marker(marcador)
            
              
class Vendedores(Screen):
    def __init__(self, **kwargs):
        super(Vendedores, self).__init__(**kwargs)
        self.sc = ScreenManager()
        self.Schedule_item = {}
        self.root = kwargs["r"]
        self.Entrega_Factura = ""
        self.screen1 = Screen(name = 'main')
        self.screen2 = Screen(name = 'Examinar documento')
        self.screen3 = Screen(name = 'Encargar pedido')
        self.temp = kwargs["temp"]
        try:
            self.connect = kwargs["connect"]
        except:
            pass

        pariente_scroll = ScrollView()
        pariente = GridLayout(cols = 1, size_hint_y = None, height = 500)
        open_filtros = Button(on_release = lambda x: self.openfilter1(x),markup = True, text = C4+"[b]Criterios",font_size = dp(18), background_normal = color + '16.png', background_down = color + '16.png',valign = 'middle',text_size = (Window.width - dp(25),dp(56)), size_hint_y = None, height = dp(56))
        
        
        self.lay = GridLayout(cols = 1, size_hint_y = None , height = dp(56))
        self.lay_dim = GridLayout(cols = 2, opacity = 0.)
 
        dim1 = RelativeLayout(size_hint_y = None, height = 52)
        dim1.add_widget(Image(source = color+"16.png", allow_stretch = True , keep_ratio = False))
        
        dim1b = GridLayout(rows = 1 , size_hint_y = None , height = 50)
        dim1b.add_widget(Label(size_hint_x = None, width = ((Window.width-382)/2)))
        
        dim1b.add_widget(Button(border = [0,0,0,0],background_normal = asset+"1.png",background_down = asset+"1.png",size_hint_x = None, width = 64))
        textwidget = TextInput(multiline=False,size_hint_x = None, width =254,font_size = 16, hint_text = "Buscar Vendedor",padding = [0,dp(18),0,0],background_normal = asset+"2.png",background_active = asset+"2.png")
        textwidget.bind(on_text_validate = lambda x: self.Filtrar(2,x.text))
        dim1b.add_widget(textwidget)
        dim1b.add_widget(Button(border = [0,0,0,0],background_normal = asset+"3.png",background_down = asset+"3.png",size_hint_x = None, width = 64))
        
        image1_parent = RelativeLayout(cols = 1, size_hint = (None,None), size = (50,50))
        dim1b.add_widget(image1_parent)
        dim1b.add_widget(Label(size_hint_x = None, width = ((Window.width-382)/2)))
        
        dim1.add_widget(Image(pos_hint = {'y': 1},opacity = .12,source = color + "3.png", keep_ratio = False , allow_stretch = True, size_hint_y = None, height = dp(1)))
        dim1.add_widget(dim1b)
        dim1.add_widget(Image(source = color + "3.png",opacity = .12, keep_ratio = False , allow_stretch = True, size_hint_y = None, height = dp(1)))

            

 
 
        self.lay.add_widget(open_filtros)
        self.lay.add_widget(self.lay_dim)
        
        for i in self.temp[2][1]:
            newwidget = ToggleButton(background_normal = color +"16.png",markup = True,group = "Account_Receivable", text =C4+i,valign = 'middle',text_size = (Window.width/2 -dp(25), dp(36)), font_size = 16)
            newwidget.bind(on_press = lambda x: self.root.set_FiltrarCampo(2,x.text[len(C4):]))
            self.lay_dim.add_widget(newwidget)
            
            
        pariente.add_widget(Image(size_hint_y = None, height = 71,opacity = 1, source =color+ "16.png", keep_ratio = False , allow_stretch = True))
        pariente.add_widget(Button(background_normal = color + "16.png",text = C4+"Vendedores",text_size = (Window.width - 50 , dp(50)),valign = 'middle', halign = 'left',size_hint_y = None , height = '50dp', markup = True, font_size = '24sp')) 
        relat1 = RelativeLayout(size_hint_y = None, height = 100)
        relat1.add_widget(Image(size_hint_y = 1,opacity = 1, source =color+ "16.png", keep_ratio = False , allow_stretch = True))
        relat1.add_widget(SizeButton(background_normal = "None",text = C4+"A continuacion se muestran las Entregas Realizadas y por Realizar, puede encargarlas presionandolas y seleccionando la opcion 'Encargar pedido'",pos_hint = {'center_x':.5, 'center_y':.5},text_size = (Window.width *.75 , 100),valign = 'middle', halign = 'center',size_hint_y = None , height = '50dp', markup = True))
        pariente.add_widget(relat1)
        
        pariente.add_widget(Image(size_hint_y = None, height = 50,opacity = 1, source =color+"16.png", keep_ratio = False , allow_stretch = True))
        pariente.add_widget(Image(source = color + "16.png", height = 25,size_hint_y = None, keep_ratio= False, allow_stretch = True))
        pariente.add_widget(dim1)
        pariente.add_widget(Image(source = color + "16.png", height = 25,size_hint_y = None, keep_ratio= False, allow_stretch = True))
        
        pariente.add_widget(self.lay)
        pariente.add_widget(Calendar())
        self.datos_parent = GridLayout(cols = 1)
        self.datos_parenth = pariente
        self.temp = kwargs['temp']
        for i in self.temp[2][0]:
            #print i
            self.datos_parent.add_widget(Vendedores_Item(managing = self.set_current, item = i, temp = self.temp))
            pariente.height += 324 


        pariente.add_widget(self.datos_parent)
        pariente_scroll.add_widget(pariente)
        self.screen1.add_widget(pariente_scroll)
        
        
        self.sc.add_widget(self.screen1)
        self.sc.add_widget(self.screen2)
        self.sc.add_widget(self.screen3)
        self.add_widget(Image(size_hint_y = 1,opacity = 1, source =color+ "16.png", keep_ratio = False , allow_stretch = True))
        #self.add_widget(Image(size_hint_y = 1,opacity = .05, source =color+ "3.png", keep_ratio = False , allow_stretch = True))
        self.add_widget(self.sc)
        
        self.screen3_parent = GridLayout(cols = 1)
        self.screen3_parent.add_widget(Label(size_hint_y = None, height = 71))

        self.Desctxt = CustTextInput("Descripcion","Descripcion","Descripcion")
        self.FechaHtxt = CustTextInput("Fecha Hora Creada","Fecha Hora Creada","Fecha Hora Creada")
        self.Tipotxt = CustTextInput("Tipo","Tipo","Tipo")
        self.EntregFtxt = CustTextInput("Entregar Factura","Entregar Factura","Entregar Factura")
        self.FechaHAtxt = CustTextInput("Fecha Hora A","Fecha Hora A","Fecha Hora A")
        self.FechaHBtxt = CustTextInput("Fecha Hora B","Fecha Hora B","Fecha Hora B")
        self.FechaHRtxt = CustTextInput("Fecha Hora_Realizada","Fecha Hora_Realizada","Fecha Hora_Realizada")
        self.Vendedortxt = CustTextInput("Vendedor","Vendedor","Vendedor")
        
        self.screen3_parent.add_widget(self.Desctxt)
        self.screen3_parent.add_widget(self.FechaHtxt)
        self.screen3_parent.add_widget(self.Tipotxt)
        self.screen3_parent.add_widget(self.EntregFtxt)
        self.screen3_parent.add_widget(self.FechaHAtxt)
        self.screen3_parent.add_widget(self.FechaHBtxt)
        self.screen3_parent.add_widget(self.FechaHRtxt)
        self.screen3_parent.add_widget(self.Vendedortxt)
        
        self.screen3_parent.add_widget(Button(text = C4+"Completar", size_hint_y = None, height = dp(61), background_normal = "", background_down = ""))
        
    def confirmar_data(self):
        self.Schedule_item = {
            "idline": 0,
            "Tipo": "",
            "Fecha_Hora_B": null,
            "Fecha_Hora_A": null,
            "fecha_hora": null,
            "Vendedor": null,
            "descripcion": "",
            "codigo": "",
            "Fecha_Hora_Realizada": null,
            "id": int(len(self.temp[1][0])+1),
            "Entrega_Factura": null
        }
        #self.connect(tableid = 1, jsondata = self.Schedule_item)
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
    def add_item(self,**kwargs):
        pariente.add_widget(Entregas_Item(managing = self.set_current))
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
                if Tabla == 2:
                    x_item = Vendedores_Item(opacity = 0,managing = self.set_current, item = i, temp = self.temp)
                    self.datos_parent.add_widget(x_item)
                    self.datos_parenth.height += 324 
                    a = Animation(opacity = 1 , d = .5, t = 'out_quart')
                    a.start(x_item)
                else:
                    pass
        except:
            import traceback
            traceback.print_exc()
    
    def set_current(self,setting): 
        self.sc.current = setting
        if setting == "Examinar documento":
            self.screen2.clear_widgets()
            #self.screen2.add_widget(Image())
            scroll = ScrollView()
            screen2_pariente = GridLayout(cols = 1, size_hint_y = None, height = 1000)
            scroll.add_widget(screen2_pariente)
            self.screen2.add_widget(Image(size_hint_y = 1,opacity = 1, source =color+ "16.png", keep_ratio = False , allow_stretch = True))
            self.screen2.add_widget(scroll)
            
            campo = ["Fecha:\n",
                      "Vencimiento:\n",
                      "Monto neto:\n",
                      "Balance:\n",
                      "Total:\n",    
                      "Monto a pagar:\n",
                      "Descuento:\n",
                      "Nuevo Balance:\n",
                      "Estado:\n[/color][color=#00FF00]",
            ]
            pariente = GridLayout(cols = 1, padding = [5,25,5,0], size_hint_y = None, height = 300)
            Title = Label(valign = 'middle',halign = 'left',text_size = (Window.width- 35,24),markup = True,text = C4 + "[size=18]Factura No.: " + "[b]01244536", size_hint_y = None, height = 38)
            pariente2 = GridLayout(cols = 2, padding = [5,0,5,0])
            

            pariente.add_widget(Title)
            pariente.add_widget(pariente2)
            
      
            for i in range(9): 
                if ((i+1)%2) < 1:
                    pariente2.add_widget(Label(valign = 'bottom',halign = 'right',text_size = (Window.width/2 -25,40),markup = True,text = C4 + campo[i] + "[b]data", size_hint_y = None, height = 44))
                    pariente2.add_widget(Image(opacity = .14,source = color + "3.png",size_hint_y = None , height = 2, keep_ratio = False , allow_stretch = True))
                    pariente2.add_widget(Image(opacity = .14,source = color + "3.png",size_hint_y = None , height = 2, keep_ratio = False , allow_stretch = True))
                else:    
                    pariente2.add_widget(Label(valign = 'bottom',halign = 'left',text_size = (Window.width/2  -25,40),markup = True,text = C4 + campo[i] + "[b]data", size_hint_y = None, height = 44))

                    
                    
            self.parent_scrollview2 = ScrollView(do_scroll_x = True, do_scroll_y = False, size_hint_y = None, height = 150)
            self.scrollview2_parent = GridLayout(rows = 4, cols = 6, size_hint_x = None, width = 700)
            self.scrollview2_parent.bind(minimum_width = self.scrollview2_parent.setter('width'))
            self.parent_scrollview2.add_widget(self.scrollview2_parent)
            rowsset1 = [
            ["M","0 30","31 60","61 90","91 120","121 +"],
            ["Balance","470,000.00","80,000.00","","","15,000.00"],
            ["Porciento","83.40%","14.00%","","","2.60%"],
            ]
            for row in rowsset1:
                for i in row:
                    settimg = color + "16bb.png" 
                    if (i == "M")or(i == "Balance")or(i=="Porciento"): 
                        b = ''
                        settimg = color + "16b.png" 
                    else:
                        b = '[b]'
                    self.scrollview2_parent.add_widget(Button(background_normal = settimg,text = C4+b+i,markup= True,font_size = 16))
            
            B_pariente = GridLayout(cols = 1, padding = [5,25,5,0], spacing = 5)
            B_pariente.add_widget(Label(valign = 'middle',halign = 'left',text_size = (Window.width- 35,24),markup = True,text = C4 + "[size=18][b]Detalles", size_hint_y = None, height = 38))
            for i in range(5):
                objeto_parent = RelativeLayout(size_hint_y = None, height = 84)
                objeto_parent.add_widget(Image(source = color + '16bb.png', keep_ratio = False, allow_stretch = True , size_hint = (.95,.95), pos_hint = {'center_x':.5, 'center_y':.5}))
                objeto = GridLayout(cols = 2, padding = [7,7,7,7])
                objeto.add_widget(Label(valign = 'middle',halign = 'left',text_size = (Window.width/2 - 35,40),markup = True,text = C4 + "Objeto:\n[b]data", size_hint_y = 1, height = 38))
                objeto.add_widget(Label(valign = 'middle',halign = 'right',text_size = (Window.width/2 - 35,40),markup = True,text = C4 + "Cantidad:\n[b]data", size_hint_y = 1, height = 38))
                objeto.add_widget(Label(valign = 'middle',halign = 'left',text_size = (Window.width/2 - 35,40),markup = True,text = C4 + "Clasificacion:\n[b]data", size_hint_y = 1, height = 38))
                objeto.add_widget(Label(valign = 'middle',halign = 'right',text_size = (Window.width/2 - 35,40),markup = True,text = C4 + "Precio:\n[b]RD$ data", size_hint_y = 1, height = 38))
                objeto_parent.add_widget(objeto)
                B_pariente.add_widget(objeto_parent)

            #screen2_pariente.add_widget(self.parent_scrollview2)
           
            screen2_pariente.add_widget(pariente)
            screen2_pariente.add_widget(B_pariente)
            screen2_pariente.add_widget(Button(on_release = lambda x: self.set_current(None,"main"),size_hint_y = None,markup = True, background_normal = color + "16.png", height = 74, text = C4+"[size=17][b]volver"))
        elif setting == "Encargar pedido":
            self.EntregFtxt.input0.text = xo["cliente"] + xo["emision"]
            self.EntregFtxt.on_click_onit()
            self.EntregFtxt.disabled = True
class Seleccionar_Vendedores(Screen):
    def __init__(self, **kwargs):
        super(Seleccionar_Vendedores, self).__init__(**kwargs)
        self.sc = ScreenManager()
        self.Schedule_item = {}
        self.seleccionado = 0
        self.Entrega_Factura = ""
        self.screen1 = Screen(name = 'main')
        self.screen2 = Screen(name = 'Examinar documento')
        self.screen3 = Screen(name = 'Encargar pedido')
        self.temp = kwargs["temp"]
        try:
            self.connect = kwargs["connect"]
        except:
            pass

        pariente_scroll = ScrollView()
        pariente = GridLayout(cols = 1, size_hint_y = None, height = 500)
        open_filtros = Button(on_release = lambda x: self.openfilter1(x),markup = True, text = C4+"[b]Criterios",font_size = dp(18), background_normal = color + '16.png', background_down = color + '16.png',valign = 'middle',text_size = (Window.width - dp(25),dp(56)), size_hint_y = None, height = dp(56))
        
        
        self.lay = GridLayout(cols = 1, size_hint_y = None , height = dp(56))
        self.lay_dim = GridLayout(cols = 2, opacity = 0.)
 
        dim1 = RelativeLayout(size_hint_y = None, height = 52)
        dim1.add_widget(Image(source = color+"16.png", allow_stretch = True , keep_ratio = False))
        
        dim1b = GridLayout(rows = 1 , size_hint_y = None , height = 50)
        dim1b.add_widget(Label(size_hint_x = None, width = ((Window.width-382)/2)))
        
        dim1b.add_widget(Button(border = [0,0,0,0],background_normal = asset+"1.png",background_down = asset+"1.png",size_hint_x = None, width = 64))
        textwidget = TextInput(multiline=False,size_hint_x = None, width =254,font_size = 16, hint_text = "Buscar Vendedor",padding = [0,dp(18),0,0],background_normal = asset+"2.png",background_active = asset+"2.png")
        dim1b.add_widget(textwidget)
        dim1b.add_widget(Button(border = [0,0,0,0],background_normal = asset+"3.png",background_down = asset+"3.png",size_hint_x = None, width = 64))
        
        image1_parent = RelativeLayout(cols = 1, size_hint = (None,None), size = (50,50))
        dim1b.add_widget(image1_parent)
        dim1b.add_widget(Label(size_hint_x = None, width = ((Window.width-382)/2)))
        
        dim1.add_widget(Image(pos_hint = {'y': 1},opacity = .12,source = color + "3.png", keep_ratio = False , allow_stretch = True, size_hint_y = None, height = dp(1)))
        dim1.add_widget(dim1b)
        dim1.add_widget(Image(source = color + "3.png",opacity = .12, keep_ratio = False , allow_stretch = True, size_hint_y = None, height = dp(1)))

            

 
 
        self.lay.add_widget(open_filtros)
        self.lay.add_widget(self.lay_dim)
        
        for i in self.temp[0][1]:
            newwidget = ToggleButton(background_normal = color +"16.png",markup = True,group = "Account_Receivable", text =C4+i,valign = 'middle',text_size = (Window.width/2 -dp(25), dp(36)), font_size = 16)
            
            newwidget.bind(on_press = lambda x: self.set_FiltrarCampo(0,x.text[len(C4):]))
            self.lay_dim.add_widget(newwidget)
            
            
        pariente.add_widget(Image(size_hint_y = None, height = 71,opacity = 1, source =color+ "16.png", keep_ratio = False , allow_stretch = True))
        pariente.add_widget(Button(background_normal = color + "16.png",text = C4+"Seleccionar Vendedores",text_size = (Window.width - 50 , dp(50)),valign = 'middle', halign = 'left',size_hint_y = None , height = '50dp', markup = True, font_size = '24sp')) 
        relat1 = RelativeLayout(size_hint_y = None, height = 100)
        relat1.add_widget(Image(size_hint_y = 1,opacity = 1, source =color+ "16.png", keep_ratio = False , allow_stretch = True))
        relat1.add_widget(SizeButton(background_normal = "None",text = C4+"A continuacion se muestran todos los vendedores registrados, solo debe presionar alguno para seleccionar.",pos_hint = {'center_x':.5, 'center_y':.5},text_size = (Window.width *.75 , 100),valign = 'middle', halign = 'center',size_hint_y = None , height = '50dp', markup = True))
        pariente.add_widget(relat1)
        
        pariente.add_widget(Image(size_hint_y = None, height = 50,opacity = 1, source =color+"16.png", keep_ratio = False , allow_stretch = True))
        pariente.add_widget(Image(source = color + "16.png", height = 25,size_hint_y = None, keep_ratio= False, allow_stretch = True))
        pariente.add_widget(dim1)
        pariente.add_widget(Image(source = color + "16.png", height = 25,size_hint_y = None, keep_ratio= False, allow_stretch = True))
        
        pariente.add_widget(self.lay)
        pariente.add_widget(Calendar())
        self.temp = kwargs['temp']
        for i in self.temp[2][0]:
            #print i

            item = Vendedores_Item(managing = self.set_current, item = i, temp = self.temp)
            item_toggle = ToggleButton(on_release = lambda x: self.toggle(item = x,sc = kwargs["sc"],vtxt = kwargs["vtxt"]),opacity = .24,background_normal = color +"16.png",markup = True,group = "Account_Receivable",valign = 'middle',text_size = (Window.width/2 -dp(25), dp(36)), font_size = 16)
            item.add_widget(item_toggle)
            
                
            pariente.add_widget(item)
            pariente.height += 324 


        pariente_scroll.add_widget(pariente)
        self.screen1.add_widget(pariente_scroll)
        
        
        self.sc.add_widget(self.screen1)
        self.sc.add_widget(self.screen2)
        self.sc.add_widget(self.screen3)
        self.add_widget(Image(size_hint_y = 1,opacity = 1, source =color+ "16.png", keep_ratio = False , allow_stretch = True))
        #self.add_widget(Image(size_hint_y = 1,opacity = .05, source =color+ "3.png", keep_ratio = False , allow_stretch = True))
        self.add_widget(self.sc)
        
        self.screen3_parent = GridLayout(cols = 1)
        self.screen3_parent.add_widget(Label(size_hint_y = None, height = 71))

        self.Desctxt = CustTextInput("Descripcion","Descripcion","Descripcion")
        self.FechaHtxt = CustTextInput("Fecha Hora Creada","Fecha Hora Creada","Fecha Hora Creada")
        self.Tipotxt = CustTextInput("Tipo","Tipo","Tipo")
        self.EntregFtxt = CustTextInput("Entregar Factura","Entregar Factura","Entregar Factura")
        self.FechaHAtxt = CustTextInput("Fecha Hora A","Fecha Hora A","Fecha Hora A")
        self.FechaHBtxt = CustTextInput("Fecha Hora B","Fecha Hora B","Fecha Hora B")
        self.FechaHRtxt = CustTextInput("Fecha Hora_Realizada","Fecha Hora_Realizada","Fecha Hora_Realizada")
        self.Vendedortxt = CustTextInput("Vendedor","Vendedor","Vendedor")
        
        self.screen3_parent.add_widget(self.Desctxt)
        self.screen3_parent.add_widget(self.FechaHtxt)
        self.screen3_parent.add_widget(self.Tipotxt)
        self.screen3_parent.add_widget(self.EntregFtxt)
        self.screen3_parent.add_widget(self.FechaHAtxt)
        self.screen3_parent.add_widget(self.FechaHBtxt)
        self.screen3_parent.add_widget(self.FechaHRtxt)
        self.screen3_parent.add_widget(self.Vendedortxt)
        
        self.screen3_parent.add_widget(Button(text = C4+"Completar", size_hint_y = None, height = dp(61), background_normal = "", background_down = ""))
    def toggle(self,**kwargs):
        kwargs["item"].parent.item, "PROBANDO"
        self.seleccionado = kwargs["item"].parent.item
        kwargs["vtxt"].input0.text = self.seleccionado["first_name"] +" "+ self.seleccionado["last_name"] 
        kwargs["sc"].current = "Encargar pedido"
        
    def confirmar_data(self):
        self.Schedule_item = {
            "idline": 0,
            "Tipo": "",
            "Fecha_Hora_B": null,
            "Fecha_Hora_A": null,
            "fecha_hora": null,
            "Vendedor": null,
            "descripcion": "",
            "codigo": "",
            "Fecha_Hora_Realizada": null,
            "id": int(len(self.temp[1][0])+1),
            "Entrega_Factura": null
        }
        #self.connect(tableid = 1, jsondata = self.Schedule_item)
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
    def add_item(self):
        pariente.add_widget(Entregas_Item(managing = self.set_current))
        
    def set_current(self,setting): 
        self.sc.current = setting
        if setting == "Examinar documento":
            self.screen2.clear_widgets()
            #self.screen2.add_widget(Image())
            scroll = ScrollView()
            screen2_pariente = GridLayout(cols = 1, size_hint_y = None, height = 1000)
            scroll.add_widget(screen2_pariente)
            self.screen2.add_widget(Image(size_hint_y = 1,opacity = 1, source =color+ "16.png", keep_ratio = False , allow_stretch = True))
            self.screen2.add_widget(scroll)
            
            campo = ["Fecha:\n",
                      "Vencimiento:\n",
                      "Monto neto:\n",
                      "Balance:\n",
                      "Total:\n",    
                      "Monto a pagar:\n",
                      "Descuento:\n",
                      "Nuevo Balance:\n",
                      "Estado:\n[/color][color=#00FF00]",
            ]
            pariente = GridLayout(cols = 1, padding = [5,25,5,0], size_hint_y = None, height = 300)
            Title = Label(valign = 'middle',halign = 'left',text_size = (Window.width- 35,24),markup = True,text = C4 + "[size=18]Factura No.: " + "[b]01244536", size_hint_y = None, height = 38)
            pariente2 = GridLayout(cols = 2, padding = [5,0,5,0])
            

            pariente.add_widget(Title)
            pariente.add_widget(pariente2)
            
      
            for i in range(9): 
                if ((i+1)%2) < 1:
                    pariente2.add_widget(Label(valign = 'bottom',halign = 'right',text_size = (Window.width/2 -25,40),markup = True,text = C4 + campo[i] + "[b]data", size_hint_y = None, height = 44))
                    pariente2.add_widget(Image(opacity = .14,source = color + "3.png",size_hint_y = None , height = 2, keep_ratio = False , allow_stretch = True))
                    pariente2.add_widget(Image(opacity = .14,source = color + "3.png",size_hint_y = None , height = 2, keep_ratio = False , allow_stretch = True))
                else:    
                    pariente2.add_widget(Label(valign = 'bottom',halign = 'left',text_size = (Window.width/2  -25,40),markup = True,text = C4 + campo[i] + "[b]data", size_hint_y = None, height = 44))

                    
                    
            self.parent_scrollview2 = ScrollView(do_scroll_x = True, do_scroll_y = False, size_hint_y = None, height = 150)
            self.scrollview2_parent = GridLayout(rows = 4, cols = 6, size_hint_x = None, width = 700)
            self.scrollview2_parent.bind(minimum_width = self.scrollview2_parent.setter('width'))
            self.parent_scrollview2.add_widget(self.scrollview2_parent)
            rowsset1 = [
            ["M","0 30","31 60","61 90","91 120","121 +"],
            ["Balance","470,000.00","80,000.00","","","15,000.00"],
            ["Porciento","83.40%","14.00%","","","2.60%"],
            ]
            for row in rowsset1:
                for i in row:
                    settimg = color + "16bb.png" 
                    if (i == "M")or(i == "Balance")or(i=="Porciento"): 
                        b = ''
                        settimg = color + "16b.png" 
                    else:
                        b = '[b]'
                    self.scrollview2_parent.add_widget(Button(background_normal = settimg,text = C4+b+i,markup= True,font_size = 16))
            
            B_pariente = GridLayout(cols = 1, padding = [5,25,5,0], spacing = 5)
            B_pariente.add_widget(Label(valign = 'middle',halign = 'left',text_size = (Window.width- 35,24),markup = True,text = C4 + "[size=18][b]Detalles", size_hint_y = None, height = 38))
            for i in range(5):
                objeto_parent = RelativeLayout(size_hint_y = None, height = 84)
                objeto_parent.add_widget(Image(source = color + '16bb.png', keep_ratio = False, allow_stretch = True , size_hint = (.95,.95), pos_hint = {'center_x':.5, 'center_y':.5}))
                objeto = GridLayout(cols = 2, padding = [7,7,7,7])
                objeto.add_widget(Label(valign = 'middle',halign = 'left',text_size = (Window.width/2 - 35,40),markup = True,text = C4 + "Objeto:\n[b]data", size_hint_y = 1, height = 38))
                objeto.add_widget(Label(valign = 'middle',halign = 'right',text_size = (Window.width/2 - 35,40),markup = True,text = C4 + "Cantidad:\n[b]data", size_hint_y = 1, height = 38))
                objeto.add_widget(Label(valign = 'middle',halign = 'left',text_size = (Window.width/2 - 35,40),markup = True,text = C4 + "Clasificacion:\n[b]data", size_hint_y = 1, height = 38))
                objeto.add_widget(Label(valign = 'middle',halign = 'right',text_size = (Window.width/2 - 35,40),markup = True,text = C4 + "Precio:\n[b]RD$ data", size_hint_y = 1, height = 38))
                objeto_parent.add_widget(objeto)
                B_pariente.add_widget(objeto_parent)

            #screen2_pariente.add_widget(self.parent_scrollview2)
           
            screen2_pariente.add_widget(pariente)
            screen2_pariente.add_widget(B_pariente)
            screen2_pariente.add_widget(Button(on_release = lambda x: self.set_current(None,"main"),size_hint_y = None,markup = True, background_normal = color + "16.png", height = 74, text = C4+"[size=17][b]volver"))
        elif setting == "Encargar pedido":
            self.EntregFtxt.input0.text = xo["cliente"] + xo["emision"]
            self.EntregFtxt.on_click_onit()
            self.EntregFtxt.disabled = True

            
class MyApp(App):
    def build(self):
        return Entregas()
 

if __name__ in ('__main__', '__android__'):
    MyApp().run()

    
    
    
    
    