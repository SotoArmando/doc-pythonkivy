#!/usr/bin/env python
# -*- coding: utf-8 -*-
from kivy.config import Config
Config.set('graphics','borderless',0)
Config.set('graphics','resizable',0)
Config.set('graphics','position','custom')
Config.set('graphics','left',1000)
Config.set('graphics','top',35)
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

Window.size = (426,640)
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
        self.patch = os.path.dirname(os.path.abspath(__file__))
        Window.clearcolor = (1, 1, 1, 1)
        hud = self.patch + '/hud/'
        icon = self.patch + '/icon/'
        fonts = self.patch + '/fonts/'
        Pantalla = GridLayout(cols = 1, size_hint_y = None, height = 1000)
        Pantalla.bind(minimum_width=Pantalla.setter('height'))
        Pantalla_ScrollView = ScrollView(size_hint = (1,1))
        wmedy = Window.height/2
        wmedx = Window.width/2
        C1 = "[color=#13C0C7]"
        C4 = "[color=#000000]"
        C2 = "[color=#404040]"
        C3 = "[color=#ff3333]"
        self.Main_ScreenManager = ScreenManager(size_hint = (1,1))
        Main_Screen = Screen(name = "a")
        Main_Screen1 = Screen(name = "b")
        Main_Screen2 = Screen(name = "c")
        
        self.Main_ScreenManager.add_widget(Main_Screen)
        self.Main_ScreenManager.add_widget(Main_Screen1)
        self.Main_ScreenManager.add_widget(Main_Screen2)
        Main_Screen2_Grid1 = GridLayout(cols =1)
        Main_Screen2.add_widget(Main_Screen2_Grid1)
        mapsset = ["Frog Isle","Jaguar Falls","Serpent Beach","Fish Market","Timber Mill","Frozen Guard","Ice Mines","Stone Keep","Atrium","Distric","Undercity","Stride",""]
        for i in range(13):
            if i == 0:
                Main_Screen2_Grid1.add_widget(Button(text = C1+"Siege Maps", size_hint_y = None, height = 75, text_size = (Window.width-50,75), halign = "left", valign = "middle",markup= True))
            if i == 7:
                Main_Screen2_Grid1.add_widget(Button(text = C1+"Siege Maps - Test Queque", size_hint_y = None, height = 75, text_size = (Window.width-50,75), halign = "left", valign = "middle",markup= True))
            
            Main_Screen2_Grid1.add_widget(Button(text = C4+mapsset[i], size_hint_y = None, height = 50, text_size = (Window.width-50,50), halign = "left", valign = "middle",markup= True))
        mapsset1 = ["Outpost","Hidden Temple","Frostbite Cavern"]
        for i in range(3):
            if i == 0:
                Main_Screen2_Grid1.add_widget(Button(text = C1+"Payload Maps", size_hint_y = None, height = 75, text_size = (Window.width-50,75), halign = "left", valign = "middle",markup= True))
            Main_Screen2_Grid1.add_widget(Button(text = C4+mapsset1[i], size_hint_y = None, height = 50, text_size = (Window.width-50,50), halign = "left", valign = "middle",markup= True))
            
        
        
        Pantalla_Root = GridLayout(cols = 3)
        Pantalla_Root.add_widget(Label(size_hint_x = None, width = 25))
        Pantalla_Root.add_widget(Pantalla)
        Pantalla_Root.add_widget(Label(size_hint_x = None, width = 25))
        Main_Screen.add_widget(Pantalla_Root)
        Pantalla_ScrollView.add_widget(self.Main_ScreenManager)

        self.add_widget(Image(size_hint = (1,1), source = hud+"fondo2.png", allow_stretch =True, keep_ratio = False))
        self.add_widget(Pantalla_ScrollView)
        x = wmedx-((Window.width*0.80)/2)
        
        
        self.Topgrid2 = GridLayout(cols = 1, size_hint = (1,None), spacing =0)
        self.Topgrid2.bind(minimum_height = self.Topgrid2.setter('height'))
        self.Topgrid2_root = ScrollView(size_hint = (1,1))
        self.Topgrid2_root.add_widget(self.Topgrid2)

        imgset2 = []
        Main_Screen1.add_widget(Image(size_hint = (1,1), source = hud+"co6.png", allow_stretch =True, keep_ratio = False))
        Main_Screen1.add_widget(self.Topgrid2_root)
        self.Topgrid1_Dim = GridLayout(cols = 3, size_hint = (1,None), spacing =5, height = 1000)
        self.Topgrid1_Dim2 = GridLayout(cols = 2, size_hint = (1,None), spacing =5, height = 75)
        Button6 = Button(text_size = (wmedx-50,75),halign = "right",valign = "bottom",font_size =24,text = C1+"<",markup = True,background_normal = hud+"co6.png",size_hint_y = None, height = 75)
        Button6.bind(on_release = lambda x :self.Main_ScreenManager_ChangeCurrent("a"))
        self.Topgrid1_Dim2.add_widget(Button(text_size = (wmedx-50,75),valign = "bottom",font_size =24,text = C1+"Champions",markup = True,background_normal = hud+"co6.png",size_hint_y = None, height = 75))
        self.Topgrid1_Dim2.add_widget(Button6)
        self.Topgrid2.add_widget(self.Topgrid1_Dim2)
        self.Topgrid2.add_widget(Image(size_hint_y = None, height = 5 , source = hud+"co6.png",keep_ratio= False, allow_stretch = True))
        self.Topgrid2.add_widget(Image(size_hint_y = None, height = 3 , source = hud+"blindbar3.png",keep_ratio= False, allow_stretch = True))
        self.Topgrid2.add_widget(Image(size_hint_y = None, height = 50 , source = hud+"co6.png",keep_ratio= False, allow_stretch = True))
        
        self.Topgrid2.add_widget(self.Topgrid1_Dim)
        self.Topgrid2.add_widget(Image(size_hint_y = None, height = 3 , source = hud+"blindbar3.png",keep_ratio= False, allow_stretch = True))  
        

        #if i == 2:
        #    Button5 = Button(text = C1+"X",font_size= 40, markup = True ,size_hint_y = None,allow_stretch = True, keep_ratio = False, size = (128,128),background_normal = hud+"co6.png")
        #    self.Topgrid1_Dim.add_widget(Button5)
        #    Button5.bind(on_release = lambda x: self.Main_ScreenManager_ChangeCurrent("a"))
        for i in range(20):

            imgset2.append("a ("+str(i+1)+")")
            
            Button5 = Button(size_hint_y = None, size = (128,128),background_normal = icon+imgset2[i]+".png",background_down = icon+imgset2[i]+".png")
            contenedor1 = GridLayout(cols = 1,size_hint = (1,None), size = (128,128))
            a = Scatter(size_hint = (1,None), size = (128,128))
            a.add_widget(Button5) 
            a.add_widget(Image(size_hint_y = None,allow_stretch = True, keep_ratio = False, size = (128,128),source = icon+"marco.png")) 
            a.add_widget(Button(pos = (2,2),border = [0,0,0,0],size_hint = (None,None), size = (124,25), background_normal = hud+ "co4.png",markup =True, text = "[b]Character", font_size = 20)) 
            
            contenedor1.add_widget(a)
            self.Topgrid1_Dim.add_widget(contenedor1) 
            Button5.bind(on_press = lambda x: self.Animatesize(x.parent))

    
        
        self.Topgrid1 = GridLayout(cols = 1, size_hint = (1,1), width = Window.width, spacing =0)
        self.Topgrid1.bind(minimum_height = self.Topgrid1.setter('height'))
        self.Topgrid1_root = ScrollView(size_hint = (None,None), pos = (x,Window.height+(Window.height*0.80)), size = ((Window.width*0.80), Window.height*0.80))
        self.Topgrid1_root.add_widget(self.Topgrid1)
        self.add_widget(self.Topgrid1_root)
        u = self.Topgrid1_root.height
        u3 = self.Topgrid1_root.height/2
        u1 = self.Topgrid1_root.width/2
        u2 = self.Topgrid1_root.width
        
        self.Topgrid_ScreenManager = ScreenManager()
        self.Topgrid_ScreenManager_screen1 = Screen(name = "a")
        self.Topgrid_ScreenManager_screen2 = Screen(name = "b")
        self.Topgrid_ScreenManager_screen3 = Screen(name = "c")
        imgset1 = ["Gamemode1","Gamemode2","Gamemode3"]
        widgetset1 = [self.Topgrid_ScreenManager_screen1,self.Topgrid_ScreenManager_screen2,self.Topgrid_ScreenManager_screen3]
        self.Topgrid_ScreenManager.add_widget(self.Topgrid_ScreenManager_screen1)
        self.Topgrid_ScreenManager.add_widget(self.Topgrid_ScreenManager_screen2)
        self.Topgrid_ScreenManager.add_widget(self.Topgrid_ScreenManager_screen3)
            
        self.Topgrid1.add_widget(self.Topgrid_ScreenManager)
        for i in range(3):
            contenedor = GridLayout(cols = 1, pos = (u1-150,(u-474)-100), size_hint = (1,None), heigh = 500)
            widgetset1[i].add_widget(Image(size_hint = (None,None), size = (300,474), source = hud+imgset1[i]+".png", pos = (u1-150,u-474)))
            Button1 = Button(size_hint = (None,None), size = (50,50), pos = (u2-50,u3-25))
            Button2 = Button(size_hint = (None,None), size = (300,50),font_size = 20,background_normal = hud + "co3.png", text = imgset1[i], text_size = (250,25), pos = (u1-150,u-474))
            widgetset1[i].add_widget(Button1)
            widgetset1[i].add_widget(Button2)
            widgetset1[i].add_widget(contenedor)
            Button4 = Button(pos = (u2-60,u-60),markup = True ,background_normal = hud + "None.png",halign = "left",valign = "bottom",font_size = 28,text_size = (60,60),background_down = hud + "None.png",text = C1+"X", size_hint = (None,None), size = (60,60), allow_stretch = False, keep_ratio = True)
            Button4.bind(on_release =lambda x: self.Animatesize3b(x))
            widgetset1[i].add_widget(Button4)
            contenedor.add_widget(Button(size_hint = (None,None), size = (300,50),font_size = 20,background_normal = hud + "co2.png", text = "aaaasd", text_size = (u2-50,25), pos = (u1-150,u-474)))
            contenedor.add_widget(Button(size_hint = (None,None), size = (300,50),font_size = 20,background_normal = hud + "co2.png", text = "aaaasd", text_size = (u2-50,25), pos = (u1-150,u-474)))
            contenedor.add_widget(Button(size_hint = (None,None), size = (300,50),font_size = 20,background_normal = hud + "co2.png", text = "aaaasd", text_size = (u2-50,25), pos = (u1-150,u-474)))

            Button1.bind(on_release = lambda x :self.NextGameMode(1))
            
        

         

        
        
        
        self.Topgrid = GridLayout(cols = 1, size_hint = (1,None))
        self.Topgrid.bind(minimum_height = self.Topgrid.setter('height'))
        self.Topgrid_root = ScrollView(size_hint = (None,None), pos = (x,Window.height+(Window.height*0.80)), size = ((Window.width*0.80), Window.height*0.80))
        self.Topgrid_root.add_widget(self.Topgrid)

        Topgrid_dim1 = GridLayout(rows = 1, height = 120, size_hint_y = None)
        Topgrid_dim1_dim1 = GridLayout(cols = 1, size_hint = (1,None), heigh = 120)
        Button3 = Button(markup = True ,background_normal = hud + "co6.png",halign = "right",valign = "bottom",font_size = 24,text_size = ((wmedx+(wmedx/2)-120-50,60)),background_down = hud + "co6.png",text = C1+"X", size_hint = (1,1), size = (120,60), allow_stretch = False, keep_ratio = True)
        Button3.bind(on_release =lambda x: self.Animatesize3(x))
        Topgrid_dim1_dim1.add_widget(Button3)
        Topgrid_dim1_dim1.add_widget(Button(background_normal = hud + "co6.png",valign = "bottom",font_size = 24,text_size = ((wmedx+(wmedx/2)-120-50,60)),background_down = hud + "co6.png",text = "Barik", size_hint = (1,1), size = (120,60), allow_stretch = False, keep_ratio = True))
        Topgrid_dim1.add_widget(Image(source = icon + "a (3).png", size_hint = (None,None), size = (120,120), allow_stretch = False, keep_ratio = True))
        Topgrid_dim1.add_widget(Topgrid_dim1_dim1)
        
        self.Topgrid.add_widget(Topgrid_dim1)
        Topgrid_dim2 = GridLayout(rows = 1, height = 64, size_hint_y = None)
        img = Image(size_hint = (None,None), size  = (48,64) , source = icon + "candles.png" , allow_stretch = False, keep_ratio = True)
        img_rel = RelativeLayout(size_hint = (None,None), size  = (48,64) , source = icon + "candles.png" , allow_stretch = False, keep_ratio = True)
        img_rel.add_widget(Image(size_hint = (None,None), size  = (48,64) , source = hud + "co6.png" , allow_stretch = True, keep_ratio = False))
        img_rel.add_widget(img)
        Topgrid_dim2.add_widget(img_rel)
        Topgrid_dim2.add_widget(Button(background_normal = hud + "co6.png",font_size = 20,valign = "bottom",text_size = ((Window.width*0.80)-64,50),background_down = hud + "co6.png",markup = True,text = C1+"Story", size_hint = (1,None), size = (120,60), allow_stretch = False, keep_ratio = True))
        self.Topgrid.add_widget(Topgrid_dim2)
        self.Topgrid.add_widget(Image(size_hint = (1,None), size  = (250,2.5) , source = hud + "blindbar1.png" , allow_stretch = True, keep_ratio = False))
        self.Topgrid.add_widget(Button(background_normal = hud + "co6.png",font_size = 16,valign = "top",text_size = ((Window.width*0.80)-50,200-50),background_down = hud + "co6.png",text = "Siempre ha sido un desgraciado de mierda, pero siempre sabe como hacer que 2 torres de cerveza calmen una vida deprimente. :V", size_hint = (1,None), size = (120,200), allow_stretch = False, keep_ratio = True))
        self.Topgrid.add_widget(Image(size_hint = (1,None), size  = (250,2.5) , source = hud + "blindbar1.png" , allow_stretch = True, keep_ratio = False))
        self.Topgrid.add_widget(Button(background_normal = hud + "co6.png",font_size = 20,valign = "bottom",text_size = ((Window.width*0.80)-50,60),background_down = hud + "co6.png",markup = True,text = C1+"Front Line", size_hint = (1,None), size = (120,60), allow_stretch = False, keep_ratio = True))
        self.Topgrid.add_widget(Button(background_normal = hud + "co6.png",font_size = 16,valign = "top",text_size = ((Window.width*0.80)-50,60),background_down = hud + "co6.png",text = "Skills", size_hint = (1,None), size = (120,60), allow_stretch = False, keep_ratio = True))
        self.Topgrid.add_widget(Image(size_hint = (1,None), size  = (250,2.5) , source = hud + "blindbar3.png" , allow_stretch = True, keep_ratio = False))
        skillsset = ["Left Click - Blunderburss","Right Click - Barricade - 15 S","Q - Turret - 10 S","F - Rocket Boots - 14 S","E - Dome Shield"]
        
        skillsset_desc = ["A short range blunderbuss shooting 13 pellets that deal a total of 600 damage each, every 1s. Bonus Damage: Hitting a marked target, consumes all marks dealing 10% more damage per mark. Enemies can be marked up to 2 times."
        ,"Deploy a barricade that provides cover. Barricade has 5000 health and lasts 4 seconds or until destroyed. "
        ,"Build a turret that fires at enemies for 150 damage every second and lasts until destroyed."
        ,"A guided rocket charge that lasts 1s. "
        ,"Deploy a 20,000 health Dome Shield for 6 seconds with a Flamethrower turret inside that deals 400 damage per second."]
        
        for i in range(5):
            self.Topgrid_dim3 = GridLayout(cols = 2, size_hint_y = None, height = 64, spacing = 0)
            self.Topgrid_dim4 = GridLayout(cols = 1, size_hint_y = None, height = 74)
            Scatter1 = Scatter(size_hint_x = None, width = 64, background_normal = hud + "co6.png")
            Grid1 = GridLayout(cols = 1,size_hint = (None,None), height = 64, width = 64, background_normal = hud + "co6.png")
            Grid1.add_widget(Scatter1)
            Scatter1.add_widget(Image(size_hint = (None,None), size = (64,64), source = icon + "Barrik ("+str(i+1)+").png"))
            self.Topgrid_dim3.add_widget(Grid1)
            self.Topgrid_dim3.add_widget(Button(markup = True,text_size = ((Window.width*0.80)-64-50,64),valign = "middle",text = C1+skillsset[i], background_normal = hud + "co6.png", font_size = 18))
            #self.Topgrid_dim3.add_widget(Image(size_hint = (None,None), size = (64,10), source = hud + "co6.png", keep_ratio = False, allow_stretch = True))
            #self.Topgrid_dim3.add_widget(Image(size_hint = (1,None), size = (64,10), source = hud + "co6.png", keep_ratio = False, allow_stretch = True))
            
            self.Topgrid_dim4.add_widget(Button(markup = True,text_size = ((Window.width*0.80),64),valign = "middle",text = skillsset_desc[i], background_normal = hud + "co6.png", font_size = 16))
            self.Topgrid_dim4.add_widget(Image(size_hint = (1,None), size = (64,10), source = hud + "co6.png", keep_ratio = False, allow_stretch = True))
            
            self.Topgrid.add_widget(self.Topgrid_dim3)
            self.Topgrid.add_widget(self.Topgrid_dim4)
        
        self.add_widget(self.Topgrid_root)
        textset = ["Champions","Cards","Items","Game Modes","Maps"]
        for i in range(1):
            if i == 0:
            
                Pantalla_Dim2  = GridLayout(rows = 1, size_hint_y = None, height = 200)
                Pantalla_Dim2.add_widget(Image(size_hint = (1,None), size  = (250,250) , source = hud + "fondo1.png" , allow_stretch = True, keep_ratio = True))                
                Pantalla.add_widget(Image(size_hint = (1,None), size  = (250,50) , source = hud + "None.png" , allow_stretch = True, keep_ratio = False))
                Pantalla.add_widget(Image(size_hint = (1,None), size  = (250,2.5) , source = hud + "None.png" , allow_stretch = True, keep_ratio = False))
                Pantalla.add_widget(Pantalla_Dim2)
                Pantalla.add_widget(Image(size_hint = (1,None), size  = (250,5) , source = hud + "None.png" , allow_stretch = True, keep_ratio = False))
                Pantalla.add_widget(Image(size_hint = (1,None), size  = (250,50) , source = hud + "None.png" , allow_stretch = True, keep_ratio = False))
                Pantalla.add_widget(Image(size_hint = (1,None), size  = (250,2.5) , source = hud + "blindbar2.png" , allow_stretch = True, keep_ratio = False))
            Pantalla_Dim = GridLayout(cols = 2, size_hint = (1,None), height = 75*5, spacing = 25)
            Pantalla_DimHS = ScrollView(size_hint = (1,1), height = 140, bar_width = 0)
            
            Pantalla_DimHS_Layout = GridLayout(rows = 1 , size_hint_y = None , height = 128, size_hint_x  = None, spacing = 20)
            Pantalla_DimHS_Layout.bind(minimum_width=Pantalla_DimHS_Layout.setter('width'))
            
            Pantalla_DimHS.add_widget(Pantalla_DimHS_Layout)
            imgset = []
            
            for i in range(11):
                imgset.append("a ("+str(i+1)+")")
                a = RelativeLayout(size_hint = (None,None),heigh =128 , width = 128, background_normal = icon+ imgset[i]+".png",background_down = icon+ imgset[i]+".png",)
                a.add_widget(Button(size_hint = (None,1) , width = 128, background_normal = icon+ imgset[i]+".png",background_down = icon+ imgset[i]+".png",))
                a_button = ImageButton(size_hint = (None,None), size = (128,128), source = hud+"ico1.png")
                a_button.bind(on_press =  lambda x :self.Animatesize(x.parent.parent))
                a.add_widget(a_button)
                b = Scatter(size_hint = (None,None), size = (128,128))
                c = GridLayout(size_hint = (None,None), size = (128,128), cols = 1)
                c.add_widget(b)
                b.add_widget(a)
                Pantalla_DimHS_Layout.add_widget(c)
            
            Pantalla.add_widget(Pantalla_DimHS)
            Pantalla.add_widget(Pantalla_Dim)
            for i in range(5):
                Pantalla_Dim_Container = GridLayout(cols = 2, size_hint_y = None , height = 75)
                #Pantalla_Dim_Container.add_widget(Image(size_hint = (None,None),height = 5, size  = (64,1) , source = hud + "blindbar2.png" , allow_stretch = True, keep_ratio = False))
                #Pantalla_Dim_Container.add_widget(Image(size_hint = (1,None),height = 5, size  = (250,2.5) , source = hud + "blindbar2.png" , allow_stretch = True, keep_ratio = False))
                
                Pantalla_Dim_Container.add_widget(Image(size_hint = (None,1), width  = 64 , source = hud + "hud19.png" , allow_stretch = True, keep_ratio = False))
                a = Button(font_name = fonts+"BEBAS",size_hint_y = None, height = 75,valign = "middle",halign = "left",font_size = 18   ,background_normal = hud + "co2b.png",border = [0,0,0,0],background_down = hud + "co2b.png",markup = True, text =textset[i], text_size = (wmedx-64-12.5,75))
                b = Scatter(size_hint = (None,None),height = 75 , width  = 64 , source = hud + "hud19.png" , allow_stretch = True, keep_ratio = False)
                c = GridLayout(cols = 1 ,size_hint = (1,None), height = 75, width  = 64 , source = hud + "hud19.png" , allow_stretch = True, keep_ratio = False)
                b.add_widget(a)
                c.add_widget(b)
                a.bind(on_press = lambda x: self.Animatesize1(x.parent))
                Pantalla_Dim_Container.add_widget(c)
                Pantalla_Dim_Container.add_widget(Image(size_hint = (None,None),height = 5, size  = (64,1) , source = hud + "blindbar1.png" , allow_stretch = True, keep_ratio = False))
                Pantalla_Dim_Container.add_widget(Image(size_hint = (1,None),height = 5, size  = (250,2.5) , source = hud + "blindbar1.png" , allow_stretch = True, keep_ratio = False))
                Pantalla_Dim.add_widget(Pantalla_Dim_Container)
                
        
    def Animatesize(self,button):
        print button.parent.pos    
        anim3 = Animation(x = button.parent.pos[0], d = .75, t = "in_out_back")
        #anim3.start(self.medio)
        button.scale = 1.0
        anim1 = Animation(scale = 1.5, d = .10,t = "in_circ")
        anim2 = Animation(scale = 1.0, d = .20,t = "out_circ")
        anim = anim1 + anim2
        anim.start(button)
        self.Animatesize2(self.Topgrid_root)
        
    def Animatesize1(self,button):


        button.scale = 1.0
        anim1 = Animation(scale = 0.5, d = .10,t = "in_circ")
        anim2 = Animation(scale = 1.0, d = .20,t = "out_circ")
        anim = anim1 + anim2
        anim.start(button)
        
        if button.children[0].text == "Champions":      
            self.Main_ScreenManager_ChangeCurrent("b")
        if button.children[0].text == "Maps":      
            self.Main_ScreenManager_ChangeCurrent("c")
            
        if button.children[0].text == "Game Modes":      
            self.Animatesize2(self.Topgrid1_root)
        
    def Animatesize2(self,button):
        wmedy = Window.height/2
        wmedx = Window.width/2
        anim3 = Animation(x = button.pos[0], d = .75, t = "in_out_back")
        #anim3.start(self.medio)
        button.scale = 1.0
        anim1 = Animation(pos = (button.pos[0],wmedy-(Window.height*0.40)), d = 1,t = "out_circ")
        #anim2 = Animation(size = (wmedx+(wmedx/2), 500), d = .75,t = "out_circ")
        anim = anim1 
        anim.start(button)
        
    def NextGameMode(self,button):
        self.Topgrid_ScreenManager.current = self.Topgrid_ScreenManager.next()
        
    def Animatesize3(self,button):
        wmedy = Window.height/2
        wmedx = Window.width/2
        anim3 = Animation(x = self.Topgrid_root.pos[0], d = .75, t = "in_out_back")
        #anim3.start(self.medio)
        self.Topgrid_root.scale = 1.0
        anim1 = Animation(pos = (self.Topgrid_root.pos[0],Window.height), d = .5,t = "out_circ")
        #anim2 = Animation(size = (wmedx+(wmedx/2), 500), d = .75,t = "out_circ")
        anim = anim1 
        anim.start(self.Topgrid_root)
    def Animatesize3b(self,button):
        wmedy = Window.height/2
        wmedx = Window.width/2
        anim3 = Animation(x = self.Topgrid1_root.pos[0], d = .75, t = "in_out_back")
        #anim3.start(self.medio)
        self.Topgrid_root.scale = 1.0
        anim1 = Animation(pos = (self.Topgrid1_root.pos[0],Window.height), d = .5,t = "out_circ")
        #anim2 = Animation(size = (wmedx+(wmedx/2), 500), d = .75,t = "out_circ")
        anim = anim1 
        anim.start(self.Topgrid1_root)
    def Animatesize3c(self,button):
        wmedy = Window.height/2
        wmedx = Window.width/2
        anim3 = Animation(x = self.Topgrid2_root.pos[0], d = .75, t = "in_out_back")
        #anim3.start(self.medio)
        self.Topgrid2_root.scale = 1.0
        anim1 = Animation(pos = (self.Topgrid2_root.pos[0],Window.height), d = .5,t = "out_circ")
        #anim2 = Animation(size = (wmedx+(wmedx/2), 500), d = .75,t = "out_circ")
        anim = anim1 
        anim.start(self.Topgrid2_root)
    def Main_ScreenManager_ChangeCurrent(self,text):
        self.Main_ScreenManager.current = text
    def start(self, minTime, minDistance):
        gps.start()

    def stop(self):
        gps.stop()

    @mainthread
    def on_location(self, **kwargs):
        self.gps_location = '\n'.join([
            '{}={}'.format(k, v) for k, v in kwargs.items()])
        a = '\n'.join([
            '{}={}'.format(k, v) for k, v in kwargs.items()])
        for k, v in kwargs.items():
            if (k == "lon") or (k == "lat"):
                print str(k)+"="+str(v)

    @mainthread
    def on_status(self, stype, status):
        self.gps_status = 'type={}\n{}'.format(stype, status)
        
    @mainthread
    def on_pause(self):
        gps.stop()
        return True

    def on_resume(self):
        gps.start(1000, 0)
        pass
        
class MyApp(App):
    def build(self):
        return InterfaceManager()
 

if __name__ in ('__main__', '__android__'):
    MyApp().run()

    
    
    
    
    