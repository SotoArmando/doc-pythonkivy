#!/usr/bin/env python55555533yyyyyyyyyyyyyyyyyyyyy555555
# -*- coding: utf-8 -*-
from kivy.config import Config
from kivy.core.window import Window
import kivy
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

class InterfaceManager(AnchorLayout):
    def __init__(self, **kwargs):
        navigationdrawer = NavigationDrawer()
        super(InterfaceManager, self).__init__(**kwargs)
        self.patch = os.path.dirname(os.path.abspath(__file__))
        self.images = self.patch + '/pics/'
        self.sources = self.patch + '/source/'
        self.statsimg = self.patch + '/pics/stats/'
        self.clasesimg = self.patch + '/pics/clases/'
        self.hudimg = self.patch + '/pics/hud/'
        self.escudosimg = self.patch + '/pics/Equipamento/Escudos/'

        Window.clearcolor = (1,1,1,0)
        #------------------------------------------------------------------------------------------------
        
        self.panelesformularios = []
   
            
        self.resources =  os.listdir(self.sources) 
        self.recursos = []
        self.busqueda = []
       
        for i in self.resources:
            try:
                self.recursos.append(i)
                self.busqueda.append(i[:1])

            except:
                print i
                pass
                
        
        
        #print list(set(self.busqueda))
        self.busqueda = list(set(self.busqueda  ))
        print self.busqueda 
        #print self.recursos
        #PANEL PRINCIPAL
        
        
        
        self.ROOT_Navitagiondrawer1 = NavigationDrawer()

        self.ROOT_Boxlayout1 = GridLayout(cols = 1,spacing = 0)
        self.add_widget(self.ROOT_Navitagiondrawer1)     
        self.ROOT_Navitagiondrawer1.opening_transition = 'out_cubic'
        self.ROOT_Navitagiondrawer1.closing_transition = 'out_cubic'
        
        #MENU LATERAL
        
        self.ROOT_Button1 = Button(markup = True,font_name = "BebasNeue Regular",text = "[color=#404040]BIBLIOTECA", background_normal = self.images +"Button1B.png",background_down = self.images + "Button1B.png", border = (10,10,10,10),font_size = 30)
        self.ROOT_Button1.bind(on_press = self.FORM3) 
        self.ROOT_Button2 = Button(markup = True,text = "[color=#404040]PJ",font_name = "BebasNeue Regular", background_normal = self.images +"Button1B.png",background_down = self.images + "Button1B.png", border = (10,10,10,10),font_size = 30)    
        self.ROOT_Button2.bind(on_press = self.FORM2) 
        
        self.ROOT_Button3 = Button(markup = True,text = "[color=#404040]BESTIARIO", background_normal = self.images +"Button1B.png",background_down = self.images + "Button1B.png", border = (10,10,10,10))
        self.ROOT_Button4 = Button(markup = True,text = "[color=#404040]X", background_normal = self.images +"Button1B.png",background_down = self.images + "Button1B.png", border = (10,10,10,10))
        
        
        self.ROOT_IMG0 = AsyncImage(source = self.images + "23178.png", size_hint = (None, None) , height = 100, width = 100)
        self.ROOT_IMG1 = ImageButton(source = self.images + "V2B.png", width =70,size_hint = (None,None), height = 70)
        self.ROOT_IMG2 = ImageButton(source = self.images + "V2B.png", width =70,size_hint = (None,None), height = 70)
        self.ROOT_IMG3 = ImageButton(source = self.images + "V2B.png", width =70,size_hint = (None,None), height = 70)
        self.ROOT_IMG4 = ImageButton(source = self.images + "V2B.png", width =70,size_hint = (None,None), height = 70)
        self.ROOT_IMG5 = ImageButton(source = self.images + "V2B.png", width =70,size_hint = (None,None), height = 70)
        self.ROOT_IMG6 = ImageButton(source = self.images + "V2B.png", width =70,size_hint = (None,None), height = 70)
        self.ROOT_IMG7 = ImageButton(source = self.images + "V2B.png", width =70,size_hint = (None,None), height = 70)
        self.ROOT_IMG8 = ImageButton(source = self.images + "V2B.png", width =70,size_hint = (None,None), height = 70)
        self.ROOT_IMG9 = ImageButton(source = self.images + "V2B.png", width =70,size_hint = (None,None), height = 70)
        self.ROOT_IMG10 = ImageButton(source = self.images + "V2B.png", width =70,size_hint = (None,None), height = 70)
        self.ROOT_IMG11 = ImageButton(source = self.images + "V2B.png", width =70,size_hint = (None,None), height = 70)
        self.ROOT_IMG12 = ImageButton(source = self.images + "V2B.png", width =70,size_hint = (None,None), height = 70)
        self.partes_set = GridLayout(cols = 6, size_hint = (1, None) , height = 300, spacing = 0)
        





     
        self.partes_set.add_widget(Label())
        self.partes_set.add_widget(self.ROOT_IMG1)
        self.partes_set.add_widget(Label(size_hint_x = None , width = 70))
        self.partes_set.add_widget(self.ROOT_IMG2)
        self.partes_set.add_widget(self.ROOT_IMG3)
        self.partes_set.add_widget(Label())
        
        self.partes_set.add_widget(Label())
        self.partes_set.add_widget(self.ROOT_IMG4)
        self.partes_set.add_widget(Label(size_hint_x = None , width = 70))
        self.partes_set.add_widget(self.ROOT_IMG5)
        self.partes_set.add_widget(self.ROOT_IMG6)
        self.partes_set.add_widget(Label())
        
        self.partes_set.add_widget(Label())
        self.partes_set.add_widget(self.ROOT_IMG7)
        self.partes_set.add_widget(Label(size_hint_x = None , width = 70))
        self.partes_set.add_widget(self.ROOT_IMG8)
        self.partes_set.add_widget(self.ROOT_IMG9)
        self.partes_set.add_widget(Label())
        
        
        self.partes_set.add_widget(Label())
        self.partes_set.add_widget(self.ROOT_IMG10)
        self.partes_set.add_widget(Label(size_hint_x = None , width = 70))
        self.partes_set.add_widget(self.ROOT_IMG11)
        self.partes_set.add_widget(self.ROOT_IMG12)
        self.partes_set.add_widget(Label())
        
        self.stats =GridLayout(cols = 8, size_hint_y = None, height = 300)
        
        self.stats1 = Label(markup = True , text ="[b]VIT", size_hint_y = None, height = 30)
        self.stats2 = Label(markup = True , text ="[b]PA", size_hint_y = None, height = 30)
        self.stats3 = Label(markup = True , text ="[b]PM", size_hint_y = None, height = 30)
        self.stats4 = Label(markup = True , text ="[b]ALC", size_hint_y = None, height = 30)
        self.stats5 = Label(markup = True , text ="[b]PP", size_hint_y = None, height = 30)
        self.stats6 = Label(markup = True , text ="[b]INI", size_hint_y = None, height = 30)
        self.stats7 = Label(markup = True , text ="[b]CRIT", size_hint_y = None, height = 30)
        self.stats8 = Label(markup = True , text ="[b]INV", size_hint_y = None, height = 30)
        
        self.stats.add_widget(Label())
        self.stats.add_widget(Image(source = self.statsimg +"tx_res_water.png",size_hint_x = None , width = 30))
        self.stats.add_widget(self.stats1)
        self.stats.add_widget(Label(text = "0"))
        self.stats.add_widget(Image(source = self.statsimg +"tx_res_water.png",size_hint_x = None , width = 30))
        self.stats.add_widget(self.stats2)
        self.stats.add_widget(Label(text = "0"))
        self.stats.add_widget(Label())
        self.stats.add_widget(Label())
        self.stats.add_widget(Image(source = self.statsimg +"tx_res_water.png",size_hint_x = None , width = 30))
        self.stats.add_widget(self.stats3)
        self.stats.add_widget(Label(text = "0"))
        self.stats.add_widget(Image(source = self.statsimg +"tx_res_water.png",size_hint_x = None , width = 30))
        self.stats.add_widget(self.stats4)
        self.stats.add_widget(Label(text = "0"))
        self.stats.add_widget(Label())
        self.stats.add_widget(Label())
        self.stats.add_widget(Image(source = self.statsimg +"tx_res_water.png",size_hint_x = None , width = 30))
        self.stats.add_widget(self.stats5)
        self.stats.add_widget(Label(text = "0"))
        self.stats.add_widget(Image(source = self.statsimg +"tx_res_water.png",size_hint_x = None , width = 30))
        self.stats.add_widget(self.stats6)
        self.stats.add_widget(Label(text = "0"))
        self.stats.add_widget(Label())
        self.stats.add_widget(Label())
        self.stats.add_widget(Image(source = self.statsimg +"tx_res_water.png",size_hint_x = None , width = 30))
        self.stats.add_widget(self.stats7)
        self.stats.add_widget(Label(text = "0"))
        self.stats.add_widget(Image(source = self.statsimg +"tx_res_water.png",size_hint_x = None , width = 30))
        self.stats.add_widget(self.stats8)
        self.stats.add_widget(Label(text = "0"))
        self.stats.add_widget(Label())
        

        

        #with self.partes_set.canvas:
        #    Rectangle(source= self.images+ "V1.png",pos = self.partes_set.pos, size = self.partes_set.size)
            
        #self.ROOT_Boxlayout1.add_widget(self.ROOT_IMG0)
        self.ROOT_IMG0_grid = GridLayout(cols = 3,spacing = 0,size_hint = (1,None), height =100)
        self.ROOT_Boxlayout1.add_widget(self.ROOT_IMG0_grid)
 
        self.ROOT_IMG0_grid.add_widget(Image(source = self.images + "V1.png", allow_stretch = True, keep_ratio = False, size_hint = (1,None) , height =100))
        self.ROOT_IMG0_grid.add_widget(self.ROOT_IMG0)
        self.ROOT_IMG0_grid.add_widget(Image(source = self.images + "V1.png", allow_stretch = True, keep_ratio = False, size_hint = (1,None) , height =100))
        
        
        
        self.ROOT_Boxlayout1.add_widget(Button(font_size = 20,text = "Equipamento", size_hint = (1,None), height= 50,markup = True, background_normal = self.images + "Sponsor4.png"))
        self.ROOT_Boxlayout1.add_widget(Image(source = self.images +"A3D.png", keep_ratio = False , allow_stretch = True, size_hint = (1,None), height = 10))
        self.ROOT_Boxlayout1.add_widget(Image(source = self.images +"A3D.png", keep_ratio = False , allow_stretch = True, size_hint = (1,None), height = 10))
        #self.ROOT_Boxlayout1.add_widget(self.partes_set)
        self.ROOT_Boxlayout1.add_widget(Image(source = self.images +"A3D.png", keep_ratio = False , allow_stretch = True, size_hint = (1,None), height = 10))
        self.ROOT_Boxlayout1.add_widget(Image(source = self.images +"A3D.png", keep_ratio = False , allow_stretch = True, size_hint = (1,None), height = 10))
        #self.ROOT_Boxlayout1.add_widget(self.stats)
        
        #self.ROOT_Boxlayout1.add_widget(self.ROOT_Button1)
        #self.ROOT_Boxlayout1.add_widget(self.ROOT_Button2)
        #self.ROOT_Boxlayout1.add_widget(self.ROOT_Button3)
        #self.ROOT_Boxlayout1.add_widget(self.ROOT_Button4)

        
   

        
        
        
        
   
        
        
        #------------------------------------------------------------------------------------------------
        
        
        

        
        self.Form3 = GridLayout(cols = 1 , size_hint = (1, None) , spacing = 0)
        self.Form3_root = ScrollView(size_hint=(1, 1),size=(Window.width, Window.height))
        self.Form3.bind(minimum_height=self.Form3.setter('height'))
        self.Form3_root.add_widget(self.Form3)

        self.Espacio16C = Image(source=self.images + "lomasduro.png",width = 400, size_hint = (None, None), height = 188, allow_stretch = True, keep_ratio = True)

        self.Espacio16_GridB = GridLayout(cols = 3, size_hint = (1, None), height = 188)

        
        self.Espacio16_GridB.add_widget(self.Espacio16C)
        self.Espacio16_GridB.add_widget(Image(source=self.images + "V3.png",width = 100, size_hint = (1, None), height = 188, allow_stretch = True , keep_ratio = False))
        self.Espacio16_GridB.add_widget(Image(source=self.images + "V3.png",width = 100, size_hint = (1, None), height = 188, allow_stretch = True , keep_ratio = False))
        
        self.Form3_TextIn = TextInput(text = "Busqueda.",foreground_color =(0,0,0,.7),width = 350,border = [10,10,10,10],font_size = 25 ,padding =[20,14,0,0],multiline = False,size_hint = (None,None), height = 55,background_active = self.images + 'TextInput1.png', background_normal = self.images + 'TextInput1.png')
        self.Form3_TextIn.bind(on_text_validate = self.actualizar_busqueda)
        self.Form3_TextIMG = Image(source = self.images + "Entypo_d83d(0)_128.png", size_hint = (None, 1), width = 65, allow_stretch = True, keep_ratio = False)
        self.Espacio18 = Image(source=self.images + "Sponsor5.png", size_hint = (.025, 1), height = 30, allow_stretch = True, keep_ratio = False)
        self.Espacio19 = Image(source=self.images + "Sponsor5.png", size_hint = (.025, 1), height = 30, allow_stretch = True, keep_ratio = False)
        self.Form3_Barra3 = Image(source=self.images + "Sponsor5.png", size_hint = (1, None), height = 50, allow_stretch = True, keep_ratio = False)
        self.Form3_TextIn_Grid = GridLayout(cols = 3, size_hint = (1,None), height =55)
        self.Form3_ABC_Grid = GridLayout(cols = 21,width = 1500, size_hint = (None,None), height =75)
        self.Form3_TextIn_Grid.add_widget(self.Espacio19)
        self.Form3_TextIn_Grid.add_widget(self.Form3_TextIn)
        self.Form3_TextIn_Grid.add_widget(self.Espacio18)
        
        self.Form3_HScroll = ScrollView(size_hint=(1, None), size=self.Form3_ABC_Grid.size)
        self.Form3_HScroll.add_widget(self.Form3_ABC_Grid)
        for i in self.busqueda:
            self.Form3_ABC = Button(text = "[color=#e6e6e6][b]"+i, markup = True, background_normal = self.images + "Button1.png")
            self.Form3_ABC_Grid.add_widget(self.Form3_ABC)
        
        self.Form3.add_widget(Image(source=self.images + "A3.png", size_hint = (1, None), height = 5, allow_stretch = True, keep_ratio = False))
        self.Form3.add_widget(self.Espacio16_GridB  )
        self.Form3.add_widget(Image(source=self.images + "A3B.png", size_hint = (1, None), height = 5, allow_stretch = True, keep_ratio = False))
        self.Form3.add_widget(Image(source=self.images + "Sponsor5.png", size_hint = (.25, None), height = 40, allow_stretch = True, keep_ratio = False))
        self.Form3.add_widget(Label())
        self.Form3.add_widget(self.Form3_TextIn_Grid)
        self.Form3.add_widget(self.Form3_Barra3)
        self.Form3.add_widget(Label())
        self.Form3.add_widget(Image(source=self.images + "A3C.png", size_hint = (1, None), height = 5, allow_stretch = True, keep_ratio = False))
        self.Form3.add_widget(self.Form3_HScroll)
        self.Div4 = GridLayout(cols = 3, spacing = 0, size_hint_y = None, height =100)
        self.Div4.add_widget(Label(size_hint_x = None , width = 50, size_hint_y = None, height = 25))
        self.Div4.add_widget(Label(size_hint_x = None , width = 50, size_hint_y = None, height = 25))
        self.Div4.add_widget(Label(size_hint_x = None , width = 50, size_hint_y = None, height = 25))
        self.Div4.add_widget(Label(size_hint_x = None , width = 50, size_hint_y = None, height = 75))
        self.Div4.add_widget(Image(source = self.hudimg +"icon__0018_Equipements.png", size_hint_x = None, width = 75, size_hint_y = None, height = 75))
        self.Div4.add_widget(Button(font_name= "BebasNeue Regular",valign ='middle',text_size = (450,75),
        halign = "left",size_hint = (1,None), height = 75,text = "[color=#404040]Equipos",markup =True , font_size = 40, background_normal =self.images + "A3.png"))
        self.Form3.add_widget(self.Div4)

    
        
        for i in range(10):
            self.A = GridLayout(cols = 3, size_hint_y = None, height = 120, spacing = 0,border = [0,0,0,0])
            self.A_IMG = Image(source = self.escudosimg + "82014B.png", size_hint_x = None , width = 120)
            self.AA = GridLayout(cols = 3, size_hint_x = 1, spacing = 0,border = [0,0,0,0])
            self.AB = GridLayout(cols = 3, size_hint_x = 1, spacing = 0,border = [0,0,0,0])
            self.AC = GridLayout(cols = 3, size_hint_x = 1, spacing = 0)
           
            self.AA.add_widget(Image(source= self.statsimg +"tx_healthc.png", size_hint_x = None , width = 30,allow_stretch = True, keep_ratio = False ,size_hint_y = 1, height = 30))
            self.AA.add_widget(Button(background_normal = self.images + "Button1.png",valign ='middle',text_size = (90,30),halign = "left",text = "Stat",size_hint_y = 1, height = 30))
            self.AA.add_widget(Button(background_normal = self.images + "Button1.png",valign ='middle',text_size = (90,30),halign = "left",text = "0",size_hint_y = 1, height = 30))
            self.AA.add_widget(Image(source= self.statsimg +"tx_healthc.png", size_hint_x = None , width = 30,size_hint_y = 1, height = 30))
            self.AA.add_widget(Button(background_normal = self.images + "Button1.png",valign ='middle',text_size = (90,30),halign = "left",text = "Stat",size_hint_y = 1, height = 30))
            self.AA.add_widget(Button(background_normal = self.images + "Button1.png",valign ='middle',text_size = (90,30),halign = "left",text = "0",size_hint_y = 1, height = 30))
            self.AA.add_widget(Image(source= self.statsimg +"tx_healthc.png", size_hint_x = None , width = 30,size_hint_y = 1, height = 30))
            self.AA.add_widget(Button(background_normal = self.images + "Button1.png",valign ='middle',text_size = (90,30),halign = "left",text = "Stat",size_hint_y = 1, height = 30))
            self.AA.add_widget(Button(background_normal = self.images + "Button1.png",valign ='middle',text_size = (90,30),halign = "left",text = "0",size_hint_y = 1, height = 30))
            self.AA.add_widget(Image(source= self.statsimg +"tx_healthc.png", size_hint_x = None , width = 30,size_hint_y = 1, height = 30))
            self.AA.add_widget(Button(background_normal = self.images + "Button1.png",valign ='middle',text_size = (90,30),halign = "left",text = "Stat",size_hint_y = 1, height = 30))
            self.AA.add_widget(Button(background_normal = self.images + "Button1.png",valign ='middle',text_size = (90,30),halign = "left",text = "0",size_hint_y = 1, height = 30))
     
            self.AB.add_widget(Image(source= self.statsimg +"tx_healthc.png", size_hint_x = None , width = 30,size_hint_y = 1, height = 30))
            self.AB.add_widget(Button(background_normal = self.images + "Button1.png",valign ='middle',text_size = (90,30),halign = "left",text = "Condición",size_hint_y = 1, height = 30))
            self.AB.add_widget(Button(background_normal = self.images + "Button1.png",valign ='middle',text_size = (90,30),halign = "left",text = "0",size_hint_y = 1, height = 30))
            self.AB.add_widget(Image(source= self.statsimg +"tx_healthc.png", size_hint_x = None , width = 30,size_hint_y = 1, height = 30))
            self.AB.add_widget(Button(background_normal = self.images + "Button1.png",valign ='middle',text_size = (90,30),halign = "left",text = "Condición",size_hint_y = 1, height = 30))
            self.AB.add_widget(Button(background_normal = self.images + "Button1.png",valign ='middle',text_size = (90,30),halign = "left",text = "0",size_hint_y = 1, height = 30))
            self.AB.add_widget(Image(source= self.statsimg +"tx_healthc.png", size_hint_x = None , width = 30,size_hint_y = 1, height = 30))
            self.AB.add_widget(Button(background_normal = self.images + "Button1.png",valign ='middle',text_size = (90,30),halign = "left",text = "Condición",size_hint_y = 1, height = 30))
            self.AB.add_widget(Button(background_normal = self.images + "Button1.png",valign ='middle',text_size = (90,30),halign = "left",text = "0",size_hint_y = 1, height = 30))
            self.AB.add_widget(Image(source= self.statsimg +"tx_healthc.png", size_hint_x = None , width = 30,size_hint_y = 1, height = 30))
            self.AB.add_widget(Button(background_normal = self.images + "Button1.png",valign ='middle',text_size = (90,30),halign = "left",text = "Condición",size_hint_y = 1, height = 30))
            self.AB.add_widget(Button(background_normal = self.images + "Button1.png",valign ='middle',text_size = (90,30),halign = "left",text = "0",size_hint_y = 1, height = 30))

            
        
        
            
            
            self.Form3.add_widget(Button(font_name = "BebasNeue Regular",valign ='bottom',text_size = (550,50),halign = "left",size_hint_y = None ,font_size = 28, height = 75 ,markup = True,text = "[color=#404040]ESCUDO DE CAPITÁN AMAKNA", size_hint_x = 1, background_normal = self.images + "A3C.png"))

            self.Div3 = GridLayout(cols = 3, size_hint_y = None, height = 75, spacing = 0)
            self.Form3.add_widget(self.Div3)
            self.Div3.add_widget(Button(size_hint_y = None , height = 50,font_name = "BebasNeue Regular",background_normal = self.images + "A3B.png",valign ='bottom',text_size = (100,50),halign = "left",text = "[color=#404040]lv[color=#ff3333] 199",size_hint_x = None, width = 120,markup= True, font_size = 22))
            self.Div3.add_widget(Button(size_hint_x = 1,size_hint_y = None , height = 50,font_name = "BebasNeue Regular",background_normal = self.images + "A3B.png",valign ='bottom',text_size = (220,50),halign = "left",text = "[color=#262626][b]EFECTOS",markup= True, font_size = 25))
            self.Div3.add_widget(Button(size_hint_x = 1,size_hint_y = None , height = 50,font_name = "BebasNeue Regular",background_normal = self.images + "A3B.png",valign ='bottom',text_size = (220,50),halign = "left",text = "[color=#262626][b]CONDICIONES",markup = True,font_size = 25))
            
            self.Div3.add_widget(Image(size_hint_x = None, width = 120,source =self.images + "A3C.png" , allow_stretch = True , keep_ratio = False))
            self.Div3.add_widget(Image(source =self.images + "A3C.png" , allow_stretch = True , keep_ratio = False))
            self.Div3.add_widget(Image(source =self.images + "A3C.png" , allow_stretch = True , keep_ratio = False))
            self.Div3.add_widget(Image(size_hint_x = None, width = 120,source =self.images + "Button1.png" , allow_stretch = True , keep_ratio = False,size_hint_y = None ,height = 25))
            self.Div3.add_widget(Image(source =self.images + "Button1.png" , allow_stretch = True , keep_ratio = False,size_hint_y = None ,height = 25))
            self.Div3.add_widget(Image(source =self.images + "Button1.png" , allow_stretch = True , keep_ratio = False,size_hint_y = None ,height = 25))
            
            
            self.A.add_widget(self.A_IMG)   
            self.A.add_widget(self.AA)
            self.A.add_widget(self.AB)
            
            self.Div4 = GridLayout(cols = 3, size_hint_y = None, height = 30, spacing = 0)
            self.Div4.add_widget(Image(source = self.images + "Button1.png" , allow_stretch = True , keep_ratio = False ,size_hint_y = None ,height = 25))
            self.Div4.add_widget(Image(source = self.images + "Button1.png" , allow_stretch = True , keep_ratio = False ,size_hint_y = None ,height = 25))
            self.Div4.add_widget(Image(source = self.images + "Button1.png" , allow_stretch = True , keep_ratio = False ,size_hint_y = None ,height = 25))
            self.Div4.add_widget(Image(source = self.images + "ijdcrtvh.png" , allow_stretch = True , keep_ratio = False ,size_hint_y = None ,height = 5))
            self.Div4.add_widget(Image(source = self.images + "ijdcrtvh.png" , allow_stretch = True , keep_ratio = False ,size_hint_y = None ,height = 5))
            self.Div4.add_widget(Image(source = self.images + "ijdcrtvh.png" , allow_stretch = True , keep_ratio = False ,size_hint_y = None ,height = 5))


            self.Form3.add_widget(self.A)
            self.Form3.add_widget(self.Div4)
        
        
        #------------------------------------------------------------------------------------------------
        
        
        

        
        self.Form2 = GridLayout(cols = 2 , size_hint = (1, None) , spacing = 0)
        self.Form2_root = ScrollView(size_hint=(1, 1),size=(Window.width, Window.height))
        self.Form2.bind(minimum_height=self.Form2.setter('height'))
        self.Form2_root.add_widget(self.Form2)
        
        
        #self.Form2.add_widget(Button(size_hint = (1,None), height = 100,text = "[color=#404040]Personaje",markup =True , font_size = 30, background_normal =self.images +"A3.png"))
        #self.Form2.add_widget(Image(source=self.images + "A3.png", size_hint = (.25, None), height = 25, allow_stretch = True, keep_ratio = False))
        #self.Form2.add_widget(Image(source=self.images + "Sponsor5.png", size_hint = (.25, None), height = 5, allow_stretch = True, keep_ratio = False))
        #self.Form2.add_widget(Image(source=self.images + "A3.png", size_hint = (.25, None), height = 5, allow_stretch = True, keep_ratio = False))
        #self.Form2.add_widget(Image(source=self.images + "A3C.png", size_hint = (.25, None), height = 5, allow_stretch = True, keep_ratio = False))
        #self.Form2.add_widget(Image(source=self.images + "A3.png", size_hint = (.25, None), height = 25, allow_stretch = True, keep_ratio = False))
    
        
        Puntos = ["Clase","Caracteristicas Básicas","Caracteristicas Principales","Daños","Resistencias PVM","Resistencias PVP","Caracteristicas Avanzadas"]

        
        for i in Puntos:

            
            if i == Puntos[1]:
                self.Punto = GridLayout(cols = 1, size_hint_y = None , height = 600)
                self.Punto.add_widget(Label())
                self.Punto.add_widget(Image(size_hint_y = None, height = 30,source = self.images +"A3.png", allow_stretch = True, keep_ratio = False))
                self.Punto.add_widget(Button(font_size = 30,markup = True, text="[color=#404040]Clase",size_hint_y = None , height = 50, background_normal = self.images + "A3.png"))
                self.Punto.add_widget(Image(size_hint_y = None, height = 30,source = self.images +"A3.png", allow_stretch = True, keep_ratio = False))
                self.Punto.add_widget(Image(source = self.clasesimg + "symbol_12.png", size_hint = (1,None) , height = 275))
                self.Punto.add_widget(Image(size_hint_y = None, height = 30,source = self.images +"A3.png", allow_stretch = True, keep_ratio = False))
                self.Punto.add_widget(Button(size_hint_y = None, height = 50,font_size = 18,text="[color=#404040][b]Pandawa", background_normal = self.images +"A3.png",markup = True))
                self.Punto.add_widget(Image(size_hint_y = None, height = 30,source = self.images +"A3.png", allow_stretch = True, keep_ratio = False))
                self.Punto.add_widget(Label())
                #self.Punto.add_widget(Image(size_hint_y = None, height = 30,source = self.images +"A3C.png", allow_stretch = True, keep_ratio = False))
                self.Form2.add_widget(self.Punto)
                
                
            if i == Puntos[0]:
                self.Punto1 = GridLayout(cols = 1, size_hint_y = None , height = 650)
                self.contenedor1 = GridLayout(cols = 6,size_hint_y = None, height = 350)
                self.Punto1.add_widget(Label())
                self.Punto1.add_widget(Image(size_hint_y = None, height = 30,source = self.images +"A3.png", allow_stretch = True, keep_ratio = False))
                self.Punto1.add_widget(Button(font_size = 30,markup = True, text="[color=#404040]Stats Básicos",size_hint_y = None , height = 50, background_normal = self.images + "A3.png"))
                self.Punto1.add_widget(Image(size_hint_y = None, height = 30,source = self.images +"A3.png", allow_stretch = True, keep_ratio = False))
                self.Punto1.add_widget(Image(size_hint_y = None, height = 100,source = self.hudimg +"icon__0003_Conjoint.png", allow_stretch = False, keep_ratio = True))
                self.Punto1.add_widget(Image(size_hint_y = None, height = 30,source = self.images +"A3.png", allow_stretch = True, keep_ratio = False))
                self.Punto1.add_widget(self.contenedor1)
                self.Punto1.add_widget(Label())
                #self.Punto1.add_widget(Image(size_hint_y = None, height = 30,source = self.images +"A3C.png", allow_stretch = True, keep_ratio = False))
                self.Form2.add_widget(self.Punto1)
                
                self.contenedor1.add_widget(Label())
                self.contenedor1.add_widget(Image(source = self.statsimg +"tx_health.png",size_hint_x = None , width = 50))
                self.contenedor1.add_widget(Button(valign ='middle',text_size = (150,30),halign = "left",size_hint_x = None, width = 150,markup = True,text="[color=#404040][b]Puntos de Vida", background_normal = self.images + "A3.png"))
                self.contenedor1.add_widget(Label())
                self.contenedor1.add_widget(Button(size_hint_x = None, width = 50,markup = True,text="[color=#404040]0", background_normal = self.images + "A3.png"))
                self.contenedor1.add_widget(Label())
                
                self.contenedor1.add_widget(Label())
                self.contenedor1.add_widget(Image(source = self.statsimg +"icon_pa.png",size_hint_x = None , width = 50))
                self.contenedor1.add_widget(Button(valign ='middle',text_size = (150,30),halign = "left",size_hint_x = None, width = 150,markup = True,text="[color=#404040][b]PA", background_normal = self.images + "A3.png"))
                self.contenedor1.add_widget(Label())
                self.contenedor1.add_widget(Button(size_hint_x = None, width = 50,markup = True,text="[color=#404040]0", background_normal = self.images + "A3.png"))
                self.contenedor1.add_widget(Label())
                
                self.contenedor1.add_widget(Label())
                self.contenedor1.add_widget(Image(source = self.statsimg +"icon_pm.png",size_hint_x = None , width = 50))
                self.contenedor1.add_widget(Button(valign ='middle',text_size = (150,30),halign = "left",size_hint_x = None, width = 150,markup = True,text="[color=#404040][b]PM", background_normal = self.images + "A3.png"))
                self.contenedor1.add_widget(Label())
                self.contenedor1.add_widget(Button(size_hint_x = None, width = 50,markup = True,text="[color=#404040]0", background_normal = self.images + "A3.png"))
                self.contenedor1.add_widget(Label())
                
                self.contenedor1.add_widget(Label())
                self.contenedor1.add_widget(Image(source = self.statsimg +"tx_range.png",size_hint_x = None , width = 50))
                self.contenedor1.add_widget(Button(valign ='middle',text_size = (150,30),halign = "left",size_hint_x = None, width = 150,markup = True,text="[color=#404040][b]Alcance", background_normal = self.images + "A3.png"))
                self.contenedor1.add_widget(Label())
                self.contenedor1.add_widget(Button(size_hint_x = None, width = 50,markup = True,text="[color=#404040]0", background_normal = self.images + "A3.png"))
                self.contenedor1.add_widget(Label())
                
                self.contenedor1.add_widget(Label())
                self.contenedor1.add_widget(Image(source = self.statsimg +"tx_prospecting.png",size_hint_x = None , width = 50))
                self.contenedor1.add_widget(Button(valign ='middle',text_size = (150,30),halign = "left",size_hint_x = None, width = 150,markup = True,text="[color=#404040][b]Prosppección", background_normal = self.images + "A3.png"))
                self.contenedor1.add_widget(Label())
                self.contenedor1.add_widget(Button(size_hint_x = None, width = 50,markup = True,text="[color=#404040]0", background_normal = self.images + "A3.png"))
                self.contenedor1.add_widget(Label())
                
                self.contenedor1.add_widget(Label())
                self.contenedor1.add_widget(Image(source = self.statsimg +"tx_initiative.png",size_hint_x = None , width = 50))
                self.contenedor1.add_widget(Button(valign ='middle',text_size = (150,30),halign = "left",size_hint_x = None, width = 150,markup = True,text="[color=#404040][b]Iniciativa", background_normal = self.images + "A3.png"))
                self.contenedor1.add_widget(Label())
                self.contenedor1.add_widget(Button(size_hint_x = None, width = 50,markup = True,text="[color=#404040]0", background_normal = self.images + "A3.png"))
                self.contenedor1.add_widget(Label())
                
                self.contenedor1.add_widget(Label(size_hint_x = 1))
                self.contenedor1.add_widget(Image(source = self.statsimg +"tx_crit.png",size_hint_x = None , width = 25))
                self.contenedor1.add_widget(Button(text_size = (150,30),valign ='middle',halign = 'left',size_hint_x = None, width = 150,markup = True,text="[color=#404040][b]Críticos", background_normal = self.images + "A3.png"))
                self.contenedor1.add_widget(Label(size_hint_x = 1))
                self.contenedor1.add_widget(Button(size_hint_x = None, width = 50,markup = True,text="[color=#404040]0", background_normal = self.images + "A3.png"))
                self.contenedor1.add_widget(Label(size_hint_x = 1))
                
                self.contenedor1.add_widget(Label())
                self.contenedor1.add_widget(Image(source = self.statsimg +"tx_summonableCreaturesBoost.png",size_hint_x = None , width = 25))
                self.contenedor1.add_widget(Button(text_size = (150,30),valign ='middle',halign = 'left',size_hint_x = None, width = 150,markup = True,text="[color=#404040][b]Invocaciones", background_normal = self.images + "A3.png"))
                self.contenedor1.add_widget(Label())
                self.contenedor1.add_widget(Button(size_hint_x = None, width = 50,markup = True,text="[color=#404040]0", background_normal = self.images + "A3.png"))
                self.contenedor1.add_widget(Label())

            if i == Puntos[2]:
                self.Punto2 = GridLayout(cols = 1, size_hint_y = None , height = 480)
                self.contenedor2 = GridLayout(cols = 6,size_hint_y = None, height = 300)
                self.Punto2.add_widget(Image(size_hint_y = None, height = 30,source = self.images +"A3.png", allow_stretch = True, keep_ratio = False))
                self.Punto2.add_widget(Button(font_size = 30,markup = True, text="[color=#404040]Stats Principales",size_hint_y = None , height = 50, background_normal = self.images + "A3.png"))
                self.Punto2.add_widget(Image(size_hint_y = None, height = 30,source = self.images +"A3.png", allow_stretch = True, keep_ratio = False))
                self.Punto2.add_widget(Image(size_hint_y = None, height = 100,source = self.hudimg +"icon__0006_Titre_ornement.png", allow_stretch = False, keep_ratio = True))
                self.Punto2.add_widget(Image(size_hint_y = None, height = 30,source = self.images +"A3.png", allow_stretch = True, keep_ratio = False))
                self.Punto2.add_widget(self.contenedor2)
                self.Punto2.add_widget(Label())
                #self.Punto2.add_widget(Image(size_hint_y = None, height = 30,source = self.images +"A3C.png", allow_stretch = True, keep_ratio = False))
                self.Form2.add_widget(self.Punto2)
                
                self.contenedor2.add_widget(Label())
                self.contenedor2.add_widget(Image(source = self.statsimg +"tx_vitality.png",size_hint_x = None , width = 30))
                self.contenedor2.add_widget(Button(valign ='middle',text_size = (150,30),halign = "left",size_hint_x = None, width = 150,markup = True,text="[color=#404040][b]Vitalidad", background_normal = self.images + "A3.png"))
                self.contenedor2.add_widget(Label())
                self.contenedor2.add_widget(Button(size_hint_x = None, width = 30,markup = True,text="[color=#404040]0", background_normal = self.images + "A3.png"))
                self.contenedor2.add_widget(Label())
                
                self.contenedor2.add_widget(Label())
                self.contenedor2.add_widget(Image(source = self.statsimg +"tx_wisdom.png",size_hint_x = None , width = 30))
                self.contenedor2.add_widget(Button(valign ='middle',text_size = (150,30),halign = "left",size_hint_x = None, width = 150,markup = True,text="[color=#404040][b]Sabiduria", background_normal = self.images + "A3.png"))
                self.contenedor2.add_widget(Label())
                self.contenedor2.add_widget(Button(size_hint_x = None, width = 30,markup = True,text="[color=#404040]0", background_normal = self.images + "A3.png"))
                self.contenedor2.add_widget(Label())
                
                self.contenedor2.add_widget(Label())
                self.contenedor2.add_widget(Image(source = self.statsimg +"tx_strength.png",size_hint_x = None , width = 30))
                self.contenedor2.add_widget(Button(valign ='middle',text_size = (150,30),halign = "left",size_hint_x = None, width = 150,markup = True,text="[color=#404040][b]Fuerza", background_normal = self.images + "A3.png"))
                self.contenedor2.add_widget(Label())
                self.contenedor2.add_widget(Button(size_hint_x = None, width = 30,markup = True,text="[color=#404040]0", background_normal = self.images + "A3.png"))
                self.contenedor2.add_widget(Label())
                
                self.contenedor2.add_widget(Label())
                self.contenedor2.add_widget(Image(source = self.statsimg +"tx_intelligence.png",size_hint_x = None , width = 30))
                self.contenedor2.add_widget(Button(valign ='middle',text_size = (150,30),halign = "left",size_hint_x = None, width = 150,markup = True,text="[color=#404040][b]Inteligencia", background_normal = self.images + "A3.png"))
                self.contenedor2.add_widget(Label())
                self.contenedor2.add_widget(Button(size_hint_x = None, width = 30,markup = True,text="[color=#404040]0", background_normal = self.images + "A3.png"))
                self.contenedor2.add_widget(Label())
                
                self.contenedor2.add_widget(Label())
                self.contenedor2.add_widget(Image(source = self.statsimg +"tx_chance.png",size_hint_x = None , width = 30))
                self.contenedor2.add_widget(Button(valign ='middle',text_size = (150,30),halign = "left",size_hint_x = None, width = 150,markup = True,text="[color=#404040][b]Suerte", background_normal = self.images + "A3.png"))
                self.contenedor2.add_widget(Label())
                self.contenedor2.add_widget(Button(size_hint_x = None, width = 30,markup = True,text="[color=#404040]0", background_normal = self.images + "A3.png"))
                self.contenedor2.add_widget(Label())
                
                self.contenedor2.add_widget(Label())
                self.contenedor2.add_widget(Image(source = self.statsimg +"tx_agility.png",size_hint_x = None , width = 30))
                self.contenedor2.add_widget(Button(valign ='middle',text_size = (150,30),halign = "left",size_hint_x = None, width = 150,markup = True,text="[color=#404040][b]Agilidad", background_normal = self.images + "A3.png"))
                self.contenedor2.add_widget(Label())
                self.contenedor2.add_widget(Button(size_hint_x = None, width = 30,markup = True,text="[color=#404040]0", background_normal = self.images + "A3.png"))
                self.contenedor2.add_widget(Label())
                
            if i == Puntos[3]:
                self.Punto3 = GridLayout(cols = 1, size_hint_y = None , height = 700)
                self.contenedor3 = GridLayout(cols = 6,size_hint_y = None, height = 390)
                self.Punto3.add_widget(Image(size_hint_y = None, height = 30,source = self.images +"A3.png", allow_stretch = True, keep_ratio = False))
                self.Punto3.add_widget(Button(font_size = 30,markup = True, text="[color=#404040]Daños",size_hint_y = None , height = 50, background_normal = self.images + "A3.png"))
                self.Punto3.add_widget(Image(size_hint_y = None, height = 30,source = self.images +"A3.png", allow_stretch = True, keep_ratio = False))
                self.Punto3.add_widget(Image(size_hint_y = None, height = 100,source = self.hudimg +"icon__0010_Compagnon.png", allow_stretch = False, keep_ratio = True))
                self.Punto3.add_widget(Image(size_hint_y = None, height = 30,source = self.images +"A3.png", allow_stretch = True, keep_ratio = False))
                self.Punto3.add_widget(self.contenedor3)
                self.Punto3.add_widget(Label())
                #self.Punto3.add_widget(Image(size_hint_y = None, height = 30,source = self.images +"A3C.png", allow_stretch = True, keep_ratio = False))
                self.Form2.add_widget(self.Punto3)
                
                self.contenedor3.add_widget(Label())
                self.contenedor3.add_widget(Image(source = self.statsimg +"tx_damage.png",size_hint_x = None , width = 30))
                self.contenedor3.add_widget(Button(valign ='middle',text_size = (150,30),halign = "left",size_hint_x = None, width = 150,markup = True,text="[color=#404040][b]Daños", background_normal = self.images + "A3.png"))
                self.contenedor3.add_widget(Label())
                self.contenedor3.add_widget(Button(size_hint_x = None, width = 30,markup = True,text="[color=#404040]0", background_normal = self.images + "A3.png"))
                self.contenedor3.add_widget(Label())
                
                self.contenedor3.add_widget(Label())
                self.contenedor3.add_widget(Image(source = self.statsimg +"tx_damagesPercent.png",size_hint_x = None , width = 30))
                self.contenedor3.add_widget(Button(valign ='middle',text_size = (150,30),halign = "left",size_hint_x = None, width = 150,markup = True,text="[color=#404040][b]Potencia", background_normal = self.images + "A3.png"))
                self.contenedor3.add_widget(Label())
                self.contenedor3.add_widget(Button(size_hint_x = None, width = 30,markup = True,text="[color=#404040]0", background_normal = self.images + "A3.png"))
                self.contenedor3.add_widget(Label())
                
                self.contenedor3.add_widget(Label())
                self.contenedor3.add_widget(Image(source = self.statsimg +"tx_criticalDamage.png",size_hint_x = None , width = 30))
                self.contenedor3.add_widget(Button(valign ='middle',text_size = (150,30),halign = "left",size_hint_x = None, width = 150,markup = True,text="[color=#404040][b]Daños Criticos", background_normal = self.images + "A3.png"))
                self.contenedor3.add_widget(Label())
                self.contenedor3.add_widget(Button(size_hint_x = None, width = 30,markup = True,text="[color=#404040]0", background_normal = self.images + "A3.png"))
                self.contenedor3.add_widget(Label())
                
                self.contenedor3.add_widget(Label())
                self.contenedor3.add_widget(Image(source = self.statsimg +"tx_res_neutral.png",size_hint_x = None , width = 30))
                self.contenedor3.add_widget(Button(valign ='middle',text_size = (150,30),halign = "left",size_hint_x = None, width = 150,markup = True,text="[color=#404040][b]Neutrales", background_normal = self.images + "A3.png"))
                self.contenedor3.add_widget(Label())
                self.contenedor3.add_widget(Button(size_hint_x = None, width = 30,markup = True,text="[color=#404040]0", background_normal = self.images + "A3.png"))
                self.contenedor3.add_widget(Label())
                
                self.contenedor3.add_widget(Label())
                self.contenedor3.add_widget(Image(source = self.statsimg +"tx_res_earth.png",size_hint_x = None , width = 30))
                self.contenedor3.add_widget(Button(valign ='middle',text_size = (150,30),halign = "left",size_hint_x = None, width = 150,markup = True,text="[color=#404040][b]Tierra", background_normal = self.images + "A3.png"))
                self.contenedor3.add_widget(Label())
                self.contenedor3.add_widget(Button(size_hint_x = None, width = 30,markup = True,text="[color=#404040]0", background_normal = self.images + "A3.png"))
                self.contenedor3.add_widget(Label()) 
                
                self.contenedor3.add_widget(Label())
                self.contenedor3.add_widget(Image(source = self.statsimg +"tx_res_fire.png",size_hint_x = None , width = 30))
                self.contenedor3.add_widget(Button(valign ='middle',text_size = (150,30),halign = "left",size_hint_x = None, width = 150,markup = True,text="[color=#404040][b]Fuego", background_normal = self.images + "A3.png"))
                self.contenedor3.add_widget(Label())
                self.contenedor3.add_widget(Button(size_hint_x = None, width = 30,markup = True,text="[color=#404040]0", background_normal = self.images + "A3.png"))
                self.contenedor3.add_widget(Label())    
                
                self.contenedor3.add_widget(Label())
                self.contenedor3.add_widget(Image(source = self.statsimg +"tx_res_water.png",size_hint_x = None , width = 30))
                self.contenedor3.add_widget(Button(valign ='middle',text_size = (150,30),halign = "left",size_hint_x = None, width = 150,markup = True,text="[color=#404040][b]Agua", background_normal = self.images + "A3.png"))
                self.contenedor3.add_widget(Label())
                self.contenedor3.add_widget(Button(size_hint_x = None, width = 30,markup = True,text="[color=#404040]0", background_normal = self.images + "A3.png"))
                self.contenedor3.add_widget(Label())
                
                self.contenedor3.add_widget(Label())
                self.contenedor3.add_widget(Image(source = self.statsimg +"tx_res_air.png",size_hint_x = None , width = 30))
                self.contenedor3.add_widget(Button(valign ='middle',text_size = (150,30),halign = "left",size_hint_x = None, width = 150,markup = True,text="[color=#404040][b]Aire", background_normal = self.images + "A3.png"))
                self.contenedor3.add_widget(Label())
                self.contenedor3.add_widget(Button(size_hint_x = None, width = 30,markup = True,text="[color=#404040]0", background_normal = self.images + "A3.png"))
                self.contenedor3.add_widget(Label())
                
                self.contenedor3.add_widget(Label())
                self.contenedor3.add_widget(Image(source = self.statsimg +"tx_return.png",size_hint_x = None , width = 30))
                self.contenedor3.add_widget(Button(valign ='middle',text_size = (150,30),halign = "left",size_hint_x = None, width = 150,markup = True,text="[color=#404040][b]Reenvio", background_normal = self.images + "A3.png"))
                self.contenedor3.add_widget(Label())
                self.contenedor3.add_widget(Button(size_hint_x = None, width = 30,markup = True,text="[color=#404040]0", background_normal = self.images + "A3.png"))
                self.contenedor3.add_widget(Label())
                
                self.contenedor3.add_widget(Label())
                self.contenedor3.add_widget(Image(source = self.statsimg +"tx_weaponDamage.png",size_hint_x = None , width = 30))
                self.contenedor3.add_widget(Button(valign ='middle',text_size = (150,30),halign = "left",size_hint_x = None, width = 150,markup = True,text="[color=#404040][b]Dominio de Arma", background_normal = self.images + "A3.png"))
                self.contenedor3.add_widget(Label())
                self.contenedor3.add_widget(Button(size_hint_x = None, width = 30,markup = True,text="[color=#404040]0", background_normal = self.images + "A3.png"))
                self.contenedor3.add_widget(Label())
                
                self.contenedor3.add_widget(Label())
                self.contenedor3.add_widget(Image(source = self.statsimg +"tx_trap.png",size_hint_x = None , width = 30))
                self.contenedor3.add_widget(Button(valign ='middle',text_size = (150,30),halign = "left",size_hint_x = None, width = 150,markup = True,text="[color=#404040][b]Trampas", background_normal = self.images + "A3.png"))
                self.contenedor3.add_widget(Label())
                self.contenedor3.add_widget(Button(size_hint_x = None, width = 30,markup = True,text="[color=#404040]0", background_normal = self.images + "A3.png"))
                self.contenedor3.add_widget(Label())
                
                self.contenedor3.add_widget(Label())
                self.contenedor3.add_widget(Image(source = self.statsimg +"tx_trapPercent.png",size_hint_x = None , width = 30))
                self.contenedor3.add_widget(Button(valign ='middle',text_size = (150,30),halign = "left",size_hint_x = None, width = 150,markup = True,text="[color=#404040][b]Trampas(Potencia)", background_normal = self.images + "A3.png"))
                self.contenedor3.add_widget(Label())
                self.contenedor3.add_widget(Button(size_hint_x = None, width = 30,markup = True,text="[color=#404040]0", background_normal = self.images + "A3.png"))
                self.contenedor3.add_widget(Label())
                
                self.contenedor3.add_widget(Label())
                self.contenedor3.add_widget(Image(source = self.statsimg +"tx_push.png",size_hint_x = None , width = 30))
                self.contenedor3.add_widget(Button(valign ='middle',text_size = (150,30),halign = "left",size_hint_x = None, width = 150,markup = True,text="[color=#404040][b]Empuje", background_normal = self.images + "A3.png"))
                self.contenedor3.add_widget(Label())
                self.contenedor3.add_widget(Button(size_hint_x = None, width = 30,markup = True,text="[color=#404040]0", background_normal = self.images + "A3.png"))
                self.contenedor3.add_widget(Label())
                
                
                

                self.Avanzados1 = GridLayout(cols = 6,size_hint_y = None, height = 150)
                self.Avanzados2 = GridLayout(cols = 6,size_hint_y = None, height = 150)
                
                
                self.Avanzados1.add_widget(Label())
                self.Avanzados1.add_widget(Image(source = self.statsimg +"tx_escape.png",size_hint_x = None , width = 30))
                self.Avanzados1.add_widget(Button(valign ='middle',text_size = (150,30),halign = "left",size_hint_x = None, width = 150,markup = True,text="[color=#404040][b]Esquiva", background_normal = self.images + "A3.png"))
                self.Avanzados1.add_widget(Label())
                self.Avanzados1.add_widget(Button(size_hint_x = None, width = 30,markup = True,text="[color=#404040]0", background_normal = self.images + "A3.png"))
                self.Avanzados1.add_widget(Label())    
                
                self.Avanzados1.add_widget(Label())
                self.Avanzados1.add_widget(Image(source = self.statsimg +"icon_tackle.png",size_hint_x = None , width = 30))
                self.Avanzados1.add_widget(Button(valign ='middle',text_size = (150,30),halign = "left",size_hint_x = None, width = 150,markup = True,text="[color=#404040][b]Placaje", background_normal = self.images + "A3.png"))
                self.Avanzados1.add_widget(Label())
                self.Avanzados1.add_widget(Button(size_hint_x = None, width = 30,markup = True,text="[color=#404040]0", background_normal = self.images + "A3.png"))
                self.Avanzados1.add_widget(Label())   

                self.Avanzados1.add_widget(Label())
                self.Avanzados1.add_widget(Image(source = self.statsimg +"tx_heal.png",size_hint_x = None , width = 30))
                self.Avanzados1.add_widget(Button(valign ='middle',text_size = (150,30),halign = "left",size_hint_x = None, width = 150,markup = True,text="[color=#404040][b]Curas", background_normal = self.images + "A3.png"))
                self.Avanzados1.add_widget(Label())
                self.Avanzados1.add_widget(Button(size_hint_x = None, width = 30,markup = True,text="[color=#404040]0", background_normal = self.images + "A3.png"))
                self.Avanzados1.add_widget(Label())   



                
                
                self.Avanzados2.add_widget(Label())
                self.Avanzados2.add_widget(Image(source = self.statsimg +"tx_attackAP.png",size_hint_x = None , width = 30))
                self.Avanzados2.add_widget(Button(valign ='middle',text_size = (150,30),halign = "left",size_hint_x = None, width = 150,markup = True,text="[color=#404040][b]Robo PA", background_normal = self.images + "A3.png"))
                self.Avanzados2.add_widget(Label())
                self.Avanzados2.add_widget(Button(size_hint_x = None, width = 30,markup = True,text="[color=#404040]0", background_normal = self.images + "A3.png"))
                self.Avanzados2.add_widget(Label())
                
                self.Avanzados2.add_widget(Label())
                self.Avanzados2.add_widget(Image(source = self.statsimg +"tx_dodgeAP.png",size_hint_x = None , width = 30))
                self.Avanzados2.add_widget(Button(valign ='middle',text_size = (150,30),halign = "left",size_hint_x = None, width = 150,markup = True,text="[color=#404040][b]Res. Robo PA", background_normal = self.images + "A3.png"))
                self.Avanzados2.add_widget(Label())
                self.Avanzados2.add_widget(Button(size_hint_x = None, width = 30,markup = True,text="[color=#404040]0", background_normal = self.images + "A3.png"))
                self.Avanzados2.add_widget(Label())
                
                self.Avanzados2.add_widget(Label())
                self.Avanzados2.add_widget(Image(source = self.statsimg +"tx_attackMP.png",size_hint_x = None , width = 30))
                self.Avanzados2.add_widget(Button(valign ='middle',text_size = (150,30),halign = "left",size_hint_x = None, width = 150,markup = True,text="[color=#404040][b]Robo PM", background_normal = self.images + "A3.png"))
                self.Avanzados2.add_widget(Label())
                self.Avanzados2.add_widget(Button(size_hint_x = None, width = 30,markup = True,text="[color=#404040]0", background_normal = self.images + "A3.png"))
                self.Avanzados2.add_widget(Label())
                
                self.Avanzados2.add_widget(Label())
                self.Avanzados2.add_widget(Image(source = self.statsimg +"tx_dodgeMP.png",size_hint_x = None , width = 30))
                self.Avanzados2.add_widget(Button(valign ='middle',text_size = (150,30),halign = "left",size_hint_x = None, width = 150,markup = True,text="[color=#404040][b]Res. Robo PM", background_normal = self.images + "A3.png"))
                self.Avanzados2.add_widget(Label())
                self.Avanzados2.add_widget(Button(size_hint_x = None, width = 30,markup = True,text="[color=#404040]0", background_normal = self.images + "A3.png"))
                self.Avanzados2.add_widget(Label())
                

                
                self.Form2.add_widget(Image(source = self.images + "A3D.png", size_hint_y = None, height = 5 , allow_stretch = True , keep_ratio = False))
                self.Form2.add_widget(Image(source = self.images + "A3D.png", size_hint_y = None, height = 5 , allow_stretch = True , keep_ratio = False))
                self.Form2.add_widget(self.Avanzados1)
                self.Form2.add_widget(self.Avanzados2)
                self.Form2.add_widget(Image(source = self.images + "A3D.png", size_hint_y = None, height = 5 , allow_stretch = True , keep_ratio = False))
                self.Form2.add_widget(Image(source = self.images + "A3D.png", size_hint_y = None, height = 5 , allow_stretch = True , keep_ratio = False))
                
                
                
                
                
                
            if i == Puntos[4]:
                self.Punto3 = GridLayout(cols = 1, size_hint_y = None , height = 600)
                self.contenedor3 = GridLayout(cols = 6,size_hint_y = None, height = 300)
                self.Punto3.add_widget(Image(size_hint_y = None, height = 30,source = self.images +"A3.png", allow_stretch = True, keep_ratio = False))
                self.Punto3.add_widget(Button(font_size = 30,markup = True, text="[color=#404040]Res. % PVM",size_hint_y = None , height = 50, background_normal = self.images + "A3.png"))
                self.Punto3.add_widget(Image(size_hint_y = None, height = 30,source = self.images +"A3.png", allow_stretch = True, keep_ratio = False))
                self.Punto3.add_widget(Image(size_hint_y = None, height = 100,source = self.hudimg +"icon__0022_Groupe.png", allow_stretch = False, keep_ratio = True))
                self.Punto3.add_widget(Image(size_hint_y = None, height = 30,source = self.images +"A3.png", allow_stretch = True, keep_ratio = False))
                self.Punto3.add_widget(self.contenedor3)
                self.Punto3.add_widget(Label())
                #self.Punto3.add_widget(Image(size_hint_y = None, height = 30,source = self.images +"A3C.png", allow_stretch = True, keep_ratio = False))
                self.Form2.add_widget(self.Punto3)
                
                self.contenedor3.add_widget(Label())
                self.contenedor3.add_widget(Image(source = self.statsimg +"tx_res_neutral.png",size_hint_x = None , width = 30))
                self.contenedor3.add_widget(Button(valign ='middle',text_size = (150,30),halign = "left", size_hint_x = None, width = 150,markup = True,text="[color=#404040][b]Res. Neutral", background_normal = self.images + "A3.png"))
                self.contenedor3.add_widget(Label())
                self.contenedor3.add_widget(Button(valign ='middle',text_size = (30,30),halign = "left",size_hint_x = None, width = 30,markup = True,text="[color=#404040]0%", background_normal = self.images + "A3.png"))
                self.contenedor3.add_widget(Label())
                
                self.contenedor3.add_widget(Label())
                self.contenedor3.add_widget(Image(source = self.statsimg +"tx_res_neutral.png",size_hint_x = None , width = 30))
                self.contenedor3.add_widget(Button(valign ='middle',text_size = (150,30),halign = "left",size_hint_x = None, width = 150,markup = True,text="[color=#404040][b]Res. Neutral(Fíjo)", background_normal = self.images + "A3.png"))
                self.contenedor3.add_widget(Label())
                self.contenedor3.add_widget(Button(valign ='middle',text_size = (30,30),halign = "left",size_hint_x = None, width = 30,markup = True,text="[color=#404040]0", background_normal = self.images + "A3.png"))
                self.contenedor3.add_widget(Label())
                
                
                self.contenedor3.add_widget(Label())
                self.contenedor3.add_widget(Image(source = self.statsimg +"tx_res_fire.png",size_hint_x = None , width = 30))
                self.contenedor3.add_widget(Button(valign ='middle',text_size = (150,30),halign = "left",size_hint_x = None, width = 150,markup = True,text="[color=#404040][b]Res. Fuego", background_normal = self.images + "A3.png"))
                self.contenedor3.add_widget(Label())
                self.contenedor3.add_widget(Button(valign ='middle',text_size = (30,30),halign = "left",size_hint_x = None, width = 30,markup = True,text="[color=#404040]0%", background_normal = self.images + "A3.png"))
                self.contenedor3.add_widget(Label())
                
                self.contenedor3.add_widget(Label())
                self.contenedor3.add_widget(Image(source = self.statsimg +"tx_res_fire.png",size_hint_x = None , width = 30))
                self.contenedor3.add_widget(Button(valign ='middle',text_size = (150,30),halign = "left",size_hint_x = None, width = 150,markup = True,text="[color=#404040][b]Res. Fuego(Fíjo)", background_normal = self.images + "A3.png"))
                self.contenedor3.add_widget(Label())
                self.contenedor3.add_widget(Button(valign ='middle',text_size = (30,30),halign = "left",size_hint_x = None, width = 30,markup = True,text="[color=#404040]0", background_normal = self.images + "A3.png"))
                self.contenedor3.add_widget(Label())
                
                self.contenedor3.add_widget(Label())
                self.contenedor3.add_widget(Image(source = self.statsimg +"tx_res_earth.png",size_hint_x = None , width = 30))
                self.contenedor3.add_widget(Button(valign ='middle',text_size = (150,30),halign = "left",size_hint_x = None, width = 150,markup = True,text="[color=#404040][b]Res. Tierra", background_normal = self.images + "A3.png"))
                self.contenedor3.add_widget(Label())
                self.contenedor3.add_widget(Button(valign ='middle',text_size = (30,30),halign = "left",size_hint_x = None, width = 30,markup = True,text="[color=#404040]0%", background_normal = self.images + "A3.png"))
                self.contenedor3.add_widget(Label())
                
                self.contenedor3.add_widget(Label())
                self.contenedor3.add_widget(Image(source = self.statsimg +"tx_res_earth.png",size_hint_x = None , width = 30))
                self.contenedor3.add_widget(Button(valign ='middle',text_size = (150,30),halign = "left",size_hint_x = None, width = 150,markup = True,text="[color=#404040][b]Res. Tierra(Fíjo)", background_normal = self.images + "A3.png"))
                self.contenedor3.add_widget(Label())
                self.contenedor3.add_widget(Button(valign ='middle',text_size = (30,30),halign = "left",size_hint_x = None, width = 30,markup = True,text="[color=#404040]0", background_normal = self.images + "A3.png"))
                self.contenedor3.add_widget(Label())
                
                self.contenedor3.add_widget(Label())
                self.contenedor3.add_widget(Image(source = self.statsimg +"tx_res_air.png",size_hint_x = None , width = 30))
                self.contenedor3.add_widget(Button(valign ='middle',text_size = (150,30),halign = "left",size_hint_x = None, width = 150,markup = True,text="[color=#404040][b]Res. Aire", background_normal = self.images + "A3.png"))
                self.contenedor3.add_widget(Label())
                self.contenedor3.add_widget(Button(valign ='middle',text_size = (30,30),halign = "left",size_hint_x = None, width = 30,markup = True,text="[color=#404040]0%", background_normal = self.images + "A3.png"))
                self.contenedor3.add_widget(Label())
                
                self.contenedor3.add_widget(Label())
                self.contenedor3.add_widget(Image(source = self.statsimg +"tx_res_air.png",size_hint_x = None , width = 30))
                self.contenedor3.add_widget(Button(valign ='middle',text_size = (150,30),halign = "left",size_hint_x = None, width = 150,markup = True,text="[color=#404040][b]Res. Aire(Fíjo)", background_normal = self.images + "A3.png"))
                self.contenedor3.add_widget(Label())
                self.contenedor3.add_widget(Button(valign ='middle',text_size = (30,30),halign = "left",size_hint_x = None, width = 30,markup = True,text="[color=#404040]0", background_normal = self.images + "A3.png"))
                self.contenedor3.add_widget(Label())
                
                self.contenedor3.add_widget(Label())
                self.contenedor3.add_widget(Image(source = self.statsimg +"tx_res_water.png",size_hint_x = None , width = 30))
                self.contenedor3.add_widget(Button(valign ='middle',text_size = (150,30),halign = "left",size_hint_x = None, width = 150,markup = True,text="[color=#404040][b]Res. Agua", background_normal = self.images + "A3.png"))
                self.contenedor3.add_widget(Label())
                self.contenedor3.add_widget(Button(valign ='middle',text_size = (30,30),halign = "left",size_hint_x = None, width = 30,markup = True,text="[color=#404040]0%", background_normal = self.images + "A3.png"))
                self.contenedor3.add_widget(Label())
                
                self.contenedor3.add_widget(Label())
                self.contenedor3.add_widget(Image(source = self.statsimg +"tx_res_water.png",size_hint_x = None , width = 30))
                self.contenedor3.add_widget(Button(valign ='middle',text_size = (150,30),halign = "left",size_hint_x = None, width = 150,markup = True,text="[color=#404040][b]Res. Agua(Fíjo)", background_normal = self.images + "A3.png"))
                self.contenedor3.add_widget(Label())
                self.contenedor3.add_widget(Button(valign ='middle',text_size = (30,30),halign = "left",size_hint_x = None, width = 30,markup = True,text="[color=#404040]0", background_normal = self.images + "A3.png"))
                self.contenedor3.add_widget(Label())
                
            if i == Puntos[5]:
                self.Punto3 = GridLayout(cols = 1, size_hint_y = None , height = 600)
                self.contenedor3 = GridLayout(cols = 6,size_hint_y = None, height = 300)
                self.Punto3.add_widget(Image(size_hint_y = None, height = 30,source = self.images +"A3.png", allow_stretch = True, keep_ratio = False))
                self.Punto3.add_widget(Button(font_size = 30,markup = True, text="[color=#404040]Res. % PVP",size_hint_y = None , height = 50, background_normal = self.images + "A3.png"))
                self.Punto3.add_widget(Image(size_hint_y = None, height = 30,source = self.images +"A3.png", allow_stretch = True, keep_ratio = False))
                self.Punto3.add_widget(Image(size_hint_y = None, height = 100,source = self.hudimg +"icon__0009_Kolizeum.png", allow_stretch = False, keep_ratio = True))
                self.Punto3.add_widget(Image(size_hint_y = None, height = 30,source = self.images +"A3.png", allow_stretch = True, keep_ratio = False))
                self.Punto3.add_widget(self.contenedor3)
                self.Punto3.add_widget(Label())
                #self.Punto3.add_widget(Image(size_hint_y = None, height = 30,source = self.images +"A3C.png", allow_stretch = True, keep_ratio = False))
                self.Form2.add_widget(self.Punto3)
                
                self.contenedor3.add_widget(Label())
                self.contenedor3.add_widget(Image(source = self.statsimg +"tx_res_neutral.png",size_hint_x = None , width = 30))
                self.contenedor3.add_widget(Button(valign ='middle',text_size = (150,30),halign = "left", size_hint_x = None, width = 150,markup = True,text="[color=#404040][b]Res. Neutral", background_normal = self.images + "A3.png"))
                self.contenedor3.add_widget(Label())
                self.contenedor3.add_widget(Button(valign ='middle',text_size = (30,30),halign = "left",size_hint_x = None, width = 30,markup = True,text="[color=#404040]0%", background_normal = self.images + "A3.png"))
                self.contenedor3.add_widget(Label())
                
                self.contenedor3.add_widget(Label())
                self.contenedor3.add_widget(Image(source = self.statsimg +"tx_res_neutral.png",size_hint_x = None , width = 30))
                self.contenedor3.add_widget(Button(valign ='middle',text_size = (150,30),halign = "left",size_hint_x = None, width = 150,markup = True,text="[color=#404040][b]Res. Neutral(Fíjo)", background_normal = self.images + "A3.png"))
                self.contenedor3.add_widget(Label())
                self.contenedor3.add_widget(Button(valign ='middle',text_size = (30,30),halign = "left",size_hint_x = None, width = 30,markup = True,text="[color=#404040]0", background_normal = self.images + "A3.png"))
                self.contenedor3.add_widget(Label())
                
                
                self.contenedor3.add_widget(Label())
                self.contenedor3.add_widget(Image(source = self.statsimg +"tx_res_fire.png",size_hint_x = None , width = 30))
                self.contenedor3.add_widget(Button(valign ='middle',text_size = (150,30),halign = "left",size_hint_x = None, width = 150,markup = True,text="[color=#404040][b]Res. Fuego", background_normal = self.images + "A3.png"))
                self.contenedor3.add_widget(Label())
                self.contenedor3.add_widget(Button(valign ='middle',text_size = (30,30),halign = "left",size_hint_x = None, width = 30,markup = True,text="[color=#404040]0%", background_normal = self.images + "A3.png"))
                self.contenedor3.add_widget(Label())
                
                self.contenedor3.add_widget(Label())
                self.contenedor3.add_widget(Image(source = self.statsimg +"tx_res_fire.png",size_hint_x = None , width = 30))
                self.contenedor3.add_widget(Button(valign ='middle',text_size = (150,30),halign = "left",size_hint_x = None, width = 150,markup = True,text="[color=#404040][b]Res. Fuego(Fíjo)", background_normal = self.images + "A3.png"))
                self.contenedor3.add_widget(Label())
                self.contenedor3.add_widget(Button(valign ='middle',text_size = (30,30),halign = "left",size_hint_x = None, width = 30,markup = True,text="[color=#404040]0", background_normal = self.images + "A3.png"))
                self.contenedor3.add_widget(Label())
                
                self.contenedor3.add_widget(Label())
                self.contenedor3.add_widget(Image(source = self.statsimg +"tx_res_earth.png",size_hint_x = None , width = 30))
                self.contenedor3.add_widget(Button(valign ='middle',text_size = (150,30),halign = "left",size_hint_x = None, width = 150,markup = True,text="[color=#404040][b]Res. Tierra", background_normal = self.images + "A3.png"))
                self.contenedor3.add_widget(Label())
                self.contenedor3.add_widget(Button(valign ='middle',text_size = (30,30),halign = "left",size_hint_x = None, width = 30,markup = True,text="[color=#404040]0%", background_normal = self.images + "A3.png"))
                self.contenedor3.add_widget(Label())
                
                self.contenedor3.add_widget(Label())
                self.contenedor3.add_widget(Image(source = self.statsimg +"tx_res_earth.png",size_hint_x = None , width = 30))
                self.contenedor3.add_widget(Button(valign ='middle',text_size = (150,30),halign = "left",size_hint_x = None, width = 150,markup = True,text="[color=#404040][b]Res. Tierra(Fíjo)", background_normal = self.images + "A3.png"))
                self.contenedor3.add_widget(Label())
                self.contenedor3.add_widget(Button(valign ='middle',text_size = (30,30),halign = "left",size_hint_x = None, width = 30,markup = True,text="[color=#404040]0", background_normal = self.images + "A3.png"))
                self.contenedor3.add_widget(Label())
                
                self.contenedor3.add_widget(Label())
                self.contenedor3.add_widget(Image(source = self.statsimg +"tx_res_air.png",size_hint_x = None , width = 30))
                self.contenedor3.add_widget(Button(valign ='middle',text_size = (150,30),halign = "left",size_hint_x = None, width = 150,markup = True,text="[color=#404040][b]Res. Aire", background_normal = self.images + "A3.png"))
                self.contenedor3.add_widget(Label())
                self.contenedor3.add_widget(Button(valign ='middle',text_size = (30,30),halign = "left",size_hint_x = None, width = 30,markup = True,text="[color=#404040]0%", background_normal = self.images + "A3.png"))
                self.contenedor3.add_widget(Label())
                
                self.contenedor3.add_widget(Label())
                self.contenedor3.add_widget(Image(source = self.statsimg +"tx_res_air.png",size_hint_x = None , width = 30))
                self.contenedor3.add_widget(Button(valign ='middle',text_size = (150,30),halign = "left",size_hint_x = None, width = 150,markup = True,text="[color=#404040][b]Res. Aire(Fíjo)", background_normal = self.images + "A3.png"))
                self.contenedor3.add_widget(Label())
                self.contenedor3.add_widget(Button(valign ='middle',text_size = (30,30),halign = "left",size_hint_x = None, width = 30,markup = True,text="[color=#404040]0", background_normal = self.images + "A3.png"))
                self.contenedor3.add_widget(Label())
                
                self.contenedor3.add_widget(Label())
                self.contenedor3.add_widget(Image(source = self.statsimg +"tx_res_water.png",size_hint_x = None , width = 30))
                self.contenedor3.add_widget(Button(valign ='middle',text_size = (150,30),halign = "left",size_hint_x = None, width = 150,markup = True,text="[color=#404040][b]Res. Agua", background_normal = self.images + "A3.png"))
                self.contenedor3.add_widget(Label())
                self.contenedor3.add_widget(Button(valign ='middle',text_size = (30,30),halign = "left",size_hint_x = None, width = 30,markup = True,text="[color=#404040]0%", background_normal = self.images + "A3.png"))
                self.contenedor3.add_widget(Label())
                
                self.contenedor3.add_widget(Label())
                self.contenedor3.add_widget(Image(source = self.statsimg +"tx_res_water.png",size_hint_x = None , width = 30))
                self.contenedor3.add_widget(Button(valign ='middle',text_size = (150,30),halign = "left",size_hint_x = None, width = 150,markup = True,text="[color=#404040][b]Res. Agua(Fíjo)", background_normal = self.images + "A3.png"))
                self.contenedor3.add_widget(Label())
                self.contenedor3.add_widget(Button(valign ='middle',text_size = (30,30),halign = "left",size_hint_x = None, width = 30,markup = True,text="[color=#404040]0", background_normal = self.images + "A3.png"))
                self.contenedor3.add_widget(Label())
            
            
                

            
                
                
                

                
            
        
        
        
        
        
        
        
        #------------------------------------------------------------------------------------------------
        #ROOT 0 - LADO DERECHO
        
        self.root_0 = GridLayout(cols = 1 , size_hint = (1, 1) , spacing = 0)
        self.root_top = GridLayout(cols = 4, size_hint = (1,None),spacing = 0, height = 75)
        

            
        self.root_top_button1 = ImageButton(keep_ratio = True, allow_stretch = True,source=self.images + "Button4B.png", size_hint = (None,None),width = 75, height = 75)
        self.root_top_button3 = ImageButton(source=self.images + "Button5B.png", size_hint = (None, None),width = 75, height = 75, allow_stretch = True, keep_ratio = True)
        self.root_top_button2 = ImageButton(source=self.images + "Button6B.png", size_hint = (None, None), width = 75, height = 75, allow_stretch = True, keep_ratio = False)
        self.root_top_button4 = ImageButton(source=self.images + "Sponsor3.png", size_hint = (1, None), height = 75, allow_stretch = True, keep_ratio = False)
        self.root_top.add_widget(self.root_top_button1)
        self.root_top.add_widget(self.root_top_button3)
        self.root_top.add_widget(self.root_top_button4)
        self.root_top.add_widget(self.root_top_button2)
        self.root_0.add_widget(self.root_top)
        def pressed():
            print(" SI")
            self.Form1_Vista1.clear_widgets()
            
        #self.root_top_button1.bind(on_press = lambda j: pressed())
        self.root_top_button1.bind(on_press = lambda j: self.ROOT_Navitagiondrawer1.toggle_state())

        self.root_top_button3.bind(on_press = self.FORM1)
        
        self.MenuD =DropDown(auto_width = False , width = 300)
        self.MenuD.bind(on_select=lambda instance, x: setattr(self.root_top_button2, 'text', x))
        self.root_top_button2.bind(on_release= self.MenuD.open)

        self.MenuD.add_widget(Button(font_size = 30,text = "color=#404040]RECURSOS",font_name = "BebasNeue Regular", markup  =True ,background_normal=self.hudimg + "Button6.png", size_hint = (None, None), height = 70, width = 300,allow_stretch = True, keep_ratio = False))
        self.MenuD.add_widget(Button(font_size = 30,text = "[color=#404040]EQUIPOS",font_name = "BebasNeue Regular", markup  =True ,background_normal=self.hudimg + "Button6.png", size_hint = (None, None), height = 70,width = 300, allow_stretch = True, keep_ratio = False))
        self.MenuD.add_widget(Button(font_size = 30,text = "[color=#404040]BESTIARIO",font_name = "BebasNeue Regular", markup  =True ,background_normal=self.hudimg + "Button6.png", size_hint = (None, None), height = 70, width = 300,allow_stretch = True, keep_ratio = False))
        self.MenuD.add_widget(Button(font_size = 30,text = "[color=#404040]CONSUMIBLES",font_name = "BebasNeue Regular", markup  =True ,background_normal=self.hudimg + "Button6.png", size_hint = (None, None), height = 70, width = 300,allow_stretch = True, keep_ratio = False))
        self.MenuD.add_widget(Button(font_size = 30,text = "[color=#404040]ARMAS",font_name = "BebasNeue Regular", markup  =True ,background_normal=self.hudimg + "Button6.png", size_hint = (None, None), height = 70, width = 300,allow_stretch = True, keep_ratio = False))

       #self.root_top_button2.bind(on_release=lambda btn: self.MenuD.select(btn.text))
 
        #TOPMENU
        
        self.root_1 = GridLayout(cols = 1 , size_hint = (1, None) , spacing = 0)
        
        
        #PANEL DE VISTA
        
        
        
        self.Form1 = GridLayout(cols = 1 , size_hint = (1, None) , spacing = 0,size=(Window.width, Window.height))
        self.Form1_root = ScrollView(size_hint=(1, 1))
        self.panelesformularios = [self.Form1_root,self.Form2_root,self.Form3_root]
        self.root_0.add_widget(self.Form1_root)
        self.Form1.bind(minimum_height=self.Form1.setter('height'))
        self.Form1_root.add_widget(self.Form1)
        
        self.Espacio1 = Image(source=self.images + "A2.png", size_hint = (.25, 1), height = 25, allow_stretch = True, keep_ratio = False)
        self.Espacio2 = Image(source=self.images + "A4.png", size_hint = (.25, 1), height = 25, allow_stretch = True, keep_ratio = False)
        self.Espacio3 = Image(source=self.images + "A3.png", size_hint = (.25, None), height = 40, allow_stretch = True, keep_ratio = False)
        self.EspacioM = Image(source=self.images + "A3B.png", size_hint = (.25, None), height = 5, allow_stretch = True, keep_ratio = False)
        self.EspacioM2 = Image(source=self.images + "A3.png", size_hint = (.25, None), height = 5, allow_stretch = True, keep_ratio = False)
        self.EspacioM3 = Image(source=self.images + "A3C.png", size_hint = (.25, None), height = 5, allow_stretch = True, keep_ratio = False)
        self.Espacio4 = Image(source=self.images + "A3.png", size_hint = (.25, None), height = 40, allow_stretch = True, keep_ratio = False)
        self.Espacio5 = Image(source=self.images + "A2.png", size_hint = (.25, None), height = 40, allow_stretch = True, keep_ratio = False)
        self.Espacio6 = Image(source=self.images + "Sponsor5.png", size_hint = (.25, None), height = 40, allow_stretch = True, keep_ratio = False)
        self.Espacio7 = Image(source=self.images + "A4.png", size_hint = (.25, None), height = 40, allow_stretch = True, keep_ratio = False)
        self.Espacio_Grid = GridLayout(cols = 3, size_hint = (.25,None) , height = 100)
        self.Espacio8 = Image(source=self.images + "V3.png", size_hint = (.25, None), height = 40, allow_stretch = True, keep_ratio = False)
        self.Espacio9 = Image(source=self.images + "2201929 (2).png", size_hint = (None, None), width = 100, height = 100, allow_stretch = True, keep_ratio = False)
        self.Espacio10 = Image(source=self.images + "V3.png", size_hint = (.25, None), height = 40, allow_stretch = True, keep_ratio = False)
        self.Espacio11 = Image(source=self.images + "V3.png", size_hint = (.25, None), height = 40, allow_stretch = True, keep_ratio = False)
        self.Espacio12 = Image(source=self.images + "V3.png", size_hint = (.22, None), height = 40, allow_stretch = True, keep_ratio = False)
        self.Espacio15 = Image(source=self.images + "V3.png", size_hint = (.22, None), height = 40, allow_stretch = True, keep_ratio = False)
        
        self.Espacio16 = Image(source=self.images + "V3.png",width = 100, size_hint = (None, None), height = 188, allow_stretch = True , keep_ratio = False)
        self.Espacio16B = Image(source=self.images + "lomasduro.png",width = 400, size_hint = (None, None), height = 188, allow_stretch = True, keep_ratio = True)
        self.Espacio16C = Image(source=self.images + "V3.png", size_hint = (.22, None), height = 188, allow_stretch = True, keep_ratio = False)
        
        self.Espacio16_Grid = GridLayout(cols = 3, size_hint = (1, None), height = 188)
        self.Espacio17 = Image(source=self.images + "V3.png", size_hint = (.22, None), height = 40, allow_stretch = True, keep_ratio = False)
        
        self.Espacio16_Grid.add_widget(self.Espacio16B)
        self.Espacio16_Grid.add_widget(self.Espacio16)
        self.Espacio16_Grid.add_widget(self.Espacio16C)
        
        #self.Espacio_Grid.add_widget(self.Espacio9)
        self.Espacio_Grid.add_widget(self.Espacio8)
        #self.Espacio_Grid.add_widget(self.Espacio10)
        
        self.Titulo_grid = GridLayout(cols = 2)
        self.Titulo_grid_Label1 = Button(text = "Buscador", background_normal = self.images + "V2.png", size_hint = (1,None) , height = 25)
        self.Titulo_grid_Label2 = Button(text = "", background_normal = self.images + "A3.png", size_hint = (1,None) , height = 25)
        
        

        self.Titulo_grid.add_widget(self.Titulo_grid_Label1)
        self.Titulo_grid.add_widget(self.Titulo_grid_Label2)
        
        self.Form1.add_widget(self.EspacioM2)
        self.Form1.add_widget(self.Espacio16_Grid)
        self.Form1.add_widget(self.EspacioM)
        
    
        
        
        
        self.ROOT_Navitagiondrawer1.add_widget(self.ROOT_Boxlayout1)
        self.ROOT_Navitagiondrawer1.add_widget(self.root_0)
        

        
        
        
        
        self.Form1_TextIn = TextInput(text = "Busqueda.",foreground_color =(0,0,0,.7),width = 350,border = [10,10,10,10],font_size = 25 ,padding =[20,14,0,0],multiline = False,size_hint = (None,None), height = 55,background_active = self.images + 'TextInput1.png', background_normal = self.images + 'TextInput1.png')
        self.Form1_TextIn.bind(on_text_validate = self.actualizar_busqueda)
        self.Form1_TextIMG = Image(source = self.images + "Entypo_d83d(0)_128.png", size_hint = (None, 1), width = 65, allow_stretch = True, keep_ratio = False)
        self.Espacio18 = Image(source=self.images + "Sponsor5.png", size_hint = (.025, 1), height = 30, allow_stretch = True, keep_ratio = False)
        self.Espacio19 = Image(source=self.images + "Sponsor5.png", size_hint = (.025, 1), height = 30, allow_stretch = True, keep_ratio = False)
        self.Form1_Barra3 = Image(source=self.images + "Sponsor5.png", size_hint = (1, None), height = 50, allow_stretch = True, keep_ratio = False)
        self.Form1_TextIn_Grid = GridLayout(cols = 3, size_hint = (1,None), height =55)
        self.Form1_ABC_Grid = GridLayout(cols = 21,width = 1500, size_hint = (None,None), height =75)
        self.Form1_TextIn_Grid.add_widget(self.Espacio19)
        self.Form1_TextIn_Grid.add_widget(self.Form1_TextIn)
        self.Form1_TextIn_Grid.add_widget(self.Espacio18)
        
        self.Form1_HScroll = ScrollView(size_hint=(1, None), size=self.Form1_ABC_Grid.size)
        self.Form1_HScroll.add_widget(self.Form1_ABC_Grid)
        for i in self.busqueda:
            self.Form1_ABC = Button(text = "[color=#e6e6e6][b]"+i, markup = True, background_normal = self.images + "Button1.png")
            self.Form1_ABC_Grid.add_widget(self.Form1_ABC)
        
        
        self.Form1.add_widget(self.Espacio6)
        self.Form1.add_widget(self.Form1_TextIn_Grid)
        self.Form1.add_widget(self.Form1_Barra3)
        self.Form1.add_widget(self.EspacioM3)
        self.Form1.add_widget(self.Form1_HScroll)
        
        abcd = 0
        
        self.Espacio13 = Image(source=self.images + "A2.png", size_hint = (.25, None), height = 40, allow_stretch = True, keep_ratio =False)
        self.Espacio14 = Image(source=self.images + "A4.png", size_hint = (.25, None), height = 40, allow_stretch = True, keep_ratio = False)
        self.Form1_Vista2 = GridLayout(cols = 1 ,size_hint = (1,None), height = 400, allow_stretch = True, keep_ratio = False)
        self.Form1_Vista2_Image = Image(source = self.images + "logo_dofus.jpg", size_hint = (1,None), height = 200)

        self.textoo = "\nEsta aplicacion decidi hacerla por el echo de que \nAl final vi que quedo muy kawai asi que decidi publicarla \nsean bienvenidos a esta lista que tome de google :v."
        self.Form1_Vista2_Label1 = Label(font_size = '16sp',text = "[color=#404040]"+self.textoo , markup = True, size_hint = (1,None), height = 100)
        self.Form1_Vista2_Barra1 = Image(source=self.images + "Sponsor1.png", size_hint = (1, None), height = 75, allow_stretch = True, keep_ratio = False)
        self.Form1_Vista2_Barra2 = Image(source=self.images + "Sponsor1B.png", size_hint = (1, None), height = 25, allow_stretch = True, keep_ratio = False)
 
        self.Form1.add_widget(self.Form1_Vista2)
        
        self.All = GridLayout(cols = 1 , size_hint = (1,None), height = 200)
        self.Form1.add_widget(self.All)
        
        self.Form1_Vista2.add_widget(self.Form1_Vista2_Barra1)
        self.Form1_Vista2.add_widget(self.Form1_Vista2_Image)
        self.Form1_Vista2.add_widget(self.Form1_Vista2_Label1)
        self.Form1_Vista2.add_widget(self.Form1_Vista2_Barra2)
        
        
        for i in self.recursos:
            abcd += 1
            self.Espacio5 = Image(source=self.images + "A2.png", size_hint = (.25, 1), height = 25, allow_stretch = True, keep_ratio = False)
            self.Espacio6 = Image(source=self.images + "A4.png", size_hint = (.25, 1), height = 25, allow_stretch = True, keep_ratio = False)

            self.Form1_Vista1 = GridLayout(cols = 1 ,size_hint = (1,None), height = 635, allow_stretch = True, keep_ratio = False)
            
            self.Form1_Barra1 = Image(source=self.images + "Sponsor1.png", size_hint = (1, None), height = 70, allow_stretch = True, keep_ratio = False)
            self.Form1_Label1 = Label(text = "[color=#000000][b]#" + str(abcd),font_size = 24, markup = True, size_hint = (.30,1))
            self.Form1_Label2 = Label(text = "[color=#000000][b]", markup = True)
            self.Form1_Label3 = Label(text = "[color=#000000][b]"+i[:-4],font_size = 20, markup = True, halign = 'left')
            self.Form1_Label4 = Label(text = "[color=#000000][b]", markup = True, halign = 'left', size_hint = (1,None), height = 75)
            self.Form1_Imagen = AsyncImage(keep_ratio = True,allow_stretch = False , source = self.sources + i, size_hint = (1,None), height = 400)
            self.Form1_Barra2 = Image(source=self.images + "Sponsor2.png", size_hint = (1, None), height = 30, allow_stretch = True, keep_ratio = False)
            self.Form1_Button1 = Button(text = "[color=#404040]+",height = 50,size_hint = (1,None),background_normal = self.images + "Button2.png", markup = True )
            
            self.Form1_Label_Grid = GridLayout(cols = 2)
            self.Form1_Label_Grid2 = Label(size_hint = (1,None), height = 40)
            
            self.Form1_Label_Grid.add_widget(self.Form1_Label1)
            self.Form1_Label_Grid.add_widget(self.Form1_Label2)

            self.Form1_Vista1.add_widget(self.Form1_Label_Grid2)  
            self.Form1_Vista1.add_widget(self.Form1_Label_Grid)  
            self.Form1_Vista1.add_widget(self.Form1_Imagen)
            self.Form1_Vista1.add_widget(self.Form1_Label3)
            self.Form1_Vista1.add_widget(self.Form1_Label4)
            self.Form1_Vista1.add_widget(self.Form1_Button1)

            
            self.All.height += 635
            self.All.add_widget(self.Form1_Vista1)
            if abcd == 10:
                return



            
            
            
    def FORMULARIOS(self,a):
        for i in self.panelesformularios:
            print i
            try:
               self.root_0.remove_widget(i)
               self.root_0.add_widget(self.Form1_root) 
            except:
                pass
        
    def FORM1(self,a):
        print ("EJECUTADO")
        for i in self.panelesformularios:
            print i
            try:
               self.root_0.remove_widget(i)
               self.root_0.add_widget(self.Form1_root) 
            except:
                pass
                
    def FORM2(self,a):
        for i in self.panelesformularios:
            print i
            try:
               self.root_0.remove_widget(i)
               self.root_0.add_widget(self.Form2_root) 
            except:
                pass
        
    def FORM3(self,a):
        for i in self.panelesformularios:
            print i
            try:
               self.root_0.remove_widget(i)
               self.root_0.add_widget(self.Form3_root) 
            except:
                pass
        
    
    def actualizar_busqueda(self, a):
        patch = os.path.dirname(os.path.abspath(__file__))
        images = self.patch + '/pics/'
        print "AA"
        self.All.clear_widgets()
        self.All.height = 200
        abcd = 0

        for i in self.recursos:
            try:
                a = 0
                texto = self.Form1_TextIn.text
                #u = i.decode('utf-8', 'ignore')
                print texto + "     " + i
                
     
                i.index(texto)
                print ("ENCONTRADO")
                abcd += 1
    
                self.Espacio5 = Image(source=self.images + "A2.png", size_hint = (.25, 1), height = 25, allow_stretch = True, keep_ratio = False)
                self.Espacio6 = Image(source=self.images + "A4.png", size_hint = (.25, 1), height = 25, allow_stretch = True, keep_ratio = False)

                self.Form1_Vista1 = GridLayout(cols = 1 ,size_hint = (1,None), height = 650, allow_stretch = True, keep_ratio = False)
                
                self.Form1_Barra1 = Image(source=self.images + "Sponsor1.png", size_hint = (1, None), height = 70, allow_stretch = True, keep_ratio = False)
                self.Form1_Label1 = Label(text = "[color=#000000][b]#" + str(abcd),font_size = 24, markup = True, size_hint = (.30,1))
                self.Form1_Label2 = Label(text = "[color=#000000][b]", markup = True)
                self.Form1_Label3 = Label(text = "[color=#000000][b]"+i[:-4],font_size = 20, markup = True, halign = 'left')
                self.Form1_Label4 = Label(text = "[color=#000000][b]", markup = True, halign = 'left', size_hint = (1,None), height = 75)
                self.Form1_Imagen = AsyncImage(keep_ratio = True,allow_stretch = False , source = self.sources +  i, size_hint = (1,None), height = 400)
                self.Form1_Barra2 = Image(source=self.images + "Sponsor2.png", size_hint = (1, None), height = 30, allow_stretch = True, keep_ratio = False)
                self.Form1_Button1 = Button(text = "[color=#404040]+",height = 50,size_hint = (1,None),background_normal = self.images + "Button2.png", markup = True )
                
      


                
                self.Form1_Label_Grid = GridLayout(cols = 2)
                self.Form1_Label_Grid2 = Label(size_hint = (1,None), height = 40)
                
                self.Form1_Label_Grid.add_widget(self.Form1_Label1)
                self.Form1_Label_Grid.add_widget(self.Form1_Label2)

                #self.Form1_Vista1.add_widget(self.Form1_Barra1)
                self.Form1_Vista1.add_widget(self.Form1_Label_Grid2)  
                self.Form1_Vista1.add_widget(self.Form1_Label_Grid)  
                self.Form1_Vista1.add_widget(self.Form1_Imagen)
                self.Form1_Vista1.add_widget(self.Form1_Label3)
                self.Form1_Vista1.add_widget(self.Form1_Label4)
                self.Form1_Vista1.add_widget(self.Form1_Button1)
                #self.Form1_Vista1.add_widget(self.Form1_Barra2)
                
                
                #self.Form1.add_widget(self.Espacio5)
                self.All.add_widget(self.Form1_Vista1)
                self.All.height += 650
                print self.All.height
                #self.Form1.add_widget(self.Espacio6)
                print ("agregado")

                xcontador = 0
                self.estado_buscado = []
            except:
                print ("NO ENCONTRADO")
            print a
  

    
class MyApp(App):
    def build(self):
        return InterfaceManager()


if __name__ in ('__main__', '__android__'):
    MyApp().run()
