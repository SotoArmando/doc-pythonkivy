#!/usr/bin/env python
# -*- coding: utf-8 -*-
from kivy.config import Config
Config.set('graphics','borderless',1)
Config.set('graphics','resizable',0)
Config.set('graphics','position','custom')
Config.set('graphics','left',500)
Config.set('graphics','top',0)
import kivy
#from kivy.garden.mapview import MapView, MapMarker, MarkerMapLayer, MapSource
from kivy.uix.bubble import Bubble
from kivy.uix.checkbox import CheckBox
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
from kivy.utils import get_hex_from_color, get_color_from_hex
from kivy.parser import parse_color
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
from kivy.uix.screenmanager import ScreenManager, Screen,SwapTransition, NoTransition,SlideTransition,FadeTransition,WipeTransition,FallOutTransition,RiseInTransition 
from kivy.lang import Builder
#from kivy.garden.mapview import MapView, MapMarker, MarkerMapLayer,MapSource
from kivy.uix.button import Button
from kivy.properties import StringProperty
from kivy.clock import Clock, mainthread
from kivy.uix.relativelayout import RelativeLayout
from kivy.app import App

import requests
import os   
import os.path
import time
import sys
import urllib2
import json, requests
import math

#from plyer import gps
from threading import Timer

Window.size = (426,750)
reload(sys)
sys.setdefaultencoding('latin1')
resource_add_path(os.path.dirname(__file__))

