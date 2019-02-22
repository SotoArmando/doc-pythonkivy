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
from kivy.properties import (ObjectProperty, NumericProperty, OptionProperty,
                             BooleanProperty, StringProperty)
from kivy.resources import resource_add_path
from kivy.lang import Builder
import os.path

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
class MyButton(Button):
    pass
class CleanButton(RelativeLayout):
    def __init__(self,i_img,i_text, **kwargs):
        super(CleanButton, self).__init__(**kwargs)
        self.add_widget(Image(source = color + '16.png', keep_ratio = False, allow_stretch = True))
        self.size_hint_y = None
        self.height = '51dp'
        mywid = GridLayout(cols = 5,padding = [dp(8),0,dp(0),0])
        mywid.add_widget(ImageButton(source = asset + i_img +".png",size_hint_x = None, width = '52dp'))
        mywid.add_widget(Label(size_hint_x = None , width = '8dp'))
        mywid.add_widget(MyButton(valign = 'middle',background_normal = color+'16.png',markup = True,font_size = '16sp',text = C4+i_text))
        mywid.add_widget(Label())
        mywid.add_widget(CheckBox(background_checkbox_normal = asset + "ic_check_box_outline_blank_bl.png",background_checkbox_down = asset + "ic_check_box_black_24px.png",))
        
        self.add_widget(mywid)
class CartItem(GridLayout):
    def __init__(self, **kwargs):
        super(CartItem, self).__init__(**kwargs)
        self.size_hint_y = None
        self.height = dp(156)
        self.cols = 1
        
        pariente = GridLayout(cols = 3,padding = [0,dp(18),0,0])
        CartItem_img = Image(size_hint_x = None, width = dp(124),source = color + '5.png')
        self.CartItem_desc_Descripcion = Button(markup = True,background_normal = color + "16.png",text = C4+"[b]Articulo[/b]\n\nArticulo perfecto\npara el hogar\n\n[b]500.00 RD$")
        CartItem_desc2_cuanty = RelativeLayout(size_hint_x = None, width = dp(64))
        CartItem_desc2_cuanty.add_widget(Button(size_hint = (None,None),background_normal = color + "16bb.png", size = (dp(50),dp(50)),markup = True, text = C4 + "0", pos_hint = {'center_x':.5,'center_y':.5}))
        pariente.add_widget(CartItem_img)
        pariente.add_widget(self.CartItem_desc_Descripcion)
        pariente.add_widget(CartItem_desc2_cuanty)
        self.add_widget(pariente)
        
        parienteb = GridLayout(rows = 1 , size_hint_y = None, height = '35dp')
        parienteb.add_widget(Label())
        parienteb.add_widget(MyButton(markup = True,background_normal = color + "16.png",text = C4+'   [b]Remover',font_size = '13sp', on_release = lambda x: self.delete_anim(x.parent.parent)))

        self.bh = MyButton(markup = True,background_normal = color + "16.png",text = C4+'    Guardar   ',font_size = '13sp', on_release = lambda x: self.delete_anim(x.parent.parent))
        parienteb.add_widget(self.bh)
        self.add_widget(parienteb)
        self.add_widget(Image(opacity = .24,size_hint_y = None, height = 1 , source = color + "2.png", keep_ratio = False, allow_stretch = True))
    def returntext(self): return self.CartItem_desc_Descripcion
    def getbehavior(self): return  self.bh
    def delete_anim(self,x): 
        anim = Animation(opacity = 0,height = 0 , d =.225 , t = 'out_quart')
        def eliminate(one,two): x.parent.remove_widget(x)
        anim.bind(on_complete = eliminate)
        anim.start(x)
        
    
