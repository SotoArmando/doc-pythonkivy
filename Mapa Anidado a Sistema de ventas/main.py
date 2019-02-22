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

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
class Showcase(FloatLayout):
    pass



class InterfaceManager(RelativeLayout):
    def __init__(self, **kwargs):
        
        
        super(InterfaceManager, self).__init__(**kwargs)
        self.patch = os.path.dirname(os.path.abspath(__file__))
        self.hud = self.patch + '/hud/'
        self.icons = self.patch + '/icons/'
        self.textb = self.patch + '/textbox/'
        Window.clearcolor = (1,1,1,0)
        self.root = GridLayout(cols = 1)
        self.add_widget(self.root)
        NID = "[color=#404040]"
        self.FP = GridLayout(cols = 4   ,size_hint_y = None , height = 60) #barra principal
        self.root.add_widget(self.FP)
        
        
        self.BTN1 = ImageButton(source = self.icons + "Entypo_270e(1)_128B.png", keep_ratio = True, allow_stretch = False, size_hint_x = None , width = 60,size_hint_y = None , height = 60)
        self.BTN2 = ImageButton(source = self.icons + "Entypo_2302(0)_128.png", keep_ratio = True, allow_stretch = False, size_hint_x = None , width = 60,size_hint_y = None , height = 60)
        self.BTN3 = ImageButton(source = self.icons + "Entypo_d83c(0)_128.png", keep_ratio = True, allow_stretch = False, size_hint_x = None , width = 60,size_hint_y = None , height = 60)
        
        self.BTN1.bind(on_press = self.FORM2)
        self.BTN2.bind(on_press = self.FORM1)
        self.BTN3.bind(on_press = self.FORM3)
        
        
        self.FP.add_widget(self.BTN1)
        self.FP.add_widget(self.BTN3)
        self.FP.add_widget(ImageButton(source = self.hud + "negro.png", keep_ratio = False, allow_stretch = True,size_hint_y = None , height = 60))
        self.FP.add_widget(self.BTN2)


        
        self.F1 = GridLayout(cols = 1, size_hint_y = None) #Formulario Actual
        self.F1.add_widget(Image(source = self.hud +"negro2.png",keep_ratio = False, allow_stretch = True, size_hint_y = None , height = 2.5))
        self.F1.add_widget(Image(source = self.hud +"negro2.png",keep_ratio = False, allow_stretch = True, size_hint_y = None , height = 2.5))
        self.F1.add_widget(Button(background_normal = self.hud + "Blanco",markup = True,text = NID+"[b]Catálogo",size_hint_y = None, height = 70,font_size = 20)) #Titulo F
        self.F1_root = ScrollView(size_hint=(1, 1))
        self.F1_root.add_widget(self.F1)
        self.F1.bind(minimum_height=self.F1.setter('height'))
        
        self.root.add_widget(self.F1_root)
        
        for i in range(10):
            if i == 0:
                g = "Entypo_2795(0)_128.png"
                g1 = "[b]Añadir objeto"
                g2 = ""
                g3 = ""
            else:  
                g = "Entypo_2713(0)_128.png"
                g1 = "[b]Item" + str(i)
                g2 = "[b]Objeto[/b].Nombre"
                g3 = "[b]Objeto[/b].Precio"
            self.C = GridLayout(cols = 1, size_hint_y = None, height = 150)
            self.CC = GridLayout(cols = 3, size_hint_y = None , height = 100)
            self.CC2 = GridLayout(cols = 4, size_hint_y = None , height = 50)
            
            self.CC.add_widget(ImageButton(source = self.icons + g, size_hint_x = None , width = 100))
            self.CC.add_widget(Button(background_normal = self.hud + "Blanco",text =NID+g2,markup = True))
            self.CC.add_widget(Button(background_normal = self.hud + "Blanco",text =NID+g3,markup = True))
            
            self.CC2.add_widget(Label(text = NID+ g1,markup = True, size_hint_y = None, height = 50))
            self.CC2.add_widget(Label())
            self.CC2.add_widget(ImageButton(source = self.icons + "Entypo_e003(0)_128.png", size_hint_x = None , width = 50))
            self.CC2.add_widget(ImageButton(source = self.icons + "Entypo_e78d(0)_128.png", size_hint_x = None , width = 50))
            
            self.C.add_widget(self.CC2)
            self.C.add_widget(self.CC)
            self.C.add_widget(Image(source = self.hud +"blanco2.png", size_hint_y = None , height = 2.5, keep_ratio = False, allow_stretch = True))
            
            self.F1.add_widget(self.C)
            
        self.F2 = GridLayout(cols = 1, size_hint_y = None) #Formulario Actual
        
        self.F2.add_widget(Image(source = self.hud +"negro2.png",keep_ratio = False, allow_stretch = True, size_hint_y = None , height = 5))
        self.F2.add_widget(Button(background_normal = self.hud + "Blanco",markup = True,text = NID+"[b]Cuenta por Cobrar",size_hint_y = None, height = 70,font_size = 20)) #Titulo F
        self.F2.add_widget(Image(source = self.hud +"negro2.png",keep_ratio = False, allow_stretch = True, size_hint_y = None , height = 5))
        
        self.F2_root = ScrollView(size_hint=(1, 1))
        self.F2_root.add_widget(self.F2)
        self.F2.bind(minimum_height=self.F2.setter('height'))
        
        #self.F2.add_widget(Button(background_normal = self.hud + "Blanco",markup = True,text = NID+"Datos de Cliente",size_hint_y = None, height = 35,font_size = 17))
        
        self.F2.add_widget(Image(source = self.hud +"blanco.png",keep_ratio = False, allow_stretch = True, size_hint_y = None , height = 5))

       
        self.F2.add_widget(Button(text_size = (300,35),halign = "left",background_normal = self.hud + "Blanco",markup = True,text = NID+"[b]POSICION DEL MAPA",size_hint_y = None, height = 50,font_size = 17))
        self.Complemento1 = TextInput(text ="lat:lon",multiline = False,cursor_color = (0,0,0,1),padding = [100,0,0,0],font_size = 20,foreground_color =(0,0,0,.7),background_active = self.textb + 't1.png', background_normal = self.textb + 't1.png',size_hint_y= None, height = 35)
        self.F2.add_widget(self.Complemento1)
        self.F2.add_widget(Button(background_normal = self.hud + "blanco2.png",markup = True,text = NID+"Posicionar en el Mapa",size_hint_y = None, height = 70,font_size = 20))
        self.F2.add_widget(Image(source = self.hud +"blanco.png",keep_ratio = False, allow_stretch = True, size_hint_y = None , height = 5))
        
        #self.F2.add_widget(Image(source = self.hud +"blanco2.png",keep_ratio = False, allow_stretch = True, size_hint_y = None , height = 2.5))
        self.F2.add_widget(Button(text_size = (300,35),halign = "left",background_normal = self.hud + "Blanco",markup = True,text = NID+"[b]CODIGO",size_hint_y = None, height = 50,font_size = 17))
        
        self.Complemento2 = TextInput(multiline = False,cursor_color = (0,0,0,1),padding = [100,0,0,0],font_size = 20,foreground_color =(0,0,0,.7),background_active = self.textb + 't1.png', background_normal = self.textb + 't1.png',text ="",size_hint_y= None, height = 35)
        self.F2.add_widget(self.Complemento2)
        self.F2.add_widget(Image(source = self.hud +"blanco2.png",keep_ratio = False, allow_stretch = True, size_hint_y = None , height = 2.5))
        
        self.F2.add_widget(Button(text_size = (300,35),halign = "left",background_normal = self.hud + "Blanco",markup = True,text = NID+"[b]CLIENTE",size_hint_y = None, height = 50,font_size = 17))
        self.Complemento3 = TextInput(multiline = False,cursor_color = (0,0,0,1),padding = [100,0,0,0],font_size = 20,foreground_color =(0,0,0,.7),background_active = self.textb + 't1.png', background_normal = self.textb + 't1.png',text ="",size_hint_y= None, height = 35)
        self.F2.add_widget(self.Complemento3)
        self.F2.add_widget(Image(source = self.hud +"blanco2.png",keep_ratio = False, allow_stretch = True, size_hint_y = None , height = 2.5))
        
        self.F2.add_widget(Button(text_size = (300,35),halign = "left",background_normal = self.hud + "Blanco",markup = True,text = NID+"[b]RNC/CEDULA",size_hint_y = None, height = 50,font_size = 17))
        self.Complemento4 = TextInput(multiline = False,cursor_color = (0,0,0,1),padding = [100,0,0,0],font_size = 20,foreground_color =(0,0,0,.7),background_active = self.textb + 't1.png', background_normal = self.textb + 't1.png',text ="",size_hint_y= None, height = 35)
        self.F2.add_widget(self.Complemento4)
        self.F2.add_widget(Image(source = self.hud +"blanco2.png",keep_ratio = False, allow_stretch = True, size_hint_y = None , height = 2.5))
        
        self.F2.add_widget(Button(text_size = (300,35),halign = "left",background_normal = self.hud + "Blanco",markup = True,text = NID+"[b]CONTACTO",size_hint_y = None, height = 50,font_size = 17))
        self.Complemento5 = TextInput(multiline = False,cursor_color = (0,0,0,1),padding = [100,0,0,0],font_size = 20,foreground_color =(0,0,0,.7),background_active = self.textb + 't1.png', background_normal = self.textb + 't1.png',text ="",size_hint_y= None, height = 35)
        self.F2.add_widget(self.Complemento5)
        self.F2.add_widget(Image(source = self.hud +"blanco2.png",keep_ratio = False, allow_stretch = True, size_hint_y = None , height = 2.5))
        
        
        #self.F2.add_widget(Image(source = self.hud +"negro2.png",keep_ratio = False, allow_stretch = True, size_hint_y = None , height = 5))
        self.F2.add_widget(Button(background_normal = self.hud + "Blanco",markup = True,text = NID+"[b]Direcciones",size_hint_y = None, height = 70,font_size = 20)) #Titulo F
        self.F2.add_widget(Image(source = self.hud +"negro2.png",keep_ratio = False, allow_stretch = True, size_hint_y = None , height = 5))
        
        
        self.F2.add_widget(Button(text_size = (300,35),halign = "left",background_normal = self.hud + "Blanco",markup = True,text = NID+"[b]DIRECCION1",size_hint_y = None, height = 50,font_size = 17))
        self.Complemento6 = TextInput(multiline = False,cursor_color = (0,0,0,1),padding = [100,0,0,0],font_size = 20,foreground_color =(0,0,0,.7),background_active = self.textb + 't1.png', background_normal = self.textb + 't1.png',text ="",size_hint_y= None, height = 35)
        self.F2.add_widget(self.Complemento6)
        self.F2.add_widget(Image(source = self.hud +"blanco2.png",keep_ratio = False, allow_stretch = True, size_hint_y = None , height = 2.5))
        
        self.F2.add_widget(Button(text_size = (300,35),halign = "left",background_normal = self.hud + "Blanco",markup = True,text = NID+"[b]SECTOR",size_hint_y = None, height = 50,font_size = 17))
        self.Complemento7 = TextInput(multiline = False,cursor_color = (0,0,0,1),padding = [100,0,0,0],font_size = 20,foreground_color =(0,0,0,.7),background_active = self.textb + 't1.png', background_normal = self.textb + 't1.png',text ="",size_hint_y= None, height = 35)
        self.F2.add_widget(self.Complemento7)
        self.F2.add_widget(Image(source = self.hud +"blanco2.png",keep_ratio = False, allow_stretch = True, size_hint_y = None , height = 2.5))

        self.F2.add_widget(Button(text_size = (300,35),halign = "left",background_normal = self.hud + "Blanco",markup = True,text = NID+"[b]CIUDAD",size_hint_y = None, height = 50,font_size = 17))
        self.Complemento8 = TextInput(multiline = False,cursor_color = (0,0,0,1),padding = [100,0,0,0],font_size = 20,foreground_color =(0,0,0,.7),background_active = self.textb + 't1.png', background_normal = self.textb + 't1.png',text ="",size_hint_y= None, height = 35)
        self.F2.add_widget(self.Complemento8)
        self.F2.add_widget(Image(source = self.hud +"blanco2.png",keep_ratio = False, allow_stretch = True, size_hint_y = None , height = 2.5))
 
        self.F2.add_widget(Button(text_size = (300,35),halign = "left",background_normal = self.hud + "Blanco",markup = True,text = NID+"[b]DIRECCION2",size_hint_y = None, height = 50,font_size = 17))
        self.Complemento9 = TextInput(multiline = False,cursor_color = (0,0,0,1),padding = [100,0,0,0],font_size = 20,foreground_color =(0,0,0,.7),background_active = self.textb + 't1.png', background_normal = self.textb + 't1.png',text ="",size_hint_y= None, height = 35)
        self.F2.add_widget(self.Complemento9)
        self.F2.add_widget(Image(source = self.hud +"blanco2.png",keep_ratio = False, allow_stretch = True, size_hint_y = None , height = 2.5))

        self.F2.add_widget(Button(text_size = (300,35),halign = "left",background_normal = self.hud + "Blanco",markup = True,text = NID+"[b]SECTOR",size_hint_y = None, height = 50,font_size = 17))
        self.Complemento10 = TextInput(multiline = False,cursor_color = (0,0,0,1),padding = [100,0,0,0],font_size = 20,foreground_color =(0,0,0,.7),background_active = self.textb + 't1.png', background_normal = self.textb + 't1.png',text ="",size_hint_y= None, height = 35)
        self.F2.add_widget(self.Complemento10)
        self.F2.add_widget(Image(source = self.hud +"blanco2.png",keep_ratio = False, allow_stretch = True, size_hint_y = None , height = 2.5))
    
        self.F2.add_widget(Button(text_size = (300,35),halign = "left",background_normal = self.hud + "Blanco",markup = True,text = NID+"[b]CIUDAD",size_hint_y = None, height = 50,font_size = 17))
        self.Complemento11 = TextInput(multiline = False,cursor_color = (0,0,0,1),padding = [100,0,0,0],font_size = 20,foreground_color =(0,0,0,.7),background_active = self.textb + 't1.png', background_normal = self.textb + 't1.png',text ="",size_hint_y= None, height = 35)
        self.F2.add_widget(self.Complemento11)
        self.F2.add_widget(Image(source = self.hud +"blanco2.png",keep_ratio = False, allow_stretch = True, size_hint_y = None , height = 2.5))
        
        self.Button1 = Button(font_size = 22,text = "Confirmar cuenta",size_hint_y = None , height = 75,background_normal = self.hud  + "negro2.png",markup = True)
        self.F2.add_widget(self.Button1)
        self.Button1.bind(on_press = self.TOMARREGISTRO)
        
        
        
        
        self.F3 = GridLayout(cols = 1, size_hint_y = None) #Formulario Actual
        #self.F3.add_widget(Image(source = self.hud +"negro2.png",keep_ratio = False, allow_stretch = True, size_hint_y = None , height = 2.5))
        #self.F3.add_widget(Image(source = self.hud +"negro2.png",keep_ratio = False, allow_stretch = True, size_hint_y = None , height = 2.5))
        #self.F3.add_widget(Button(background_normal = self.hud + "Blanco",markup = True,text = NID+"[b]Mapa",size_hint_y = None, height = 70,font_size = 20)) #Titulo F
        self.F3_root = GridLayout(size_hint=(1, 1), cols = 1)
        self.ROOT_Navitagiondrawer1 = NavigationDrawer()
        self.ROOT_Navitagiondrawer1.anim_type = 'slide_above_simple'
        self.F3_btnsm = GridLayout(cols = 1)
        self.ROOT_Navitagiondrawer1.add_widget(self.F3_btnsm )
        self.ROOT_Navitagiondrawer1.add_widget(self.F3_root)
        self.F3_btnsm.add_widget(ImageButton(source = self.hud + "negro2.png",size_hint = (1,None), height = 100))
        self.F3_btnsm.add_widget(ImageButton(source = self.hud + "negro2.png",size_hint = (1,None), height = 100))
        self.F3_btnsm.add_widget(ImageButton(source = self.hud + "negro2.png",size_hint = (1,None), height = 100))
        self.F3_btnsm.add_widget(Button(text= "hola",size_hint = (1,None), height = 100))
        #self.F3_root.add_widget(self.F3)
        self.F3.bind(minimum_height=self.F3.setter('height'))
        accesstoken = "pk.eyJ1IjoiYXJtYW5kbzI5IiwiYSI6ImNpd282ZHJ3azAwMWoydHFuZmJudnNzYzEifQ.12vIF51BCThjrut4Q56sGg"
        sourcex = MapSource(url="https://api.mapbox.com/v4/mapbox.streets/1/0/0@2x.png?access_token="+accesstoken,
        cache_key="map2",tile_size=512,
        image_ext="png", attribution="@Armando Josè Soto Melo")
        self.mv = MapView(zoom = 15, lat = 18.454651 , lon = -69.971119, map_source = sourcex)


        
        self.layer = MarkerMapLayer()
        self.m1 = MapMarker(lat = 18.454651 , lon = -69.971119, layer = self.layer, source = self.icons + "marker.png")
        self.m2 = MapMarker(lat = 18.434651 , lon = -69.981119, layer = self.layer, source = self.icons + "marker.png")
        
        pposicion = str(self.m1)
        self.mv.add_layer(self.layer)
        self.mv.add_marker(self.m1,layer = self.layer)
        self.mv.add_marker(self.m2  ,layer = self.layer)
        bcm = 0
        self.pos0 = 15
        self.pos1 = 15
        self.abcd = 0
        self.ALL = []
        self.puntos = [self.m1,self.m2]
        def mmm(m,b,c):
            
            self.abcd += 1
            self.ALL.append(self.mv.lat)
            if len(self.ALL) == 11:
                print("-------------------")
                print self.ALL[0]
                print self.ALL[10]
                self.ALL[:] = []
            if self.abcd == 1:
                print "---------------------------------------"
            print self.mv.zoom
            print self.mv.lat
            

            #self.m1.lat += 0.00041991*(x*-1)
            

            
        self.zoom = 15
        self.zoom2 = 15
        
        #self.lat = self.mv.lat
        #self.lat2 = self.mv.lat
        self.abcd = 0
        def mmm2(m,b,c):
            
            self.zoom2 = self.mv.zoom
            if self.abcd == 0:
                if self.zoom2 == self.zoom:
                    self.abcd +=1
                    self.lat = self.mv.lat
                
            if self.zoom2 != self.zoom:
                self.abcd = 0
                print self.zoom2
                print self.zoom
                y = self.zoom - self.zoom2
                print y
                self.lat2 = self.mv.lat
                x = self.lat2 - self.lat
                print x
                if y == -1:
                    print("acercar")
                    self.m1.lat +=  x
                else:
                    print("alejar")
                    self.m1.lat +=  x
                
                self.zoom = self.mv.zoom
                self.lat = self.lat2
                
            
            
            
          
            

        #self.mv.bind(on_map_relocated = mmm)
        self.btng = GridLayout(cols = 3)
        self.btng.add_widget(Button())
        self.btng.add_widget(Button())
        self.btng.add_widget(Button())
        self.F3_root.add_widget(self.mv)
        #self.F3_root.add_widget(self.btng)
        self.panelesformularios = [self.F1_root,self.F2_root,self.F3_root]
        
    def FORMULARIOS(self,a):
        self.clear_widgets()
        self.add_widget(self.root)
                
    def FORM2(self,a):
        for i in self.panelesformularios:
            print i
            try:
               self.root.remove_widget(i)
               self.root.add_widget(self.F2_root) 
            except:
                pass

    def FORM1(self,a):
        for i in self.panelesformularios:
            print i
            try:
               self.root.remove_widget(i)
               self.root.add_widget(self.F1_root) 
            except:
                pass
    def TOMARREGISTRO(self,Button):
        self.textos = [self.Complemento1,self.Complemento2,self.Complemento3,self.Complemento4,self.Complemento5,self.Complemento6,self.Complemento7,self.Complemento8,self.Complemento9,self.Complemento10,self.Complemento11]
        with open('registro.txt', 'a') as file:
            textos_R = ""
            for i in self.textos:
                textos_R = textos_R + i.text + ","
            textos_R = """
"""+textos_R
            
            file.write(textos_R[:-1])
    def FORM3(self,a):
        self.clear_widgets()
        self.add_widget(self.ROOT_Navitagiondrawer1)
        self.A = GridLayout(cols = 3, size_hint = (None,None),width = 225, height = 75, pos=(0,25),spacing = 0)
        self.A.add_widget(ImageButton(source = self.icons + "Entypo_e744(2)_128.png",keep_ratio = False, allow_stretch = True))
        self.imgbtn2 = ImageButton(source = self.icons + "Entypo_e724(0)_128.png",keep_ratio = False, allow_stretch = True)
        self.imgbtn3 = ImageButton(source = self.icons + "Entypo_e746(3)_128.png",keep_ratio = False, allow_stretch = True)
        
        
        
        self.imgbtn3.bind(on_press = self.FORMULARIOS)
        self.imgbtn2.bind(on_press = self.marcar_direccion)
        
        
        self.A.add_widget(self.imgbtn2)
        self.A.add_widget(self.imgbtn3)
        self.A.add_widget(ImageButton(source = self.hud + "Negro.png",keep_ratio = False, allow_stretch = True,size_hint_y = None , height = 5))
        self.A.add_widget(ImageButton(source = self.hud + "Negro.png",keep_ratio = False, allow_stretch = True,size_hint_y = None , height = 5))
        self.imgbtn = ImageButton(source = self.hud + "Negro.png",keep_ratio = False, allow_stretch = True,size_hint_y = None , height = 5)
        self.A.add_widget(self.imgbtn)

        self.A.x = (Window.width / 2) - (225/2)

        self.add_widget(self.A)
        
        
        self.imgbtn4 = ImageButton(source = self.icons + "Entypo_e727(0)_128.png",keep_ratio = False, allow_stretch = True, size_hint = (None,None), size = (75,75), pos = (int(self.A.x),int(self.A.y) + 75))
        self.imgbtn4.bind(on_press = lambda j: self.ROOT_Navitagiondrawer1.toggle_state())
        self.add_widget(self.imgbtn4)
        

    def set_marker_position(self,mapview, marker):
        x, y = mapview.get_window_xy_from(marker.lat, marker.lon, mapview.zoom)
        marker.x = int(x - marker.width * marker.anchor_x)
        marker.y = int(y - marker.height * marker.anchor_y)
        if isinstance(marker, MapMarkerPopup):
            marker.placeholder.x = marker.x - marker.width / 2
            marker.placeholder.y = marker.y + marker.height

    def marcar_direccion(self,zz):
        puntoA = self.puntos[0]
        puntoB = self.puntos[1]
        if puntoA.lon > puntoB.lon:
            direccionx = puntoA.lon - puntoB.lon
        else:
            direccionx = puntoB.lon - puntoA.lon 
        
        if puntoA.lat > puntoB.lat:
            direcciony = puntoA.lat - puntoB.lat
        else:
            direcciony = puntoB.lat - puntoA.lat
            
            
        distanciax = direccionx/50
        distanciay = direcciony/50
        import math


        for i in range(50):
            print i
            puntox = distanciax*i
            puntoy = distanciay*i
            self.mv.add_marker(MapMarker(lat = self.puntos[1].lat + puntoy , lon = self.puntos[1].lon + puntox, source = self.icons + "Entypo_e78b(0)_32.png"))
        index = "https://maps.googleapis.com/maps/api/directions/json?"
        url = 'http://maps.googleapis.com/maps/api/directions/json'

        params = dict(
            origin= str(puntoA.lat)+","+str(puntoA.lon),
            destination=str(puntoB.lat)+","+str(puntoB.lon),
            sensor='false'
        )

        resp = requests.get(url=url, params=params)
        data = json.loads(resp.text)
                
        

    
class MyApp(App):
    def build(self):
        return InterfaceManager()


if __name__ in ('__main__', '__android__'):
    MyApp().run()
