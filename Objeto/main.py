#!/usr/bin/env python55555533yyyyyyyyyyyyyyyyyyyyy555555
# -*- coding: utf-8 -*-
from kivy.config import Config
Config.set('graphics','borderless',1)
Config.set('graphics','resizable',0)
Config.set('graphics','position','custom')
Config.set('graphics','left',1000)
Config.set('graphics','top',35)
import kivy
import requests
from kivy.garden.mapview import MapView, MapMarker, MarkerMapLayer,MapSource
from kivy.uix.bubble import Bubble
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
Window.size = (426,640)
from kivy.utils import get_hex_from_color, get_color_from_hex
from kivy.parser import parse_color
import time
import json
import urllib2
import os   
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
from kivy.uix.behaviors import ButtonBehavior
import math
    
from kivy.lang import Builder
import os.path
import time
import sys


reload(sys)
sys.setdefaultencoding('latin1')
resource_add_path(os.path.dirname(__file__))

Window.size = (426,640)
from kivy.garden.mapview import MapView, MapMarker, MarkerMapLayer,MapSource
import json, requests
from kivy.uix.button import Button
from plyer import gps
from kivy.properties import StringProperty
from kivy.clock import Clock, mainthread

from kivy.uix.relativelayout import RelativeLayout
from kivy.app import App

Builder.load_string('''
<NavigationDrawer>:
    size_hint: (1,1)
    _side_panel: sidepanel
    _main_panel: mainpanel
    _join_image: joinimage
    side_panel_width: min(0.5*self.width, 0.5*self.width)
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
                rgba: (0,0,0,.80)
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
                rgba: (0,0,0,1)
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
class ImageButton(ButtonBehavior, AsyncImage):
    pass
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

class InterfaceManager(RelativeLayout):
    def __init__(self, **kwargs):
        super(InterfaceManager, self).__init__(**kwargs)
        
        pantalla_principall = GridLayout(cols =1,size_hint_y = None)
        pantalla_principall_root = ScrollView()
        pantalla_principall.bind(minimum_height = pantalla_principall.setter('height'))
        patch = os.path.dirname(os.path.abspath(__file__))
        hud = patch + '/hud/'
        icon = patch + '/icons/'
        textb = patch + '/textbox/'
        database = patch + '/database/'
        color = patch + '/hud/color/'
        barra = patch + '/hud/barras/'
        C1 = "[color=#13C0C7]"
        C4 = "[color=#000000]"
        C2 = "[color=#404040]"
        C3 = "[color=#ff3333]"
        C5 = "[color=#00FF21]"
        C6 = "[color=#A0A0A0]"
        TC = "[/color]"
        self.ROOT_Navitagiondrawer1 = NavigationDrawer()
        self.ROOT_Navitagiondrawer1.add_widget(Button())
        self.ROOT_Navitagiondrawer1.add_widget(pantalla_principall_root)
        pantalla_principall_root.add_widget(pantalla_principall)
        #self.ROOT_Navitagiondrawer1.add_widget(Button())
        self.add_widget(self.ROOT_Navitagiondrawer1)
        objetos = 5
        textvar1 = ['[b]Tu busqueda:[/b] "Goma Grande numero 10"',"[b]15 Coincidencias[/b]"]
        textvar1r = ""
        for i in textvar1:
            textvar1r += i + '\n' 
        pantalla_principall.add_widget(Button(text = "Panel de Busqueda", background_normal = color + "5.png", size_hint_y = None, height = 50))
        pantalla_principall.add_widget(Button(line_height = 1.4,markup = True,text= C4+textvar1r,size_hint_y = None , height = 100,background_normal = color+"16.png"))

        for i in range(objetos):
            objeto = GridLayout(cols = 2, size_hint_y= None, height = 350)
            columna1 = RelativeLayout()
            
            columna1.add_widget(Image(source = color + "16.png", keep_ratio = False, allow_stretch = True))
            columna1.add_widget(Image(source = "goma.jpg", keep_ratio = True, allow_stretch = False))
            columna1.add_widget(Button(text_size = (Window.width/2 -50, 50),halign = "left",valign = "middle",font_size = 15,background_normal = color + "None.png",markup = True,text = C5+"Disponible",size_hint = (None,None),width = (Window.width/2 -50 ), height = 50, pos = (50,0)))
            columna1.add_widget(Image(size_hint = (None,None), size = (30,30), source = icon + "checked.png", keep_ratio = False, allow_stretch = True,pos = (25-15,25-15)))
            
            columna2 = GridLayout(cols = 1)
            datos = Button(line_height = 1.2,valign = "top",background_normal = color+"16.png",background_down = color+"16b.png",font_size = 15,text = C4,text_size = (Window.width/2 -20,240),markup = True)
            columna2.add_widget(datos)
            columna2botones_cont = GridLayout(cols = 1, size_hint_y = None, height = 100)
            columna2botones = GridLayout(cols = 2, size_hint_y = None, height = 50)
            columna2botones1 = GridLayout(rows = 1, size_hint_y = None, height = 50)
            columna2botones_cont.add_widget(columna2botones1)
            columna2botones_cont.add_widget(columna2botones)
            
            columna2botones1.add_widget(Image(size_hint_x = 1, source = color + "16.png",keep_ratio = False , allow_stretch = True))
            columna2botones1.add_widget(ImageButton(text_size = (75,50),halign = "right",valign = "middle",font_size = 30,markup = True ,text = C4+"<",size_hint_x = None, width = 50,source = icon + "plus.png"))
            columna2botones1.add_widget(Button(size_hint_x = None, width = 50,border = [0,0,0,0],font_size = 20,markup = True,text = C4+"[b]0",background_normal = barra + "Path 1.png"))
            columna2botones1.add_widget(ImageButton(font_size = 30,text_size = (75,50),halign = "left",valign = "middle",markup = True, text = C4+">",size_hint_x = None, width = 50,source = icon + "minus.png"))
            columna2botones1.add_widget(Image(size_hint_x = 1, source = color + "16.png",keep_ratio = False , allow_stretch = True))
            
            
            
            
            
            columna2botones.add_widget(Button(border = [0,0,0,0],font_size = 19,size_hint_y = None, height = 50,background_normal = icon + "add-to-cart.png",background_down = color + "16.png",text =C5+ "",markup = True,size_hint_x = None, width = 50))
            columna2botones.add_widget(Button(font_size = 19,size_hint_y = None, height = 50,background_normal = color + "16.png",background_down = color + "16.png",markup = True,text =C4+ "[b]$19.99[/b] Pieza"))
            
            columna2.add_widget(columna2botones_cont)
            
            
            columna2text = ['[b]Contratuerca para\nmangueta Delantera[/b]',C4+'[b]PARTE[/b]'+TC,'UP 28492',C4+'[b]LINEA DE PRODUCTO[/b]'+TC,'NAPA Ultra Premium Brake Parts']
            for i in columna2text:
                datos.text += i + '\n' 
            objeto.add_widget(columna1)
            objeto.add_widget(columna2)
            pantalla_principall.add_widget(Image(size_hint_y = None, height = 1, source = color + "16b.png",keep_ratio = False, allow_stretch = True))
            pantalla_principall.add_widget(objeto)
        
        




        
        
class MyApp(App):
    def build(self):
        return InterfaceManager()
 

if __name__ in ('__main__', '__android__'):
    MyApp().run()

    
    
    
    
    