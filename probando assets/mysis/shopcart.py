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




resource_add_path(os.path.dirname(__file__))
from mysis.clientshow import ClientShow_B
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
    def __init__(self,Marca,Descripcion,clasificacion, precio_1, precio_2,precio_3,unidades, **kwargs):
        super(CartItem, self).__init__(**kwargs)
        self.size_hint_y = None
        self.height = dp(156)
        self.cols = 1
        self.item = kwargs["item"] - 1 
        temp = kwargs["temp"]
        #-------------------------------
        self.marca = temp[4][0][self.item]["marca"]
        self.descripcion = temp[4][0][self.item]["descripcion"]
        self.clasificacion = temp[4][0][self.item]["clasificacion"]
        self.precio_1 = temp[4][0][self.item]["precio_1"]
        self.precio_2 = temp[4][0][self.item]["precio_2"]
        self.precio_3 = temp[4][0][self.item]["precio_3"]
        self.unidades = int(unidades)
        #-------------------------------
        pariente_root = GridLayout(cols = 1)
        pariente_root.add_widget(Button(size_hint_y = None, height = dp(46),halign = 'left',valign = 'middle',text_size = (Window.width - dp(25),dp(46)),markup = True,background_normal = color + "16.png",text = C4+"[b]"+self.marca))
        pariente = GridLayout(cols = 3,padding = [0,dp(18),0,0])
        CartItem_img = Image(size_hint_x = None, width = dp(124),source = asset+ 'alloy-wheel.png')
        texting = C4+self.descripcion+"\n\n[b]"+self.precio_1+" RD$\n"+self.precio_2+" RD$\n"+self.precio_3+" RD$"
        self.CartItem_desc_Descripcion = Button(halign = 'left',valign = 'middle',text_size = (Window.width - dp(184) - dp(25),dp(156)),markup = True,background_normal = color + "16.png",text = texting)
        CartItem_desc2_cuanty = RelativeLayout(size_hint_x = None, width = dp(64))
        self.cuanty_txt = Button(size_hint = (None,None),background_normal = color + "16bb.png", size = (dp(50),dp(50)),markup = True, text = C4 + str(self.unidades), pos_hint = {'center_x':.5,'center_y':.5})
        CartItem_desc2_cuanty.add_widget(self.cuanty_txt)
        pariente.add_widget(CartItem_img)
        pariente.add_widget(self.CartItem_desc_Descripcion)
        pariente.add_widget(CartItem_desc2_cuanty)
        pariente_root.add_widget(pariente)
        self.add_widget(pariente_root)
        
        parienteb = GridLayout(rows = 1 , size_hint_y = None, height = '35dp')
        parienteb.add_widget(Label())
        self.genial = MyButton(markup = True,background_normal = color + "16.png",text = C4+'   [b]Remover',font_size = '13sp', on_release = lambda x: self.delete_anim(x.parent.parent))
        parienteb.add_widget(self.genial)

        self.bh = MyButton(markup = True,background_normal = color + "16.png",text = C4+'    Guardar   ',font_size = '13sp', on_release = lambda x: self.delete_anim(x.parent.parent))
        parienteb.add_widget(self.bh)
        self.add_widget(parienteb)
        self.add_widget(Image(opacity = .24,size_hint_y = None, height = 1 , source = color + "2.png", keep_ratio = False, allow_stretch = True))
    def removebehavior(self): return self.genial
    def returncuanty(self): return  self.cuanty_txt
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
        CartItem_img = Image(size_hint_x = None, width = dp(124),source = asset+ 'alloy-wheel.png')
        self.CartItem_desc_Descripcion = Button(halign = 'left',valign = 'middle',text_size = (Window.width - dp(184) - dp(25),dp(156)),markup = True,background_normal = color + "16.png",text = C4+"[b]Articulo[/b]\n\nArticulo perfecto\npara el hogar\n\n[b]500.00 RD$")
        CartItem_desc2_cuanty = RelativeLayout(size_hint_x = None, width = dp(64))
        self.cuanty_txt = Button(size_hint = (None,None),background_normal = color + "16bb.png", size = (dp(50),dp(50)),markup = True, text = C4 + "0", pos_hint = {'center_x':.5,'center_y':.5})
        CartItem_desc2_cuanty.add_widget(self.cuanty_txt)
        pariente.add_widget(CartItem_img)
        pariente.add_widget(self.CartItem_desc_Descripcion)
        pariente.add_widget(CartItem_desc2_cuanty)
        self.add_widget(pariente)
        
        parienteb = GridLayout(rows = 1 , size_hint_y = None, height = '35dp')
        parienteb.add_widget(Label())
        parienteb.add_widget(MyButton(markup = True,background_normal = color + "16.png",text = C4+'   [b]Remover',font_size = '13sp', on_release = lambda x: self.delete_anim(x.parent.parent)))

        self.bh = MyButton(markup = True,background_normal = color + "16.png",text = C4+'    Mover al Carrito   ',font_size = '13sp', on_release = lambda x: self.delete_anim(x.parent.parent))
        parienteb.add_widget(self.bh)
        self.add_widget(parienteb)
        self.add_widget(Image(opacity = .24,size_hint_y = None, height = 1 , source = color + "2.png", keep_ratio = False, allow_stretch = True))
 
    def returncuanty(self): return  self.cuanty_txt
    def returntext(self): return self.CartItem_desc_Descripcion
    def getbehavior(self): return  self.bh
    def delete_anim(self,x): 
        anim = Animation(opacity = 0,height = 0 , d =.225 , t = 'out_quart')
        def eliminate(one,two): x.parent.remove_widget(x)
        anim.bind(on_complete = eliminate)
        anim.start(x)
        
