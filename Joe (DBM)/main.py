#!/usr/bin/env python55555533yyyyyyyyyyyyyyyyyyyyy555555
# -*- coding: utf-8 -*-
from kivy.config import Config
Config.set('graphics','window_state','maximized')
Config.set('graphics','borderless', 0)
Config.set('kivy','window_icon', "C:\Users\Armando\Desktop\Avances\Joe (DBM)\icon\coffee.png")
import kivy
import threading 
from threading import *
from kivy.effects.opacityscroll import OpacityScrollEffect
from kivy.effects.scroll import ScrollEffect
from kivy.garden.mapview import MapView, MapMarker, MarkerMapLayer, MapSource
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
from kivy.garden.mapview import MapView, MapMarker, MarkerMapLayer,MapSource
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

from plyer import gps
from threading import Timer


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
        Window.clearcolor = (1, 1, 1, 1)
        self.patch = os.path.dirname(os.path.abspath(__file__))
        hud = self.patch + '/hud/'
        icon = self.patch + '/icon/'
        fonts = self.patch + '/fonts/'
        databases = self.patch + '/databases/'
        color = self.patch + '/hud/color/'
        
        pantalla_principall = GridLayout(cols =2)
        self.pantalla_principall_root = RelativeLayout()
        C1 = "[color=#13C0C7]"
        C4 = "[color=#000000]"
        C2 = "[color=#404040]"
        C3 = "[color=#ff3333]"
        
        self.ROOT_Navitagiondrawer1 = NavigationDrawer()
        self.ROOT_Navitagiondrawer1.add_widget(Button())
        self.pantalla_principall_root.add_widget(pantalla_principall)
        self.ROOT_Navitagiondrawer1.add_widget(self.pantalla_principall_root)
        #self.ROOT_Navitagiondrawer1.add_widget(Button())
        self.add_widget(self.ROOT_Navitagiondrawer1)

        main_dim = GridLayout(cols = 1)
        pantalla_principall.add_widget(main_dim)
        main_dim_grid1 = GridLayout(rows = 1,size_hint_y = None, height = 60)
        main_dim_grid2 = GridLayout(rows = 1,size_hint_y = None, height = 60)
        main_dim.add_widget(main_dim_grid1)
        
        main_dim_grid1.add_widget(Button(size_hint_x = None, width =60, text = "", background_normal = color+"12.png"))
        main_dim_grid1.add_widget(Button(size_hint_x = None, width =60, background_normal = color+"15.png", background_down = color+"15.png"))
        main_dim_grid1.add_widget(Button(size_hint_x = None, width =60, background_normal = color+"14.png", background_down = color+"14.png"))
        main_dim_grid1.add_widget(Button(size_hint_x = None, width =60, background_normal = color+"13.png", background_down = color+"13.png"))
        main_dim_grid1.add_widget(Button(size_hint_x = None, width =60, background_normal = color+"11.png", background_down = color+"11.png"))
        main_dim_grid1.add_widget(Button(size_hint_x = 1, background_normal = color+"3.png"))
        #main_dim_grid1.add_widget(Image(size_hint_y = None, height = 1 ,allow_stretch = True, keep_ratio = False , source = color+"2.png"))
        
        main_dim.add_widget(main_dim_grid2)
        main_dim_grid2.add_widget(Button(size_hint_x = None, width =60, text = "", background_normal = color+"12.png"))
        main_dim_grid2.add_widget(Button(size_hint_x = None, width =60, background_normal = color+"15.png", background_down = color+"15.png"))
        main_dim_grid2.add_widget(Button(size_hint_x = None, width =60, background_normal = color+"14.png", background_down = color+"14.png"))
        main_dim_grid2.add_widget(Button(size_hint_x = None, width =60, background_normal = color+"13.png", background_down = color+"13.png"))
        main_dim_grid2.add_widget(Button(size_hint_x = None, width =60, background_normal = color+"11.png", background_down = color+"11.png"))
        main_dim_grid2.add_widget(Button(background_normal = color+"3.png",size_hint_x = None, width = 100, text = "Archivo"))
        main_dim_grid2.add_widget(Button(background_normal = color+"3.png",size_hint_x = None, width = 100, text = "Editar"))
        main_dim_grid2.add_widget(Button(background_normal = color+"3.png",size_hint_x = None, width = 100, text = "Busqueda"))
        main_dim_grid2.add_widget(Button(background_normal = color+"3.png",size_hint_x = None, width = 100, text = "Encriptacion"))
        main_dim_grid2.add_widget(Button(background_normal = color+"3.png",size_hint_x = None, width = 100, text = "Vista"))
        main_dim_grid2.add_widget(Button(background_normal = color+"3.png",size_hint_x = None, width = 100, text = "Herramientas"))
        main_dim_grid2.add_widget(Button(background_normal = color+"3.png",size_hint_x = None, width = 100, text = "Opciones"))
        main_dim_grid2.add_widget(Button(background_normal = color+"3.png"))
        
        main_dim_grid3 = GridLayout(cols = 3)
        main_dim.add_widget(main_dim_grid3)
        main_dim_grid3_dim1 = GridLayout(cols = 1, size_hint_x = None, width = 300)
        main_dim_grid3_dim2 = GridLayout(cols = 1)
        main_dim_grid3.add_widget(main_dim_grid3_dim1)
        main_dim_grid3.add_widget(Image(size_hint_x = None, width = 1 ,allow_stretch = True, keep_ratio = False , source = color+"15.png"))
        main_dim_grid3.add_widget(main_dim_grid3_dim2)
        main_dim_grid3_dim1.add_widget(Button(text_size = (250,30),valign = "middle",background_normal = color +"3.png",halign = "left",size_hint_y = None , height = 30, text = "Sources"))
        for i in range(10): 
            if i == 0:
                pass
            else:
                main_dim_grid3_dim1.add_widget(Image(source =color+"16c.png", allow_stretch = True, keep_ratio = False, size_hint_y = None, height = 1))
            

            dim2 = GridLayout(cols = 1,size_hint_y = None, height = 50)
            dim1 = GridLayout(rows = 1,size_hint_y = None, height = 25)
            dim3 = GridLayout(rows = 1,size_hint_y = None, height = 25)
            Button2 = Button(font_size = 15,text_size = (200,20),valign ="bottom",halign = "left",background_normal = color+"16.png",background_down = color+"16b.png",size_hint_y = None, height = 25 ,markup = True, text = C4+"Archive"+ str(i)+".txt")
            Button2.bind(on_release = lambda x: self.conectar("t"))
            dim1.add_widget(Image(source= color+"5.png", size_hint_x = None, width = 25, keep_ratio = False, allow_stretch = True))
            dim1.add_widget(Button2)
            dim1.add_widget(Button(size_hint_x = None, width = 25 , text = C4+"X",markup = True, background_normal = color+"16b.png",background_down = color+"16b.png",))
            dim2.add_widget(dim1)
            dim3.add_widget(Image(source= color+"5.png", size_hint_x = None, width = 25, keep_ratio = False, allow_stretch = True))
            dim3.add_widget(Button(font_size = 15,text_size = (200,20),valign ="bottom",halign = "left",background_normal = color+"16.png",background_down = color+"16b.png",size_hint_y = None, height = 25 ,markup = True, text = C2+"...Dir\Folder\Archive"+str(i)+".txt" ))
            dim2.add_widget(dim3)
            
            main_dim_grid3_dim1.add_widget(dim2)
        main_dim_grid3_dim1.add_widget(Button(background_normal = color+"16.png"))
        Button3 =Button(text_size = (250,60),valign ="middle",halign = "left",background_normal = color+"15.png",size_hint_y = None, height = 45 ,markup = True, text = C4+"New source")
        main_dim_grid3_dim1.add_widget(Button3)
        Button3.bind(on_release = lambda x: self.agregarconexion())
        
        main_dim_grid3_dim2.add_widget(Button(text_size = (Window.width-300-50,30),valign = "middle",background_normal = color +"3.png",halign = "left",size_hint_y = None , height = 30, text = "Work behavior"))
        self.main_ScreenManager = ScreenManager()
        self.main_ScreenManager_Screen1 = Screen(name = "a")
        self.main_ScreenManager_Screen2 = Screen(name = "b")
        self.main_ScreenManager_Screen3 = Screen(name = "c")
        self.main_ScreenManager_Screen4 = Screen(name = "d")
        self.main_ScreenManager.add_widget(self.main_ScreenManager_Screen1)
        self.main_ScreenManager.add_widget(self.main_ScreenManager_Screen2)
        self.main_ScreenManager.add_widget(self.main_ScreenManager_Screen3)
        self.main_ScreenManager.add_widget(self.main_ScreenManager_Screen4)
        screenset = [self.main_ScreenManager_Screen1,self.main_ScreenManager_Screen2,self.main_ScreenManager_Screen3]
        textset = ["Una plataforma echa a las medidas de nuestros alcances, para uso personal.",
        "Un Nuevo formato para tus bases de datos :v (en realidad es puro texto)",
        "Una Nueva plataforma para tu nuevo formato."]
        for i in range(3):
            dim = GridLayout(cols = 1)
            dim.add_widget(Button(background_normal = color+"16.png"))
            Button1 = Button(background_normal = color+"16.png",background_down = color+"16.png",size_hint_y = None, height = 500, text_size = (500,500), halign = "center", valign = "middle",markup = True, text = C4+textset[i],font_size = 24)
            Button1.bind(on_release = lambda x: self.main_next())
            dim.add_widget(Button1)
            dim.add_widget(Button(background_normal = color+"16.png"))
            screenset[i].add_widget(dim)

        
        main_dim_grid3_dim2.add_widget(self.main_ScreenManager)
        main_dim_relativelay1 = RelativeLayout(size_hint_y = None, size_hint_x = None , width = Window.width-300, height = 60)
        dim2sizex = main_dim_relativelay1.width/2
        dim2sizey = main_dim_relativelay1.height/2
        #main_dim_grid3_dim2.add_widget(main_dim_relativelay1)
        main_dim_relativelay1.add_widget(Image(source = color+"16.png", allow_stretch = True , keep_ratio = False))
        main_dim_relativelay1.add_widget(Image(source = hud+"ball.png",pos = (dim2sizex-25,dim2sizey-25),size_hint = (None,None), size = (50,50), allow_stretch = True , keep_ratio = False))
        main_dim_relativelay1.add_widget(Image(source = hud+"ball.png",pos = (dim2sizex-25-50,dim2sizey-25),size_hint = (None,None), size = (50,50), allow_stretch = True , keep_ratio = False))
        main_dim_relativelay1.add_widget(Image(source = hud+"ball.png",pos = (dim2sizex-25+50,dim2sizey-25),size_hint = (None,None), size = (50,50), allow_stretch = True , keep_ratio = False))

        
        #main_dim_grid3_dim2.add_widget(Button(markup = True,text = C4+"", size_hint_y = .2, height = 60,background_normal = color+"16.png"))
        
        main_ScreenManager_Screen4_grid = GridLayout(cols = 1,spacing = 1)
        main_ScreenManager_Screen4_grid3 = GridLayout(cols = 1,spacing = 0, size_hint_x = None, width = 300, pos = (Window.width-600,0))
        main_ScreenManager_Screen4_grid4 = GridLayout(rows = 1,spacing = 0, size_hint_y = None, height = 45, pos = (0,0))
        
        for i in range(10):
            if i == 0:
                main_ScreenManager_Screen4_grid2 = GridLayout(rows = 1, spacing= 1, size_hint_y = None, height = 35)
                for x in range(5):
                    main_ScreenManager_Screen4_grid2.add_widget(Button(markup = True,text = C4+"Column "+str(x),size_hint_x = None , width = 150,background_normal = color+"16.png"))
                main_ScreenManager_Screen4_grid.add_widget(main_ScreenManager_Screen4_grid2)
                
            main_ScreenManager_Screen4_grid1 = GridLayout(rows = 1, spacing= 1, size_hint_y = None, height = 35)
            for x in range(5):
                main_ScreenManager_Screen4_grid1.add_widget(Button(size_hint_x = None , width = 150,background_normal = color+"16.png"))
            main_ScreenManager_Screen4_grid.add_widget(main_ScreenManager_Screen4_grid1)
            
        self.main_ScreenManager_Screen4.add_widget(Image(source= color + "16b.png", allow_stretch = True , keep_ratio = False))
        self.main_ScreenManager_Screen4.add_widget(main_ScreenManager_Screen4_grid)
        self.main_ScreenManager_Screen4.add_widget(main_ScreenManager_Screen4_grid4)
        self.main_ScreenManager_Screen4.add_widget(main_ScreenManager_Screen4_grid3)
        main_ScreenManager_Screen4_grid4.add_widget(Button(markup= True,text = C4+'Tabla: "[b]Usuarios[/b]"', size_hint_x = None, width =150,background_normal = color + "16.png"))
        main_ScreenManager_Screen4_grid4.add_widget(Button(markup= True,text = C4+"[b]0[/b] Registros", size_hint_x = None, width =100,background_normal = color + "16.png"))
        main_ScreenManager_Screen4_grid4.add_widget(Image(keep_ratio = False, allow_stretch = True,size_hint_x = 1 , source = color + "16.png"))
        main_ScreenManager_Screen4_grid3.add_widget(Image(size_hint_y = None , height = 1 , source = color+"16c.png", keep_ratio = True , allow_stretch = True))
        main_ScreenManager_Screen4_grid3.add_widget(Button(halign = "left",valign = "middle",text_size = (250,35),background_normal = color + "16.png",size_hint_y = None, height = 35 ,markup = True, text = C4+"Tablas"))
        main_ScreenManager_Screen4_grid3.add_widget(Image(source = color + "16b.png", height = 1 , size_hint_y = None))
        tableset = ["Usuarios","Clientes","Facturados","Por Facturar","Inventarios"]
        for i in range(5):
            if i == 0:
                pass
            else:
                main_ScreenManager_Screen4_grid3.add_widget(Image(source =color+"16c.png", allow_stretch = True, keep_ratio = False, size_hint_y = None, height = 1))
            
            dim4 = GridLayout(rows = 1, size_hint_y = None, height =35)
            dim4.add_widget(Image(source = color+"6.png", size_hint_x = None, width = 35, allow_stretch = True, keep_ratio = True))
            dim4.add_widget(Button(halign = "left",valign = "middle",text_size = (250-35,35),background_normal = color + "16.png",size_hint_y = None, height = 35 ,markup = True, text = C2+tableset[i],  ))
            main_ScreenManager_Screen4_grid3.add_widget(dim4)
        main_ScreenManager_Screen4_grid3.add_widget(Button(background_normal = color + "16.png"))
        main_ScreenManager_Screen4_grid3.add_widget(Button(halign = "left",valign = "middle",text_size = (250,35),background_normal = color + "16.png",size_hint_y = None, height = 35 ,markup = True, text = C2+"Añadir Tabla"  ))
        
    def main_next(self):
        self.main_ScreenManager.current = self.main_ScreenManager.next()



    def conectar(self,url):
        with open('C:\Users\Armando\Desktop\Avances\Joe (DBM)\databases\main.set') as f:
            lines = f.readlines()
        for i in lines:
            print i
    def agregarconexion(self):
        def aceptar(button):
            self.pantalla_principall_root.remove_widget(agregarconexion_grid)

        def cancelar(button):
            self.pantalla_principall_root.remove_widget(agregarconexion_grid)

        hud = self.patch + '/hud/'
        icon = self.patch + '/icon/'
        fonts = self.patch + '/fonts/'
        databases = self.patch + '/databases/'
        color = self.patch + '/hud/color/'
        wmedx = Window.width/2
        wmedy = Window.height/2
        C1 = "[color=#13C0C7]"
        C4 = "[color=#000000]"
        C2 = "[color=#404040]"
        C3 = "[color=#ff3333]"
        agregarconexion_grid = GridLayout(cols = 1,size = (350,350) , size_hint =(None,None), pos = (wmedx-175,wmedy-175))
        self.pantalla_principall_root.add_widget(agregarconexion_grid)
        dim7 = GridLayout(rows = 1,size_hint_y =None, height =35)
        agregarconexion_grid.add_widget(Button(text_size = (300,40),valign = "middle",halign = "left",background_normal = color+"3.png",markup = True, text = "[b]N[/b]ueva Fuente de Datos" ,size_hint_y = None, height = 40))
        agregarconexion_grid.add_widget(Button(background_normal = color+"16b.png",markup = True, text = C4+"" ,size_hint_y = None, height = 35))
        agregarconexion_grid.add_widget(Button(text_size = (300,35),halign = "left",background_normal = color+"16b.png",markup = True, text = C4+"Nombre de la Fuente" ,size_hint_y = None, height = 35))
        agregarconexion_grid.add_widget(Button(markup = True,text_size = (300-35,35),halign = "left",valign = "middle",background_normal = color+"16c.png",background_down = color+"16c.png", text = C2+"Proyecto 1" ,size_hint_y = None, height = 35))
        agregarconexion_grid.add_widget(Button(text_size = (300,35),halign = "left",background_normal = color+"16b.png",markup = True, text = C4+"Direccion del Archivo" ,size_hint_y = None, height = 35))
        dim5 = GridLayout(rows = 1,size_hint_y =None, height =35)
        dim6 = GridLayout(rows = 1,size_hint_y =None, height =35)
        dim5.add_widget(Button(markup = True,text_size = (300-35,35),halign = "left",valign = "middle",background_normal = color+"16c.png",background_down = color+"16c.png", text = C2+"...Dir/Carpeta/archive.joe" ,size_hint_y = None, height = 35))
        dim5.add_widget(Image(source = color+"5.png", keep_ratio = False, allow_stretch = True, size_hint_x = None , width =35))
        agregarconexion_grid.add_widget(dim5)
        agregarconexion_grid.add_widget(Button(background_normal = color+"16b.png", text = "" ,size_hint_y = 1, height = 35))
        agregarconexion_grid.add_widget(dim6)
        Button4 = Button(markup = True,text_size = (150,50),halign = "center",valign = "middle",background_normal = color+"16c.png",background_down = color+"16c.png", text = C4+"Aceptar" ,size_hint_y = None, height = 50)
        Button5 = Button(markup = True,text_size = (150,50),halign = "center",valign = "middle",background_normal = color+"16c.png",background_down = color+"16c.png", text = C4+"Cancelar" ,size_hint_y = None, height = 50)
        dim6.add_widget(Button4)
        dim6.add_widget(Button5)
        Button4.bind(on_release = aceptar)
        Button5.bind(on_release = cancelar)
       
class MyApp(App):
    def build(self):
        self.title = "JOE Dataset Manager"
        Window.clearcolor = [0,0,0,1]
        return InterfaceManager()
 

if __name__ in ('__main__', '__android__'):
    MyApp().run()

    
    
    
    
    