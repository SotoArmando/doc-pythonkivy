#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
from kivy.core.audio import SoundLoader,Sound
from kivy.utils import platform
from kivy.metrics import dp, sp

import os   
import os.path
import time
import sys
import urllib2
import requests
import json
import math

Window.size = dp(340), dp(640)


from threading import Timer






if platform() == "android":

    from jnius import cast
    from jnius import autoclass
    MediaPlayer = autoclass('android.media.MediaPlayer')

else:
    print(platform()), "PLATAFORMA"




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
        self.patch = os.path.dirname(os.path.abspath(__file__))
        hud = self.patch + '/hud/'
        icon = self.patch + '/icon/'
        fonts = self.patch + '/fonts/'
        sounds = self.patch + '/sounds/'
        
        
        medx = Window.width/2
        medy = 200/2
        wmedy = Window.height/2
        wmedx = Window.width/2
        C1 = "[color=#000000]"
        C2 = "[color=#404040]"
        C3 = "[color=#ff3333]"
        
        #-------------------------------------------------------------------------ROOT
        self.dimstate1 = False
        self.Contador_state = -1
        self.Tiempo = float(0)
        self.Grado = float(0.0083333333333333)
        self.Grado1 = float(6)
        self.TimeState = float(0)
        print self.Grado
        self.NotificarBtn = Button(markup = True,font_size = 17,text = "Notificar",text_size =(Window.width-64, 32),size_hint = (None,None), pos = (0,Window.height), size = (Window.width, dp(64)), background_normal = hud + "co6.png", allow_stretch = True , keep_ratio = False)
        self.sm = ScreenManager(size_hint = (1,1))
        menulateral= GridLayout(cols = 1)
        
        pantalla1 = Screen(name='Lobby')
        pantalla2 = Screen(name='Lobby2')
        pantalla3 = Screen(name='Lobby3')
        
        strings = ["Iniciar","Detener","Reiniciar","Iniciar Sesion","Salir"]

        #''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        for i in range(5):
            if i == 0:
                menulateral.add_widget(Image(size_hint_y = None , height = dp(64),source = hud+"None.png", keep_ratio = False , allow_stretch = True))
            menulateral_dim = GridLayout(rows = 1, size_hint_y = None, height = dp(64))
            menulateral_dim.add_widget(Image(size_hint_y = None , height = dp(64),text = "",size_hint_x=None, width = 64, source = hud+"themify_e622(0)_64.png"))
            menulateral_dim.add_widget(Button(size_hint_y = None , height = dp(64),markup = True,text_size = (medx-80,dp(64)), valign = "middle",text = C1+strings[i] , background_normal = hud+"None.png"))
            menulateral.add_widget(menulateral_dim)
            menulateral.add_widget(Image(size_hint_y = None , height = 1,source = hud+"blindbar1.png", keep_ratio = False , allow_stretch = True))
            
        self.ROOT_Navitagiondrawer1 = NavigationDrawer(size_hint = (1,1))
        self.ROOT_Navitagiondrawer1.add_widget(menulateral)
        self.ROOT_Navitagiondrawer1.add_widget(self.sm)
        self.ROOT_Navitagiondrawer1.anim_type = 'slide_above_simple'
        
        
        
        self.sm.add_widget(pantalla1)
        self.sm.add_widget(pantalla2)
        self.sm.add_widget(pantalla3)
        ##-------------------------------------------------------------------------
        
        
        
        
        
        
        
        
        
        
        
        
        #-------------------------------------------------------------------------PANTALLA1
    
        
        pantalla1_grid1 = GridLayout(cols = 1)
        pantalla1_relat1 = RelativeLayout(cols = 1, size_hint = (1,None), height = dp(100))
        pantalla1_grid1_dim1 = GridLayout(cols = 7, size_hint = (1,None), height = dp(107))
        pantalla1_grid1_dim2 = GridLayout(cols = 7, size_hint = (1,None), height = dp(107))
        pantalla1_grid1_dim3 = GridLayout(cols = 7, size_hint = (1,None), height = dp(107))
        self.pantalla1_grid1_dim1_root = Screen(name = "a",cols = 7, size_hint = (1,None), height = dp(107))
        self.pantalla1_grid1_dim1_root2 = Screen(name = "b",cols = 7, size_hint = (1,None), height = dp(107))
        self.pantalla1_grid1_dim1_root3 = Screen(name = "c",cols = 7, size_hint = (1,None), height = dp(107))
        self.pantalla1_grid1_dim1_root_screen = ScreenManager(cols = 7, size_hint = (1,None), height = dp(107))
        self.pantalla1_grid1_dim1_root_screen.add_widget(self.pantalla1_grid1_dim1_root)
        self.pantalla1_grid1_dim1_root_screen.add_widget(self.pantalla1_grid1_dim1_root2)
        self.pantalla1_grid1_dim1_root_screen.add_widget(self.pantalla1_grid1_dim1_root3)
        
        self.pantalla1_grid1_dim1_root.add_widget(pantalla1_grid1_dim1)
        self.pantalla1_grid1_dim1_root2.add_widget(pantalla1_grid1_dim2)
        self.pantalla1_grid1_dim1_root3.add_widget(pantalla1_grid1_dim3)
        
        pantalla1_relat1_image1 = Image(size_hint = (None,None),width = Window.width, height = dp(200), source = hud+"hud1.png", keep_ratio = True)
        self.pantalla1_relat1_image2_Scatter = Scatter(size_hint = (None,None),width = Window.width, height = dp(200), source = hud+"hud9.png", keep_ratio = True,do_scale=False, do_translation_y=False,do_translation_x=False)
        self.pantalla1_relat1_image3_Scatter = Scatter(size_hint = (None,None),width = Window.width, height = dp(200), source = hud+"hud9.png", keep_ratio = True,do_scale=False, do_translation_y=False,do_translation_x=False)
        
        pantalla1_relat1_image2 = Image(size_hint = (None,None),width = Window.width, height = dp(200), source = hud+"hud9.png", keep_ratio = True)
        pantalla1_relat1_image3 = Image(size_hint = (None,None),width = Window.width, height = dp(200), source = hud+"hud10.png", keep_ratio = True)
        self.pantalla1_relat1_image2_Scatter.add_widget(pantalla1_relat1_image2)
        self.pantalla1_relat1_image3_Scatter.add_widget(pantalla1_relat1_image3)

        
        pantalla1_relat1_image4 = Image(size_hint = (None,None),size  = (dp(14),dp(15)), source = hud+"xy.png", keep_ratio = False,pos = (medx-7,medy-7.5), allow_stretch = True)
        
        
        for i in range(2):
            img = ["b3","b3","b3"]
            if i == 1:
                T1="30 S"
                T2="1 M"
                T3="3 M"
            else:
                T1=""
                T2=""
                T3=""
            if i == 0:    
                pantalla1_grid1_dim1.add_widget(Image(source = hud+"None.png",allow_stretch = True,keep_ratio = False))
                Button5 = Button(size_hint = (None,None), size = (dp(64),dp(20.0)),background_normal = hud+img[i]+".png", text = C1+T1,markup = True, font_size = dp(23))
                Button5.bind(on_release = lambda x: self.AumentarTiempo(float(30.0),x))
                pantalla1_grid1_dim1.add_widget(Button5)
                
                pantalla1_grid1_dim1.add_widget(Image(source = hud+"None.png",allow_stretch = True,keep_ratio = False))
                Button6 = Button(size_hint = (None,None), size = (dp(64),dp(20.0)),background_normal = hud+img[i]+".png", text = C1+T2,markup = True, font_size = dp(23))
                Button6.bind(on_release = lambda x: self.AumentarTiempo(float(60.0),x))
                pantalla1_grid1_dim1.add_widget(Button6)
                
                pantalla1_grid1_dim1.add_widget(Image(source = hud+"None.png",allow_stretch = True,keep_ratio = False))
                Button7 =  Button(size_hint = (None,None), size = (dp(64),dp(20.0)),background_normal = hud+img[i]+".png", text = C1+T3,markup = True, font_size = dp(23))
                Button7.bind(on_release = lambda x: self.AumentarTiempo(float(180.0),x))
                pantalla1_grid1_dim1.add_widget(Button7)
                
                pantalla1_grid1_dim1.add_widget(Image(source = hud+"None.png",allow_stretch = True,keep_ratio = False))
            else:
                print i
                pantalla1_grid1_dim1.add_widget(ImageButton(source = hud+"None.png",allow_stretch = True,keep_ratio = False))
                Button5 = Button(size_hint = (None,None), size = (dp(64),dp(64)),background_normal = hud+img[i]+".png",background_down = hud+img[i]+".png", text = C1+T1,markup = True, font_size = 30)
                Button5_Scatter = Scatter(size_hint = (None,None), size = (dp(64),dp(64)),background_normal = hud+img[i]+".png",background_down = hud+img[i]+".png", text = C1+T1,markup = True, font_size = 30)
                Button5_Grid = GridLayout(cols = 1 , size_hint = (None,None), size = (dp(64),dp(64)),background_normal = hud+img[i]+".png",background_down = hud+img[i]+".png", text = C1+T1,markup = True, font_size = 30)
                Button5_Scatter.add_widget(Button5)
                Button5_Grid.add_widget(Button5_Scatter)
                Button5.bind(on_release = lambda x: self.AumentarTiempo(float(30.0),x))
                pantalla1_grid1_dim1.add_widget(Button5_Grid)
                
                pantalla1_grid1_dim1.add_widget(Image(source = hud+"None.png",allow_stretch = True,keep_ratio = False))
                Button6 = Button(size_hint = (None,None), size = (dp(64),dp(64)),background_normal = hud+img[i]+".png",background_down = hud+img[i]+".png", text =  C1+T2,markup = True, font_size = 30)
                Button6_Scatter = Scatter(size_hint = (None,None), size = (dp(64),dp(64)),background_normal = hud+img[i]+".png",background_down = hud+img[i]+".png", text =  C1+T2,markup = True, font_size = 30)
                Button6_Grid = GridLayout(cols = 1,size_hint = (None,None), size = (dp(64),dp(64)),background_normal = hud+img[i]+".png",background_down = hud+img[i]+".png", text =  C1+T2,markup = True, font_size = 30)
                Button6_Scatter.add_widget(Button6)
                Button6_Grid.add_widget(Button6_Scatter)
                Button6.bind(on_release = lambda x: self.AumentarTiempo(float(60.0),x))
                pantalla1_grid1_dim1.add_widget(Button6_Grid)
                
                pantalla1_grid1_dim1.add_widget(Image(source = hud+"None.png",allow_stretch = True,keep_ratio = False))
                Button7 =  Button(size_hint = (None,None), size = (dp(64),dp(64)),background_normal = hud+img[i]+".png",background_down = hud+img[i]+".png", text = C1+T3,markup = True, font_size = 30)
                Button7_Scatter = Scatter(size_hint = (None,None), size = (dp(64),dp(64)),background_normal = hud+img[i]+".png",background_down = hud+img[i]+".png", text = C1+T1,markup = True, font_size = 30)
                Button7_Grid = GridLayout(cols = 1 , size_hint = (None,None), size = (dp(64),dp(64)),background_normal = hud+img[i]+".png",background_down = hud+img[i]+".png", text = C1+T3,markup = True, font_size = 30)
                Button7_Scatter.add_widget(Button7)
                Button7_Grid.add_widget(Button7_Scatter)
                Button7.bind(on_release = lambda x: self.AumentarTiempo(float(180.0),x))
                pantalla1_grid1_dim1.add_widget(Button7_Grid)
                
                pantalla1_grid1_dim1.add_widget(ImageButton(source = hud+"None.png",allow_stretch = True,keep_ratio = True))

        for i in range(2):
            img = ["b3","b3","b3"]
            if i == 1:
                T1="3 M"
                T2="5 M"
                T3="15 M"
            else:
                T1=""
                T2=""
                T3=""
            if i == 0:    
                pantalla1_grid1_dim2.add_widget(Image(source = hud+"None.png",allow_stretch = True,keep_ratio = False))
                Button5 = Button(size_hint = (None,None), size = (dp(64),dp(20.0)),background_normal = hud+img[i]+".png", text = C1+T1,markup = True, font_size = dp(23))
                Button5.bind(on_release = lambda x: self.AumentarTiempo(float(180.0),x))
                pantalla1_grid1_dim2.add_widget(Button5)
                
                pantalla1_grid1_dim2.add_widget(Image(source = hud+"None.png",allow_stretch = True,keep_ratio = False))
                Button6 = Button(size_hint = (None,None), size = (dp(64),dp(20.0)),background_normal = hud+img[i]+".png", text = C1+T2,markup = True, font_size = dp(23))
                Button6.bind(on_release = lambda x: self.AumentarTiempo(float(300.0),x))
                pantalla1_grid1_dim2.add_widget(Button6)
                
                pantalla1_grid1_dim2.add_widget(Image(source = hud+"None.png",allow_stretch = True,keep_ratio = False))
                Button7 =  Button(size_hint = (None,None), size = (dp(64),dp(20.0)),background_normal = hud+img[i]+".png", text = C1+T3,markup = True, font_size = dp(23))
                Button7.bind(on_release = lambda x: self.AumentarTiempo(float(900.0),x))
                pantalla1_grid1_dim2.add_widget(Button7)
                
                pantalla1_grid1_dim2.add_widget(Image(source = hud+"None.png",allow_stretch = True,keep_ratio = False))
            else:
                print i
                pantalla1_grid1_dim2.add_widget(ImageButton(source = hud+"None.png",allow_stretch = True,keep_ratio = False))
                Button5 = Button(size_hint = (None,None), size = (dp(64),dp(64)),background_normal = hud+img[i]+".png",background_down = hud+img[i]+".png", text = C1+T1,markup = True, font_size = 30)
                Button5_Scatter = Scatter(size_hint = (None,None), size = (dp(64),dp(64)),background_normal = hud+img[i]+".png",background_down = hud+img[i]+".png", text = C1+T1,markup = True, font_size = 30)
                Button5_Grid = GridLayout(cols = 1 , size_hint = (None,None), size = (dp(64),dp(64)),background_normal = hud+img[i]+".png",background_down = hud+img[i]+".png", text = C1+T1,markup = True, font_size = 30)
                Button5_Scatter.add_widget(Button5)
                Button5_Grid.add_widget(Button5_Scatter)
                Button5.bind(on_release = lambda x: self.AumentarTiempo(float(180.0),x))
                pantalla1_grid1_dim2.add_widget(Button5_Grid)
                
                pantalla1_grid1_dim2.add_widget(Image(source = hud+"None.png",allow_stretch = True,keep_ratio = False))
                Button6 = Button(size_hint = (None,None), size = (dp(64),dp(64)),background_normal = hud+img[i]+".png",background_down = hud+img[i]+".png", text =  C1+T2,markup = True, font_size = 30)
                Button6_Scatter = Scatter(size_hint = (None,None), size = (dp(64),dp(64)),background_normal = hud+img[i]+".png",background_down = hud+img[i]+".png", text =  C1+T2,markup = True, font_size = 30)
                Button6_Grid = GridLayout(cols = 1,size_hint = (None,None), size = (dp(64),dp(64)),background_normal = hud+img[i]+".png",background_down = hud+img[i]+".png", text =  C1+T2,markup = True, font_size = 30)
                Button6_Scatter.add_widget(Button6)
                Button6_Grid.add_widget(Button6_Scatter)
                Button6.bind(on_release = lambda x: self.AumentarTiempo(float(300.0),x))
                pantalla1_grid1_dim2.add_widget(Button6_Grid)
                
                pantalla1_grid1_dim2.add_widget(Image(source = hud+"None.png",allow_stretch = True,keep_ratio = False))
                Button7 =  Button(size_hint = (None,None), size = (dp(64),dp(64)),background_normal = hud+img[i]+".png",background_down = hud+img[i]+".png", text = C1+T3,markup = True, font_size = 30)
                Button7_Scatter = Scatter(size_hint = (None,None), size = (dp(64),dp(64)),background_normal = hud+img[i]+".png",background_down = hud+img[i]+".png", text = C1+T1,markup = True, font_size = 30)
                Button7_Grid = GridLayout(cols = 1 , size_hint = (None,None), size = (dp(64),dp(64)),background_normal = hud+img[i]+".png",background_down = hud+img[i]+".png", text = C1+T3,markup = True, font_size = 30)
                Button7_Scatter.add_widget(Button7)
                Button7_Grid.add_widget(Button7_Scatter)
                Button7.bind(on_release = lambda x: self.AumentarTiempo(float(900.0),x))
                pantalla1_grid1_dim2.add_widget(Button7_Grid)
                
                pantalla1_grid1_dim2.add_widget(ImageButton(source = hud+"None.png",allow_stretch = True,keep_ratio = True))

        for i in range(2):
            img = ["b3","b3","b3"]
            if i == 1:
                T1="15 M"
                T2="30 M"
                T3="1 H"
            else:
                T1=""
                T2=""
                T3=""
            if i == 0:    
                pantalla1_grid1_dim3.add_widget(Image(source = hud+"None.png",allow_stretch = True,keep_ratio = False))
                Button5 = Button(size_hint = (None,None), size = dp(64),dp(20.0)),background_normal = hud+img[i]+".png", text = C1+T1,markup = True, font_size = dp(23))
                Button5.bind(on_release = lambda x: self.AumentarTiempo(float(900.0),x))
                pantalla1_grid1_dim3.add_widget(Button5)
                
                pantalla1_grid1_dim3.add_widget(Image(source = hud+"None.png",allow_stretch = True,keep_ratio = False))
                Button6 = Button(size_hint = (None,None), size = dp(64),dp(20.0)),background_normal = hud+img[i]+".png", text = C1+T2,markup = True, font_size = dp(23))
                Button6.bind(on_release = lambda x: self.AumentarTiempo(float(1800.0),x))
                pantalla1_grid1_dim3.add_widget(Button6)
                
                pantalla1_grid1_dim3.add_widget(Image(source = hud+"None.png",allow_stretch = True,keep_ratio = False))
                Button7 =  Button(size_hint = (None,None), size = dp(64),dp(20.0)),background_normal = hud+img[i]+".png", text = C1+T3,markup = True, font_size = dp(23))
                Button7.bind(on_release = lambda x: self.AumentarTiempo(float(3600.0),x))
                pantalla1_grid1_dim3.add_widget(Button7)
                
                pantalla1_grid1_dim3.add_widget(Image(source = hud+"None.png",allow_stretch = True,keep_ratio = False))
            else:
                print i
                pantalla1_grid1_dim3.add_widget(ImageButton(source = hud+"None.png",allow_stretch = True,keep_ratio = False))
                Button5 = Button(size_hint = (None,None), size = (dp(64),dp(64)),background_normal = hud+img[i]+".png",background_down = hud+img[i]+".png", text = C1+T1,markup = True, font_size = dp(30))
                Button5_Scatter = Scatter(size_hint = (None,None), size = (dp(64),dp(64)),background_normal = hud+img[i]+".png",background_down = hud+img[i]+".png", text = C1+T1,markup = True, font_size = 30)
                Button5_Grid = GridLayout(cols = 1 , size_hint = (None,None), size = (dp(64),dp(64)),background_normal = hud+img[i]+".png",background_down = hud+img[i]+".png", text = C1+T1,markup = True, font_size = dp(30))
                Button5_Scatter.add_widget(Button5)
                Button5_Grid.add_widget(Button5_Scatter)
                Button5.bind(on_release = lambda x: self.AumentarTiempo(float(900.0),x))
                pantalla1_grid1_dim3.add_widget(Button5_Grid)
                
                pantalla1_grid1_dim3.add_widget(Image(source = hud+"None.png",allow_stretch = True,keep_ratio = False))
                Button6 = Button(size_hint = (None,None), size = (dp(64),dp(64)),background_normal = hud+img[i]+".png",background_down = hud+img[i]+".png", text =  C1+T2,markup = True, font_size = dp(30))
                Button6_Scatter = Scatter(size_hint = (None,None), size = (dp(64),dp(64)),background_normal = hud+img[i]+".png",background_down = hud+img[i]+".png", text =  C1+T2,markup = True, font_size = dp(30))
                Button6_Grid = GridLayout(cols = 1,size_hint = (None,None), size = (dp(64),dp(64)),background_normal = hud+img[i]+".png",background_down = hud+img[i]+".png", text =  C1+T2,markup = True, font_size = dp(30))
                Button6_Scatter.add_widget(Button6)
                Button6_Grid.add_widget(Button6_Scatter)
                Button6.bind(on_release = lambda x: self.AumentarTiempo(float(1800.0),x))
                pantalla1_grid1_dim3.add_widget(Button6_Grid)
                
                pantalla1_grid1_dim3.add_widget(Image(source = hud+"None.png",allow_stretch = True,keep_ratio = False))
                Button7 =  Button(size_hint = (None,None), size = (dp(64),dp(64)),background_normal = hud+img[i]+".png",background_down = hud+img[i]+".png", text = C1+T3,markup = True, font_size = 30)
                Button7_Scatter = Scatter(size_hint = (None,None), size = (dp(64),dp(64)),background_normal = hud+img[i]+".png",background_down = hud+img[i]+".png", text = C1+T1,markup = True, font_size = dp(30))
                Button7_Grid = GridLayout(cols = 1 , size_hint = (None,None), size = (dp(64),dp(64)),background_normal = hud+img[i]+".png",background_down = hud+img[i]+".png", text = C1+T3,markup = True, font_size = 30)
                Button7_Scatter.add_widget(Button7)
                Button7_Grid.add_widget(Button7_Scatter)
                Button7.bind(on_release = lambda x: self.AumentarTiempo(float(3600.0),x))
                pantalla1_grid1_dim3.add_widget(Button7_Grid)
                
                pantalla1_grid1_dim3.add_widget(ImageButton(source = hud+"None.png",allow_stretch = True,keep_ratio = True))
        
        pantalla1_grid2 = GridLayout(cols = 5 , size_hint_y = None, height = dp(80))
        
        #''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        pantalla1_relat1.add_widget(pantalla1_relat1_image1)
        pantalla1_relat1.add_widget(self.pantalla1_relat1_image2_Scatter)
        pantalla1_relat1.add_widget(self.pantalla1_relat1_image3_Scatter)
        
        pantalla1_grid1.add_widget(Image(source = hud+"None.png", allow_stretch = True, keep_ratio = False))
        self.Tiempo_text2 = Button(background_normal = hud+"None.png" ,background_down = hud+"None.png" ,size_hint_y = None , height = 120,  text = C1+"00:00:00",markup = True, font_size = '90sp', font_name = fonts+"FiraSans-Thin")
       
        #pantalla1_grid1.add_widget(Image(source = hud+"blindbar2.png",size_hint_y = None, height = 1, allow_stretch = True, keep_ratio = False))
        choose_height = dp(100)
        choose = ScrollView(bar_margin = 0,size_hint_y = None, height = choose_height,do_scroll_y = False, do_scroll_x = True,scroll_x = 0.5,bar_color = [0,0,0,.6],bar_inactive_color = [.7,.7,.7,.2],scroll_type = ['content'],bar_width = 3, bar_pos_x = "top")
        chooseroot_root = RelativeLayout(size_hint_y = None, size_hint_x = None, height = choose_height, width = 1000 + ((wmedx-64)*2)+45)
        chooseroot = GridLayout(rows = 1, size_hint_y = None, size_hint_x = None, height = choose_height, spacing = 5)
        chooseroot_root.add_widget(chooseroot)
        choose.add_widget(chooseroot_root)
        self.medio = Image(source = icon + "clock.png", size_hint = (None,None), size = (24,24), pos = (0,100-30))
        chooseroot_root.add_widget(self.medio)
        imgset = ["bacon","bread","coffeex","fried-egg","meat","toaster","tea","teapot","pizza","shrimp",]
        for i in range(10):  
                
            if i == 0:
                chooseroot.add_widget(Image(source = hud+"None.png",allow_stretch = True, keep_ratio = False,size_hint_x = None, width = dp(wmedx-64)))
            self.container = GridLayout(cols = 1, size_hint = (None,None), size = (choose_height,choose_height))
            image = ImageButton(source = icon +imgset[i]+".png",size_hint = (None,None) , width = dp(64)),height = dp(64)), allow_stretch = True,  keep_ratio = True, pos = (50-32,50-32))
            self.imagescatter = Scatter(scale = 1,do_translation_y=False,do_translation_x=False,source = icon +imgset[i],size_hint = (None,None) , size = (choose_height,choose_height), allow_stretch = True,  keep_ratio = True)
            image.bind(on_press =lambda x: self.Animatesize(x.parent))
            self.imagescatter.add_widget(image)
            self.container.add_widget(self.imagescatter)
            chooseroot.add_widget(self.container)
            if i == 9:
                chooseroot.add_widget(Image(source = hud+"None.png",allow_stretch = True, keep_ratio = False,size_hint_x = None, width = dp(wmedx-64)))
        
        


            

        chooseroot.bind(minimum_width=chooseroot.setter('width'))

        pantalla1_grid1_dim4 = GridLayout(rows = 1, size_hint_y = None, height = dp(10))
        #pantalla1_grid1_dim4.add_widget(Image(source = hud+"None.png", allow_stretch = True, keep_ratio = False,size_hint_y = None, height =50  ))
        self.TiempoTxt = Button(markup = True,font_size = sp(15),halign = "center",text_size =(Window.width,50+220),text = C1+"Comienza a Cocinar :D !",background_normal = hud+"None.png",background_down = hud+"None.png", allow_stretch = True, keep_ratio = False,size_hint_y = None, height =10  )
        pantalla1_grid1_dim4.add_widget(self.TiempoTxt)
        pantalla1_grid1.add_widget(choose)
        pantalla1_grid1.add_widget(pantalla1_grid1_dim4)
        self.Diseno_Text = GridLayout(cols = 10, size_hint_y = None , height = dp(120))
        Letras = ["0","0",":","0","0",":","0","0"]
        self.Diseno_Text.add_widget(Label())
        self.Botones = []
        for i in Letras:  
            if Window.width > Window.height:
                ButtonX = Button(size_hint_x = .15,font_size = sp(Window.width/12),markup = True,text = C1+i,background_normal = hud +"None2.png")
                self.Diseno_Text.add_widget(ButtonX)
                self.Botones.append(ButtonX)
            else:
                ButtonX = Button(size_hint_x = .75,font_size = sp(Window.width/7),markup = True,text = C1+i,background_normal = hud +"None2.png")
                self.Diseno_Text.add_widget(ButtonX)
                self.Botones.append(ButtonX)
                
        self.Diseno_Text.add_widget(Label())
        pantalla1_grid1.add_widget(self.Diseno_Text)
        #pantalla1_grid1.add_widget(self.Tiempo_text2)
        #pantalla1_grid1.add_widget(pantalla1_relat1)   
        pantalla1_grid1.add_widget(pantalla1_grid2)
        pantalla1_grid1.add_widget(self.pantalla1_grid1_dim1_root_screen)
        #pantalla1_grid1.add_widget(Button(background_normal = hud+"None.png" ,size_hint_y = None , height = 50,  text = "[color=#00A2E8]"+"Sin fijar recetas. [b]Agrega tus Recetas!",markup = True, font_size = 17))
        pantalla1_grid1.add_widget(Button(background_normal = hud+"None.png" ,size_hint_y = None , height = dp(25),  text = C1+"",markup = True, font_size = 17))
        #pantalla1_grid1.add_widget(Image(source = hud+"blindbar2.png",size_hint_y = None, height = 1, allow_stretch = True, keep_ratio = False))
        pantalla1_grid1.add_widget(Image(source = hud+"None.png", allow_stretch = True, keep_ratio = False))
        pantalla1.add_widget(pantalla1_grid1)
        ##-------------------------------------------------------------------------

        
        
        
        
        
     

        self.Button1 = Button(size_hint = (None,None), size = (dp(64),dp(64)), pos = (0,wmedy-32-20), background_normal = hud+"hud11.png",markup = True , text = C1+"",font_size = 72 , font_name = fonts+"FiraSans-Light")
        self.Button2 = Button(size_hint = (None,None), size = (dp(dp(64),dp(64)), pos = (Window.width-64,wmedy-32-20), background_normal = hud+"hud12.png",markup = True , text = C1+"",font_size = 72, font_name = fonts+"FiraSans-Light")
        Root_grid = GridLayout(rows = 1, pos = (0, Window.height - 64), height = dp(64)), size_hint = (1,None),spacing = 0)
        Button3 = Button(background_normal = hud+"hud13.png", size_hint_x = None , width = dp(64)),)
        Button4 = Button(background_normal = hud+"hud13.png", size_hint_x = None , width = dp(64)
        
        Button5 = Button(background_normal = hud+"hud15.png",background_down = hud+"hud15.png", size_hint = (None,None) , height = dp(64)),width = dp(64)
        Button6 = Button(background_normal = hud+"hud14.png",background_down = hud+"hud14.png", size_hint = (None,None), height = dp(64)), width = dp(64)
        Button7 = Button(background_normal = hud+"hud16.png",background_down = hud+"hud16.png", size_hint = (None,None) , height = dp(64)), width = dp(64)
        Button5.bind(on_release = lambda x: self.activar_state())
        Button6.bind(on_release = lambda x: self.ReiniciarTiempo(x))
        Button7.bind(on_release = lambda x: self.ReducirTiempo(self.Tiempo))
        
        Button5_container = GridLayout(cols = 1 , size_hint = (None,None),size =dp(64),dp(64))
        Button6_container = GridLayout(cols = 1 , size_hint = (None,None),size =dp(64),dp(64))
        Button7_container = GridLayout(cols = 1 , size_hint = (None,None),size =dp(64),dp(64))
        
        Button5_Scatter = Scatter(background_normal = hud+"hud15.png",background_down = hud+"hud15.png", size_hint = (None,None) , height = dp(64)),width = dp(64)
        Button6_Scatter = Scatter(background_normal = hud+"hud14.png",background_down = hud+"hud14.png", size_hint = (None,None), height = dp(64)), width = dp(64)
        Button7_Scatter = Scatter(background_normal = hud+"hud16.png",background_down = hud+"hud16.png", size_hint = (None,None) , height = dp(64)), width = dp(64)
        
        Button5_Scatter.add_widget(Button5)
        Button6_Scatter.add_widget(Button6)
        Button7_Scatter.add_widget(Button7)
        
        Button5_container.add_widget(Button5_Scatter)
        Button6_container.add_widget(Button6_Scatter)
        Button7_container.add_widget(Button7_Scatter)
        

        
        #Root_grid.add_widget(Button3)
        Root_grid.add_widget(Button4)

        Root_grid.add_widget(Button(background_normal = hud+"co6.png",))

        
        Button3.bind(on_release = self.ROOT_Navitagiondrawer1.toggle_state)
        Button4.bind(on_release = lambda x: self.Notificar("Demasiado Duro!"))
        Button5.bind(on_press =lambda x: self.Animatesize(x.parent))
        Button6.bind(on_press =lambda x: self.Animatesize(x.parent))
        Button7.bind(on_press =lambda x: self.Animatesize(x.parent))
        self.Button2.bind(on_release  = lambda x: self.next("Lobby2"))
        self.Button1.bind(on_release  = lambda x: self.previous("Lobby"))
        self.add_widget(self.ROOT_Navitagiondrawer1)
        self.add_widget(self.Button1)
        self.add_widget(self.Button2)

        
        pantalla1_grid2.add_widget(Label())
        pantalla1_grid2.add_widget(Label(size_hint_x = None , width = dp(64))
        pantalla1_grid2.add_widget(Label(size_hint_x = None , width = dp(64))
        pantalla1_grid2.add_widget(Label(size_hint_x = None , width = dp(64))
        pantalla1_grid2.add_widget(Label())
        
        pantalla1_grid2.add_widget(Label())
        pantalla1_grid2.add_widget(Button5_container)
        pantalla1_grid2.add_widget(Button6_container)
        pantalla1_grid2.add_widget(Button7_container)
        pantalla1_grid2.add_widget(Label())
        
        self.add_widget(Root_grid)
        self.add_widget(self.NotificarBtn)
        
        
        self.activar_contar()

        
        
        
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def activar_contar(self):
        
        if self.Tiempo == 0:
            pass
            if self.Contador_state == -1: threading.Timer(1, self.activar_contar).cancel()
        else:
            if self.Contador_state == 1: 
                threading.Timer(1, self.activar_contar).start()
                self.contar()
                self.CalcularTiempo(1)
                
          


           
    def activar_state(self):
        self.Contador_state *= -1
        self.activar_contar()
        print self.Contador_state
        
    def cambiar(self,text):
        
        self.sm.current = text
      
    def next(self,button):
        print (self.pantalla1_grid1_dim1_root_screen.next())
        self.pantalla1_grid1_dim1_root_screen.transition = transition = SlideTransition(direction ="left")
        self.pantalla1_grid1_dim1_root_screen.current = self.pantalla1_grid1_dim1_root_screen.next()
        
    def previous(self,button):
        print (self.pantalla1_grid1_dim1_root_screen.previous())
        self.pantalla1_grid1_dim1_root_screen.transition = transition = SlideTransition(direction ="right")
        self.pantalla1_grid1_dim1_root_screen.current = self.pantalla1_grid1_dim1_root_screen.previous()
             
    def contar(self):  
        self.Tiempo -= 1
        self.CalcularTiempo(1)
        
      

    def Notificar(self,text):
        self.NotificarBtn.text = text
        anim2 = Animation(x=0, y=Window.height,t='in_out_sine', d = .5)
        t2 = Timer(1.75,lambda x=1: anim2.start(self.NotificarBtn))
        anim = Animation(x=0, y= Window.height-64  ,t='in_out_sine', d = .5)
        t4 = Timer(0.25,lambda x=1: anim.start(self.NotificarBtn))
        t4.start()
        t2.start()
        #t3 = Timer(3,lambda x=1:self.definir2(text))
        #t3.start()
    
    def rotate1(self,button):
        self.scatter1.rotation -= 30
        
    def Activar(self):
        C1 = "[color=#000000]"  
        mPlayer = MediaPlayer()
        mPlayer.setDataSource(self.patch + '\sounds\default.wav')
        mPlayer.prepare()
        mPlayer.start()

            

   

            

        
    def CalcularTiempo(self,In):

        hud = self.patch + '/hud/'
        icon = self.patch + '/icon/'
        fonts = self.patch + '/fonts/'
        
        C1 = "[color=#000000]"
        #In = [2,30,59]
        #tiempo = float((In[0]*216000)+(In[1]*3600)+(In[2]*60))
        
        segundos = (((self.Tiempo/60))%1)*60
        minutos = ((((self.Tiempo/60))/60)%1)*60
        horas = (((((self.Tiempo/60))/60)/60)%1)*60

        print ("Calculando" + str(self.Tiempo) + " segundos...")
        if self.dimstate1 == True:
            self.dimstate1 = False
            pass
        else:
            if self.Tiempo == 0: self.Activar()

            
        
        if segundos< 10:
            segundos = "0"+ str(segundos)[:-2]
        else:
            segundos = str(segundos)[:-2]
            
        if minutos< 10:
            minutos = "0"+ str(int(minutos))
        else:
            minutos = str(int(minutos))

        if horas < 10:
            horas = "0"+ str(int(horas))
        else:
            horas = str(int(horas))
            
        a = -1*(self.Grado*self.Tiempo)
        b = -1*(self.Grado1*self.Tiempo)
        TimeVar = (str(horas)+":"+str(minutos)+":"+str(segundos))
        self.pantalla1_relat1_image2_Scatter.rotation = a
        self.pantalla1_relat1_image3_Scatter.rotation = b
        self.Tiempo_text2.text= (C1+str(horas)+":"+str(minutos)+":"+str(segundos))
        self.TiempoTxt.text = (C1+str(horas)+" Horas "+str(minutos)+" Minutos y "+str(segundos))+" segundos"
        print TimeVar
        cc = 0
        for i in TimeVar: 
            self.Botones[cc].text = C1+i
            cc += 1
        print horas
        print minutos
        print segundos
        
        


        
    def AumentarTiempo(self,Plus,button):
        self.Animatesize(button.parent)
        self.Tiempo += Plus
        self.CalcularTiempo(1)
        self.TimeState = self.Tiempo
        

        
    def ReiniciarTiempo(self,button):
        #self.Animatesize(button.parent)
        self.Tiempo = self.TimeState
        self.CalcularTiempo(1)
        if self.Contador_state == 1: self.Contador_state *= -1
        
    def Animatesize(self,button):

        print button.parent.pos

        
        anim3 = Animation(x = button.parent.pos[0], d = .75, t = "in_out_back")
        anim3.start(self.medio)
        button.scale = 1.0
        anim1 = Animation(scale = 1.5, d = .05,t = "in_circ")
        anim2 = Animation(scale = 1.0, d = .15,t = "out_circ")
        anim = anim1 + anim2
        anim.start(button)

    def ReducirTiempo(self,Plus):
        C1 = "[color=#000000]"
        if Plus == self.Tiempo:
            self.dimstate1 = True
        self.Tiempo -= Plus
        self.CalcularTiempo(1)
        if self.Contador_state == 1: self.Contador_state *= -1
        
        threading.Timer(1, self.activar_contar).cancel()
        Letras = ["0","0",":","0","0",":","0","0"]
        for i in self.Botones:
            i.text = C1+Letras[self.Botones.index(i)]
    
class MyApp(App):
    def build(self):
        return InterfaceManager()
        

if __name__ in ('__main__', '__android__'):
    MyApp().run()

    

    
    
    
    
    