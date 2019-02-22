#!/usr/bin/env python
# -*- coding: latin-1 -*-

import sys  
reload(sys)  
sys.setdefaultencoding('latin-1')

from kivy.core.window import Window
from kivy.animation import Animation
from kivy.metrics import dp,sp, MetricsBase
from kivy.resources import resource_add_path
from kivy.uix.screenmanager import ScreenManager, Screen,CardTransition,SwapTransition, NoTransition,SlideTransition,FadeTransition,WipeTransition,FallOutTransition,RiseInTransition 
from kivy.uix.button import Button
from kivy.uix.relativelayout import RelativeLayout
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.image import Image,AsyncImage
from kivy.uix.scrollview import ScrollView
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.scatterlayout import ScatterLayout as Scatter
from kivy.uix.textinput import TextInput
from kivy.uix.effectwidget import EffectWidget
from kivy.uix.effectwidget import HorizontalBlurEffect,VerticalBlurEffect
import os   
import os.path


from navigator import ImageButton

resource_add_path(os.path.dirname(__file__))

from kivy.uix.behaviors import ButtonBehavior
from kivy.animation import Animation
from kivy.uix.widget import Widget
from kivy.uix.stencilview import StencilView
from kivy.clock import Clock
from kivy.properties import (ObjectProperty, NumericProperty, OptionProperty,
                             BooleanProperty, StringProperty)
from kivy.resources import resource_add_path
from kivy.lang import Builder
import os.path




C1 = "[color=#13C0C7]"
C4 = "[color=#000000]"
C2 = "[color=#404040]"
C3 = "[color=#ff3333]"
C5 = "[color=#f2f2f2]"
EC = "[/color]"
patch = os.path.dirname(os.path.abspath(__file__))
metrics = MetricsBase()
android_dpi = metrics.dpi_rounded;print android_dpi
asset_dpi = [120,160,240,320]
asset_dpi2 = ['ldpi','mdpi','hdpi','xhdpi','xxhdpi']


from kivy.config import Config
Config.set('graphics','borderless', 1)
Config.set('graphics','position','custom')
Config.set('graphics','window_state','visible')
Config.set('graphics','resizable',0)
Config.set('graphics','left',1000)
Config.set('graphics','top',35)
Window.size = (360,640)

for i in asset_dpi:
    if android_dpi == i:
        asset = patch + '/assets/drawable-'+str(asset_dpi2[asset_dpi.index(i)])+'/'


color = patch + '/colors/'
font = patch + '/fonts/'

Window.clearcolor = (1,1,1,1)

alerta_content = GridLayout(cols = 1)
alerta_content.add_widget(Button(size_hint_y = None, height = dp(50),text_size = (dp(250),dp(50)),font_size = '16sp',valign = 'top',font_name = font+"Roboto-Regular.ttf",markup = True,text = C4+"Deseas descargar el material de apoyo de esta materia?", background_normal = color + "16.png"))
alerta_content.add_widget(Button(text_size = (dp(250),dp(30)),font_size = '16sp',valign = 'top',font_name = font+"Roboto-Light.ttf",markup = True,text = C4+"Si", background_normal = color + "16.png"))
alerta_content.add_widget(Button(text_size = (dp(250),dp(30)),font_size = '16sp',valign = 'top',font_name = font+"Roboto-Light.ttf",markup = True,text = C4+"No", background_normal = color + "16.png"))
alerta0 = Popup(title_size = '20sp',title_color = [0,0,0,1], title = "Descargar Contenido",content = alerta_content, size_hint = (None,None), size = ('300dp','200dp'),
separator_color = (0,0,0,0),background = color + "16.png")

class NavigationDrawerException(Exception):
    '''Raised when add_widget or remove_widget called incorrectly on a
    NavigationDrawer.

    '''