class SavedItem(GridLayout):
    def __init__(self, **kwargs):
        super(SavedItem, self).__init__(**kwargs)
        self.size_hint_y = None
        self.height = dp(156)
        self.cols = 1
        
        pariente = GridLayout(cols = 3,padding = [0,dp(18),0,0])
        CartItem_img = Image(size_hint_x = None, width = dp(124),source = color + '5.png')
        self.CartItem_desc_Descripcion = Button(markup = True,background_normal = color + "16.png",text = C4+"[b]Articulo[/b]\n\nArticulo perfecto\npara el hogar\n\n[b]500.00 RD$")
        CartItem_desc2_cuanty = RelativeLayout(size_hint_x = None, width = dp(64))
        CartItem_desc2_cuanty.add_widget(Button(size_hint = (None,None),background_normal = color + "16bb.png", size = (dp(50),dp(50)),markup = True, text = C4 + "0", pos_hint = {'center_x':.5,'center_y':.5}))
        pariente.add_widget(CartItem_img)
        pariente.add_widget(self.CartItem_desc_Descripcion)
        pariente.add_widget(CartItem_desc2_cuanty)
        self.add_widget(pariente)
        
        parienteb = GridLayout(rows = 1 , size_hint_y = None, height = '35dp')
        parienteb.add_widget(Label())
        parienteb.add_widget(MyButton(markup = True,background_normal = color + "16.png",text = C4+' Remover  ',font_size = '13sp', on_release = lambda x: delete_anim(x)))
        self.bh = MyButton(markup = True,background_normal = color + "16.png",text = C4+'    Pasar al Carrito   ',font_size = '13sp', on_release = lambda x: delete_anim(x))
        parienteb.add_widget(self.bh)
        self.add_widget(parienteb)
        self.add_widget(Image(opacity = .24,size_hint_y = None, height = 1 , source = color + "2.png", keep_ratio = False, allow_stretch = True))
    def returntext(self): return self.CartItem_desc_Descripcion    
    def getbehavior(self): return  self.bh
    def delete_anim(self,x): 
        anim = Animation(opacity = 0,height = 0 , d =.225 , t = 'out_quart')
        def eliminate(one,two): x.parent.remove_widget(x)
        anim.bind(on_complete = eliminate)
        anim.start(x)
class ClientButton(RelativeLayout):
    def __init__(self,nombre,subdato, **kwargs):
        super(ClientButton, self).__init__(**kwargs)
        self.size_hint_y = None ; self.height = dp(56)
        self.clientnombre = nombre
        self.clientsubdato = subdato
        self.disp = True
        self.add_widget(Image(source = color + "16.png", allow_stretch = True, keep_ratio = False))
        pariente = GridLayout(rows = 3)
        titles = GridLayout(rows = 1 , size_hint_y = None, height = dp(56))
        titles.add_widget(Image(source = asset + 'Group 1.png', allow_stretch = False, keep_ratio = True,size_hint_x = None, width = dp(56)))
        titles.add_widget(Button(text_size = (Window.width - dp(56*2) - dp(25), dp(56)),valign = 'middle',markup = True,text = C4+"[b]"+nombre+"[/b]\n"+subdato, background_normal = color + '16.png'))
        #----------------------animated
        scatter0_parent = GridLayout(cols = 1, size_hint_x = None, width = dp(56))
        scatter0_parent_child = RelativeLayout()
        scatter0 = Scatter()
        scatter0_child = ImageButton(size_hint = (None,None), size = (dp(56),dp(56)), source = asset + 'Group 3.png',allow_stretch = True , keep_ratio = False, on_release = lambda x: self.animate(x))
        scatter0_child.bind(on_release = lambda x: self.open())
        scatter0_parent.add_widget(scatter0_parent_child)
        scatter0_parent_child.add_widget(scatter0)
        scatter0.add_widget(scatter0_child)
        
        titles.add_widget(scatter0_parent)
        pariente.add_widget(titles)
        #--------------------------------------
        self.titles_data = GridLayout(cols = 2,opacity = 0.)
        for i in range(10):self.titles_data.add_widget(Label(valign = 'middle',text_size = (Window.width/2,dp(200/5)),markup = True,halign = 'center',text = C4+"[b][campo]: [/b] Base de datos no conectada."))
        
        shadow_parent = GridLayout(cols = 1,size_hint_y = None, height = dp(0))
        shadow_parent.add_widget(Image(source = "Repeat Grid 20.png",allow_stretch = True, keep_ratio = False, height = dp(25)))
        pariente.add_widget(shadow_parent)
        pariente.add_widget(self.titles_data)
        self.Toggle = ToggleButton(group='Clientbuttons',text = nombre ,opacity = .24, size_hint = (None,None), height = dp(56), background_normal = color + '16.png', width = Window.width - dp(56*2), pos_hint = {'center_x':.5})
        self.add_widget(pariente)
        self.add_widget(self.Toggle)
    def return_behavior(self): return self.Toggle
    def open(self):
        if self.titles_data.opacity == 0.:
            anim = Animation(height = dp(256), d = .255, t = 'out_expo')
            anim1 = Animation(opacity = 1., d = .255, t = 'out_expo')
            anim2 = Animation(y = dp(200), d = .255, t = 'out_expo')
            anim.start(self)
            anim1.start(self.titles_data)
            anim2.start(self.Toggle)
        elif self.titles_data.opacity == 1.:
            anim = Animation(height = dp(56), d = .255, t = 'out_expo')
            anim1 = Animation(opacity = 0.,  d = .255, t = 'out_expo')
            anim2 = Animation(y = dp(0), d = .255, t = 'out_expo')
            anim.start(self)
            anim1.start(self.titles_data)
            anim2.start(self.Toggle)
            
    def animate(self,object):
        if self.disp == True:
            anim = Animation(size = (dp(50),dp(50)),x = object.x + 3, y = object.y + 3, d = .225/2 , t = 'out_quart') + Animation(size = (dp(56),dp(56)),x = object.x, y = object.y, d = .225/2 , t = 'in_quart')
            self.disp = False
            def change(a,x): self.disp = True
            anim.bind(on_complete = change)
            anim.start(object)
