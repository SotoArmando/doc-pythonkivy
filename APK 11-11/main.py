#!/usr/bin/env python
# -*- coding: utf-8 -*-

import kivy
from kivy.config import Config

Config.set('graphics','borderless', 0)
Config.set('graphics','position','custom')
Config.set('graphics','window_state','visible')
Config.set('graphics','resizable',1)
Config.set('graphics','left',1000)
Config.set('graphics','top',35)
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
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
Window.size = (426,950)
import time
import json
import urllib2
import os

from kivy.uix.accordion import Accordion, AccordionItem
from kivy.base import runTouchApp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.popup import Popup
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.animation import Animation
from kivy.uix.widget import Widget
from kivy.uix.stencilview import StencilView
from kivy.metrics import dp
from kivy.clock import Clock
from kivy.properties import (ObjectProperty, NumericProperty, OptionProperty, BooleanProperty, StringProperty)
from kivy.resources import resource_add_path
from kivy.uix.checkbox import CheckBox

from kivy.lang import Builder
import os.path
from kivy.config import Config
import time
import sys
resource_add_path(os.path.dirname(__file__))


Builder.load_string('''
<NavigationDrawer>:
    size_hint: (1,1)
    _side_panel: sidepanel
    _main_panel: mainpanel
    _join_image: joinimage
    side_panel_width: min(dp(250), 0.5*self.width)
    BoxLayout:
        id: sidepanel
        y: root.y
        x: root.x - \
           (1-root._anim_progress)* \
           root.side_panel_init_offset*root.side_panel_width
        height: root.height
        width: root.side_panel_width
        opacity: root.side_panel_opacity + \
                 (1-root.side_panel_opacity)*root._anim_progress
        canvas:
            Color:
                rgba: (1,1,1,1)
            Rectangle:
                pos: self.pos
                size: self.size
        canvas.after:
            Color:
                rgba: (1,1,1,(1-root._anim_progress)*root.side_panel_darkness)
            Rectangle:
                size: self.size
                pos: self.pos
    BoxLayout:
        id: mainpanel
        x: root.x + \
           root._anim_progress * \
           root.side_panel_width * \
           root.main_panel_final_offset
        y: root.y
        size: root.size
        canvas:
            Color:
                rgba: (1,1,1,1)
            Rectangle:
                pos: self.pos
                size: self.size
        canvas.after:
            Color:
                rgba: (0,0,0,root._anim_progress*root.main_panel_darkness)
            Rectangle:
                size: self.size
                pos: self.pos
    Image:
        id: joinimage
        opacity: min(sidepanel.opacity, 0 if root._anim_progress < 0.00001 \
                 else min(root._anim_progress*40,1))
        source: root._choose_image(root._main_above, root.separator_image)
        mipmap: False
        width: 1
        height: root._side_panel.height
        x: (mainpanel.x - self.width + 1) if root._main_above \
           else (sidepanel.x + sidepanel.width - 1)
        y: root.y
        allow_stretch: True
        keep_ratio: False
''')
class NavigationDrawerException(Exception):
    '''Raised when add_widget or remove_widget called incorrectly on a
    NavigationDrawer.

    '''
class NavigationDrawer(StencilView):

    # Internal references for side, main and image widgets
    _side_panel = ObjectProperty()
    _main_panel = ObjectProperty()
    _join_image = ObjectProperty()

    side_panel = ObjectProperty(None, allownone=True)
    main_panel = ObjectProperty(None, allownone=True)


    # Appearance properties
    side_panel_width = NumericProperty()

    separator_image = StringProperty('')


    # Touch properties
    touch_accept_width = NumericProperty('14dp')
    _touch = ObjectProperty(None, allownone=True)  # The currently active touch

    # Animation properties
    state = OptionProperty('closed', options=('open', 'closed'))
    anim_time = NumericProperty(0.3)
    min_dist_to_open = NumericProperty(0.7)
    _anim_progress = NumericProperty(0)  # Internal state controlling
                                         # widget positions
    _anim_init_progress = NumericProperty(0)

    # Animation controls
    top_panel = OptionProperty('main', options=['main', 'side'])
    _main_above = BooleanProperty(True)

    side_panel_init_offset = NumericProperty(0.5)

    side_panel_darkness = NumericProperty(0.8)

    side_panel_opacity = NumericProperty(1)

    main_panel_final_offset = NumericProperty(1)

    main_panel_darkness = NumericProperty(0)

    opening_transition = StringProperty('out_cubic')

    closing_transition = StringProperty('in_cubic')

    anim_type = OptionProperty('reveal_from_below',
                               options=['slide_above_anim',
                                        'slide_above_simple',
                                        'fade_in',
                                        'reveal_below_anim',
                                        'reveal_below_simple',
                                        ])

    def __init__(self, **kwargs):
        super(NavigationDrawer, self).__init__(**kwargs)
        Clock.schedule_once(self.on__main_above, 0)

    def on_anim_type(self, *args):
        anim_type = self.anim_type
        if anim_type == 'slide_above_anim':
            self.top_panel = 'side'
            self.side_panel_darkness = 0
            self.side_panel_opacity = 1
            self.main_panel_final_offset = 0.5
            self.main_panel_darkness = 0.5
            self.side_panel_init_offset = 1
        if anim_type == 'slide_above_simple':
            self.top_panel = 'side'
            self.side_panel_darkness = 0
            self.side_panel_opacity = 1
            self.main_panel_final_offset = 0
            self.main_panel_darkness = 0
            self.side_panel_init_offset = 1
        elif anim_type == 'fade_in':
            self.top_panel = 'side'
            self.side_panel_darkness = 0
            self.side_panel_opacity = 0
            self.main_panel_final_offset = 0
            self.main_panel_darkness = 0
            self.side_panel_init_offset = 0.5
        elif anim_type == 'reveal_below_anim':
            self.top_panel = 'main'
            self.side_panel_darkness = 0.8
            self.side_panel_opacity = 1
            self.main_panel_final_offset = 1
            self.main_panel_darkness = 0
            self.side_panel_init_offset = 0.5
        elif anim_type == 'reveal_below_simple':
            self.top_panel = 'main'
            self.side_panel_darkness = 0
            self.side_panel_opacity = 1
            self.main_panel_final_offset = 1
            self.main_panel_darkness = 0
            self.side_panel_init_offset = 0

    def on_top_panel(self, *args):
        if self.top_panel == 'main':
            self._main_above = True
        else:
            self._main_above = False

    def on__main_above(self, *args):
        newval = self._main_above
        main_panel = self._main_panel
        side_panel = self._side_panel
        self.canvas.remove(main_panel.canvas)
        self.canvas.remove(side_panel.canvas)
        if newval:
            self.canvas.insert(0, main_panel.canvas)
            self.canvas.insert(0, side_panel.canvas)
        else:
            self.canvas.insert(0, side_panel.canvas)
            self.canvas.insert(0, main_panel.canvas)

    def toggle_main_above(self, *args):
        if self._main_above:
            self._main_above = False
        else:
            self._main_above = True

    def add_widget(self, widget):
        if len(self.children) == 0:
            super(NavigationDrawer, self).add_widget(widget)
            self._side_panel = widget
        elif len(self.children) == 1:
            super(NavigationDrawer, self).add_widget(widget)
            self._main_panel = widget
        elif len(self.children) == 2:
            super(NavigationDrawer, self).add_widget(widget)
            self._join_image = widget
        elif self.side_panel is None:
            self._side_panel.add_widget(widget)
            self.side_panel = widget
        elif self.main_panel is None:
            self._main_panel.add_widget(widget)
            self.main_panel = widget
        else:
            raise NavigationDrawerException(
                'Can\'t add more than two widgets'
                'directly to NavigationDrawer')

    def remove_widget(self, widget):
        if widget is self.side_panel:
            self._side_panel.remove_widget(widget)
            self.side_panel = None
        elif widget is self.main_panel:
            self._main_panel.remove_widget(widget)
            self.main_panel = None
        else:
            raise NavigationDrawerException(
                'Widget is neither the side or main panel, can\'t remove it.')

    def set_side_panel(self, widget):
        '''Removes any existing side panel widgets, and replaces them with the
        argument `widget`.
        '''
        # Clear existing side panel entries
        if len(self._side_panel.children) > 0:
            for child in self._side_panel.children:
                self._side_panel.remove(child)
        # Set new side panel
        self._side_panel.add_widget(widget)
        self.side_panel = widget

    def set_main_panel(self, widget):
        '''Removes any existing main panel widgets, and replaces them with the
        argument `widget`.
        '''
        # Clear existing side panel entries
        if len(self._main_panel.children) > 0:
            for child in self._main_panel.children:
                self._main_panel.remove(child)
        # Set new side panel
        self._main_panel.add_widget(widget)
        self.main_panel = widget

    def on__anim_progress(self, *args):
        if self._anim_progress > 1:
            self._anim_progress = 1
        elif self._anim_progress < 0:
            self._anim_progress = 0
        if self._anim_progress >= 1:
            self.state = 'open'
        elif self._anim_progress <= 0:
            self.state = 'closed'

    def on_state(self, *args):
        Animation.cancel_all(self)
        if self.state == 'open':
            self._anim_progress = 1
        else:
            self._anim_progress = 0

    def anim_to_state(self, state):
        '''If not already in state `state`, animates smoothly to it, taking
        the time given by self.anim_time. State may be either 'open'
        or 'closed'.

        '''
        if state == 'open':
            anim = Animation(_anim_progress=1,
                             duration=self.anim_time,
                             t=self.closing_transition)
            anim.start(self)
        elif state == 'closed':
            anim = Animation(_anim_progress=0,
                             duration=self.anim_time,
                             t=self.opening_transition)
            anim.start(self)
        else:
            raise NavigationDrawerException(
                'Invalid state received, should be one of `open` or `closed`')

    def toggle_state(self, animate=True):
        '''Toggles from open to closed or vice versa, optionally animating or
        simply jumping.'''
        if self.state == 'open':
            if animate:
                self.anim_to_state('closed')
            else:
                self.state = 'closed'
        elif self.state == 'closed':
            if animate:
                self.anim_to_state('open')
            else:
                self.state = 'open'

    def on_touch_down(self, touch):
        col_self = self.collide_point(*touch.pos)
        col_side = self._side_panel.collide_point(*touch.pos)
        col_main = self._main_panel.collide_point(*touch.pos)

        if self._anim_progress < 0.001:  # i.e. closed
            valid_region = (self.x <=
                            touch.x <=
                            (self.x + self.touch_accept_width))
            if not valid_region:
                self._main_panel.on_touch_down(touch)
                return False
        else:
            if col_side and not self._main_above:
                self._side_panel.on_touch_down(touch)
                return False
            valid_region = (self._main_panel.x <=
                            touch.x <=
                            (self._main_panel.x + self._main_panel.width))
            if not valid_region:
                if self._main_above:
                    if col_main:
                        self._main_panel.on_touch_down(touch)
                    elif col_side:
                        self._side_panel.on_touch_down(touch)
                else:
                    if col_side:
                        self._side_panel.on_touch_down(touch)
                    elif col_main:
                        self._main_panel.on_touch_down(touch)
                return False
        Animation.cancel_all(self)
        self._anim_init_progress = self._anim_progress
        self._touch = touch
        touch.ud['type'] = self.state
        touch.ud['panels_jiggled'] = False  # If user moved panels back
                                            # and forth, don't default
                                            # to close on touch release
        touch.grab(self)
        return True

    def on_touch_move(self, touch):
        if touch is self._touch:
            dx = touch.x - touch.ox
            self._anim_progress = max(0, min(self._anim_init_progress +
                                            (dx / self.side_panel_width), 1))
            if self._anim_progress < 0.975:
                touch.ud['panels_jiggled'] = True
        else:
            super(NavigationDrawer, self).on_touch_move(touch)
            return

    def on_touch_up(self, touch):
        if touch is self._touch:
            self._touch = None
            init_state = touch.ud['type']
            touch.ungrab(self)
            jiggled = touch.ud['panels_jiggled']
            if init_state == 'open' and not jiggled:
                if self._anim_progress >= 0.975:
                        self.anim_to_state('closed')
                else:
                    self._anim_relax()
            else:
                self._anim_relax()
        else:
            super(NavigationDrawer, self).on_touch_up(touch)
            return

    def _anim_relax(self):
        '''Animates to the open or closed position, depending on whether the
        current position is past self.min_dist_to_open.

        '''
        if self._anim_progress > self.min_dist_to_open:
            self.anim_to_state('open')
        else:
            self.anim_to_state('closed')

    def _choose_image(self, *args):
        '''Chooses which image to display as the main/side separator, based on
        _main_above.'''
        if self.separator_image:
            return self.separator_image
        if self._main_above:
            return 'navigationdrawer_gradient_rtol.png'
        else:
            return 'navigationdrawer_gradient_ltor.png'

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
class Showcase(FloatLayout):
    pass


class DataItem(SelectableDataItem):
    def __init__(self, text, **kwargs):
        self.text = text
        super(DataItem, self).__init__(**kwargs)


class DataItem_P(SelectableDataItem):
    def __init__(self, text, sub_text, **kwargs):
        self.text = text
        self.sub_text = sub_text
        super(DataItem, self).__init__(**kwargs)


class InterfaceManager(AnchorLayout):
    def __init__(self, **kwargs):
        self.Primerinicio = None
        self.patch = os.path.dirname(os.path.abspath(__file__))
        self.Label7 =Label(text ="[color=#404040]SIN SELECCIONAR" , markup = True)
        self.checkin = os.path.isfile(self.patch + "/data.dat")
        self.checkin2 = os.path.isfile(self.patch + "/loggeduser.data")
        print "ESTE ESSSSSSSSSSSS "+ str(self.checkin)
        self.DatosAdheridos = []
        self.DatosAdheridos2 = []
        
        self.Predet = False
        print self.Primerinicio
        self.Dominio2 = "https://mighty-escarpment-67010.herokuapp.com/API/"
        self.Dominio2 = "http://127.0.0.1:8000/API/"
        self.Dominio2 = "http://g-005.herokuapp.com/API/"
        Tablas = ["Usuario","Categoria","Contacto","Rating", "Menu","Menu_Sub_Categorias","Pedido","Pedidos_Detalles", "Sugerencia", "Plato","Profile"] #falta la tabla "sugerencia".
        #USUARIO PRESENTE
        
        self.UserU = ""
        self.UserPW = ""
        self.UserID = ""
        self.UserNO = ""
        self.UserDIR = []
        self.UserPriv = ""
        self.total1= 0
        self.TiendaSolicitada = 0
        #                   

        self.images = self.patch + '/images/'
        self.UsuarioNO = 0
        self.CategoriaNO = 0
        self.ContactoNO = 0
        self.RatingNO = 0
        self.MenuNO = 0
        self.Menu_Sub_CategoriasNO = 0
        self.PedidoNO = 0
        self.Pedidos_DetallesNO = 0
        self.SugerenciaNO = 0
        self.inventario_objetos = []
        self.inventario_precio = []
        self.inventario_id = []
        self.Total_Txt = Button(background_down = self.images + "blanco.png" ,text = "[color=#404040][b]0.00 RD$",markup = True, background_color = (1,1,1,1), background_normal = self.images + "blanco.png",size_hint_y = None, height = 50)
        self.Subtotal_Txt = Button(background_down = self.images + "blanco.png" ,text = "[color=#404040][b]",markup = True, background_color = (1,1,1,1), background_normal = self.images + "blanco.png",size_hint_y = None, height = 50)
        self.Items_No_Txt= Button(background_down = self.images + "blanco.png" ,text = "[color=#404040][b]Vacio",markup = True, background_color = (1,1,1,1), background_normal = self.images + "blanco.png",size_hint_y = None, height = 50)
        self.Total_Txt2 = Button(background_down = self.images + "blanco.png" ,text = "[color=#404040][b]Sin Seleccionar",markup = True, background_color = (1,1,1,1), background_normal = self.images + "blanco.png",size_hint_y = None, height = 50)
        self.PedidoRealizados = []
        self.ASD = self.Total_Txt
        self.ASD2 = self.Subtotal_Txt
        self.ASD3 = self.Items_No_Txt
        self.UsuariostableID = []
        self.UsuariostableU = []
        self.UsuariostableLastID = 0
        self.IDDisponibles = []
        self.UsuariostableID2 = []
        self.PedidoID = []
        self.Lista_Contactos_Categorias = []
        self.Filtro = "contacto"
        self.Filtro2 = "nombre"
        self.Activos = []
        for i in Tablas:
            url = self.Dominio2 + i + "/"
            json_obj = urllib2.urlopen(url)
            Datos_Tabla = json.load(json_obj)
            print str(i) + " " + str(len(Datos_Tabla))+ " Registros"
            
            if i == "Usuario":
                self.Usuariostable = Datos_Tabla
                self.UsuarioNO = len(Datos_Tabla)
                for i in self.Usuariostable:
                    #if i["estado"] == ""
                    if self.UsuariostableLastID < i["id"]:
                        self.UsuariostableLastID = i["id"]
                    self.UsuariostableID.append(i["id"])
                    self.UsuariostableU.append(i["usuario"])
                for i in range(self.UsuariostableLastID):
                    self.UsuariostableID2.append(i)
                    for g in  self.UsuariostableID:
                        if g == i:
                            self.UsuariostableID2.remove(g)
                   
                    
                self.UsuariostableID2.remove(0)  
                print self.UsuariostableID2
                            
                            
                    
            elif i == "Categoria":
                self.categorias = []
                for i in Datos_Tabla:
                    self.categorias.append(i["categoria"])
                    
                self.Categoriatable = Datos_Tabla
                self.CategoriaNO = len(Datos_Tabla)
            elif i == "Contacto":
                self.Lista_Contactos_IDs = []
                self.Lista_Contactos_Nombres = []
                for i in Datos_Tabla:
                    if i["estado"] == "Activo":
                        self.Activos.append(i["id"])
                        
                    self.Lista_Contactos_Nombres.append(str(i["nombre"]))
                    self.Lista_Contactos_IDs.append(str(i["id"]))
                    self.Lista_Contactos_Categorias.append(str(i["categoria"]))
                print self.Activos
                print str(int(len(self.Activos)-4))
                guardado05 = str(int(len(self.Activos)-4))
                for i in range(int(guardado05)):
                    print i
                    #print self.Activos[i]
                    del self.Activos[0]
                    
                print self.Activos
                print self.Lista_Contactos_Nombres
                self.Contactotable = Datos_Tabla
                self.ContactoNO = len(Datos_Tabla)
            elif i == "Rating":
                self.Ratingtable = Datos_Tabla
                self.RatingNO = len(Datos_Tabla)
            elif i == "Menu":
                self.Menutable = Datos_Tabla
                self.MenuNO = len(Datos_Tabla)
            elif i == "Menu_Sub_Categorias":
                self.MenuSCtable = Datos_Tabla
                self.Menu_Sub_CategoriasNO = len(Datos_Tabla)
            elif i == "Plato":
                self.PlatoTable = Datos_Tabla
                self.PlatoNO = len(Datos_Tabla)
                for i in self.PlatoTable:
                    self.inventario_objetos.append(i['plato'])
                    self.inventario_precio.append(i['precio'])
                    self.inventario_id.append(i['plato_id'])
            elif i == "Pedido":
                self.Pedidotable = Datos_Tabla
                self.PedidoNO = len(Datos_Tabla)
            elif i == "Pedidos_Detalles":
                self.Pedidos_Detallestable = Datos_Tabla
                self.Pedidos_DetallesNO = len(Datos_Tabla)
            elif i == "Sugerencia":
                self.Sugerenciastable = Datos_Tabla
                self.Pedidos_DetallesNO = len(Datos_Tabla)
            elif i == "Profile":
                self.Profiletable = Datos_Tabla
                self.ProfileNO = len(Datos_Tabla)


        self.pedido_objetos = []
        self.pedido_precios = []
        self.pedido_establecimiento = []
        self.pedido_divisa = "DOP"
        self.usuario_pedido = {}





        textASAD = "[color=#ff3399]_________________________________________________________________[/color]"


        self.Window = Window

        self.Window.clearcolor = (1, 1, 1, 1)

        self.Label_4 = Button(background_down = self.images + "blanco.png" ,text="[b][color=#262626]", markup=True,
                             font_size=24, background_normal = self.images + "blanco.png" )

        self.Label_4B = CheckBox(text="[color=#404040]", markup=True,font_size=16,
        background_normal = self.images + "blanco.png" , background_color = (1,1,1,1) , size_hint_x = None , width = 25 )
        self.Label_4B1 = Label(text="[color=#404040]Recordar Contraseña?", markup=True,background_color=[1, 1, 1, 1],
                            font_size=16,size_hint_x = .3 , halign="left")
        self.Label_4B2 = CheckBox(text="[color=#404040]", markup=True,font_size=16,
        background_normal = self.images + "blanco.png" , background_color = (1,1,1,1) , size_hint_x = None , width = 25)
        self.Label_4B3 = Label(text="[color=#404040]Mantener Sesión", markup=True,background_color=[1, 1, 1, 1],
                            font_size=16,size_hint_x = .3 ,  halign="left")
            
        self.Label_4Grid = GridLayout(cols = 4 )
        self.Label_4Grid.add_widget(self.Label_4B)
        self.Label_4Grid.add_widget(self.Label_4B1) 
        self.Label_4Grid.add_widget(self.Label_4B2)
        self.Label_4Grid.add_widget(self.Label_4B3)

        self.Label_4C = Image(source = self.images + "principal.png" )

        self.Label_4D = Button(background_down = self.images + "blanco.png" ,text="[color=#ff3333]", markup=True,
                             font_size=20, background_normal = self.images + "blanco.png" )

        self.Label1 = Label(text="[color=#404040]Usuario*[/color]", markup=True,background_color=[1, 1, 1, 1], font_size=16)


        self.Label2 = Label(text="[color=#404040]Contraseña*[/color]", markup=True,
                            background_color=[1, 1, 1, 1],
                            font_size=16)
        label_head2 = (
            '[color=ff0000][b]- Olvidaste tu Contraseña?'
            '\n[color=#404040]- Haznos un Mensage. :)')
        self.Label_3 = Label(text=label_head2, markup=True,font_size=16, background_color = (1,1,1,1), valign = 'top' )

        self.Button1 = Button(background_down = self.images + "blanco4B.png" ,text="Ingresar", font_size=18 , background_normal = self.images + 'blanco4.png', background_color = (1,1,1,1), markup = True)

        self.GL1Button2 = Button(background_down = self.images + "blanco4B.png" ,text="Registrar", markup = True ,
                                 font_size=18 , background_normal = self.images + 'blanco4.png', background_color = (1,1,1,1))

        self.Usuario_Textbox = TextInput(font_size=16, height=35, size_hint_y=None,
                                         multiline=False, text = "Invitado1",
                                         background_color=(1,1,1,1),
                                         background_normal = self.images + 'textbox.png',
                                         background_active = self.images + 'textbox2.png', foreground_color = (0,0,0,.7),
                                         )

        self.Constrasena_Textbox = TextInput(font_size=16, height=35, size_hint_y=None,
                                             multiline=False,text = "1234567890",
                                             password=True,
                                             background_color = (1,1,1,1),
                                             background_normal = self.images + 'textbox.png',
                                             background_active = self.images + 'textbox2.png',foreground_color = (0,0,0,.7),
                                             )

        self.GL1 = GridLayout(x=0,
                              y=0,
                              cols=3,
                              anchor_x='center',
                              anchor_y='center',
                              size_hint_y=1.01,
                              size_hint_x=1)

        self.GL1_Vertical = GridLayout(x=0,
                                       y=0,
                                       cols=3,
                                       anchor_x='center',
                                       anchor_y='center',
                                       size_hint_y=1,
                                       size_hint_x=1)

        self.GL1_fondo1 = Button(background_down = self.images + "fondo_inicio2.png" ,size_hint_x = .250, background_normal = self.images + "fondo_inicio2.png" , background_color = (1,1,1,1))
        self.GL1_fondo2 = Button(background_down = self.images + "fondo_inicio.png" ,size_hint_x = .250, background_normal = self.images + "fondo_inicio.png" , background_color = (1,1,1,1))

        self.GL1_fondo3 = Button(background_down = self.images + "fondo_inicio2.png" ,size_hint_x = .250, background_normal = self.images + "fondo_inicio2.png" , background_color = (1,1,1,1))
        self.GL1_fondo4 = Button(background_down = self.images + "fondo_inicio.png" ,size_hint_x = .250, background_normal = self.images + "fondo_inicio.png" , background_color = (1,1,1,1))

        self.GL1_fondo5 = Button(background_down = self.images + "fondo_inicio2.png" ,height=35, size_hint_y=None,size_hint_x = .250, background_normal = self.images + "fondo_inicio2.png" , background_color = (1,1,1,1))
        self.GL1_fondo6 = Button(background_down = self.images + "fondo_inicio.png" ,height=35, size_hint_y=None,size_hint_x = .250, background_normal = self.images + "fondo_inicio.png" , background_color = (1,1,1,1))

        self.GL1_fondo7 = Button(background_down = self.images + "fondo_inicio2.png" ,size_hint_x = .250, background_normal = self.images + "fondo_inicio2.png" , background_color = (1,1,1,1))
        self.GL1_fondo8 = Button(background_down = self.images + "fondo_inicio.png" ,size_hint_x = .250, background_normal = self.images + "fondo_inicio.png" , background_color = (1,1,1,1))

        self.GL1_fondo9 = Button(background_down = self.images + "fondo_inicio2.png" ,height=35, size_hint_y=None,size_hint_x = .250, background_normal = self.images + "fondo_inicio2.png" , background_color = (1,1,1,1))
        self.GL1_fondo10 = Button(background_down = self.images + "fondo_inicio" ,height=35, size_hint_y=None,size_hint_x = .250, background_normal = self.images + "fondo_inicio.png" , background_color = (1,1,1,1))

        self.GL1_fondo11 = Button(background_down = self.images + "fondo_inicio2.png" ,size_hint_x = .250, background_normal = self.images + "fondo_inicio2.png" , background_color = (1,1,1,1))
        self.GL1_fondo12 = Button(background_down = self.images + "fondo_inicio.png" ,size_hint_x = .250, background_normal = self.images + "fondo_inicio.png" , background_color = (1,1,1,1))

        self.GL1_fondo13 = Button(background_down = self.images + "fondo_inicio2.png" ,size_hint_x = .250, background_normal = self.images + "fondo_inicio2B.png" , background_color = (1,1,1,1))
        self.GL1_fondo14 = Button(background_down = self.images + "fondo_inicio.png" ,size_hint_x = .250, background_normal = self.images + "fondo_inicioB.png" , background_color = (1,1,1,1))
        self.GL1_fondo15 = Button(background_down = self.images + "fondo_inicio2.png" ,size_hint_x = .250, background_normal = self.images + "fondo_inicio2.png" , background_color = (1,1,1,1))
        self.GL1_fondo16 = Button(background_down = self.images + "fondo_inicio.png" ,size_hint_x = .250, background_normal = self.images + "fondo_inicio.png" , background_color = (1,1,1,1))

        self.GL1_fondo15B = Button(background_down = self.images + "fondo_inicio2.png" ,size_hint_x = .250, background_normal = self.images + "fondo_inicio2.png" , background_color = (1,1,1,1))
        self.GL1_fondo16B = Button(background_down = self.images + "fondo_inicio.png" ,size_hint_x = .250, background_normal = self.images + "fondo_inicio.png" , background_color = (1,1,1,1))
        self.GL1_fondo15C = Button(background_down = self.images + "fondo_inicio2.png" ,size_hint_x = .250, background_normal = self.images + "fondo_inicio2.png" , background_color = (1,1,1,1))
        self.GL1_fondo16C = Button(background_down = self.images + "fondo_inicio.png" ,size_hint_x = .250, background_normal = self.images + "fondo_inicio.png" , background_color = (1,1,1,1))




        
        self.GL1.add_widget(self.GL1_fondo1)
        self.GL1.add_widget(self.Label_4)
        self.GL1.add_widget(self.GL1_fondo2)

        self.GL1.add_widget(self.GL1_fondo15B)
        self.GL1.add_widget(self.Label_4C)
        self.GL1.add_widget(self.GL1_fondo16B)
        
        self.GL1.add_widget(self.GL1_fondo3)
        self.GL1.add_widget(self.Label1)
        self.GL1.add_widget(self.GL1_fondo4)

        self.GL1.add_widget(self.GL1_fondo5)
        self.GL1.add_widget(self.Usuario_Textbox)
        self.GL1.add_widget(self.GL1_fondo6)

        self.GL1.add_widget(self.GL1_fondo7)
        self.GL1.add_widget(self.Label2)
        self.GL1.add_widget(self.GL1_fondo8)

        self.GL1.add_widget(self.GL1_fondo9)
        self.GL1.add_widget(self.Constrasena_Textbox)
        self.GL1.add_widget(self.GL1_fondo10)

        self.GL1.add_widget(self.GL1_fondo15)
        self.GL1.add_widget(self.Label_4Grid)
        self.GL1.add_widget(self.GL1_fondo16)

        self.GL1.add_widget(self.GL1_fondo11)
        self.GL1.add_widget(self.Label_3)
        self.GL1.add_widget(self.GL1_fondo12)

        #self.GL1.add_widget(self.GL1_fondo15C)
        #self.GL1.add_widget(self.Label_4D)
        #self.GL1.add_widget(self.GL1_fondo16C)

        self.GL1.add_widget(self.GL1_fondo13)
        self.GL1.add_widget(self.GL1_Vertical)
        self.GL1.add_widget(self.GL1_fondo14)



        self.GL1_Vertical.add_widget(self.Button1)
        self.GL1_Vertical.add_widget(self.GL1Button2)

        # GL1 <----------- formulario completo
        self.Button1.bind(on_press=self.LOG_IN)  # <----------- Camino al Menu

        self.GL1Button2.bind(on_press=self.REGISTRAR_USUARIO)  # <----------- Camino a la Salida
        #self.add_widget(self.GL1)  # <----------- primer formulario mostrado.

        # ___________________________________________________________________________________________________________________













        navigationdrawer = NavigationDrawer()

        self.side_panel = BoxLayout(orientation='vertical')
        #self.side_panel.add_widget(Button(background_down = self.images + "" ,text='MENU', height=70, background_normal = self.images + 'color_rojo.png', font_size = 24, size_hint_y = None))
        popup = Popup(title='Sidebar popup',
                      content=Label(
                          text='You clicked the sidebar\npopup button'),
                      size_hint=(0.7, 0.7))
        self.EmailIncorrecto = Popup(title='',
                      content=Label(
                          text='Email no permitido.'),
                      size_hint=(None, None), width = 200)
        first_button = Button(background_down = self.images + "" ,text='Popup\nbutton')
        first_button.bind(on_release=popup.open)
        #side_panel.add_widget(first_button)
        #side_panel.add_widget(Button(background_down = self.images + "" ,text='Another\nbutton'))
        navigationdrawer.add_widget(self.side_panel)

        label_head = (
            '[color=ff0000][b]No encuentras \n tu Tienda Favorita?'
            '\n\n[color=#404040] Haznos una Sugerencia :)')
        self.GL2_root = GridLayout(cols=1,
                              size_hint_y=1,
                              size_hint_x=1)
        main_panel = ScrollView(size_hint=(1, 1), size=(Window.width, Window.height - self.GL2_root.height  +25))
        self.main_panel = main_panel
        self.layout = GridLayout(cols=2, spacing=1, size_hint_y=None)
        self.layout.bind(minimum_height=self.layout.setter('height'))

        label_bl = BoxLayout(orientation='horizontal')
        label = Label(text=label_head, font_size='15sp',
                      markup=True, valign='top')
        label_bl.add_widget(Widget(size_hint_x=None, width=dp(10)))
        label_bl.add_widget(label)
        label_bl.add_widget(Widget(size_hint_x=None, width=dp(10)))

        #navigationdrawer.add_widget(Widget(size_hint_y=None, height=dp(10)))
        #navigationdrawer.add_widget(label_bl)
        #navigationdrawer.add_widget(Widget(size_hint_y=None, height=dp(10)))
        main_panel.add_widget(self.layout)

        self.sugerencia_Layout = GridLayout(cols = 1 , size_hint = (1,1))
        self.sugerenciapopup = Popup(
        title='',
        markup = True, title_size = 14,
        title_align = 'center',
        content = self.sugerencia_Layout ,
        background = "blanco3.png",
        separator_color = (0,0,0,0),
        title_color = (0,0,0,.5),
        size_hint = (.5, .8)
        )

        def printR(a):
            print a

        abcd = 0
        for i in self.Contactotable:
            for x in self.Activos:
                abcd += 1
                f = GridLayout(cols=1, spacing=0, size_hint_y=None, height = 410 , size_hint_x = 1)
                if abcd == 1:
                    self.tiendas2 = Button(background_down = self.images + "blanco.png" ,text="[color=#404040]Nuevos Contactos", halign = 'center', height = 70 ,size_hint_y=None,markup=True, font_size = 24, background_normal = self.images + 'blanco.png', background_color = (1,1,1,1))
                    self.tiendas2_txt = Button(background_down = self.images + "blanco.png" ,text = "",size_hint_y=None, height = 70 , background_normal = self.images + 'blanco.png', background_color = (1,1,1,1), markup = True)

                    self.layout.add_widget(self.tiendas2)
                    self.layout.add_widget(self.tiendas2_txt)
                   
                if i["id"] == x:
                    
                    btnC3 = Button(background_down = self.images + "roro.png" ,size_hint_y=0.025 , background_normal = self.images + 'roro.png', background_color = (1,1,1,1))
                    btnC4 = Button(background_down = self.images + "roro2.png" ,size_hint_y=0.025 , background_normal = self.images + 'roro2.png', background_color = (1,1,1,1))
                    btnC6 = Button(background_down = self.images + "asd.png" ,size_hint_y= None ,height=25, background_normal = self.images + 'asd.png', background_color = (1,1,1,1))
                    btnC0 = Image(size_hint_y=0.4, height=300, source = self.images + '404.png')
                    btnC1 = Button(background_down = self.images + "blanco.png" ,text='[b][color=#404040] ' + i["nombre"], size_hint_y=0.1, height=30, background_normal = self.images + 'blanco.png', background_color = (1,1,1,1), markup = True , font_size = 18,valign = 'top')
                    btnC5 = Button(background_down = self.images + "blanco.png" ,text='', size_hint_y=0.050, height=30, background_normal = self.images + 'blanco.png', background_color = (1,1,1,1), markup = True , font_size = '15sp')
                    btnC = Button(background_down = self.images + "color_rojoB.png" ,text="[color=#ed1d27]"+str(i['id'])+"[/color]"+'>' , size_hint_y=0.2, size_hint_x = 0.2, height=70, background_normal = self.images + 'color_rojo.png', markup = True, font_size = 23)
                    categoria_save = self.categorias[(i["categoria"])-1]
                    btnC2 = Button(background_down = self.images + "blanco.png" ,text='[color=#404040][b] ' + categoria_save , size_hint_y=0.1, height=30, background_normal = self.images + 'blanco.png',background_color = (1,1,1,1), markup   = True, font_size = 18)
                    name = btnC.text

                    #btnC.bind(on_press= lambda name=name: printR(name.text))
                    integer =i["id"]
                    seleccionado = self.Lista_Contactos_IDs[int(integer)-1]
                    print btnC.text[15:-9]
                    btnC.bind(on_press=lambda seleccionado=seleccionado: self.TIENDA(seleccionado.text[15:-9]))

                    f.add_widget(btnC6)
                    f.add_widget(btnC0)
                    f.add_widget(btnC1)
                    f.add_widget(btnC3)
                    f.add_widget(btnC2)
                    f.add_widget(btnC4)
                    f.add_widget(btnC5)
                    f.add_widget(btnC)
                    self.layout.add_widget(f)
        abcd = 0
        for i in self.Contactotable:
            abcd += 1
            a = GridLayout(cols=1, spacing=0, size_hint_y=None, height = 410 , size_hint_x = 1)
            if abcd == 1 :
                self.btnK = Button(background_down = self.images + "K.png" ,size_hint_y=None,height = 250  , background_normal = self.images + 'K.png', background_color = (1,1,1,1))
                self.btnO = Button(background_down = self.images + "O.png" ,size_hint_y=None, height = 250 , background_normal = self.images + 'O.png', background_color = (1,1,1,1))
                self.layout.add_widget(self.btnK)
                self.layout.add_widget(self.btnO)
                self.label_12 = Label(text=label_head, font_size='15sp', halign = 'center', height = 100 ,size_hint_y=None,
                              markup=True)
                self.btnO_B = Button(background_down = self.images + "color_rojo.png" ,text = "[b]Hacer Sugerencia.",size_hint_y=None, height = 100 , background_normal = self.images + 'color_rojo.png', background_color = (1,1,1,1), markup = True)
                self.layout.add_widget(self.label_12)
                self.layout.add_widget(self.btnO_B)

                self.btnO_B.bind(on_press=self.sugerenciapopup.open)
                self.tiendas = Button(background_down = self.images + "blanco.png" ,text="[color=#404040]Directorio", halign = 'center', height = 70 ,size_hint_y=None,markup=True, font_size = 24, background_normal = self.images + 'blanco.png', background_color = (1,1,1,1))

                self.tiendas_txt = Button(background_down = self.images + "blanco.png" ,text = "",size_hint_y=None, height = 70 , background_normal = self.images + 'blanco.png', background_color = (1,1,1,1), markup = True)

                self.layout.add_widget(self.tiendas)
                self.layout.add_widget(self.tiendas_txt)


            if i["estado"] == "Activo":
                btn3 = Button(background_down = self.images + "roro.png" ,size_hint_y=0.025 , background_normal = self.images + 'roro.png', background_color = (1,1,1,1))
                btn4 = Button(background_down = self.images + "roro2.png" ,size_hint_y=0.025 , background_normal = self.images + 'roro2.png', background_color = (1,1,1,1))
                btn6 = Button(background_down = self.images + "asd.png" ,size_hint_y= None ,height=25, background_normal = self.images + 'asd.png', background_color = (1,1,1,1))
                btn0 = Image(size_hint_y=0.4, height=300, source = self.images + '404.png')
                btn1 = Button(background_down = self.images + "blanco.png" ,text='[b][color=#404040] ' + i["nombre"], size_hint_y=0.1, height=30, background_normal = self.images + 'blanco.png', background_color = (1,1,1,1), markup = True , font_size = 18,valign = 'top')
                btn5 = Button(background_down = self.images + "blanco.png" ,text='', size_hint_y=0.050, height=30, background_normal = self.images + 'blanco.png', background_color = (1,1,1,1), markup = True , font_size = '15sp')
                btn = Button(background_down = self.images + "color_rojoB.png" ,text="[color=#ed1d27]"+str(i['id'])+"[/color]"+'>' , size_hint_y=0.2, size_hint_x = 0.2, height=70, background_normal = self.images + 'color_rojo.png', markup = True, font_size = 23)
                categoria_save = self.categorias[(i["categoria"])-1]
                btn2 = Button(background_down = self.images + "blanco.png" ,text='[color=#404040][b] ' + categoria_save , size_hint_y=0.1, height=30, background_normal = self.images + 'blanco.png',background_color = (1,1,1,1), markup   = True, font_size = 18)
                name = btn.text

                #btn.bind(on_press= lambda name=name: printR(name.text))
                integer =i["id"]
                seleccionado = self.Lista_Contactos_IDs[int(integer)-1]
                print btn.text[15:-9]
                btn.bind(on_press=lambda seleccionado=seleccionado: self.TIENDA(seleccionado.text[15:-9]))

                a.add_widget(btn6)
                a.add_widget(btn0)
                a.add_widget(btn1)
                a.add_widget(btn3)
                a.add_widget(btn2)
                a.add_widget(btn4)
                a.add_widget(btn5)
                a.add_widget(btn)
                self.layout.add_widget(a)
            else:
                pass




        navigationdrawer.add_widget(main_panel)
        label.bind(size=label.setter('text_size'))

        def set_anim_type(name):
            navigationdrawer.anim_type = name

        def set_transition(name):
            navigationdrawer.opening_transition = name
            navigationdrawer.closing_transition = name

        modes_layout = BoxLayout(orientation='horizontal')
        modes_layout.add_widget(Label(text='preset\nanims:'))
        slide_an = Button(text='slide_\nabove_\nanim')
        slide_an.bind(on_press=lambda j: set_anim_type('slide_above_anim'))
        slide_sim = Button(text='slide_\nabove_\nsimple')
        slide_sim.bind(on_press=lambda j: set_anim_type('slide_above_simple'))
        fade_in_button = Button(text='fade_in')
        fade_in_button.bind(on_press=lambda j: set_anim_type('fade_in'))
        reveal_button = Button(text='reveal_\nbelow_\nanim')
        reveal_button.bind(on_press=
                           lambda j: set_anim_type('reveal_below_anim'))
        slide_button = Button( text='reveal_\nbelow_\nsimple')
        slide_button.bind(on_press=
                          lambda j: set_anim_type('reveal_below_simple'))
        modes_layout.add_widget(slide_an)
        modes_layout.add_widget(slide_sim)
        modes_layout.add_widget(fade_in_button)
        modes_layout.add_widget(reveal_button)
        modes_layout.add_widget(slide_button)
        #main_panel.add_widget(modes_layout)

        transitions_layout = BoxLayout(orientation='horizontal')
        transitions_layout.add_widget(Label(text='anim\ntransitions'))
        out_cubic = Button(text='out_cubic')
        out_cubic.bind(on_press=
                       lambda j: set_transition('out_cubic'))
        in_quint = Button(text='in_quint')
        in_quint.bind(on_press=
                      lambda j: set_transition('in_quint'))
        linear = Button(text='linear')
        linear.bind(on_press=
                    lambda j: set_transition('linear'))
        out_sine = Button(text='out_sine')
        out_sine.bind(on_press=
                      lambda j: set_transition('out_sine'))
        transitions_layout.add_widget(out_cubic)
        transitions_layout.add_widget(in_quint)
        transitions_layout.add_widget(linear)
        transitions_layout.add_widget(out_sine)
        #main_panel.add_widget(transitions_layout)

        button = Button(text='toggle NavigationDrawer state (animate)',
                        size_hint_y=0.2)
        button.bind(on_press=lambda j: navigationdrawer.toggle_state())
        button2 = Button(text='toggle NavigationDrawer state (jump)',
                         size_hint_y=0.2)
        button2.bind(on_press=lambda j: navigationdrawer.toggle_state(False))
        button3 = Button(text='toggle _main_above', size_hint_y=0.2)
        button3.bind(on_press=navigationdrawer.toggle_main_above)
        #main_panel.add_widget(button)
        #main_panel.add_widget(button2)
        #main_panel.add_widget(button3)




        self.Button3 = Button(border = (1,1,1,1),background_down = self.images + "blanco6B.png" ,text="[color=#404040]Carrito",
                              font_size='13sp', background_normal = self.images + 'blanco6C.png' , background_color = (1,1,1,1,), markup = True)

        self.Button5 = Button(border = (1,1,1,1),background_down = self.images + "blanco6B.png" ,text="[color=#404040]Pedidos",
                              font_size='13sp' , background_normal = self.images + 'blanco6C.png' , background_color = (1,1,1,1,), markup = True)

        self.GL2Label_1 = Button(border = (1,1,1,1),background_down = self.images + "blanco6B.png" ,text="[color=#404040][b]Home",
                              font_size='13sp', background_normal = self.images + 'blanco6C.png' , background_color = (1,1,1,1,), markup = True)
        self.GL2Label_2 = Label(text="[color=#404040]PANEL ADMINISTRADOR", size_hint_y=1, markup=True)
        self.GL1Button1 = Button(background_down = self.images + "blanco6C.png" ,text="[color=#404040]",
                                 font_size='13sp', background_normal = self.images + 'blanco6C.png' , background_color = (1,1,1,1,), markup = True)

        self.Button7 = Button(border = (1,1,1,1),background_down = self.images + "blanco6B.png" ,text="[color=#ff0000]Salir",
                              font_size='13sp', background_normal = self.images + 'blanco6C.png' , background_color = (1,1,1,1,), markup = True)
        self.GL2Button2 = Button(border = (1,1,1,1),background_down = self.images + "blanco6B.png" ,text="[color=#404040]Perfil", font_size='13sp', background_normal = self.images + 'blanco6C.png' , background_color = (1,1,1,1,), markup = True)
        self.GL2Button3 = Button(border = (1,1,1,1),background_down = self.images + "blanco6B.png" ,text="[color=#404040]Administrador", font_size='13sp', background_normal = self.images + 'blanco6C.png' , background_color = (1,1,1,1,), markup = True)
        self.GL2Button4 = Button(border = (1,1,1,1),background_down = self.images + "blanco6B.png" ,text="[color=#404040]Departamentos", font_size='13sp', background_normal = self.images + 'blanco6C.png' , background_color = (1,1,1,1,), markup = True)

        self.GL2Button4B = Button(border = (1,1,1,1),background_down = self.images + "blanco6B.png" ,text="[color=#404040][b]Tu[/b] Tienda", font_size='13sp', background_normal = self.images + 'blanco6C.png' , background_color = (1,1,1,1,), markup = True)

        self.GL2root_Textbox = Button(text= "[color=#1a1a1a][b]",font_size=18, height = 50, background_normal = self.images + 'panel_button.png' , background_color = (1,1,1,1,), background_down = self.images + 'panel_button_2.png', markup = True ,
                                             size_hint_y= None,
                                             size_hint_x=1)

        self.GL2root_Label = Button(text= "[color=#404040]Carrito:  [b]0",font_size=14, height = 25, background_normal = self.images + 'panal.png' , background_color = (1,1,1,1,), background_down = self.images + 'panel_button_2.png', markup = True, halign = 'left' ,
                                             size_hint_y= None,
                                             size_hint_x=1)

        self.GL2root_Label_1 = Button(text= "[color=#404040]Hi, Armando",font_size=14, height = 25, background_normal = self.images + 'panal.png' , background_color = (1,1,1,1,), background_down = self.images + 'panel_button_2.png', markup = True, halign = 'left' ,
                                             size_hint_y= None,
                                             size_hint_x=1)

        self.GL2root_Label_2 = Button(text= "[color=#404040]Pedidos:  [b]0",font_size=14, height = 25, background_normal = self.images + 'panal.png' , background_color = (1,1,1,1,), background_down = self.images + 'panel_button_2.png', markup = True, halign = 'left' ,
                                             size_hint_y= None,
                                             size_hint_x= 1)

        self.vacio_1 = Button(text= "",font_size=18, height = 25, background_normal = self.images + 'menudots.png' , background_color = (1,1,1,1,), background_down = self.images + 'panel_button_2.png', markup = True ,   size_hint_y= 1, size_hint_x= 1)


        self.vacio_2 = Button(text= "",font_size=18, height = 25, background_normal = self.images + 'menudots.png' , background_color = (1,1,1,1,), background_down = self.images + 'panel_button_2.png', markup = True,
                                             size_hint_y= 1,
                                             size_hint_x= 1)

        self.vacio_3 = Button(text= "",font_size=18, height = 25, background_normal = self.images + 'menudots.png' , background_color = (1,1,1,1,), background_down = self.images + 'panel_button_2.png', markup = True,
                                             size_hint_y= 1,
                                             size_hint_x= 1)


        self.vacio_1B = Button(text= "<",font_size=24, height = 25, background_normal = self.images + 'panel_button.png' , background_color = (1,1,1,1,), background_down = self.images + 'panel_button_2.png', markup = True ,   size_hint_y= 0.25, size_hint_x= 1)


        self.vacio_2B = Button(text= "Busqueda",font_size=18, height = 25, background_normal = self.images + 'panel_button.png' , background_color = (1,1,1,1,), background_down = self.images + 'panel_button_2.png', markup = True,
                                             size_hint_y= 0.50,
                                             size_hint_x= 1)



        self.vacio_3B = Button(text= ">",font_size=24, height = 25, background_normal = self.images + 'panel_button.png' , background_color = (1,1,1,1,), background_down = self.images + 'panel_button_2.png', markup = True,
                                             size_hint_y= 0.25,
                                             size_hint_x= 1)

        self.anidadodebotones = GridLayout(cols=3,height = 25,
                              anchor_x='center',
                              anchor_y='center',
                              size_hint_y= None,
                              size_hint_x=1)

        self.anidadodebotones_2 = GridLayout(cols=3,height = 50,
                              anchor_x='center',
                              anchor_y='center',
                              size_hint_y= None,
                              size_hint_x=1)


        self.GL2 = GridLayout(cols=1,
                              anchor_x='center',
                              anchor_y='center',
                              size_hint_y=1,
                              size_hint_x=0.7)





        self.navigationdrawer = navigationdrawer

        self.anidadodebotones.add_widget(self.GL2root_Label_1)
        self.anidadodebotones.add_widget(self.GL2root_Label)
        self.anidadodebotones.add_widget(self.GL2root_Label_2)
        #self.anidadodebotones.add_widget(self.vacio_1)
        #self.anidadodebotones.add_widget(self.vacio_2)
        #self.anidadodebotones.add_widget(self.vacio_3)
        self.anidadodebotones_2.add_widget(self.vacio_1B)
        self.anidadodebotones_2.add_widget(self.vacio_2B)
        self.anidadodebotones_2.add_widget(self.vacio_3B)




        self.GL2_root.add_widget(self.anidadodebotones_2)
        self.GL2_root.add_widget(self.anidadodebotones)


        self.GL2_root.add_widget(self.navigationdrawer)


        #self.layout.add_widget(self.GL2_list_view)




        self.side_panel.add_widget(self.GL2Label_1)

        self.side_panel.add_widget(self.Button3)
        self.side_panel.add_widget(self.Button5)
        #self.side_panel.add_widget(self.GL1Button1)


        #self.side_panel.add_widget(self.GL2Label_2)

        self.side_panel.add_widget(self.GL2Button2)
        #self.side_panel.add_widget(self.GL2Button3)
        #self.side_panel.add_widget(self.GL2Button4)
        self.side_panel.add_widget(self.GL2Button4B)
        self.side_panel.add_widget(self.Button7)
        # GL2 <----------- formulario completo
        self.Button3.bind(on_press=self.INVENTARIO)  

        self.Button5.bind(on_press=self.PEDIDOS)  

        self.Button7.bind(on_press=self.INICIO)  
        #self.GL1Button1.bind(on_press=self.ADMINISTRAR_USUARIOS)  
        self.GL2Button3.bind(on_press=self.MENU_ADMINISTRADOR)  
        self.GL2Button2.bind(on_press=self.PERFIL)
        self.GL2Button4.bind(on_press=self.DEPARTAMENTOS)
        self.GL2Label_1.bind(on_press=self.HOME)
        self.GL2Button4B.bind(on_press=self.PERFIL_TIENDA)
        self.vacio_2B.bind(on_press = self.PANELDEBUSQUEDA)
        
        
        
        # ________________________________________________________________________________________________





        #self.data = [{'text': str(row['Producto']), 'is_selected': False,'precio': row['Precio'], 'medio': "50 RD$"} for row in self.MenuSCtable]

        ratas = [str("adasd") for row in self.MenuSCtable]
        print ratas

        self.PRECIOS = [str("adasd") for row in self.MenuSCtable]
        print self.PRECIOS

        self.args_converter = lambda row_index, rec: \
        {'text': rec['text'],
        'size_hint_y': None,
        'size_hint_': None,
        'height': 300,
        'padding_bottom': 20,
        'orientation': 'vertical',
        'cls_dicts': [
                    {'cls': ListItemButton,
                        'kwargs': {'text': rec['text'] ,'background_normal':'color_gris_oscuro.png','deselected_color': [1, 1, 1, 1]
                        }},
                    {'cls': ListItemButton,
                        'kwargs': {'text': rec['text'] ,
                        'background_normal': '404-not-found-error-page-examples.png',
                        'height': 200, 'size_hint_y': None,
                        'size_hint_x': None, 'width' : 200,'deselected_color': [1, 1, 1, 1],'selected_color': [1,1,1,1], 'anchor_x': 'center'
                        }},
                    {'cls': ListItemButton,
                        'kwargs': {'text': "[color=#404040]{0}".format(rec['medio']),'markup': True,
                                'background_normal':'color_gris.png','deselected_color': [1, 1, 1, 1],'selected_color': [1,1,1,1]
                                }},
                    {'cls': ListItemButton,
                        'kwargs': {'text': '+','background_normal':'color_verde.png','deselected_color': [1, 1, 1, 1],
                        }}
                        ]}




        self.Button9 = Button(text="Salir",
                              font_size=18)

        self.Input1 = Label(text="[color=#f2f2f2]MI CARRITO[/color]", markup=True,
                            size_hint_y=None,
                            size_hint_x=0.2,
                            height=70,
                            font_size=24
                            )
        self.Input1_B = Label(text="[color=#f2f2f2][/color]", markup=True,
                            size_hint_y=None,
                            size_hint_x=0.2,
                            height=40,
                            font_size=24
                            )



        self.Label7 = Label(text="[color=#404040]SIN SELECCIONAR", markup=True,
                            size_hint_y=None,
                            size_hint_x=0.2,
                            height=40,
                            font_size=24,
                            bcolor=Color(215, 86, 119, 0.9)
                            )

        self.Button10 = Button(text="CONFIRMAR MONTO",
                               size_hint_y=None,
                               size_hint_x=0.2,
                               height=100,
                               font_size=18, background_normal = self.images + 'color_rojo.png', background_color = (1,1,1,1))

        self.Button10_B = Button(text="LIMPIAR MONTO",
                               size_hint_y=None,
                               size_hint_x=0.2,
                               height=100,
                               font_size=18, background_normal = self.images + 'color_rojo.png', background_color = (1,1,1,1))

        self.Button11 = Button(text="Ver Pedido",
                               size_hint_y=None,
                               size_hint_x=0.2,
                               height=100,
                               font_size=18
                               )

        self.Button12 = Button(text="Volver",
                               size_hint_y=None,
                               size_hint_x=0.2,
                               height=100,
                               font_size=18
                               )

        self.GL3 = GridLayout(x=0,
                              y=0,
                              cols=2,
                              anchor_x='center',
                              anchor_y='center',
                              size_hint_y=None,
                              size_hint_x=1,
                              spacing = 1
                              )

        self.GL3.bind(minimum_height=self.GL3.setter('height'))
        self.GL3_Vertical = GridLayout(x=0,
                                       y=0,
                                       cols=2,
                                       anchor_x='center',
                                       anchor_y='center',
                                       size_hint_y=None,
                                       size_hint_x=1)

        self.GL3root = ScrollView(size_hint=(1, None), size=(Window.width, Window.height))

        #self.GL3root.add_widget(self.GL3)

        #self.GL3.add_widget(self.list_view)








        #self.GL3.add_widget(self.Label7)




        #self.GL3_Vertical.add_widget(self.Button11)
        #self.GL3_Vertical.add_widget(self.Button12)

        self.ID_Objeto_Seleccionado = 0

        #self.GL3.add_widget(self.GL3_Vertical)
        self.Item_Seleccionado = ""

        def on_selected_item(*args):
            try:
                contador = -1
                encontrado = 0
                selected_item = args[0].selection[0].text
                encontrado2 = 0

                for i in ratas:
                    contador = contador + 1
                    if selected_item == i:
                        print str(contador) + " - " + str(selected_item)
                        encontrado = contador
                        self.ID_Objeto_Seleccionado = contador
                        self.Item_Seleccionado = selected_item

                self.Label7.text = "[color=#404040]" + str(selected_item)
                self.Item_Seleccionado = "[color=#404040]" + str(selected_item)
                contador = -1
                encontrado = 0

                for i in ratas_2:
                    contador = contador + 1
                    if selected_item == i:
                        print str(contador) + " - " + str(selected_item)
                        encontrado = contador
                        self.GL7Label1.text = "[color=#404040]SELECCIONADO: " + str(selected_item)
                        self.Label18.text = "[color=#404040]" + str(selected_item)

                contador = -1
                encontrado = 0

                for i in self.ratas_3:
                    contador = contador + 1
                    if selected_item == i:
                        print str(self.ratas_3_id[contador]) + " - " + str(selected_item)
                        self.guardado = self.ratas_3_id[contador]


            except:
                pass

        self.Button11.bind(on_press=self.LISTADEPEDIDOS)  # <----------- Camino al Formulario para Pedidos
        self.Button12.bind(on_press=self.MENU)  # <----------- Camino al Menu de Ayuda
        self.Button10.bind(on_press=self.DIRECCIONES)  # <----------- Crear Pedido
        self.Button10_B.bind(on_press = self.LIMPIARPEDIDO)
        #self.list_adapter.bind(on_selection_change=on_selected_item)

        # ___________________________________________________________________________________________________________________



        self.datos_guardados = []

        list_item_args_converter_temp = lambda row_index, obj: {'text': obj.text,
                                                                'size_hint_y': None,
                                                                'size_hint_y': None,
                                                                'font_size': 18,
                                                                'markup': True,
                                                                'background_color': [1, 1, 1, 1],
                                                                'deselected_color': [0.24, 0.255, 0.173, 0.4],
                                                                'selected_color': [215, 44, 153, 1],
                                                                'color': [0, 0, 0, 0.95]
                                                                }

        self.list_adapter_temp = \
            ListAdapter(data=self.datos_guardados,
                        args_converter=list_item_args_converter_temp,
                        selection_mode='single',
                        propagate_selection_to_data=False,
                        allow_empty_selection=False,
                        cls=ListItemButton)

        self.list_view2 = ListView(adapter=self.list_adapter_temp,
                                   size_hint_x=1,
                                   size_hint_y=None,
                                   height=425
                                   )

        self.Button13 = Button(text="Realizar Compra",
                               font_size=18)

        self.Button14 = Button(text="Volver",
                               font_size=18)

        self.GL4_Button1 = Button(text="Limpiar Pedido",
                                  font_size=18)

        self.GL4 = GridLayout(cols=1,
                              anchor_x='center',
                              anchor_y='center',
                              size_hint_y=1,
                              size_hint_x=1,
                              )
        self.GL4_V = GridLayout(cols=3)

        #self.GL4_Accordion = Accordion(size_hint_y = 1, orientation = 'horizontal')

        #for x in range(5):
        #    GL4item = AccordionItem(title='Title %d' % x)
        #    GL4item.add_widget(Label(text='[color=#404040]Very big content\n' * 10 , markup = True , size_hint = (None,None) ))
        #    self.GL4_Accordion.add_widget(GL4item)


        #self.GL4.add_widget(self.list_view2)

        #self.GL4.add_widget(self.GL4_Accordion)
        self.GL4_V.add_widget(self.Button14)
        self.GL4_V.add_widget(self.Button13)
        self.GL4_V.add_widget(self.GL4_Button1)

        self.GL4.add_widget(self.GL4_V)


        # GL2 <----------- formulario completo
        self.Button13.bind(on_press=self.FACTURA_VISTA)  # <----------- Camino al Formulario para Pedidos
        self.Button14.bind(on_press=self.INVENTARIO)  # <----------- Camino al Menu de Ayuda
        self.GL4_Button1.bind(on_press=self.LIMPIARPEDIDO)

        # ___________________________________________________________________________________________________________________

        # ESPACIO PARA VARIABLES DE USUARIO


        # ___________________________________________________________________________________________________________________


        self.Label17 = Label(text="[color=#404040]INTELLISYS CHALLENGE PROJECT", markup=True,
                             font_size=18)
        self.Label18 = Label(text="[color=#404040]McDonalds", markup=True,
                             font_size=18)
        self.Label19 = Label(text="[color=#404040]FACTURA DEL PEDIDO", markup=True,
                             font_size=20)
        self.Label20 = Label(text="[color=#404040]DIRECCION: ", markup=True,
                             font_size=16)
        self.Label21 = Label(text="[color=#404040]SECTOR: ", markup=True,
                             font_size=16)
        self.Label22 = Label(text="[color=#404040]NOMBRE: ", markup=True,
                             font_size=16)
        self.Label23 = Label(text="[color=#404040]IDENTIFICACION: ", markup=True,
                             font_size=16)

        self.Label24 = Label(text="[color=#404040]PEDIDO", font_size=18)

        self.datos_guardados_2 = []
        self.datos_guardados_2.append(DataItem("Pedido a Realizar"))

        list_item_args_converter_temp_2 = lambda row_index, obj: {'text': obj.text,
                                                                  'height': 20,
                                                                  'font_size': 18,
                                                                  'markup': True,
                                                                  'background_color': [1, 1, 1, 1],
                                                                  'deselected_color': [0.24, 0.255, 0.173, 0.4],
                                                                  'selected_color': [215, 44, 153, 1],
                                                                  'color': [0, 0, 0, 0.95]
                                                                  }

        self.list_adapter_temp_2 = \
            ListAdapter(data=self.datos_guardados_2,
                        args_converter=list_item_args_converter_temp_2,
                        selection_mode='single',
                        propagate_selection_to_data=False,
                        allow_empty_selection=False,
                        cls=ListItemLabel)

        self.list_view_3 = ListView(adapter=self.list_adapter_temp_2)

        self.Label26 = Label(text="[color=#404040]TOTAL: 950.00 RD$", markup=True,
                             font_size=18)
        self.Label27 = Label(text="[color=#404040]SANTO DOMINGO D.N", markup=True,
                             font_size=18)
        self.Label28 = Label(text="[color=#404040]7 DE JULIO DEL 2016", markup=True,
                             font_size=18)

        self.Button98 = Button(text="CONFIRMAR PEDIDO",
                               font_size=18)
        self.Button99 = Button(text="CANCELAR",
                               font_size=18)

        self.GLFACTURA = GridLayout(cols=1, size_hint_y=None)
        self.GL5 = GridLayout(cols=1)
        self.GL5_V = GridLayout(cols=2)

        self.GL5.add_widget(self.Label17)
        self.GL5.add_widget(self.Label18)
        self.GL5.add_widget(self.Label19)

        self.GL5.add_widget(self.Label20)
        self.GL5.add_widget(self.Label21)
        self.GL5.add_widget(self.Label22)
        self.GL5.add_widget(self.Label23)
        self.GL5.add_widget(self.Label24)

        self.GLFACTURA.add_widget(self.list_view_3)
        self.GL5.add_widget(self.GLFACTURA)

        self.GL5.add_widget(self.Label26)
        self.GL5.add_widget(self.Label27)
        self.GL5.add_widget(self.Label28)
        self.GL5_V.add_widget(self.Button98)
        self.GL5_V.add_widget(self.Button99)
        self.GL5.add_widget(self.GL5_V)
        self.Button98.bind(on_press=self.CREAR_PEDIDO)
        self.Button99.bind(on_press=self.MENU)

        # _______________________________________#REGISTRAR CONTACTOS___________________________________________




        self.GL6Label1 = Label(text="[color=#404040]Nombre", markup=True,
                               size_hint_y=0.20,
                               size_hint_x=0.20,
                               font_size=18)
        self.GL6Label2 = Label(text="[color=#404040]Direccion", markup=True,
                               size_hint_y=0.20,
                               size_hint_x=0.20,
                               font_size=18)
        self.GL6Label3 = Label(text="[color=#404040]Numero de Contacto", markup=True,
                               size_hint_y=0.20,
                               size_hint_x=0.20,
                               font_size=18)
        self.GL6Label4 = Label(text="Contacto", markup=True,
                               size_hint_y=0.20,
                               size_hint_x=0.20,
                               font_size=18)

        self.GL6Estableciminento = TextInput(font_size=18,
                                             size_hint_y=0.20,
                                             size_hint_x=0.20)

        self.GL6Direccion = TextInput(font_size=18,
                                      size_hint_y=0.20,
                                      size_hint_x=0.20)

        self.GL6Contacto = TextInput(font_size=18,
                                     size_hint_y=0.20,
                                     size_hint_x=0.20)

        self.GL6Button1 = Button(text="CONFIRMAR",
                                 size_hint_y=0.20,
                                 size_hint_x=0.20,
                                 font_size=18)

        self.GL6Button2 = Button(text="CANCELAR Y SALIR",
                                 size_hint_y=0.20,
                                 size_hint_x=0.20,
                                 font_size=18)

        self.GL6 = GridLayout(x=0,
                              y=0,
                              cols=1,
                              anchor_x='center',
                              anchor_y='center',
                              size_hint_y=1,
                              size_hint_x=0.80)

        self.GL6.add_widget(self.GL6Label1)
        self.GL6.add_widget(self.GL6Estableciminento)

        self.GL6.add_widget(self.GL6Label2)
        self.GL6.add_widget(self.GL6Direccion)

        self.GL6.add_widget(self.GL6Label3)
        self.GL6.add_widget(self.GL6Contacto)

        self.GL6.add_widget(self.GL6Label4)

        self.GL6.add_widget(self.GL6Button1)
        self.GL6.add_widget(self.GL6Button2)

        self.GL6Button1.bind(on_press=self.CREAR_CONTACTO)  # <----------- Camino al Menu
        self.GL6Button2.bind(on_press=self.CREAR_CONTACTO)  # <----------- Camino a la Salida

        # _______________________________#LISTA DE CONTACTOS___________________________________________




        self.GL7data = [{'text': str(row['nombre']), 'is_selected': False} for row in self.Contactotable]
        ratas_2 = [str(row['nombre']) for row in self.Contactotable]

        print ratas_2

        self.GL7args_converter = lambda row_index, rec: {'text': rec['text'],
                                                         'height': 50,
                                                         'size_hint_y': None,
                                                         'font_size': 18,
                                                         'markup': True,
                                                         'background_color': [1, 1, 1, 1],
                                                         'deselected_color': [0.24, 0.255, 0.173, 0.4],
                                                         'selected_color': [215, 44, 153, 1],
                                                         'color': [0, 0, 0, 0.95]}

        self.GL7list_adapter = ListAdapter(data=self.GL7data, args_converter=self.GL7args_converter, cls=ListItemButton,
                                           propagate_selection_to_data=True, selection_mode='single',
                                           allow_empty_selection=False)

        self.GL7list_view = ListView(adapter=self.GL7list_adapter)

        self.GL7Label1 = Label(text="[color=#404040]CONTACTO SELECCIONADO < MCDONALDS >", markup=True, font_size=18,
                               size_hint_y=None, height=50)

        self.GL7Label2 = Label(text="[color=#404040]CONTACTOS", markup=True, font_size=18, size_hint_y=None, height=50)

        self.GL7Button1 = Button(text="SUGERIR CONTACTO", font_size=18, size_hint_y=None, height=75)

        self.GL7Button2 = Button(text="COMENZAR PEDIDO", font_size=18, size_hint_y=None, height=75)

        self.GL7 = GridLayout(x=0,
                              y=0,
                              cols=1,
                              anchor_x='center',
                              anchor_y='center',
                              size_hint_y=1,
                              size_hint_x=1)
        self.GL7.add_widget(self.GL7Label2)
        self.GL7.add_widget(self.GL7list_view)
        self.GL7.add_widget(self.GL7Label1)
        self.GL7.add_widget(self.GL7Button1)
        self.GL7.add_widget(self.GL7Button2)

        self.GL7Button1.bind(on_press=self.REGISTRAR_CONTACTO)  # <----------- Camino al Menu
        self.GL7Button2.bind(on_press=self.INVENTARIO)  # <----------- Camino a la Salida

        self.GL7list_adapter.bind(on_selection_change=on_selected_item)
        # ________________________________________________________________________________________________



        self.GL8Label1 = Label(text="[color=#404040]Nombre Completo", markup=True,
                               size_hint_y=0.20,
                               size_hint_x=0.20,
                               font_size=18)
        self.GL8Label2 = Label(text="[color=#404040]Identificacion", markup=True,
                               size_hint_y=0.20,
                               size_hint_x=0.20,
                               font_size=18)
        self.GL8Label3 = Label(text="[color=#404040]Hotmail", markup=True,
                               size_hint_y=0.20,
                               size_hint_x=0.20,
                               font_size=18)
        self.GL8Label4 = Label(text="[color=#404040]Sector", markup=True,
                               size_hint_y=0.20,
                               size_hint_x=0.20,
                               font_size=18)
        self.GL8Label5 = Label(text="[color=#404040]Numero Telefonico", markup=True,
                               size_hint_y=0.20,
                               size_hint_x=0.20,
                               font_size=18)
        self.GL8Label6 = Label(text="[color=#404040]Numero", markup=True,
                               size_hint_y=0.20,
                               size_hint_x=0.20,
                               font_size=18)
        self.GL8Label7 = Label(text="[color=#404040]Usuario", markup=True,
                               size_hint_y=0.20,
                               size_hint_x=0.20,
                               font_size=18)
        self.GL8Label8 = Label(text="[color=#404040]Contraseña", markup=True,
                               size_hint_y=0.20,
                               size_hint_x=0.20,
                               font_size=18)

        self.GL8Label9 = Label(text="[color=#404040]Confirmar Contraseña", markup=True,
                               size_hint_y=0.20,
                               size_hint_x=0.20,
                               font_size=18)



        self.GL8Nombre_C = TextInput(font_size=18, multiline= False,
                                     size_hint_y= None , height = 35,background_color=[1, 1, 1,1],background_normal = self.images + 'textbox.png',background_active = self.images + 'textbox.png',
                                     size_hint_x=0.20)

        self.GL8Identificacion = TextInput(font_size=18, multiline= False,
                                           size_hint_y= None , height = 35,background_color=[1, 1, 1,1],background_normal = self.images + 'textbox.png',background_active = self.images + 'textbox.png',
                                           size_hint_x=0.20)

        self.GL8Direccion = TextInput(font_size=18, multiline= False,
                                      size_hint_y= None , height = 35,background_color=[1, 1, 1,1],background_normal = self.images + 'textbox.png',background_active = self.images + 'textbox.png',
                                      size_hint_x=0.20)

        self.GL8Sector = TextInput(font_size=18, multiline= False,
                                   size_hint_y= None , height = 35,background_color=[1, 1, 1,1],background_normal = self.images + 'textbox.png',background_active = self.images + 'textbox.png',
                                   size_hint_x=0.20)

        self.GL8No_telefonico = TextInput(font_size=18, multiline= False,
                                          size_hint_y= None , height = 35,background_color=[1, 1, 1,1],background_normal = self.images + 'textbox.png',background_active = self.images + 'textbox.png',
                                          size_hint_x=0.20)

        self.GL8No_Movil = TextInput(font_size=18, multiline= False,
                                     size_hint_y= None , height = 35,background_color=[1, 1, 1,1],background_normal = self.images + 'textbox.png',background_active = self.images + 'textbox.png',
                                     size_hint_x=0.20)

        self.GL8Usuario = TextInput(font_size=18, multiline= False,
                                    size_hint_y= None , height = 35,background_color=[1, 1, 1,1],background_normal = self.images + 'textbox.png',background_active = self.images + 'textbox.png',
                                    size_hint_x=0.20)

        self.GL8Contrasena = TextInput(font_size=18, multiline= False,
                                       size_hint_y= None , height = 35,background_color=[1, 1, 1,1],background_normal = self.images + 'textbox.png',background_active = self.images + 'textbox.png',
                                       size_hint_x=0.20)

        self.GL8Conf_Contrasena = TextInput(font_size=18, multiline= False,
                                            size_hint_y= None , height = 35,background_color=[1, 1, 1,1],background_normal = self.images + 'textbox.png',background_active = self.images + 'textbox.png',
                                            size_hint_x=0.20)

        self.GL8Button1 = Button(text="CONFIRMAR",
                                 size_hint_y=0.20,
                                 size_hint_x=0.20,
                                 font_size=18)
        self.GL8Button2 = Button(text="CANCELAR Y SALIR",
                                 size_hint_y=0.20,
                                 size_hint_x=0.20,
                                 font_size=18)
        self.GL8Button3 = Button(text="Siguiente",
                                 size_hint_y=0.20,
                                 size_hint_x=0.20,
                                 font_size=18)
        self.GL8Button4 = Button(text="Siguiente",
                                 size_hint_y=0.20,
                                 size_hint_x=0.20,
                                 font_size=18)

        self.GL8 = GridLayout(x=0,
                              y=0,
                              cols=1,
                              anchor_x='center',
                              anchor_y='center',
                              size_hint_y=1,
                              size_hint_x=0.5)
        self.GL8_1 = GridLayout(x=0,
                                y=0,
                                cols=1,
                                anchor_x='center',
                                anchor_y='center',
                                size_hint_y=1,
                                size_hint_x=0.5)
        self.GL8_2 = GridLayout(x=0,
                                y=0,
                                cols=1,
                                anchor_x='center',
                                anchor_y='center',
                                size_hint_y=1,
                                size_hint_x=0.5)

        self.GL8vacio1 = Label(text="[color=#404040]", markup=True,
                               size_hint_y=0.20,
                               size_hint_x=0.20,
                               font_size=18)
        self.GL8vacio2 = Label(text="[color=#404040]", markup=True,
                               size_hint_y=0.20,
                               size_hint_x=0.20,
                               font_size=18)
        self.GL8vacio3 = Label(text="[color=#404040]", markup=True,
                               size_hint_y=0.20,
                               size_hint_x=0.20,
                               font_size=18)

        self.GL8.add_widget(self.GL8Label1)
        self.GL8.add_widget(self.GL8Nombre_C)

        self.GL8.add_widget(self.GL8Label3)
        self.GL8.add_widget(self.GL8Direccion)

        self.GL8.add_widget(self.GL8Label4)
        self.GL8.add_widget(self.GL8Sector)
        self.GL8.add_widget(self.GL8vacio1)

        self.GL8_1.add_widget(self.GL8Label6)
        self.GL8_1.add_widget(self.GL8No_Movil)

        self.GL8_1.add_widget(self.GL8Label2)
        self.GL8_1.add_widget(self.GL8Identificacion)

        self.GL8_1.add_widget(self.GL8vacio2)

        self.GL8_2.add_widget(self.GL8Label7)
        self.GL8_2.add_widget(self.GL8Usuario)

        self.GL8_2.add_widget(self.GL8Label8)
        self.GL8_2.add_widget(self.GL8Contrasena)

        self.GL8_2.add_widget(self.GL8Label9)
        self.GL8_2.add_widget(self.GL8Conf_Contrasena)

        self.GL8_2.add_widget(self.GL8vacio3)

        self.GL8_2.add_widget(self.GL8Button1)
        self.GL8_2.add_widget(self.GL8Button2)



        self.GL8.add_widget(self.GL8Button3)
        self.GL8_1.add_widget(self.GL8Button4)




        print self.UsuarioNO
        self.GL8Button1.bind(on_press=(lambda x: self.CREAR_USUARIO(str(self.UsuarioNO + 1),self.GL8Usuario.text, self.GL8Contrasena.text,self.GL8Direccion.text,"False")))  # <----------- Camino al Menu
        self.GL8Button2.bind(on_press=self.MENU)  # <----------- Camino a la Salida
        self.GL8Button3.bind(on_press=self.REGISTRAR_USUARIO_1)
        self.GL8Button4.bind(on_press=self.REGISTRAR_USUARIO_2)

        # ____________________________________________________________________________________________________

        # VISTA DETALLADA DE PEDIDOS

        self.ID_user = ""
        self.NOMBRE_user = ""
        self.Establecimiento_user = ""
        self.row_count = 0
        self.A = ({"Nombre": "", "ID": ""})
        self.Pedidos = []
        self.ratas_3 = []
        self.ratas_3_id = []
        self.Pedidos_Detalles = []

        self.GL9args_converter = lambda row_index, rec: {'text': rec['text'],
                                                         'size_hint_y': None,
                                                         'height': 60,
                                                         'font_size': 15,
                                                         'markup': True,
                                                         'background_color': [1, 1, 1, 1],
                                                         'deselected_color': parse_color("#7fffffff"),
                                                         'selected_color': [215, 44, 153, 1],
                                                         'color': [0, 0, 0, 0.95]
                                                         }

        self.GL9list_adapter = ListAdapter(data=self.Pedidos, args_converter=self.GL9args_converter, cls=ListItemButton,
                                           propagate_selection_to_data=False, selection_mode='single',
                                           allow_empty_selection=False)

        self.GL9args_converter_2 = lambda row_index, rec: {'text': rec['text'],
                                                           'height': 20,
                                                           'font_size': 15,
                                                           'markup': True,
                                                           'deselected_color': parse_color("#32ff65ff"),
                                                           'selected_color': [215, 44, 153, 1],
                                                           'color': [0, 0, 0, 0.95]
                                                           }

        self.GL9list_adapter_2 = ListAdapter(data=self.Pedidos_Detalles, args_converter=self.GL9args_converter_2,
                                             cls=ListItemLabel, propagate_selection_to_data=True,
                                             selection_mode='single', allow_empty_selection=False)

        self.GL9list_view = ListView(adapter=self.GL9list_adapter, size_hint_y=0.4)
        self.GL9list_view_2 = ListView(adapter=self.GL9list_adapter_2, size_hint_y=None, height=200)

        self.GL9Button_1 = Button(text="Salir", size_hint_y=0.1)
        self.GL9Label_1 = Label(text="asdasd", size_hint_y=0.025, markup=True)

        self.GL9 = GridLayout(x=0, background_color=(1, 1, 1, 1),
                              y=0,
                              cols=2,
                              anchor_x='center',
                              anchor_y='center',
                              spacing = 0,
                              size_hint_y=None,
                              size_hint_x=1)

        self.GL9.bind(minimum_height=self.GL9.setter('height'))

        self.GL9_ScrollView = ScrollView(size_hint=(1, None), size=(Window.width, Window.height))

        self.panel_gl9 = GridLayout(cols = 2 ,size_hint_y = None , size_hint_x = 1)
        self.botones_perfil = ['id', 'usuario', 'password','email' , 'privilegios','fecha_registro' , 'ultimo_ingreso' , 'verification_Id']
        self.panel_gl9.bind(minimum_height=self.panel_gl9.setter('height'))
        self.panel_gl9_root = ScrollView(size_hint=(1, 1), size=(Window.width, Window.height))
        self.panel_gl9_root.add_widget(self.panel_gl9)

        for i in self.Pedidotable:
            if i["pedido_por"] == self.UserU:
                self.BarraGL9_1 = Button(background_down = self.images + "blanco.png" ,text="[color=#404040]HISTORIAL DE PEDIDOS", size_hint_y = None , height = 70, background_color = (1,1,1,1), background_normal = self.images + "blanco.png", markup = True, font_size = 24)
                self.BarraGL9_2 = Button(background_down = self.images + "blanco.png" ,text="", size_hint_y = None , height = 50, background_color = (1,1,1,0), background_normal = self.images + "blanco.png", font_size= 24, markup = True)
                self.panel_gl9.add_widget(self.BarraGL9_1)
                self.panel_gl9.add_widget(self.BarraGL9_2)
                
                self.BarraGL9_3 = Button(background_down = self.images + "color_rojo.png" ,text=i["pedido_id"], size_hint_y = None , height = 50, background_color = (1,1,1,1), background_normal = self.images + "color_rojo.png", font_size = 20)
                self.BarraGL9_4 = Button(background_down = self.images + "color_rojo.png" ,text=i["fecha_pedido"], size_hint_y = None , height = 50, background_color = (1,1,1,1), background_normal = self.images + "color_rojo.png", font_size = 20)
                self.panel_gl9.add_widget(self.BarraGL9_3)
                self.panel_gl9.add_widget(self.BarraGL9_4)
                
                string1 = i["descripcion_del_pedido"]
                str3 = string1.split(",")
                self.PedidoRealizados[:]= []
                for i in str2:
                    print i.encode("utf-8 ")
                    self.PedidoRealizados.append(i.encode("utf-8 "))
                    
                
                

                for y in self.PedidoRealizados:
                    for x in self.PlatoTable:
                        if y == x["id"]:
                            a_B_GL9 = GridLayout(cols=1, spacing=0, size_hint_y=None, height = 120 , size_hint_x = 1)


                            btn3_BGL9 = Button(background_down = self.images + "roro.png" ,size_hint_y=0.025 , background_normal = self.images + 'roro.png', background_color = (1,1,1,1))
                            btn4_BGL9 = Button(background_down = self.images + "roro2.png" ,size_hint_y=0.025 , background_normal = self.images + 'roro2.png', background_color = (1,1,1,1))
                            btn6_BGL9 = Button(background_down = self.images + "asd.png" ,size_hint_y= None ,height=25, background_normal = self.images + 'asd2.png', background_color = (1,1,1,1))
                            btn1_BGL9 = Button(background_down = self.images + "blanco.png" ,text='[b][color=#ff1a1a]Objeto', size_hint_y=0.1, height=30, background_normal = self.images + 'blanco.png', background_color = (1,1,1,1), markup = True , font_size = 18,valign = 'top')
                            btn5_BGL9 = Button(background_down = self.images + "blanco.png" ,text='', size_hint_y=0.050, height=30, background_normal = self.images + 'blanco.png', background_color = (1,1,1,1), markup = True , font_size = '15sp')
                            btn2_BGL9 = Button(background_down = self.images + "blanco.png" ,text='[color=#404040][b].Amazon' , size_hint_y=0.1, height=30, background_normal = self.images + 'blanco.png',background_color = (1,1,1,1), markup   = True, font_size = 18)
                            name_BGL9 = btn.text
                            
                            a_B_GL9.add_widget(btn6_BGL9)
                            a_B_GL9.add_widget(btn1_BGL9)
                            a_B_GL9.add_widget(btn3_BGL9)
                            a_B_GL9.add_widget(btn2_BGL9)
                            a_B_GL9.add_widget(btn4_BGL9)
                            a_B_GL9.add_widget(btn5_BGL9)
                            self.panel_gl9.add_widget(a_B_GL9)

                            a_B_GL9_2 = GridLayout(cols=1, spacing=0, size_hint_y=None, height = 120 , size_hint_x = 1)

                            btn3_BGL9_2 = Button(background_down = self.images + "roro.png" ,size_hint_y=0.025 , background_normal = self.images + 'roro.png', background_color = (1,1,1,1))
                            btn4_BGL9_2 = Button(background_down = self.images + "roro2.png" ,size_hint_y=0.025 , background_normal = self.images + 'roro2.png', background_color = (1,1,1,1))
                            btn6_BGL9_2 = Button(background_down = self.images + "asd2.png" ,size_hint_y= None ,height=25, background_normal = self.images + 'asd2.png', background_color = (1,1,1,1))
                            btn1_BGL9_2 = Button(background_down = self.images + "blanco.png" ,text='[b][color=#404040]500.00 RD$', size_hint_y=0.1, height=30, background_normal = self.images + 'blanco.png', background_color = (1,1,1,1), markup = True , font_size = 18,valign = 'top')
                            btn5_BGL9_2 = Button(background_down = self.images + "blanco.png" ,text='', size_hint_y=0.050, height=30, background_normal = self.images + 'blanco.png', background_color = (1,1,1,1), markup = True , font_size = '15sp')
                            btn2_BGL9_2 = Button(background_down = self.images + "blanco2.png" ,text='[color=#404040][b]DOP' , size_hint_y=0.1, height=30, background_normal = self.images + 'blanco.png',background_color = (1,1,1,1), markup   = True, font_size = 18)
                            name_BGL9_2 = btn.text
                            
                            a_B_GL9_2.add_widget(btn6_BGL9_2)
                            a_B_GL9_2.add_widget(btn1_BGL9_2)
                            a_B_GL9_2.add_widget(btn3_BGL9_2)
                            a_B_GL9_2.add_widget(btn2_BGL9_2)
                            a_B_GL9_2.add_widget(btn4_BGL9_2)
                            a_B_GL9_2.add_widget(btn5_BGL9_2)
                            self.panel_gl9.add_widget(a_B_GL9_2)





        #self.GL9.add_widget(self.GL9list_view)
        #self.GL9.add_widget(self.GL9Label_1)
        #self.GL9.add_widget(self.GL9_Accordion)
        #self.GL9.add_widget(self.GL9_Accordion)
        #self.GL9.add_widget(self.GL9list_view_2)
        #self.GL9.add_widget(self.GL9Button_1)
        self.GL9_ScrollView.add_widget(self.GL9)
        self.GL9Button_1.bind(on_press=self.MENU)
        self.GL9list_adapter.bind(on_selection_change=on_selected_item)

        # ____________________________________________________________________________________________________

        # VISTA DETALLADA DE PEDIDOS





        # ____________________________________________________________________________________________________


        self.popup = Popup(title='Test popup',
                           content=Label(text='Hello world'),
                           size_hint=(None, None),
                           size=(400, 400)
                           )

        self.popup_1 = Popup(title='Lo Sentimos!',
                             content=Label(text='Usuario o Contraseña Incorrectos.', text_size=(300, None)),
                             size_hint=(None, None),
                             size=(400, 400)
                             )

        self.popup_2 = Popup(title='Enhorabuena!',
                             content=Label(
                                 text='Pedido Realizado con Exito. Para ver con detalles su pedido reinicie la session y dirigase al menu de pedidos.',
                                 text_size=(300, None)),
                             size_hint=(None, None),
                             size=(400, 400)
                             )

        self.popup_3 = Popup(title='Lo Sentimos!',
                             content=Label(text='Debe Agregar productos a su factura para proceder.',
                                           text_size=(300, None)),
                             size_hint=(None, None),
                             size=(400, 400)
                             )

        self.popup_4 = Popup(title='Lo Sentimos!',
                             content=Label(text='Debe Agregar productos a su factura para proceder.',
                                           text_size=(300, None)),
                             size_hint=(None, None),
                             size=(400, 400)
                             )

        self.popup_5 = Popup(title='Lo Sentimos!',
                             content=Label(
                                 text='Primero dirigase al Panel de Contactos y seleccione el Contacto al cual quiere realizar su pedido.',
                                 text_size=(300, None)),
                             size_hint=(None, None),
                             size=(400, 400)
                             )

        self.popup_6 = Popup(title='Espere!',
                             content=Label(
                                 text='Sucitando cambios.',
                                 text_size=(150, None)),
                             size_hint=(None, None),
                             size=(150, 50)
                             )              
        # ____________________________________________________________________________________________________






        # ____________________________________________________________________________________________________



        self.GL11Button_1 = Button(text="Volver", size_hint_y=0.1)
        self.GL11Button_2 = Button(text="Aceptar", size_hint_y=0.1)

        self.GL11 = GridLayout(x=0,
                               y=0,
                               cols=1,
                               anchor_x='center',
                               anchor_y='center',
                               size_hint_y=1,
                               size_hint_x=1)


        self.GL11.add_widget(self.GL11Button_1)
        self.GL11.add_widget(self.GL11Button_2)
        self.GL11Button_1.bind(on_press=self.MENU)
        # _________________________________________________________________________________________________

        #self.GL12data = [{'text': str(row['Producto']) + " " + str(row['Precio']) + ".00 RD$ - " + str(row['Establecimiento']), 'is_selected': False}
         #                for row in self.MenuSCtable]



        self.GL12Button_1 = Button(text="Volver", size_hint_y=0.1)

        self.GL12 = GridLayout(x=0,
                               y=0,
                               cols=1,
                               anchor_x='center',
                               anchor_y='center',
                               size_hint_y=1,
                               size_hint_x=1)

#        self.GL12.add_widget(self.GL12list_view)
        self.GL12.add_widget(self.GL12Button_1)

        self.GL12Button_1.bind(on_press=self.MENU)
        # _________________________________________________________________________________________________

        self.panel_busqueda_IN_Layout = GridLayout(cols = 1, size_hint_y = 1, spacing = 0)

        self.panel_busqueda_Layout = GridLayout(cols = 1, size_hint_y = None, spacing = 0)
        self.panel_busqueda_Layout2 = GridLayout(cols = 2, size_hint_y = None, height = 50, spacing = 0)
        self.panel_busqueda_INPUT_TXT = TextInput(size_hint= (1,None), height = 32, background_color = (1,1,1,1), background_normal = self.images + 'textbox.png',background_active = self.images + 'textbox.png',multiline=False)
        self.panel_busqueda_ScrollView = ScrollView(size_hint=(1, 0.3), size=(Window.width, Window.height - 500))
        self.panel_busqueda_Layout.bind(minimum_height=self.panel_busqueda_Layout.setter('height'))
        self.panel_busqueda_Buscarbtn = Button(background_down = self.images + "color_rojoB.png" ,size_hint = (1,None), height = 50, text = "Filtros", markup = True, background_color = (1,1,1,1), background_normal = self.images + 'color_rojo.png')
        self.panel_busqueda_Buscarbtn.bind(on_press = self.SELFILTRO2)
        self.panel_busqueda_Buscarbtn1 = Button(background_down = self.images + "color_rojoB.png" ,size_hint = (1,None), height = 50, text = "Borrar Filtros", markup = True, background_color = (1,1,1,1), background_normal = self.images + 'color_rojo.png')
        
        
        
        self.panel_busqueda_IN_Layout.add_widget(self.panel_busqueda_INPUT_TXT)
        self.panel_busqueda_IN_Layout.add_widget(self.panel_busqueda_ScrollView)
        self.panel_busqueda_IN_Layout.add_widget(self.panel_busqueda_Layout2)
        self.panel_busqueda_Layout2.add_widget(self.panel_busqueda_Buscarbtn)
        self.panel_busqueda_Layout2.add_widget(self.panel_busqueda_Buscarbtn1)
        self.panel_busqueda_ScrollView.add_widget(self.panel_busqueda_Layout)


        self.panel_busqueda = Popup(title='Panel de Busqueda.', markup = True, title_size = 14, title_align = 'center',
                    content = self.panel_busqueda_IN_Layout ,
                    background = "blanco3.png", separator_color = (0,0,0,0),title_color = (0,0,0,.5),
                  size_hint = (.7, .8))
        def actualizar_busqueda():
            self.panel_busqueda_Layout.clear_widgets()
            for i in self.Contactotable:
                    try:
                        texto = self.panel_busqueda_INPUT_TXT.text
                        i["nombre"].index(texto)
                        cajas = GridLayout(cols=3, spacing=0, size_hint_y=None, height = 50 , size_hint_x = 1)
                        caja1 = Button(background_down = self.images + "blanco2.png" ,size_hint = (.2,None), height = 50, text = "[color=#404040]"+ str(i["id"]), markup = True, background_color = (1,1,1,1), background_normal = self.images + 'blanco2.png')
                        caja2 = Button(background_down = self.images + "blanco2.png" ,size_hint = (.6,None), height = 50, text = "[color=#404040][b]"+ i["nombre"] , markup = True, background_color = (1,1,1,1), background_normal = self.images + 'blanco2.png')
                        caja3 = Button(background_down = self.images + "blanco2.png" ,size_hint = (.2,None), height = 50, text = "[color=#404040]>[color=#ffffff]"+str(i["id"]), markup = True, background_color = (1,1,1,1), background_normal = self.images + 'blanco2.png')
                        
                        
                        integer =i["id"]
                        seleccionado = self.Lista_Contactos_IDs[int(integer)-1]
                        
                        caja3.bind(on_press=lambda seleccionado=seleccionado: self.TIENDA(seleccionado.text[31:]))
                        cajas.add_widget(caja1)
                        cajas.add_widget(caja2)
                        cajas.add_widget(caja3)

                        self.panel_busqueda_Layout.add_widget(cajas)
                    except:
                        pass
        text = ""
        self.panel_busqueda_INPUT_TXT.bind(on_text_validate = lambda text = text: actualizar_busqueda())

            

        # _________________________________________________________________________________________________
    
        self.panel_privilegio_IN_Layout = GridLayout(cols = 1, size_hint_y = 1, spacing = 0)

        self.panel_privilegio_Layout = GridLayout(cols = 1, size_hint_y = None, spacing = 0)
        self.panel_privilegio_INPUT_TXT = TextInput(size_hint= (1,None), height = 32, background_color = (1,1,1,1), background_normal = self.images + 'textbox.png',background_active = self.images + 'textbox.png',)
        self.panel_privilegio_ScrollView = ScrollView(size_hint=(1, 0.3), size=(Window.width, Window.height - 500))
        self.panel_privilegio_Layout.bind(minimum_height=self.panel_privilegio_Layout.setter('height'))
        self.panel_privilegio_Buscarbtn = Button(background_down = self.images + "color_rojoB.png" ,size_hint = (1,None), height = 70, text = "[color=#404040]BUSCAR", markup = True, background_color = (1,1,1,1), background_normal = self.images + 'color_rojo.png')



        #self.panel_privilegio_IN_Layout.add_widget(self.panel_privilegio_INPUT_TXT)
        self.panel_privilegio_IN_Layout.add_widget(self.panel_privilegio_ScrollView)
        #self.panel_privilegio_IN_Layout.add_widget(self.panel_privilegio_Buscarbtn)
        self.panel_privilegio_ScrollView.add_widget(self.panel_privilegio_Layout)


        self.panel_privilegio = Popup(title='Seleccione un Privilegio', markup = True, title_size = 14, title_align = 'center',
                    content = self.panel_privilegio_IN_Layout ,
                    background = "blanco3.png", separator_color = (0,0,0,0),title_color = (0,0,0,.5),
                  size_hint = (.7, .8))
        self.privilegiosB = ["Super Administrador","Administrador","Developer", "Usuario FF", "Invitado"]
        for i in range(len(self.privilegiosB)):
                cajasB = GridLayout(cols=1, spacing=0, size_hint_y=None, height = 265 , size_hint_x = 1)
                caja1B = Button(background_down = self.images + "blanco2.png" ,size_hint = (1,None), height = 50, text = "[color=#404040]"+ self.privilegiosB[i], markup = True, background_color = (1,1,1,1), background_normal = self.images + 'blanco2.png')
                textoo = "Me parece increible, esta aplicacion facilita mucho la manera en la que se hacen las cosas, nunca lo habia echo tan rapido y con tanto estilo."
                caja2B = TextInput(disabled = True,text = textoo ,size_hint_y = 0.75 , Readonly = True , Line_Spacing = 3, background_normal = self.images + "blanco3.png" , background_color = (1,1,1,1), font_size = '13sp', background_disabled_normal = self.images + "blanco3.png", disabled_foreground_color = (0,0,0,1))
                caja3B = Button(text = "[color=#404040]seleccionar "+ str(i), size_hint =(1,None), height = 40, background_color = (1,1,1,1), markup = True, background_normal = self.images + "blanco8.png")
                seleccionado = caja3B.text
                
                caja3B.bind(on_press=lambda seleccionado=seleccionado: self.CAMBIARPRIVILEGIO(seleccionado.text[27:]))

                cajasB.add_widget(caja1B)
                cajasB.add_widget(caja2B)
                cajasB.add_widget(caja3B)

                self.panel_privilegio_Layout.add_widget(cajasB)
    
    
        # _________________________________________________________________________________________________

        self.perfil_tienda = GridLayout(cols = 1, spacing = 0, size_hint_y = None)









        self.panel_perfil = GridLayout(cols = 1 ,size_hint_y = None , size_hint_x = 1)
        self.botones_perfil = ['id', 'usuario', 'password','email' , 'privilegios','fecha_registro' , 'ultimo_ingreso' , 'verification_Id']
        self.panel_perfil.bind(minimum_height=self.panel_perfil.setter('height'))
        self.panel_perfil_root = ScrollView(size_hint=(1, 1), size=(Window.width, Window.height),scroll_type = ['content'])
        self.panel_perfil_root.add_widget(self.panel_perfil)
        for i in self.botones_perfil:
            mascara = GridLayout(cols = 2, size_hint_y = None , height = 50)
            LABELMASK = GridLayout(cols = 1, size_hint_y = None , height = 50)
            if i == self.botones_perfil[0]:
                labelperfil = Button(text= "[color=#404040]Perfil" , markup = True, font_size = 18 , background_color = (1,1,1,1) , size_hint_y = 1, height = 100, background_normal = self.images + "color_rojo.png")
                #labelperfil_2 = Label(size_hint_y = None, height = 100)
                LABELMASK.add_widget(labelperfil)
                #mascara.add_widget(labelperfil_2)
                self.panel_perfil.add_widget(LABELMASK)

            label = Button(text = i + " :", background_color = (1,1,1,1), size_hint = (1,None), background_normal = self.images + "color_rojo.png" , height = 50)
            label1 = Button(text = "[color=#404040]Usuario.[b]"+ i , markup = True , size_hint = (1, None), height = 50 , background_color = (1,1,1,1) , background_normal = self.images + "blanco2.png")
            mascara.add_widget(label)
            mascara.add_widget(label1)
            self.panel_perfil.add_widget(mascara)
            
            

            # _________________________________________________________________________________________________

            self.panel_tienda_perfil = GridLayout(cols = 1 ,size_hint_y = None , size_hint_x = 1)
            campos_perfil = ['Nombre','Total Ventas Realizadas' , 'Rating' , 'Ventas Promedio por mes' , 'Email Oficial' , 'Direccion de Transacciones' , 'Pagos Disponibles' , 'Horario Disponible', 'Fecha de Inscripcion']
            self.panel_tienda_perfil.bind(minimum_height=self.panel_tienda_perfil.setter('height'))
            self.panel_tienda_perfil_root = ScrollView(size_hint=(1, 1), size=(Window.width, Window.height))

            self.panel_tienda_perfil_root.add_widget(self.panel_tienda_perfil)

            for i in campos_perfil:
                mascara_B = GridLayout(cols = 2, size_hint_y = None , height = 50)
                LABELMASK_B = GridLayout(cols = 1, size_hint_y = None , height = 50)
                if i == campos_perfil[0]:
                    labelperfil_B = Button(text= "[color=#404040]Perfil de Tienda" , markup = True, font_size = 18 , background_color = (1,1,1,1) , size_hint_y = 1, height = 100, background_normal = self.images + "color_rojo.png")
                    #labelperfil_2 = Label(size_hint_y = None, height = 100)
                    LABELMASK_B.add_widget(labelperfil_B)
                    #mascara_B.add_widget(labelperfil_2)
                    self.panel_tienda_perfil.add_widget(LABELMASK_B)

                label_B = Button(text = i + " :", background_color = (1,1,1,1), size_hint = (1,None), background_normal = self.images + "color_rojo.png" , height = 50)
                label1_B = Button(text = "[color=#404040]Tienda.[b]"+ i , markup = True , size_hint = (1, None), height = 50 , background_color = (1,1,1,1) , background_normal = self.images + "blanco2.png")

                mascara_B.add_widget(label_B)
                mascara_B.add_widget(label1_B)
                self.panel_tienda_perfil.add_widget(mascara_B)

                if i == 'Fecha de Inscripcion':

                    mascara_C = GridLayout(cols = 2, size_hint_y = None , height = 50)
                    a_D_caja_S1_B = Button(background_down = self.images + "color_rojo.png" ,size_hint = (1,None), height = 50, text = "[color=#404040] Comentarios", markup = True, background_color = (1,1,1,1), background_normal = self.images + 'color_rojo.png', font_size = 24 )
                    a_D_caja_S2_B = Button(background_down = self.images + "color_rojo.png" ,size_hint = (1,None), height = 50, text = "[color=#404040]", markup = True, background_color = (1,1,1,1), background_normal = self.images + 'color_rojo.png')
                    mascara_C.add_widget(a_D_caja_S1_B)
                    mascara_C.add_widget(a_D_caja_S2_B)

                    self.panel_tienda_perfil.add_widget(mascara_C)

                    for i in range(5):
                        a_E = GridLayout(cols=1, spacing=0, size_hint_y=None, height = 150 , size_hint_x = 0.8)


                        a_E_Label1 = Label(text ="[color=#404040]Armando José Soto Melo - 17/9/2016" , size_hint_y = 0.25, markup = True)
                        textoo = "Me parece increible, esta aplicacion facilita mucho la manera en la que se hacen las cosas, nunca lo habia echo tan rapido y con tanto estilo."

                        a_E_Input = TextInput(disabled = True,text = textoo ,size_hint_y = 0.75 , Readonly = True , Line_Spacing = 3, background_normal = self.images + "blanco3.png" , background_color = (1,1,1,1), font_size = '13sp', background_disabled_normal = self.images + "blanco3.png", disabled_foreground_color = (0,0,0,1))


                        a_E.add_widget(a_E_Label1)
                        a_E.add_widget(a_E_Input)
                        self.panel_tienda_perfil.add_widget(a_E)

                    mascara_D = GridLayout(cols = 2, size_hint_y = None , height = 50)
                    a_D_caja_S1_C = Button(background_down = self.images + "color_rojo.png" ,size_hint = (1,None), height = 50, text = "[color=#404040] Sugerencias", markup = True, background_color = (1,1,1,1), background_normal = self.images + 'color_rojo.png', font_size = 24 )
                    a_D_caja_S2_C = Button(background_down = self.images + "color_rojo.png" ,size_hint = (1,None), height = 50, text = "[color=#404040]", markup = True, background_color = (1,1,1,1), background_normal = self.images + 'color_rojo.png')
                    mascara_D.add_widget(a_D_caja_S1_C)
                    mascara_D.add_widget(a_D_caja_S2_C)

                    self.panel_tienda_perfil.add_widget(mascara_D)

                    for i in range(5):
                        a_F = GridLayout(cols=1, spacing=0, size_hint_y=None, height = 150 , size_hint_x = 0.8)


                        a_F_Label1 = Label(text ="[color=#404040]Armando José Soto Melo - 17/9/2016" , size_hint_y = 0.25, markup = True)
                        textoo = "Me parece increible, esta aplicacion facilita mucho la manera en la que se hacen las cosas, nunca lo habia echo tan rapido y con tanto estilo."

                        a_F_Input = TextInput(disabled = True,text = textoo ,size_hint_y = 0.75 , Readonly = True , Line_Spacing = 3, background_normal = self.images + "blanco3.png" , background_color = (1,1,1,1), font_size = '13sp', background_disabled_normal = self.images + "blanco3.png", disabled_foreground_color = (0,0,0,1))


                        a_F.add_widget(a_F_Label1)
                        a_F.add_widget(a_F_Input)
                        self.panel_tienda_perfil.add_widget(a_F)











        # _________________________________________________________________________________________________




        self.sugerencia_Titulo = Label(text = "[color=#404040]Sugerencia :)" , background_color = (1,1,1,1),
        size_hint_y = None , height = 50, font_size = 24, markup = True

        )

        self.sugerencia_Button = Button(text = "Listo" , background_color = (1,1,1,1) , border = (1,1,1,1) , background_normal = self.images + "color_rojo.png" , size_hint_y = None , height = 50)
        self.sugerencia_TextInput1 = TextInput(height = 30 , text = "Nombre del Contacto" ,size_hint_y = None , Readonly = True , Line_Spacing = 3, background_normal = self.images + "blanco3.png" , background_color = (1,1,1,1), font_size = '15sp', background_disabled_normal = self.images + "blanco3.png", disabled_foreground_color = (0,0,0,1))
        self.sugerencia_TextInput2 = TextInput(height = 30 , text = "Teléfono" ,size_hint_y = None , Readonly = True , Line_Spacing = 3, background_normal = self.images + "blanco3.png" , background_color = (1,1,1,1), font_size = '15sp', background_disabled_normal = self.images + "blanco3.png", disabled_foreground_color = (0,0,0,1))
        self.sugerencia_TextInput3 = TextInput(height = 30 , text = "Direccion" ,size_hint_y = None , Readonly = True , Line_Spacing = 3, background_normal = self.images + "blanco3.png" , background_color = (1,1,1,1), font_size = '15sp', background_disabled_normal = self.images + "blanco3.png", disabled_foreground_color = (0,0,0,1))
        self.sugerencia_TextInput4 = TextInput(height = 30 , text = "Categoria" ,size_hint_y = None , Readonly = True , Line_Spacing = 3, background_normal = self.images + "blanco3.png" , background_color = (1,1,1,1), font_size = '15sp', background_disabled_normal = self.images + "blanco3.png", disabled_foreground_color = (0,0,0,1))
        
        
        self.sugerencia_Layout.add_widget(self.sugerencia_Titulo)
        self.sugerencia_Layout.add_widget(self.sugerencia_TextInput1)
        self.sugerencia_Layout.add_widget(self.sugerencia_TextInput2)
        self.sugerencia_Layout.add_widget(self.sugerencia_TextInput3)
        self.sugerencia_Layout.add_widget(self.sugerencia_TextInput4)
        
        self.sugerencia_Layout.add_widget(self.sugerencia_Button)
        self.sugerencia_Button.bind(on_press = lambda x: self.CREARSUGERENCIA(self.sugerencia_TextInput1.text , self.sugerencia_TextInput2.text ,
        self.sugerencia_TextInput3.text,self.sugerencia_TextInput4.text))




        #  ________________________________________________________________________________________________

        self.panel_departamentos = GridLayout(cols = 1 , size_hint = (1, None))
        self.panel_deptartamentos_root = ScrollView(size_hint=(1, 1), size=(Window.width, Window.height))
        self.panel_departamentos.bind(minimum_height=self.panel_departamentos.setter('height'))

        self.panel_deptartamentos_root.add_widget(self.panel_departamentos)
        self.Departamentos_array = ["Celulares", "Ropas", "Computadoras", "Electronica", "Comestibles", "Instrumentos", "Video Juegos", "Variety Store"]

        for i in range(len(self.Departamentos_array)):
            vista_departamento = GridLayout(cols = 1 , size_hint = (1,None) , height = 520)
            titulo_departamento = Button(text = "[color=#404040]"+ self.Departamentos_array[i], background_color = (1,1,1,1), markup =True, background_normal = self.images + "blanco7.png", font_size = 24)
            titulo_departamento_B = Button(text = "", background_color = (1,1,1,1), markup =True, background_normal = self.images + "blanco7.png")
            imagen_departamento = Button(background_color = (1,1,1,1), background_normal = self.images + "404.png")
            boton_departamento = Button(text = "[color=#404040][b]>>>", height = 70, size_hint_y = None, background_color = (1,1,1,1) , background_normal = self.images + "blanco.png", markup = True , font_size = 50)
            boton_departamento_B = Button(text = "", height = 70, size_hint_y = None, background_color = (1,1,1,1) , background_normal = self.images + "blanco.png")
            doble_columna_boton = GridLayout(cols = 2, size_hint = (1,None) , height = 70)

            doble_columna_titulo = GridLayout(cols = 2, size_hint = (1,None) , height = 50)

            doble_columna_titulo.add_widget(titulo_departamento)
            doble_columna_titulo.add_widget(titulo_departamento_B)
            doble_columna_boton.add_widget(boton_departamento_B)
            doble_columna_boton.add_widget(boton_departamento)
            vista_departamento.add_widget(doble_columna_titulo)
            vista_departamento.add_widget(imagen_departamento)
            vista_departamento.add_widget(doble_columna_boton)


            self.panel_departamentos.add_widget(vista_departamento)



        # _________________________________________________________________________________________________
        # ESPACIO PARA VARIABLES DE ENTORNO

        self.ESTABLECIMIENTO_SELECCIONADO = ""
        self.SUBTOTAL = 0
        self.ID_Pedido_user = ""
        self.G1 = ""
        self.G2 = ""
        self.Privilegios = ""
        # self.PRECIOS
        Clock.schedule_once(self.SPLASH, 1)



        # ADMINISTRADOR DE USUARIOS
        
        self.panel_Administrador = GridLayout(cols = 1 , size_hint = (1, None))
        self.panel_Administrador_root = ScrollView(size_hint=(1, 1), size=(Window.width, Window.height))
        self.panel_Administrador.bind(minimum_height=self.panel_Administrador.setter('height'))

        self.panel_Administrador_root.add_widget(self.panel_Administrador)
        
        for i in self.Usuariostable:
            vista_usuario = GridLayout(cols = 5 , size_hint = (1,None) , height = 50, spacing = 0)
                
            vista_usuario_label1 = Button(text ="[color=#404040]"+str(i["id"]) , markup = True,  background_normal = self.images + "color_rojo.png" , background_color = (1,1,1,1), size_hint_x = None , width = 25)
            vista_usuario_label2 = Button(text ="[color=#404040]"+i["usuario"] , markup = True, background_normal = self.images + "blanco2.png" , background_color = (1,1,1,1))
            vista_usuario_label3 = Button(text ="[color=#404040]"+i["privilegios"] , markup = True, background_normal = self.images + "blanco2.png" , background_color = (1,1,1,1))
            vista_usuario_label4 = Button(text ="[color=#404040]"+i["verification_Id"] , markup = True, background_normal = self.images + "blanco2.png" , background_color = (1,1,1,1))
            vista_usuario_label5 = Button(text ="[color=#404040]>"+"[/color]"+"[color=#f2f2f2]"+str(i["id"]) , markup = True, background_normal = self.images + "blanco8.png" , background_color = (1,1,1,1), size_hint_x = None , width = 50 )
            seleccionado = vista_usuario_label5.text
            vista_usuario_label5.bind(on_press=lambda seleccionado=seleccionado: self.ADMINISTRAR_USUARIO(seleccionado.text[39:]))
            vista_usuario.add_widget(vista_usuario_label1)
            vista_usuario.add_widget(vista_usuario_label2)
            vista_usuario.add_widget(vista_usuario_label3)
            vista_usuario.add_widget(vista_usuario_label4)
            vista_usuario.add_widget(vista_usuario_label5)
            
            self.panel_Administrador.add_widget(vista_usuario)
            
        # ADMINISTRADOR DE INVITADOS
        
        self.panel2_Administrador = GridLayout(cols = 1 , size_hint = (1, None))
        self.panel2_Administrador_root = ScrollView(size_hint=(1, 1), size=(Window.width, Window.height))
        self.panel2_Administrador.bind(minimum_height=self.panel2_Administrador.setter('height'))
        self.panel2_Administrador2 = GridLayout(cols = 2 , size_hint = (1, None) , height = 64)
        self.panel2_Administrador_root.add_widget(self.panel2_Administrador)
        
        self.panel_busqueda_INPUT_TXT2 = TextInput(size_hint= (1,None), height = 32, background_color = (1,1,1,1), background_normal = self.images + 'blanco3.png',background_active = self.images + 'textboxB2.png',multiline=False)
        self.panel_busqueda_INPUT_TXT3 = Image(source = self.images + "Entypo_d83d(0)_64.png", size_hint = (.2,None), height = 32)
        self.panel_busqueda_INPUT_TXT4 = Button(size_hint= (.2,None), height = 32,border = (1,1,1,1), background_color = (1,1,1,1), background_normal = self.images + 'blanco2B.png',background_active = self.images + 'blanco2B.png',multiline=False)
        self.panel_busqueda_INPUT_TXT4B = Button(size_hint= (.2,None), height = 32,border = (1,1,1,1),  background_color = (1,1,1,1), background_normal = self.images + 'blanco2B.png',background_active = self.images + 'blanco2B.png',multiline=False)
        
        self.panel_busqueda_INPUT_TXT2.bind(on_text_validate = lambda text = text: actualizar_busqueda())
        menu_Administradorbutton5 = Button(text="[color=#404040]"+ "Filtros",  markup = True, background_normal = self.images + "blanco2.png" , background_color = (1,1,1,1),font_size = 16, size_hint = (1,None), height = 50)
        menu_Administradorbutton51 = Button(text="[color=#404040]"+ "Filtar por Usuario",  markup = True, background_normal = self.images + "blanco2.png" , background_color = (1,1,1,1),font_size = 16, size_hint = (1,None), height = 50)
        menu_Administradorbutton52 = Button(text="[color=#404040]"+ "Filtrar por Equipo",  markup = True, background_normal = self.images + "blanco2.png" , background_color = (1,1,1,1),font_size = 16, size_hint = (1,None), height = 50)
        menu_Administradorbutton53 = Button(text="[color=#404040]"+ "Filtrar por Estado",  markup = True, background_normal = self.images + "blanco2.png" , background_color = (1,1,1,1),font_size = 16, size_hint = (1,None), height = 50)
        menu_Administradorbutton54 = Button(text="[color=#404040]"+ "Borrar Filtros",  markup = True, background_normal = self.images + "blanco2.png" , background_color = (1,1,1,1),font_size = 16, size_hint = (1,None), height = 50)
        
        self.panel2_Administrador2.add_widget(self.panel_busqueda_INPUT_TXT3)
        self.panel2_Administrador2.add_widget(self.panel_busqueda_INPUT_TXT2)
        self.panel2_Administrador2.add_widget(self.panel_busqueda_INPUT_TXT4)
        self.panel2_Administrador2.add_widget(self.panel_busqueda_INPUT_TXT4B)
        
        menu_Administradorbutton5.bind(on_press = self.SELFILTRO)
        self.panel2_Administrador.add_widget(self.panel2_Administrador2)
        
        self.panel2_Administrador.add_widget(menu_Administradorbutton5)
        #self.panel2_Administrador.add_widget(menu_Administradorbutton51)
        #self.panel2_Administrador.add_widget(menu_Administradorbutton52)
        #self.panel2_Administrador.add_widget(menu_Administradorbutton53)
        self.panel2_Administrador.add_widget(menu_Administradorbutton54)
        
        
        self.panel2_Administrador.bind(on_press = self.SELFILTRO)
        
        for i in self.Pedidotable:
            vista_usuario2 = GridLayout(cols = 5 , size_hint = (1,None) , height = 50, spacing = 0)
            vista_usuario2_label1 = Button(text ="[color=#404040]"+str(i["pedido_id"]) , markup = True,  background_normal = self.images + "color_rojo.png" , background_color = (1,1,1,1), size_hint_x = None , width = 25)
            vista_usuario2_label2 = Button(text ="[color=#404040]"+i["pedido_por"] , markup = True, background_normal = self.images + "blanco2.png" , background_color = (1,1,1,1))
            vista_usuario2_label3 = Button(text ="[color=#404040]"+i["estado"] , markup = True, background_normal = self.images + "blanco2.png" , background_color = (1,1,1,1))
            vista_usuario2_label4 = Button(text ="[color=#404040]"+i["fecha_pedido"] , markup = True, background_normal = self.images + "blanco2.png" , background_color = (1,1,1,1))
            vista_usuario2_label5 = Button(text ="[color=#404040]>"+"[/color]"+"[color=#f2f2f2]"+str(i["pedido_id"]) , markup = True, background_normal = self.images + "blanco8.png" , background_color = (1,1,1,1), size_hint_x = None , width = 50 )
            seleccionado = vista_usuario2_label5.text
            vista_usuario2_label5.bind(on_press=lambda seleccionado=seleccionado: self.ADMPEDIDOS(seleccionado.text[39:]))
            vista_usuario2.add_widget(vista_usuario2_label1)
            vista_usuario2.add_widget(vista_usuario2_label2)
            vista_usuario2.add_widget(vista_usuario2_label3)
            vista_usuario2.add_widget(vista_usuario2_label4)
            vista_usuario2.add_widget(vista_usuario2_label5)
            
            self.panel2_Administrador.add_widget(vista_usuario2)
            
        def Filtrar(a):
            print("Filtrando")
            self.panel2_Administrador.clear_widgets()
            self.panel2_Administrador.add_widget(self.panel2_Administrador2)
            self.panel2_Administrador.add_widget(menu_Administradorbutton5)
            self.panel2_Administrador.add_widget(menu_Administradorbutton54)
            
            
            self.panel2_Administrador.bind(on_press = self.SELFILTRO)
            
            for i in self.Pedidotable:
                if i[self.Filtro] == self.panel_busqueda_INPUT_TXT2.text:
                    vista_usuario2 = GridLayout(cols = 5 , size_hint = (1,None) , height = 50, spacing = 0)
                    vista_usuario2_label1 = Button(text ="[color=#404040]"+str(i["pedido_id"]) , markup = True,  background_normal = self.images + "color_rojo.png" , background_color = (1,1,1,1), size_hint_x = None , width = 25)
                    vista_usuario2_label2 = Button(text ="[color=#404040]"+i["pedido_por"] , markup = True, background_normal = self.images + "blanco2.png" , background_color = (1,1,1,1))
                    vista_usuario2_label3 = Button(text ="[color=#404040]"+i["estado"] , markup = True, background_normal = self.images + "blanco2.png" , background_color = (1,1,1,1))
                    vista_usuario2_label4 = Button(text ="[color=#404040]"+i["fecha_pedido"] , markup = True, background_normal = self.images + "blanco2.png" , background_color = (1,1,1,1))
                    vista_usuario2_label5 = Button(text ="[color=#404040]>"+"[/color]"+"[color=#f2f2f2]"+str(i["pedido_id"]) , markup = True, background_normal = self.images + "blanco8.png" , background_color = (1,1,1,1), size_hint_x = None , width = 50 )
                    seleccionado = vista_usuario2_label5.text
                    vista_usuario2_label5.bind(on_press=lambda seleccionado=seleccionado: self.ADMINISTRAR_USUARIO(seleccionado.text[39:]))
                    vista_usuario2.add_widget(vista_usuario2_label1)
                    vista_usuario2.add_widget(vista_usuario2_label2)
                    vista_usuario2.add_widget(vista_usuario2_label3)
                    vista_usuario2.add_widget(vista_usuario2_label4)
                    vista_usuario2.add_widget(vista_usuario2_label5)
                    self.panel2_Administrador.add_widget(vista_usuario2)
                elif self.Filtro == "contacto":
                    if i[self.Filtro] == int(self.panel_busqueda_INPUT_TXT2.text):
                        vista_usuario3 = GridLayout(cols = 5 , size_hint = (1,None) , height = 50, spacing = 0)
                        vista_usuario3_label1 = Button(text ="[color=#404040]"+str(i["pedido_id"]) , markup = True,  background_normal = self.images + "color_rojo.png" , background_color = (1,1,1,1), size_hint_x = None , width = 25)
                        vista_usuario3_label2 = Button(text ="[color=#404040]"+i["pedido_por"] , markup = True, background_normal = self.images + "blanco2.png" , background_color = (1,1,1,1))
                        vista_usuario3_label3 = Button(text ="[color=#404040]"+i["estado"] , markup = True, background_normal = self.images + "blanco2.png" , background_color = (1,1,1,1))
                        vista_usuario3_label4 = Button(text ="[color=#404040]"+i["fecha_pedido"] , markup = True, background_normal = self.images + "blanco2.png" , background_color = (1,1,1,1))
                        vista_usuario3_label5 = Button(text ="[color=#404040]>"+"[/color]"+"[color=#f2f2f2]"+str(i["pedido_id"]) , markup = True, background_normal = self.images + "blanco8.png" , background_color = (1,1,1,1), size_hint_x = None , width = 50 )
                        seleccionado = vista_usuario3_label5.text
                        vista_usuario3_label5.bind(on_press=lambda seleccionado=seleccionado: self.ADMINISTRAR_USUARIO(seleccionado.text[39:]))
                        vista_usuario3.add_widget(vista_usuario3_label1)
                        vista_usuario3.add_widget(vista_usuario3_label2)
                        vista_usuario3.add_widget(vista_usuario3_label3)
                        vista_usuario3.add_widget(vista_usuario3_label4)
                        vista_usuario3.add_widget(vista_usuario3_label5)
                        self.panel2_Administrador.add_widget(vista_usuario3)
                
                
        self.panel_busqueda_INPUT_TXT2.bind(on_text_validate = Filtrar)
          
            
        # ADMINISTRADOR DE MENUS
        
        self.Menu_Administrador = GridLayout(cols = 1 , size_hint = (1, None))
        self.Menu_Administrador_root = ScrollView(size_hint=(1, 1), size=(Window.width, Window.height))
        self.Menu_Administrador.bind(minimum_height=self.Menu_Administrador.setter('height'))

        self.Menu_Administrador_root.add_widget(self.Menu_Administrador)
        
        
        menu_Administradorbutton4 = Button(text="[color=#404040]"+ "Crear Menu",  markup = True, background_normal = self.images + "blanco2.png" , background_color = (1,1,1,1),font_size = 16, size_hint = (1,None), height = 50)
        self.Menu_Administrador.add_widget(menu_Administradorbutton4)
        menu_Administradorbutton4.bind(on_press = self.CREAR_MENU_P)
        for i in self.Menutable:
            vista_Menu = GridLayout(cols = 5 , size_hint = (1,None) , height = 50, spacing = 0)
            vista_Menu_label1 = Button(text ="[color=#404040]"+str(i["id"]) , markup = True,  background_normal = self.images + "color_rojo.png" , background_color = (1,1,1,1), size_hint_x = None , width = 25)
            vista_Menu_label2 = Button(text ="[color=#404040]"+i["menu_titulo"] , markup = True, background_normal = self.images + "blanco2.png" , background_color = (1,1,1,1))
            vista_Menu_label3 = Button(text ="[color=#404040]"+i["categoria"] , markup = True, background_normal = self.images + "blanco2.png" , background_color = (1,1,1,1))
            vista_Menu_label4 = Button(text ="[color=#404040]"+str(i["contacto"]) , markup = True, background_normal = self.images + "blanco2.png" , background_color = (1,1,1,1))
            vista_Menu_label5 = Button(text ="[color=#404040]>"+"[/color]"+"[color=#f2f2f2]"+str(i["id"]) , markup = True, background_normal = self.images + "blanco8.png" , background_color = (1,1,1,1), size_hint_x = None , width = 50 )
            seleccionado = vista_Menu_label5.text
            #vista_Menu_label5.bind(on_press=lambda seleccionado=seleccionado: self.ADMINISTRAR_USUARIO(seleccionado.text[39:]))
            vista_Menu.add_widget(vista_Menu_label1)
            vista_Menu.add_widget(vista_Menu_label2)
            vista_Menu.add_widget(vista_Menu_label3)
            vista_Menu.add_widget(vista_Menu_label4)
            vista_Menu.add_widget(vista_Menu_label5)
            
            self.Menu_Administrador.add_widget(vista_Menu)
            
        # ADMINISTRADOR DE CATEGORIAS
        
        self.panel_Categorias = GridLayout(cols = 1 , size_hint = (1, None))
        self.panel_Categorias_root = ScrollView(size_hint=(1, 1), size=(Window.width, Window.height))
        self.panel_Categorias.bind(minimum_height=self.panel_Categorias.setter('height'))
        self.panel_Categorias_root.add_widget(self.panel_Categorias)
        menu_Administradorbutton2 = Button(text="[color=#404040]"+ "Crear Categoria",  markup = True, background_normal = self.images + "blanco2.png" , background_color = (1,1,1,1),font_size = 16, size_hint = (1,None), height = 50)
        self.panel_Categorias.add_widget(menu_Administradorbutton2)
        menu_Administradorbutton2.bind(on_press = self.CREAR_CATEGORIA)
        
        for i in self.Categoriatable:
            vista_categoria = GridLayout(cols = 5 , size_hint = (1,None) , height = 50, spacing = 0)
                
            vista_categoria_label1 = Button(text ="[color=#404040]"+str(i["id"]) , markup = True,  background_normal = self.images + "color_rojo.png" , background_color = (1,1,1,1), size_hint_x = None , width = 25)
            vista_categoria_label2 = Button(text ="[color=#404040]"+i["categoria"] , markup = True, background_normal = self.images + "blanco2.png" , background_color = (1,1,1,1))
            vista_categoria_label3 = Button(text ="[color=#404040]"+i["fecha_creacion"] , markup = True, background_normal = self.images + "blanco2.png" , background_color = (1,1,1,1))
            vista_categoria_label4 = Button(text ="[color=#404040]"+i["creada_por"] , markup = True, background_normal = self.images + "blanco2.png" , background_color = (1,1,1,1))
            vista_categoria_label5 = Button(text ="[color=#404040]>"+"[/color]"+"[color=#f2f2f2]"+str(i["id"]) , markup = True, background_normal = self.images + "blanco8.png" , background_color = (1,1,1,1), size_hint_x = None , width = 50 )
            seleccionado = vista_categoria_label5.text
            #vista_categoria_label5.bind(on_press=lambda seleccionado=seleccionado: self.ADMINISTRAR_USUARIO(seleccionado.text[39:]))
            vista_categoria.add_widget(vista_categoria_label1)
            vista_categoria.add_widget(vista_categoria_label2)
            vista_categoria.add_widget(vista_categoria_label3)
            vista_categoria.add_widget(vista_categoria_label4)
            vista_categoria.add_widget(vista_categoria_label5)
            
            self.panel_Categorias.add_widget(vista_categoria)
        
        
        # ADMINISTACION DE USUARIO SELECCIONADO
           
        self.panel_Administrado = GridLayout(cols = 1 , size_hint = (1, None))
        self.panel_Administrado_root = ScrollView(size_hint=(1, 1), size=(Window.width, Window.height))
        self.panel_Administrado.bind(minimum_height=self.panel_Administrado.setter('height'))

        self.panel_Administrado_root.add_widget(self.panel_Administrado)
            
        vista_usuario2 = GridLayout(cols = 1 , size_hint = (1,None) , spacing = 0, height = 325)
        vista_usuario3 = GridLayout(cols = 1 , size_hint = (1,None) , spacing = 0, height = 70)
        vista_usuario2_doble = GridLayout ( cols = 2 , size_hint = (1,None) ,height = 410, spacing = 0)
        
        vista_usuario2_imagen = Button(background_normal = self.images + "PP.png" , background_color = (1,1,1,1))
        
        vista_usuario2_perfil = Button(text ="Usuario" , markup = True, background_normal = self.images + "color_rojo.png" , background_color = (1,1,1,1), size_hint_y = None , height = 50 , font_size = 24)
        vista_usuario2_perfilB = Button(markup = True, background_normal = self.images + "color_rojo.png" , background_color = (1,1,1,1), size_hint_y = None , height = 50)
        
        vista_usuario2_perfil1 = Button(text ="[color=#404040]Nombre:" , markup = True, background_normal = self.images + "blanco.png" , background_color = (1,1,1,1), size_hint_y = None , height = 50)
        self.vista_usuario2_perfil1B = Button(text ="[color=#404040]Usuario.Nombre" , markup = True, background_normal = self.images + "blanco.png" , background_color = (1,1,1,1), size_hint_y = None , height = 50)
        vista_usuario2_perfil2 = Button(text ="[color=#404040]Email" , markup = True, background_normal = self.images + "blanco.png" , background_color = (1,1,1,1), size_hint_y = None , height = 50)
        self.vista_usuario2_perfil2B = Button(text ="[color=#404040]Usuario.Email" ,markup = True, background_normal = self.images + "blanco.png" , background_color = (1,1,1,1), size_hint_y = None , height = 50)
        vista_usuario2_perfil3 = Button(text ="[color=#404040]Fecha Creado:" , markup = True, background_normal = self.images + "blanco.png" , background_color = (1,1,1,1), size_hint_y = None , height = 50)
        self.vista_usuario2_perfil3B = Button(text ="[color=#404040]Usuario.Creacion" ,markup = True,background_normal = self.images + "blanco.png" , background_color = (1,1,1,1), size_hint_y = None , height = 50)
        vista_usuario2_perfil4 = Button(text ="[color=#404040]Ultima Session:" , markup = True, background_normal = self.images + "blanco.png" , background_color = (1,1,1,1), size_hint_y = None , height = 50)
        self.vista_usuario2_perfil4B = Button(text ="[color=#404040]Usuario.Ultima Session" , markup = True ,background_normal = self.images + "blanco.png" , background_color = (1,1,1,1), size_hint_y = None , height = 50)
        vista_usuario2_perfil5 = Button(text ="[color=#404040]ID:" , markup = True, background_normal = self.images + "blanco.png" , background_color = (1,1,1,1), size_hint_y = None , height = 50)
        self.vista_usuario2_perfil5B = Button(text ="[color=#404040]Usuario.ID" , markup = True, background_normal = self.images + "blanco.png" , background_color = (1,1,1,1), size_hint_y = None , height = 50)
        vista_usuario2_perfil6 = Button(text ="[color=#404040]Privilegios:" , markup = True, background_normal = self.images + "blanco.png" , background_color = (1,1,1,1), size_hint_y = None , height = 50)
        self.vista_usuario2_perfil6B = Button(text ="[color=#404040]Usuario.Privilegios" , markup = True, background_normal = self.images + "blanco.png" , background_color = (1,1,1,1), size_hint_y = None , height = 50)
        
        vista_usuario3_Button1 = Button(text= "Eliminar",  markup = True, background_normal = self.images + "color_rojo.png" , background_color = (1,1,1,1),font_size = 16)
        vista_usuario3_Button2 = Button(text= "[color=#404040]Cambiar Privilegios", markup = True, background_normal = self.images + "blanco7.png" , background_color = (1,1,1,1),font_size = 16)
        vista_usuario3_Button3 = Button(text= "Guardar", markup = True, background_normal = self.images + "color_rojo.png" , background_color = (1,1,1,1),font_size = 16)
        vista_usuario3_Button4 = Button(text= "Volver", markup = True, background_normal = self.images + "color_rojo.png" , background_color = (1,1,1,1), font_size = 16)
        vista_usuario3_Button2.bind(on_press = self.PANELPRIVILEGIOS)
        btn6_F = Image(source=self.images + "asd.png", size_hint = (1, None), height = 25, allow_stretch = True, keep_ratio = False) 
        vista_usuario2.add_widget(btn6_F)
        vista_usuario2.add_widget(vista_usuario2_imagen)
        #vista_usuario3.add_widget(vista_usuario3_Button1)
        vista_usuario3.add_widget(vista_usuario3_Button2)
        #vista_usuario3.add_widget(vista_usuario3_Button4)
        vista_usuario2_doble.add_widget(vista_usuario2_perfil)
        vista_usuario2_doble.add_widget(vista_usuario2_perfilB)
        vista_usuario2_doble.add_widget(vista_usuario2_perfil1)
        vista_usuario2_doble.add_widget(self.vista_usuario2_perfil1B)
        vista_usuario2_doble.add_widget(vista_usuario2_perfil2)
        vista_usuario2_doble.add_widget(self.vista_usuario2_perfil2B)
        vista_usuario2_doble.add_widget(vista_usuario2_perfil3)
        vista_usuario2_doble.add_widget(self.vista_usuario2_perfil3B)
        vista_usuario2_doble.add_widget(vista_usuario2_perfil4)
        vista_usuario2_doble.add_widget(self.vista_usuario2_perfil4B)
        vista_usuario2_doble.add_widget(vista_usuario2_perfil5)
        vista_usuario2_doble.add_widget(self.vista_usuario2_perfil5B)
        vista_usuario2_doble.add_widget(vista_usuario2_perfil6)
        vista_usuario2_doble.add_widget(self.vista_usuario2_perfil6B)
        self.panel_Administrado.add_widget(vista_usuario2)
        self.panel_Administrado.add_widget(vista_usuario2_doble)
        self.panel_Administrado.add_widget(vista_usuario3)
        


        
        
        # ___________________________________________________________________________________________
        #PANEL DE CONTACTOS
        
        self.panel_Contactos = GridLayout(cols = 1 , size_hint = (1, None))
        self.panel_Contactos_root = ScrollView(size_hint=(1, 1), size=(Window.width, Window.height))
        self.panel_Contactos.bind(minimum_height=self.panel_Contactos.setter('height'))

        self.panel_Contactos_root.add_widget(self.panel_Contactos)
        menu_Administradorbutton3 = Button(text="[color=#404040]"+ "Crear Contacto",  markup = True, background_normal = self.images + "blanco2.png" , background_color = (1,1,1,1),font_size = 16, size_hint = (1,None), height = 50)
        self.panel_Contactos.add_widget(menu_Administradorbutton3)
        menu_Administradorbutton3.bind(on_press = self.CONTACTOSPOPUP)
        for i in self.Contactotable:
            vista_usuario2 = GridLayout(cols = 5 , size_hint = (1,None) , height = 50, spacing = 1)
            
            vista_usuario2_labelb1 = Button(text ="[color=#404040]"+ str(i["id"]) , markup = True,  background_normal = self.images + "color_rojo.png" , background_color = (1,1,1,1), size_hint_x = None , width = 25)
            vista_usuario2_labelb2 = Button(text ="[color=#404040]" + i["nombre"] , markup = True, background_normal = self.images + "blanco.png" , background_color = (1,1,1,1))
            vista_usuario2_labelb3 = Button(text ="[color=#404040]"+i["telefono"] , markup = True, background_normal = self.images + "blanco.png" , background_color = (1,1,1,1))
            vista_usuario2_labelb4 = Button(text ="[color=#404040]"+i["direccion"] , markup = True, background_normal = self.images + "blanco.png" , background_color = (1,1,1,1))
            vista_usuario2_labelb4 = Button(text ="[color=#404040]"+self.categorias[i["categoria"]] , markup = True, background_normal = self.images + "blanco.png" , background_color = (1,1,1,1))
            vista_usuario2_labelb5 = Button(text ="[color=#404040]>[/color][color=#f2f2f2]"+str(i["id"]) , markup = True, background_normal = self.images + "blanco.png" , background_color = (1,1,1,1), size_hint_x = None , width = 50 )
            seleccionado = vista_usuario2_labelb5.text
            vista_usuario2_labelb5.bind(on_press = lambda seleccionado = seleccionado: self.ADMCONTACTOS(seleccionado.text[39:]))
            vista_usuario2.add_widget(vista_usuario2_labelb1)
            vista_usuario2.add_widget(vista_usuario2_labelb2)
            vista_usuario2.add_widget(vista_usuario2_labelb3)
            vista_usuario2.add_widget(vista_usuario2_labelb4)
            vista_usuario2.add_widget(vista_usuario2_labelb5)
            
            self.panel_Contactos.add_widget(vista_usuario2)
            
        # ____________________________________________________________________________________________________
        #PANEL DE SUGERENCIAS
        
        self.panel_Sugerencias = GridLayout(cols = 1 , size_hint = (1, None))
        self.panel_Sugerencias_root = ScrollView(size_hint=(1, 1), size=(Window.width, Window.height))
        self.panel_Sugerencias.bind(minimum_height=self.panel_Sugerencias.setter('height'))

        self.panel_Sugerencias_root.add_widget(self.panel_Sugerencias)
        
        #menu_Administradorbutton3 = Button(text="[color=#404040]"+ "Crear Contacto",  markup = True, background_normal = self.images + "blanco2.png" , background_color = (1,1,1,1),font_size = 16, size_hint = (1,None), height = 50)
        #self.panel_Sugerencias.add_widget(menu_Administradorbutton3)
        #menu_Administradorbutton3.bind(on_press = self.CONTACTOSPOPUP)
        
        for i in self.Sugerenciastable:
            vista_usuario3 = GridLayout(cols = 5 , size_hint = (1,None) , height = 50, spacing = 1)
            
            vista_usuario3_labelb1 = Button(text ="[color=#404040]"+ str(i["id"]) , markup = True,  background_normal = self.images + "color_rojo.png" , background_color = (1,1,1,1), size_hint_x = None , width = 25)
            vista_usuario3_labelb2 = Button(text ="[color=#404040]" + i["nombre"] , markup = True, background_normal = self.images + "blanco.png" , background_color = (1,1,1,1))
            vista_usuario3_labelb3 = Button(text ="[color=#404040]"+i["telefono"] , markup = True, background_normal = self.images + "blanco.png" , background_color = (1,1,1,1))
            vista_usuario3_labelb4 = Button(text ="[color=#404040]"+i["direccion"] , markup = True, background_normal = self.images + "blanco.png" , background_color = (1,1,1,1))
            vista_usuario3_labelb4 = Button(text ="[color=#404040]"+i["categoria"] , markup = True, background_normal = self.images + "blanco.png" , background_color = (1,1,1,1))
            vista_usuario3_labelb5 = Button(text ="[color=#404040]>[/color][color=#f2f2f2]"+str(i["id"]) , markup = True, background_normal = self.images + "blanco.png" , background_color = (1,1,1,1), size_hint_x = None , width = 50 )
            seleccionado = vista_usuario3_labelb5.text
            vista_usuario3_labelb5.bind(on_press = lambda seleccionado = seleccionado: self.ADMSUGERENCIAS(seleccionado.text[39:]))
            vista_usuario3.add_widget(vista_usuario3_labelb1)
            vista_usuario3.add_widget(vista_usuario3_labelb2)
            vista_usuario3.add_widget(vista_usuario3_labelb3)
            vista_usuario3.add_widget(vista_usuario3_labelb4)
            vista_usuario3.add_widget(vista_usuario3_labelb5)
            
            self.panel_Sugerencias.add_widget(vista_usuario3)
            
            
        
        # ADMINISTRADOR DE SUGERENCIAS
        
        self.panel_AdmSugerencias = GridLayout(cols = 1 , size_hint = (1, None))
        self.panel_AdmSugerencias_root = ScrollView(size_hint=(1, 1), size=(Window.width, Window.height))
        self.panel_AdmSugerencias.bind(minimum_height=self.panel_AdmSugerencias.setter('height'))

        self.panel_AdmSugerencias_root.add_widget(self.panel_AdmSugerencias)
            
        vista_sugerencia2 = GridLayout(cols = 1 , size_hint = (1,None) , spacing = 0, height = 300)
        vista_sugerencia3 = GridLayout(cols = 1 , size_hint = (1,None) , spacing = 0, height = 100)
        vista_sugerencia2_doble = GridLayout ( cols = 2 , size_hint = (1,None) ,height = 410, spacing = 0)
        
        btn6_H = Image(source=self.images + "asd.png", size_hint = (1, None), height = 25, allow_stretch = True, keep_ratio = False) 
        
        
        vista_sugerencia2_imagen = Button(background_normal = self.images + "PP.png" , background_color = (1,1,1,1))
        
        vista_sugerencia2_perfil = Button(text ="Sugerencia" , markup = True, background_normal = self.images + "color_rojo.png" , background_color = (1,1,1,1), size_hint_y = None , height = 50 , font_size = 24)
        vista_sugerencia2_perfilB = Button(markup = True, background_normal = self.images + "color_rojo.png" , background_color = (1,1,1,1), size_hint_y = None , height = 50)
        
        vista_sugerencia2_perfil1 = Button(text ="[color=#404040]Local" , markup = True, background_normal = self.images + "blanco.png" , background_color = (1,1,1,1), size_hint_y = None , height = 50)
        self.vista_sugerencia2_perfil1B = Button(text ="[color=#404040]Sugerencia.Nombre" , markup = True, background_normal = self.images + "blanco.png" , background_color = (1,1,1,1), size_hint_y = None , height = 50)
        vista_sugerencia2_perfil2 = Button(text ="[color=#404040]Categoria" , markup = True, background_normal = self.images + "blanco.png" , background_color = (1,1,1,1), size_hint_y = None , height = 50)
        self.vista_sugerencia2_perfil2B = Button(text ="[color=#404040]Sugerencia.Categoria" ,markup = True, background_normal = self.images + "blanco.png" , background_color = (1,1,1,1), size_hint_y = None , height = 50)
        vista_sugerencia2_perfil3 = Button(text ="[color=#404040]Teléfono:" , markup = True, background_normal = self.images + "blanco.png" , background_color = (1,1,1,1), size_hint_y = None , height = 50)
        self.vista_sugerencia2_perfil3B = Button(text ="[color=#404040]Sugerncia.Creacion" ,markup = True,background_normal = self.images + "blanco.png" , background_color = (1,1,1,1), size_hint_y = None , height = 50)
        vista_sugerencia2_perfil4 = Button(text ="[color=#404040]Direccion:" , markup = True, background_normal = self.images + "blanco.png" , background_color = (1,1,1,1), size_hint_y = None , height = 50)
        self.vista_sugerencia2_perfil4B = Button(text ="[color=#404040]Sugerencia.Ultima Session" , markup = True ,background_normal = self.images + "blanco.png" , background_color = (1,1,1,1), size_hint_y = None , height = 50)
        vista_sugerencia2_perfil5 = Button(text ="[color=#404040]Sugerido por:" , markup = True, background_normal = self.images + "blanco.png" , background_color = (1,1,1,1), size_hint_y = None , height = 50)
        self.vista_sugerencia2_perfil5B = Button(text ="[color=#404040]Usuario.ID" , markup = True, background_normal = self.images + "blanco.png" , background_color = (1,1,1,1), size_hint_y = None , height = 50)
        vista_sugerencia2_perfil6 = Button(text ="[color=#404040]Fecha sugerido:" , markup = True, background_normal = self.images + "blanco.png" , background_color = (1,1,1,1), size_hint_y = None , height = 50)
        self.vista_sugerencia2_perfil6B = Button(text ="[color=#404040]Usuario.Privilegios" , markup = True, background_normal = self.images + "blanco.png" , background_color = (1,1,1,1), size_hint_y = None , height = 50)
        vista_sugerencia2_perfil7 = Button(text ="" , markup = True, background_normal = self.images + "blanco.png" , background_color = (1,1,1,1), size_hint_y = None , height = 50)
        self.vista_sugerencia2_perfil7B = Button(text ="asdasd" , markup = True, background_normal = self.images + "blanco.png" , background_color = (1,1,1,1), size_hint_y = None , height = 50)
        
        vista_sugerencia3_Button1 = Button(text= "[color=#404040]Aceptar y Registrar",  markup = True, background_normal = self.images + "blanco2C.png" , background_color = (1,1,1,1),font_size = 16)
        vista_sugerencia3_Button2 = Button(text= "[color=#404040]Eliminar", markup = True, background_normal = self.images + "blanco2.png" , background_color = (1,1,1,1),font_size = 16)
        vista_sugerencia3_Button3 = Button(text= "Guardar", markup = True, background_normal = self.images + "color_rojo.png" , background_color = (1,1,1,1),font_size = 16)
        vista_sugerencia3_Button4 = Button(text= "Volver", markup = True, background_normal = self.images + "color_rojo.png" , background_color = (1,1,1,1), font_size = 16)
        vista_sugerencia2.add_widget(btn6_H)
        vista_sugerencia2.add_widget(vista_sugerencia2_imagen)
        vista_sugerencia3.add_widget(vista_sugerencia3_Button1)
        vista_sugerencia3.add_widget(vista_sugerencia3_Button2)
        vista_sugerencia3_Button1.bind(on_press = self.ADMSUGERENCIAS_REGISTRAR)
        vista_sugerencia3_Button2.bind(on_press = self.ADMSUGERENCIAS_ELIMINAR)
        #vista_sugerencia3.add_widget(vista_sugerencia3_Button4)
        vista_sugerencia2_doble.add_widget(vista_sugerencia2_perfil)
        vista_sugerencia2_doble.add_widget(vista_sugerencia2_perfilB)
        vista_sugerencia2_doble.add_widget(vista_sugerencia2_perfil7)
        vista_sugerencia2_doble.add_widget(self.vista_sugerencia2_perfil7B)
        vista_sugerencia2_doble.add_widget(vista_sugerencia2_perfil1)
        vista_sugerencia2_doble.add_widget(self.vista_sugerencia2_perfil1B)
        vista_sugerencia2_doble.add_widget(vista_sugerencia2_perfil2)
        vista_sugerencia2_doble.add_widget(self.vista_sugerencia2_perfil2B)
        vista_sugerencia2_doble.add_widget(vista_sugerencia2_perfil3)
        vista_sugerencia2_doble.add_widget(self.vista_sugerencia2_perfil3B)
        vista_sugerencia2_doble.add_widget(vista_sugerencia2_perfil4)
        vista_sugerencia2_doble.add_widget(self.vista_sugerencia2_perfil4B)
        vista_sugerencia2_doble.add_widget(vista_sugerencia2_perfil5)
        vista_sugerencia2_doble.add_widget(self.vista_sugerencia2_perfil5B)
        vista_sugerencia2_doble.add_widget(vista_sugerencia2_perfil6)
        vista_sugerencia2_doble.add_widget(self.vista_sugerencia2_perfil6B)
        self.panel_AdmSugerencias.add_widget(vista_sugerencia2)
        self.panel_AdmSugerencias.add_widget(vista_sugerencia2_doble)
        self.panel_AdmSugerencias.add_widget(vista_sugerencia3)
        
       # ADMINISTRADOR DE CONTACTO SELECCIONADO
        
        self.panel_AdmContactos = GridLayout(cols = 1 , size_hint = (1, None))
        self.panel_AdmContactos_root = ScrollView(size_hint=(1, 1), size=(Window.width, Window.height))
        self.panel_AdmContactos.bind(minimum_height=self.panel_AdmContactos.setter('height'))

        self.panel_AdmContactos_root.add_widget(self.panel_AdmContactos)
            
        vista_contacto1 = GridLayout(cols = 1 , size_hint = (1,None) , spacing = 0, height = 300)
        vista_contacto3 = GridLayout(cols = 1 , size_hint = (1,None) , spacing = 0, height = 200)
        vista_contacto1_doble = GridLayout ( cols = 2 , size_hint = (1,None) ,height = 410, spacing = 0)
        
        btn6_H = Image(source=self.images + "asd.png", size_hint = (1, None), height = 25, allow_stretch = True, keep_ratio = False) 
        
        
        vista_contacto1_imagen = Button(background_normal = self.images + "PP.png" , background_color = (1,1,1,1))
        
        vista_contacto1_perfil = Button(text ="Contacto" , markup = True, background_normal = self.images + "color_rojo.png" , background_color = (1,1,1,1), size_hint_y = None , height = 50 , font_size = 24)
        vista_contacto1_perfilB = Button(markup = True, background_normal = self.images + "color_rojo.png" , background_color = (1,1,1,1), size_hint_y = None , height = 50)
        
        vista_contacto1_perfil1 = Button(text ="[color=#404040]ID:" , markup = True, background_normal = self.images + "blanco.png" , background_color = (1,1,1,1), size_hint_y = None , height = 50)
        self.vista_contacto1_perfil1B = Button(text ="[color=#404040]Contacto.Nombre" , markup = True, background_normal = self.images + "blanco.png" , background_color = (1,1,1,1), size_hint_y = None , height = 50)
        vista_contacto1_perfil2 = Button(text ="[color=#404040]Nombre:" , markup = True, background_normal = self.images + "blanco.png" , background_color = (1,1,1,1), size_hint_y = None , height = 50)
        self.vista_contacto1_perfil2B = Button(text ="[color=#404040]Contacto.Categoria" ,markup = True, background_normal = self.images + "blanco.png" , background_color = (1,1,1,1), size_hint_y = None , height = 50)
        vista_contacto1_perfil3 = Button(text ="[color=#404040]Teléfono:" , markup = True, background_normal = self.images + "blanco.png" , background_color = (1,1,1,1), size_hint_y = None , height = 50)
        self.vista_contacto1_perfil3B = Button(text ="[color=#404040]Contacto.Creacion" ,markup = True,background_normal = self.images + "blanco.png" , background_color = (1,1,1,1), size_hint_y = None , height = 50)
        vista_contacto1_perfil4 = Button(text ="[color=#404040]Direccion:" , markup = True, background_normal = self.images + "blanco.png" , background_color = (1,1,1,1), size_hint_y = None , height = 50)
        self.vista_contacto1_perfil4B = Button(text ="[color=#404040]Contacto.Ultima Session" , markup = True ,background_normal = self.images + "blanco.png" , background_color = (1,1,1,1), size_hint_y = None , height = 50)
        vista_contacto1_perfil5 = Button(text ="[color=#404040]Estado:" , markup = True, background_normal = self.images + "blanco.png" , background_color = (1,1,1,1), size_hint_y = None , height = 50)
        self.vista_contacto1_perfil5B = Button(text ="[color=#404040]Contacto.ID" , markup = True, background_normal = self.images + "blanco.png" , background_color = (1,1,1,1), size_hint_y = None , height = 50)
        vista_contacto1_perfil6 = Button(text ="[color=#404040]Categoria" , markup = True, background_normal = self.images + "blanco.png" , background_color = (1,1,1,1), size_hint_y = None , height = 50)
        self.vista_contacto1_perfil6B = Button(text ="[color=#404040]Contacto.Privilegios" , markup = True, background_normal = self.images + "blanco.png" , background_color = (1,1,1,1), size_hint_y = None , height = 50)
        vista_contacto1_perfil7 = Button(text ="" , markup = True, background_normal = self.images + "blanco.png" , background_color = (1,1,1,1), size_hint_y = None , height = 50)
        self.vista_contacto1_perfil7B = Button(text ="asdasd" , markup = True, background_normal = self.images + "blanco.png" , background_color = (1,1,1,1), size_hint_y = None , height = 50)
        
        vista_contacto3_Button1 = Button(text= "[color=#404040]Cambiar Estado",  markup = True, background_normal = self.images + "blanco2C.png" , background_color = (1,1,1,1),font_size = 16)
        vista_contacto3_Button2 = Button(text= "[color=#404040]Eliminar", markup = True, background_normal = self.images + "blanco2.png" , background_color = (1,1,1,1),font_size = 16)
        vista_contacto3_Button6 = Button(text= "[color=#404040]Anidar Usuario", markup = True, background_normal = self.images + "blanco2.png" , background_color = (1,1,1,1),font_size = 16)
        vista_contacto3_Button6.bind(on_press = self.ANIDARPOPUP)
        #vista_contacto3_Button6.bind(on_press = pass)
        vista_contacto3_Button5 = Button(text= "[color=#404040]Cambiar Horario", markup = True, background_normal = self.images + "blanco2.png" , background_color = (1,1,1,1),font_size = 16)
        vista_contacto3_Button5.bind(on_press = self.CAMBIARHORARIOPOPUP)
        vista_contacto3_Button3 = Button(text= "Guardar", markup = True, background_normal = self.images + "color_rojo.png" , background_color = (1,1,1,1),font_size = 16)
        vista_contacto3_Button4 = Button(text= "Volver", markup = True, background_normal = self.images + "color_rojo.png" , background_color = (1,1,1,1), font_size = 16)
        vista_contacto1.add_widget(btn6_H)
        vista_contacto1.add_widget(vista_contacto1_imagen)
        vista_contacto3.add_widget(vista_contacto3_Button1)
        vista_contacto3.add_widget(vista_contacto3_Button5)
        vista_contacto3.add_widget(vista_contacto3_Button6)
        vista_contacto3.add_widget(vista_contacto3_Button2)
        vista_contacto3_Button1.bind(on_press = self.CAMBIARESTADO)
        vista_contacto3_Button2.bind(on_press = self.ADMSUGERENCIAS_ELIMINAR)
        #vista_contacto3.add_widget(vista_contacto3_Button4)
        vista_contacto1_doble.add_widget(vista_contacto1_perfil)
        vista_contacto1_doble.add_widget(vista_contacto1_perfilB)
        vista_contacto1_doble.add_widget(vista_contacto1_perfil7)
        vista_contacto1_doble.add_widget(self.vista_contacto1_perfil7B)
        vista_contacto1_doble.add_widget(vista_contacto1_perfil1)
        vista_contacto1_doble.add_widget(self.vista_contacto1_perfil1B)
        vista_contacto1_doble.add_widget(vista_contacto1_perfil2)
        vista_contacto1_doble.add_widget(self.vista_contacto1_perfil2B)
        vista_contacto1_doble.add_widget(vista_contacto1_perfil3)
        vista_contacto1_doble.add_widget(self.vista_contacto1_perfil3B)
        vista_contacto1_doble.add_widget(vista_contacto1_perfil4)
        vista_contacto1_doble.add_widget(self.vista_contacto1_perfil4B)
        vista_contacto1_doble.add_widget(vista_contacto1_perfil5)
        vista_contacto1_doble.add_widget(self.vista_contacto1_perfil5B)
        vista_contacto1_doble.add_widget(vista_contacto1_perfil6)
        vista_contacto1_doble.add_widget(self.vista_contacto1_perfil6B)
        self.panel_AdmContactos.add_widget(vista_contacto1)
        self.panel_AdmContactos.add_widget(vista_contacto1_doble)
        self.panel_AdmContactos.add_widget(vista_contacto3)
        
       # ADMINISTRADOR DE PEDIDO SELECCIONADO
        
        self.panel_AdmPedidos = GridLayout(cols = 1 , size_hint = (1, None))
        self.panel_AdmPedidos_root = ScrollView(size_hint=(1, 1), size=(Window.width, Window.height))
        self.panel_AdmPedidos.bind(minimum_height=self.panel_AdmPedidos.setter('height'))

        self.panel_AdmPedidos_root.add_widget(self.panel_AdmPedidos)
            
        vista_pedido1 = GridLayout(cols = 1 , size_hint = (1,None) , spacing = 0, height = 300)
        vista_pedido3 = GridLayout(cols = 1 , size_hint = (1,None) , spacing = 0, height = 100)
        vista_pedido1_doble = GridLayout ( cols = 2 , size_hint = (1,None) ,height = 410, spacing = 0)
        
        btn6_H = Image(source=self.images + "asd.png", size_hint = (1, None), height = 25, allow_stretch = True, keep_ratio = False) 
        
        
        vista_pedido1_imagen = Button(background_normal = self.images + "PP.png" , background_color = (1,1,1,1))
        
        vista_pedido1_perfil = Button(text ="Pedido" , markup = True, background_normal = self.images + "color_rojo.png" , background_color = (1,1,1,1), size_hint_y = None , height = 50 , font_size = 24)
        vista_pedido1_perfilB = Button(markup = True, background_normal = self.images + "color_rojo.png" , background_color = (1,1,1,1), size_hint_y = None , height = 50)
        
        vista_pedido1_perfil1 = Button(text ="[color=#404040]ID:" , markup = True, background_normal = self.images + "blanco.png" , background_color = (1,1,1,1), size_hint_y = None , height = 50)
        self.vista_pedido1_perfil1B = Button(text ="[color=#404040]Contacto.Nombre" , markup = True, background_normal = self.images + "blanco.png" , background_color = (1,1,1,1), size_hint_y = None , height = 50)
        vista_pedido1_perfil2 = Button(text ="[color=#404040]Pedido por:" , markup = True, background_normal = self.images + "blanco.png" , background_color = (1,1,1,1), size_hint_y = None , height = 50)
        self.vista_pedido1_perfil2B = Button(text ="[color=#404040]Contacto.Categoria" ,markup = True, background_normal = self.images + "blanco.png" , background_color = (1,1,1,1), size_hint_y = None , height = 50)
        vista_pedido1_perfil3 = Button(text ="[color=#404040]Detalles:" , markup = True, background_normal = self.images + "blanco.png" , background_color = (1,1,1,1), size_hint_y = None , height = 50)
        self.vista_pedido1_perfil3B = Button(text ="[color=#404040]Contacto.Creacion" ,markup = True,background_normal = self.images + "blanco.png" , background_color = (1,1,1,1), size_hint_y = None , height = 50)
        vista_pedido1_perfil4 = Button(text ="[color=#404040]Costo Total:" , markup = True, background_normal = self.images + "blanco.png" , background_color = (1,1,1,1), size_hint_y = None , height = 50)
        self.vista_pedido1_perfil4B = Button(text ="[color=#404040]Contacto.Ultima Session" , markup = True ,background_normal = self.images + "blanco.png" , background_color = (1,1,1,1), size_hint_y = None , height = 50)
        vista_pedido1_perfil5 = Button(text ="[color=#404040]Estado:" , markup = True, background_normal = self.images + "blanco.png" , background_color = (1,1,1,1), size_hint_y = None , height = 50)
        self.vista_pedido1_perfil5B = Button(text ="[color=#404040]Contacto.ID" , markup = True, background_normal = self.images + "blanco.png" , background_color = (1,1,1,1), size_hint_y = None , height = 50)
        vista_pedido1_perfil6 = Button(text ="[color=#404040]Categoria" , markup = True, background_normal = self.images + "blanco.png" , background_color = (1,1,1,1), size_hint_y = None , height = 50)
        self.vista_pedido1_perfil6B = Button(text ="[color=#404040]Contacto.Privilegios" , markup = True, background_normal = self.images + "blanco.png" , background_color = (1,1,1,1), size_hint_y = None , height = 50)
        vista_pedido1_perfil7 = Button(text ="" , markup = True, background_normal = self.images + "blanco.png" , background_color = (1,1,1,1), size_hint_y = None , height = 50)
        self.vista_pedido1_perfil7B = Button(text ="asdasd" , markup = True, background_normal = self.images + "blanco.png" , background_color = (1,1,1,1), size_hint_y = None , height = 50)
        
        vista_pedido3_Button1 = Button(text= "[color=#404040]Cambiar Estado",  markup = True, background_normal = self.images + "blanco2C.png" , background_color = (1,1,1,1),font_size = 16)
        vista_pedido3_Button2 = Button(text= "[color=#404040]Cancelar", markup = True, background_normal = self.images + "blanco2.png" , background_color = (1,1,1,1),font_size = 16)
        vista_pedido3_Button3 = Button(text= "Guardar", markup = True, background_normal = self.images + "color_rojo.png" , background_color = (1,1,1,1),font_size = 16)
        vista_pedido3_Button4 = Button(text= "Volver", markup = True, background_normal = self.images + "color_rojo.png" , background_color = (1,1,1,1), font_size = 16)
        vista_pedido1.add_widget(btn6_H)
        vista_pedido1.add_widget(vista_pedido1_imagen)
        #vista_pedido3.add_widget(vista_pedido3_Button1)
        vista_pedido3.add_widget(vista_pedido3_Button2)
        vista_pedido3_Button1.bind(on_press = self.CAMBIARESTADO)
        #vista_pedido3_Button2.bind(on_press = self.ADMSUGERENCIAS_ELIMINAR)
        #vista_pedido3.add_widget(vista_pedido3_Button4)
        vista_pedido1_doble.add_widget(vista_pedido1_perfil)
        vista_pedido1_doble.add_widget(vista_pedido1_perfilB)
        vista_pedido1_doble.add_widget(vista_pedido1_perfil7)
        vista_pedido1_doble.add_widget(self.vista_pedido1_perfil7B)
        vista_pedido1_doble.add_widget(vista_pedido1_perfil1)
        vista_pedido1_doble.add_widget(self.vista_pedido1_perfil1B)
        vista_pedido1_doble.add_widget(vista_pedido1_perfil2)
        vista_pedido1_doble.add_widget(self.vista_pedido1_perfil2B)
        vista_pedido1_doble.add_widget(vista_pedido1_perfil3)
        vista_pedido1_doble.add_widget(self.vista_pedido1_perfil3B)
        vista_pedido1_doble.add_widget(vista_pedido1_perfil4)
        vista_pedido1_doble.add_widget(self.vista_pedido1_perfil4B)
        vista_pedido1_doble.add_widget(vista_pedido1_perfil5)
        vista_pedido1_doble.add_widget(self.vista_pedido1_perfil5B)
        vista_pedido1_doble.add_widget(vista_pedido1_perfil6)
        vista_pedido1_doble.add_widget(self.vista_pedido1_perfil6B)
        self.panel_AdmPedidos.add_widget(vista_pedido1)
        self.panel_AdmPedidos.add_widget(vista_pedido1_doble)
        self.panel_AdmPedidos.add_widget(vista_pedido3)
        
        # ADMINISTRADOR DE TIENDA
        
        self.panel_AdmTienda = GridLayout(cols = 1 , size_hint = (1, None))
        self.panel_AdmTienda_root = ScrollView(size_hint=(1, 1), size=(Window.width, Window.height))
        self.panel_AdmTienda.bind(minimum_height=self.panel_AdmTienda.setter('height'))

        self.panel_AdmTienda_root.add_widget(self.panel_AdmTienda)
            
        vista_Tienda2 = GridLayout(cols = 1 , size_hint = (1,None) , spacing = 0, height = 300)
        vista_Tienda3 = GridLayout(cols = 1 , size_hint = (1,None) , spacing = 0, height = 100)
        vista_Tienda2_doble = GridLayout ( cols = 2 , size_hint = (1,None) ,height = 370, spacing = 0)
        self.cajas_dobles2 = GridLayout(cols=1, spacing = 0, size_hint_y = None , height= 210 , size_hint_x =1 )
        
        vista_Tienda2_imagen = Image(source = self.images + "404.png" , background_color = (1,1,1,1))
        
        vista_Tienda2_perfil = Button(text ="[color=#404040]Contacto" , markup = True, background_normal = self.images + "blanco7.png" , background_color = (1,1,1,1), size_hint_y = None , height = 50 , font_size = 24)
        vista_Tienda2_perfilB = Button(markup = True, background_normal = self.images + "blanco7C.png" , background_color = (1,1,1,1), size_hint_y = None , height = 50)
        
        vista_Tienda2_perfil1 = Button(text ="[color=#404040][b]Id" , markup = True, background_normal = self.images + "blanco.png" , background_color = (1,1,1,1), size_hint_y = None , height = 50)
        self.vista_Tienda2_perfil1B = Button(text ="[color=#404040]Tienda.Nombre" , markup = True, background_normal = self.images + "blanco.png" , background_color = (1,1,1,1), size_hint_y = None , height = 50)
        vista_Tienda2_perfil2 = Button(text ="[color=#404040][b]Nombre" , markup = True, background_normal = self.images + "blanco.png" , background_color = (1,1,1,1), size_hint_y = None , height = 50)
        self.vista_Tienda2_perfil2B = Button(text ="[color=#404040]Tienda.Categoria" ,markup = True, background_normal = self.images + "blanco.png" , background_color = (1,1,1,1), size_hint_y = None , height = 50)
        vista_Tienda2_perfil3 = Button(text ="[color=#404040][b]Telefono" , markup = True, background_normal = self.images + "blanco.png" , background_color = (1,1,1,1), size_hint_y = None , height = 50)
        self.vista_Tienda2_perfil3B = Button(text ="[color=#404040]Sugerncia.Creacion" ,markup = True,background_normal = self.images + "blanco.png" , background_color = (1,1,1,1), size_hint_y = None , height = 50)
        vista_Tienda2_perfil4 = Button(text ="[color=#404040][b]Direccion" , markup = True, background_normal = self.images + "blanco.png" , background_color = (1,1,1,1), size_hint_y = None , height = 50)
        self.vista_Tienda2_perfil4B = Button(text ="[color=#404040]Tienda.Ultima Session" , markup = True ,background_normal = self.images + "blanco.png" , background_color = (1,1,1,1), size_hint_y = None , height = 50)
        vista_Tienda2_perfil5 = Button(text ="[color=#404040][b]Estado" , markup = True, background_normal = self.images + "blanco.png" , background_color = (1,1,1,1), size_hint_y = None , height = 50)
        self.vista_Tienda2_perfil5B = Button(text ="[color=#404040]Usuario.ID" , markup = True, background_normal = self.images + "blanco.png" , background_color = (1,1,1,1), size_hint_y = None , height = 50)
        vista_Tienda2_perfil6 = Button(text ="[color=#404040][b]Categoria" , markup = True, background_normal = self.images + "blanco.png" , background_color = (1,1,1,1), size_hint_y = None , height = 50)
        self.vista_Tienda2_perfil6B = Button(text ="[color=#404040]Usuario.Privilegios" , markup = True, background_normal = self.images + "blanco.png" , background_color = (1,1,1,1), size_hint_y = None , height = 50)
        
        vista_Tienda3_Button1 = Button(text= "[color=#404040]Añadir Categoria",  markup = True, background_normal = self.images + "blanco2C.png" , background_color = (1,1,1,1),font_size = 16)
        vista_Tienda3_Button2 = Button(text= "[color=#404040]Desactivar Contacto", markup = True, background_normal = self.images + "blanco.png" , background_color = (1,1,1,1),font_size = 16)
        vista_Tienda3_Button3 = Button(text= "[color=#404040]Boton3", markup = True, background_normal = self.images + "blanco2.png" , background_color = (1,1,1,1),font_size = 16)
        vista_Tienda3_Button4 = Button(text= "[color=#404040]Boton4", markup = True, background_normal = self.images + "blanco2.png" , background_color = (1,1,1,1), font_size = 16)
        
        vista_Tienda2_perfil = Button(text ="[color=#404040]Contacto" , markup = True, background_normal = self.images + "blanco7.png" , background_color = (1,1,1,1), size_hint_y = None , height = 50 , font_size = 24)
        vista_Tienda2_perfilB = Button(markup = True, background_normal = self.images + "blanco7C.png" , background_color = (1,1,1,1), size_hint_y = None , height = 50)
        vista_Tienda2.add_widget(vista_Tienda2_imagen)
        vista_Tienda3.add_widget(vista_Tienda3_Button1)
        vista_Tienda3.add_widget(vista_Tienda3_Button2)
        #vista_Tienda3.add_widget(vista_Tienda3_Button3)
        #vista_Tienda3.add_widget(vista_Tienda3_Button4)
        vista_Tienda2_doble.add_widget(vista_Tienda2_perfil)
        vista_Tienda2_doble.add_widget(vista_Tienda2_perfilB)
        vista_Tienda2_doble.add_widget(vista_Tienda2_perfil1)
        vista_Tienda2_doble.add_widget(self.vista_Tienda2_perfil1B)
        vista_Tienda2_doble.add_widget(vista_Tienda2_perfil2)
        vista_Tienda2_doble.add_widget(self.vista_Tienda2_perfil2B)
        vista_Tienda2_doble.add_widget(vista_Tienda2_perfil3)
        vista_Tienda2_doble.add_widget(self.vista_Tienda2_perfil3B)
        vista_Tienda2_doble.add_widget(vista_Tienda2_perfil4)
        vista_Tienda2_doble.add_widget(self.vista_Tienda2_perfil4B)
        vista_Tienda2_doble.add_widget(vista_Tienda2_perfil5)
        vista_Tienda2_doble.add_widget(self.vista_Tienda2_perfil5B)
        vista_Tienda2_doble.add_widget(vista_Tienda2_perfil6)
        vista_Tienda2_doble.add_widget(self.vista_Tienda2_perfil6B)
        self.panel_AdmTienda.add_widget(vista_Tienda2)
        self.panel_AdmTienda.add_widget(vista_Tienda2_doble)
        self.panel_AdmTienda.add_widget(vista_Tienda3)
        self.panel_AdmTienda.add_widget(self.cajas_dobles2)
        
        
        for i in self.Menutable:
            contador_o = 0
            for x in self.MenuSCtable:
                if i['contacto'] == x['contacto_id']:
                    for g in x['menu']:
                        contador_o += 1
                        if i['id'] == g:
                        
                            
                            caja_C4 = Button(background_down = self.images + "blanco2C.png" ,size_hint = (1,None), height = 50, text = "[color=#ff3333]"+x['sub_categoria'], markup = True, background_color = (1,1,1,1), background_normal = self.images + 'blanco2C.png', font_size = 24 )
                            caja_C5 = Button(background_down = self.images + "blanco2C.png" ,size_hint = (1,None), height = 50, text = "[color=#404040]""", markup = True, background_color = (1,1,1,1), background_normal = self.images + 'blanco2C.png')
                            self.caja_grid = GridLayout(cols = 2 ,spacing = 0, size_hint_y = None, height= 50, size_hint_x = .7)
                            self.caja_grid_IN = GridLayout(cols = 3 ,spacing = 0, size_hint_y = None, height= 50, size_hint_x = .3)
                            self.caja_grid_Button1 = Button(text = "[color=#404040]Add", background_normal = self.images + "blanco2C.png", markup = True)
                            self.caja_grid_Button2 = Button(text = "[color=#404040]Edit", background_normal = self.images + "blanco2C.png", markup = True)
                            self.caja_grid_Button3 = Button(text = "[color=#404040]Del", background_normal = self.images + "blanco2C.png", markup = True)
                            
                            self.caja_grid_IN.add_widget(self.caja_grid_Button1)
                            self.caja_grid_IN.add_widget(self.caja_grid_Button2)
                            self.caja_grid_IN.add_widget(self.caja_grid_Button3)
                            self.caja_grid.add_widget(caja_C4)
                            self.caja_grid.add_widget(self.caja_grid_IN)
                            self.cajas_dobles2.add_widget(self.caja_grid)
                            #self.cajas_dobles2.add_widget(self.caja_grid_IN)
                            iguales11 = 0
                            for z in self.PlatoTable:
                                if z ['sub_categoria'] == x['id']:
                                    iguales11 += 1
                                    
                            for z in self.PlatoTable:
                                if z ['sub_categoria'] == x['id']:
                                    a_F = GridLayout(cols=3, spacing=0, size_hint_y=None, height = 100 , size_hint_x = 1)
                                    
                                    btn6_F = Button(background_down = self.images + "blanco7B.png" ,size_hint_y= None ,height=25, background_normal = self.images + 'blanco7B.png', background_color = (1,1,1,1))                                    
                                    btn6_FB = Button(background_down = self.images + "blanco7B.png" ,size_hint_y= None ,height=25, background_normal = self.images + 'blanco7B.png', background_color = (1,1,1,1))                                    
                                    btn6_FC = Button(background_down = self.images + "blanco7B.png" ,size_hint_y= None ,height=25, background_normal = self.images + 'blanco7B.png', background_color = (1,1,1,1))                                    
                                    btn1_F = Button(background_down = self.images + "blanco.png" ,text='[b][color=#404040]'+ z['plato'], size_hint_y=0.1, height=30, background_normal = self.images + 'blanco.png', background_color = (1,1,1,1), markup = True , font_size = 18,valign = 'top')                                                                                                      
                                    btn5_F = CheckBox()
                                    btn2_F = Button(background_down = self.images + "blanco.png" ,text='[color=#404040][b]'+ z['precio'] + ' RD$' , size_hint_y=0.1, height=30, background_normal = self.images + 'blanco.png',background_color = (1,1,1,1), markup   = True, font_size = 18)
                                    btn4_F = Button(background_down = self.images + "roro2.png" ,size_hint_y=0.025 , background_normal = self.images + 'roro2.png', background_color = (1,1,1,1))
                                    btn4_FB = Button(background_down = self.images + "roro2.png" ,size_hint_y=0.025 , background_normal = self.images + 'roro2.png', background_color = (1,1,1,1))
                                    btn4_FC = Button(background_down = self.images + "roro2.png" ,size_hint_y=0.025 , background_normal = self.images + 'roro2.png', background_color = (1,1,1,1))
                                    
                                    a_F.add_widget(btn6_F)                                
                                    a_F.add_widget(btn6_FB)                                
                                    a_F.add_widget(btn6_FC)                                
                                    a_F.add_widget(btn5_F)                           
                                    a_F.add_widget(btn1_F)                           
                                    a_F.add_widget(btn2_F)
                                    a_F.add_widget(btn4_F)
                                    a_F.add_widget(btn4_FB)
                                    a_F.add_widget(btn4_FC)
                        
                     
                                    self.cajas_dobles2.add_widget(a_F)
                                    self.cajas_dobles2.height += 100
                                    print self.cajas_dobles2.height
                                    
                            if(iguales11%2==0):
                                pass
                            elif self.UserID == "09090909":
                                
                                print(str(a)+" es impar")
                                a_G = GridLayout(cols=1, spacing=0, size_hint_y=None, height = 100 , size_hint_x = 1)
                                btn3_G = Button(background_down = self.images + "roro.png" ,size_hint_y=0.025 , background_normal = self.images + 'roro.png', background_color = (1,1,1,1))
                                btn4_G = Button(background_down = self.images + "roro2.png" ,size_hint_y=0.025 , background_normal = self.images + 'roro2.png', background_color = (1,1,1,1))
                                btn6_G = Button(background_down = self.images + "asd.png" ,size_hint_y= None ,height=25, background_normal = self.images + 'asd.png', background_color = (1,1,1,1))
                                btn0_G = Button(background_down = self.images + "404.png" ,text='', size_hint_y=0.400, height=100, background_normal = self.images + '404.png')
                                btn1_G = Button(background_down = self.images + "blanco.png" ,text='[b][color=#404040]'+ "Espacio publicitario", size_hint_y=0.1, height=30, background_normal = self.images + 'blanco.png', background_color = (1,1,1,1), markup = True , font_size = 18,valign = 'top')
                                btn5_G = Button(background_down = self.images + "blanco.png" ,text='', size_hint_y=0.050, height=30, background_normal = self.images + 'blanco.png', background_color = (1,1,1,1), markup = True , font_size = '15sp')
                                btn_G = Button(background_down = self.images + "color_rojo.png" ,text="[color=#ed1c24]"+str(1)+'[/color]'+'+' , size_hint_y=0.2, size_hint_x = 0.2, height=70, background_normal = self.images + 'color_rojo.png', markup = True)
                                btn2_G = Button(background_down = self.images + "blanco.png" ,text='' , size_hint_y=0.1, height=30, background_normal = self.images + 'blanco.png',background_color = (1,1,1,1), markup   = True, font_size = 18)
                                name_G = btn_G.text
                                btn_G.bind(on_press= lambda name_G=name_G: self.INSERTAR_in_PEDIDO(name_G.text[15:-9],self.guardado01))

                                a_G.add_widget(btn6_G)
                                #a_G.add_widget(btn0_G)
                                a_G.add_widget(btn1_G)
                                #a_G.add_widget(btn3_G)
                                a_G.add_widget(btn2_G)
                                a_G.add_widget(btn4_G)
                                #a_G.add_widget(btn5_G)
                                #a_G.add_widget(btn_G)
                                self.cajas_dobles2.add_widget(a_G)
                                self.cajas_dobles2.height += 100
                            
        
        
        
        
        
        # ____________________________________________________________________________________________________
        # MENU ADMINISTRADOR

        
        self.menu_Administrador = GridLayout(cols = 1 , size_hint = (1, None))
        self.menu_Administrador_root = ScrollView(size_hint=(1, 1), size=(Window.width, Window.height))
        self.menu_Administrador.bind(minimum_height=self.menu_Administrador.setter('height'))

        self.menu_Administrador_root.add_widget(self.menu_Administrador)
        
        
        
        botones = ["Administrar Usuarios", "Administrar Contactos", "Administrar Categorias","Administrar Sugerencias","Administrar Menus","Administrar Pedidos","Actualizar Base de Datos"]
        for i in botones:
            menu_Administradorbutton = Button(text="[color=#404040]"+ i,  markup = True, background_normal = self.images + "blanco2.png" , background_color = (1,1,1,1),font_size = 18, size_hint = (1,None), height = 120)
            self.menu_Administrador.add_widget(menu_Administradorbutton)
            if i == botones[0]:
                menu_Administradorbutton.bind(on_press = self.ADMINISTRAR_USUARIOS)
            if i == botones[1]:
                menu_Administradorbutton.bind(on_press = self.CONTACTOS)
            if i == botones[2]:
                menu_Administradorbutton.bind(on_press = self.CATEGORIAS)
            if i == botones[3]:
                menu_Administradorbutton.bind(on_press = self.SUGERENCIAS)
            if i == botones[4]:
                menu_Administradorbutton.bind(on_press = self.MENUS)
            if i == botones[5]:
                menu_Administradorbutton.bind(on_press = self.ADMINISTRAR_INVITADOS)
            if i == botones[6]:
                pass

        # ____________________________________________________________________________________________________
        
        self.Perfil_Direcciones = GridLayout(cols = 1 , size_hint = (1, None))
        self.Perfil_Direcciones_root = ScrollView(size_hint=(1, 1), size=(Window.width, Window.height))
        self.Perfil_Direcciones.bind(minimum_height=self.Perfil_Direcciones.setter('height'))
        campos = ["Distrito", "Sector", "Calle", "Casa/Apt","Edificio","Numero#"]
        self.Perfil_Direcciones_root.add_widget(self.Perfil_Direcciones)
        a = 0
        a = a + 1
        if a == 1:
            PanelD2 =  GridLayout (cols = 2 , size_hint = (1,None) ,height = 120, spacing = 0) 
            PBoriginal2 = Button(text= "[color=#404040]",  markup = True, background_normal = self.images + "blanco.png" , background_color = (1,1,1,1),font_size = "13sp", size_hint= (1, None), height = 25)
            PBoriginalB2 = Button(text= "[color=#404040]",  markup = True, background_normal = self.images + "blanco.png" , background_color = (1,1,1,1),font_size = "13sp", size_hint= (1, None), height = 25)
            PToriginal = Button(text= "Direccion de entrega",  markup = True, background_normal = self.images + "color_rojo.png" , background_color = (1,1,1,1),font_size = 24, size_hint= (1, None), height = 70)
            PToriginalB = Button(text= "[color=#404040]"+"",  markup = True, background_normal = self.images + "blanco2.png" , background_color = (1,1,1,1),font_size = 24, size_hint= (1, None), height = 70)
            btn6_E = Button(background_down = self.images + "blanco.png" ,size_hint_y= None ,height=25, background_normal = self.images + 'blanco.png', background_color = (1,1,1,1))
            btn6_EB = Button(background_down = self.images + "blanco.png" ,size_hint_y= None ,height=25, background_normal = self.images + 'blanco.png', background_color = (1,1,1,1))
            PanelD2.add_widget(btn6_E)
            PanelD2.add_widget(btn6_EB)
            PanelD2.add_widget(PToriginal)
            PanelD2.add_widget(PToriginalB)
            PanelD2.add_widget(PBoriginal2)
            PanelD2.add_widget(PBoriginalB2)
            self.Perfil_Direcciones.add_widget(PanelD2)
            
        PanelD =  GridLayout (cols = 2 , size_hint = (1,None) ,height = 345, spacing = 0) 
        
        PBoriginal1 = Button(text= "[color=#404040]"+"[b]"+campos[0],  markup = True, background_normal = self.images + "blanco.png" , background_color = (1,1,1,1),font_size = "16sp", size_hint= (1, None), height = 45)
        self.PBoriginal1B = Button(text= "[color=#404040]"+"self.UserDIR[0]",  markup = True, background_normal = self.images + "blanco.png" , background_color = (1,1,1,1),font_size = "16sp", size_hint= (1, None), height = 45)
        
        PBoriginal2 = Button(text= "[color=#404040]"+"[b]"+campos[1],  markup = True, background_normal = self.images + "blanco.png" , background_color = (1,1,1,1),font_size = "16sp", size_hint= (1, None), height = 45)
        self.PBoriginal2B = Button(text= "[color=#404040]"+"self.UserDIR[1]",  markup = True, background_normal = self.images + "blanco.png" , background_color = (1,1,1,1),font_size = "16sp", size_hint= (1, None), height = 45)
        
        PBoriginal3 = Button(text= "[color=#404040]"+"[b]"+campos[2],  markup = True, background_normal = self.images + "blanco.png" , background_color = (1,1,1,1),font_size = "16sp", size_hint= (1, None), height = 45)
        self.PBoriginal3B = Button(text= "[color=#404040]"+"self.UserDIR[2]",  markup = True, background_normal = self.images + "blanco.png" , background_color = (1,1,1,1),font_size = "16sp", size_hint= (1, None), height = 45)
                
        PBoriginal4 = Button(text= "[color=#404040]"+"[b]"+campos[3],  markup = True, background_normal = self.images + "blanco.png" , background_color = (1,1,1,1),font_size = "16sp", size_hint= (1, None), height = 45)
        self.PBoriginal4B = Button(text= "[color=#404040]"+"self.UserDIR[3]",  markup = True, background_normal = self.images + "blanco.png" , background_color = (1,1,1,1),font_size = "16sp", size_hint= (1, None), height = 45)
        
        PBoriginal5 = Button(text= "[color=#404040]"+"[b]"+campos[4],  markup = True, background_normal = self.images + "blanco.png" , background_color = (1,1,1,1),font_size = "16sp", size_hint= (1, None), height = 45)
        self.PBoriginal5B = Button(text= "[color=#404040]"+"self.UserDIR[4]",  markup = True, background_normal = self.images + "blanco.png" , background_color = (1,1,1,1),font_size = "16sp", size_hint= (1, None), height = 45)
        
        PBoriginal6 = Button(text= "[color=#404040]"+"[b]"+campos[5],  markup = True, background_normal = self.images + "blanco.png" , background_color = (1,1,1,1),font_size = "16sp", size_hint= (1, None), height = 45)
        self.PBoriginal6B = Button(text= "[color=#404040]"+"self.UserDIR[5]",  markup = True, background_normal = self.images + "blanco.png" , background_color = (1,1,1,1),font_size = "16sp", size_hint= (1, None), height = 45)
        
        
        caja_S12B = ToggleButton(background_down = self.images + "blanco2C.png" ,size_hint = (1,None), height = 50, text = "[color=#404040]", markup = True, background_color = (1,1,1,1), background_normal = self.images + 'blanco2C.png')
        caja_S12BB = ToggleButton(background_down = self.images + "blanco2C.png" ,size_hint = (1,None), height = 50, text = "[color=#404040]Modificar", markup = True, background_color = (1,1,1,1), background_normal = self.images + 'blanco2C.png')
        
        PBoriginal7 = Button(text= "[color=#404040]",  markup = True, background_normal = self.images + "blanco.png" , background_color = (1,1,1,1),font_size = "13sp", size_hint= (1, None), height = 25)
        PBoriginalB7 = Button(text= "[color=#404040]",  markup = True, background_normal = self.images + "blanco.png" , background_color = (1,1,1,1),font_size = "13sp", size_hint= (1, None), height = 25)
        
        def cambias2(self):
            if caja_S12BB.text == ("[color=#404040]Seleccionar"):
                caja_S12BB.text = "[b][color=#ff1a1a]Seleccionado"
            else:
                caja_S12BB.text = "[color=#404040]Seleccionar"
                
        #caja_S12BB.bind(on_press = cambias2)
        
        PanelD.add_widget(PBoriginal1)
        PanelD.add_widget(self.PBoriginal1B)
        PanelD.add_widget(PBoriginal2)
        PanelD.add_widget(self.PBoriginal2B)
        PanelD.add_widget(PBoriginal3)
        PanelD.add_widget(self.PBoriginal3B)
        PanelD.add_widget(PBoriginal4)
        PanelD.add_widget(self.PBoriginal4B)
        PanelD.add_widget(PBoriginal5)
        PanelD.add_widget(self.PBoriginal5B)
        PanelD.add_widget(PBoriginal6)
        PanelD.add_widget(self.PBoriginal6B)
        PanelD.add_widget(PBoriginal7)
        PanelD.add_widget(PBoriginalB7)
        
        PanelD.add_widget(caja_S12BB)
        PanelD.add_widget(caja_S12B)
        self.Perfil_Direcciones.add_widget(PanelD)

        
        PanelD3 =  GridLayout (cols = 2 , size_hint = (1,None) ,height = 120, spacing = 0) 
        PBoriginal22 = Button(text= "[color=#404040]",  markup = True, background_normal = self.images + "blanco.png" , background_color = (1,1,1,1),font_size = "13sp", size_hint= (1, None), height = 25)
        PBoriginalB22 = Button(text= "[color=#404040]",  markup = True, background_normal = self.images + "blanco.png" , background_color = (1,1,1,1),font_size = "13sp", size_hint= (1, None), height = 25)
        PToriginal2 = Button(text= "Forma de Entrega",  markup = True, background_normal = self.images + "color_rojo.png" , background_color = (1,1,1,1),font_size = 24, size_hint= (1, None), height = 70)
        PToriginalB2 = Button(text= "[color=#404040]"+"",  markup = True, background_normal = self.images + "blanco2.png" , background_color = (1,1,1,1),font_size = 24, size_hint= (1, None), height = 70)
        btn6_E2 = Button(background_down = self.images + "blanco.png" ,size_hint_y= None ,height=25, background_normal = self.images + 'blanco.png', background_color = (1,1,1,1))
        btn6_EB2 = Button(background_down = self.images + "blanco.png" ,size_hint_y= None ,height=25, background_normal = self.images + 'blanco.png', background_color = (1,1,1,1))
        
        PanelD3.add_widget(btn6_E2)
        PanelD3.add_widget(btn6_EB2)
        PanelD3.add_widget(PToriginal2)
        PanelD3.add_widget(PToriginalB2)
        PanelD3.add_widget(PBoriginal22)
        PanelD3.add_widget(PBoriginalB22)
        self.Perfil_Direcciones.add_widget(PanelD3)
        
        PanelD4 =  GridLayout (cols = 3 , size_hint = (1,None) ,height = 340, spacing = 0) 
        predimage = Image(source=self.images + "Entypo_2713(6)_64.png", size_hint = (.20, None), height = 100, allow_stretch = False, keep_ratio = True)
        PBoriginal13 = Button(text= "[color=#404040]",  markup = True, background_normal = self.images + "blanco2CB.png" , background_color = (1,1,1,1),font_size = "16sp", size_hint= (.20, None), height = 70)
        self.PBoriginal1B3 = Button(text= "[color=#404040]Recibo en Caja",  markup = True, background_normal = self.images + "blanco2C.png" , background_color = (1,1,1,1),font_size = "16sp", size_hint= (1, None), height = 70)
        PBoriginal23 = Button(text= "[color=#404040]"+"[b]"+"",  markup = True, background_normal = self.images + "blanco2C2.png" , background_color = (1,1,1,1),font_size = "16sp", size_hint= (.20, None), height = 70)
        
        
        textoo = "\nRetirar su pedido directamente en la tienda."
        self.PBoriginal2B3B2 = Image(source="", size_hint = (.20, None), height = 100, allow_stretch = False, keep_ratio = True)
        a_D_Input1 = TextInput(size_hint_x = 0.8,disabled = True,text = textoo ,size_hint_y = None,height = 100, Readonly = True , Line_Spacing = 3, background_normal = self.images + "blanco2C3.png" , background_color = (1,1,1,1), font_size = '16sp', background_disabled_normal = self.images + "blanco.png", disabled_foreground_color = (0,0,0,1))
        self.PBoriginal2B3B3 = Button(text= "",  markup = True, background_normal = self.images + "blanco2C3.png" , background_color = (1,1,1,1),font_size = "16sp", size_hint= (.20, None), height = 100)

        
        self.PBoriginal2B3 =  Button(text= "[color=#404040]",  markup = True, background_normal = self.images + "blanco2CB.png" , background_color = (1,1,1,1),font_size = "16sp", size_hint= (.20, None), height = 70)
        PBoriginal23B = Button(text= "[color=#404040]Recibo Domicilio",  markup = True, background_normal = self.images + "blanco2C.png" , background_color = (1,1,1,1),font_size = "16sp", size_hint= (1, None), height = 70)
        self.PBoriginal2B3B = Button(text= "",  markup = True, background_normal = self.images + "blanco2C2.png" , background_color = (1,1,1,1),font_size = "16sp", size_hint= (.20, None), height = 70)
        
        
        textoo1 = "\nPagar a su domicilio en efectivo, una vez su pedido le sea entregado."
        self.PBoriginal2B3B4 = Image(source="", size_hint = (.20, None), height = 100, allow_stretch = False, keep_ratio = True)
        a_D_Input2 = TextInput(size_hint_x = 0.8,disabled = True,text = textoo1 ,size_hint_y = None,height = 100 , Readonly = True , Line_Spacing = 3, background_normal = self.images + "blanco2C3.png" , background_color = (1,1,1,1), font_size = '16sp', background_disabled_normal = self.images + "blanco2.png", disabled_foreground_color = (0,0,0,1))
        self.PBoriginal2B3B5 = Button(text= "",  markup = True, background_normal = self.images + "blanco22.png" , background_color = (1,1,1,1),font_size = "16sp", size_hint= (.20, None), height = 100)
        
        
        
        
        def definir1(button):
            if self.PBoriginal2B3B4.source == self.images + "Entypo_2713(6)_64.png":
                self.PBoriginal2B3B4.source = self.images + "blanco.png"
            else:
                self.PBoriginal2B3B4.source = self.images + "Entypo_2713(6)_64.png"
                self.PBoriginal2B3B2.source = self.images + "blanco.png"
                
        def definir2(button):
            if self.PBoriginal2B3B2.source == self.images + "Entypo_2713(6)_64.png":
                self.PBoriginal2B3B2.source = self.images + "blanco.png"
            else:
                self.PBoriginal2B3B2.source = self.images + "Entypo_2713(6)_64.png"
                self.PBoriginal2B3B4.source = self.images + "blanco.png"
            
        PBoriginal13.bind(on_press = definir2)
        self.PBoriginal2B3.bind(on_press = definir1)
        
        PanelD4.add_widget(PBoriginal13)
        PanelD4.add_widget(PBoriginal23)
        PanelD4.add_widget(self.PBoriginal1B3)

        PanelD4.add_widget(self.PBoriginal2B3B2)
        PanelD4.add_widget(self.PBoriginal2B3B3)
        PanelD4.add_widget(a_D_Input1)
        
        PanelD4.add_widget(self.PBoriginal2B3)
        PanelD4.add_widget(self.PBoriginal2B3B)
        PanelD4.add_widget(PBoriginal23B)
        
        PanelD4.add_widget(self.PBoriginal2B3B4)
        PanelD4.add_widget(self.PBoriginal2B3B5)
        PanelD4.add_widget(a_D_Input2)
        
        self.Perfil_Direcciones.add_widget(PanelD4)
        
        PanelD6 =  GridLayout (cols = 2 , size_hint = (1,None) ,height = 120, spacing = 0) 
        PBoriginal23 = Button(text= "[color=#404040]",  markup = True, background_normal = self.images + "blanco.png" , background_color = (1,1,1,1),font_size = "13sp", size_hint= (1, None), height = 25)
        PBoriginalB23 = Button(text= "[color=#404040]",  markup = True, background_normal = self.images + "blanco.png" , background_color = (1,1,1,1),font_size = "13sp", size_hint= (1, None), height = 25)
        PToriginal3 = Button(text= "Modo de Pago",  markup = True, background_normal = self.images + "color_rojo.png" , background_color = (1,1,1,1),font_size = 24, size_hint= (1, None), height = 70)
        PToriginalB3 = Button(text= "[color=#404040]"+"",  markup = True, background_normal = self.images + "blanco2.png" , background_color = (1,1,1,1),font_size = 24, size_hint= (1, None), height = 70)
        btn6_E3 = Button(background_down = self.images + "blanco.png" ,size_hint_y= None ,height=25, background_normal = self.images + 'blanco.png', background_color = (1,1,1,1))
        btn6_EB3 = Button(background_down = self.images + "blanco.png" ,size_hint_y= None ,height=25, background_normal = self.images + 'blanco.png', background_color = (1,1,1,1))
        
		

		
		
        PanelD6.add_widget(btn6_E3)
        PanelD6.add_widget(btn6_EB3)
        PanelD6.add_widget(PToriginal3)
        PanelD6.add_widget(PToriginalB3)
        PanelD6.add_widget(PBoriginal23)
        PanelD6.add_widget(PBoriginalB23)
        self.Perfil_Direcciones.add_widget(PanelD6)
        
        PanelD5 =  GridLayout (cols = 3 , size_hint = (1,None) ,height = 210, spacing = 0) 
        
        PBoriginal14 = Button(text= "[color=#404040]",  markup = True, background_normal = self.images + "blanco2CB2.png" , background_color = (1,1,1,1),font_size = "16sp", size_hint= (.20, None), height = 70)
        self.PBoriginal1B4 = Button(text= "[color=#404040]Deposito/Transferencia Bancaria",  markup = True, background_normal = self.images + "blanco2C2.png" , background_color = (1,1,1,1),font_size = "16sp", size_hint= (1, None), height = 70)
        PBoriginal24 = Image(source="", size_hint = (.20, None), height = 70, allow_stretch = False, keep_ratio = True)
        
        self.PBoriginal2B4 =  Button(text= "[color=#404040]",  markup = True, background_normal = self.images + "blanco2CC2.png" , background_color = (1,1,1,1),font_size = "16sp", size_hint= (.20, None), height = 70)
        PBoriginal24B = Button(text= "[color=#404040]Paypal",  markup = True, background_normal = self.images + "blanco2C2.png" , background_color = (1,1,1,1),font_size = "16sp", size_hint= (1, None), height = 70)
        self.PBoriginal2B4B = Image(source="", size_hint = (.20, None), height = 70, allow_stretch = False, keep_ratio = True)
        
        self.PBoriginal3B4 =  Button(text= "[color=#404040]",  markup = True, background_normal = self.images + "blanco2CC2.png" , background_color = (1,1,1,1),font_size = "16sp", size_hint= (.20, None), height = 70)
        PBoriginal34B = Button(text= "[color=#404040]Contra Engrega",  markup = True, background_normal = self.images + "blanco2C2.png" , background_color = (1,1,1,1),font_size = "16sp", size_hint= (1, None), height = 70)
        self.PBoriginal3B4B = Image(source="", size_hint = (.20, None), height = 70, allow_stretch = False, keep_ratio = True)
		
        PanelD5.add_widget(PBoriginal14)
        PanelD5.add_widget(PBoriginal24)
        PanelD5.add_widget(self.PBoriginal1B4)
        
		
		
        PanelD5.add_widget(self.PBoriginal2B4)
        PanelD5.add_widget(self.PBoriginal2B4B)
        PanelD5.add_widget(PBoriginal24B)
        
        PanelD5.add_widget(self.PBoriginal3B4)
        PanelD5.add_widget(self.PBoriginal3B4B)
        PanelD5.add_widget(PBoriginal34B)
		
        def definirA1(button):
			PBoriginal24.source = self.images + "Entypo_2713(6)_64.png"
			self.PBoriginal2B4B.source = self.images +"blanco.png"
			self.PBoriginal3B4B.source = self.images +"blanco.png"

                
        def definirA2(button):
			self.PBoriginal2B4B.source = self.images + "Entypo_2713(6)_64.png"
			self.PBoriginal3B4B.source = self.images +"blanco.png"
			PBoriginal24.source = self.images +"blanco.png"

				
        def definirA3(button):
			self.PBoriginal3B4B.source = self.images + "Entypo_2713(6)_64.png"
			self.PBoriginal2B4B.source = self.images +"blanco.png"
			PBoriginal24.source = self.images +"blanco.png"
			
		
        PBoriginal14.bind(on_press = definirA1)
        self.PBoriginal2B4.bind(on_press = definirA2)
        self.PBoriginal3B4.bind(on_press = definirA3)

			
        self.PBoriginal3B5B = Button(text= "[color=#404040]"+"Confirmar Pedido",  markup = True, background_normal = self.images + "blanco2.png" , background_color = (1,1,1,1),font_size = "16sp", size_hint= (.20, None), height = 70, width = 35)
        self.PBoriginal3B6B = Button(text= "[color=#404040]"+"Cancelar Pedido",  markup = True, background_normal = self.images + "blanco2.png" , background_color = (1,1,1,1),font_size = "16sp", size_hint= (.20, None), height = 70, width = 35)
        btn6_G_4 = Image(source=self.images + "asdB.png", size_hint = (1, None), height = 25, allow_stretch = True, keep_ratio = False)
        
        self.Perfil_Direcciones.add_widget(PanelD5)
        self.Perfil_Direcciones.add_widget(btn6_G_4)
        self.Perfil_Direcciones.add_widget(self.PBoriginal3B5B )
        self.Perfil_Direcciones.add_widget(self.PBoriginal3B6B )
        
        
        self.PBoriginal3B5B.bind(on_press = self.CREAR_PEDIDO)

        
        # ____________________________________________________________________________________________________
        
        self.Registro_Usuario = GridLayout(cols = 1 , size_hint = (1, None))
        self.Registro_Usuario_root = ScrollView(size_hint=(1, 1), size=(Window.width, Window.height))
        self.Registro_Usuario.bind(minimum_height=self.Registro_Usuario.setter('height'))

        self.Registro_Usuario_root.add_widget(self.Registro_Usuario)
        
        Campos = ["Usuario", "Password", "Correo"]
        a = 0

        a = a + 1
        Registro_grid = GridLayout(cols = 1 , size_hint = (1,None), height = 300)
        btn6_G = Image(source=self.images + "asd.png", size_hint = (1, None), height = 25, allow_stretch = True, keep_ratio = False) 
        btn6_G_2 = Image(source=self.images + "blanco.png", size_hint = (1, None), height = 25, allow_stretch = True, keep_ratio = False) 
        btn6_G_3 = Image(source=self.images + "blanco.png", size_hint = (1, None), height = 50, allow_stretch = True, keep_ratio = False) 
        caja_B6_2 = Button(background_down = self.images + "color_negro.png" ,size_hint = (1,None), height = 50, text = "Registro", markup = True, background_color = (1,1,1,1), background_normal = self.images + 'color_negro.png', font_size = 24 )
        if a == 1:
            self.Registro_Usuario.add_widget(btn6_G_3)
            self.Registro_Usuario.add_widget(caja_B6_2)
            self.Registro_Usuario.add_widget(btn6_G)
        self.Registro_label = Button(text ="[color=#404040]"+ "Usuario", background_color = (1,1,1,1) , background_normal = self.images + "blanco.png", size_hint = (1,None), height = 40, markup = True)
        self.Registro_text = TextInput(font_size=16, height=35, size_hint_y=None,
                                     multiline=False,
                                     background_color=(1,1,1,1),
                                     background_normal = self.images + 'textboxB.png',
                                     background_active = self.images + 'textboxB2.png', foreground_color = (0,0,0,.7),
                                     )
        self.Registro_label2 = Button(text ="[color=#404040]"+ "Password", background_color = (1,1,1,1) , background_normal = self.images + "blanco.png", size_hint = (1,None), height = 40, markup = True)
        self.Registro_text2 = TextInput(font_size=16, height=35, size_hint_y=None,
                                     multiline=False,
                                     background_color=(1,1,1,1),
                                     background_normal = self.images + 'textboxB.png',
                                     background_active = self.images + 'textboxB2.png', foreground_color = (0,0,0,.7),password = True
                                     )
        self.Registro_label3 = Button(text ="[color=#404040]"+ "Correo", background_color = (1,1,1,1) , background_normal = self.images + "blanco.png", size_hint = (1,None), height = 40, markup = True)
        self.Registro_text3 = TextInput(font_size=16, height=35, size_hint_y=None,
                                     multiline=False,
                                     background_color=(1,1,1,1),
                                     background_normal = self.images + 'textboxB.png',
                                     background_active = self.images + 'textboxB2.png', foreground_color = (0,0,0,.7),
                                     )
        
        Registro_grid.add_widget(self.Registro_label)
        Registro_grid.add_widget(self.Registro_text)
        Registro_grid.add_widget(self.Registro_label2)
        Registro_grid.add_widget(self.Registro_text2)
        Registro_grid.add_widget(self.Registro_label3)
        Registro_grid.add_widget(self.Registro_text3)
        Registro_grid.add_widget(btn6_G_2)
        self.Registro_Usuario.add_widget(Registro_grid)
        btn6_G_3 = Image(source=self.images + "asdB.png", size_hint = (1, None), height = 25, allow_stretch = True, keep_ratio = False)
        Registro_Button1 = Button(text = "[color=#404040]Confirmar Registro", size_hint = (1,None), height = 50, background_normal = self.images + "blanco2C.png", markup = True)
        Registro_Button2 = Button(text = "[color=#404040]Cancelar", size_hint = (1,None), height = 50, background_normal = self.images + "blanco2.png", markup = True)
        Registro_Button1.bind(on_press=(lambda x: self.CREAR_USUARIO(str(self.UsuarioNO + 1),self.Registro_text.text, self.Registro_text2.text,self.Registro_text3.text,"False")))
        self.Registro_Usuario.add_widget(btn6_G_3)
        self.Registro_Usuario.add_widget(Registro_Button1)
        self.Registro_Usuario.add_widget(Registro_Button2)
        Registro_Button2.bind(on_press = self.INICIO)
        
            
        # ____________________________________________________________________________________________________
        
        self.Crearcategoria_Layout = GridLayout(cols = 1 , size_hint = (1,1))
        self.crearcategoriapopup = Popup(
        title='',
        markup = True, title_size = 14,
        title_align = 'center',
        content = self.Crearcategoria_Layout ,
        background = "blanco3.png",
        separator_color = (0,0,0,0),
        title_color = (0,0,0,.5),
        size_hint = (.5, .8)
        )
        
        self.Crearcategoria_Titulo = Label(text = "[color=#404040]Categoria" , background_color = (1,1,1,1),
        size_hint_y = None , height = 50, font_size = 24, markup = True

        )

        self.Crearcategoria_Button = Button(text = "Listo" , background_color = (1,1,1,1) , border = (1,1,1,1) , background_normal = self.images + "color_rojo.png" , size_hint_y = None , height = 50)
        self.Crearcategoria_TextInput1 = TextInput(height = 30 , text = "Nombre" ,size_hint_y = None , Readonly = True , Line_Spacing = 3, background_normal = self.images + "blanco3.png" , background_color = (1,1,1,1), font_size = '15sp', background_disabled_normal = self.images + "blanco3.png", disabled_foreground_color = (0,0,0,1))
        self.Crearcategoria_TextInput2 = TextInput(height = 30 , text = "Teléfono" ,size_hint_y = None , Readonly = True , Line_Spacing = 3, background_normal = self.images + "blanco3.png" , background_color = (1,1,1,1), font_size = '15sp', background_disabled_normal = self.images + "blanco3.png", disabled_foreground_color = (0,0,0,1))
        self.Crearcategoria_TextInput3 = TextInput(height = 30 , text = "Direccion" ,size_hint_y = None , Readonly = True , Line_Spacing = 3, background_normal = self.images + "blanco3.png" , background_color = (1,1,1,1), font_size = '15sp', background_disabled_normal = self.images + "blanco3.png", disabled_foreground_color = (0,0,0,1))
        self.Crearcategoria_TextInput4 = TextInput(height = 30 , text = "Categoria" ,size_hint_y = None , Readonly = True , Line_Spacing = 3, background_normal = self.images + "blanco3.png" , background_color = (1,1,1,1), font_size = '15sp', background_disabled_normal = self.images + "blanco3.png", disabled_foreground_color = (0,0,0,1))
        
        
        self.Crearcategoria_Layout.add_widget(self.Crearcategoria_Titulo)
        self.Crearcategoria_Layout.add_widget(self.Crearcategoria_TextInput1)
        #self.Crearcategoria_Layout.add_widget(self.Crearcategoria_TextInput2)
        #self.Crearcategoria_Layout.add_widget(self.Crearcategoria_TextInput3)
        #self.Crearcategoria_Layout.add_widget(self.Crearcategoria_TextInput4)
        
        self.Crearcategoria_Layout.add_widget(self.Crearcategoria_Button)
        #s = 0
        self.Crearcategoria_Button.bind(on_press = lambda x: self.CREARCATEGORIA(self.Crearcategoria_TextInput1.text))
        
        # ____________________________________________________________________________________________________
        
        self.Primerinicio_Layout_Layout = GridLayout(cols = 1 , size_hint = (None,1) , width = 300)
        self.Primerinicio_Root = GridLayout(cols = 3 , size_hint = (1,1))
        AX1 = Image()
        AX2 = Image()
        AX3 = Image()
        AX4 = Image()
        AX5 = Image()
        
        self.Primerinicio_Root.add_widget(AX1)
        self.Primerinicio_Root.add_widget(self.Primerinicio_Layout_Layout)
        self.Primerinicio_Root.add_widget(AX2)
        self.Primerinicio_Layoutpopup = Popup(
        title='',
        markup = True, title_size = 14,
        title_align = 'center',
        content = self.Primerinicio_Root ,
        background = "blanco3.png",
        separator_color = (0,0,0,0),
        title_color = (0,0,0,.5),
        size_hint = (None, .8),
        width = 400,auto_dismiss=False
        )
        
        self.Primerinicio_Layout_Titulo = Label(text = "[color=#404040]Configure su Administrador." , background_color = (1,1,1,1),
        size_hint_y = None , height = 50, font_size = 24, markup = True

        )

        self.Primerinicio_Layout_Button = Button(text = "Listo" , background_color = (1,1,1,1) , border = (1,1,1,1) , background_normal = self.images + "color_rojo.png" , size_hint_y = None , height = 50)
        self.Primerinicio_Layout_Label1 = Label(markup = True,height = 30 , text = "[color=#404040]User" ,size_hint_y = None , Readonly = True , Line_Spacing = 3, background_normal = self.images + "blanco3.png" , background_color = (1,1,1,1), font_size = '15sp', background_disabled_normal = self.images + "blanco3.png", disabled_foreground_color = (0,0,0,1))
        self.Primerinicio_Layout_Text1 = TextInput(height = 30 ,size_hint_y = None , Readonly = True , Line_Spacing = 3, background_normal = self.images + "blanco3.png" , background_color = (1,1,1,1), font_size = '15sp', background_disabled_normal = self.images + "blanco3.png", disabled_foreground_color = (0,0,0,1))
        self.Primerinicio_Layout_Label2 = Label(markup = True,height = 30 , text = "[color=#404040]Password" ,size_hint_y = None , Readonly = True , Line_Spacing = 3, background_normal = self.images + "blanco3.png" , background_color = (1,1,1,1), font_size = '15sp', background_disabled_normal = self.images + "blanco3.png", disabled_foreground_color = (0,0,0,1))
        self.Primerinicio_Layout_Text2 = TextInput(password = True,height = 30 ,size_hint_y = None , Readonly = True , Line_Spacing = 3, background_normal = self.images + "blanco3.png" , background_color = (1,1,1,1), font_size = '15sp', background_disabled_normal = self.images + "blanco3.png", disabled_foreground_color = (0,0,0,1))
        self.Primerinicio_Layout_Label3 = Label(markup = True,height = 30 , text = "[color=#404040]E-Mail" ,size_hint_y = None , Readonly = True , Line_Spacing = 3, background_normal = self.images + "blanco3.png" , background_color = (1,1,1,1), font_size = '15sp', background_disabled_normal = self.images + "blanco3.png", disabled_foreground_color = (0,0,0,1))
        self.Primerinicio_Layout_Text3 = TextInput(height = 30 ,size_hint_y = None , Readonly = True , Line_Spacing = 3, background_normal = self.images + "blanco3.png" , background_color = (1,1,1,1), font_size = '15sp', background_disabled_normal = self.images + "blanco3.png", disabled_foreground_color = (0,0,0,1))
        self.Primerinicio_Layout_Label4 = Label(markup = True,height = 30 , text = "[color=#404040]Este usuario tendra derechos de" ,size_hint_y = None , Readonly = True , Line_Spacing = 3, background_normal = self.images + "blanco3.png" , background_color = (1,1,1,1), font_size = '13sp', background_disabled_normal = self.images + "blanco3.png", disabled_foreground_color = (0,0,0,1))
        self.Primerinicio_Layout_Label5 = Label(markup = True,height = 30 , text = "[color=#404040]administrador para su disposicion." ,size_hint_y = None , Readonly = True , Line_Spacing = 3, background_normal = self.images + "blanco3.png" , background_color = (1,1,1,1), font_size = '13sp', background_disabled_normal = self.images + "blanco3.png", disabled_foreground_color = (0,0,0,1))

        
        self.Primerinicio_Layout_Layout.add_widget(self.Primerinicio_Layout_Titulo)
        self.Primerinicio_Layout_Layout.add_widget(AX5)
        self.Primerinicio_Layout_Layout.add_widget(self.Primerinicio_Layout_Label1)
        self.Primerinicio_Layout_Layout.add_widget(self.Primerinicio_Layout_Text1)
        self.Primerinicio_Layout_Layout.add_widget(self.Primerinicio_Layout_Label2)
        self.Primerinicio_Layout_Layout.add_widget(self.Primerinicio_Layout_Text2)
        self.Primerinicio_Layout_Layout.add_widget(self.Primerinicio_Layout_Label3)
        self.Primerinicio_Layout_Layout.add_widget(self.Primerinicio_Layout_Text3)
        self.Primerinicio_Layout_Layout.add_widget(AX4)
        self.Primerinicio_Layout_Layout.add_widget(self.Primerinicio_Layout_Label4)
        self.Primerinicio_Layout_Layout.add_widget(self.Primerinicio_Layout_Label5)
        self.Primerinicio_Layout_Layout.add_widget(AX3)



        
        self.Primerinicio_Layout_Layout.add_widget(self.Primerinicio_Layout_Button)
        #s = 0
        #self.Primerinicio_Layout_Button.bind(on_press = lambda x: self.Primerinicio_Layout(self.Primerinicio_Layout_TextInput1.text))
        #self.Primerinicio_Layout_Button.bind(on_press = self.PINICIOPOPUPCERRAR)
        self.Primerinicio_Layout_Button.bind(on_press =lambda x: self.CREAR_USUARIO(str(self.UsuarioNO + 1), self.Primerinicio_Layout_Text1.text, self.Primerinicio_Layout_Text2.text , self.Primerinicio_Layout_Text3.text, "True"))
        
        
        # ____________________________________________________________________________________________________
        
        self.Anidar_Layout_Layout = GridLayout(cols = 1 , size_hint = (None,1) , width = 300)
        self.Anidar_Root = GridLayout(cols = 3 , size_hint = (1,1))
        AL1 = Image()
        AL2 = Image()
        AL3 = Image()
        AL4 = Image()
        AL5 = Image()
        
        self.Anidar_Root.add_widget(AL1)
        self.Anidar_Root.add_widget(self.Anidar_Layout_Layout)
        self.Anidar_Root.add_widget(AL2)
        self.Anidar_Layoutpopup = Popup(
        title='',
        markup = True, title_size = 14,
        title_align = 'center',
        content = self.Anidar_Root ,
        background = "blanco3.png",
        separator_color = (0,0,0,0),
        title_color = (0,0,0,.5),
        size_hint = (None, .8),
        width = 400,auto_dismiss=True
        )
        
        self.Anidar_Layout_Titulo = Label(text = "[color=#404040]Configurar Usuario." , background_color = (1,1,1,1),
        size_hint_y = None , height = 50, font_size = 24, markup = True

        )

        self.Anidar_Layout_Button = Button(text = "Listo" , background_color = (1,1,1,1) , border = (1,1,1,1) , background_normal = self.images + "color_rojo.png" , size_hint_y = None , height = 50)
        self.Anidar_Layout_Label1 = Label(markup = True,height = 30 , text = "[color=#404040]User" ,size_hint_y = None , Readonly = True , Line_Spacing = 3, background_normal = self.images + "blanco3.png" , background_color = (1,1,1,1), font_size = '15sp', background_disabled_normal = self.images + "blanco3.png", disabled_foreground_color = (0,0,0,1))
        self.Anidar_Layout_Text1 = TextInput(height = 30 ,size_hint_y = None , Readonly = True , Line_Spacing = 3, background_normal = self.images + "blanco3.png" , background_color = (1,1,1,1), font_size = '15sp', background_disabled_normal = self.images + "blanco3.png", disabled_foreground_color = (0,0,0,1))
        self.Anidar_Layout_Label2 = Label(markup = True,height = 30 , text = "[color=#404040]Password" ,size_hint_y = None , Readonly = True , Line_Spacing = 3, background_normal = self.images + "blanco3.png" , background_color = (1,1,1,1), font_size = '15sp', background_disabled_normal = self.images + "blanco3.png", disabled_foreground_color = (0,0,0,1))
        self.Anidar_Layout_Text2 = TextInput(password = True,height = 30 ,size_hint_y = None , Readonly = True , Line_Spacing = 3, background_normal = self.images + "blanco3.png" , background_color = (1,1,1,1), font_size = '15sp', background_disabled_normal = self.images + "blanco3.png", disabled_foreground_color = (0,0,0,1))
        self.Anidar_Layout_Label3 = Label(markup = True,height = 30 , text = "[color=#404040]E-Mail" ,size_hint_y = None , Readonly = True , Line_Spacing = 3, background_normal = self.images + "blanco3.png" , background_color = (1,1,1,1), font_size = '15sp', background_disabled_normal = self.images + "blanco3.png", disabled_foreground_color = (0,0,0,1))
        self.Anidar_Layout_Text3 = TextInput(height = 30 ,size_hint_y = None , Readonly = True , Line_Spacing = 3, background_normal = self.images + "blanco3.png" , background_color = (1,1,1,1), font_size = '15sp', background_disabled_normal = self.images + "blanco3.png", disabled_foreground_color = (0,0,0,1))
        self.Anidar_Layout_Label4 = Label(markup = True,height = 30 , text = "[color=#404040]Este usuario tendra derechos" ,size_hint_y = None , Readonly = True , Line_Spacing = 3, background_normal = self.images + "blanco3.png" , background_color = (1,1,1,1), font_size = '13sp', background_disabled_normal = self.images + "blanco3.png", disabled_foreground_color = (0,0,0,1))
        self.Anidar_Layout_Label5 = Label(markup = True,height = 30 , text = "[color=#404040]de informarse sobre este contacto." ,size_hint_y = None , Readonly = True , Line_Spacing = 3, background_normal = self.images + "blanco3.png" , background_color = (1,1,1,1), font_size = '13sp', background_disabled_normal = self.images + "blanco3.png", disabled_foreground_color = (0,0,0,1))

        
        self.Anidar_Layout_Layout.add_widget(self.Anidar_Layout_Titulo)
        self.Anidar_Layout_Layout.add_widget(AL5)
        self.Anidar_Layout_Layout.add_widget(self.Anidar_Layout_Label1)
        self.Anidar_Layout_Layout.add_widget(self.Anidar_Layout_Text1)
        self.Anidar_Layout_Layout.add_widget(self.Anidar_Layout_Label2)
        self.Anidar_Layout_Layout.add_widget(self.Anidar_Layout_Text2)
        self.Anidar_Layout_Layout.add_widget(self.Anidar_Layout_Label3)
        self.Anidar_Layout_Layout.add_widget(self.Anidar_Layout_Text3)
        self.Anidar_Layout_Layout.add_widget(AL4)
        self.Anidar_Layout_Layout.add_widget(self.Anidar_Layout_Label4)
        self.Anidar_Layout_Layout.add_widget(self.Anidar_Layout_Label5)
        self.Anidar_Layout_Layout.add_widget(AL3)



        
        self.Anidar_Layout_Layout.add_widget(self.Anidar_Layout_Button)
        #s = 0
        #self.Anidar_Layout_Button.bind(on_press = lambda x: self.Anidar_Layout(self.Anidar_Layout_TextInput1.text))
        self.Anidar_Layout_Button.bind(on_press = self.ANIDARPOPUPCERRAR)
        #self.Anidar_Layout_Button.bind(on_press =lambda x: self.CREAR_USUARIO(str(self.UsuarioNO + 1), self.Primerinicio_Layout_Text1.text, self.Primerinicio_Layout_Text2.text , self.Primerinicio_Layout_Text3.text, "True"))
        
        
        
        
        
        
        
        
        
        
        # ____________________________________________________________________________________________________
        
        self.SelFiltro_Layout = GridLayout(cols = 1 , size_hint = (1,1))
        self.SelFiltropopup = Popup(
        title='',
        markup = True, title_size = 14,
        title_align = 'center',
        content = self.SelFiltro_Layout ,
        background = "blanco3.png",
        separator_color = (0,0,0,0),
        title_color = (0,0,0,.5),
        size_hint = (.5, .5)
        )
        
        self.SelFiltro_Titulo = Label(text = "[color=#404040]Filtros" , background_color = (1,1,1,1),
        size_hint_y = None , height = 50, font_size = 24, markup = True

        )

        self.SelFiltro_Button = Button(markup = True,text = "[color=#404040]Contacto" , background_color = (1,1,1,1) , border = (1,1,1,1) , background_normal = self.images + "blanco2.png" , size_hint_y = None , height = 50)
        self.SelFiltro_TextInput1 = Button(markup = True,text = "[color=#404040]Usuario" , background_color = (1,1,1,1) , border = (1,1,1,1) , background_normal = self.images + "blanco2.png" , size_hint_y = None , height = 50)
        self.SelFiltro_TextInput2 = Button(markup = True,text = "[color=#404040]Equipo" , background_color = (1,1,1,1) , border = (1,1,1,1) , background_normal = self.images + "blanco2.png" , size_hint_y = None , height = 50)
        self.SelFiltro_TextInput3 = Button(markup = True,text = "[color=#404040]Estado" , background_color = (1,1,1,1) , border = (1,1,1,1) , background_normal = self.images + "blanco2.png" , size_hint_y = None , height = 50)
        #self.SelFiltro_TextInput4 = Button(text = "Listo" , background_color = (1,1,1,1) , border = (1,1,1,1) , background_normal = self.images + "color_rojo.png" , size_hint_y = None , height = 50)
        
        
        self.SelFiltro_Layout.add_widget(self.SelFiltro_Titulo)
        self.SelFiltro_Layout.add_widget(self.SelFiltro_TextInput1)
        self.SelFiltro_Layout.add_widget(self.SelFiltro_TextInput2)
        self.SelFiltro_Layout.add_widget(self.SelFiltro_TextInput3)
        #self.SelFiltro_Layout.add_widget(self.SelFiltro_TextInput4)
        
        def SelFiltro1(a):
            self.Filtro = "estado"
            self.SelFiltropopup.dismiss()
        def SelFiltro2(a):
            self.Filtro = "contacto"
            self.SelFiltropopup.dismiss()
        def SelFiltro3(a):
            self.Filtro = "pedido_por"
            self.SelFiltropopup.dismiss()
        def SelFiltro4(a):
            self.SelFiltropopup.dismiss()
            
            
        self.SelFiltro_Button.bind(on_press = SelFiltro2)
        self.SelFiltro_TextInput1.bind(on_press = SelFiltro3)
        self.SelFiltro_TextInput2.bind(on_press = SelFiltro4)
        self.SelFiltro_TextInput3.bind(on_press = SelFiltro1)
        
        
        self.SelFiltro_Layout.add_widget(self.SelFiltro_Button)
        #s = 0
        #self.SelFiltro_Button.bind(on_press = lambda x: self.CREARCATEGORIA(self.Crearcategoria_TextInput1.text))       


        # ____________________________________________________________________________________________________
        
        self.SelFiltro1_Layout = GridLayout(cols = 1 , size_hint = (1,1))
        self.SelFiltro1popup = Popup(
        title='',
        markup = True, title_size = 14,
        title_align = 'center',
        content = self.SelFiltro1_Layout ,
        background = "blanco3.png",
        separator_color = (0,0,0,0),
        title_color = (0,0,0,.5),
        size_hint = (.5, .5)
        )
        
        self.SelFiltro1_Titulo = Label(text = "[color=#404040]Filtros" , background_color = (1,1,1,1),
        size_hint_y = None , height = 50, font_size = 24, markup = True

        )

        self.SelFiltro1_Button = Button(markup = True,text = "[color=#404040]Contacto" , background_color = (1,1,1,1) , border = (1,1,1,1) , background_normal = self.images + "blanco2.png" , size_hint_y = None , height = 50)
        self.SelFiltro1_TextInput1 = Button(markup = True,text = "[color=#404040]Nombre" , background_color = (1,1,1,1) , border = (1,1,1,1) , background_normal = self.images + "blanco2.png" , size_hint_y = None , height = 50)
        self.SelFiltro1_TextInput2 = Button(markup = True,text = "[color=#404040]Telefono" , background_color = (1,1,1,1) , border = (1,1,1,1) , background_normal = self.images + "blanco2.png" , size_hint_y = None , height = 50)
        self.SelFiltro1_TextInput3 = Button(markup = True,text = "[color=#404040]Estado" , background_color = (1,1,1,1) , border = (1,1,1,1) , background_normal = self.images + "blanco2.png" , size_hint_y = None , height = 50)
        #self.SelFiltro1_TextInput4 = Button(text = "Listo" , background_color = (1,1,1,1) , border = (1,1,1,1) , background_normal = self.images + "color_rojo.png" , size_hint_y = None , height = 50)
        
        
        self.SelFiltro1_Layout.add_widget(self.SelFiltro1_Titulo)
        self.SelFiltro1_Layout.add_widget(self.SelFiltro1_TextInput1)
        self.SelFiltro1_Layout.add_widget(self.SelFiltro1_TextInput2)
        #self.SelFiltro1_Layout.add_widget(self.SelFiltro1_TextInput3)
        #self.SelFiltro1_Layout.add_widget(self.SelFiltro1_TextInput4)
        
        def SelFiltro11(a):
            self.Filtro2 = "nombre"
            self.SelFiltro1popup.dismiss()
        def SelFiltro12(a):
            self.Filtro2 = "telefono"
            self.SelFiltro1popup.dismiss()
        def SelFiltro13(a):
            self.Filtro = "pedido_por"
            self.SelFiltro1popup.dismiss()
        def SelFiltro14(a):
            self.SelFiltro1popup.dismiss()
            
            
        self.SelFiltro1_Button.bind(on_press = SelFiltro12)
        self.SelFiltro1_TextInput1.bind(on_press = SelFiltro11)
        self.SelFiltro1_TextInput2.bind(on_press = SelFiltro12)
        #self.SelFiltro1_TextInput3.bind(on_press = SelFiltro11)
        
        
        #self.SelFiltro1_Layout.add_widget(self.SelFiltro1_Button)
        #s = 0
        #self.SelFiltro1_Button.bind(on_press = lambda x: self.CREARCATEGORIA(self.Crearcategoria_TextInput1.text))
        
        # ____________________________________________________________________________________________________
        
        
        
        
        
        self.crearmenu_Layout = GridLayout(cols = 1 , size_hint = (1,1))
        self.crearmenupopup = Popup(
        title='',
        markup = True, title_size = 14,
        title_align = 'center',
        content = self.crearmenu_Layout ,
        background = "blanco3.png",
        separator_color = (0,0,0,0),
        title_color = (0,0,0,.5),
        size_hint = (.5, .8)
        )
        
        self.crearmenu_Titulo = Label(text = "[color=#404040]Menu" , background_color = (1,1,1,1),
        size_hint_y = None , height = 50, font_size = 24, markup = True

        )

        self.crearmenu_Button = Button(text = "Listo" , background_color = (1,1,1,1) , border = (1,1,1,1) , background_normal = self.images + "color_rojo.png" , size_hint_y = None , height = 50)
        self.crearmenu_Button.bind(on_press = self.CREARMENU)
        self.crearmenu_TextInput1 = TextInput(height = 30 , text = "" ,size_hint_y = None , Readonly = True , Line_Spacing = 3, background_normal = self.images + "blanco3.png" , background_color = (1,1,1,1), font_size = '15sp', background_disabled_normal = self.images + "blanco3.png", disabled_foreground_color = (0,0,0,1))
        self.crearmenu_Label1 = Label(markup = True,height = 30 , text = "[color=#404040]Titulo" ,size_hint_y = None , Readonly = True , Line_Spacing = 3, background_normal = self.images + "blanco3.png" , background_color = (1,1,1,1), font_size = '15sp', background_disabled_normal = self.images + "blanco3.png", disabled_foreground_color = (0,0,0,1))
        self.crearmenu_TextInput2 = TextInput(height = 30 , text = "" ,size_hint_y = None , Readonly = True , Line_Spacing = 3, background_normal = self.images + "blanco3.png" , background_color = (1,1,1,1), font_size = '15sp', background_disabled_normal = self.images + "blanco3.png", disabled_foreground_color = (0,0,0,1))
        self.crearmenu_Label2 = Label(markup = True,height = 30 , text = "[color=#404040]categoria" ,size_hint_y = None , Readonly = True , Line_Spacing = 3, background_normal = self.images + "blanco3.png" , background_color = (1,1,1,1), font_size = '15sp', background_disabled_normal = self.images + "blanco3.png", disabled_foreground_color = (0,0,0,1))
        self.crearmenu_TextInput3 = TextInput(disabled = True,height = 30 , text = "" ,size_hint_y = None , Readonly = True , Line_Spacing = 3, background_normal = self.images + "blanco3.png" , background_color = (1,1,1,1), font_size = '15sp', background_disabled_normal = self.images + "blanco3.png", disabled_foreground_color = (0,0,0,1))
        self.crearmenu_Label4 = Label(markup = True,height = 30 , text = "[color=#404040]Usuario" ,size_hint_y = None , Readonly = True , Line_Spacing = 3, background_normal = self.images + "blanco3.png" , background_color = (1,1,1,1), font_size = '15sp', background_disabled_normal = self.images + "blanco3.png", disabled_foreground_color = (0,0,0,1))
        self.crearmenu_TextInput4 = TextInput(height = 30 , text = "" ,size_hint_y = None , Readonly = True , Line_Spacing = 3, background_normal = self.images + "blanco3.png" , background_color = (1,1,1,1), font_size = '15sp', background_disabled_normal = self.images + "blanco3.png", disabled_foreground_color = (0,0,0,1))
        self.crearmenu_Label5 = Label(markup = True,height = 30 , text = "[color=#404040]contacto" ,size_hint_y = None , Readonly = True , Line_Spacing = 3, background_normal = self.images + "blanco3.png" , background_color = (1,1,1,1), font_size = '15sp', background_disabled_normal = self.images + "blanco3.png", disabled_foreground_color = (0,0,0,1))
        AX8 = Label()
        
        self.crearmenu_Layout.add_widget(self.crearmenu_Titulo)
        self.crearmenu_Layout.add_widget(self.crearmenu_Label1)
        self.crearmenu_Layout.add_widget(self.crearmenu_TextInput1)
        self.crearmenu_Layout.add_widget(self.crearmenu_Label2)
        self.crearmenu_Layout.add_widget(self.crearmenu_TextInput2)
        self.crearmenu_Layout.add_widget(self.crearmenu_Label4)
        self.crearmenu_Layout.add_widget(self.crearmenu_TextInput3)
        self.crearmenu_Layout.add_widget(self.crearmenu_Label5)
        self.crearmenu_Layout.add_widget(self.crearmenu_TextInput4)
        self.crearmenu_Layout.add_widget(AX8)
        
        self.crearmenu_Layout.add_widget(self.crearmenu_Button)
        #s = 0
        
        
        
        
        
        
        
        
        # ____________________________________________________________________________________________________
        self.Crearcontacto_Layout = GridLayout(cols = 1 , size_hint = (1,1))
        self.Crearcontactopopup = Popup(
        title='',
        markup = True, title_size = 14,
        title_align = 'center',
        content = self.Crearcontacto_Layout ,
        background = "blanco3.png",
        separator_color = (0,0,0,0),
        title_color = (0,0,0,.5),
        size_hint = (.5, .8)
        )
        
        self.Crearcontacto_Titulo = Label(text = "[color=#404040]Contacto" , background_color = (1,1,1,1),
        size_hint_y = None , height = 50, font_size = 24, markup = True

        )

        self.Crearcontacto_Button = Button(text = "Listo" , background_color = (1,1,1,1) , border = (1,1,1,1) , background_normal = self.images + "color_rojo.png" , size_hint_y = None , height = 50)
        self.Crearcontacto_TextInput1 = TextInput(height = 30 , text = "Nombre" ,size_hint_y = None , Readonly = True , Line_Spacing = 3, background_normal = self.images + "blanco3.png" , background_color = (1,1,1,1), font_size = '15sp', background_disabled_normal = self.images + "blanco3.png", disabled_foreground_color = (0,0,0,1))
        self.Crearcontacto_TextInput2 = TextInput(height = 30 , text = "Teléfono" ,size_hint_y = None , Readonly = True , Line_Spacing = 3, background_normal = self.images + "blanco3.png" , background_color = (1,1,1,1), font_size = '15sp', background_disabled_normal = self.images + "blanco3.png", disabled_foreground_color = (0,0,0,1))
        self.Crearcontacto_TextInput3 = TextInput(height = 30 , text = "Direccion" ,size_hint_y = None , Readonly = True , Line_Spacing = 3, background_normal = self.images + "blanco3.png" , background_color = (1,1,1,1), font_size = '15sp', background_disabled_normal = self.images + "blanco3.png", disabled_foreground_color = (0,0,0,1))
        self.Crearcontacto_TextInput4 = TextInput(height = 30 , text = "Categoria" ,size_hint_y = None , Readonly = True , Line_Spacing = 3, background_normal = self.images + "blanco3.png" , background_color = (1,1,1,1), font_size = '15sp', background_disabled_normal = self.images + "blanco3.png", disabled_foreground_color = (0,0,0,1))
        
        
        self.Crearcontacto_Layout.add_widget(self.Crearcontacto_Titulo)
        self.Crearcontacto_Layout.add_widget(self.Crearcontacto_TextInput1)
        self.Crearcontacto_Layout.add_widget(self.Crearcontacto_TextInput2)
        self.Crearcontacto_Layout.add_widget(self.Crearcontacto_TextInput3)
        self.Crearcontacto_Layout.add_widget(self.Crearcontacto_TextInput4)
        
        self.Crearcontacto_Layout.add_widget(self.Crearcontacto_Button)
        #s = 0
        self.Crearcontacto_Button.bind(on_press = lambda x: self.CREARCONTACTO(self.Crearcontacto_TextInput1.text,self.Crearcontacto_TextInput2.text,self.Crearcontacto_TextInput3.text,self.Crearcontacto_TextInput4.text))
        
        
        # ____________________________________________________________________________________________________
        self.CambiarHorario_Layout = GridLayout(cols = 1 , size_hint = (1,1))
        self.CambiarHorariopopup = Popup(
        title='',
        markup = True, title_size = 14,
        title_align = 'center',
        content = self.CambiarHorario_Layout ,
        background = "blanco3.png",
        separator_color = (0,0,0,0),
        title_color = (0,0,0,.5),
        size_hint = (.5, .835)
        )
        
        self.CambiarHorario_Titulo = Label(text = "[color=#404040]Cambiar Horario" , background_color = (1,1,1,1),
        size_hint_y = None , height = 50, font_size = 24, markup = True

        )

        self.CambiarHorario_Button = Button(text = "Listo" , background_color = (1,1,1,1) , border = (1,1,1,1) , background_normal = self.images + "color_rojo.png" , size_hint_y = None , height = 50)
        
        self.Dias = ['Lunes','Martes','Miercoles','Jueves','Viernes','Sabado','Domingo']
        self.CambiarHorario_Layout.add_widget(self.CambiarHorario_Titulo)
        for i in self.Dias:
            CambiarHorario_Layout2 = GridLayout(cols = 2 , height = 30 , size_hint = (1,None))
            CambiarHorario_TextInput1 = CheckBox()
            CambiarHorario_TextInput2 = Label(text ="[color=#404040][b]"+ i  , markup = True)
            
            CambiarHorario_Layout2.add_widget(CambiarHorario_TextInput2)
            CambiarHorario_Layout2.add_widget(CambiarHorario_TextInput1)
            #self.CambiarHorario_Layout.add_widget(CambiarHorario_Layout2)
            self.CambiarHorario_Layout.add_widget(CambiarHorario_Layout2)
            if i == self.Dias[len(self.Dias)-1]:
                CambiarHorario_Layout3 = GridLayout(cols = 2 , height = 150 , size_hint = (1,None))
                Espacio = Label()
                Espacio1 = Label()
                Espacio2 = Label()
                Espacio3 = Label()
                Espacio4 = Label()
                Espacio5 = Label()
                CambiarHorario_TextInput3 = Label(text ="[color=#404040][b]"+ "Desde" , markup = True)
                CambiarHorario_TextInput4 = TextInput(background_active = self.images + "textboxB2.png", background_normal = self.images + "textboxB2.png")
                CambiarHorario_TextInput5 = Label(text ="[color=#404040][b]"+ "Hasta" , markup = True)
                CambiarHorario_TextInput6 = TextInput(background_active = self.images + "textboxB2.png", background_normal = self.images + "textboxB2.png")
                CambiarHorario_Layout3.add_widget(Espacio)
                CambiarHorario_Layout3.add_widget(Espacio1)
                CambiarHorario_Layout3.add_widget(CambiarHorario_TextInput3)
                CambiarHorario_Layout3.add_widget(CambiarHorario_TextInput4)
                CambiarHorario_Layout3.add_widget(Espacio2)
                CambiarHorario_Layout3.add_widget(Espacio3)
                CambiarHorario_Layout3.add_widget(CambiarHorario_TextInput5)
                CambiarHorario_Layout3.add_widget(CambiarHorario_TextInput6)
                CambiarHorario_Layout3.add_widget(Espacio4)
                CambiarHorario_Layout3.add_widget(Espacio5)
                self.CambiarHorario_Layout.add_widget(CambiarHorario_Layout3)
                
        
                
        
        #self.CambiarHorario_Layout.add_widget(self.CambiarHorario_TextInput1)
        self.CambiarHorario_Layout.add_widget(self.CambiarHorario_Button)
        #s = 0
        #self.CambiarHorario_Button.bind(on_press = lambda x: self.CREARCONTACTO(self.CambiarHorario_TextInput1.text,self.CambiarHorario_TextInput2.text,self.CambiarHorario_TextInput3.text,self.CambiarHorario_TextInput4.text))

        
        
        
        
        
        
        
        
        
        # ____________________________________________________________________________________________________
        self.panelesformularios = [self.panel_AdmPedidos_root,self.panel_AdmContactos_root,self.panel2_Administrador_root,self.Menu_Administrador_root,self.panel_Sugerencias_root,self.panel_Categorias_root,self.Perfil_Direcciones_root, self.panel_AdmTienda_root ,self.panel_AdmSugerencias_root, self.panel_Contactos_root ,self.menu_Administrador_root , self.GL3,self.layout,self.panel_deptartamentos_root  , self.menu_Administrador_root,self.panel_Administrador_root , self.panel_Administrado_root, self.perfil_tienda, self.panel_perfil_root, self.panel_tienda_perfil_root, self.GL9_ScrollView, self.panel_gl9_root]
        # ____________________________________________________________________________________________________
        
        super(InterfaceManager, self).__init__(**kwargs)

        
    def SPLASH(self, button):
        guardado000 = self.images
        wing = Image(source =self.images + "principal.png",pos=(800,800))
        def cambiar(self):
            wing.source = guardado000 + "principal.png"
        self.animation = Animation(x=0, y=0, d=2, t='in_out_back')
        self.add_widget(wing)
        self.animation.start(wing)
        

        
        
        
        if self.checkin == True:
            self.Primerinicio = False
            print ("PRIMER INICIO DESACTIVADO")
            pass
        elif self.checkin == False:
            self.Primerinicio = True
            print ("PRIMER INICIO ACTIVADO")
            try:
                f = file("data.dat", "r")
                with open(self.patch + "/data.dat") as f:
                    content = f.readlines()
                self.DatosAdheridos = content[0].split(",")
                print self.DatosAdheridos
            except:
                pass
            
        if self.checkin2 == True:
            #self.Primerinicio = False
            print ("SESSION MANTENIDA ACTIVADA")
            try:
                f = file("loggeduser.data", "r")
                with open(self.patch + "/loggeduser.data") as f:
                    content2 = f.readlines()
                self.DatosAdheridos2 = content2[0].split(",")
                print self.DatosAdheridos2
                self.Usuario_Textbox.text = self.DatosAdheridos2[1]
                self.Constrasena_Textbox.text = self.DatosAdheridos2[2]
                self.Label_4B.active = True
                numerog = self.UsuariostableU.index(self.DatosAdheridos2[1])
                self.UserID = self.UsuariostableID[numerog]
                self.UserU = self.DatosAdheridos2[1]
                print self.UserID
                print self.UserU

            except:
                pass
        elif self.checkin2 == False:
            #self.Primerinicio = True
            print ("SESSION MANTENIDA DESACTIVADA")
            
        try:
            if self.DatosAdheridos2[0] == "ON":
                self.Label_4B2.active = True
                self.clear_widgets()
                self.add_widget(self.GL2_root)
                self.LOG_IN("Desactivado")
            else:
                Clock.schedule_once(cambiar, 0)
                Clock.schedule_once(self.INICIO, 5)
                pass
        except:
            self.Label_4B2.active = False
            Clock.schedule_once(cambiar, 0)
            Clock.schedule_once(self.INICIO, 5)
            pass

        
            
        if self.Primerinicio == True:
            print self.checkin
            print self.Primerinicio
            Clock.schedule_once(self.PINICIOPOPUP, 5)
            

    def LIMPIARPEDIDO(self, button):

        self.pedido_objetos[:] = []
        self.pedido_precios[:] = []
        self.pedido_establecimiento[:] = []
        self.usuario_pedido = ({'objeto': self.pedido_objetos[i], 'precio': self.pedido_precios[i] , 'establecimiento': self.pedido_establecimiento[i]} for i in range(len(self.pedido_objetos)))
        self.GL3.clear_widgets()
        self.Input2 = Label(text="[color=#f2f2f2]FACTURA[/color]", markup=True,
                                    size_hint_y=None,
                                    size_hint_x=0.2,
                                    height=70,
                                    font_size=24
                                    )
        self.Input2_B = Label(text="[color=#f2f2f2][/color]", markup=True,
                            size_hint_y=None,
                            size_hint_x=0.2,
                            height=40,
                            font_size=24
                            )
        self.GL3.add_widget(self.Input2)
        self.GL3.add_widget(self.Input2_B)

        self.Total = Button(background_down = self.images + "blanco.png" ,text = "[color=#404040][b] Total : ",markup = True, background_color = (1,1,1,1), background_normal = self.images + "blanco.png",size_hint_y = None, height = 50)
        
        self.Subtotal = Button(background_down = self.images + "blanco.png" ,text = "[color=#404040][b]Departamento : " ,markup = True, background_color = (1,1,1,1), background_normal = self.images + "blanco.png",size_hint_y = None, height = 50)
        

        self.Factura = Button(background_down = self.images + "blanco.png" ,text = "[color=#404040][b]CHECK-IN",markup = True, background_color = (1,1,1,1), background_normal = self.images + "blanco.png",size_hint_y = None, height = 50)
        self.Factura_Txt= Button(background_down = self.images + "blanco.png" ,text = "[color=#404040][b]",markup = True, background_color = (1,1,1,1), background_normal = self.images + "blanco.png",size_hint_y = None, height = 50)
        self.Items_No = Button(background_down = self.images + "blanco.png" ,text = "[color=#404040][b]Items : ",markup = True, background_color = (1,1,1,1), background_normal = self.images + "blanco.png",size_hint_y = None, height = 50)

        self.Fecha = Button(background_down = self.images + "blanco.png" ,text = "[color=#404040][b]Fecha : ",markup = True, background_color = (1,1,1,1), background_normal = self.images + "blanco.png",size_hint_y = None, height = 50)
        self.Fecha_Txt = Button(background_down = self.images + "blanco.png" ,text = "[color=#404040][b]"+ time.strftime("%d/%m/%Y"),markup = True, background_color = (1,1,1,1), background_normal = self.images + "blanco.png",size_hint_y = None, height = 50)

        self.grade = Button(background_down = self.images + "asd.png" ,size_hint_y= None ,height=25, background_normal = self.images + 'asd.png', background_color = (1,1,1,1))
        self.grade2 = Button(background_down = self.images + "asd.png" ,size_hint_y= None ,height=25, background_normal = self.images + 'asd.png', background_color = (1,1,1,1))

        self.grade3 = Button(background_down = self.images + "blanco.png" ,size_hint_y= None ,height=25, background_normal = self.images + 'blanco.png', background_color = (1,1,1,1))
        self.grade4 = Button(background_down = self.images + "blanco.png" ,size_hint_y= None ,height=25, background_normal = self.images + 'blanco.png', background_color = (1,1,1,1))

        #self.GL3.add_widget(self.Factura)
        #self.GL3.add_widget(self.Factura_Txt)

        self.GL3.add_widget(self.grade)
        self.GL3.add_widget(self.grade2)
        self.GL3.add_widget(self.Fecha)
        self.GL3.add_widget(self.Fecha_Txt)
        self.GL3.add_widget(self.Items_No)
        self.GL3.add_widget(self.Items_No_Txt)

        self.GL3.add_widget(self.Total)
        self.GL3.add_widget(self.Total_Txt)
        self.GL3.add_widget(self.Subtotal)
        self.GL3.add_widget(self.Subtotal_Txt)

        self.GL3.add_widget(self.grade3)
        self.GL3.add_widget(self.grade4)

        self.GL3.add_widget(self.Button10)
        self.GL3.add_widget(self.Button10_B)

        #self.GL3.add_widget(self.Input1)
        #self.GL3.add_widget(self.Input1_B)
        self.Items_No_Txt.text ="[color=#404040][b]"+"Vacio"
        self.Total_Txt.text ="[color=#404040][b]"+"0.00 RD$"
        self.Subtotal_Txt.text ="[color=#404040][b]"+"Sin seleccionar."
        self.usuario_pedido = ({'objeto': self.pedido_objetos[i], 'precio': self.pedido_precios[i] , 'establecimiento': self.pedido_establecimiento[i]} for i in range(len(self.pedido_objetos)))
        for i in self.usuario_pedido:
            print i
            a_B_GL10 = GridLayout(cols=1, spacing=0, size_hint_y=None, height = 120 , size_hint_x = 1)
            a_B_GL10_B = GridLayout(cols=1, spacing=0, size_hint_y=None, height = 120 , size_hint_x = 1)
            btn3_BGL10 = Button(background_down = self.images + "roro.png" ,size_hint_y=0.025 , background_normal = self.images + 'roro.png', background_color = (1,1,1,1))
            btn4_BGL10 = Button(background_down = self.images + "roro2.png" ,size_hint_y=0.025 , background_normal = self.images + 'roro2.png', background_color = (1,1,1,1))
            btn6_BGL10 = Button(background_down = self.images + "asd.png" ,size_hint_y= None ,height=25, background_normal = self.images + 'asd2.png', background_color = (1,1,1,1))

            btn1_BGL10 = Button(background_down = self.images + "blanco.png" ,text='[b][color=#ff1a1a]'+ i["objeto"], size_hint_y=0.1, height=30, background_normal = self.images + 'blanco.png', background_color = (1,1,1,1) , markup = True , font_size = 18,valign = 'top')
            btn5_BGL10 = Button(background_down = self.images + "blanco.png" ,text=i["precio"] , size_hint_y=0.050, height=30, background_normal = self.images + 'blanco.png', background_color = (1,1,1,1), markup = True , font_size = '15sp')

            btn2_BGL10 = Button(background_down = self.images + "blanco.png" ,text='[color=#404040][b]MC' , size_hint_y=0.1, height=30, background_normal = self.images + 'blanco.png',background_color = (1,1,1,1), markup   = True, font_size = 18)

            a_B_GL10.add_widget(btn6_BGL10)
            a_B_GL10.add_widget(btn1_BGL10)
            a_B_GL10.add_widget(btn3_BGL10)
            a_B_GL10.add_widget(btn2_BGL10)
            a_B_GL10.add_widget(btn4_BGL10)
            a_B_GL10.add_widget(btn5_BGL10)
            self.GL3.add_widget(a_B_GL10)
            
            btn3_BGL11 = Button(background_down = self.images + "roro.png" ,size_hint_y=0.025 , background_normal = self.images + 'roro.png', background_color = (1,1,1,1))
            btn4_BGL11 = Button(background_down = self.images + "roro2.png" ,size_hint_y=0.025 , background_normal = self.images + 'roro2.png', background_color = (1,1,1,1))
            btn6_BGL11 = Button(background_down = self.images + "asd.png" ,size_hint_y= None ,height=25, background_normal = self.images + 'asd2.png', background_color = (1,1,1,1))

            btn1_BGL11 = Button(background_down = self.images + "blanco.png" ,text='[b][color=#ff1a1a]'+ i["precio"] + ".00 RD$", size_hint_y=0.1, height=30, background_normal = self.images + 'blanco.png', background_color = (1,1,1,1) , markup = True , font_size = 18,valign = 'top')
            btn5_BGL11 = Button(background_down = self.images + "blanco.png" ,text=i["precio"] , size_hint_y=0.050, height=30, background_normal = self.images + 'blanco.png', background_color = (1,1,1,1), markup = True , font_size = '15sp')

            btn2_BGL11 = Button(background_down = self.images + "blanco.png" ,text='[color=#404040][b]1' , size_hint_y=0.1, height=30, background_normal = self.images + 'blanco.png',background_color = (1,1,1,1), markup   = True, font_size = 18)

            
            a_B_GL10_B.add_widget(btn6_BGL11)
            a_B_GL10_B.add_widget(btn1_BGL11)
            a_B_GL10_B.add_widget(btn3_BGL11)
            a_B_GL10_B.add_widget(btn2_BGL11)
            a_B_GL10_B.add_widget(btn4_BGL11)
            a_B_GL10_B.add_widget(btn5_BGL11)
            self.GL3.add_widget(a_B_GL10_B)
        
    def INSERTAR_in_PEDIDO(self, id_objeto, id_tienda):
        print id_tienda
        
        url = self.Dominio2+"Contacto/"+str(id_tienda)+"/"
        json_obj = urllib2.urlopen(url)
        i = json.load(json_obj)
        self.TiendaSolicitada = id_tienda
        self.Total_Txt2.text = "[color=#404040][b]"+i["nombre"]
        print self.Total_Txt2.text
        self.guardado02 = i["categoria"]
        url = self.Dominio2+"Categoria/"+str(self.guardado02)+"/"
        json_obj = urllib2.urlopen(url)
        i = json.load(json_obj)
        self.Subtotal_Txt.text = "[color=#404040][b]"+i["categoria"]
        

        print ("No."+ str(id_objeto) + " Agregado")
        self.PedidoID.append(id_objeto)
        self.pedido_objetos.append(self.inventario_objetos[int(id_objeto)-1]) #AGREGAR OBJETO AL PEDIDO
        self.pedido_establecimiento.append("sin indexar")
        self.pedido_precios.append(self.inventario_precio[int(id_objeto)-1])
        self.usuario_pedido = ({'objeto': self.pedido_objetos[i], 'precio': self.pedido_precios[i] , 'establecimiento': self.pedido_establecimiento[i]} for i in range(len(self.pedido_objetos)))
        self.total1= 0
        for i in self.pedido_precios:
            self.total1 = self.total1 + int(i)
        A = "[color=#404040][b]"+str(self.total1)+ ".00 RD$"
        B = "[color=#404040][b]"+ str(len(self.pedido_objetos))
        self.ASD.text = A
        self.ASD3.text = B


    def SELECCIONAR_CONTACTO(self, button):
        pass
        self.clear_widgets()

    def INICIO(self, button):
        self.clear_widgets()
        self.add_widget(self.GL1)

    def MENU(self, button):
        self.clear_widgets()
        self.add_widget(self.GL2_root)
        
    def DIRECCIONES(self, button):
        if self.Items_No_Txt.text =="[color=#404040][b]Vacio":
            popupX = Popup(title='Noticias normales :v',markup = True, title_color = (0,0,0,.5),
                 content=Label(markup = True,
                     text='[color=#404040]Monto vacio.',
                     text_size=(150, None)),
                 size_hint=(None, None),background = self.images + "Button3.png", separator_color = (0,0,0,0),
                 size=(200, 100)
                 ) 
            popupX.open()
            print ("MONTO VACIO")
        else:
            for i in self.panelesformularios:
                try:
                   self.main_panel.remove_widget(i)
                   self.main_panel.add_widget(self.Perfil_Direcciones_root) 
                except:
                    pass
                
    def PRIMERINICIO(self, button):
        for i in self.panelesformularios:
            try:
               self.main_panel.remove_widget(i)
               self.main_panel.add_widget(self.Perfil_Direcciones_root) 
            except:
                pass

    def MENUS(self, button):
        for i in self.panelesformularios:
            try:
               self.main_panel.remove_widget(i)
               self.main_panel.add_widget(self.Menu_Administrador_root) 
            except:
                pass
    def CATEGORIAS(self, button):
        for i in self.panelesformularios:
            try: 
               self.main_panel.remove_widget(i)
               self.main_panel.add_widget(self.panel_Categorias_root) 
            except:
                pass
    def INVENTARIO(self, button):
        for i in self.panelesformularios:
            try:
               self.main_panel.remove_widget(i)
               self.main_panel.add_widget(self.GL3) 
            except:
                pass
        try:
            print self.usuario_pedido
            self.GL3.clear_widgets()
            self.Input2 = Label(text="[color=#f2f2f2]FACTURA[/color]", markup=True,
                                        size_hint_y=None,
                                        size_hint_x=0.2,
                                        height=70,
                                        font_size=24
                                        )
            self.Input2_B = Label(text="[color=#f2f2f2][/color]", markup=True,
                                size_hint_y=None,
                                size_hint_x=0.2,
                                height=40,
                                font_size=24
                                )
            self.GL3.add_widget(self.Input2)
            self.GL3.add_widget(self.Input2_B)

            self.Total = Button(background_down = self.images + "blanco.png" ,text = "[color=#404040][b] Total : ",markup = True, background_color = (1,1,1,1), background_normal = self.images + "blanco.png",size_hint_y = None, height = 50)
            
            self.Subtotal = Button(background_down = self.images + "blanco.png" ,text = "[color=#404040][b]Categoria : " ,markup = True, background_color = (1,1,1,1), background_normal = self.images + "blanco.png",size_hint_y = None, height = 50)
            

            self.Factura = Button(background_down = self.images + "blanco.png" ,text = "[color=#404040][b]CHECK-IN",markup = True, background_color = (1,1,1,1), background_normal = self.images + "blanco.png",size_hint_y = None, height = 50)
            self.Factura_Txt= Button(background_down = self.images + "blanco.png" ,text = "[color=#404040][b]",markup = True, background_color = (1,1,1,1), background_normal = self.images + "blanco.png",size_hint_y = None, height = 50)
            
            self.Total2 = Button(background_down = self.images + "blanco.png" ,text = "[color=#404040][b]Contacto : ",markup = True, background_color = (1,1,1,1), background_normal = self.images + "blanco.png",size_hint_y = None, height = 50)
            

            self.Items_No = Button(background_down = self.images + "blanco.png" ,text = "[color=#404040][b]Items : ",markup = True, background_color = (1,1,1,1), background_normal = self.images + "blanco.png",size_hint_y = None, height = 50)

            self.Fecha = Button(background_down = self.images + "blanco.png" ,text = "[color=#404040][b]Fecha : ",markup = True, background_color = (1,1,1,1), background_normal = self.images + "blanco.png",size_hint_y = None, height = 50)
            self.Fecha_Txt = Button(background_down = self.images + "blanco.png" ,text = "[color=#404040][b]"+ time.strftime("%d/%m/%Y"),markup = True, background_color = (1,1,1,1), background_normal = self.images + "blanco.png",size_hint_y = None, height = 50)

            self.grade = Button(background_down = self.images + "asd.png" ,size_hint_y= None ,height=25, background_normal = self.images + 'asd.png', background_color = (1,1,1,1))
            self.grade2 = Button(background_down = self.images + "asd.png" ,size_hint_y= None ,height=25, background_normal = self.images + 'asd.png', background_color = (1,1,1,1))

            self.grade3 = Button(background_down = self.images + "blanco.png" ,size_hint_y= None ,height=25, background_normal = self.images + 'blanco.png', background_color = (1,1,1,1))
            self.grade4 = Button(background_down = self.images + "blanco.png" ,size_hint_y= None ,height=25, background_normal = self.images + 'blanco.png', background_color = (1,1,1,1))

            #self.GL3.add_widget(self.Factura)
            #self.GL3.add_widget(self.Factura_Txt)

            self.GL3.add_widget(self.grade)
            self.GL3.add_widget(self.grade2)
            self.GL3.add_widget(self.Fecha)
            self.GL3.add_widget(self.Fecha_Txt)
            self.GL3.add_widget(self.Items_No)
            self.GL3.add_widget(self.Items_No_Txt)

            self.GL3.add_widget(self.Total)
            self.GL3.add_widget(self.Total_Txt)
            self.GL3.add_widget(self.Total2)
            self.GL3.add_widget(self.Total_Txt2)
            self.GL3.add_widget(self.Subtotal)
            self.GL3.add_widget(self.Subtotal_Txt)

            self.GL3.add_widget(self.grade3)
            self.GL3.add_widget(self.grade4)

            self.GL3.add_widget(self.Button10)
            self.GL3.add_widget(self.Button10_B)


            self.usuario_pedido = ({'objeto': self.pedido_objetos[i], 'precio': self.pedido_precios[i] , 'establecimiento': self.pedido_establecimiento[i]} for i in range(len(self.pedido_objetos)))
            for i in self.usuario_pedido:
                print i
                a_B_GL10 = GridLayout(cols=1, spacing=0, size_hint_y=None, height = 120 , size_hint_x = 1)
                a_B_GL10_B = GridLayout(cols=1, spacing=0, size_hint_y=None, height = 120 , size_hint_x = 1)
                btn3_BGL10 = Button(background_down = self.images + "roro.png" ,size_hint_y=0.025 , background_normal = self.images + 'roro.png', background_color = (1,1,1,1))
                btn4_BGL10 = Button(background_down = self.images + "roro2.png" ,size_hint_y=0.025 , background_normal = self.images + 'roro2.png', background_color = (1,1,1,1))
                btn6_BGL10 = Button(background_down = self.images + "asd.png" ,size_hint_y= None ,height=25, background_normal = self.images + 'asd2.png', background_color = (1,1,1,1))

                btn1_BGL10 = Button(background_down = self.images + "blanco.png" ,text='[b][color=#ff1a1a]'+ i["objeto"], size_hint_y=0.1, height=30, background_normal = self.images + 'blanco.png', background_color = (1,1,1,1) , markup = True , font_size = 18,valign = 'top')
                btn5_BGL10 = Button(background_down = self.images + "blanco.png" ,text=i["precio"] , size_hint_y=0.050, height=30, background_normal = self.images + 'blanco.png', background_color = (1,1,1,1), markup = True , font_size = '15sp')

                btn2_BGL10 = Button(background_down = self.images + "blanco.png" ,text='[color=#404040][b]MC' , size_hint_y=0.1, height=30, background_normal = self.images + 'blanco.png',background_color = (1,1,1,1), markup   = True, font_size = 18)

                a_B_GL10.add_widget(btn6_BGL10)
                a_B_GL10.add_widget(btn1_BGL10)
                a_B_GL10.add_widget(btn3_BGL10)
                a_B_GL10.add_widget(btn2_BGL10)
                a_B_GL10.add_widget(btn4_BGL10)
                a_B_GL10.add_widget(btn5_BGL10)
                self.GL3.add_widget(a_B_GL10)
                
                btn3_BGL11 = Button(background_down = self.images + "roro.png" ,size_hint_y=0.025 , background_normal = self.images + 'roro.png', background_color = (1,1,1,1))
                btn4_BGL11 = Button(background_down = self.images + "roro2.png" ,size_hint_y=0.025 , background_normal = self.images + 'roro2.png', background_color = (1,1,1,1))
                btn6_BGL11 = Button(background_down = self.images + "asd.png" ,size_hint_y= None ,height=25, background_normal = self.images + 'asd2.png', background_color = (1,1,1,1))

                btn1_BGL11 = Button(background_down = self.images + "blanco.png" ,text='[b][color=#ff1a1a]'+ i["precio"] + ".00 RD$", size_hint_y=0.1, height=30, background_normal = self.images + 'blanco.png', background_color = (1,1,1,1) , markup = True , font_size = 18,valign = 'top')
                btn5_BGL11 = Button(background_down = self.images + "blanco.png" ,text=i["precio"] , size_hint_y=0.050, height=30, background_normal = self.images + 'blanco.png', background_color = (1,1,1,1), markup = True , font_size = '15sp')

                btn2_BGL11 = Button(background_down = self.images + "blanco.png" ,text='[color=#404040][b]1' , size_hint_y=0.1, height=30, background_normal = self.images + 'blanco.png',background_color = (1,1,1,1), markup   = True, font_size = 18)

                
                a_B_GL10_B.add_widget(btn6_BGL11)
                a_B_GL10_B.add_widget(btn1_BGL11)
                a_B_GL10_B.add_widget(btn3_BGL11)
                a_B_GL10_B.add_widget(btn2_BGL11)
                a_B_GL10_B.add_widget(btn4_BGL11)
                a_B_GL10_B.add_widget(btn5_BGL11)
                self.GL3.add_widget(a_B_GL10_B)
                    
        
        except:
            ("carrito vacio.")
        texto = self.Items_No_Txt.text[18:]
        
        #if texto != "0":
            #self.GL3.add_widget(self.Input1)
            #self.GL3.add_widget(self.Input1_B)

    def CONTACTOS(self, button):
        for i in self.panelesformularios:
            try:
               self.main_panel.remove_widget(i)
               self.main_panel.add_widget(self.panel_Contactos_root) 
            except:
                pass
                
                
    def ADMTIENDA(self, button):
        ID_preciso = self.caja_B10.text[45:]
        url = self.Dominio2+"Contacto/"+str(ID_preciso)+"/"
        json_obj = urllib2.urlopen(url)
        i = json.load(json_obj)
        self.vista_Tienda2_perfil1B.text = "[color=#404040]"+ str(i['id'])
        self.vista_Tienda2_perfil2B.text = "[color=#404040]"+ str(i['nombre'])
        self.vista_Tienda2_perfil3B.text = "[color=#404040]"+ str(i['telefono'])
        self.vista_Tienda2_perfil4B.text = "[color=#404040]"+ str(i['direccion'])
        self.vista_Tienda2_perfil5B.text = "[color=#404040]"+ str(i['estado'])
        self.vista_Tienda2_perfil6B.text = "[color=#404040]"+ str(i['categoria'])
        self.cajas_dobles2.clear_widgets()
        for i in self.Menutable:
            print i['contacto']
            contador_o = 0
            #if i['contacto'] == self.UserID_C:
            for x in self.MenuSCtable:
                if i['contacto'] == x['contacto_id']:
                    for g in x['menu']:
                        contador_o += 1
                        if i['id'] == g:
                        
                            
                            caja_C4 = Button(background_down = self.images + "blanco.png" ,size_hint = (1,None), height = 50, text = "[color=#ff3333]"+x['sub_categoria'], markup = True, background_color = (1,1,1,1), background_normal = self.images + 'blanco.png', font_size = 24 )
                            caja_C5 = Button(background_down = self.images + "blanco.png" ,size_hint = (1,None), height = 50, text = "[color=#404040]""", markup = True, background_color = (1,1,1,1), background_normal = self.images + 'blanco.png')
                            self.caja_grid = GridLayout(cols = 2 ,spacing = 0, size_hint_y = None, height= 50, size_hint_x = .7)
                            self.caja_grid_IN = GridLayout(cols = 3 ,spacing = 0, size_hint_y = None, height= 50, size_hint_x = .3)
                            self.caja_grid_Button1 = Button(text = "[color=#404040]Add", background_normal = self.images + "blanco2C3.png", markup = True)
                            self.caja_grid_Button2 = Button(text = "[color=#404040]Edit", background_normal = self.images + "blanco2C3.png", markup = True)
                            self.caja_grid_Button3 = Button(text = "[color=#404040]Del", background_normal = self.images + "blanco2C3.png", markup = True)
                            
                            self.caja_grid_IN.add_widget(self.caja_grid_Button1)
                            self.caja_grid_IN.add_widget(self.caja_grid_Button2)
                            self.caja_grid_IN.add_widget(self.caja_grid_Button3)
                            self.caja_grid.add_widget(caja_C4)
                            self.caja_grid.add_widget(self.caja_grid_IN)
                            self.cajas_dobles2.add_widget(self.caja_grid)
                            #self.cajas_dobles2.add_widget(self.caja_grid_IN)
                            iguales11 = 0
                            for z in self.PlatoTable:
                                if z ['sub_categoria'] == x['id']:
                                    iguales11 += 1
                                    
                            for z in self.PlatoTable:
                                if z ['sub_categoria'] == x['id']:
                                    a_F = GridLayout(cols=3, spacing=0, size_hint_y=None, height = 100 , size_hint_x = 1)
                                    
                                    btn6_F = Button(background_down = self.images + "blanco7B.png" ,size_hint_y= None ,height=25, background_normal = self.images + 'blanco7.png', background_color = (1,1,1,1))                                    
                                    btn6_FB = Button(background_down = self.images + "blanco7B.png" ,size_hint_y= None ,height=25, background_normal = self.images + 'blanco7.png', background_color = (1,1,1,1))                                    
                                    btn6_FC = Button(background_down = self.images + "blanco7B.png" ,size_hint_y= None ,height=25, background_normal = self.images + 'blanco7.png', background_color = (1,1,1,1))                                    
                                    btn1_F = Button(background_down = self.images + "blanco.png" ,text='[b][color=#404040]'+ z['plato'], size_hint_y=0.1, height=30, background_normal = self.images + 'blanco.png', background_color = (1,1,1,1), markup = True , font_size = 18,valign = 'top')                                                                                                      
                                    btn5_F = CheckBox()
                                    btn2_F = Button(background_down = self.images + "blanco.png" ,text='[color=#404040][b]'+ z['precio'] + ' RD$' , size_hint_y=0.1, height=30, background_normal = self.images + 'blanco.png',background_color = (1,1,1,1), markup   = True, font_size = 18)
                                    btn4_F = Button(background_down = self.images + "roro2.png" ,size_hint_y=0.025 , background_normal = self.images + 'roro2.png', background_color = (1,1,1,1))
                                    btn4_FB = Button(background_down = self.images + "roro2.png" ,size_hint_y=0.025 , background_normal = self.images + 'roro2.png', background_color = (1,1,1,1))
                                    btn4_FC = Button(background_down = self.images + "roro2.png" ,size_hint_y=0.025 , background_normal = self.images + 'roro2.png', background_color = (1,1,1,1))
                                    
                                    a_F.add_widget(btn6_F)                                
                                    a_F.add_widget(btn6_FB)                                
                                    a_F.add_widget(btn6_FC)                                
                                    a_F.add_widget(btn5_F)                           
                                    a_F.add_widget(btn1_F)                           
                                    a_F.add_widget(btn2_F)
                                    a_F.add_widget(btn4_F)
                                    a_F.add_widget(btn4_FB)
                                    a_F.add_widget(btn4_FC)
                        
                     
                                    self.cajas_dobles2.add_widget(a_F)
                                    self.cajas_dobles2.height += 100
                                    print self.cajas_dobles2.height
                                    
                            if(iguales11%2==0):
                                pass
                            elif self.UserID == "09090909":
                                
                                print(str(a)+" es impar")
                                a_G = GridLayout(cols=1, spacing=0, size_hint_y=None, height = 100 , size_hint_x = 1)
                                btn3_G = Button(background_down = self.images + "roro.png" ,size_hint_y=0.025 , background_normal = self.images + 'roro.png', background_color = (1,1,1,1))
                                btn4_G = Button(background_down = self.images + "roro2.png" ,size_hint_y=0.025 , background_normal = self.images + 'roro2.png', background_color = (1,1,1,1))
                                btn6_G = Button(background_down = self.images + "asd.png" ,size_hint_y= None ,height=25, background_normal = self.images + 'asd.png', background_color = (1,1,1,1))
                                btn0_G = Button(background_down = self.images + "404.png" ,text='', size_hint_y=0.400, height=100, background_normal = self.images + '404.png')
                                btn1_G = Button(background_down = self.images + "blanco.png" ,text='[b][color=#404040]'+ "Espacio publicitario", size_hint_y=0.1, height=30, background_normal = self.images + 'blanco.png', background_color = (1,1,1,1), markup = True , font_size = 18,valign = 'top')
                                btn5_G = Button(background_down = self.images + "blanco.png" ,text='', size_hint_y=0.050, height=30, background_normal = self.images + 'blanco.png', background_color = (1,1,1,1), markup = True , font_size = '15sp')
                                btn_G = Button(background_down = self.images + "color_rojo.png" ,text="[color=#ed1c24]"+str(1)+'[/color]'+'+' , size_hint_y=0.2, size_hint_x = 0.2, height=70, background_normal = self.images + 'color_rojo.png', markup = True)
                                btn2_G = Button(background_down = self.images + "blanco.png" ,text='' , size_hint_y=0.1, height=30, background_normal = self.images + 'blanco.png',background_color = (1,1,1,1), markup   = True, font_size = 18)
                                name_G = btn_G.text
                                btn_G.bind(on_press= lambda name_G=name_G: self.INSERTAR_in_PEDIDO(name_G.text[15:-9],self.guardado01))

                                a_G.add_widget(btn6_G)
                                #a_G.add_widget(btn0_G)
                                a_G.add_widget(btn1_G)
                                #a_G.add_widget(btn3_G)
                                a_G.add_widget(btn2_G)
                                a_G.add_widget(btn4_G)
                                #a_G.add_widget(btn5_G)
                                #a_G.add_widget(btn_G)
                                self.cajas_dobles2.add_widget(a_G)
                                self.cajas_dobles2.height += 100
        for i in self.panelesformularios:
            try:
               self.main_panel.remove_widget(i)
               self.main_panel.add_widget(self.panel_AdmTienda_root)
            except:
                pass


            
    def ADMSUGERENCIAS(self,id):
        for i in self.panelesformularios:
            try:
                self.main_panel.remove_widget(i)
                self.main_panel.add_widget(self.panel_AdmSugerencias_root) 
            except:
                pass
                
        url = self.Dominio2+"Sugerencia/"+str(id)+"/"
        json_obj = urllib2.urlopen(url)
        i = json.load(json_obj)
        self.vista_sugerencia2_perfil1B.text ="[color=#404040]"+i["nombre"]
        self.vista_sugerencia2_perfil2B.text ="[color=#404040]"+str(i["categoria"])
        self.vista_sugerencia2_perfil3B.text ="[color=#404040]"+i["telefono"]
        self.vista_sugerencia2_perfil4B.text ="[color=#404040]"+i["direccion"]
        self.vista_sugerencia2_perfil5B.text ="[color=#404040]"+i["sugerido_por"]
        self.vista_sugerencia2_perfil6B.text ="[color=#404040]"+i["fecha_sugerencia"]
        self.vista_sugerencia2_perfil7B.text =str(i["id"])
                
                
    def ADMCONTACTOS(self,id):
        for i in self.panelesformularios:
            try:
                self.main_panel.remove_widget(i)
                self.main_panel.add_widget(self.panel_AdmContactos_root) 
            except:
                print "Error"
                
        url = self.Dominio2+"Contacto/"+str(id)+"/"
        print url
        json_obj = urllib2.urlopen(url)
        i = json.load(json_obj)
        self.vista_contacto1_perfil1B.text ="[color=#404040]"+str(i["id"])
        self.vista_contacto1_perfil2B.text ="[color=#404040]"+i["nombre"]
        self.vista_contacto1_perfil3B.text ="[color=#404040]"+i["telefono"]
        self.vista_contacto1_perfil4B.text ="[color=#404040]"+i["direccion"]
        self.vista_contacto1_perfil5B.text ="[color=#404040]"+i["estado"]
        self.vista_contacto1_perfil6B.text ="[color=#404040]"+str(i["categoria"])
        self.vista_contacto1_perfil7B.text =str(i["id"])
        
    def ADMPEDIDOS(self,id):
        for i in self.panelesformularios:
            try:
                self.main_panel.remove_widget(i)
                self.main_panel.add_widget(self.panel_AdmPedidos_root) 
            except:
                print "Error"
                
        url = self.Dominio2+"Pedido/"+str(id)+"/"
        print url
        json_obj = urllib2.urlopen(url)
        i = json.load(json_obj)
        self.vista_pedido1_perfil1B.text ="[color=#404040]"+str(i["pedido_id"])
        self.vista_pedido1_perfil2B.text ="[color=#404040]"+i["pedido_por"]
        self.vista_pedido1_perfil3B.text ="[color=#404040]"+i["descripcion_del_pedido"]
        self.vista_pedido1_perfil4B.text ="[color=#404040]"+str(i["precio_pedido_total"])
        self.vista_pedido1_perfil5B.text ="[color=#404040]"+i["estado"]
        self.vista_pedido1_perfil6B.text ="[color=#404040]"+str(i["categoria"])
        self.vista_pedido1_perfil7B.text =str(i["pedido_id"])
        
    def ADMSUGERENCIAS(self,id):
        for i in self.panelesformularios:
            try:
                self.main_panel.remove_widget(i)
                self.main_panel.add_widget(self.panel_AdmSugerencias_root) 
            except:
                print "Error"
                
        url = self.Dominio2+"Sugerencia/"+str(id)+"/"
        print url
        json_obj = urllib2.urlopen(url)
        i = json.load(json_obj)
        self.vista_sugerencia2_perfil1B.text ="[color=#404040]"+i["nombre"]
        self.vista_sugerencia2_perfil2B.text ="[color=#404040]"+str(i["categoria"])
        self.vista_sugerencia2_perfil3B.text ="[color=#404040]"+i["telefono"]
        self.vista_sugerencia2_perfil4B.text ="[color=#404040]"+i["direccion"]
        self.vista_sugerencia2_perfil5B.text ="[color=#404040]"+i["sugerido_por"]
        self.vista_sugerencia2_perfil6B.text ="[color=#404040]"+i["fecha_sugerencia"]
        self.vista_sugerencia2_perfil7B.text =str(i["id"])

    def ADMSUGERENCIAS_REGISTRAR(self,id):
        try:
            req = urllib2.Request(self.Dominio2+"Sugerencia/"+self.vista_sugerencia2_perfil7B.text+ "/")
            req.add_header('Content-Type', 'application/json')
            req.get_method = lambda: 'DELETE'
            response = urllib2.urlopen(req)
            
            abcz = len(self.Contactotable)+1
            data = {
            "id": int(abcz),
            "nombre": self.vista_sugerencia2_perfil1B.text[15:],
            "telefono": self.vista_sugerencia2_perfil3B.text[15:],
            "direccion":  self.vista_sugerencia2_perfil4B.text[15:],
            "categoria": 1
         }
            print data
                        
            req = urllib2.Request(self.Dominio2+"Contacto/")
            req.add_header('Content-Type', 'application/json')
            response = urllib2.urlopen(req, json.dumps(data))
            print("Contacto creado con exito.")
        except:
            print("ha ocurrido un error.")
            
    def ADMSUGERENCIAS_ELIMINAR(self,id):
        try:
            req = urllib2.Request(self.Dominio2+"Sugerencia/"+self.vista_sugerencia2_perfil7B.text+"/")
            print (self.Dominio2+"Sugerencia/"+self.vista_sugerencia2_perfil7B.text+"/")
            req.add_header('Content-Type', 'application/json')
            req.get_method = lambda: 'DELETE'
            response = urllib2.urlopen(req, json.dumps(data))
            for i in self.panelesformularios:
                try:
                   self.main_panel.remove_widget(i)
                   self.main_panel.add_widget(self.menu_Administrador_root) 
                except:
                    pass
        except:
            print ("ERROR")


                
    def HOME(self, button):
        for i in self.panelesformularios:
            try:
               self.main_panel.remove_widget(i)
               self.main_panel.add_widget(self.layout) 
            except:
                pass
                
        json_obj = urllib2.urlopen(self.Dominio2+"Contacto/" )
        Datos_Tabla = json.load(json_obj)
        for i in Datos_Tabla:
            self.Lista_Contactos_Nombres.append(str(i["nombre"]))
            self.Lista_Contactos_IDs.append(str(i["id"]))
            self.Lista_Contactos_Categorias.append(str(i["categoria"]))
        abcd = 0
        self.layout.clear_widgets()
        self.Contactotable = Datos_Tabla
        
        
        entrados = 0
        agregados = 0
        limite = 3
        
        for i in self.Contactotable:
            for x in self.Activos:
                abcd += 1
                f = GridLayout(cols=1, spacing=0, size_hint_y=None, height = 410 , size_hint_x = 1)
                if abcd == 1:
                    self.tiendas2 = Button(background_down = self.images + "blanco.png" ,text="[color=#404040]Nuevos Contactos", halign = 'center', height = 70 ,size_hint_y=None,markup=True, font_size = 24, background_normal = self.images + 'blanco.png', background_color = (1,1,1,1))
                    self.tiendas2_txt = Button(background_down = self.images + "blanco.png" ,text = "",size_hint_y=None, height = 70 , background_normal = self.images + 'blanco.png', background_color = (1,1,1,1), markup = True)

                    self.layout.add_widget(self.tiendas2)
                    self.layout.add_widget(self.tiendas2_txt)
                   
                if i["id"] == x:
                    
                    btnC3 = Button(background_down = self.images + "roro.png" ,size_hint_y=0.025 , background_normal = self.images + 'roro.png', background_color = (1,1,1,1))
                    btnC4 = Button(background_down = self.images + "roro2.png" ,size_hint_y=0.025 , background_normal = self.images + 'roro2.png', background_color = (1,1,1,1))
                    btnC6 = Button(background_down = self.images + "asd.png" ,size_hint_y= None ,height=25, background_normal = self.images + 'asd.png', background_color = (1,1,1,1))
                    btnC0 = Image(size_hint_y=0.4, height=300, source = self.images + '404.png')
                    btnC1 = Button(background_down = self.images + "blanco.png" ,text='[b][color=#404040] ' + i["nombre"], size_hint_y=0.1, height=30, background_normal = self.images + 'blanco.png', background_color = (1,1,1,1), markup = True , font_size = 18,valign = 'top')
                    btnC5 = Button(background_down = self.images + "blanco.png" ,text='', size_hint_y=0.050, height=30, background_normal = self.images + 'blanco.png', background_color = (1,1,1,1), markup = True , font_size = '15sp')
                    btnC = Button(background_down = self.images + "color_rojoB.png" ,text="[color=#ed1d27]"+str(i['id'])+"[/color]"+'>' , size_hint_y=0.2, size_hint_x = 0.2, height=70, background_normal = self.images + 'color_rojo.png', markup = True,font_size =23)
                    categoria_save = self.categorias[(i["categoria"])-1]
                    btnC2 = Button(background_down = self.images + "blanco.png" ,text='[color=#404040][b] ' + categoria_save , size_hint_y=0.1, height=30, background_normal = self.images + 'blanco.png',background_color = (1,1,1,1), markup   = True, font_size = 18)
                    name = btnC.text

                    #btnC.bind(on_press= lambda name=name: printR(name.text))
                    integer =i["id"]
                    seleccionado = self.Lista_Contactos_IDs[int(integer)-1]
                    print btnC.text[15:-9]
                    btnC.bind(on_press=lambda seleccionado=seleccionado: self.TIENDA(seleccionado.text[15:-9]))

                    f.add_widget(btnC6)
                    f.add_widget(btnC0)
                    f.add_widget(btnC1)
                    f.add_widget(btnC3)
                    f.add_widget(btnC2)
                    f.add_widget(btnC4)
                    f.add_widget(btnC5)
                    f.add_widget(btnC)
                    self.layout.add_widget(f)

                

                    
                    
        abcd = 0
        for i in self.Contactotable:
            abcd += 1
            a = GridLayout(cols=1, spacing=0, size_hint_y=None, height = 410 , size_hint_x = 1)
            if abcd == 1 :
                self.btnK = Button(background_down = self.images + "K.png" ,size_hint_y=None,height = 250  , background_normal = self.images + 'K.png', background_color = (1,1,1,1))
                self.btnO = Button(background_down = self.images + "O.png" ,size_hint_y=None, height = 250 , background_normal = self.images + 'O.png', background_color = (1,1,1,1))
                self.layout.add_widget(self.btnK)
                self.layout.add_widget(self.btnO)
                label_head = (
                '[color=ff0000][b]No encuentras \n tu Tienda Favorita?'
                '\n\n[color=#404040] Haznos una Sugerencia :)')
                self.label_12 = Label(text=label_head, font_size='15sp', halign = 'center', height = 100 ,size_hint_y=None,
                              markup=True)
                self.btnO_B = Button(background_down = self.images + "color_rojo.png" ,text = "[b]Hacer Sugerencia.",size_hint_y=None, height = 100 , background_normal = self.images + 'color_rojo.png', background_color = (1,1,1,1), markup = True)
                self.layout.add_widget(self.label_12)
                self.layout.add_widget(self.btnO_B)

                self.btnO_B.bind(on_press=self.sugerenciapopup.open)
                self.tiendas = Button(background_down = self.images + "blanco.png" ,text="[color=#404040]Directorio", halign = 'center', height = 70 ,size_hint_y=None,markup=True, font_size = 24, background_normal = self.images + 'blanco.png', background_color = (1,1,1,1))

                self.tiendas_txt = Button(background_down = self.images + "blanco.png" ,text = "",size_hint_y=None, height = 70 , background_normal = self.images + 'blanco.png', background_color = (1,1,1,1), markup = True)

                self.layout.add_widget(self.tiendas)
                self.layout.add_widget(self.tiendas_txt)


            if i["estado"] == "Activo":
                btn3 = Button(background_down = self.images + "roro.png" ,size_hint_y=0.025 , background_normal = self.images + 'roro.png', background_color = (1,1,1,1))
                btn4 = Button(background_down = self.images + "roro2.png" ,size_hint_y=0.025 , background_normal = self.images + 'roro2.png', background_color = (1,1,1,1))
                btn6 = Button(background_down = self.images + "asd.png" ,size_hint_y= None ,height=25, background_normal = self.images + 'asd.png', background_color = (1,1,1,1))
                btn0 = Image(size_hint_y=0.4, height=300, source = self.images + '404.png')
                btn1 = Button(background_down = self.images + "blanco.png" ,text='[b][color=#404040] ' + i["nombre"], size_hint_y=0.1, height=30, background_normal = self.images + 'blanco.png', background_color = (1,1,1,1), markup = True , font_size = 18,valign = 'top')
                btn5 = Button(background_down = self.images + "blanco.png" ,text='', size_hint_y=0.050, height=30, background_normal = self.images + 'blanco.png', background_color = (1,1,1,1), markup = True , font_size = '15sp')
                btn = Button(background_down = self.images + "color_rojoB.png" ,text="[color=#ed1d27]"+str(i['id'])+"[/color]"+'>' , size_hint_y=0.2, size_hint_x = 0.2, height=70, background_normal = self.images + 'color_rojo.png', markup = True, font_size = 23)
                categoria_save = self.categorias[(i["categoria"])-1]
                btn2 = Button(background_down = self.images + "blanco.png" ,text='[color=#404040][b] ' + categoria_save , size_hint_y=0.1, height=30, background_normal = self.images + 'blanco.png',background_color = (1,1,1,1), markup   = True, font_size = 18)
                name = btn.text

                #btn.bind(on_press= lambda name=name: printR(name.text))
                integer =i["id"]
                seleccionado = self.Lista_Contactos_IDs[int(integer)-1]
                print btn.text[15:-9]
                btn.bind(on_press=lambda seleccionado=seleccionado: self.TIENDA(seleccionado.text[15:-9]))

                a.add_widget(btn6)
                a.add_widget(btn0)
                a.add_widget(btn1)
                a.add_widget(btn3)
                a.add_widget(btn2)
                a.add_widget(btn4)
                a.add_widget(btn5)
                a.add_widget(btn)
                self.layout.add_widget(a)
            else:
                pass
                
    def CREARCATEGORIA(self,categoria):
        try:
            id = len(self.Categoriatable)+1
            data = {
                "id": id,
                "categoria": categoria,
                "creada_por": self.UserU
            }
                        
            req = urllib2.Request(self.Dominio2+"Categoria/")
            req.add_header('Content-Type', 'application/json')
            response = urllib2.urlopen(req, json.dumps(data))
            print("Categoria creada con exito.")
            self.crearcategoriapopup.dismiss()
        except:
            print("ha ocurrido un error.")
            
    def CREARCONTACTO(self,a,b,c,d):
        try:
            id = len(self.Contactotable)+1
            data = {
            "id": id,
            "nombre": a,
            "telefono": b,
            "direccion": c,
            "categoria": d
        }
                        
            req = urllib2.Request(self.Dominio2+"Contacto/")
            req.add_header('Content-Type', 'application/json')
            response = urllib2.urlopen(req, json.dumps(data))
            print("Contacto creado con exito.")
            self.Crearcontactopopup.dismiss()
        except:
            print("ha ocurrido un error.")
            
    def CREARMENU(self,button):

        print "asdasdasd"
        id = len(self.Menutable)+1
        print id
        print self.Lista_Contactos_Nombres
        print self.crearmenu_TextInput4.text
        self.guardado03 = self.Lista_Contactos_Nombres.index(self.crearmenu_TextInput4.text)
        print self.guardado03
        self.guardado04 = int(self.Lista_Contactos_IDs[int(self.guardado03)])
        print self.guardado04
        
        
        data = {
        "id": (id + 1),
        "menu_titulo": self.crearmenu_TextInput1.text,
        "categoria": self.crearmenu_TextInput2.text,
        "creado_por": self.crearmenu_TextInput3.text,
        "fecha_creacion": str(time.strftime("%d/%m/%Y")),
        "contacto": int(self.guardado04 + 1)

        }
        print data
        req = urllib2.Request(self.Dominio2+"Menu/")
        req.add_header('Content-Type', 'application/json')
        response = urllib2.urlopen(req, json.dumps(data))
        print("Menu creado con exito.")
        self.crearmenupopup.dismiss()

            
    def CREARSUGERENCIA(self,a,b,c,d):
        try:
            data = { "nombre": a,"categoria": d, "telefono": "+1"+b,"direccion": c,"sugerido_por": self.UserID }
            print(str(self.sugerencia_TextInput2.text))            
            req = urllib2.Request(self.Dominio2+"Sugerencia/")
            req.add_header('Content-Type', 'application/json')
            response = urllib2.urlopen(req, json.dumps(data))
            print("Sugerencia creada con exito.")
        except:
            print("ha ocurrido un error.")     
            
    def CREARRATING(self,a):
        try:
            data = { "id": self.RatingNO + 1,"categoria": "Comida Rapida","comentario":self.a_E_Input.text, "valor_rating": 8 ,"rating_por": self.UserU,"contacto": self.TiendaSolicitada }
            #print(str(self.sugerencia_TextInput2.text))            
            req = urllib2.Request(self.Dominio2+"Rating/")
            req.add_header('Content-Type', 'application/json')
            response = urllib2.urlopen(req, json.dumps(data))
            
            url = self.Dominio2 + "Rating/"
            json_obj = urllib2.urlopen(url)
            Datos_Tabla = json.load(json_obj)
            self.Ratingtable = Datos_Tabla
            self.RatingNO = len(Datos_Tabla)
            self.TIENDA(self.TiendaSolicitada)
            self.main_panel.scroll_y = 0
            print("Comentario creado con exito.")
        except:
            print("ha ocurrido un error.")
            
    def DEPARTAMENTOS(self, button):
        for i in self.panelesformularios:
            try:
               self.main_panel.remove_widget(i)
               self.main_panel.add_widget(self.panel_deptartamentos_root) 
            except:
                pass
                
                
    def MENU_ADMINISTRADOR(self, button):
        for i in self.panelesformularios:
            try:
               self.main_panel.remove_widget(i)
               self.main_panel.add_widget(self.menu_Administrador_root) 
            except:
                pass
   
                
    def ADMINISTRAR_USUARIOS(self, button):
        for i in self.panelesformularios:
            try:
               self.main_panel.remove_widget(i)
               self.main_panel.add_widget(self.panel_Administrador_root) 
            except:
                pass
               
    def ADMINISTRAR_INVITADOS(self, button):
        for i in self.panelesformularios:
            try:
               self.main_panel.remove_widget(i)
               self.main_panel.add_widget(self.panel2_Administrador_root) 
            
            except:
                pass
                
    def ADMINISTRAR_USUARIO(self,id):
        for i in self.panelesformularios:
            try:
                
                self.main_panel.remove_widget(i)
                self.main_panel.add_widget(self.panel_Administrado_root)
            except:
                pass
                
        url = self.Dominio2+"" + "Usuario" + "/" + str(id) 
        json_obj = urllib2.urlopen(url)
        i = json.load(json_obj)
        print i
        self.vista_usuario2_perfil1B.text = "[color=#404040]"+i["usuario"]
        self.vista_usuario2_perfil2B.text = "[color=#404040]"+i["email"]
        self.vista_usuario2_perfil3B.text = "[color=#404040]"+i["fecha_registro"][:-17]
        self.vista_usuario2_perfil4B.text = "[color=#404040]"+i["ultimo_ingreso"][:-17]
        self.vista_usuario2_perfil5B.text = "[color=#404040]"+str(i["id"])
        self.vista_usuario2_perfil6B.text = "[color=#404040]"+i["privilegios"]

    def TIENDA(self, integer):
        try:
            self.panel_busqueda.dismiss()
        except:
            pass
        self.perfil_tienda.clear_widgets()
        self.TiendaSolicitada = integer
        print (""*5)
        a = 0
        guardad00001 = 0
        iguales = 0
        self.guardado01 = integer
        for i in self.Menutable:
            if integer == str(i['contacto']):
                iguales = iguales + 1
        try:
            for i in self.Menutable:
                if integer == str(i['contacto']):
                    print ("son iguales")
                    if a == 0 :
                        for i in self.Lista_Contactos_IDs:
                            print str(integer) + "-------"
                            print str(i) + "------"
                            if str(integer) == str(i):
                                guardad00001 = self.Lista_Contactos_IDs.index(i)
                                print str(guardad00001) + "ASDADASD"
                                
                          
                        self.cajasB = GridLayout(cols=1, spacing=0, size_hint_y=None, height = 250 , size_hint_x = 1)
                        self.cajas_dobles = GridLayout(cols=2, spacing = 0, size_hint_y = None , height= 50 , size_hint_x =1 )
                        self.cajas_dobles2 = GridLayout(cols=2, spacing = 0, size_hint_y = None , height= 50 , size_hint_x =1 )
                        self.cajasB.bind(minimum_height=self.cajasB.setter('height'))
                        self.cajas_dobles.bind(minimum_height=self.cajas_dobles.setter('height'))
                        self.perfil_tienda.bind(minimum_height=self.perfil_tienda.setter('height'))
                        caja_S1 = Button(background_down = self.images + "color_rojo.png" ,size_hint = (1,None), height = 50, text = "[color=#404040] Spoiler", markup = True, background_color = (1,1,1,1), background_normal = self.images + 'color_rojo.png', font_size = 24 )
                        caja_S2 = Button(background_down = self.images + "color_rojo.png" ,size_hint = (1,None), height = 50, text = "[color=#404040]", markup = True, background_color = (1,1,1,1), background_normal = self.images + 'color_rojo.png')
                        caja_S3 = Button(background_down = self.images + "blanco2.png" ,size_hint = (1,None), height = 50, text = "[color=#404040] Horario :", markup = True, background_color = (1,1,1,1), background_normal = self.images + 'blanco2.png')
                        caja_S4 = Button(background_down = self.images + "blanco2.png" ,size_hint = (1,None), height = 50, text = "[color=#404040] Lun - Sab, 7 AM - 10 PM", markup = True, background_color = (1,1,1,1), background_normal = self.images + 'blanco2.png')
                        caja_S5 = Button(background_down = self.images + "blanco2.png" ,size_hint = (1,None), height = 50, text = "[color=#404040] Domicilio :", markup = True, background_color = (1,1,1,1), background_normal = self.images + 'blanco2.png')
                        caja_S6 = Button(background_down = self.images + "blanco2.png" ,size_hint = (1,None), height = 50, text = "[color=#404040] Disponible", markup = True, background_color = (1,1,1,1), background_normal = self.images + 'blanco2.png')
                        caja_S7 = Button(background_down = self.images + "blanco2.png" ,size_hint = (1,None), height = 50, text = "[color=#404040] Pagos Disponibles :", markup = True, background_color = (1,1,1,1), background_normal = self.images + 'blanco2.png')
                        caja_S8 = Button(background_down = self.images + "blanco2.png" ,size_hint = (1,None), height = 50, text = "[color=#404040] Contra Entrega o Targeta.", markup = True, background_color = (1,1,1,1), background_normal = self.images + 'blanco2.png')
                        caja_S9 = Button(background_down = self.images + "blanco2.png" ,size_hint = (1,None), height = 50, text = "[color=#404040] Rating :", markup = True, background_color = (1,1,1,1), background_normal = self.images + 'blanco2.png')
                        caja_S10 = Button(background_down = self.images + "blanco2.png" ,size_hint = (1,None), height = 50, text = "[color=#404040] 10.0", markup = True, background_color = (1,1,1,1), background_normal = self.images + 'blanco2.png')
                        caja_S11 = Button(background_down = self.images + "blanco2.png" ,size_hint = (1,None), height = 50, text = "[color=#404040]", markup = True, background_color = (1,1,1,1), background_normal = self.images + 'blanco2.png')
                        caja_S12 = ToggleButton(background_down = self.images + "blanco2.png" ,size_hint = (1,None), height = 50, text = "[color=#404040]Me Gusta", markup = True, background_color = (1,1,1,1), background_normal = self.images + 'blanco2.png')

                        def cambias(self):
                            if caja_S12.text == ("[color=#404040]Me Gusta"):
                                caja_S12.text = "[b][color=#ff1a1a]Me Gusta"
                            else:
                                caja_S12.text = "[color=#404040]Me Gusta"
                            
                            
                        caja_S12.bind(on_press = cambias)
                        
                        self.cajas_dobles.add_widget(caja_S1)
                        self.cajas_dobles.add_widget(caja_S2)
                        self.cajas_dobles.add_widget(caja_S9)
                        self.cajas_dobles.add_widget(caja_S10)
                        self.cajas_dobles.add_widget(caja_S3)
                        self.cajas_dobles.add_widget(caja_S4)
                        self.cajas_dobles.add_widget(caja_S5)
                        self.cajas_dobles.add_widget(caja_S6)
                        self.cajas_dobles.add_widget(caja_S7)
                        self.cajas_dobles.add_widget(caja_S8)
                        self.cajas_dobles.add_widget(caja_S11)
                        self.cajas_dobles.add_widget(caja_S12)

                        caja_B1 = Image(source = self.images + "Tienda.png", size_hint_y = None , height = 250)
                        caja_B2 = Button(background_down = self.images + "blanco2.png" ,size_hint = (1,None), height = 50, text = "[color=#404040]"+ self.Lista_Contactos_Nombres[guardad00001], markup = True, background_color = (1,1,1,1), background_normal = self.images + 'blanco2.png', font_size = 24 )
                        caja_B3 = Button(background_down = self.images + "blanco2.png" ,size_hint = (1,None), height = 50, text = "[color=#404040]", markup = True, background_color = (1,1,1,1), background_normal = self.images + 'blanco2.png')
                        self.caja_B10 = Button(text = "[color=#404040]Editar Contacto[color=#000000]"+str(self.guardado01), background_down = self.images + "blanco.png" ,size_hint = (1,None), height = 50, markup = True, background_color = (1,1,1,1), background_normal = self.images + 'blanco.png', font_size = 24)
                        
                        self.cajas_dobles.add_widget(caja_B2)
                        self.cajas_dobles.add_widget(caja_B3)
                        self.caja_B10.bind(on_press = self.ADMTIENDA)

                        self.cajasB.add_widget(caja_B1)
                        if self.UserPriv == "Administrador":
                            self.cajasB.add_widget(self.caja_B10)
                            
                        self.cajasB.add_widget(self.cajas_dobles)
                        self.perfil_tienda.add_widget(self.cajasB)


                        caja_B4 = Button(background_down = self.images + "color_rojo.png" ,size_hint = (1,None), height = 50, text = "Recomendados", markup = True, background_color = (1,1,1,1), background_normal = self.images + 'color_rojo.png', font_size = 24 )
                        caja_B5 = Button(background_down = self.images + "color_rojo.png" ,size_hint = (1,None), height = 50, text = "[color=#404040]""", markup = True, background_color = (1,1,1,1), background_normal = self.images + 'color_rojo.png')
                        self.cajas_dobles.add_widget(caja_B4)
                        self.cajas_dobles.add_widget(caja_B5)


                    elif a == 5:

                        caja_B6 = Button(background_down = self.images + "color_rojo.png" ,size_hint = (1,None), height = 50, text = " Tienda Completa", markup = True, background_color = (1,1,1,1), background_normal = self.images + 'color_rojo.png', font_size = 24 )
                        caja_B7 = Button(background_down = self.images + "color_rojo.png" ,size_hint = (1,None), height = 50, text = "[color=#404040]", markup = True, background_color = (1,1,1,1), background_normal = self.images + 'color_rojo.png')
                        caja_B8 = Button(background_down = self.images + "blanco.png" ,size_hint = (1,None), height = 50, text = "[color=#ff0000][b] Buscas algo?", markup = True, background_color = (1,1,1,1), background_normal = self.images + 'blanco.png', font_size = '15sp' )
                        caja_B9 = Button(background_down = self.images + "blanco.png" ,size_hint = (.1,None), height = 50, text = "[color=#404040][b] Has una Busqueda :)", markup = True, background_color = (1,1,1,0), background_normal = self.images + 'blanco.png', font_size = '15sp')
                        self.cajas_dobles.add_widget(caja_B6)
                        self.cajas_dobles.add_widget(caja_B7)
                        self.cajas_dobles.add_widget(caja_B8)
                        self.cajas_dobles.add_widget(caja_B9)

                    else:
                        contador_o = 0
                        for x in self.MenuSCtable:
                            if i['contacto'] == x['contacto_id']:
                                for g in x['menu']:
                                    contador_o += 1
                                    if i['id'] == g:
                                        caja_B4 = Button(background_down = self.images + "blanco.png" ,size_hint = (1,None), height = 50, text = "[color=#404040]"+x['sub_categoria'], markup = True, background_color = (1,1,1,1), background_normal = self.images + 'blanco.png', font_size = 24 )
                                        caja_B5 = Button(background_down = self.images + "blanco.png" ,size_hint = (1,None), height = 50, text = "[color=#404040]""", markup = True, background_color = (1,1,1,1), background_normal = self.images + 'blanco.png')
                                        self.cajas_dobles.add_widget(caja_B4)
                                        self.cajas_dobles.add_widget(caja_B5)
                                        iguales11 = 0
                                        for z in self.PlatoTable:
                                            if z ['sub_categoria'] == x['id']:
                                                iguales11 += 1
                                                
                                        for z in self.PlatoTable:
                                            if z ['sub_categoria'] == x['id']:
                                                a_E = GridLayout(cols=1, spacing=0, size_hint_y=None, height = 410 , size_hint_x = 1)
                                                btn3_E = Button(background_down = self.images + "roro.png" ,size_hint_y=0.025 , background_normal = self.images + 'roro.png', background_color = (1,1,1,1))
                                                btn4_E = Button(background_down = self.images + "roro2.png" ,size_hint_y=0.025 , background_normal = self.images + 'roro2.png', background_color = (1,1,1,1))
                                                btn6_E = Button(background_down = self.images + "asd.png" ,size_hint_y= None ,height=25, background_normal = self.images + 'asd.png', background_color = (1,1,1,1))
                                                btn0_E = Image(source = self.images + "404.png" ,text='', size_hint_y=0.400, height=100, background_normal = self.images + '404.png')
                                                btn1_E = Button(background_down = self.images + "blanco.png" ,text='[b][color=#404040]'+ z['plato'], size_hint_y=0.1, height=30, background_normal = self.images + 'blanco.png', background_color = (1,1,1,1), markup = True , font_size = 18,valign = 'top')
                                                btn5_E = Button(background_down = self.images + "blanco.png" ,text='', size_hint_y=0.050, height=30, background_normal = self.images + 'blanco.png', background_color = (1,1,1,1), markup = True , font_size = '15sp')
                                           
                                                btn_E = Button(background_down = self.images + "color_rojo.png" ,text="[color=#ed1c24]"+str(self.inventario_id[int(z['plato_id']-1)])+'[/color]'+'+' , size_hint_y=0.2, size_hint_x = 0.2, height=70, background_normal = self.images + 'color_rojo.png', markup = True)
                                                btn2_E = Button(background_down = self.images + "blanco.png" ,text='[color=#404040][b]'+ z['precio'] + ' RD$' , size_hint_y=0.1, height=30, background_normal = self.images + 'blanco.png',background_color = (1,1,1,1), markup   = True, font_size = 18)
                                                name_E = btn_E.text
                                                btn_E.bind(on_press= lambda name_E=name_E: self.INSERTAR_in_PEDIDO(name_E.text[15:-9], self.guardado01))

                                                a_E.add_widget(btn6_E)
                                                a_E.add_widget(btn0_E)
                                                a_E.add_widget(btn1_E)
                                                a_E.add_widget(btn3_E)
                                                a_E.add_widget(btn2_E)
                                                a_E.add_widget(btn4_E)
                                                a_E.add_widget(btn5_E)
                                                a_E.add_widget(btn_E)
                                                self.cajas_dobles.add_widget(a_E)
                                                
                                        if(iguales11%2==0):
                                            pass
                                        else:
                                            print(str(a)+" es impar")
                                            a_D = GridLayout(cols=1, spacing=0, size_hint_y=None, height = 410 , size_hint_x = 1)
                                            btn3_D = Button(background_down = self.images + "roro.png" ,size_hint_y=0.025 , background_normal = self.images + 'roro.png', background_color = (1,1,1,1))
                                            btn4_D = Button(background_down = self.images + "roro2.png" ,size_hint_y=0.025 , background_normal = self.images + 'roro2.png', background_color = (1,1,1,1))
                                            btn6_D = Button(background_down = self.images + "asd.png" ,size_hint_y= None ,height=25, background_normal = self.images + 'asd.png', background_color = (1,1,1,1))
                                            btn0_D = Image(source = self.images + "404.png" ,text='', size_hint_y=0.400, height=100, background_normal = self.images + '404.png')
                                            btn1_D = Button(background_down = self.images + "blanco.png" ,text='[b][color=#404040]'+ "Espacio publicitario", size_hint_y=0.1, height=30, background_normal = self.images + 'blanco.png', background_color = (1,1,1,1), markup = True , font_size = 18,valign = 'top')
                                            btn5_D = Button(background_down = self.images + "blanco.png" ,text='', size_hint_y=0.050, height=30, background_normal = self.images + 'blanco.png', background_color = (1,1,1,1), markup = True , font_size = '15sp')
                                            btn_C = Button(background_down = self.images + "color_rojo.png" ,text="[color=#ed1c24]"+str(1)+'[/color]'+'+' , size_hint_y=0.2, size_hint_x = 0.2, height=70, background_normal = self.images + 'color_rojo.png', markup = True)
                                            btn2_D = Button(background_down = self.images + "blanco.png" ,text='' , size_hint_y=0.1, height=30, background_normal = self.images + 'blanco.png',background_color = (1,1,1,1), markup   = True, font_size = 18)
                                            name_D = btn_C.text
                                            btn_C.bind(on_press= lambda name_D=name_D: self.INSERTAR_in_PEDIDO(name_D.text[15:-9],self.guardado01))

                                            a_D.add_widget(btn6_D)
                                            a_D.add_widget(btn0_D)
                                            a_D.add_widget(btn1_D)
                                            a_D.add_widget(btn3_D)
                                            a_D.add_widget(btn2_D)
                                            a_D.add_widget(btn4_D)
                                            a_D.add_widget(btn5_D)
                                            a_D.add_widget(btn_C)
                                            self.cajas_dobles.add_widget(a_D)
                                                
                                                
                                            

                                        
                    a = a + 1
                    print str(a)
                    print str(iguales)
                    
                    if a == iguales:
                        if(iguales%2==0):
                            print(str(a)+" es par")
                            a_D = GridLayout(cols=1, spacing=0, size_hint_y=None, height = 410 , size_hint_x = 1)
                            btn3_D = Button(background_down = self.images + "roro.png" ,size_hint_y=0.025 , background_normal = self.images + 'roro.png', background_color = (1,1,1,1))
                            btn4_D = Button(background_down = self.images + "roro2.png" ,size_hint_y=0.025 , background_normal = self.images + 'roro2.png', background_color = (1,1,1,1))
                            btn6_D = Button(background_down = self.images + "asd.png" ,size_hint_y= None ,height=25, background_normal = self.images + 'asd.png', background_color = (1,1,1,1))
                            btn0_D = Image(source = self.images + "404.png" ,text='', size_hint_y=0.400, height=100, background_normal = self.images + '404.png')
                            btn1_D = Button(background_down = self.images + "blanco.png" ,text='[b][color=#404040]'+ "Espacio publicitario", size_hint_y=0.1, height=30, background_normal = self.images + 'blanco.png', background_color = (1,1,1,1), markup = True , font_size = 18,valign = 'top')
                            btn5_D = Button(background_down = self.images + "blanco.png" ,text='', size_hint_y=0.050, height=30, background_normal = self.images + 'blanco.png', background_color = (1,1,1,1), markup = True , font_size = '15sp')
                            btn_C = Button(background_down = self.images + "color_rojo.png" ,text="[color=#ed1c24]"+str(1)+'[/color]'+'+' , size_hint_y=0.2, size_hint_x = 0.2, height=70, background_normal = self.images + 'color_rojo.png', markup = True)
                            btn2_D = Button(background_down = self.images + "blanco.png" ,text='' , size_hint_y=0.1, height=30, background_normal = self.images + 'blanco.png',background_color = (1,1,1,1), markup   = True, font_size = 18)
                            name_D = btn_C.text
                            btn_C.bind(on_press= lambda name_D=name_D: self.INSERTAR_in_PEDIDO(name_D.text[15:-9],self.guardado01))

                            #a_D.add_widget(btn6_D)
                            #a_D.add_widget(btn0_D)
                            #a_D.add_widget(btn1_D)
                            #a_D.add_widget(btn3_D)
                            #a_D.add_widget(btn2_D)
                            #a_D.add_widget(btn4_D)
                            #a_D.add_widget(btn5_D)
                            #a_D.add_widget(btn_C)
                            #self.cajas_dobles.add_widget(a_D)
                        else:
                            pass
                    
 
                        
                        abcd = 0
                        
                        for i in self.Ratingtable:
                            abcd = abcd + 1
                            if abcd == 1:
                                self.Galeria_horizontal = ScrollView(size_hint=(1, None), height = 410)
                                self.Form1_ABC_Grid = GridLayout(cols = 0,width = 0, size_hint = (None,None), height =410)
                                self.Galeria_horizontal.add_widget(self.Form1_ABC_Grid)
                                self.cajasB.add_widget(self.Galeria_horizontal)
                                a_D_caja_S1 = Button(background_down = self.images + "color_rojo.png" ,size_hint = (1,None), height = 50, text = "[color=#404040] Comentarios", markup = True, background_color = (1,1,1,1), background_normal = self.images + 'color_rojo.png', font_size = 24 )
                                a_D_caja_S2 = Button(background_down = self.images + "color_rojo.png" ,size_hint = (1,None), height = 50, text = "[color=#404040]", markup = True, background_color = (1,1,1,1), background_normal = self.images + 'color_rojo.png')
                                self.cajasB.add_widget(a_D_caja_S1)
                                #self.cajasB.add_widget(a_D_caja_S2)
                            if i["contacto"] == int(self.guardado01):  
                                a_H = GridLayout(cols = 2 , size_hint_y = None, height = 150 , size_hint_x = 1)
                                a_D = GridLayout(cols=1, spacing=0, size_hint_y=None, height = 150 , size_hint_x = 1)
                                a_H_Perfil = Image(allow_stretch =True , keep_ratio = False,size_hint_x = None, width = 75,source = self.images + "user.png" ,text='', size_hint_y=None, height=75, background_normal = self.images + '404.png')
                                a_H_Perfil_Grid = GridLayout(cols = 1 , size_hint_y = 1, size_hint_x = None, width = 75)
                                a_H_Perfil_Grid2 = GridLayout(cols = 2 , size_hint_y = 1, size_hint_x = None, width = 85)
                                a_H_Perfil_L1 = Label(size_hint_y = None, height = 82)
                                a_H_Perfil_L2 = Label()
                                
                                
                                a_D_Label1 = Label(size_hint_x = None, width = 100,text ="[color=#ff4d4d][b]"+i["rating_por"] , size_hint_y = None, height = 25, markup = True)
                                a_D_Label2 = Label()
                                a_D_Label3 = Label()
                                a_D_LabelGrid = GridLayout(cols = 2, size_hint_y = None, height = 30)
                                textoo = "Me parece increible, esta aplicacion facilita mucho la manera en la que se hacen las cosas, nunca lo habia echo tan rapido y con tanto estilo."

                                a_D_Input = TextInput(padding = [30,20,0,0],disabled = True,text = i["comentario"] ,size_hint_y = 1 , Readonly = True , Line_Spacing = 3, background_normal = self.images + "blanco.png" , background_color = (1,1,1,1), font_size = '13sp', background_disabled_normal = self.images + "blanco .png", disabled_foreground_color = (0,0,0,.6))
                                
                                a_D_Label1_Grid = GridLayout(cols = 2, size_hint_y = None, height = 30, size_hint_x = None, width = 200)
                                estrellas = GridLayout(cols = 6 ,size_hint_x = None, width = 100, spacing = 2)
                                
                                estrella1 = Image(source = self.images + "51.png", size_hint_x = None, width = 20)
                                estrella2 = Image(source = self.images + "51.png", size_hint_x = None, width = 20)
                                estrella3 = Image(source = self.images + "51.png", size_hint_x = None, width = 20)
                                estrella4 = Image(source = self.images + "51.png", size_hint_x = None, width = 20)
                                estrella5 = Image(source = self.images + "51.png", size_hint_x = None, width = 20)
                                AX7 = Label()
                                
                                if i['valor_rating'] < 10:
                                    estrella1.size = (0,0)
                                    estrella1.size_hint = (None,None)
                                    
                                                                
                                if i['valor_rating'] < 8:
                                    estrella2.size = (0,0)
                                    estrella2.size_hint = (None,None)
                                        
                                if i['valor_rating'] < 6:
                                    estrella3.size = (0,0)
                                    estrella3.size_hint = (None,None)
                                    
                                                                
                                if i['valor_rating'] < 4:
                                    estrella4.size = (0,0)
                                    estrella4.size_hint = (None,None)
                                    
                                                                
                                if i['valor_rating'] < 2:
                                    estrella5.size = (0,0)
                                    estrella5.size_hint = (None,None)
                                    
                                
                                estrellas.add_widget(estrella1)
                                estrellas.add_widget(estrella2)
                                estrellas.add_widget(estrella3)
                                estrellas.add_widget(estrella4)
                                estrellas.add_widget(estrella5)
                                estrellas.add_widget(AX7)
                                
                                a_D_Label1_Grid.add_widget(a_D_Label1)
                                a_D_Label1_Grid.add_widget(estrellas)
                                
                                
                                a_D_LabelGrid.add_widget(a_D_Label1_Grid)
                                a_D_LabelGrid.add_widget(a_D_Label2)
                                
                                a_D.add_widget(a_D_Label3)
                                a_D.add_widget(a_D_LabelGrid)
                                a_D.add_widget(a_D_Input)
                                
                                a_H_Perfil_Grid.add_widget(a_H_Perfil_L1)
                                a_H_Perfil_Grid.add_widget(a_H_Perfil)
                                
                                
                                #a_H_Perfil_Grid.add_widget(a_H_Perfil_L2)
                                AX6 = Label(size_hint_x = None , width = 10)
                                a_H_Perfil_Grid2.add_widget(AX6)
                                a_H_Perfil_Grid2.add_widget(a_H_Perfil_Grid)
                                a_H.add_widget(a_H_Perfil_Grid2)
                                
                                a_H.add_widget(a_D)
                                self.cajasB.add_widget(a_H)

                        a_E = GridLayout(cols=1, spacing=0, size_hint_y=None, height = 150 , size_hint_x = 1)

                        self.a_E_Input = TextInput(text = "" ,size_hint_y = 0.75 , Readonly = True , Line_Spacing = 3, background_normal = self.images + "blanco3.png" , background_color = (1,1,1,1), font_size = '13sp')

                        a_E_Label1 = Label(text ="[color=#404040]Que te ha parecido esta tienda?" , size_hint_y = 0.25, markup = True)

                        a_E.add_widget(a_E_Label1)
                        a_E.add_widget(self.a_E_Input)

                        self.cajasB.add_widget(a_E)
                        a_D = GridLayout(cols=1, spacing=0, size_hint_y=None, height = 70 , size_hint_x = 1)
                        a_D_Button1 = Button(text = "Listo")
                        a_D_Button1.bind(on_press = self.CREARRATING)
                            
                        a_D.add_widget(a_D_Button1)
                        self.cajasB.add_widget(a_D)
                        
                        a_D_caja_S3 = Button(background_down = self.images + "color_rojo.png" ,size_hint = (1,None), height = 50, text = "[color=#404040] Otras Tiendas", markup = True, background_color = (1,1,1,1), background_normal = self.images + 'color_rojo.png', font_size = 24 )
                        a_D_caja_S4 = Button(background_down = self.images + "color_rojo.png" ,size_hint = (1,None), height = 50, text = "[color=#404040]", markup = True, background_color = (1,1,1,1), background_normal = self.images + 'color_rojo.png')
                        self.cajas_dobles.add_widget(a_D_caja_S3)
                        self.cajas_dobles.add_widget(a_D_caja_S4)

                        for y in self.Contactotable:
                            print y
                            abcd += 1
                            print y["categoria"]
                            print self.Lista_Contactos_Categorias[int(guardad00001)]    
                            if y["categoria"] == int(self.Lista_Contactos_Categorias[int(guardad00001)]):
                                a2 = GridLayout(cols=1, spacing=0, size_hint_y=None, height = 410 , size_hint_x = None, width = 300)
                            
                                btnB3 = Button(background_down = self.images + "roro.png" ,size_hint_y=0.025 , background_normal = self.images + 'roro.png', background_color = (1,1,1,1))
                                btnB4 = Button(background_down = self.images + "roro2.png" ,size_hint_y=0.025 , background_normal = self.images + 'roro2.png', background_color = (1,1,1,1))
                                btnB6 = Button(background_down = self.images + "asd.png" ,size_hint_y= None ,height=25, background_normal = self.images + 'asd.png', background_color = (1,1,1,1))
                                btnB0 = Image(source = self.images + "404.png" ,text='', size_hint_y=0.400, height=100, background_normal = self.images + '404.png')
                                btnB1 = Button(background_down = self.images + "blanco.png" ,text='[b][color=#404040] ' + y["nombre"], size_hint_y=0.1, height=30, background_normal = self.images + 'blanco.png', background_color = (1,1,1,1), markup = True , font_size = 18,valign = 'top')
                                btnB5 = Button(background_down = self.images + "blanco.png" ,text='', size_hint_y=0.050, height=30, background_normal = self.images + 'blanco.png', background_color = (1,1,1,1), markup = True , font_size = '15sp')
                                btnB = Button(background_down = self.images + "color_rojoB.png" ,text="[color=#ed1d27]"+str(y['id'])+"[/color]"+'>' , size_hint_y=0.2, size_hint_x = 0.2, height=70, background_normal = self.images + 'color_rojo.png', markup = True, font_size = 23)
                                categoria_save = self.categorias[(y["categoria"])-1]
                                btnB2 = Button(background_down = self.images + "blanco.png" ,text='[color=#404040][b] ' + categoria_save , size_hint_y=0.1, height=30, background_normal = self.images + 'blanco.png',background_color = (1,1,1,1), markup   = True, font_size = 18)
                                name = btnB.text

                                #btnB.bind(on_press= lambda name=name: printR(name.text))
                                integer =y["id"]
                                seleccionado = self.Lista_Contactos_IDs[int(integer)-1]
                                print btnB.text[15:-9]
                                btnB.bind(on_press=lambda seleccionado=seleccionado: self.TIENDA(seleccionado.text[15:-9]))

                                a2.add_widget(btnB6)
                                a2.add_widget(btnB0)
                                a2.add_widget(btnB1)
                                a2.add_widget(btnB3)
                                a2.add_widget(btnB2)
                                a2.add_widget(btnB4)
                                a2.add_widget(btnB5)
                                a2.add_widget(btnB)
                                self.Form1_ABC_Grid.cols += 1
                                self.Form1_ABC_Grid.width += 300
                                self.Form1_ABC_Grid.add_widget(a2)
                                
                                
                                print "agregado"
                                

                    

        except IOError as e:
            print "I/O error({0}): {1}".format(e.errno, e.strerror)
        except ValueError:
            print "Could not convert data to an integer."
        except:
            raise


        for i in self.panelesformularios:
            try:
               #i.do_scroll_y = True
               print "TIEMNDA"
               #i.update_from_scroll(*largs)
               #self.perfil_tienda.scroll_to(caja_B1, padding=10, animate=True)
               
               #self.perfil_tienda.scroll_type = ["content","bars"]
               #self.perfil_tienda.scroll_y = 0
               self.main_panel.remove_widget(i)
               self.main_panel.add_widget(self.perfil_tienda) 
               self.main_panel.scroll_y = 1
            except:
                pass

    def PERFIL(self, button):
        for i in self.panelesformularios:
            try:
               self.main_panel.remove_widget(i)
               self.main_panel.add_widget(self.panel_perfil_root) 
            except:
                pass
        self.panel_perfil.clear_widgets()
        url = self.Dominio2+"Usuario/" + str(self.UserID) + "/"
        json_obj = urllib2.urlopen(url)
        Datos_Tabla = json.load(json_obj)
        for i in self.botones_perfil:
            mascara = GridLayout(cols = 2, size_hint_y = None , height = 50)
            LABELMASK = GridLayout(cols = 1, size_hint_y = None , height = 350)
            if i == self.botones_perfil[0]:
                vista_usuario2_imagen = Button(background_normal = self.images + "PP.png" , background_color = (1,1,1,1))
                labelperfil = Button(text= "[b]PERFIL" , markup = True, font_size = 20 , background_color = (1,1,1,1) , size_hint_y = None, height = 50, background_normal = self.images + "color_rojo.png")
                #labelperfil_2 = Label(size_hint_y = None, height = 100)
                LABELMASK.add_widget(vista_usuario2_imagen)
                LABELMASK.add_widget(labelperfil)
                #mascara.add_widget(labelperfil_2)
                self.panel_perfil.add_widget(LABELMASK)
                
            
            label = Button(text = i + " :", background_color = (1,1,1,1), size_hint = (1,None), background_normal = self.images + "color_rojo.png" , height = 50)
            label1 = Button(text = "[color=#404040]"+ str(Datos_Tabla[i]) , markup = True , size_hint = (1, None), height = 50 , background_color = (1,1,1,1) , background_normal = self.images + "blanco2.png")
        
            mascara.add_widget(label)
            mascara.add_widget(label1)
            self.panel_perfil.add_widget(mascara)
            
                
    def CAMBIARPRIVILEGIO(self, id):
        try:
            url = self.Dominio2+"Usuario/" + self.vista_usuario2_perfil5B.text[15:] + "/"
            json_obj = urllib2.urlopen(url)
            Datos_Tabla = json.load(json_obj)
            data =   {
            "id": Datos_Tabla["id"],
            "usuario": Datos_Tabla["usuario"],
            "password": Datos_Tabla["password"],
            "email": Datos_Tabla["email"],
            "direccion": Datos_Tabla["direccion"],
            "privilegios": self.privilegiosB[int(id)],
            "fecha_registro": Datos_Tabla["fecha_registro"],
            "ultimo_ingreso": Datos_Tabla["ultimo_ingreso"],
            "verification_Id":Datos_Tabla["verification_Id"] 
            }
            self.vista_usuario2_perfil6B.text = "[color=#404040]"+self.privilegiosB[int(id)]
            req = urllib2.Request(url)
            req.add_header('Content-Type', 'application/json')
            req.get_method = lambda: 'PUT'
            response = urllib2.urlopen(req, json.dumps(data))
            self.panel_privilegio.dismiss()
        except:
            print("ERROR")
            
    def CAMBIARESTADO(self, id):
        #self.popup_5.open()
        id2 = self.vista_contacto1_perfil1B.text[15:]
        print id2
        
        url = self.Dominio2+"Contacto/" + str(id2) + "/"
        print url
        json_obj = urllib2.urlopen(url)
        Datos_Tabla = json.load(json_obj)
        if Datos_Tabla["estado"] == "Activo":
            data =   {
            "id": Datos_Tabla["id"],
            "nombre": Datos_Tabla["nombre"],
            "telefono": Datos_Tabla["telefono"],
            "direccion": Datos_Tabla["direccion"],
            "estado": "Desactivado",
            "categoria": Datos_Tabla["categoria"]
            }
            self.vista_contacto1_perfil5B.text = "[color=#404040]"+"Desactivado"
        else:
            data =   {
            "id": Datos_Tabla["id"],
            "nombre": Datos_Tabla["nombre"],
            "telefono": Datos_Tabla["telefono"],
            "direccion": Datos_Tabla["direccion"],
            "estado": "Activo",
            "categoria": Datos_Tabla["categoria"]
            }
            self.vista_contacto1_perfil5B.text = "[color=#404040]"+"Activo"

        
        req = urllib2.Request(url)
        req.add_header('Content-Type', 'application/json')
        req.get_method = lambda: 'PUT'
        response = urllib2.urlopen(req, json.dumps(data))
        #self.panel_privilegio.dismiss()
        



                
            #self.popup_5.dismiss()

    def PERFIL_TIENDA(self, button):
        for i in self.panelesformularios:
            try:
               self.main_panel.remove_widget(i)
               self.main_panel.add_widget(self.panel_tienda_perfil_root) 
            except:
                pass
                
    def CREAR_CATEGORIA(self, button):
        self.crearcategoriapopup.open()
        
    def SELFILTRO(self, button):
        self.SelFiltropopup.open()
    
    def SELFILTRO2(self, button):
        self.SelFiltro1popup.open()
           
    def CREAR_MENU_P(self, button):
        self.crearmenupopup.open()
        self.crearmenu_TextInput3.text = self.UserU
        
    def CONTACTOSPOPUP(self, button):
        self.Crearcontactopopup.open()
    
    def PINICIOPOPUP(self, button):
        self.Primerinicio_Layoutpopup.open()

    def PINICIOPOPUPCERRAR(self, button):
        self.Primerinicio_Layoutpopup.dismiss()
        
    def ANIDARPOPUP(self, button):
        self.Anidar_Layoutpopup.open()

    def ANIDARPOPUPCERRAR(self, button):
        self.Anidar_Layoutpopup.dismiss()

    def CAMBIARHORARIOPOPUP(self, button):
        self.CambiarHorariopopup.open()
        
        
    def SUGERENCIAS(self, button):
        for i in self.panelesformularios:
            try:
               self.main_panel.remove_widget(i)
               self.main_panel.add_widget(self.panel_Sugerencias_root) 
            except:
                pass
        
    def LISTADEPEDIDOS(self, button):
        contador99 = 0
        for i in self.list_adapter_temp.data:
            contador99 += 1
        if contador99 != 0:
            self.clear_widgets()
            self.add_widget(self.GL4)
        else:
            self.popup_3.open()

    def PANELDEBUSQUEDA(self, button):

            self.panel_busqueda.open()
            
    def PANELPRIVILEGIOS(self,button):
            self.panel_privilegio.open()

    def FACTURA_VISTA(self, button):
        contador99 = 0
        for i in self.list_adapter_temp.data:
            contador99 += 1
        if contador99 != 0:
            self.clear_widgets()
            self.add_widget(self.GL5)
        else:
            self.popup_3.open()

    def REGISTRAR_CONTACTO(self, button):
        self.clear_widgets()
        self.add_widget(self.GL6)

    def LISTA_CONTACTOS(self, button):
        self.clear_widgets()
        self.add_widget(self.GL7)

    def REGISTRAR_USUARIO(self, button):
        self.clear_widgets()
        self.add_widget(self.Registro_Usuario_root)

    def REGISTRAR_USUARIO_1(self, button):
        self.clear_widgets()
        self.add_widget(self.GL8_1)

    def REGISTRAR_USUARIO_2(self, button):
        self.clear_widgets()
        self.add_widget(self.GL8_2)

    def PEDIDOS(self, button):
        for i in self.panelesformularios:
            try:
               self.main_panel.remove_widget(i)
               self.main_panel.add_widget(self.panel_gl9_root) 
            except:
                pass
        abcd = 0
        for i in self.Pedidotable:
            if i["pedido_por"] == self.UserU:
                abcd += 1
                if abcd == 1:
                    self.BarraGL9_1 = Button(background_down = self.images + "blanco.png" ,text="[color=#404040]HISTORIAL DE PEDIDOS", size_hint_y = None , height = 70, background_color = (1,1,1,1), background_normal = self.images + "blanco.png", markup = True, font_size = 24)
                    self.BarraGL9_2 = Button(background_down = self.images + "blanco.png" ,text="", size_hint_y = None , height = 50, background_color = (1,1,1,0), background_normal = self.images + "blanco.png", font_size= 24, markup = True)
                    self.panel_gl9.add_widget(self.BarraGL9_1)
                    self.panel_gl9.add_widget(self.BarraGL9_2)
                    
                self.BarraGL9_3 = Button(background_down = self.images + "color_rojo.png" ,text=str(i["pedido_id"]), size_hint_y = None , height = 50, background_color = (1,1,1,1), background_normal = self.images + "color_rojo.png", font_size = 20)
                self.BarraGL9_4 = Button(background_down = self.images + "color_rojo.png" ,text=i["fecha_pedido"], size_hint_y = None , height = 50, background_color = (1,1,1,1), background_normal = self.images + "color_rojo.png", font_size = 20)
                self.panel_gl9.add_widget(self.BarraGL9_3)
                self.panel_gl9.add_widget(self.BarraGL9_4)
                
                string1 = i["descripcion_del_pedido"]
                string2 = i["categoria"]
                str3 = string1.split(",")
                self.PedidoRealizados[:]= []
                for i in str3:
                    print i.encode("utf-8 ")
                    self.PedidoRealizados.append(i.encode("utf-8 "))
                   
                
                print self.PedidoRealizados
                for y in self.PedidoRealizados:
                    for x in self.PlatoTable:
                        try:
                            guarda = int(y)
                            guarda2 = 1
                        except:
                            guarda1 = y.index("x")
                            guarda = y[:guarda1]
                            print guarda
                            try:
                                guardado1 = self.inventario_objetos.index(guarda)
                            except:
                                guardado1 = self.inventario_objetos.index(guarda[1:])
                            print guardado1
                            guarda = int(self.inventario_id[guardado1])      
                            print guarda
                            guarda2 = y[guarda1+1:]
                            print guarda2
                            
                        
                        if guarda == x["plato_id"]:
                            for i in range(int(guarda2)):
                                a_B_GL9 = GridLayout(cols=1, spacing=0, size_hint_y=None, height = 120 , size_hint_x = 1)
                                btn3_BGL9 = Button(background_down = self.images + "roro.png" ,size_hint_y=0.025 , background_normal = self.images + 'roro.png', background_color = (1,1,1,1))
                                btn4_BGL9 = Button(background_down = self.images + "roro2.png" ,size_hint_y=0.025 , background_normal = self.images + 'roro2.png', background_color = (1,1,1,1))
                                btn6_BGL9 = Button(background_down = self.images + "asd.png" ,size_hint_y= None ,height=25, background_normal = self.images + 'asd2.png', background_color = (1,1,1,1))
                                btn1_BGL9 = Button(background_down = self.images + "blanco.png" ,text='[b][color=#ff1a1a]'+ str(x["plato"]), size_hint_y=0.1, height=30, background_normal = self.images + 'blanco.png', background_color = (1,1,1,1), markup = True , font_size = 18,valign = 'top')
                                btn5_BGL9 = Button(background_down = self.images + "blanco.png" ,text='', size_hint_y=0.050, height=30, background_normal = self.images + 'blanco.png', background_color = (1,1,1,1), markup = True , font_size = '15sp')
                                btn2_BGL9 = Button(background_down = self.images + "blanco.png" ,text='[color=#404040][b]'+str(string2) , size_hint_y=0.1, height=30, background_normal = self.images + 'blanco.png',background_color = (1,1,1,1), markup   = True, font_size = 18)
                                
                                a_B_GL9.add_widget(btn6_BGL9)
                                a_B_GL9.add_widget(btn1_BGL9)
                                a_B_GL9.add_widget(btn3_BGL9)
                                a_B_GL9.add_widget(btn2_BGL9)
                                a_B_GL9.add_widget(btn4_BGL9)
                                a_B_GL9.add_widget(btn5_BGL9)
                                self.panel_gl9.add_widget(a_B_GL9)

                                a_B_GL9_2 = GridLayout(cols=1, spacing=0, size_hint_y=None, height = 120 , size_hint_x = 1)

                                btn3_BGL9_2 = Button(background_down = self.images + "roro.png" ,size_hint_y=0.025 , background_normal = self.images + 'roro.png', background_color = (1,1,1,1))
                                btn4_BGL9_2 = Button(background_down = self.images + "roro2.png" ,size_hint_y=0.025 , background_normal = self.images + 'roro2.png', background_color = (1,1,1,1))
                                btn6_BGL9_2 = Button(background_down = self.images + "asd2.png" ,size_hint_y= None ,height=25, background_normal = self.images + 'asd2.png', background_color = (1,1,1,1))
                                btn1_BGL9_2 = Button(background_down = self.images + "blanco.png" ,text='[b][color=#404040]'+x["precio"]+' RD$', size_hint_y=0.1, height=30, background_normal = self.images + 'blanco.png', background_color = (1,1,1,1), markup = True , font_size = 18,valign = 'top')
                                btn5_BGL9_2 = Button(background_down = self.images + "blanco.png" ,text='', size_hint_y=0.050, height=30, background_normal = self.images + 'blanco.png', background_color = (1,1,1,1), markup = True , font_size = '15sp')
                                btn2_BGL9_2 = Button(background_down = self.images + "blanco2.png" ,text='[color=#404040][b]DOP' , size_hint_y=0.1, height=30, background_normal = self.images + 'blanco.png',background_color = (1,1,1,1), markup   = True, font_size = 18)
                                
                                a_B_GL9_2.add_widget(btn6_BGL9_2)
                                a_B_GL9_2.add_widget(btn1_BGL9_2)
                                a_B_GL9_2.add_widget(btn3_BGL9_2)
                                a_B_GL9_2.add_widget(btn2_BGL9_2)
                                a_B_GL9_2.add_widget(btn4_BGL9_2)
                                a_B_GL9_2.add_widget(btn5_BGL9_2)
                                self.panel_gl9.add_widget(a_B_GL9_2)
                        else:
                            pass
                            
                            

    def ESTABLECIMIENTO_SUGERIDOS(self, button):
        try:
            self.clear_widgets()
            self.add_widget(self.GL10)
        except:
            pass

    def ESTABLECIMIENTO_CATEGORIAS(self, button):
        try:
            self.clear_widgets()
            self.add_widget(self.GL11)
        except:
            pass

    def ADMINISTRAR_INVENTARIO(self, button):
        try:
            self.clear_widgets()
            self.add_widget(self.GL12)
        except:
            pass






    def CREAR_PEDIDO(self, button):

        try:    
            if self.Items_No_Txt.text =="[color=#404040][b]"+"Vacio":
                print("MONTO VACIO")
                return
            else:
                pass
            self.string = ""
            a = 0
            for i in self.PedidoID:
                a = a + 1
                if a == 1:
                    self.string = self.string + i
                else:
                    self.string = self.string +","+ i
            print self.string
            
            
            
            data1 = {
            "pedido_id": str(int(self.PedidoNO) + 1),
            "pedido_por": str(self.UserU),
            "usuario_id": self.UserID,
            "categoria": str(self.Subtotal_Txt.text[18:]),
            "descripcion_del_pedido": self.string,
            "estado": "Activo",
            "fecha_pedido": str(time.strftime("%d/%m/%Y")),
            "precio_total": str(self.Total_Txt.text[18:-7]),
            "contacto": int(self.TiendaSolicitada)
            }
            print data1

            req = urllib2.Request(self.Dominio2+"Pedido/")
            req.add_header('Content-Type', 'application/json')
            response = urllib2.urlopen(req, json.dumps(data1))
            print("Pedido creado con exito")
            url = self.Dominio2+"Pedido/"
            json_obj = urllib2.urlopen(url)
            Datos_Tabla = json.load(json_obj)
            self.Pedidotable = Datos_Tabla
            self.PedidoNO = len(Datos_Tabla)
                
            self.pedido_objetos[:] = []
            self.pedido_precios[:] = []
            self.pedido_establecimiento[:] = []
            self.usuario_pedido = ({'objeto': self.pedido_objetos[i], 'precio': self.pedido_precios[i] , 'establecimiento': self.pedido_establecimiento[i]} for i in range(len(self.pedido_objetos)))
            self.GL3.clear_widgets()
            self.Input2 = Label(text="[color=#f2f2f2]FACTURA[/color]", markup=True,
                                        size_hint_y=None,
                                        size_hint_x=0.2,
                                        height=70,
                                        font_size=24
                                        )
            self.Input2_B = Label(text="[color=#f2f2f2][/color]", markup=True,
                                size_hint_y=None,
                                size_hint_x=0.2,
                                height=40,
                                font_size=24
                                )
            self.GL3.add_widget(self.Input2)
            self.GL3.add_widget(self.Input2_B)

            self.Total = Button(background_down = self.images + "blanco.png" ,text = "[color=#404040][b] Total : ",markup = True, background_color = (1,1,1,1), background_normal = self.images + "blanco.png",size_hint_y = None, height = 50)
            
            self.Subtotal = Button(background_down = self.images + "blanco.png" ,text = "[color=#404040][b]Departamento : " ,markup = True, background_color = (1,1,1,1), background_normal = self.images + "blanco.png",size_hint_y = None, height = 50)
            

            self.Factura = Button(background_down = self.images + "blanco.png" ,text = "[color=#404040][b]CHECK-IN",markup = True, background_color = (1,1,1,1), background_normal = self.images + "blanco.png",size_hint_y = None, height = 50)
            self.Factura_Txt= Button(background_down = self.images + "blanco.png" ,text = "[color=#404040][b]",markup = True, background_color = (1,1,1,1), background_normal = self.images + "blanco.png",size_hint_y = None, height = 50)
            self.Items_No = Button(background_down = self.images + "blanco.png" ,text = "[color=#404040][b]Items : ",markup = True, background_color = (1,1,1,1), background_normal = self.images + "blanco.png",size_hint_y = None, height = 50)

            self.Fecha = Button(background_down = self.images + "blanco.png" ,text = "[color=#404040][b]Fecha : ",markup = True, background_color = (1,1,1,1), background_normal = self.images + "blanco.png",size_hint_y = None, height = 50)
            self.Fecha_Txt = Button(background_down = self.images + "blanco.png" ,text = "[color=#404040][b]"+ time.strftime("%d/%m/%Y"),markup = True, background_color = (1,1,1,1), background_normal = self.images + "blanco.png",size_hint_y = None, height = 50)

            self.grade = Button(background_down = self.images + "asd.png" ,size_hint_y= None ,height=25, background_normal = self.images + 'asd.png', background_color = (1,1,1,1))
            self.grade2 = Button(background_down = self.images + "asd.png" ,size_hint_y= None ,height=25, background_normal = self.images + 'asd.png', background_color = (1,1,1,1))

            self.grade3 = Button(background_down = self.images + "blanco.png" ,size_hint_y= None ,height=25, background_normal = self.images + 'blanco.png', background_color = (1,1,1,1))
            self.grade4 = Button(background_down = self.images + "blanco.png" ,size_hint_y= None ,height=25, background_normal = self.images + 'blanco.png', background_color = (1,1,1,1))

            #self.GL3.add_widget(self.Factura)
            #self.GL3.add_widget(self.Factura_Txt)

            self.GL3.add_widget(self.grade)
            self.GL3.add_widget(self.grade2)
            self.GL3.add_widget(self.Fecha)
            self.GL3.add_widget(self.Fecha_Txt)
            self.GL3.add_widget(self.Items_No)
            self.GL3.add_widget(self.Items_No_Txt)

            self.GL3.add_widget(self.Total)
            self.GL3.add_widget(self.Total_Txt)
            self.GL3.add_widget(self.Subtotal)
            self.GL3.add_widget(self.Subtotal_Txt)

            self.GL3.add_widget(self.grade3)
            self.GL3.add_widget(self.grade4)

            self.GL3.add_widget(self.Button10)
            self.GL3.add_widget(self.Button10_B)

            #self.GL3.add_widget(self.Input1)
            #self.GL3.add_widget(self.Input1_B)
            self.Items_No_Txt.text ="[color=#404040][b]"+"Vacio"
            self.Total_Txt.text ="[color=#404040][b]"+"0.00 RD$"
            self.Subtotal_Txt.text ="[color=#404040][b]"+"Sin seleccionar."
            self.usuario_pedido = ({'objeto': self.pedido_objetos[i], 'precio': self.pedido_precios[i] , 'establecimiento': self.pedido_establecimiento[i]} for i in range(len(self.pedido_objetos)))
            for i in self.usuario_pedido:
                print i
                a_B_GL10 = GridLayout(cols=1, spacing=0, size_hint_y=None, height = 120 , size_hint_x = 1)
                a_B_GL10_B = GridLayout(cols=1, spacing=0, size_hint_y=None, height = 120 , size_hint_x = 1)
                btn3_BGL10 = Button(background_down = self.images + "roro.png" ,size_hint_y=0.025 , background_normal = self.images + 'roro.png', background_color = (1,1,1,1))
                btn4_BGL10 = Button(background_down = self.images + "roro2.png" ,size_hint_y=0.025 , background_normal = self.images + 'roro2.png', background_color = (1,1,1,1))
                btn6_BGL10 = Button(background_down = self.images + "asd.png" ,size_hint_y= None ,height=25, background_normal = self.images + 'asd2.png', background_color = (1,1,1,1))

                btn1_BGL10 = Button(background_down = self.images + "blanco.png" ,text='[b][color=#ff1a1a]'+ i["objeto"], size_hint_y=0.1, height=30, background_normal = self.images + 'blanco.png', background_color = (1,1,1,1) , markup = True , font_size = 18,valign = 'top')
                btn5_BGL10 = Button(background_down = self.images + "blanco.png" ,text=i["precio"] , size_hint_y=0.050, height=30, background_normal = self.images + 'blanco.png', background_color = (1,1,1,1), markup = True , font_size = '15sp')

                btn2_BGL10 = Button(background_down = self.images + "blanco.png" ,text='[color=#404040][b]MC' , size_hint_y=0.1, height=30, background_normal = self.images + 'blanco.png',background_color = (1,1,1,1), markup   = True, font_size = 18)

                a_B_GL10.add_widget(btn6_BGL10)
                a_B_GL10.add_widget(btn1_BGL10)
                a_B_GL10.add_widget(btn3_BGL10)
                a_B_GL10.add_widget(btn2_BGL10)
                a_B_GL10.add_widget(btn4_BGL10)
                a_B_GL10.add_widget(btn5_BGL10)
                self.GL3.add_widget(a_B_GL10)
                
                btn3_BGL11 = Button(background_down = self.images + "roro.png" ,size_hint_y=0.025 , background_normal = self.images + 'roro.png', background_color = (1,1,1,1))
                btn4_BGL11 = Button(background_down = self.images + "roro2.png" ,size_hint_y=0.025 , background_normal = self.images + 'roro2.png', background_color = (1,1,1,1))
                btn6_BGL11 = Button(background_down = self.images + "asd.png" ,size_hint_y= None ,height=25, background_normal = self.images + 'asd2.png', background_color = (1,1,1,1))

                btn1_BGL11 = Button(background_down = self.images + "blanco.png" ,text='[b][color=#ff1a1a]'+ i["precio"] + ".00 RD$", size_hint_y=0.1, height=30, background_normal = self.images + 'blanco.png', background_color = (1,1,1,1) , markup = True , font_size = 18,valign = 'top')
                btn5_BGL11 = Button(background_down = self.images + "blanco.png" ,text=i["precio"] , size_hint_y=0.050, height=30, background_normal = self.images + 'blanco.png', background_color = (1,1,1,1), markup = True , font_size = '15sp')

                btn2_BGL11 = Button(background_down = self.images + "blanco.png" ,text='[color=#404040][b]1' , size_hint_y=0.1, height=30, background_normal = self.images + 'blanco.png',background_color = (1,1,1,1), markup   = True, font_size = 18)

                
                a_B_GL10_B.add_widget(btn6_BGL11)
                a_B_GL10_B.add_widget(btn1_BGL11)
                a_B_GL10_B.add_widget(btn3_BGL11)
                a_B_GL10_B.add_widget(btn2_BGL11)
                a_B_GL10_B.add_widget(btn4_BGL11)
                a_B_GL10_B.add_widget(btn5_BGL11)
                self.GL3.add_widget(a_B_GL10_B)
            for i in self.panelesformularios:
                try:
                   self.main_panel.remove_widget(i)
                   self.main_panel.add_widget(self.layout) 
                except:
                    pass
        except:
            print("Monto vacio.")

    def CREAR_USUARIO(self, id, usuario, password , email, predet):
        try: 
            print id
            try:
                arrobaindex = email.index('@')
                arrobaindex2 = email.index('.com')
            except:
                self.Popup2 = Popup(title='',content=Label(text='Campos vacios'),size_hint=(None, None), width = 200)
                self.Popup2.open()
            print arrobaindex2

            print email[arrobaindex:arrobaindex2]
            if predet == "True":
                derechos = "Administrador"
            else:
                derechos = "Developer"
            if (email[arrobaindex:arrobaindex2] == "@intellisys") or (email[arrobaindex:] == "@cincinnatus"):
                if len(self.UsuariostableID2) >= 1:
                    data =   {
                    "id": self.UsuariostableID2[0],
                    "usuario": usuario,
                    "password": password,
                    "email": email,
                    "direccion": "Vacio",
                    "privilegios": derechos,
                    "verification_Id": "b1q2g10o5c3x8"
                    }
                else:
                    data =   {
                    "id": id,
                    "usuario": usuario,
                    "password": password,
                    "email": email,
                    "direccion": "Vacio",
                    "privilegios": derechos,
                    "verification_Id": "b1q2g10o5c3x8"
                    }
                    
                req = urllib2.Request(self.Dominio2+"Usuario/")
                req.add_header('Content-Type', 'application/json')
                response = urllib2.urlopen(req, json.dumps(data))
                print("Usuario Creado con Exito.")
                self.clear_widgets()
                self.add_widget(self.GL2_root)
                if derechos == "Administrador":
                    f = file("data.dat", "w")
                    self.Primerinicio_Layoutpopup.dismiss()
                self.Dominio = "http://g-005.herokuapp.com/API/"
                self.Dominio2 = "http://127.0.0.1:8000/API/"
                Tablas = ["Usuario","Categoria","Contacto","Rating", "Menu","Menu_Sub_Categorias","Pedido","Pedidos_Detalles", "Sugerencia"] #falta la tabla "sugerencia".
                
                
                self.UsuarioNO = 0
                self.CategoriaNO = 0
                self.ContactoNO = 0
                self.RatingNO = 0
                self.MenuNO = 0
                self.Menu_Sub_CategoriasNO = 0
                self.PedidoNO = 0
                self.Pedidos_DetallesNO = 0
                self.SugerenciaNO = 0
                
                for i in Tablas:
                    url = self.Dominio2 + i + "/"
                    json_obj = urllib2.urlopen(url)
                    Datos_Tabla = json.load(json_obj)
                    print str(i) + " " + str(len(Datos_Tabla))+ " Registros"
                            
                    if i == "Usuario":
                        self.Usuariostable = Datos_Tabla
                        self.UsuarioNO = len(Datos_Tabla)
                        for i in self.Usuariostable:
                            if self.UsuariostableLastID < i["id"]:
                                self.UsuariostableLastID = i["id"]
                            self.UsuariostableID.append(i["id"])
                        for i in range(self.UsuariostableLastID):
                            self.UsuariostableID2.append(i)
                            for g in  self.UsuariostableID:
                                if g == i:
                                    self.UsuariostableID2.remove(g)
                           
                            
                        self.UsuariostableID2.remove(0)  
                        print self.UsuariostableID2
                    elif i == "Categoria":
                        self.categorias = []
                        for i in Datos_Tabla:
                            self.categorias.append(i["categoria"])
                            
                        self.Categoriatable = Datos_Tabla
                        self.CategoriaNO = len(Datos_Tabla)
                    elif i == "Contacto":
                        self.Lista_Contactos_IDs = []
                        self.Lista_Contactos_Nombres = []
                        self.Contactotable = Datos_Tabla
                        for i in self.Contactotable:
                            self.Lista_Contactos_Nombres.append(""+str(i["nombre"]))
                            self.Lista_Contactos_IDs.append(str(""+i["id"]))
                            
                        self.ContactoNO = len(Datos_Tabla)
                    elif i == "Rating":
                        self.Ratingtable = Datos_Tabla
                        self.RatingNO = len(Datos_Tabla)
                    elif i == "Menu":
                        self.Menutable = Datos_Tabla
                        self.MenuNO = len(Datos_Tabla)
                    elif i == "Menu_Sub_Categorias":
                        self.MenuSCtable = Datos_Tabla
                        self.Menu_Sub_CategoriasNO = len(Datos_Tabla)
                    elif i == "Pedido":
                        self.Pedidotable = Datos_Tabla
                        self.PedidoNO = len(Datos_Tabla)
                    elif i == "Pedidos_Detalles":
                        self.Pedidos_Detallestable = Datos_Tabla
                        self.Pedidos_DetallesNO = len(Datos_Tabla)
                    elif i == "Sugerencia":
                        self.Sugerenciastable = Datos_Tabla
                        self.Pedidos_DetallesNO = len(Datos_Tabla)
                self.clear_widgets()
                self.add_widget(self.GL1)
            else:
                print("Email no permitido.")
                self.EmailIncorrecto.open()
                    
                        
                
        except:
            pass



    def CREAR_CONTACTO(self, button):
        self.clear_widgets()
        self.add_widget(self.GL7)

    def CREAR_ACEPTAR_CONTACTO(self, button):

        self.clear_widgets()
        self.add_widget(self.GL7)

    def LOG_IN(self, button):
        try:
            B = ({"User": self.Usuario_Textbox.text, "Pass": self.Constrasena_Textbox.text})
            print B
            self.UserU = self.Usuario_Textbox.text
            for i in self.Usuariostable:
                print i['usuario']
                print self.Usuario_Textbox.text
                if i['usuario'] == self.Usuario_Textbox.text:
                    print("usuario encontrado.")
                    if i['password'] == self.Constrasena_Textbox.text:
                        print("contrasena correcta.")
                        if i["verification_Id"] == "Verificado":
                            self.UserU = i['usuario']
                            self.UserPW = i['password']
                            self.UserID = i['id']
                            self.UserPriv = i['privilegios']
                            print self.UserPriv
                            str = i['direccion']
                            print i['direccion']
                            print self.UserID 
                            str2 = str.split(",")
                            self.UserDIR[:]= []
                            for i in str2:
                                print i.encode("utf-8 ")
                                self.UserDIR.append(i.encode("utf-8 "))
                            
                            try:
                                self.PBoriginal1B.text ="[color=#404040][b]"+self.UserDIR[0]
                                self.PBoriginal2B.text ="[color=#404040][b]"+self.UserDIR[1]
                                self.PBoriginal3B.text ="[color=#404040][b]"+self.UserDIR[2]
                                self.PBoriginal4B.text ="[color=#404040][b]"+self.UserDIR[3]
                                self.PBoriginal5B.text ="[color=#404040][b]"+self.UserDIR[4]
                                self.PBoriginal6B.text ="[color=#404040][b]"+self.UserDIR[5]
                                
                                if self.Label_4B.active == True:
                                    self.coneccion = open(self.patch + "/loggeduser.data", "w")
                                    if self.Label_4B2.active == True:
                                        self.coneccion.write("ON,"+ self.UserU + "," + self.UserPW)
                                        self.coneccion.close()
                                    else:
                                        print ("Desactivado")
                                        self.coneccion.write("OFF,"+ self.UserU + "," + self.UserPW)
                                        self.coneccion.close()
                                    
                            except IOError as (errno, strerror):
                                print "I/O error({0}): {1}".format(errno, strerror)
                            except ValueError:
                                print "Could not convert data to an integer."
                            except:
                                print "Unexpected error:", sys.exc_info()[0]
                                pass
                            
                            self.clear_widgets()
                            self.add_widget(self.GL2_root)
                            
                            if self.UserPriv == "Super Administrador":
                                self.side_panel.add_widget(self.GL2Button3)
                                self.caja_B10
                                self.caja_B10.bind(on_press = self.ADMTIENDA)
                                pass
                            elif self.UserPriv == "Administrador":
                                print ("AAAAAAAAAAAAAAAAAAAAAAA")
                                self.side_panel.add_widget(self.GL2Button3)
                                pass

                            elif self.UserPriv == "Developer":
                                #TIENDAS SOLO LECTURA
                                self.side_panel.remove_widget(self.GL2Button3)
                                pass

                            elif self.UserPriv == "UsuarioFF":
                                #TIENDAS SOLO LECTURA
                                self.side_panel.remove_widget(self.GL2Button3)
                                pass

                            elif self.UserPriv == "Invitado":
                                #TIENDAS SOLO LECTURA
                                
                                self.side_panel.remove_widget(self.GL2Button3)
                                print ("AAAAAAAAAAAAAAAAAAAAAAA")
                                pass
                        else:
                             self.Label_4B.text = '[color=#ff1a1a]Usuario no ha sido activado.'
                             return
                            


                    elif i['password'] != self.Constrasena_Textbox.text:
                        print("contrasena incorrecta.")
                        self.Label_4B.text = '[color=#ff1a1a]Usuario o Contraseña Incorrectos.'
                else:
                    print("usuario no existe.")
                    self.Label_4B.text = '[color=#ff1a1a]Usuario o Contraseña Incorrectos.'





            print self.NOMBRE_user
            print self.ID_user


            print self.Pedidos








        except:
            print("ERROR")


class MyApp(App):
    def build(self):
        return InterfaceManager()


if __name__ in ('__main__', '__android__'):
    MyApp().run()