class NavigationDrawer(StencilView):
    '''Widget taking two children, a side panel and a main panel,
    displaying them in a way that replicates the popular Android
    functionality. See module documentation for more info.

    '''

    # Internal references for side, main and image widgets
    _side_panel = ObjectProperty()
    _main_panel = ObjectProperty()
    _join_image = ObjectProperty()

    side_panel = ObjectProperty(None, allownone=True)
    '''Automatically bound to whatever widget is added as the hidden panel.'''
    main_panel = ObjectProperty(None, allownone=True)
    '''Automatically bound to whatever widget is added as the main panel.'''

    # Appearance properties
    side_panel_width = NumericProperty()
    '''The width of the hidden side panel. Defaults to the minimum of
    250dp or half the NavigationDrawer width.'''
    separator_image = StringProperty('')
    '''The path to an image that will be placed between the side and main
    panels. If set to `''`, defaults to a gradient from black to
    transparent in an appropriate direction (left->right if side panel
    above main, right->left if main panel on top).'''
    separator_image_width = NumericProperty(dp(10))
    '''The width of the separator image. Defaults to 10dp'''

    # Touch properties
    touch_accept_width = NumericProperty('14dp')
    '''Distance from the left of the NavigationDrawer in which to grab the
    touch and allow revealing of the hidden panel.'''
    _touch = ObjectProperty(None, allownone=True)  # The currently active touch

    # Animation properties
    state = OptionProperty('closed', options=('open', 'closed'))
    '''Specifies the state of the widget. Must be one of 'open' or
    'closed'. Setting its value automatically jumps to the relevant state,
    or users may use the anim_to_state() method to animate the
    transition.'''
    anim_time = NumericProperty(0.3)
    '''The time taken for the panel to slide to the open/closed state when
    released or manually animated with anim_to_state.'''
    min_dist_to_open = NumericProperty(0.7)
    '''Must be between 0 and 1. Specifies the fraction of the hidden panel
    width beyond which the NavigationDrawer will relax to open state when
    released. Defaults to 0.7.'''
    _anim_progress = NumericProperty(0)  # Internal state controlling
                                         # widget positions
    _anim_init_progress = NumericProperty(0)

    # Animation controls
    top_panel = OptionProperty('main', options=['main', 'side'])
    '''Denotes which panel should be drawn on top of the other. Must be
    one of 'main' or 'side'. Defaults to 'main'.'''
    _main_above = BooleanProperty(True)

    side_panel_init_offset = NumericProperty(0.5)
    '''Intial offset (to the left of the widget) of the side panel, in
    units of its total width. Opening the panel moves it smoothly to its
    final position at the left of the screen.'''

    side_panel_darkness = NumericProperty(0.8)
    '''Controls the fade-to-black of the side panel in its hidden
    state. Must be between 0 (no fading) and 1 (fades to totally
    black).'''

    side_panel_opacity = NumericProperty(1)
    '''Controls the opacity of the side panel in its hidden state. Must be
    between 0 (fade to transparent) and 1 (no transparency)'''

    main_panel_final_offset = NumericProperty(1)
    '''Final offset (to the right of the normal position) of the main
    panel, in units of the side panel width.'''

    main_panel_darkness = NumericProperty(0)
    '''Controls the fade-to-black of the main panel when the side panel is
    in its hidden state. Must be between 0 (no fading) and 1 (fades to
    totally black).
    '''

    opening_transition = StringProperty('out_cubic')
    '''The name of the animation transition type to use when animating to
    an open state. Defaults to 'out_cubic'.'''

    closing_transition = StringProperty('in_cubic')
    '''The name of the animation transition type to use when animating to
    a closed state. Defaults to 'out_cubic'.'''

    anim_type = OptionProperty('reveal_from_below',
                               options=['slide_above_anim',
                                        'slide_above_simple',
                                        'fade_in',
                                        'reveal_below_anim',
                                        'reveal_below_simple',
                                        ])
    '''The default animation type to use. Several options are available,
    modifying all possibly animation properties including darkness,
    opacity, movement and draw height. Users may also (and are
    encouaged to) edit these properties individually, for a vastly
    larger range of possible animations. Defaults to reveal_below_anim.
    '''

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
class ImageButton(ButtonBehavior, Image):
    pass