Window.size = (426,750)



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
                rgba: (1,1,1,.95)
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
                rgba: (1,1,1,root._anim_progress*root.main_panel_darkness)
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
class TextInputButton(ButtonBehavior, TextInput):
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
        '''If not already in state `state`, animates self.smoothly to it, taking
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
        NID = "[color=#404040]"
        NID2 = "[color=#ff3333]"
        self.patch = os.path.dirname(os.path.abspath(__file__))
        hud = self.patch + '/hud/'
        pantalla_principall = GridLayout(cols =2)
        
        menulateral= GridLayout(cols = 1)
        self.Button5 = Button(markup = True,font_size = 17,text = "Demasiado Duro para irse.",text_size =(Window.width-50, 25),size_hint = (None,None), pos = (0,Window.height), size = (Window.width, 50), background_normal = hud + "TT.png", allow_stretch = True , keep_ratio = False)
        #menulateral.add_widget(Image(text = "",font_size = 15,markup = True, size_hint = (1,None), height = 5, source = hud + "A6.png",keep_ratio = False , allow_stretch = True))
        datosgrid = GridLayout(cols = 2, row_default_height = 60, size_hint_y = None, height = 60)
        
        
        datosgrid.add_widget(Button(size_hint_y = 1 , size_hint_x = None , width = 60, background_normal = hud + "ICO10.png"))
        datosgrid.add_widget(Button(markup = True,font_size = 19,background_normal = hud + "A3.png", text = NID+"865.00 RD$", text_size = (126,30), halign = "left"))


        
        botonesgrid = ScrollView(size_hint_y = 1)
        botonesgrid_root = GridLayout(cols = 2, size_hint_y = None)
        botonesgrid_root.bind(minimum_height=botonesgrid_root.setter('height'))
        botonesgrid.add_widget(botonesgrid_root)
        
        botonesgrid2 = GridLayout(cols = 2, size_hint_y = None, height = 60)
        
        menulateral.add_widget(botonesgrid2)
        menulateral.add_widget(datosgrid)
        botonesgrid2.add_widget(Button(text = "",font_size = 14,markup = True, size_hint = (1,None), height = 60, background_normal = hud + "A10.png",background_down = hud + "A10.png",text_size = (130,25),halign = "left"))
        botonesgrid2.add_widget(Button(text = "",font_size = 14,markup = True, size_hint = (None,None),width = 60, height = 60, background_normal = hud + "ICO11.png"))
        
        menulateral.add_widget(botonesgrid)
        
        botonesgrid_root.add_widget(Image(text = "",font_size = 15,markup = True, size_hint = (None,None),width= 60, height = 5, source = hud + "A6.png",keep_ratio = False , allow_stretch = True))
        botonesgrid_root.add_widget(Image(text = "",font_size = 15,markup = True, size_hint = (1,None), height = 5, source = hud + "A6.png",keep_ratio = False , allow_stretch = True))

        for i in range(10):
            dim = GridLayout(rows = 3, size_hint_x = None, width = 60, size_hint_y = None, height = 70)
            dim.add_widget(Image(size_hint_y = None,height = 5 , size_hint_x = None , width = 60, source = hud + "A11.png", allow_stretch = True, keep_ratio = False))
            dim.add_widget(Image(size_hint_y = None,height = 60 , size_hint_x = None , width = 60, source = hud + "ICO12.png", allow_stretch = True, keep_ratio = False))
            dim.add_widget(Image(size_hint_y = None,height = 5 , size_hint_x = None , width = 60, source = hud + "A9.png", allow_stretch = True, keep_ratio = False))
            
            dim2 = GridLayout(rows = 2, size_hint_x = 1, width = 60, size_hint_y = None, height = 70)
            dim2.add_widget(Button(background_normal = hud + "A3.png", text = NID+"Agora Mall",markup = True, font_size = 17, text_size = (100,35), halign = "center"))
            dim2.add_widget(Button(background_normal = hud + "A12.png", text = NID+"Churros", markup = True, font_size = 13, text_size = (100,35), halign ="center", valign = "top"))
            botonesgrid_root.add_widget(dim)
            botonesgrid_root.add_widget(dim2)
        
        
        
        self.ROOT_Navitagiondrawer1 = NavigationDrawer()
        self.ROOT_Navitagiondrawer1.add_widget(menulateral)
        #self.ROOT_Navitagiondrawer1.add_widget(pantalla_principall)
        #self.ROOT_Navitagiondrawer1.add_widget(Button())
        self.add_widget(self.ROOT_Navitagiondrawer1)
        pantalla_principall.add_widget(Label(size_hint = (None,1), width = 100))
        pantalla_principall.add_widget(Label(text = "Botones 1"))
        
        pantalla_principall.add_widget(Button(size_hint = (None,1), width = 100,background_normal = hud + "A1.png"))
        pantalla_principall.add_widget(Button(background_normal = hud + "A1.png"))
        
        pantalla_principall.add_widget(Button(size_hint = (None,1), width = 100,background_normal = hud + "A1.png"))
        pantalla_principall.add_widget(Button(background_normal = hud + "A1.png"))

        pantalla_principall.add_widget(Label(size_hint = (None,1), width = 100))
        pantalla_principall.add_widget(Label(text = "Botones 2"))
        
        pantalla_principall.add_widget(Button(size_hint = (None,1), width = 100,background_normal = hud + "A1.png"))
        pantalla_principall.add_widget(Button(background_normal = hud + "A1.png"))

        pantalla_principall.add_widget(Button(size_hint = (None,1), width = 100,background_normal = hud + "A1.png"))
        pantalla_principall.add_widget(Button(background_normal = hud + "A1.png"))

        pantalla_principall.add_widget(Button(size_hint = (None,1), width = 100,background_normal = hud + "A1.png"))
        pantalla_principall.add_widget(Button(background_normal = hud + "A1.png"))

        self.sm = ScreenManager(size_hint = (1,1))
        #self.sm.transition = FadeTransition()
        pantalla = Screen(name='Armando2')
        self.pantalla3 = Screen(name='Armando3')
        pantalla4 = Screen(name='Catalogos')
        pantalla5 = Screen(name='Departamentos')
        pantalla6 = Screen(name='Lobby')
        pantalla7 = Screen(name='Perfil')
        pantalla2 = Screen(name='Armando')
        self.sm.add_widget(self.pantalla3)
        self.sm.add_widget(pantalla7)
        self.sm.add_widget(pantalla6)
        self.sm.add_widget(pantalla5)
        self.sm.add_widget(pantalla4)
        self.sm.add_widget(pantalla2)
        self.sm.add_widget(pantalla)
        self.sm.current = 'Armando3'
        
        pantalla7_root = ScrollView(size_hint = (1,1))
        pantalla7.add_widget(pantalla7_root)
        self.pantalla7_complementos = GridLayout(cols = 1, size_hint_y = None)
        self.pantalla7_complementos.bind(minimum_height = self.pantalla7_complementos.setter('height'))
        pantalla7_root.add_widget(self.pantalla7_complementos)
        pantalla7_relative = RelativeLayout(size_hint_y = None , height = 300)

        pantalla7_relative.add_widget(ImageButton(source = hud+"fondo2.png", allow_stretch = True, keep_ratio = False, pos=(0,50), size_hint = (None, None), height = 250, width = Window.width))
        dim30 = GridLayout(rows = 1, allow_stretch = True, keep_ratio = False, pos=(0,0), size_hint = (1, None), height = 50, width = Window.width, spacing = 0)
        pantalla7_relative.add_widget(dim30)
        dim30.add_widget(Button(font_size = 21,text_size = (Window.width-50-300,50), halign = "left", valign = "middle",text = "Spoiler",background_normal = hud + "fondo3.png", size_hint_y = None, height = 50))
        pantalla7_relative.add_widget(ImageButton(source = hud+"hudp.png", allow_stretch = True, keep_ratio = False, pos=(50,25), size_hint = (None, None), height = 100, width = 100))
        pantalla7_relative.add_widget(Button(font_size = 19,halign = "left",valign = "bottom",markup = True,text_size = (Window.width - 175,50),text = "[b]Empanadas Mañon",background_normal = hud+"TT3.png", allow_stretch = True, keep_ratio = False, pos=(50+100+25,50), size_hint = (None, None), height = (50), width = (Window.width - 175)))
        self.pantalla7_complementos.add_widget(pantalla7_relative)
      
        dim31 = GridLayout(cols = 4, spacing  = 0, size_hint_y = None , height = 250)
        for i in range(5):
            items = ["Horario","Domicilio","Metodos de Pago","Especialidad","Seguidores"]
            items2 = ["Lun - Vier","Disponible","Tarjeta o Efectivo","Empanadas","[b]9,905"]
            dim31.add_widget(Button(background_normal = hud+"23.png",text = "",markup = True, allow_stretch = True, keep_ratio = False, pos=(0,0), size_hint = (None, None), height = 50, width = 50))
            dim31.add_widget(Button(text_size = ((Window.width/2 )-50,25),background_normal = hud+"23.png",text = NID+"[b]"+str(items[i]),markup= True, allow_stretch = True, keep_ratio = False, pos=(0,0), size_hint = (1, None), height = 50, width = Window.width))
            dim31.add_widget(Button(text_size = ((Window.width/2 )-50,25),background_normal = hud+"23.png",text = NID+str(items2[i]),markup = True, allow_stretch = True, keep_ratio = False, pos=(0,0), size_hint = (1, None), height = 50, width = Window.width))
            dim31.add_widget(Button(background_normal = hud+"23.png",text = "",markup = True, allow_stretch = True, keep_ratio = False, pos=(0,0), size_hint = (None, None), height = 50, width = 50))

        self.pantalla7_complementos.add_widget(dim31)
        a1 = GridLayout(cols = 2, size_hint_y = None , spacing = 0)
        acont = GridLayout(cols = 3, size_hint_y = None, spacing = 0)
        acont.bind(minimum_height = acont.setter('height'))
        acont.add_widget(Image(source = hud+"a3.png",keep_ratio = False , allow_stretch = True, size_hint_y = 1 , height = 48, size_hint_x = None, width = 5))
        acont.add_widget(a1)
        acont.add_widget(Image(source = hud+"a3.png",keep_ratio = False , allow_stretch = True, size_hint_y = 1 , height = 48, size_hint_x = None, width = 5))
        
        self.Aplicarvista(a1,1)
        
        

       

        self.pantalla7_complementos.add_widget(acont)
        dim39 = GridLayout(cols = 2, size_hint_y = None, height = 225)
        self.pantalla7_complementos.add_widget(dim39)
        for i in range(4):
            if i == 0:
                pass
                dim39.add_widget(Image(source = hud+"fondo1.png", allow_stretch = True, keep_ratio = False, size_hint_y = None , height  =50))
                dim39.add_widget(Image(source = hud+"fondo1.png", allow_stretch = True, keep_ratio = False, size_hint_y = None , height  =50))
            p = ["Ubicacion","Teléfono","Horario","Email"]
            s = ["Calle Dr. Mario García Alvarado No.8","(809) 636-1020","Lun-Vie 9am a 6:30pm | Sab 9:00am a 3:00pm","info@guatapo.com"]
            dim39.add_widget(Button(text_size = ((Window.width/2)-50,40),valign ="middle",text = NID+"[b]"+p[i],markup = True, background_normal = hud+"fondo1.png", size_hint_y = None, height = 40))
            dim39.add_widget(Button(text_size = ((Window.width/2)-50,40),valign ="middle",text = NID+s[i],markup = True, background_normal = hud+"fondo1.png", size_hint_y = None, height = 40))
            
            dim39.add_widget(Image(source = hud+"blindbar1.png", allow_stretch = True, keep_ratio = False, size_hint_y = None , height  =1))
            dim39.add_widget(Image(source = hud+"blindbar1.png", allow_stretch = True, keep_ratio = False, size_hint_y = None , height  =1))
            
            if i == 3:
                dim39.add_widget(Image(source = hud+"fondo1.png", allow_stretch = True, keep_ratio = False, size_hint_y = None , height  =15))
                dim39.add_widget(Image(source = hud+"fondo1.png", allow_stretch = True, keep_ratio = False, size_hint_y = None , height  =15))

    
        

       
        
        
        
        pantalla6_root = ScrollView(size_hint = (1,1))
        pantalla6.add_widget(pantalla6_root)
        pantalla6_complementos = GridLayout(cols = 1, size_hint_y = None)
        pantalla6_complementos.bind(minimum_height = pantalla6_complementos.setter('height'))
        #pantalla6_root.add_widget(pantalla6_complementos)
        
        #pantalla6_complementos.add_widget(Image(source = hud+"fondo2.png",keep_ratio = False , allow_stretch = True, size_hint_y = None , height = 48, size_hint_x = 1, width = 20))
        pantalla6_complementos.add_widget(TextInput(background_normal = hud+"fondo1.png",background_active = hud+"fondo1.png",padding =[30,30,0,0],text = "Que estas pensando?",size_hint = (1,None), size = (1,150)))
        #pantalla6_complementos.add_widget(Image(size_hint_y = None, height = 1, source =hud+ "blindbar1.png", keep_ratio = False , allow_stretch = True))
        dim7 = GridLayout(cols =2 , size_hint_x = 1 ,size_hint_y = None , height = 30)
        pantalla6_complementos.add_widget(dim7)
        dim7.add_widget(Button(background_normal = hud+"fondo1.png"))
        dim7.add_widget(Button(background_normal = hud+"A20.png",markup = True, text = "[color=#bfbfbf]"+"Publicar",size_hint_x = None , width =150, font_size = 14, text_size = (100,30), valign = "middle", halign = "center"))
        
        for i in range(10):
            dim17= GridLayout(cols = 2, size_hint_y = None, size_hint_x = 1 , height = 70)
            
            dim17.add_widget(ImageButton(size_hint = (None,None),width = 45, height = 45, source = hud + "ICO40.png", keep_ratio  = False , allow_stretch = True))
            
            dim17.add_widget(Button(markup = True,text = NID+"Nuestra primera portada!! :D",font_size = 17,text_size = ((Window.width * 0.9)-75, 30),halign = "left",valign = "bottom",size_hint = (1,None), height = 45 ,background_normal = hud + "fondo1.png", keep_ratio = False , allow_stretch = True))
            
            dim17.add_widget(ImageButton(size_hint = (None,None),width = 45, height = 25, source = hud + "fondo1.png", keep_ratio  = False , allow_stretch = True))
            dim17.add_widget(Button(markup = True,text = NID+"Hace 1 Semana",font_size = 14,text_size = ((Window.width * 0.9)-75, 30),halign = "left",valign = "top",size_hint = (1,None), height = 25 ,background_normal = hud + "fondo1.png", keep_ratio = False , allow_stretch = True))
            
            #pantalla6_complementos.add_widget(Image(size_hint_y = None, height = 5, source =hud+ "fondo1.png", keep_ratio = False , allow_stretch = True))
            pantalla6_complementos.add_widget(Image(size_hint_y = None, height = 1, source =hud+ "blindbar1.png", keep_ratio = False , allow_stretch = True))
            pantalla6_complementos.add_widget(dim17)
            pantalla6_complementos.add_widget(Image(size_hint_y = None, height = Window.width, source =hud+ "fondo2.png", keep_ratio = False , allow_stretch = True))
            
            dim19 = GridLayout(cols =4 , size_hint_y = None , height = 35)
            
            for i in range(3):
                if i == 0:
                    dimtemp1 = GridLayout(cols = 2, size_hint_y = None, height = 40, size_hint_x = None, width = 15)
                    dimtemp1.add_widget(Image(allow_stretch = True, keep_ratio = False,source =  hud+"fondo1.png",size_hint_y = 1 , height = 35,size_hint_x = 1 , width = 35,markup = True,font_size = 17,  text  ="", text_size = (Window.width-50-64, 32)))
                    dimtemp1.add_widget(Image(allow_stretch = True, keep_ratio = False,source =  hud+"fondo1.png",size_hint_y = 1 , height = 35,size_hint_x = 1 , width = 35,markup = True,font_size = 17,  text  ="", text_size = (Window.width-50-64, 32)))
                    dim19.add_widget(dimtemp1)
                images = ["ICO26","ICO19","ICO27"]
                textemp =  ["Me Gusta","Compartir","Comentar"]
                dimtemp = GridLayout(cols = 2, size_hint_y = None, height = 40)
                dimtemp.add_widget(Image(allow_stretch = True, keep_ratio = False,source =  hud+images[i]+".png",size_hint_y = None , height = 35,size_hint_x = None , width = 35,markup = True,font_size = 17,  text  ="", text_size = (Window.width-50-64, 32)))
                dimtemp.add_widget(Button(markup = True,text =NID+ textemp[i], background_normal = hud + "fondo1.png",background_down= hud + "fondo2.png",text_size = ((Window.width/3)-50,22.5)))
                dim19.add_widget(dimtemp)


            
            pantalla6_complementos.add_widget(Image(size_hint_y = None, height = 5, source =hud+ "fondo1.png", keep_ratio = False , allow_stretch = True))
            pantalla6_complementos.add_widget(dim19)
            pantalla6_complementos.add_widget(Image(size_hint_y = None, height = 15, source =hud+ "fondo1.png", keep_ratio = False , allow_stretch = True))
            pantalla6_complementos.add_widget(Button(halign = "left",valign = "middle",font_size = 16,size_hint_y = None, height = 90,text_size = (Window.width-50, 90),markup = True, text = NID+"Hoy fue el cumpleaños de mi mama!!\narmando soso\n@[b]sosodross\n9.877 Me Gusta", background_normal =hud+ "fondo1.png", background_active =hud+ "fondo1.png", keep_ratio = False , allow_stretch = True))
            #pantalla6_complementos.add_widget(Button(font_size = 17,size_hint_y = None, height = 30,text_size = (Window.width-50, 12.5),markup = True, text = NID+"", background_normal =hud+ "fondo1.png", keep_ratio = False , allow_stretch = True))
            textentry = Button(text_size = (Window.width-50,150),foreground_color = [0,0,0,.50],valign = "middle",halign = "center",font_size = 16,markup = True,text = NID+"hola chavales, espero que hayan tenido un gran dia. :)",size_hint = (1,None), height = 75,background_normal= hud+"fondo1.png",background_active= hud+"fondo1.png")
            #pantalla6_complementos.add_widget(Button(size_hint_y = None, height = 40,text_size = (Window.width-50, 20),markup = True, text = NID+"[b]9.877 Me Gusta", background_normal =hud+ "fondo1.png", keep_ratio = False , allow_stretch = True))
            pantalla6_complementos.add_widget(textentry)
            content3 = GridLayout(cols = 1, spacing = 0, size_hint_y = None , height = 240 )
            for i in range(5):
                textos = ["Me Gusta","Comentar","Compartir","Perfil","Editar"]
                dim21 = GridLayout(cols = 5, size_hint_y = None , height = 48, spacing = 0)
                dim21.add_widget(Image(size_hint_x = None , width = 48, source = hud+"fondo1.png"))
                dim21.add_widget(Image(allow_stretch = True , keep_ratio = False,size_hint_x = None , width = 1, source = hud+"blindbar1.png"))
                dim21.add_widget(Image(size_hint_x = None , width = 48, source = hud+"ICO30.png"))
                dim21.add_widget(Image(allow_stretch = True , keep_ratio = False,size_hint_x = None , width = 1, source = hud+"blindbar1.png"))
                dim21.add_widget(Button(background_normal = hud +"fondo1.png",markup = True, text = NID+textos[i], text_size = ((Window.width)-48-50-50,24)))
                content3.add_widget(dim21)
                content3.add_widget(Image(allow_stretch = True , keep_ratio = False,size_hint_y = None , height = 1, source = hud+"blindbar1.png"))
                
                
            self.a = ScreenManager(size_hint = (None, None) ,height = 201, width = 107, transition = SlideTransition(direction ="up"))
            c = Screen(name= "c")
            b = Screen(name= "b")
            self.a.add_widget(c)
            self.a.add_widget(b)
        

        
            DropD = DropDown(auto_width = False , width = 107, auto_dismiss = False)
            DropD.add_widget(self.a)
            cont_b = GridLayout(cols = 1, size_hint_x = None , width =107, height = 201, size_hint_y = None)
            b.add_widget(cont_b)
            cont_b.add_widget(Image(allow_stretch = True, keep_ratio = False,size_hint = (1,None), height = 1  , source = hud + "blindbar1.png",markup = True, text = NID+"", font_size = 14   ))
            button1 = Button(size_hint = (1,None), height = 50 , background_normal = hud + "A17.png",markup = True,text = NID+"Abrir", font_size = 14)
            cont_b.add_widget(button1)
            button1.bind(on_release = lambda x : self.definir("c"))
            cont_b.add_widget(Button(size_hint = (1,None), height = 50  , background_normal = hud + "A17.png",markup = True, text = NID+"Me Gusta", font_size = 14))        
            cont_b.add_widget(Button(size_hint = (1,None), height = 50  , background_normal = hud + "A17.png",markup = True, text = NID+"Comentarios", font_size = 14))
            cont_b.add_widget(Button(size_hint = (1,None), height = 50  , background_normal = hud + "A17.png",markup = True, text = NID+"Etiquetar", font_size = 14))        
            
            button2 = Button(size_hint = (1,None), height = 201, background_normal = hud + "TT3.png", keep_ratio  = False , allow_stretch = True,markup = True,text = NID+"")
            c.add_widget(button2)
            button2.bind(on_release =lambda x : self.definir("b"))
            self.a.current = "c"
            
            
            
            def abrir(x):
                if self.a.current == "c":
                    DropD.open(x)
                    DropD.dismiss
                    x.disabled = True
                    def activar():
                        x.disabled = False
                    t2 = Timer(0.5, activar)
                    t2.start()
                    print DropD.attach_to.pos
                    print DropD.pos
                    DropD.open(x)
                   
                    self.a.transition = FadeTransition(direction ="up", clearcolor = [1,1,1,0])
                    self.a.current = "b"
                elif self.a.current == "b":
                    x.disabled = True
                    def activar():
                        x.disabled = False
                    self.a.transition = FadeTransition(direction ="down", clearcolor = [1,1,1,0])
                    self.a.current = "c"
                    t = Timer(0.3, DropD.dismiss)
                    t2 = Timer(0.45, activar)
                    t.start()
                    t2.start()

                    
                    
                    
                    
            self.Popup = Popup(pos_hint={'right': 1.05, 'top': .388},size_hint = (1.0755,None), size_hint_y = None , height = 375, separator_color = [1,1,1,0], content =content3, separator_height = 0 ,title_size = 0, title = "",background =hud+"TT2.png")
            for i in range(2):
                dim24 = GridLayout(cols = 4,size_hint_y = None , height = 90)
                if i == 0: 
                    dim25 = GridLayout(cols = 1, size_hint_x = None , width = 90, size_hint_y = None , height = 90)
                    dim24.add_widget(Button(background_normal = hud + "fondo5.png",markup = True,text = "" , size_hint_x = None , width = 40, text_size = (80,75),halign = "right", valign = "top"))
                    #dim24.add_widget(Image(allow_stretch = True , keep_ratio = False,size_hint_x = None , width = 1, source = hud+"blindbar1.png"))
                    dim24.add_widget(TextInput(foreground_color = [0,0,0,.35],auto_indent = True,padding = [25 ,25,0,0],width = 300,markup = True,text = "Escribe tu opinion :)",size_hint = (None,None),height = 90,background_normal= hud+"fondo1.png",background_active= hud+"fondo1.png"))
                    #dim24.add_widget(Image(allow_stretch = True , keep_ratio = False,size_hint_x = None , width = 1, source = hud+"blindbar1.png"))
                    

                    dim25.add_widget(ImageButton(source = hud + "ICO42.png",markup = True,text = "" , size_hint_y = None, height = 90, width = 90, text_size = (80,75),halign = "right", valign = "top"))
                    dim24.add_widget(dim25)
                    
                    
                    dim24.add_widget(Button(background_normal = hud + "fondo1.png",markup = True,text = "" , size_hint_x = None , width = 20, text_size = (80,75),halign = "right", valign = "top"))
                    pantalla6_complementos.add_widget(Image(allow_stretch = True , keep_ratio = False,size_hint_y = None , height = 1, source = hud+"blindbar1.png"))
                    dim26 = GridLayout(cols = 4, size_hint_y = None , height = 10)
                    dim26.add_widget(Image(allow_stretch = True, keep_ratio = False,source = hud + "fondo2.png",markup = True,text = "" ,size_hint_y = None , height = 10, size_hint_x = None , width = 40, text_size = (80,75),halign = "right", valign = "top"))
                    dim26.add_widget(Image(allow_stretch = True , keep_ratio = False,size_hint_x = None , width = 1, source = hud+"blindbar1.png"))
                    dim26.add_widget(Image(allow_stretch = True , keep_ratio = False,size_hint_x = None , width = 24, source = hud+"M12.png"))
                    dim26.add_widget(Image(allow_stretch = True , keep_ratio = False,size_hint_y = None , height = 10, source = hud+"fondo2.png"))
                    #pantalla6_complementos.add_widget(dim26)
                    #pantalla6_complementos.add_widget(dim24)
                    #pantalla6_complementos.add_widget(Image(allow_stretch = True , keep_ratio = False,size_hint_y = None , height = 1, source = hud+"blindbar1.png"))
                    
                dim18 = GridLayout(cols = 3,size_hint_y = None , height = 135)
                textentry2 = Button(width = 300,markup = True,text = NID+"[b]@User[/b] Ha sido un buen lugar, no me molestaria pasar denuevo. probando la segunda linea.",size_hint = (1,None),background_normal= hud+"A19.png", text_size = (Window.width-40-40-48,75),valign ="middle")
                textentry3 = Button(width = 48,markup = True,text = NID+"",size_hint = (None,None),background_normal= hud+"ICO16.png", text_size = (Window.width-50-40-40,75),valign ="middle")
                textentry2.height =75
 
                textentry2.bind(on_release =lambda x = textentry2: abrir(x))    
                
                dim18.add_widget(Button(background_normal = hud + "fondo4.png",text = NID+"1",markup = True, size_hint_x = None , width = 40, text_size = (80,15),halign = "right", valign = "top"))
                dim23 = GridLayout(cols = 1, size_hint_y = None , height = 30)
                dim23.add_widget(Button(height = 30,markup = True,text = NID+"[b]99 Me Gusta[/b]",size_hint = (1,None),background_normal= hud+"A19.png", text_size = ((Window.width-40-40-48),75),valign ="middle"))
                dim18.add_widget(dim23)
                dim18.add_widget(Button(background_normal = hud + "fondo4.png",text = NID+"3",markup = True, size_hint_x = None , width = 40, text_size = (80,15),halign = "right", valign = "top"))
                
                
                
                dim18.add_widget(Button(background_normal = hud + "fondo4.png",markup = True,text = "" , size_hint_x = None , width = 40, text_size = (80,75),halign = "right", valign = "top"))
                dim18.add_widget(textentry2)
                dim18.add_widget(Button(background_normal = hud + "fondo4.png",markup = True,text = "" , size_hint_x = None , width = 40, text_size = (80,75),halign = "right", valign = "top"))
                
                dim18.add_widget(Button(background_normal = hud + "fondo4.png",text = NID+"1",markup = True, size_hint_x = None , width = 40, text_size = (80,15),halign = "right", valign = "top"))
                dim22 = GridLayout(cols = 2, size_hint_y = None , height = 30)
                dim22.add_widget(Button(height = 30,markup = True,text = NID+"Me Gusta",size_hint = (1,None),background_normal= hud+"A19.png", text_size = ((Window.width-50-40-40-48)/2,75),valign ="middle"))
                dim22.add_widget(Button(height = 30,markup = True,text = NID+"Responder",size_hint = (1,None),background_normal= hud+"A19.png", text_size = ((Window.width-50-40-40-48)/2,75),valign ="middle"))
                dim18.add_widget(dim22)
                dim18.add_widget(Button(background_normal = hud + "fondo4.png",text = NID+"3",markup = True, size_hint_x = None , width = 40, text_size = (80,15),halign = "right", valign = "top"))
                
                #pantalla6_complementos.add_widget(Image(size_hint_y = None, height = 1, source =hud+ "blindbar1.png", keep_ratio = False , allow_stretch = True))
                pantalla6_complementos.add_widget(Image(size_hint_y = None, height = 15, source =hud+ "fondo4.png", keep_ratio = False , allow_stretch = True))
                
                pantalla6_complementos.add_widget(dim18)
                if i == 1:
                    dim27 = GridLayout(cols = 3,size_hint_y = None , height = 120)
                    textentry2 = TextInput(width = 300,markup = True,foreground_color = [0,0,0,.35],padding = [25,25,0,0],text = "Danos tu opinon :)",size_hint = (1,None),background_normal= hud+"A21.png",background_active= hud+"A21.png", text_size = (Window.width-50-40-40-48,75),valign ="middle")
                    textentry3 = Button(width = 48,markup = True,text = NID+"",size_hint = (None,None),background_normal= hud+"ICO16.png", text_size = (Window.width-50-40-40,75),valign ="middle")
                    textentry2.height =90
     
                    textentry2.bind(on_release =lambda x = textentry2: abrir(x))    
                    
                    dim27.add_widget(Button(background_normal = hud + "fondo4.png",text = NID+"1",markup = True, size_hint_x = None , width = 40, text_size = (80,15),halign = "right", valign = "top"))
                    dim28 = GridLayout(cols = 1, size_hint_y = None , height = 30)
                    dim28.add_widget(Button(height = 30,markup = True,text = NID+"",size_hint = (1,None),background_normal= hud+"A21.png", text_size = ((Window.width-50-40-40-48),75),valign ="middle"))
                    dim27.add_widget(dim28)
                    dim27.add_widget(Button(background_normal = hud + "fondo4.png",text = NID+"3",markup = True, size_hint_x = None , width = 40, text_size = (80,15),halign = "right", valign = "top"))
                    
                    
                    
                    dim27.add_widget(Button(background_normal = hud + "fondo4.png",markup = True,text = "" , size_hint_x = None , width = 40, text_size = (80,75),halign = "right", valign = "top"))
                    dim27.add_widget(textentry2)
                    dim27.add_widget(Button(background_normal = hud + "fondo4.png",markup = True,text = "" , size_hint_x = None , width = 40, text_size = (80,75),halign = "right", valign = "top"))
                    
                    #dim27.add_widget(Button(background_normal = hud + "fondo4.png",text = NID+"1",markup = True, size_hint_x = None , width = 40, text_size = (80,15),halign = "right", valign = "top"))
                    dim29 = GridLayout(cols = 2, size_hint_y = None , height = 30)
                    dim29.add_widget(Button(height = 30,markup = True,text = NID+"Me Gusta",size_hint = (1,None),background_normal= hud+"A21.png", text_size = ((Window.width-50-40-40-48)/2,75),valign ="middle"))
                    dim29.add_widget(Button(height = 30,markup = True,text = NID+"Responder",size_hint = (1,None),background_normal= hud+"A21.png", text_size = ((Window.width-50-40-40-48)/2,75),valign ="middle"))
                    #dim27.add_widget(dim29)
                    #dim27.add_widget(Button(background_normal = hud + "fondo4.png",text = NID+"3",markup = True, size_hint_x = None , width = 40, text_size = (80,15),halign = "right", valign = "top"))
                    
                    #pantalla6_complementos.add_widget(Image(size_hint_y = None, height = 1, source =hud+ "blindbar1.png", keep_ratio = False , allow_stretch = True))
                    pantalla6_complementos.add_widget(Image(size_hint_y = None, height = 15, source =hud+ "fondo4.png", keep_ratio = False , allow_stretch = True))
                    
                    pantalla6_complementos.add_widget(dim27)
                
                    pantalla6_complementos.add_widget(Image(size_hint_y = None, height = 15, source =hud+ "fondo4.png", keep_ratio = False , allow_stretch = True))
                    dim20 = GridLayout(cols = 3, size_hint_y = None , height = 16)
                    dim20.add_widget(Image(size_hint_y = 1, height = 16, source =hud+ "fondo4.png", keep_ratio = False , allow_stretch = True))
                    dim20.add_widget(Image(size_hint_y = None, height = 16, source =hud+ "M.png", keep_ratio = False , allow_stretch = True, size_hint_x = None , width = 300))
                    dim20.add_widget(Image(size_hint_y = 1, height = 16, source =hud+ "fondo4.png", keep_ratio = False , allow_stretch = True))
                    pantalla6_complementos.add_widget(dim20)
                    pantalla6_complementos.add_widget(Image(size_hint_y = None, height = 15, source =hud+ "fondo4.png", keep_ratio = False , allow_stretch = True))
                    
                    
                
            #pantalla6_complementos.add_widget(Image(size_hint_y = None, height = 1, source =hud+ "blindbar1.png", keep_ratio = False , allow_stretch = True))
            
		
		
		
		
        pantalla5_root = ScrollView(size_hint = (1,1))
        pantalla5.add_widget(pantalla5_root)
        pantalla5_complementos = GridLayout(cols = 1, size_hint_y = None)
        pantalla5_complementos.bind(minimum_height = pantalla5_complementos.setter('height'))
        pantalla5_root.add_widget(pantalla5_complementos)
        pantalla5_complementos.add_widget(Image(source = hud+"fondo2.png",keep_ratio = False , allow_stretch = True, size_hint_y = None , height = 48, size_hint_x = 1, width = 20))
        
        dim15 = GridLayout(cols = 3, size_hint_y = None , height = 64)
        dim15.add_widget(Image(allow_stretch = True, keep_ratio = False,source =  hud+"ICO38.png",size_hint_y = None , height = 64,size_hint_x = None , width = 64,markup = True,font_size = 17,  text  ="", text_size = (Window.width-50-64, 32)))
        dim15.add_widget(Button(background_normal =  hud+"fondo2.png",size_hint_y = None , height = 70,markup = True, text  = "Departamentos", font_size = 20, text_size = (Window.width-50-64-64, 30)))
        button7 = ImageButton(allow_stretch = True, keep_ratio = False, source=  hud+"ICO39.png",size_hint_y = None , height = 64,size_hint_x = None , width = 64,markup = True,font_size = 17,  text  ="", text_size = (Window.width-50-64, 32))
        dim15.add_widget(button7)
        button7.bind(on_press = lambda x : self.cambiar('Armando'))
        pantalla5_complementos.add_widget(dim15)
        pantalla5_complementos.add_widget(Image(source = hud+"fondo2.png",keep_ratio = False , allow_stretch = True, size_hint_y = None , height = 15, size_hint_x = 1, width = 20))
        
        Departamentos = ["Joyerias","Mercados","Vestimentas","Calzado","Relojes","Otras Prendas"]
        for i in Departamentos:
            if i == Departamentos[0]:
                pantalla5_complementos.add_widget(Button(background_normal =  hud+"fondo1.png",size_hint_y = None , height = 15,markup = True,font_size = 17,  text  ="", text_size = (Window.width-50, 17.5)))

            dim16 = GridLayout(cols = 3, size_hint_y = None , height = 64)
            dim16.add_widget(Button(background_normal =  hud+"ICO34.png",size_hint_y = None , height = 64,size_hint_x = None , width = 64,markup = True,font_size = 17,  text  ="", text_size = (Window.width-50-64, 32)))
            dim16.add_widget(Button(background_normal =  hud+"fondo1.png",size_hint_y = None , height = 64,markup = True,font_size = 17,  text  =NID+ i , text_size = (Window.width-50-64-64, 32)))
            dim16.add_widget(Button(background_normal =  hud+"ICO36.png",size_hint_y = None , height = 64,size_hint_x = None , width = 64,markup = True,font_size = 17,  text  ="", text_size = (Window.width-50-64, 32)))
            pantalla5_complementos.add_widget(dim16)
            pantalla5_complementos.add_widget(Image(size_hint_y = None ,size_hint_x = None, width = Window.width  , height = Window.width , keep_ratio = True, allow_stretch = True, source = hud+"ICOBEBIDAS.jpg"))
            if i == Departamentos[len(Departamentos)-1]:
                pass
            else:
                pantalla5_complementos.add_widget(Image(source = hud + "blindbar1.png", size_hint_y = None , height = 1,keep_ratio =False , allow_stretch = True))
                
        pantalla4_root = ScrollView(size_hint = (1,1))
        pantalla4.add_widget(pantalla4_root)
        pantalla4_complementos = GridLayout(cols = 1, size_hint_y = None)
        pantalla4_complementos.bind(minimum_height = pantalla4_complementos.setter('height'))
        pantalla4_root.add_widget(pantalla4_complementos)
        IMG= ["ICOPIZZA","ICOHAMBURGER","ICOPASTEL","ICODONAS","ICOPOLLOFRITO","ICOCAFEYPOSTRE","ICOSANDWICH","ICOCHINA","ICOHELADO"]
        Restaurantes = ["Pizzas","Hamburguesas","Pasteles","Donas","Pollo Frito","Cafe y Postres","Sandwiches","Comida China","Helado"]
        pantalla4_complementos.add_widget(Image(source = hud+"fondo2.png",keep_ratio = False , allow_stretch = True, size_hint_y = None , height = 48, size_hint_x = 1, width = 20))
        
        dim14 = GridLayout(cols = 3, size_hint_y = None , height = 64)
        dim14.add_widget(Image(allow_stretch = True, keep_ratio = False,source =  hud+"ICO37.png",size_hint_y = None , height = 64,size_hint_x = None , width = 64,markup = True,font_size = 17,  text  ="", text_size = (Window.width-50-64, 32)))
        dim14.add_widget(Button(background_normal =  hud+"fondo2.png",size_hint_y = None , height = 70,markup = True, text  = "Gastronomia", font_size = 20, text_size = (Window.width-50-64-64, 30)))
        button6 = ImageButton(allow_stretch = True, keep_ratio = False, source=  hud+"ICO39.png",size_hint_y = None , height = 64,size_hint_x = None , width = 64,markup = True,font_size = 17,  text  ="", text_size = (Window.width-50-64, 32))
        dim14.add_widget(button6)
        button6.bind(on_press = lambda x : self.cambiar('Armando'))
        pantalla4_complementos.add_widget(dim14)
        pantalla4_complementos.add_widget(Image(source = hud+"fondo2.png",keep_ratio = False , allow_stretch = True, size_hint_y = None , height = 15, size_hint_x = 1, width = 20))
        for i in Restaurantes:
            if i == Restaurantes[0]:
                pantalla4_complementos.add_widget(Button(background_normal =  hud+"fondo1.png",size_hint_y = None , height = 15,markup = True,font_size = 17,  text  ="", text_size = (Window.width-50, 17.5)))

            dim13 = GridLayout(cols = 3, size_hint_y = None , height = 64)
            dim13.add_widget(Button(background_normal =  hud+"ICO34.png",size_hint_y = None , height = 64,size_hint_x = None , width = 64,markup = True,font_size = 17,  text  ="", text_size = (Window.width-50-64, 32)))
            dim13.add_widget(Button(background_normal =  hud+"fondo1.png",size_hint_y = None , height = 64,markup = True,font_size = 17,  text  =NID+ i , text_size = (Window.width-50-64-64, 32)))
            button8 = Button(background_normal =  hud+"ICO36.png",size_hint_y = None , height = 64,size_hint_x = None , width = 64,markup = True,font_size = 17,  text  ="", text_size = (Window.width-50-64, 32))
            dim13.add_widget(button8)
            pantalla4_complementos.add_widget(dim13)
            pantalla4_complementos.add_widget(Image(size_hint_y = None ,size_hint_x = None, width = Window.width  , height = Window.width , keep_ratio = True, allow_stretch = True, source = hud+IMG[(Restaurantes.index(i))]+".jpg"))
            
            if i == Restaurantes[0]:
				button8.bind(on_release = lambda x : self.cambiar('Lobby'))
				
            if i == Restaurantes[len(Restaurantes)-1]:
                pass
            else:
                pantalla4_complementos.add_widget(Image(source = hud + "blindbar1.png", size_hint_y = None , height = 1,keep_ratio =False , allow_stretch = True))
            

        pantalla4_complementos.add_widget(Image(source = hud+"fondo1.png",keep_ratio = False , allow_stretch = True, size_hint_y = None , height = 15, size_hint_x = 1, width = 20))
        pantalla4_complementos.add_widget(Image(source = hud+"A18.png",keep_ratio = False , allow_stretch = True, size_hint_y = None , height = 15, size_hint_x = 1, width = 20))
        
       
        def limpiartext(widget):
            widget.text = ""
            
            
        
        self.pantalla3_grid = GridLayout(cols = 1, size_hint = (1,None), height = Window.height+1)
        self.pantalla3_grid.add_widget(Image(source = hud+"fondo2.png",keep_ratio = False , allow_stretch = True))
        self.pantalla3_grid.add_widget(Button(background_normal = hud+"fondo2.png",text = "Inntag", size_hint_y = None , height = 70, text_size = (Window.width-50, 35), font_size = 21))
        self.pantalla3_grid.add_widget(Image(source = hud+"fondo1.png",size_hint_y = None, height = 15,keep_ratio = False , allow_stretch = True))
        dim8 = GridLayout(cols = 3, size_hint_y  = None, height = 111)
        dim8.add_widget(Image(source = hud+"fondo1.png",keep_ratio = False , allow_stretch = True, size_hint_y = None , height = 48, size_hint_x = None, width = 20))
        dim8.add_widget(Image(source = hud+"ICO26.png", size_hint = (None,None), height = 48, width = 48, anim_delay = 0.030))
        TextInput1 = TextInputButton(padding = [30,17,0,0],background_normal = hud+"fondo1.png", background_active = hud+"fondo1.png", size_hint = (1,None), height = 48, width = 48, text = "Usuario")
        dim8.add_widget(TextInput1)
        TextInput1.bind(on_release = lambda x = 1 :limpiartext(TextInput1))
        
        dim8.add_widget(Image(source = hud+"fondo1.png",keep_ratio = False , allow_stretch = True, size_hint_y = None , height = 15, size_hint_x = None, width = 20))
        dim8.add_widget(Image(source = hud+"fondo1.png",keep_ratio = False , allow_stretch = True, size_hint_y = None , height = 15, size_hint_x = None, width = 48))
        dim8.add_widget(Image(source = hud+"fondo1.png",keep_ratio = False , allow_stretch = True, size_hint_y = None , height = 15, size_hint_x = 1))
        
        dim8.add_widget(Image(source = hud+"fondo1.png",keep_ratio = False , allow_stretch = True, size_hint_y = None , height = 48, size_hint_x = None, width = 20))
        dim8.add_widget(Image(source = hud+"ICO27.png", size_hint = (None,None), height = 48, width = 48))
        TextInput2 = TextInputButton(padding = [30,17,0,0],background_normal = hud+"fondo1.png", background_active = hud+"fondo1.png", size_hint = (1,None), height = 48, width = 48, text = "Contraseña", password = True)
        dim8.add_widget(TextInput2)
        TextInput2.bind(on_release = lambda x = 1 :limpiartext(TextInput2))
        
        self.pantalla3_grid.add_widget(dim8)
        self.pantalla3_grid.add_widget(Image(source = hud+"fondo1.png",keep_ratio = False , allow_stretch = True, size_hint_y = None , height = 35))
        dim10 = GridLayout(cols = 3, size_hint_y = None , height = 120)
        dim10.add_widget(Image(source = hud+"fondo1.png",keep_ratio = False , allow_stretch = True, size_hint_y = None , height = 30, size_hint_x = None, width = 30))
        dim10.add_widget(CheckBox(text ="Iniciar como Invitado.",size_hint_x = None , width = 30, size_hint_y = None , height = 30))
        dim10.add_widget(Button(font_size = 14,text_size = ((Window.width-30-50),15),halign = "left",markup = True,text = NID +"Recordar Contraseña",size_hint_x = 1 , width = 20, size_hint_y = None , height = 30, background_normal = hud + "fondo1.png"))
        
        dim10.add_widget(Image(source = hud+"fondo1.png",keep_ratio = False , allow_stretch = True, size_hint_y = None , height = 30, size_hint_x = None, width = 30))
        dim10.add_widget(CheckBox(text ="Recordar Contraseña.",size_hint_x = None , width = 30, size_hint_y = None , height = 30))
        dim10.add_widget(Button(font_size = 14,text_size = ((Window.width-30-50),15),halign = "left",markup = True,text = NID +"Inicio Automàtico.",size_hint_x = 1 , width = 20, size_hint_y = None , height = 30, background_normal = hud + "fondo1.png"))
        
        dim10.add_widget(Image(source = hud+"fondo1.png",keep_ratio = False , allow_stretch = True, size_hint_y = None , height = 30, size_hint_x = None, width = 30))
        dim10.add_widget(CheckBox(text ="Inicio Automàtico.",size_hint_x = None , width = 30, size_hint_y = None, height = 30))
        dim10.add_widget(Button(font_size = 14,text_size = ((Window.width-30-50),15),halign = "left",markup = True,text = NID +"Iniciar como Invitado.",size_hint_x = 1 , width = 20, size_hint_y = None , height = 30, background_normal = hud + "fondo1.png"))
        
        dim10.add_widget(Image(source = hud+"fondo1.png",keep_ratio = False , allow_stretch = True, size_hint_y = None , height = 30, size_hint_x = None, width = 30))
        dim10.add_widget(Image(source = hud+"fondo1.png",keep_ratio = False , allow_stretch = True, size_hint_y = None , height = 30, size_hint_x = None, width = 30))
        dim10.add_widget(Button(font_size = 14,text_size = ((Window.width-30-50),15),halign = "left",markup = True,text = NID +"No tienes cuenta? [b]Registrate",size_hint_x = 1 , width = 20, size_hint_y = None , height = 30, background_normal = hud + "fondo1.png"))
        
        self.pantalla3_grid.add_widget(dim10)

        self.pantalla3_grid.add_widget(Image(source = hud+"fondo1.png",keep_ratio = False , allow_stretch = True, size_hint_y = None , height = 15))
        dim9 = GridLayout(cols = 2,size_hint_y = None, height = 70)
        button3 = Button(text = NID+"Ingresar",background_normal = hud+"fondo1.png", markup = True)
        button3.bind(on_release = lambda x : self.cambiar("Armando"))
        dim9.add_widget(button3)
        Inicio = Button(text = NID+"Salir",background_normal = hud+"fondo1.png",markup = True)
        Inicio.bind(on_release = self.loading   )
        dim9.add_widget(Inicio)
        
        self.pantalla3_grid.add_widget(dim9)
        self.pantalla3_grid.add_widget(Image(source = hud+"fondo2.png",keep_ratio = False , allow_stretch = True))
        self.pantalla3.add_widget(self.pantalla3_grid)
        
        
        pantalla_grid = GridLayout(cols = 3,row_default_height = 60)
        boton = Button(size_hint_x = None, width = 60, background_normal = hud + "ICO1.png")
        boton.bind(on_press = lambda x : self.cambiar("Armando"))
        pantalla_grid.add_widget(boton)
        pantalla_grid.add_widget(Button(font_size = 15,text_size = (250,28),halign = "left",text = "[color=#404040][b]Explorer",background_normal = hud + "A4.png",markup = True))
        pantalla_grid.add_widget(Button(size_hint_x = None ,width = 60,background_normal = hud + "A6.png"))
        
        pantalla_grid.add_widget(Button(size_hint_x = None ,width = 60, background_normal = hud + "ICO2.png"))
        pantalla_grid.add_widget(Button(background_normal = hud + "A1.png",markup = True, text = NID +  "Abrir", font_size = 15,text_size = (250,28),halign = "left"))
        pantalla_grid.add_widget(Button(size_hint_x = None ,width = 60, background_normal = hud + "ICO2.png"))
        
        pantalla_grid.add_widget(Button(size_hint_x = None ,width = 60, background_normal = hud + "ICO3.png"))
        pantalla_grid.add_widget(Button(background_normal = hud + "A1.png",markup = True, text = NID +  "Cerrar", font_size = 15,text_size = (250,28),halign = "left"))
        pantalla_grid.add_widget(Button(size_hint_x = None ,width = 60, background_normal = hud + "A3.png"))
        
        pantalla_grid.add_widget(Button(size_hint_x = None ,width = 60, background_normal = hud + "A2.png"))
        pantalla_grid.add_widget(Button(background_normal = hud + "A1.png",markup = True, text = NID +  "Eliminar Documento", font_size = 15,text_size = (250,28),halign = "left"))
        pantalla_grid.add_widget(Button(size_hint_x = None ,width = 60, background_normal = hud + "ICO8.png"))
        
        pantalla_grid.add_widget(Button(size_hint_x = None ,width = 60, background_normal = hud + "A7.png"))
        pantalla_grid.add_widget(Button(background_normal = hud + "A1.png",markup = True, text = NID +  "Reportar", font_size = 15,text_size = (250,28),halign = "left"))
        pantalla_grid.add_widget(Button(size_hint_x = None ,width = 60, background_normal = hud + "A3.png"))
        
        pantalla_grid.add_widget(Button(size_hint_x = None ,width = 60, background_normal = hud + "ICO6.png"))
        pantalla_grid.add_widget(Button(background_normal = hud + "A1.png",markup = True, text = NID +  "Encuadernar", font_size = 15,text_size = (250,28),halign = "left"))
        pantalla_grid.add_widget(Button(size_hint_x = None ,width = 60, background_normal = hud + "A3.png"))
        
        pantalla_grid.add_widget(Button(size_hint_x = None ,width = 60, background_normal = hud + "ICO7.png"))
        pantalla_grid.add_widget(Button(background_normal = hud + "A1.png",markup = True, text = NID +  "Dibujar", font_size = 15,text_size = (250,28),halign = "left"))
        pantalla_grid.add_widget(Button(size_hint_x = None ,width = 60, background_normal = hud + "ICO2.png"))
        
        pantalla_grid.add_widget(Button(size_hint_x = None ,width = 60, background_normal = hud + "ICO8.png"))
        pantalla_grid.add_widget(Button(background_normal = hud + "A1.png",markup = True, text = NID +  "Cocer", font_size = 15,text_size = (250,28),halign = "left"))
        pantalla_grid.add_widget(Button(size_hint_x = None ,width = 60, background_normal = hud + "ICO2.png"))
        
        pantalla_grid.add_widget(Button(size_hint_x = None ,width = 60, background_normal = hud + "ICO4.png"))
        pantalla_grid.add_widget(Button(background_normal = hud + "A1.png",markup = True, text = NID +  "Salir", font_size = 15,text_size = (250,28),halign = "center"    ))
        pantalla_grid.add_widget(Button(size_hint_x = None ,width = 60, background_normal = hud + "ICO2.png"))
        
        
        pantalla.add_widget(pantalla_grid)
        pantalla2_root = ScrollView(size_hint=(1, 1), bar_width = 0)
        pantalla2.add_widget(pantalla2_root)
        pantalla2_grid = GridLayout(cols = 1, size_hint_y = None)
        pantalla2_root.add_widget(pantalla2_grid)
        pantalla2_grid.bind(minimum_height=pantalla2_grid.setter('height'))
        
        boton2 = Button(text = NID+"Inntag",font_size = 19,markup = True, size_hint = (1,None), height = 60, background_normal = hud + "A3.png",text_size = (200,28),halign = "left")
        boton2.bind(on_press = lambda x : self.cambiar("Armando2"))
        portada = GridLayout(cols = 3,  height = (Window.width/2) , size_hint_y = None)
        portada.add_widget(Image(source = hud + "A8.png", keep_ratio = False , allow_stretch = True, size_hint_y = None, height = Window.width/2))
        portada.add_widget(Image(source = hud + "FON1.png", size_hint = (None,None), size = (Window.width/2,Window.width/2), height = Window.width/2))
        portada.add_widget(Image(source = hud + "A8.png", keep_ratio = False , allow_stretch = True, size_hint_y = None, height = Window.width/2))

        buscador = GridLayout(cols = 2, size_hint_y = None, height = 60)
        buscador.add_widget(Button(size_hint_x = None ,width = 60, background_normal = hud + "ICO5.png"))
        buscador.add_widget(TextInput(text = "Buscador de Tiendas.",background_normal = hud + "A13.png",background_active = hud+"A13.png", font_size = 17 , padding = [30,20,0,0]))
        
        
        pantalla2_grid.add_widget(buscador)

        dim12 = GridLayout(cols = 2, size_hint_y = None , height = 356)
        
        dim12.add_widget(Button(size_hint_x = None , width = 45, text = "", background_normal = hud + "ICO31.png", background_down = hud +"ICO31.png" ))
        Button1 = Button(markup =True,size_hint_y = None , height = 45, background_normal = hud+"TT4.png",text= NID+"Perfil", text_size =  (Window.width-50,22.5),halign = "left")
        dim12.add_widget(Button1)
        Button1.bind(on_release =lambda x : self.cambiar("Perfil"))
        
        dim12.add_widget(Image(source = hud + "blindbar1.png", size_hint_y = None ,size_hint_x = None, width = 45, height = 1,keep_ratio =False , allow_stretch = True))
        dim12.add_widget(Image(source = hud + "blindbar1.png", size_hint_y = 1 , height = 1,keep_ratio =False , allow_stretch = True))
        
        dim12.add_widget(Button(size_hint_x = None , width = 45, text = "", background_normal = hud + "ICO31.png", background_down = hud +"ICO31.png" ))
        dim12.add_widget(Button(markup =True,size_hint_y = None , height = 45, background_normal = hud+"TT4.png",text= NID+"Sugerir Tienda", text_size =  (Window.width-50,22.5),halign = "left"))
        
        dim12.add_widget(Image(source = hud + "blindbar1.png", size_hint_y = None ,size_hint_x = None, width = 45, height = 1,keep_ratio =False , allow_stretch = True))
        dim12.add_widget(Image(source = hud + "blindbar1.png", size_hint_y = 1 , height = 1,keep_ratio =False , allow_stretch = True))
        
        dim12.add_widget(Button(size_hint_x = None , width = 45, text = "", background_normal = hud + "ICO30.png", background_down = hud +"ICO30.png" ))
        dim12.add_widget(Button(markup =True,size_hint_y = None , height = 45, background_normal = hud+"TT4.png",text= NID+"Hacerse Miembro", text_size =  (Window.width-50,22.5),halign = "left"))
        
        dim12.add_widget(Image(source = hud + "blindbar1.png", size_hint_y = None ,size_hint_x = None, width = 45, height = 1,keep_ratio =False , allow_stretch = True))
        dim12.add_widget(Image(source = hud + "blindbar1.png", size_hint_y = 1 , height = 1,keep_ratio =False , allow_stretch = True))
        
        dim12.add_widget(Button(size_hint_x = None , width = 45, text = "", background_normal = hud + "ICO32.png", background_down = hud +"ICO32.png" ))
        self.Button4 = Button(markup =True,size_hint_y = None , height = 45, background_normal = hud+"TT4.png",text= NID+"Catàlogos de Comida", text_size =  (Window.width-50,22.5),halign = "left")
        self.Button4.bind(on_release = lambda x : self.cambiar("Catalogos"))
        dim12.add_widget(self.Button4)
        
        dim12.add_widget(Image(source = hud + "blindbar1.png", size_hint_y = None ,size_hint_x = None, width = 45, height = 1,keep_ratio =False , allow_stretch = True))
        dim12.add_widget(Image(source = hud + "blindbar1.png", size_hint_y = 1 , height = 1,keep_ratio =False , allow_stretch = True))
        
        dim12.add_widget(Button(size_hint_x = None , width = 45, text = "", background_normal = hud + "ICO33.png", background_down = hud +"ICO33.png" ))
        button5 = Button(markup =True,size_hint_y = None , height = 45, background_normal = hud+"TT4.png",text= NID+"Departamentos de Ropa", text_size =  (Window.width-50,22.5),halign = "left")
        button5.bind(on_release = lambda x : self.cambiar("Departamentos"))
        dim12.add_widget(button5)
        
        dim12.add_widget(Image(source = hud + "blindbar1.png", size_hint_y = None ,size_hint_x = None, width = 45, height = 1,keep_ratio =False , allow_stretch = True))
        dim12.add_widget(Image(source = hud + "blindbar1.png", size_hint_y = 1 , height = 1,keep_ratio =False , allow_stretch = True))
        
        dim12.add_widget(Button(size_hint_x = None , width = 45, text = "", background_normal = hud + "ICO33.png", background_down = hud +"ICO33.png" ))
        dim12.add_widget(Button(markup =True,size_hint_y = None , height = 45, background_normal = hud+"TT4.png",text= NID+"Directorios", text_size =  (Window.width-50,22.5),halign = "left"))
        
        dim12.add_widget(Image(source = hud + "blindbar1.png", size_hint_y = None ,size_hint_x = None, width = 45, height = 1,keep_ratio =False , allow_stretch = True))
        dim12.add_widget(Image(source = hud + "blindbar1.png", size_hint_y = 1 , height = 1,keep_ratio =False , allow_stretch = True))
        
        dim12.add_widget(Button(size_hint_x = None , width = 45, text = "", background_normal = hud + "ICO33.png", background_down = hud +"ICO33.png" ))
        dim12.add_widget(Button(markup =True,size_hint_y = None , height = 45, background_normal = hud+"TT4.png",text= NID+"Random shop", text_size =  (Window.width-50,22.5),halign = "left"))
        
        dim12.add_widget(Image(source = hud + "blindbar1.png", size_hint_y = None ,size_hint_x = None, width = 45, height = 1,keep_ratio =False , allow_stretch = True))
        dim12.add_widget(Image(source = hud + "blindbar1.png", size_hint_y = 1 , height = 1,keep_ratio =False , allow_stretch = True))
        
        dim12.add_widget(Button(size_hint_x = None , width = 45, text = "", background_normal = hud + "ICO33.png", background_down = hud +"ICO33.png" ))
        dim12.add_widget(Button(markup =True,size_hint_y = None , height = 45, background_normal = hud+"TT4.png",text= NID+"Cerrar Sesion", text_size =  (Window.width-50,22.5),halign = "left"))
        pantalla2_grid.add_widget(dim12)
        
        pantalla2_grid.add_widget(portada)
        grid1 = GridLayout(cols = 3, size_hint_y = None, height = 60)
        grid1.add_widget(boton2)
        grid1.add_widget(Button(size_hint_x = None ,width = 60, background_normal = hud + "ICO14.png"))
        grid1.add_widget(Button(size_hint_x = None, width = 70, background_normal = hud + "A1.png", background_down = hud + "A1.png"))
        departamentos = GridLayout(rows = 1, size_hint_x = None, size_hint_y = None , height = 60)
        departamentos.bind(minimum_width=departamentos.setter('width'))
        root3 = ScrollView(size_hint=(1, None), height = 60, do_scroll_y = False)
        root3.add_widget(departamentos) 
        #pantalla2_grid.add_widget(root3)
        for i in range(10):
            departamentos.add_widget(Button(size_hint_x = None , width = 60, text = "", background_normal = hud + "ICO"+str(i+2)+".png", background_down = hud +"ICO19.png" ))
        pantalla2_grid.add_widget(grid1)
        pantalla2_grid.add_widget(pantalla6_complementos)
        pantalla2_grid.add_widget(Button(text = NID+"Top 10",font_size = 15,markup = True, size_hint = (1,None), height = 30, background_normal = hud + "A6.png",text_size = (330,17),halign = "left"))
        
        layout = GridLayout(cols=5, spacing=1, size_hint_x=None, size_hint_y = None)
        # Make sure the height is such that there is something to scroll.
        layout.bind(minimum_width=layout.setter('width'))
        #layout.bind(minimum_height=layout.setter('height'))

        content2 = GridLayout(cols = 3, size_hint_y = None)
        content2_scroll = ScrollView(size_hint=(1, 1),bar_width = 0)
        content2_scroll.add_widget(content2)
        content2.bind(minimum_height=content2.setter('height'))
        
        vista_pred = Popup(size_hint = (1,1.1), separator_color = [1,1,1,0], content =content2_scroll, separator_height = 0 ,title_size = 0, title = "",background =hud+"TT.png")
        #content1.add_widget(Button())
        content2.add_widget(Label(size_hint_y = None))
        content_dim = GridLayout(cols = 1, size_hint_y = None, size_hint_x = None , width = (Window.width*0.9))
        content2.add_widget(content_dim)
        content_dim.bind(minimum_height=content_dim.setter('height'))
        dim7 = GridLayout(cols = 2, size_hint_y = None, size_hint_x = 1 , height = 45)
        dim7.add_widget(ImageButton(size_hint = (None,None),width = 45, height = 45, source = hud + "ICO25.png", keep_ratio  = False , allow_stretch = True))
        dim7.add_widget(Button(markup = True,text = "Nuestra primera portada!! :D",font_size = 17,text_size = ((Window.width * 0.9)-75, 30),halign = "left",valign = "bottom",size_hint = (1,None), height = 45 ,background_normal = hud + "TT.png", keep_ratio = False , allow_stretch = True))
        content_dim.add_widget(dim7)
        content_dim.add_widget(ImageButton(size_hint = (None,None), height = (Window.width*0.9) , width = (Window.width*0.9), source = hud + "ICO15.png"))
        content_dimgrid = GridLayout(cols = 5, size_hint_y = None , height = 48)
        content_dimgrid.add_widget(ImageButton(size_hint = (None,None),width = 15, height = 48, source = hud + "A1.png", keep_ratio  = False , allow_stretch = True))
        content_dimgrid.add_widget(ImageButton(size_hint = (None,None),width = 48, height = 48, source = hud + "ICO21.jpg", keep_ratio  = False , allow_stretch = True))
        content_dimgrid.add_widget(ImageButton(size_hint = (None,None),width = 15, height = 48, source = hud + "A1.png", keep_ratio  = False , allow_stretch = True))
        content_dimgrid.add_widget(ImageButton(size_hint = (None,None),width = 48, height = 48, source = hud + "ICO20.jpg", keep_ratio  = False , allow_stretch = True))
        content_dimgrid.add_widget(ImageButton(size_hint = (1,None), height = 48, source = hud + "A1.png", keep_ratio  = False , allow_stretch = True))
        #content_dim.add_widget(Image(markup = True, size_hint = (1,None), height = 10, keep_ratio = False, allow_stretch = True,source = hud + "TT.jpg"))
        #content_dim.add_widget(content_dimgrid)
        
        dim3 = GridLayout(cols = 7, size_hint_y = None , height = 99)
        dim4 = GridLayout(cols = 1, size_hint_y = None , height = 99)
        dim6 = GridLayout(cols = 1, size_hint_y = None , height = 99, size_hint_x = None , width = 64)
        
        dim3.add_widget(ImageButton(size_hint = (None,1), height = 99,width = 15, source = hud + "fondo1.png", keep_ratio  = False , allow_stretch = True))
        dim6.add_widget(ImageButton(size_hint = (None,None), height = 10,width = 64, source = hud + "fondo1.png", keep_ratio  = False , allow_stretch = True))
        dim6.add_widget(ImageButton(size_hint = (None,None),width = 64, height = 64, source = hud + "FON3.png", keep_ratio  = False , allow_stretch = True))
        dim6.add_widget(ImageButton(size_hint = (None,1), height = 99,width = 64, source = hud + "fondo1.png", keep_ratio  = False , allow_stretch = True))
        dim3.add_widget(dim6)
        dim3.add_widget(ImageButton(size_hint = (None,1), height = 99,width = 15, source = hud + "fondo1.png", keep_ratio  = False , allow_stretch = True))
        dim4.add_widget(Button(text=str("[color=#404040]"+"[b]Armando S."),text_size = (100,42),halign = "left", valign = "bottom",font_size = 17,markup = True,background_normal = hud + "TT4.png", size_hint_y=None, height=35, size_hint_x = 1 , width = 200))
        dim4.add_widget(Button(text=str("[color=#404040]"+"@LilBoy"), height=64,text_size = (100,55),halign = "left", valign = "top",font_size = 17,markup = True,background_normal = hud + "TT4.png", size_hint_y=None, size_hint_x = 1 , width = 200))
        dim3.add_widget(dim4)
        dim3.add_widget(ImageButton(size_hint = (1,None), height = 99, source = hud + "fondo1.png", keep_ratio  = False , allow_stretch = True))
        dim5 = GridLayout(cols = 1, size_hint_y = None , height = 100, size_hint_x = None, width = 64)
        #dim5.add_widget(ImageButton(size_hint = (None,1), height = 99,width = 64, source = hud + "fondo1.png", keep_ratio  = False , allow_stretch = True))
        dim5.add_widget(ImageButton(size_hint = (None,None),width = 64, height = 64, source = hud + "ICO22.png", keep_ratio  = True , allow_stretch = False))
        dim5.add_widget(ImageButton(size_hint = (None,1), height = 99,width = 64, source = hud + "fondo1.png", keep_ratio  = False , allow_stretch = True))
        dim3.add_widget(dim5)
        dim3.add_widget(ImageButton(size_hint = (None,1), height = 99,width = 15, source = hud + "fondo1.png", keep_ratio  = False , allow_stretch = True))
       
        
        
        content_dim.add_widget(dim3)
        content_dim.add_widget(TextInput(line_spacing = 2.5,font_size = 15,size_hint = (1,None),padding = [20,0,20,0], height = 200, background_active = hud + "fondo1.png",background_normal = hud + "fondo1.png",  markup = True , text = "Buenos Dias Chavales Espero que hayan tenido un gran dia como nosotros los esperamos para cuando quieran volver! no nos olviden :)", Enable = False))
        #content_dim.add_widget(ImageButton(size_hint = (1,None), height = 16,width = 15, source = hud + "M9.png", keep_ratio  = False , allow_stretch = True))
        content2.add_widget(Label(size_hint_y = None))
        
        
       
                
            
        for i in range(10):
            vista1 = GridLayout(cols = 1, size_hint = (None,None), width = 230, height = 440)
            dim11 = GridLayout(cols = 1, height = 330, size_hint_y = None)
            imagen = ImageButton(size_hint = (None,None), height = 230 , width = 230, source = hud + "ICO15.png")
            imagen.bind(on_press = vista_pred.open)
            dim11.add_widget(ImageButton(size_hint = (None,1), height = 230 , width = 230, source = hud + "fondo3.png",allow_stretch = True, keep_ratio = False))
            dim11.add_widget(imagen)
            dim11.add_widget(ImageButton(size_hint = (None,1), height = 230 , width = 230, source = hud + "fondo3.png",allow_stretch = True, keep_ratio = False))
            vista1.add_widget(dim11)
            dim = GridLayout(cols = 2, size_hint = (None,None), width = 230,height = 70)
            vista1.add_widget(dim)
            dim2 = GridLayout(cols = 1)
            dim.add_widget(dim2)
            dim2.add_widget(Button(text=str(NID+"Churros"),text_size = (150,42),halign = "left", valign = "bottom",font_size = 17,markup = True,background_normal = hud + "A9.png", size_hint_y=None, height=35, size_hint_x = 1 , width = 200))
            dim2.add_widget(Button(text=str(NID+"Agora Mall"),text_size = (150,15),halign = "left",font_size = 14,markup = True,background_normal = hud + "A9.png", size_hint_y=None, height=35, size_hint_x = None , width = 200))
            boton3 = ImageButton(size_hint_y = None,height = 60 , size_hint_x = None , width = 60, source = hud + "ICO16.png", allow_stretch = True, keep_ratio = False)
            boton3.bind(on_release=lambda x = boton3 :abrir(x))
            dim.add_widget(boton3)
            #boton3.bind(on_press = vista_pred.open)
            vista1.add_widget(Button(text="",font_size = 14,markup = True,background_normal = hud + "A9.png", size_hint_y=None, height=20, size_hint_x = None , width = 230))
            vista1.add_widget(Button(text="",font_size = 14,markup = True,background_normal = hud + "A14.png", size_hint_y=None, height=20, size_hint_x = None , width = 230))

            layout.add_widget(vista1)
        
        
        
        
        root = ScrollView(size_hint=(1, None), height = 440, do_scroll_y = False)
        root.add_widget(layout)
        #pantalla2_grid.add_widget(root)
        MasVisitados = GridLayout(cols = 3, size_hint_y = None , height = 490, spacing = 0)
        for i in range(10):
            MasVisitados.add_widget(Button(background_normal = hud+"fondo1.png", text = NID+str(10-i)+".",markup = True, font_size = 20, size_hint_x = None , width = 48, size_hint_y = None , height = 48))
            MasVisitados.add_widget(Button(background_normal = hud+"fondo1.png",text_size = (Window.width-50-96,25), text = NID+"Tienda "+str(10-i),markup = True, font_size = 14, size_hint_y = None ,size_hint_x = 1, height = 48))
            MasVisitados.add_widget(Button(background_normal = hud+"ICO35.png", text = "",markup = True, font_size = 14, size_hint_x = None , width = 48, size_hint_y = None , height = 48))
            
            MasVisitados.add_widget(Image(allow_stretch = True, keep_ratio = False,source = hud+"blindbar1.png",size_hint_y = None , height = 1, text = "",markup = True,  size_hint_x = None , width = 48))
            MasVisitados.add_widget(Image(allow_stretch = True, keep_ratio = False,source = hud+"blindbar1.png",size_hint_y = None , height = 1, text = "",markup = True,  size_hint_x = 1 , width = 48))
            MasVisitados.add_widget(Image(allow_stretch = True, keep_ratio = False,source = hud+"blindbar1.png",size_hint_y = None , height = 1, text = "",markup = True,  size_hint_x = None , width = 48))

        pantalla2_grid.add_widget(MasVisitados)
            
        
        
        
        self.ROOT_Navitagiondrawer1.add_widget(self.sm)
        
        

        grid2 = GridLayout(cols = 3, size_hint_y = None, height = 60, spacing = 0 )
        grid2.add_widget(Button(text = NID+"Malls",font_size = 19,markup = True, size_hint = (1,None), height = 60, background_normal = hud + "A3.png",text_size = (200,28),halign = "left"))
        grid2.add_widget(Button(size_hint_x = None ,width = 60, background_normal = hud + "ICO18.png"))
        grid2.add_widget(Button(size_hint_x = None, width = 70, background_normal = hud + "A1.png", background_down = hud + "A1.png"))
        
        #pantalla2_grid.add_widget(grid2)
        layout2 = GridLayout(cols=5, spacing=1, size_hint_x=None)
        layout2.bind(minimum_width=layout2.setter('width'))
        for i in range(5):
            vista1 = GridLayout(cols = 1, size_hint = (None,None), width = 230, height = 340)
            vista1.add_widget(Image(size_hint = (None,None), height = 230 , width = 230, source = hud + "ICO15.png"))
            dim = GridLayout(cols = 2, size_hint = (None,None), width = 230,height = 70)
            vista1.add_widget(dim)
            dim2 = GridLayout(cols = 1)
            dim.add_widget(dim2)
            dim2.add_widget(Button(text=str(NID+"Churros"),text_size = (150,42),halign = "left", valign = "bottom",font_size = 17,markup = True,background_normal = hud + "A9.png", size_hint_y=None, height=35, size_hint_x = 1 , width = 200))
            dim2.add_widget(Button(text=str(NID+"Agora Mall"),text_size = (150,15),halign = "left",font_size = 14,markup = True,background_normal = hud + "A9.png", size_hint_y=None, height=35, size_hint_x = None , width = 200))
            dim.add_widget(Image(size_hint_y = None,height = 60 , size_hint_x = None , width = 60, source = hud + "ICO16.png", allow_stretch = True, keep_ratio = False))
            vista1.add_widget(Button(text="",font_size = 14,markup = True,background_normal = hud + "A9.png", size_hint_y=None, height=20, size_hint_x = None , width = 230))
            vista1.add_widget(Button(text="",font_size = 14,markup = True,background_normal = hud + "A14.png", size_hint_y=None, height=20, size_hint_x = None , width = 230))

            layout2.add_widget(vista1)
        root2 = ScrollView(size_hint=(1, None), height = 340)
        #pantalla2_grid.add_widget(root2)
        root2.add_widget(layout2)
        self.add_widget(self.Button5)    
        
    def cambiar(self,text):
        #print text
        if text == "Armando":
            print("a")
            if self.Button5.pos == [0,Window.height]:
                self.loading(self)
                self.Button5.text = "Usuario Confirmado."
                anim2 = Animation(x=0, y=Window.height,t='in_out_sine', d = .5)
                t2 = Timer(1.75,lambda x=1: anim2.start(self.Button5))
                anim = Animation(x=0, y= Window.height-50,t='in_out_sine', d = .5)
                t4 = Timer(0.25,lambda x=1: anim.start(self.Button5))
                t4.start()
                t2.start()
                t3 = Timer(3,lambda x=1:self.definir2(text))
                t3.start()
        else:
            self.sm.current = text
                
        if text == "Perfil":
            #   self.add_widget(Button(size_hint = (None,None), size = (100,100), pos = (Window.width-25-100,25)))
            pass

        else:
            pass
        

    def definir(self,text):
        self.a.current = text

    def definir2(self,text):
        self.sm.current = text


    def loading(self,button):
        NID = "[color=#404040]"
        NID2 = "[color=#ff3333]"
        self.patch = os.path.dirname(os.path.abspath(__file__))
        hud = self.patch + '/hud/'
        #gridload = GridLayout(cols = 1)
        #loadingbar = Popup(pos_hint={'center_x': .5, 'center_y': .5},content = gridload, size_hint = (None,None), size = (256,256), separator_color = [1,1,1,0]   , separator_height = 0 ,title_size = 0, title = "",background =hud+"TT2.png")
        loadgin =Image(source = hud + "loadinfo.gif", size_hint=(None,None), size = (48,48), anim_delay = 0.040, pos = ((Window.width/2)-24,125))
        self.pantalla3.add_widget(loadgin)
        def aplicar():
            print ("Moviendo Imagen..")
            loadgin.pos = (-50,-50)
        tz = Timer(3,lambda x=1: aplicar())
        #tz.start()
        
        
    def Aplicarvista(self,contenedor,num):
        NID = "[color=#404040]"
        NID2 = "[color=#ff3333]"
        patch = os.path.dirname(os.path.abspath(__file__))
        hud = patch + '/hud/'
        if num == 1:
            for i in range(6):
                if i == 0:
                    portada_p = RelativeLayout(size_hint_y = None, height = 300)
                    portada_screen = ScreenManager(size_hint_y = None, height = 300)
                    ps_screen1 = Screen(name = "1")
                    ps_screen2 = Screen(name = "2")
                    portada_screen.add_widget(ps_screen1)
                    portada_screen.add_widget(ps_screen2)
                    portada_screen.current = "2"
                    ps_screen1.add_widget(Image(size_hint_y = None, height = 300, source = hud+"fondo1.png",allow_stretch = True, keep_ratio = False))
                    ps_screen2.add_widget(Image(size_hint_y = None, height = 300, source = hud+"fondo2.png",allow_stretch = True, keep_ratio = False))
                    portada_p.add_widget(portada_screen)
                    Button2 = Button(size_hint = (None,None), size = (50,50), pos = (25,100), text = "[b]<",markup = True , font_size = 20, background_normal = hud+"TT.png")
                    portada_p.add_widget(Button2)
                    Button3 = Button(size_hint = (None,None), size = (50,50), pos = (Window.width -50-25,100), text = "[b]>",markup = True , font_size = 20, background_normal = hud+"TT.png")
                    portada_p.add_widget(Button3)
                    def cambiarportada(text):  
                        if text == "2":
                            portada_screen.current = portada_screen.next()
                        else:
                            portada_screen.current = portada_screen.previous()
                        
                    Button3.bind(on_release = lambda x: cambiarportada("2"))
                    Button2.bind(on_release = lambda x: cambiarportada("1"))
                    tags_strings = ["Celulares","Computadoras","Tarjetas de Video","Random Access Memory","Procesadores"]
                    tags = GridLayout(size_hint_y = None, height = 99, cols = 1)
                    tags.add_widget(Button(size_hint_y = None, height = 50,markup = True,text ="Tags",font_size = 19    ,background_normal = hud +"fondo2.png", text_size = ((Window.width/2) - 10 - 50, 50),valign = "middle"))
                    for i in range(5):
                        tags.add_widget(Button(markup = True,text =NID+ "[b]"+ tags_strings[i],background_normal = hud +"23.png", text_size = ((Window.width/2) - 10 - 50, 35),valign = "middle"))
                    tags.height = ((35 * 5) + 100)
                    #tags.add_widget(Button(size_hint_y = None, height = 50,markup = True,text ="Portada",font_size = 19    ,background_normal = hud +"fondo2.png", text_size = (Window.width - 10 - 50, 50),valign = "middle"))
                    
                    tags_strings2 = ["Motherboards","Accessorios","Power Suply","[+]Agregar",""]
                    tags2 = GridLayout(size_hint_y = None, height = 99, cols = 1)
                    tags2.add_widget(Button(size_hint_y = None, height = 50,markup = True,text ="",font_size = 19    ,background_normal = hud +"fondo2.png", text_size = ((Window.width/2) - 10 - 50, 50),valign = "middle"))
                    for i in range(5):
                        if tags_strings2[i] == "[+]Agregar":
                            tags2.add_widget(Button(markup = True,text ="[color=#0066ff]"+ "[b]"+ tags_strings2[i],background_normal = hud +"23.png", text_size = ((Window.width/2) - 10 - 50, 35),valign = "middle"))
                        else:
                            tags2.add_widget(Button(markup = True,text =NID+ "[b]"+ tags_strings2[i],background_normal = hud +"23.png", text_size = ((Window.width/2) - 10 - 50, 35),valign = "middle"))
                    tags2.height = ((35 * 5) + 100)
                    #tags2.add_widget(Button(size_hint_y = None, height = 50,markup = True,text ="Portada",font_size = 19    ,background_normal = hud +"fondo2.png", text_size = (Window.width - 10 - 50, 50),valign = "middle"))
                    
                    self.pantalla7_complementos.add_widget(portada_p)
                    self.pantalla7_complementos.add_widget(Image(source = hud + "fondo1.png", size_hint_y = None, height = 5, allow_stretch = True, keep_ratio = False))
                    contenedor.add_widget(tags)
                    contenedor.add_widget(tags2)
                print i
                dim_contenedor = GridLayout(cols = 1,size_hint_y = None, height = 470)
                dim_contenedor.add_widget(Image(source = hud + "fondo2.png", size_hint_y = None , height = 280, allow_stretch = True , keep_ratio = False))
                dim_contenedor.add_widget(Image(source = hud + "fondo1.png", size_hint_y = None , height = 10, allow_stretch = True , keep_ratio = False))
                dim_contenedor.add_widget(Button(text_size = ((Window.width/2)-50, 30), valign = "top",background_normal = hud + "fondo1.png",markup = True,text = NID+"[b]Artículo", size_hint_y = None , height = 40, allow_stretch = True , keep_ratio = False))
                dim_contenedor.add_widget(Button(text_size = ((Window.width/2)-50, 60), valign = "top",background_normal = hud + "fondo1.png",markup = True,text = NID+"La mejor descripcíon que podria tener un artículo :)", size_hint_y = None , height = 70, allow_stretch = True , keep_ratio = False))
                dim32 = GridLayout(cols = 2, size_hint_y = None , height = 70)
                dim_contenedor.add_widget(dim32)
                dim32.add_widget(Button(text_size = ((Window.width/4)-50, 60),background_normal = hud + "fondo1.png",markup = True,text = NID+"[b]2400.00 RD$", size_hint_y = None , height = 70, allow_stretch = True , keep_ratio = False))
                dim32.add_widget(Button(background_normal = hud + "fondo1.png",text = "", size_hint_y = None , height = 70, allow_stretch = True , keep_ratio = False))
                
                contenedor.add_widget(dim_contenedor)
                contenedor.height = 3 * 470 +   tags.height
                contenedor.spacing = 0
        if num == 2:
            for i in range(6):
                if i == 0:
                    tags_strings = ["Celulares","Computadoras","Tarjetas de Video","Random Access Memory","Procesadores"]
                    tags = GridLayout(size_hint_y = None, height = 99, cols = 1)
                    tags.add_widget(Button(size_hint_y = None, height = 50,markup = True,text ="Tags",font_size = 19    ,background_normal = hud +"fondo2.png", text_size = (Window.width - 10 - 50, 50),valign = "middle"))
                    for i in range(5):
                        tags.add_widget(Button(markup = True,text =NID+ "[b]"+ tags_strings[i],background_normal = hud +"23.png", text_size = (Window.width - 10 - 50, 35),valign = "middle"))
                    tags.height = ((35 * 5) + 100)
                    tags.add_widget(Button(size_hint_y = None, height = 50,markup = True,text ="Portada",font_size = 19    ,background_normal = hud +"fondo2.png", text_size = (Window.width - 10 - 50, 50),valign = "middle"))
                    contenedor.add_widget(tags)
                print i
                dim_contenedor = GridLayout(cols = 2,size_hint_y = None, height = 125)
                dim_contenedor.add_widget(Image(source = hud + "fondo2.png", size_hint_x = None , Width = 125, allow_stretch = True , keep_ratio = False))
                dim35 = GridLayout(cols = 1, size_hint_y = None ,height = 125)
                dim33 = GridLayout(cols = 1 , size_hint_y = None ,height =95)
                dim33.add_widget(Button( valign = "top",background_normal = hud + "fondo1.png",markup = True,text = NID+"[b]Artículo", size_hint_y = None , height = 30, allow_stretch = True , keep_ratio = False))
                dim33.add_widget(Button(text_size = (Window.width-125-50,65), valign = "top",background_normal = hud + "fondo1.png",markup = True,text = NID+"La mejor descripcíon que podria tener un artículo :)", size_hint_y = None , height = 65, allow_stretch = True , keep_ratio = False))
                dim35.add_widget(dim33)
                dim34 = GridLayout(cols = 2, size_hint_y = None ,height = 30)
                dim34.add_widget(Button(background_normal = hud + "fondo1.png",text = "", size_hint_y = None , height = 30, allow_stretch = True , keep_ratio = False))
                dim34.add_widget(Button(background_normal = hud + "fondo1.png",markup = True,text = NID+"[b]2400.00 RD$", size_hint_y = None , height = 30, allow_stretch = True , keep_ratio = False))
                dim35.add_widget(dim34)
                dim_contenedor.add_widget(dim35)
                
                
                contenedor.add_widget(dim_contenedor)
                
                contenedor.height = (6 * 125) + 5 + (tags.height)
                contenedor.cols = 1
        if num == 3:
            for i in range(6):
                if i == 0:
                    tags_strings = ["Celulares","Computadoras","Tarjetas de Video","Random Access Memory","Procesadores"]
                    tags = GridLayout(size_hint_y = None, height = 99, cols = 1)
                    tags.add_widget(Button(size_hint_y = None, height = 50,markup = True,text ="Tags",font_size = 19    ,background_normal = hud +"fondo2.png", text_size = (Window.width - 10 - 50, 50),valign = "middle"))
                    for i in range(5):
                        tags.add_widget(Button(markup = True,text =NID+ "[b]"+ tags_strings[i],background_normal = hud +"23.png", text_size = (Window.width - 10 - 50, 35),valign = "middle"))
                    tags.height = ((35 * 5) + 100)
                    tags.add_widget(Button(size_hint_y = None, height = 50,markup = True,text ="Portada",font_size = 19    ,background_normal = hud +"fondo2.png", text_size = (Window.width - 10 - 50, 50),valign = "middle"))
                    contenedor.add_widget(tags)
                print i
                dim_contenedor = GridLayout(cols = 2,size_hint_y = None, height = 280)
                dim_contenedor.add_widget(Image(source = hud + "fondo2.png", size_hint_y = None , height = 280, allow_stretch = True , keep_ratio = False))
                dim36 = GridLayout(cols = 1,size_hint_y = None, height = 280)
                dim36.add_widget(Image(source = hud + "fondo1.png", size_hint_y = None , height = 10, allow_stretch = True , keep_ratio = False))
                dim36.add_widget(Button(text_size = ((Window.width/2)-50, 30), valign = "top",background_normal = hud + "fondo1.png",markup = True,text = NID+"[b]Artículo", size_hint_y = None , height = 40, allow_stretch = True , keep_ratio = False))
                dim36.add_widget(Button(text_size = ((Window.width/2)-50, 60), valign = "top",background_normal = hud + "fondo1.png",markup = True,text = NID+"La mejor descripcíon que podria tener un artículo :)", size_hint_y = None , height = 160, allow_stretch = True , keep_ratio = False))
                dim37 = GridLayout(cols = 2, size_hint_y = None , height = 70)
                dim36.add_widget(dim37)
                dim37.add_widget(Button(background_normal = hud + "fondo1.png",text = "", size_hint_y = None , height = 70, allow_stretch = True , keep_ratio = False))
                dim37.add_widget(Button(text_size = ((Window.width/4), 60),background_normal = hud + "fondo1.png",markup = True,text = NID+"[b]2400.00 RD$", size_hint_y = None , height = 70, allow_stretch = True , keep_ratio = False))
                dim_contenedor.add_widget(dim36)
                contenedor.add_widget(dim_contenedor)
                contenedor.height = (6 * 280)  + tags.height +6
                contenedor.cols = 1
                
        if num == 4:
            for i in range(6):
                print i
                dim_contenedor = GridLayout(cols = 1,size_hint_y = None, height = 400)
                dim_contenedor.add_widget(Image(source = hud + "fondo2.png", size_hint_y = None , height = 280, allow_stretch = True , keep_ratio = False))
                dim_contenedor.add_widget(Image(source = hud + "fondo1.png", size_hint_y = None , height = 10, allow_stretch = True , keep_ratio = False))
                dim_contenedor.add_widget(Button(text_size = ((Window.width/2)-50, 30), valign = "top",background_normal = hud + "fondo1.png",markup = True,text = NID+"[b]Artículo", size_hint_y = None , height = 40, allow_stretch = True , keep_ratio = False))
                #dim_contenedor.add_widget(Button(text_size = ((Window.width/2)-50, 60), valign = "top",background_normal = hud + "fondo1.png",markup = True,text = NID+"Detalles", size_hint_y = None , height = 70, allow_stretch = True , keep_ratio = False))
                dim32 = GridLayout(cols = 2, size_hint_y = None , height = 35)
                dim_contenedor.add_widget(dim32)
                dim32.add_widget(Button(text_size = ((Window.width/4)-50, 60),background_normal = hud + "fondo1.png",markup = True,text = NID+"[b]2400.00 RD$", size_hint_y = None , height = 35, allow_stretch = True , keep_ratio = False))
                dim32.add_widget(Button(background_normal = hud + "fondo1.png",text = "", size_hint_y = None , height = 35, allow_stretch = True , keep_ratio = False))
                
                contenedor.add_widget(dim_contenedor)
                contenedor.height = 3 * 470             
                
        if num == 5:
            for i in range(6):
                print i
                dim_contenedor = RelativeLayout(cols = 1,size_hint_y = None, height = 300)
                dim_contenedor.add_widget(Image(source = hud + "fondo2.png", size_hint_y = None , height = 300, allow_stretch = True , keep_ratio = False))
                dim38 = GridLayout(size_hint_y = None, height = 45, cols = 2)
                dim_contenedor.add_widget(dim38)
                dim38.add_widget(Button(background_normal = hud + "TT.png", size_hint_y = None , height = 45, allow_stretch = True , keep_ratio = False, text = "Articulo"))
                dim38.add_widget(Button(background_normal = hud + "TT.png", size_hint_y = None , height = 45, allow_stretch = True , keep_ratio = False, text = "[b]2400.00 RD$", markup = True))

                contenedor.add_widget(dim_contenedor)
                contenedor.height = (3 * 300)            
                
                
        if num == 6:
            for i in range(6):
                print i
                dim_contenedor = RelativeLayout(cols = 1,size_hint_y = None, height = 200)
                dim_contenedor.add_widget(Image(source = hud + "fondo2.png", size_hint_y = None , height = 200, allow_stretch = True , keep_ratio = False))
                dim38 = GridLayout(size_hint_y = None, height = 45, cols = 3)
                dim_contenedor.add_widget(dim38)
                dim38.add_widget(Button(background_normal = hud + "TT.png", size_hint_y = None , height = 45, allow_stretch = True , keep_ratio = False, text = "Articulo"))
                dim38.add_widget(Button(background_normal = hud + "TT.png", size_hint_y = None , height = 45, allow_stretch = True , keep_ratio = False, text = "[b]2400.00 RD$", markup = True))

                contenedor.add_widget(dim_contenedor)
                contenedor.height = 6 * 200            
                contenedor.cols = 1
                
                
class MyApp(App):
    def build(self):
        return InterfaceManager()
        

if __name__ in ('__main__', '__android__'):
    MyApp().run()

    
    
    
    
    