class blackline(Image):
    def __init__(self, **kwargs):
        super(blackline, self).__init__(**kwargs)
        self.size_hint_y = None
        self.height = dp(1)
        self.source = color + "3.png"
        self.keep_ratio = False
        self.allow_stretch = True
        self.opacity = .24
        
class ClientShow(RelativeLayout):
    def __init__(self, **kwargs):
        super(ClientShow, self).__init__(**kwargs)
        self.opened =[]
        
        pariente = GridLayout(cols = 1,size_hint = (.95,None), size = (dp(335),dp(225)), pos_hint = {'center_x':.5,'center_y':.5})
        self.back = Image(source = "Repeat Grid 3.png", keep_ratio = False, allow_stretch = True)
        self.add_widget(self.back)
        self.add_widget(pariente)
        
        self.size_hint_y = None
        self.height = 250
        item = kwargs["item"]
        rows1 = GridLayout(rows = 1, size_hint_y = None, height = 60)
        
        rows1.add_widget(Image(source = asset + "ic_assignment_ind_black_24px.png", keep_ratio = True, allow_stretch = False, size_hint_x = None, width = 64))
        rows1.add_widget(Label(markup = True,text = C4+"[b].: "+ item["cliente"] + '\n' + item["direccion1"],size_hint_y = None ,text_size = ((Window.width * 0.90) - 25, 60), valign = 'middle', height =60))
        pariente.add_widget(rows1)

        #pariente.add_widget(Image(opacity = .54,source = color + "3.png", keep_ratio = False , allow_stretch = True, size_hint_y = None , height = 1))
        
        parienteb = GridLayout(cols = 2, padding = [0,10,0,10], size_hint_y = None, height = 150)
        
        parienteb.add_widget(Label(text = C4+"Identificacion:\n[b]"+item["identificacion"],markup = True,text_size = ((Window.width*0.85)/2, 75), halign = 'left', valign = 'middle'))
        parienteb.add_widget(Label(text = C4+"Correo:\n[b]"+item["correo"],markup = True,text_size = ((Window.width*0.85)/2, 75), halign = 'right', valign = 'middle'))
        Facturas = 0
        Fecha = ["No se ha emitido"]
        Totales = 0
        for i in kwargs["temp"][0][0]:
            if i["cliente"] == item["id"]: 
                Facturas += 1
                Fecha.append(i["emision"])
                Totales += float(i["balance_original"])
            
        
        
        parienteb.add_widget(Label(text = C4+"Facturas:\n[b]" + str(Facturas),markup = True,text_size = ((Window.width*0.85)/2, 75), halign = 'left', valign = 'middle'))
        parienteb.add_widget(Label(text = C4+"Fecha:\n[b]"+ str(Fecha[-1]),markup = True,text_size = ((Window.width*0.85)/2, 75), halign = 'right', valign = 'middle'))
        parienteb.add_widget(Label(text = C4+"",markup = True,text_size = ((Window.width*0.85)/2, 75), halign = 'left', valign = 'middle'))
        parienteb.add_widget(Label(text = C4+"Balance Total:\n[b]RD$"+str(Totales),markup = True,text_size = ((Window.width*0.85)/2, 75), halign = 'right', valign = 'middle'))
        
        
        
        pariente.add_widget(parienteb)
        #pariente.add_widget(Label(size_hint_y = None, height = 60,text = C4+"Nota: [b] deposito para tal excepcion que se ha dado el dia de hoy.",markup = True,text_size = ((Window.width*0.85), 50), halign = 'left', valign = 'middle'))
        self.behavior = Button(opacity = 0, on_release = lambda x: self.opciones(managing = kwargs["managing"]))
        self.add_widget(self.behavior)
    def opciones(self,**kwargs):
        try:
            for i in self.opened:
                i.parent.remove_widget(i)
        except:
            pass
                
        relat = RelativeLayout()
        img = Image(opacity = .0, keep_ratio = False, allow_stretch = True, source = color + "3.png")
        pp = ['Examinar Documento','Realizar pedido', 'Estado de cuenta' ]
        pp1 = ['Examinar Documento','Realizar pedido', 'Estado de cuenta' ]
        
        opciones = GridLayout(cols = 1,opacity = .0,size_hint = (.8,None),height = 250, pos_hint = {'center_x':.5,'center_y':.5})
        for i in range(3): opciones.add_widget(Button(on_release = lambda x: kwargs["managing"](x,x.text[len(C4+"[size=17][b]"):]),halign = 'left', valign = 'middle',text_size = ((Window.width * 0.8)-35,400.0/7.0),background_normal = 'None',background_down = color + '16bb.png',markup = True,text = C4+"[size=17][b]"+pp[i]))
        
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
        
        
class ClientShow_B(RelativeLayout):
    def __init__(self, **kwargs):
        super(ClientShow_B, self).__init__(**kwargs)
        self.opened =[]
        
        pariente = GridLayout(cols = 1,size_hint = (.95,None), size = (dp(335),dp(225)), pos_hint = {'center_x':.5,'center_y':.5})
        self.add_widget(Image(source = "Repeat Grid 3.png", keep_ratio = False, allow_stretch = True))
        self.add_widget(pariente)
        
        self.size_hint_y = None
        self.height = 250
        item = kwargs["item"]
        rows1 = GridLayout(rows = 1, size_hint_y = None, height = 60)
        
        rows1.add_widget(Image(source = asset + "ic_assignment_ind_black_24px.png", keep_ratio = True, allow_stretch = False, size_hint_x = None, width = 64))
        rows1.add_widget(Label(markup = True,text = C4+"[b].: "+ item["cliente"] + '\n' + item["direccion1"],size_hint_y = None ,text_size = ((Window.width * 0.90) - 25, 60), valign = 'middle', height =60))
        pariente.add_widget(rows1)

        #pariente.add_widget(Image(opacity = .54,source = color + "3.png", keep_ratio = False , allow_stretch = True, size_hint_y = None , height = 1))
        
        parienteb = GridLayout(cols = 2, padding = [0,10,0,10], size_hint_y = None, height = 150)
        
        parienteb.add_widget(Label(text = C4+"Identificacion:\n[b]"+item["identificacion"],markup = True,text_size = ((Window.width*0.85)/2, 75), halign = 'left', valign = 'middle'))
        parienteb.add_widget(Label(text = C4+"Correo:\n[b]"+item["correo"],markup = True,text_size = ((Window.width*0.85)/2, 75), halign = 'right', valign = 'middle'))
        Facturas = 0
        Fecha = ["No se ha emitido"]
        Totales = 0
        for i in kwargs["temp"][0][0]:
            if i["cliente"] == item["id"]: 
                Facturas += 1
                Fecha.append(i["emision"])
                Totales += float(i["balance_original"])
            
        
        
        parienteb.add_widget(Label(text = C4+"Facturas:\n[b]" + str(Facturas),markup = True,text_size = ((Window.width*0.85)/2, 75), halign = 'left', valign = 'middle'))
        parienteb.add_widget(Label(text = C4+"Fecha:\n[b]"+ str(Fecha[-1]),markup = True,text_size = ((Window.width*0.85)/2, 75), halign = 'right', valign = 'middle'))
        parienteb.add_widget(Label(text = C4+"",markup = True,text_size = ((Window.width*0.85)/2, 75), halign = 'left', valign = 'middle'))
        parienteb.add_widget(Label(text = C4+"Balance Total:\n[b]RD$"+str(Totales),markup = True,text_size = ((Window.width*0.85)/2, 75), halign = 'right', valign = 'middle'))
        
        
        
        pariente.add_widget(parienteb)
        #pariente.add_widget(Label(size_hint_y = None, height = 60,text = C4+"Nota: [b] deposito para tal excepcion que se ha dado el dia de hoy.",markup = True,text_size = ((Window.width*0.85), 50), halign = 'left', valign = 'middle'))
        self.behavior = Button(opacity = 0, on_release = lambda x: self.opciones(managing = kwargs["managing"]))
        
        #self.add_widget(self.behavior)
        self.Toggle = ToggleButton(group='Clientbuttons',text = str(item["id"]) ,opacity = .24, size_hint = (1,1), height = dp(56), background_normal = color + '16.png', width = Window.width - dp(56*2), pos_hint = {'center_x':.5})
        self.add_widget(self.Toggle)
    def return_behavior(self): return self.Toggle
    def open(self):
        if self.titles_data.opacity == 0.:
            anim = Animation(height = dp(256), d = .255, t = 'out_expo')
            anim1 = Animation(opacity = 1., d = .255, t = 'out_expo')
            anim2 = Animation(y = dp(200), d = .255, t = 'out_expo')
            anim.start(self)
            anim1.start(self.titles_data)
            anim2.start(self.Toggle)
        elif self.titles_data.opacity == 1.:
            anim = Animation(height = dp(56), d = .255, t = 'out_expo')
            anim1 = Animation(opacity = 0.,  d = .255, t = 'out_expo')
            anim2 = Animation(y = dp(0), d = .255, t = 'out_expo')
            anim.start(self)
            anim1.start(self.titles_data)
            anim2.start(self.Toggle)
            
    def animate(self,object):
        if self.disp == True:
            anim = Animation(size = (dp(50),dp(50)),x = object.x + 3, y = object.y + 3, d = .225/2 , t = 'out_quart') + Animation(size = (dp(56),dp(56)),x = object.x, y = object.y, d = .225/2 , t = 'in_quart')
            self.disp = False
            def change(a,x): self.disp = True
            anim.bind(on_complete = change)
            anim.start(object)
        
        
    def opciones(self,**kwargs):
        try:
            for i in self.opened:
                i.parent.remove_widget(i)
        except:
            pass
                
        relat = RelativeLayout()
        img = Image(opacity = .0, keep_ratio = False, allow_stretch = True, source = color + "3.png")
        pp = ['Examinar Documento','Realizar pedido', 'Estado de cuenta' ]
        pp1 = ['Examinar Documento','Realizar pedido', 'Estado de cuenta' ]
        
        opciones = GridLayout(cols = 1,opacity = .0,size_hint = (.8,None),height = 250, pos_hint = {'center_x':.5,'center_y':.5})
        for i in range(3): opciones.add_widget(Button(on_release = lambda x: kwargs["managing"](x,x.text[len(C4+"[size=17][b]"):]),halign = 'left', valign = 'middle',text_size = ((Window.width * 0.8)-35,400.0/7.0),background_normal = 'None',background_down = color + '16bb.png',markup = True,text = C4+"[size=17][b]"+pp[i]))
        
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
        
        
        
class MyApp(App):
    def build(self):
        return ClientShow()
 

if __name__ in ('__main__', '__android__'):
    MyApp().run()

    
    
    
    
    