class InterfaceManager(RelativeLayout):
    def __init__(self, **kwargs):
        
        super(InterfaceManager, self).__init__(**kwargs)
        self.state0 = -1
        self.state1 = -1
        self.state2 = -1
        self.state3 = -1

        
        self.navigatorwid = NavigationDrawer()
        self.navbar = RelativeLayout()
        self.navbar.add_widget(Image(size_hint = (None,None), size = (1000,1000),source = "16.png", keep_ratio = False, allow_stretch = True))
        self.navbar_parent = GridLayout(cols = 3)
        self.navbar.add_widget(self.navbar_parent)
        self.navbar_parent.add_widget(Label(size_hint_y = None , height = dp(49), size_hint_x = None, width = '25dp'))
        self.navbar_parent.add_widget(Label(size_hint_y = None , height = dp(49), size_hint_x = None, width = '25dp'))
        self.navbar_parent.add_widget(Label(size_hint_y = None , height = dp(49)))

        self.navigatorwid.add_widget(self.navbar)
        buttons = ["Inicio","Recientes","Papelera","Leer Mas Tarde","Continuar ..."]
        buttons_img = ["home.png","history-button.png","garbage.png","heart.png","continuous-line-clock.png"]

        for i in range(5): 
           
            self.navbar_parent.add_widget(Label(size_hint_y = None , height = dp(49), size_hint_x = None, width = '25dp'))
            self.navbar_parent.add_widget(Image(size_hint_x = None,size_hint_y = None , height = '60dp', width ='25dp', source = asset + buttons_img[i]))
            button3 =Button(size_hint_x = None, width = dp(130),valign = "middle",text_size = (dp(90),dp(60)),font_name = font + "Roboto-regular.ttf",markup = True,font_size = '14sp',background_normal = color+"16.png",text = C4+buttons[i],size_hint_y = None, height = dp(60))

            if i == 0:button3.bind(on_release = lambda x: self.choose("1"))
            elif i == 1:button3.bind(on_release = lambda x: self.choose("1"))
            elif i == 2:button3.bind(on_release = lambda x: self.choose("1"))
            elif i == 3:button3.bind(on_release = lambda x: self.choose("4"))
            elif i == 4:button3.bind(on_release = lambda x: self.choose("1"))
            self.navbar_parent.add_widget(button3)
            
            
        self.add_widget(self.navigatorwid)  

        w = EffectWidget()
        
        self.main = ScreenManager() ;self.navigatorwid.add_widget(w)
        
        w.add_widget(self.main)
        #w.effects = [HorizontalBlurEffect(size=3.0),VerticalBlurEffect(size=3.0)]
        
        self.add_widget(Button(text_size = (dp(100),dp(20)), valign = "middle", halign = "center",font_name = font + "Roboto-Light.ttf", font_size = '17sp',text = C4 + "Inicio",markup = True,pos = (0,Window.height - dp(60)), size_hint = (1,None), height = dp(60), background_normal = asset + "Repeat Grid 8.png", keep_ratio = False, allow_stretch = True))
        self.add_widget(ImageButton(on_release = lambda x: self.navigatorwid.toggle_state(),pos = (0,Window.height - dp(49)), size_hint = (None,None),width = dp(49), height = dp(49), source = asset + "Group 55.png"))
        self.add_widget(ImageButton(source = asset+"Group 33.png",size_hint = (None,None), pos_hint = {'center_x': .15,'center_y': .15}))
        self.mainmenu = RelativeLayout(cols = 1, pos = (0,'-350dp'), height = '400dp', size_hint_y = None) ;# self.add_widget(self.mainmenu)
        self.mainmenu_backgroundcolor = Image(y = dp(-50),source = color + "16.png", keep_ratio = False, allow_stretch = True);self.mainmenu.add_widget(self.mainmenu_backgroundcolor)
        self.screen1()
        self.screen2()
        self.screen3()
        self.screen4()
        button0_parent = RelativeLayout(size_hint_y = None , height = '50dp')
        #self.button0 = ImageButton(size_hint = (1,1),width = '31dp' ,height = '7dp', source = asset + "Group 54.png")
        

        mainmenu_parent = GridLayout(cols = 1);  self.mainmenu.add_widget(mainmenu_parent)
        imagebutton0 = ImageButton(keep_ratio = False, allow_stretch = True,size_hint = (1,None) ,height = '50dp', source = asset + "Repeat Grid 17.png",)
        button0_parent.add_widget(imagebutton0)
        #button0_parent.add_widget(self.button0)
        imagebutton0.bind(on_release = lambda x: self.Openmainmenu())
        mainmenu_scroll = ScrollView()
        mainmenu_parent.add_widget(button0_parent) 
        mainmenu_parent.add_widget(Image(source = color + "16bb.png", size_hint_y = None, height = 1, keep_ratio = False, allow_stretch = True)) 
        mainmenu_parent.add_widget(mainmenu_scroll)
        mainmenu_scrollparent1 = GridLayout(cols = 2, size_hint_y = None, height = 150) ; mainmenu_scroll.add_widget(mainmenu_scrollparent1)
        
        
        Unidades = ["Funciones","Variables","Constantes","Clases","Que es Lambda"]
        #Agregar Buscador
        mainmenu_scrollparent1.add_widget(Button(size_hint_x = None,font_size = '40sp',size_hint_y = None , height = '90dp', font_name = font + "Bevan.ttf", width = '75dp', background_normal = color + "None.png", text = "[color=#000000]", markup = True ))
        mainmenu_scrollparent1.add_widget(Button(font_size = '12sp',markup = True,font_name = font+"Roboto-Regular.ttf",text = C4+"[size=20sp]"+"Buscador"+"[/size]\nTocar para abrir Buscador.",background_normal = color + "None.png",size_hint_y = None , height = '75dp', line_height = 1.4, text_size = (Window.width - dp(75),dp(75)),halign='left', valign = 'middle'))
        
        x = 1
        for i in Unidades: #Agregar Unidad
            if Unidades.index(i) % 2 == 1: background = color + "16.png"
            if Unidades.index(i) % 2 == 0: background = color + "16bb.png"
            mainmenu_scrollparent1.add_widget(Button(size_hint_x = None,font_size = '40sp',size_hint_y = None , height = '75dp', font_name = font + "Bevan.ttf", width = '75dp', background_normal = background, text = "[color=#000000]i", markup = True ))
            mainmenu_scrollparent1.add_widget(Button(font_size = '12sp',markup = True,font_name = font+"Roboto-Regular.ttf",text = C4+"[size=20sp]"+i+"[/size]\n[color=#000000]Tocar para ver contenido.",background_normal = background,size_hint_y = None , height = '75dp', line_height = 1.4, text_size = (Window.width - dp(75),dp(75)),halign='left', valign = 'middle'))
            mainmenu_scrollparent1.height += dp(90) 
        

        
        
    def favorito(self,button):
        self.state2 *= -1
        if self.state2 == 1:
            x_anim = Animation(opacity = 1., d = .10)
            x_anim.start(button)
            print 0
        else:
            x_anim = Animation(opacity = 0., d = .10)
            x_anim.start(button)
            pass
    def sumpos(self,x):
        listadepos = []
        for i in x: listadepos.append([i[0],i[1]])
        newpos = [-100,-100]
        for i in listadepos:
            print i
            newpos[0] += i[0]
            newpos[1] += i[1]
        print (newpos[0],newpos[1])
        return (newpos[0],newpos[1])
    def newpos(self): self.boxwidget_parent.pos = (0,0)
    def positate(self,x):
        self.state1 *= -1
        if self.state1 == 1:
            self.boxwidget_parent.pos = self.sumpos([x.parent.parent.parent.pos,x.parent.parent.pos,x.pos])
            #self.boxwidget.current = self.boxwidget.next()
            #print self.boxwidget.current
            self.boxwidget_parent.scale = .9
            self.boxwidget_parent.opacity = 0
            x_anim = Animation(scale = 1., opacity = 1., d = .15)
            x_anim.start(self.boxwidget_parent)
        else:
            
            x_anim = Animation(scale = .9, opacity = .0, d = .15)
            x_anim.bind(on_complete = lambda x,y:self.newpos())
            x_anim.start(self.boxwidget_parent)
            
            #self.boxwidget.current = self.boxwidget.next()
            #print self.boxwidget.current
            
    
    
    def next(self): self.main.current = self.main.next()
    def back(self): self.main.current = self.main.previous()
    def choose(self,str): self.main.current = str; print str
    
    
    def Openmainmenu(self):
        self.state0 *= -1
        
        if self.state0 == 1 : A1 = Animation(pos = (0,0)); opac = .2
        else: A1 = Animation(pos = (0,dp(-350))) ; opac = 1
        
        A1.start(self.mainmenu)
        #with self.button0.canvas:
        #    A2 = Animation(opacity = opac )
        #    A2.start(self.button0)
        
        
    def screen1(self):

        screen = Screen(name = "1")
        screen_parent = GridLayout(cols = 1) ; screen.add_widget(screen_parent)
        a = Label(size_hint_y = None , height = '50dp')  
        b = RelativeLayout()
        b_backgroundcolor = Image(y = dp(-50),source = color + "16.png", keep_ratio = False, allow_stretch = True);b.add_widget(b_backgroundcolor)
        screen_parent.add_widget(a)
        screen_parent.add_widget(b)
        
        self.main.add_widget(screen)
        
        
        
        
        b_scrollview = ScrollView();b.add_widget(b_scrollview)

        b_parent = GridLayout(cols = 1,spacing = 15,size_hint_y = None, height = '250dp');b_scrollview.add_widget(b_parent)
        b_parentsearcher = Image(source = color + "None.png", keep_ratio = False, allow_stretch = True)
        b_parentsearcherparent = RelativeLayout(opacity = 0.,size_hint_y = None, height = 0); #b_parentsearcherparent.add_widget(b_parentsearcher)
        
        b_parentsearcherparent_dim1 = GridLayout(rows = 1, pos = (0,-20))
        
       
        b_parentsearcherparent_dim1.add_widget(Label(size_hint_x = None , width = '25dp'))
        b_parentsearcherparent_dim1.add_widget(Image(size_hint_x = None , width = '47dp' , source = asset+"ic_search.png"))
        b_parentsearcherparent_dim1.add_widget(TextInput(size_hint_x = 1,text = "Busca tu materia! :D",cursor_color = (0,0,0,.5),font_name = font + "Roboto-Light.ttf",padding = [dp(20),dp(40),0,0],multiline = False,font_size = '20dp',  background_normal = color + "None.png", background_active = color + "None.png"))
        #b_parentsearcherparent_dim1.add_widget(Image(size_hint_x = None , width = '1dp' ,keep_ratio = False, allow_stretch = True, source = color+"17b.png"))
        #b_parentsearcherparent_dim1.add_widget(Label(size_hint_x = None , width = '25dp'))
        #b_parentsearcherparent_dim1.add_widget(Label())
        
        b_parentsearcherparent.add_widget(b_parentsearcherparent_dim1)
        
        b_parent.add_widget(b_parentsearcherparent)   
        self.boxwidget_parent = Scatter(size_hint = (None,None), size = (dp(150),dp(150))); 
        self.boxwidget = RelativeLayout(); 
        self.boxscreen1 = Screen(name = "b1");self.boxwidget.add_widget(Image(source = asset + "Repeat Grid 11.png", keep_ratio = False, allow_stretch = True))
        def saludar(): 
            print str(b_scrollview.scroll_y)[:3]
            x_anim2 = Animation(height = dp(100), d = .15)
            x_anim1 = Animation(opacity = 1., d = .5)
            x_anim = x_anim2 + x_anim1
            if (b_scrollview.scroll_y > 1.3) and (self.state3 == -1): 
                self.state3 *= -1
                def desactivar(): self.state3 *= -1;print self.state3
                x_anim.bind(on_complete = lambda x,y:desactivar())
                x_anim.start(b_parentsearcherparent)
                
            
        b_scrollview.bind(on_scroll_stop = lambda x,y: saludar())
        #self.boxscreen2 = Screen(name = "b2"); self.boxwidget.add_widget(self.boxscreen2)
        #self.boxscreen2.add_widget(Image(source = "None.png", keep_ratio = False, allow_stretch = True))
        self.boxwidget_parent.add_widget(self.boxwidget)
        #self.boxwidget.add_widget(self.boxscreen1)
        self.boxwidgetparent = GridLayout(cols = 1);self.boxwidget.add_widget(self.boxwidgetparent)
        self.boxwidgetparent.add_widget(Button(text_size = (dp(100),dp(30)),background_normal = color +"None.png", text = C4+ "Abrir", markup = True))
        self.boxwidgetparent.add_widget(Button(text_size = (dp(100),dp(30)),background_normal = color +"None.png", text = C4+ "Eliminar", markup = True))
        self.boxwidgetparent.add_widget(Button(text_size = (dp(100),dp(30)),background_normal = color +"None.png", text = C4+ "Cerrar", markup = True))
        self.boxwidgetparent.add_widget(Label(size_hint_y = None , height = 17))
        
        Materias = [C4+"[size=21sp][font="+font+"Roboto-Medium]Agregar una Materia[/font][/size]\n@Profesor",
                    C4+"[size=21sp][font="+font+"Roboto-Medium]Logica de Programacion[/font][/size]\nLorenzo",
                    C4+"[size=21sp][font="+font+"Roboto-Medium]Fundamentos de Programacion[/font][/size]\nHirujo",
                    C4+"[size=21sp][font="+font+"Roboto-Medium]Integrales[/font][/size]\nSegura",
                    ]
        for i in Materias:
            if Materias.index(i) == 0: img = asset + "Repeat Grid 12.png"
            else : img = asset + "Repeat Grid 11.png"
            button_text = i
            buttonparent = RelativeLayout(size_hint = (1,None), height = '150dp')
            button = Button(pos_hint = {'center_x':.5}, background_normal = img,background_color = [1,1,1,1],border = [0,0,0,0],font_size = '17sp',valign = "middle",size_hint_x = None, height = '150dp', width = '300dp',font_name = font+"Roboto-Light.ttf",text_size = (dp(215),dp(125)),line_height = 1.5,markup = True, text = button_text,size_hint_y = None ) 
            button.bind(on_release = lambda x:self.next())
            button_grid = RelativeLayout(pos_hint = {'center_x':.5},background_color = [1,1,1,1],border = [0,0,0,0],font_size = '17sp',valign = "middle",size_hint_x = None, height = '150dp', width = '360dp',font_name = font+"Roboto-Light.ttf",text_size = (dp(275),dp(125)),line_height = 1.5,markup = True, text = button_text,size_hint_y = None , background_normal = img) 
            button_grid.add_widget(button)
            buttonparent.add_widget(button_grid)
            buttonchilds = GridLayout(rows = 1,pos_hint = {'center_x':.65, 'center_y': .2},size_hint = (None,None), size = (dp(150),'50dp'))
            
            dimbutton = RelativeLayout()

            
            button1 = Button(background_normal = asset + "Group 58.png");dimbutton.add_widget(button1)
            self.button2 = Button(background_down = asset + "Group 59.png",opacity = 0.,background_normal = asset + "Group 59.png");dimbutton.add_widget(self.button2)
            self.button2.bind(on_release = lambda x: self.favorito(x))
            buttonchilds.add_widget(dimbutton)
            
            este0 = Button(background_normal = asset + "Group 56.png")
            este0.bind(on_release = lambda x: alerta0.open())
            buttonchilds.add_widget(este0)
            este = Button(background_normal = asset + "Group 57.png",background_down = asset + "Group 57.png")
            este.bind(on_release = lambda x:self.positate(x))
            buttonchilds.add_widget(este)
            button_grid.add_widget(buttonchilds)
            
            b_parent.add_widget(buttonparent)
            
            b_parent.height += dp(150) 
            if i == 0: pass
            else:
                pass
        b_parent.add_widget(self.boxwidget_parent)
            
    def screen2(self):
        screen2 = Screen(name = "2"); self.main.add_widget(screen2)
        screen2_scrollview = ScrollView();screen2.add_widget(screen2_scrollview)
        screen2_parent = GridLayout(height = dp(250),cols = 1, size_hint_y = None); screen2_scrollview.add_widget(screen2_parent)
        title_text = "[size=30sp][color=#000000]Unidad[/color][/size]\n"+C4+"contenido"
        title = Button(font_name = font + "Roboto-Regular.ttf",valign = "top",text_size = (Window.width-50, dp(80)),markup = True,background_normal = asset + 'Repeat Grid 8.png',font_size = '20sp',size_hint_y = None, height = '100dp', text = title_text)
        
        
        a = RelativeLayout(size_hint_y = None , height = '60dp'); screen2_parent.add_widget(a) 
        #screen2_parent.add_widget(Button(font_size = '17sp',valign = "middle",font_name = font+"Roboto-Light.ttf",text_size = (dp(Window.width-50)-dp(65),dp(125)),line_height = 1.5,markup = True, text = (C4+"[size=21sp][font="+font+"Roboto-Medium]Logica de Programacion[/font][/size]\nLorenzo"),size_hint_y = None , height = '150dp', background_normal = asset + "Repeat Grid 12.png"))
        
        button_text = C4+"[size=21sp][font="+font+"Roboto-Medium]Agregar una Materia[/font][/size]\n@Profesor"
        buttonparent = RelativeLayout(size_hint = (1,None), height = '150dp')
        button = Button(font_size = '17sp',valign = "middle",font_name = font+"Roboto-Light.ttf",text_size = (dp(300),dp(125)),line_height = 1.5,markup = True, text = button_text,size_hint_y = None , height = '150dp', background_normal = asset + "Repeat Grid 12.png") 
        button.bind(on_release = lambda x:self.next())
        buttonparent.add_widget(button)
        buttonchilds = GridLayout(rows = 1,pos_hint = {'center_x':.7, 'center_y': .2},size_hint = (None,None), size = ('150dp','50dp'))
        
        dimbutton = RelativeLayout()

        
        button1 = Button(background_normal = asset + "Group 58.png");dimbutton.add_widget(button1)
        self.button2 = Button(background_down = asset + "Group 59.png",opacity = 0.,background_normal = asset + "Group 59.png");dimbutton.add_widget(self.button2)
        self.button2.bind(on_release = lambda x: self.favorito(x))
        buttonchilds.add_widget(dimbutton)
        
        este0 = Button(background_normal = asset + "Group 56.png")
        este0.bind(on_release = lambda x: alerta0.open())
        buttonchilds.add_widget(este0)
        este = Button(background_normal = asset + "Group 57.png")
        este.bind(on_release = lambda x:self.positate(x))
        buttonchilds.add_widget(este)
        buttonparent.add_widget(buttonchilds)
        
        screen2_parent.add_widget(buttonparent)
        #screen2_parent.add_widget(title)
        
        for i in range(4):
            button_text = C4+"Unidad "+str(i)+"\n[size=18sp][font="+font+"Roboto-medium.ttf]Experiencias Geniales"; screen2_parent.height += dp(125)
            button = Button(font_name = font+"Roboto-Light.ttf",valign = 'middle',text_size = (Window.width-50, dp(125)),font_size = '25sp',markup = True,background_normal = color + '16.png',text = button_text,size_hint_y = None, height = '125sp')
            button.bind(on_release = lambda x: self.next())
            screen2_parent.add_widget(button)
            screen2_parent.add_widget(Image(source = color + "16b.png", size_hint_y = None, height = 1 , keep_ratio = False, allow_stretch = True))
        
    def screen3(self):
        screen3 = Screen(name = "3"); self.main.add_widget(screen3)
        screen3_scrollview = ScrollView(); screen3.add_widget(screen3_scrollview)
        screen3_parent = GridLayout(cols = 1,size_hint_x = None , width = dp(500), size_hint_y = None , height = dp(300)); screen3_scrollview.add_widget(screen3_parent)
        a = RelativeLayout(size_hint_y = None , height = '60dp'); screen3_parent.add_widget(a) 
        button_text = C4+"Unidad "+str(1)+"\n[size=18sp][font="+font+"Roboto-medium.ttf]Experiencias Geniales"; 
        screen3_parent.add_widget(Button(font_name = font+"Roboto-Light.ttf",valign = 'middle',text_size = (dp(450), dp(125)),font_size = '25sp',markup = True,background_normal = color + '16.png',text = button_text,size_hint_y = None, height = '125sp'))
    
        screen3_parent.add_widget(Image(source = color + "16bb.png",keep_ratio = False, allow_stretch = True , size_hint_y = None, height = 1))
        
        parrafo1 = C4+"Solo mira la hermoza imagen que estoy probando lindo, puede ser realmente letal :v"
        

        Unidad = [["t","[color=#0066ff]"+"Titulo del Concepto"],
                  ["p",parrafo1],
                  ["i",asset + "Group 47.png"],
                  ["p",parrafo1],
                  ["t","[color=#0066ff]"+"Titulo del Concepto"],
                  ["p",parrafo1],
                  ]
        #f_unidades = []
        #with open('U1.txt') as f:
        #    for line in f:
        #        exec("f_unidades.append("+line+")")
        #for i in f_unidades: print i
        
     
        for i in Unidad:
            if i[0] == "p":widget = Button(height = dp(len(i[1])*.50),size_hint_y = None,valign = 'top',text_size = (dp(450),None),font_size = '16sp',markup = True,text = C4+i[1] , background_normal = color + "16.png")
            elif i[0] == "i":widget = Image(size_hint = (1,None), source = i[1])  
            elif i[0] == "t":widget = Button(height = dp(30),size_hint_y = None,font_name = font + "Roboto-medium.ttf",valign = 'top',text_size = (dp(450),None),font_size = '20sp',markup = True,text = str(i[1]) , background_normal = color + "16.png")
            screen3_parent.add_widget(widget)
            
            if i[0] == "p":screen3_parent.height += dp(len(i[1]))
            elif i[0] == "i": screen3_parent.height += widget.texture_size[1]
            elif i[0] == "t": screen3_parent.height += dp(30)
            
    def screen4(self):
        screen4 = Screen(name = "4"); self.main.add_widget(screen4)
        screen4.add_widget(Image(source = color + "16.png", keep_ratio = False, allow_stretch = True))
        screen4scrollparent = ScrollView(); screen4.add_widget(screen4scrollparent)
        screen4scrollchid0 = GridLayout(cols = 1,size_hint_y = None, height = 1000);screen4scrollparent.add_widget(screen4scrollchid0)
        
        a = RelativeLayout(size_hint_y = None , height = '60dp'); screen4scrollchid0.add_widget(a) 
        screen4scrollchid0.add_widget(Image(size_hint_y = None, height = '100dp', source = color + "16.png")) 
        screen4scrollchid0.add_widget(Image(size_hint_y = None, height = '50dp', source = asset + "Repeat Grid 18.png")) 
        screen4scrollchid0.add_widget(Image(size_hint_y = None, height = '65dp', source = color + "16.png")) 
        screen4scrollchid0.add_widget(Button(text = "Esta Semana",font_size = '17sp',background_normal = asset + "Repeat Grid 12.png",size_hint_y = None ,height = '60dp')) 

        for i in range(2):
            button_text = C4+"[size=21sp][font="+font+"Roboto-Medium]Unidad 9[/font][/size]\nLogica de Programacion"
           
            buttonparent = RelativeLayout(size_hint = (1,None), height = '150dp')
            button = Button(font_size = '17sp',valign = "middle",font_name = font+"Roboto-Light.ttf",text_size = (dp(300),dp(125)),line_height = 1.5,markup = True, text = button_text,size_hint_y = None , height = '150dp', background_normal = asset + "Repeat Grid 11.png") 
            button.bind(on_release = lambda x:self.next())
            buttonparent.add_widget(button)
            buttonchilds = GridLayout(rows = 1,pos_hint = {'center_x':.7, 'center_y': .2},size_hint = (None,None), size = ('150dp','50dp'))
            
            dimbutton = RelativeLayout()

            
            button1 = Button(background_normal = asset + "Group 58.png");dimbutton.add_widget(button1)
            self.button2 = Button(background_down = asset + "Group 59.png",opacity = 0.,background_normal = asset + "Group 59.png");dimbutton.add_widget(self.button2)
            self.button2.bind(on_release = lambda x: self.favorito(x))
            buttonchilds.add_widget(dimbutton)
            
            este0 = Button(background_normal = asset + "Group 56.png")
            este0.bind(on_release = lambda x: alerta0.open())
            buttonchilds.add_widget(este0)
            este = Button(background_normal = asset + "Group 57.png")
            este.bind(on_release = lambda x:self.positate(x))
            buttonchilds.add_widget(este)
            buttonparent.add_widget(buttonchilds)
            
            screen4scrollchid0.add_widget(buttonparent)
            
        screen4scrollchid0.add_widget(Button(text = "Semana Pasada",font_size = '17sp'  ,background_normal = asset + "Repeat Grid 12.png",size_hint_y = None ,height = '60dp')) 
        for i in range(2):
            button_text = C4+"[size=21sp][font="+font+"Roboto-Medium]Unidad 4[/font][/size]\nSociedad y Cultura"
            
           
            buttonparent = RelativeLayout(size_hint = (1,None), height = '150dp')
            button = Button(font_size = '17sp',valign = "middle",font_name = font+"Roboto-Light.ttf",text_size = (dp(300),dp(125)),line_height = 1.5,markup = True, text = button_text,size_hint_y = None , height = '150dp', background_normal = asset + "Repeat Grid 11.png") 
            button.bind(on_release = lambda x:self.next())
            buttonparent.add_widget(button)
            buttonchilds = GridLayout(rows = 1,pos_hint = {'center_x':.7, 'center_y': .2},size_hint = (None,None), size = ('150dp','50dp'))
            buttonchilds.add_widget(Label())
            dimbutton = RelativeLayout()

            
            button1 = Button(background_normal = asset + "Group 58.png");dimbutton.add_widget(button1)
            self.button2 = Button(background_down = asset + "Group 59.png", size_hint_x = None, width = "50dp",opacity = 0.,background_normal = asset + "Group 59.png");dimbutton.add_widget(self.button2)
            self.button2.bind(on_release = lambda x: self.favorito(x))
            buttonchilds.add_widget(dimbutton)

            este0 = Button(background_normal = asset + "Group 56.png", size_hint_x = None, width = "50dp")
            este0.bind(on_release = lambda x: alerta0.open())
            buttonchilds.add_widget(este0)
            este = Button(background_normal = asset + "Group 57.png", size_hint_x = None, width = "50dp")
            este.bind(on_release = lambda x:self.positate(x))
            buttonchilds.add_widget(este)

            buttonparent.add_widget(buttonchilds)
            buttonchilds.add_widget(Label())
            screen4scrollchid0.add_widget(buttonparent)
        
        
        
            
        
        
        
class MyApp(App):
    def build(self):
        return InterfaceManager()
 

if __name__ in ('__main__', '__android__'):
    MyApp().run()

    
    
    
    
    