class StockItem(GridLayout):
    def __init__(self,Marca,Descripcion,clasificacion, precio_1, precio_2,precio_3, **kwargs):
        super(StockItem, self).__init__(**kwargs)
        self.size_hint_y = None
        self.height = dp(250)
        self.cols = 1
        #-------------------------------
        self.item = int(kwargs["item"]["id"])
        self.marca = Marca
        self.descripcion = Descripcion
        self.clasificacion = clasificacion
        self.precio_1 = precio_1
        self.precio_2 = precio_2
        self.precio_3 = precio_3
        self.unidades = 0
        #-------------------------------
        pariente_root = GridLayout(cols = 1)
        pariente_root.add_widget(Button(size_hint_y = None, height = dp(46),halign = 'left',valign = 'middle',text_size = (Window.width - dp(25),dp(46)),markup = True,background_normal = color + "16.png",text = C4+"[b]"+Marca))
        pariente = GridLayout(cols = 3,padding = [0,dp(0),0,0])
        CartItem_img = Image(size_hint_x = None, width = dp(124),source = asset+ 'alloy-wheel.png')
        texting = C4+"\nPrecio[sup]1[/sup]:\n[b]RD$"+precio_1+"[/b]\nPrecio[sup]2[/sup]:\n[b]RD$"+precio_2+"[/b]\nPrecio[sup]3[/sup]:\n[b]RD$"+precio_3
        self.CartItem_desc_Descripcion = Button(halign = 'left',valign = 'middle',text_size = (Window.width - dp(184) - dp(25),dp(250 - 96)),markup = True,background_normal = color + "16.png",text = texting)
        self.CartItem_desc_Descripcion2 = Button(halign = 'left',valign = 'top',text_size = (Window.width - dp(184) - dp(25),dp(60)), size_hint_y = None, height = 50,markup = True,background_normal = color + "16.png",text = C4 + Descripcion)
        CartItem_desc2_cuanty = RelativeLayout(size_hint_x = None, width = dp(64))
        self.cuanty_txt = Button(size_hint = (None,None),background_normal = color + "16bb.png", size = (dp(50),dp(50)),markup = True, text = C4 + "0", pos_hint = {'center_x':.5,'center_y':.5})
        CartItem_desc2_cuanty.add_widget(self.cuanty_txt)
        pariente.add_widget(CartItem_img)
        dim = GridLayout(cols = 1)
        dim.add_widget(self.CartItem_desc_Descripcion2)
        dim.add_widget(self.CartItem_desc_Descripcion)
        pariente.add_widget(dim)
        pariente.add_widget(CartItem_desc2_cuanty)
        pariente_root.add_widget(pariente)
        self.add_widget(pariente_root)
        
        parienteb = GridLayout(rows = 1 , size_hint_y = None, height = '35dp')
        parienteb.add_widget(Label())
        
        self.genial = MyButton(markup = True,background_normal = color + "16.png",text = C4+'   [b]Remover',font_size = '13sp')
        parienteb.add_widget(self.genial)

        self.bh = MyButton(markup = True,background_normal = color + "16.png",text = C4+'    Mover al Carrito   ',font_size = '13sp')
        parienteb.add_widget(self.bh)
        self.add_widget(parienteb)
        self.add_widget(Image(opacity = .24,size_hint_y = None, height = 1 , source = color + "2.png", keep_ratio = False, allow_stretch = True))
    def removebehavior(self):return self.genial
    def actualizarcantidad(self):  self.unidades = int(self.cuanty_txt.text[len(C4):])
    def returncuanty(self): return  self.cuanty_txt
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
        self.Toggle = ToggleButton(group='Clientbuttons',text = nombre,opacity = .24, size_hint = (None,None), height = dp(56), background_normal = color + '16.png', width = Window.width - dp(56*2), pos_hint = {'center_x':.5})
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
            
            
class ShopCart(Screen):
    def __init__(self, **kwargs):
        super(ShopCart, self).__init__(**kwargs)
        self.idexadis = {}
        self.opened = []
        self.items = []
        self.connect = kwargs["connect"]
        self.seleccionado = ""
        self.vendedor = ""
        self.creditos = 0
        self.insertar_item = {}
        self.temp = kwargs["temp"]
        self.balance_original = 0
        self.parent_height = Window.height - dp(79)
        self.add_widget(Image(source = color + "16.png",keep_ratio = False, allow_stretch = True))
        self.paint = ScreenManager(y = -71)
        self.paint.transition.duration = .225
        self.paint_screen1 = Screen(name = "1")
        self.paint_screen2 = Screen(name = "2")
        self.paint_screen3 = Screen(name = "3")
        self.paint_screen4 = Screen(name = "4")
        self.paint.add_widget(self.paint_screen1)
        self.paint.add_widget(self.paint_screen2)
        self.paint.add_widget(self.paint_screen3)
        self.paint.add_widget(self.paint_screen4)
        
        emisiontxt = CustTextInput("Emision","Emision","Emision")
        self.clientetxt = CustTextInput("Cliente","Cliente","Cliente")
        self.venctotxt = CustTextInput("vencto","vencto","vencto")
        self.diastxt = CustTextInput("dias","dias","dias")
        self.balancetxt = CustTextInput("balance_original","balance_original","balance_original")
        self.Mapapostxt = CustTextInput("Posicion del Mapa","Posicion del Mapa","Posicion del Mapa")
        screen4_root = ScrollView(size_hint_y = None, height = Window.height - dp(79))
        screen4_rootchildp = GridLayout(cols = 1, size_hint_y = None , height = dp(1000))
        screen4_root.add_widget(screen4_rootchildp)
        self.paint_screen4.add_widget(screen4_root)
        screen4_rootchildp.add_widget(Label(size_hint_y = None, height = dp(76)))
        screen4_rootchildp.add_widget(Label(text = C4+"Cuenta por Cobrar",text_size = (Window.width - 50 , dp(50)),valign = 'middle', halign = 'left',size_hint_y = None , height = '50dp', markup = True, font_size = '24sp'))
        screen4_rootchildp.add_widget(Image(size_hint_y = None, height = dp(1), keep_ratio = False, allow_stretch = True, source = color+'3.png', opacity = .14))
        screen4_rootchildp.add_widget(self.clientetxt)
        screen4_rootchildp.add_widget(self.Mapapostxt)

        screen4_rootchildp.add_widget(emisiontxt)
        screen4_rootchildp.add_widget(self.diastxt)
        screen4_rootchildp.add_widget(self.venctotxt)
        screen4_rootchildp.add_widget(self.balancetxt)
        #screen4_rootchildp.add_widget(CustTextInput("creditos","creditos","creditos"))
        
        
        date_1 = datetime.datetime.strptime(datetime.date.today().strftime('%m-%d-%y')  , "%m-%d-%y")
        end_date = date_1 + datetime.timedelta(days=0)
        emisiontxt.returninput().text = str(end_date)[:-9]+"T"+str(end_date)[-8:]+"Z"
        emisiontxt.sizing1()
        emisiontxt.sizing()
        
        self.clientetxt.returninput().text = "[cliente]"
        self.clientetxt.sizing1()
        self.clientetxt.sizing()
        
        date_1 = datetime.datetime.strptime(datetime.date.today().strftime('%m-%d-%y')  , "%m-%d-%y")
        end_date = date_1 + datetime.timedelta(days=30)
        self.venctotxt.returninput().text = str(end_date)[:-9]+"T"+str(end_date)[-8:]+"Z"
        self.venctotxt.sizing1()
        self.venctotxt.sizing()
        
        self.balancetxt.returninput().text = "Vacio"
        self.balancetxt.sizing1()
        self.balancetxt.sizing()
        
        self.diastxt.returninput().bind(on_text_validate = self.dating)
        
        scrollview_screen3_root = ScrollView(size_hint_y = None, height = Window.height)
        self.screen3_root = GridLayout(cols = 1,size_hint_y = None, height = 400)
        
        self.dim1 = RelativeLayout(size_hint_y = None, height = 50)
        self.dim1.add_widget(Image(source = color+"16.png", allow_stretch = True , keep_ratio = False))
        
        self.dim1b = GridLayout(rows = 1 , size_hint_y = None , height = 50)
        self.dim1b.add_widget(Label(size_hint_x = None, width = ((Window.width-382)/2)))
        
        self.dim1b.add_widget(Button(border = [0,0,0,0],background_normal = asset+"1.png",background_down = asset+"1.png",size_hint_x = None, width = 64))
        textwidget = TextInput(multiline=False,size_hint_x = None, width =254,font_size = 16, hint_text = "Buscar Cliente",padding = [0,dp(18),0,0],background_normal = asset+"2.png",background_active = asset+"2.png")
        textwidget.bind(on_text_validate = lambda x: self.Filtrar(3,x.text))
        self.dim1b.add_widget(textwidget)
        self.dim1b.add_widget(Button(border = [0,0,0,0],background_normal = asset+"3.png",background_down = asset+"3.png",size_hint_x = None, width = 64))
        
        image1_parent = RelativeLayout(cols = 1, size_hint = (None,None), size = (50,50))
        self.dim1b.add_widget(image1_parent)
        self.dim1b.add_widget(Label(size_hint_x = None, width = ((Window.width-382)/2)))
        
        self.dim1.add_widget(self.dim1b)

        
        open_filtros = Button(on_release = lambda x: self.openfilter1(x),markup = True, text = C4+"[b]Criterios",font_size = dp(18), background_normal = color + '16.png', background_down = color + '16.png',valign = 'middle',text_size = (Window.width - dp(25),dp(56)), size_hint_y = None, height = dp(56))
        self.lay = GridLayout(cols = 1, size_hint_y = None , height = dp(56))
        self.lay_dim = GridLayout(cols = 2, opacity = 0.)
        self.lay.add_widget(open_filtros)
        self.lay.add_widget(self.lay_dim)
        self.root = kwargs["root"]
        for i in self.temp[3][1]:
            newwidget = ToggleButton(background_normal = color +"16.png",markup = True,group = "Clientes", text =C4+i,valign = 'middle',text_size = (Window.width/2 -dp(25), dp(36)), font_size = 16)
            newwidget.bind(on_press = lambda x: self.root.set_FiltrarCampo(3,x.text[len(C4):]))
            self.lay_dim.add_widget(newwidget)


        self.screen3_root.add_widget(Label(size_hint_y = None, height = dp(56)))
        self.screen3_root.add_widget(Label(size_hint_y = None, height = dp(16)))
        self.screen3_root.add_widget(self.dim1)
        self.screen3_root.add_widget(self.lay)
        scrollview_screen3_root.add_widget(self.screen3_root)
        self.paint_screen3.add_widget(scrollview_screen3_root)
        pariente_scroll = ScrollView()
        self.pariente = GridLayout(y = dp(0),cols = 1, spacing = 0, size_hint_y = None, height = dp(2000))
        self.pariente.add_widget(Label(size_hint_y = None, height = dp(56)))
        #for i in range(3):
        #    item = CartItem()
        #    item.returncuanty().bind(on_release = lambda x: self.manymenu(x))
        #    item.getbehavior().bind(on_release = lambda x: self.agregarguardados())
        #    self.pariente.add_widget(item)
 

        root = GridLayout(cols = 1,size_hint_y = None, height = Window.height - dp(79))
        root_dim = GridLayout(cols = 1, size_hint_y = None, height = dp(56))
        root_dim1 = GridLayout(cols = 2, size_hint_y = None, height = dp(56))
        root_dim1.add_widget(Button(markup = True,text = C4+"[b]CARRITO", background_normal = color + "16.png",background_down = color + "16.png",on_release = lambda x: self.show_carrito()))
        root_dim1.add_widget(Button(markup = True,text = C4+"[b]GUARDADO", background_normal = color + "16.png",background_down = color + "16.png",on_release = lambda x: self.show_guardados()))
        root_dim.add_widget(root_dim1)
        root_dim.add_widget(Image(size_hint_y = None, height = dp(14),source = "Repeat Grid 20.png",keep_ratio = False, allow_stretch = True))
        pariente_scroll.add_widget(self.pariente)

        root.add_widget(pariente_scroll)
        self.paint_screen1.add_widget(root)
        
        self.add_widget(self.paint)
        bottomtitles = GridLayout(size_hint_y = None, height = dp(56),cols = 3)
        bottomtitles.add_widget(Image(opacity = .24,size_hint_y = None, height = 1 , source = color + "2.png", keep_ratio = False, allow_stretch = True))
        bottomtitles.add_widget(Image(opacity = .24,size_hint_y = None, height = 1 , source = color + "2.png", keep_ratio = False, allow_stretch = True))
        bottomtitles.add_widget(Image(opacity = .24,size_hint_y = None, height = 1 , source = color + "2.png", keep_ratio = False, allow_stretch = True))   
        self.total = Button(markup = True,background_normal = color + "16.png",text = C4+'[b]Total de\n0 Items',font_size = '13sp')
        bottomtitles.add_widget(self.total)
        self.totalrd = Button(markup = True,background_normal = color + "16.png",text = C4+'0.00 RD$',font_size = '13sp')
        bottomtitles.add_widget(self.totalrd)
        self.real = Button(markup = True,background_normal = color + "16.png",text = C4+'[b]Confirmar',on_release = lambda x: self.show_confirmacion(),font_size = '16sp')
        bottomtitles.add_widget(self.real)
        
        self.add_widget(bottomtitles)
        
        #------------------------------------------------------
        pariente2_root = ScrollView(size_hint_y = None, height = Window.height - dp(79))
        self.pariente2 = GridLayout(cols = 1, size_hint_y = None, height = dp(1000))
        self.pariente2.add_widget(Label(size_hint_y = None, height = dp(56)))
        pariente2_root.add_widget(self.pariente2)
        self.paint_screen2.add_widget(pariente2_root)
        #self.pariente2.add
        self.add_widget(root_dim)
        root_dim.y = Window.height - dp(79) - dp(56)
        
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

            self.screen3_root.clear_widgets()
            self.screen3_root.add_widget(Label(size_hint_y = None, height = dp(56)))
            self.screen3_root.add_widget(Label(size_hint_y = None, height = dp(16)))
            self.screen3_root.add_widget(self.dim1)
            self.screen3_root.add_widget(self.lay)
            def managinx(x,y):
                print x,y
                self.root.screen5sc.current = y
            for i in datos:
                if Tabla == 3:

                    cliente = ClientShow_B(opacity = 0,item = i, temp = self.temp, managing = managinx)
                    #cliente.return_behavior().bind(on_release = lambda x: self.advice(x))
                    self.clientes_root().add_widget(cliente)
                    a = Animation(opacity = 1, d = .5 , t = 'out_quart')
                    
                    def seleccionar(x):
                        self.seleccionado = x
                        print x, "seleccionado"
                    cliente.return_behavior().bind(on_release = lambda x : seleccionar(x.text))
                    self.clientes_root().height += 250
                    a.start(cliente)
                else:
                    pass
        except:
            import traceback
            traceback.print_exc()
    def returncliente(self):
        return self.clientetxt.selfTextInput()
    def returnmappos(self): 
        self.Mapapostxt.selfTextInput().text = "0"
        self.Mapapostxt.sizing1()
        self.Mapapostxt.sizing()
        return self.Mapapostxt.selfTextInput()
    def clientes_root(self): return self.screen3_root
    def manymenu(self,item,objecto):
        try:
            for i in self.opened: i.parent.remove_widget(i)
            self.opened[:] = []
            def plus(x): 
                item.text = C4 + str(int(item.text[len(C4):]) + 1)
                objecto.unidades += 1
                
                total = 0
                total1 = 0
                for i in self.pariente.children:
                    try:
                        total += i.unidades
                        total1 += (float(i.precio_1) * float(i.unidades))
                        print i.unidades
                        print i.marca
                    except:
                        import traceback
                        traceback.print_exc()
                self.total.text = C4+'[b]Total de\n'+str(total)+' Items'
                self.totalrd.text = C4+str(total1)+' RD$'
                self.balancetxt.returninput().text = str(total1)+' RD$'
                
            def less(x): 
                item.text = C4 + str(int(item.text[len(C4):]) - 1)
                objecto.unidades -= 1
                
                total = 0
                total1 = 0
                for i in self.pariente.children:
                    try:
                        total += i.unidades
                        total1 += (float(i.precio_1) * float(i.unidades))
                        print i.unidades
                        print i.marca
                    except:
                        import traceback
                        traceback.print_exc()
                self.total.text = C4+'[b]Total de\n'+str(total)+' Items'
                self.totalrd.text = C4+str(total1)+' RD$'
                self.balancetxt.returninput().text = str(total1)+' RD$'  
                
            manymenu_parent = GridLayout(y = dp(-56),rows = 1, size_hint_y = None, height = dp(56), opacity = .94)
            manymenu_parent.add_widget(Button(background_normal = color + "3.png",background_down = color + "2.png",text = "-", on_release = lambda x: less(x)))
            def close(x):
                anim = Animation(y = dp(-56), d = .225 , t = 'in_expo')
                def eliminate_x(): x.parent.parent.remove_widget(x.parent)
                #anim.bind(on_complete = lambda a,b: eliminate_x())
                anim.start(x.parent)

                
            manymenu_parent.add_widget(Button(background_normal = color + "3.png",background_down = color + "2.png",text = "close", on_release = lambda x: close(x)))
            manymenu_parent.add_widget(Button(background_normal = color + "3.png",background_down = color + "2.png",text = "+", on_release = lambda x: plus(x)))
            self.add_widget(manymenu_parent)
            anim = Animation(y = 0, d = .225 , t = 'out_expo')
            anim.start(manymenu_parent)
            self.opened.append(manymenu_parent)

            
            
            
        except:
            pass
        total = 0
        total1 = 0

        
    def dating(self,x):
        date_1 = datetime.datetime.strptime(datetime.date.today().strftime('%m/%d/%y')  , "%m/%d/%y")
        end_date = date_1 + datetime.timedelta(days= int(self.diastxt.returninput().text))
        self.venctotxt.returninput().text = str(end_date)[:-9]+"T"+str(end_date)[-8:]+"Z"
        
    def openfilter1(self,object):
        print "hola"
        print object.parent.height
        if object.parent.height == dp(56):
            anim1 = Animation(height = dp(400), d = .225 , t = 'out_expo')
            anim2 = Animation(opacity = 1, d = .225 , t = 'out_expo')
            anim1.start(object.parent)
            anim2.start(object.parent.children[0])
        elif object.parent.height == dp(400):
            anim1 = Animation(height = dp(56), d = .225 , t = 'out_expo')
            anim2 = Animation(opacity = 0, d = .225 , t = 'out_expo')
            anim1.start(object.parent)
            anim2.start(object.parent.children[0])
    def advice(self, item):
        advice_widget = Button(background_normal = color+'2.png',opacity = 0.,markup = True,text_size = (Window.width - dp(25),dp(56)),valign = 'middle',halign = 'center',font_size = '16sp',text = "Cliente [b][Nombre del Cliente][/b] Seleccionado",size_hint_y = None, height = dp(56), y = 0)
        self.add_widget(advice_widget)
        anim = Animation(opacity = 1.,y =  dp(56), d = .3 , t = 'out_expo') + Animation(opacity = 0.,y =
        0, d = .3 , t = 'in_expo')
        def change(x,y): self.remove_widget(advice_widget)
        anim.bind(on_complete = change)
        anim.start(advice_widget)
        print item.text
        self.clientetxt.selfTextInput().text = item.text
    def redadvice(self):
        advice_widget = Button(background_normal = color+'1.png',opacity = 0.,markup = True,text_size = (Window.width - dp(25),dp(56)),valign = 'middle',halign = 'center',font_size = '16sp',text = "El Cliente ha vencido su credito.",size_hint_y = None, height = dp(56), y = 0)
        self.add_widget(advice_widget)
        anim = Animation(opacity = 1.,y =  dp(56), d = .3 , t = 'out_expo') + Animation(opacity = 0.,y =
        0, d = .3 , t = 'in_expo')
        def change(x,y): self.remove_widget(advice_widget)
        anim.bind(on_complete = change)
        anim.start(advice_widget)
        
    def show_carrito(self):self.paint.current = "1"
    def show_guardados(self):self.paint.current = "2"
    def show_confirmacion(self,*args):
        if self.paint.current == "3": 
            try:
                if args[0] == "error":
                    self.redadvice()
            except:
                pass
            self.paint.current = "4"
        elif self.paint.current == "4": 
            import datetime
            x = datetime.datetime.now()
            y = str(x).replace(" ", "T")
            y += "Z"
            id = len(self.temp[0][0]) + 1
            objetos = []
            
            self.insertar_item = {
            "estado_entrega": "Sin entregar",
            "cliente": int(self.seleccionado),
            "vendedor": self.vendedor,
            "emision": y,
            "vencto": self.venctotxt.input0.text,
            "dias": int(self.diastxt.input0.text),
            "no_factura": "00000"+str(id),
            "posicion_mapa": self.Mapapostxt.input0.text,
            "balance_actual": "0",
            "balance_original": self.balancetxt.input0.text[:-4],
            "id": int(id),
            "idobjetos": str(self.items)[1:-1].replace(' ',''),
            "creditos": "0",
            "authorizada": "No",
            }

    


            
            self.connect(tableid = 0 , jsondata = self.insertar_item)
            print "DATA ENVIADA"
            self.paint.current = "1"
        else: self.paint.current = "3"
    def agregarguardados(self):
        guardadoitem = SavedItem()
        guardadoitem.getbehavior().bind(on_release = lambda x:self.agregarcarrito())
        
        self.pariente2.add_widget(guardadoitem)
    def agregarcarrito(self,Marca,Descripcion,clasificacion, precio_1, precio_2,precio_3,unidades,**kwargs):
     
        item = CartItem(Marca,Descripcion,clasificacion, precio_1, precio_2,precio_3,unidades,temp = self.temp, item = kwargs["item"])
        item.getbehavior().bind(on_release = lambda x: item.actualizarcantidad())
        item.getbehavior().bind(on_release = lambda x: self.shopcart.agregarcarrito(item.marca,item.descripcion,item.clasificacion,item.precio_1,item.precio_2,item.precio_3,item.unidades))
        item.returncuanty().bind(on_release = lambda x: self.manymenu(x,item))
        def unico():
            print self.idexadis[str(item.marca + item.descripcion)]
            self.idexadis[str(item.marca + item.descripcion)] -= 1
            print self.idexadis[str(item.marca + item.descripcion)]
        item.removebehavior().bind(on_release = lambda x: unico())
        items = []
        for i in self.pariente.children:
            try:
                items.append(i.item)
            except:
                pass
        try:
            items.index(item.item)
        except:
            self.pariente.add_widget(item)
            for i in range(unidades):
                self.items.append(item.item)
            

            
           
                
            
        
        total = 0
        total1 = 0
        
        for i in self.pariente.children:
            try:
                total += i.unidades
                total1 += (float(i.precio_1) * float(i.unidades))
                print i.unidades
                print i.marca
            except:
                import traceback
                traceback.print_exc()
        self.total.text = C4+'[b]Total de\n'+str(total)+' Items'
        self.totalrd.text = C4+str(total1)+' RD$'
        self.balancetxt.returninput().text = str(total1)+' RD$'

            
  
            

class MyApp(App):
    def build(self):
        return ShopCart()
 

if __name__ in ('__main__', '__android__'):
    MyApp().run()

    
    
    
    
    