from kivy.uix.stencilview import StencilView
from kivy.properties import (ObjectProperty, NumericProperty, OptionProperty, BooleanProperty, StringProperty)
from kivy.lang import Builder

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
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.checkbox import CheckBox
from kivy.uix.scatterlayout import ScatterLayout as Scatter
from kivy.uix.textinput import TextInput
from kivy.graphics import Color, Line, Rectangle
from kivy.uix.behaviors import ButtonBehavior
from kivy.animation import Animation
from kivy.uix.widget import Widget
from kivy.metrics import dp
from kivy.clock import Clock
from kivy.resources import resource_add_path
import os
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

Builder.load_string('''
<NavigationDrawer>:
    size_hint: (1,1)
    _side_panel: sidepanel
    _main_panel: mainpanel
    _join_image: joinimage
    side_panel_width: min(0.75*self.width, 0.75*self.width)
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
class ImageButton(ButtonBehavior,Image):pass
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

class TopNavigationS(RelativeLayout):
    def __init__(self, **kwargs):
        super(TopNavigationS, self).__init__(**kwargs)
        self.size_hint_y = None 
        self.height = '79dp'
        background = Image(opacity= 0.,source = color + "16.png", keep_ratio = False, allow_stretch = True)
        parent = GridLayout(rows = 1)
        self.parent_child = GridLayout(rows = 1, padding = [12,6,12,10])
        self.search_parent = RelativeLayout(size_hint_x = None, width = dp(55))
        self.search_parent_grid = GridLayout(rows = 1, padding = [0,6,0,10]);self.search_parent.add_widget(self.search_parent_grid)
        
        self.Img = ImageButton(on_release = lambda x: self.bar_animate(),source = asset + "Group 569.png",size_hint = (None,None), size = ('55dp','55dp'))
        self.Img_parent = Scatter(do_translation_y=False, size_hint = (None,None), size = (dp(55),dp(55)))
        self.Img_parent_parent = RelativeLayout(size_hint = (None,1), width = dp(55))
        self.Img_parent.add_widget(self.Img)
        self.Img_parent_parent.add_widget(self.Img_parent)
        
        
        self.parent_child.add_widget(self.Img_parent_parent)
        self.parent_child.add_widget(Label(halign = 'left',valign = 'bottom',text_size = (Window.width - dp(110) - 50,dp(30)),markup = True,text = C4+"Page Title",font_name = font + "Roboto-Medium.ttf" ,font_size = '20sp'))
        self.Img1 = ImageButton(size_hint = (None,1), size = ('55dp','55dp'),source = asset + "Group 570.png", on_release = lambda x: self.search_animate())
        self.search_parent_grid.add_widget(self.Img1)
        self.TextInput0 =TextInput(hint_text_color = (0,0,0,.91),cursor_color = (0,0,0,.91),foreground_color = [0,0,0,.91],padding = [5,27,0,0],hint_text = "Buscar lugares y personas",font_size = '16sp',background_normal = color + "None.png",background_active = color + "None.png", multiline = False)
        self.search_parent_grid.add_widget(self.TextInput0)
        
        parent.add_widget(self.parent_child)
        parent.add_widget(self.search_parent)
        
        
        
        #self.add_widget(background)    
        self.add_widget(parent)
    def leftbutton(self): return self.Img
    def rightbutton(self): return self.Img1
    def textinput(self): return self.TextInput0
        
    def bar_animate(self):

        animate_d = .5
        if self.Img_parent.rotation == 360:
            animate_anim = Animation(rotation = 0, d = animate_d, t = 'in_out_quart')
            animate_anim1 = Animation(opacity = 1 , d = animate_d/2., t = 'in_out_quart')
            animate_anim2 = Animation(opacity = 1 , d = animate_d/2., t = 'in_out_quart')
            def ch(): 
                if self.Img.source == asset + "Group 568.png":
                    self.Img.source = asset + "Group 569.png"
                else:
                    self.Img.source = asset + "Group 568.png"
            animate_anim1.bind(on_complete= lambda x,y: ch())
            animate_anim2 = animate_anim1 + animate_anim2
            animate_anim.start(self.Img_parent)
            animate_anim2.start(self.Img_parent)
        elif self.Img_parent.rotation == 0:
            animate_anim = Animation(rotation = 360, d = animate_d, t = 'in_out_quart')
            animate_anim1 = Animation(opacity = 1 , d = animate_d/2., t = 'in_out_quart')
            animate_anim2 = Animation(opacity = 1 , d = animate_d/2., t = 'in_out_quart')
            def ch(): 
                if self.Img.source == asset + "Group 568.png":
                    self.Img.source = asset + "Group 569.png"
                else:
                    self.Img.source = asset + "Group 568.png"
            animate_anim1.bind(on_complete= lambda x,y: ch())
            animate_anim2 = animate_anim1 + animate_anim2
            animate_anim.start(self.Img_parent)
            animate_anim2.start(self.Img_parent)
        #animate_anim1.start(self.Img_parent)
    def search_animate(self):
        animate_d = .5
        if self.search_parent.width == dp(55):
            animate_anim = Animation(width = Window.width, d = animate_d, t = 'in_out_quart')
            animate_anim1 = Animation(opacity = 0., d = animate_d, t = 'in_out_quart')
            animate_anim2 = Animation(padding = [12,6,12,10], d = animate_d, t = 'in_out_quart')
            animate_anim1.start(self.parent_child)
            animate_anim.start(self.search_parent)
            animate_anim2.start(self.search_parent_grid)
        else:
            animate_anim = Animation(width = dp(55), d = animate_d, t = 'in_out_quart')
            animate_anim1 = Animation(opacity = 1., d = animate_d, t = 'in_out_quart')
            animate_anim2 = Animation(padding = [0,6,0,10], d = animate_d/2, t = 'in_out_quart')
            animate_anim.start(self.search_parent)
            animate_anim2.start(self.search_parent_grid)
            #animate_anim.bind(on_complete = lambda x,y:animate_anim1.start(self.parent_child))
            animate_anim1.start(self.parent_child)
        
    def funcion(self):
        print("hola")

class BottomNavigation(RelativeLayout):
    def __init__(self, **kwargs):
        super(BottomNavigation, self).__init__(**kwargs)
        
        self.size_hint_y = None
        self.height = '56dp'
        self.background = Image(source = color + "3.png", keep_ratio = False, allow_stretch = True)
        self.add_widget(self.background)
        self.colors_manager = ScreenManager()
        parent = GridLayout(rows = 1)
        self.colors_manager.transition = FadeTransition(duration = .25)
     
        #eTransition,FadeTransition,WipeTransition,FallOutTransition,NoTransition ,RiseInTransition 
  
        colors = ["3","2","15","10"]
        text =  ["Inicio", "Agenda", "Libros", "Tareas"]
        img =  ["ic_alarm_black_24px", "ic_bookmark_border_black_24px", "ic_class_black_24px", "ic_copyright_black_24px"]
        for i in range(4):
            color_screen = Screen(name = str(i))
            color_screen.add_widget(Image(source = color + colors[i] + ".png", keep_ratio = False, allow_stretch = True))
            self.colors_manager.add_widget(color_screen)
            
        for i in range(4):
            if i == 1:
                button_parent = GridLayout(size_hint_x = None, width = '96dp',cols = 1, padding = [12,6,12,10])
                button_label = Label(size_hint_y = None, height = '14sp',font = font + "Roboto-Regular.ttf",font_size = '14sp',text = text[i], markup = True, halign = 'center', valign = 'bottom')
                
                button_parent.add_widget(Label())
                button_parent.add_widget(ImageButton(on_release = lambda x: self.animate(x.parent.children[0]),size_hint = (1,None), size = (dp(24),dp(24)), source = asset + img[i] +".png", keep_ratio = False, allow_stretch = False))
                button_parent.add_widget(button_label)
                parent.add_widget(button_parent)
            else:
                button_parent = GridLayout(size_hint_x = None, width = '96dp',cols = 1, padding = [12,6,12,10])
                button_label = Label(opacity = 0.,size_hint_y = None,height= 0, font = font + "Roboto-Regular.ttf",font_size = '14sp',text = text[i], markup = True, halign = 'center', valign = 'bottom')
                
                button_parent.add_widget(Label())
                button_parent.add_widget(ImageButton(on_release = lambda x: self.animate(x.parent.children[0]),size_hint = (1,None), size = (dp(24),dp(24)), source = asset + img[i] +".png", keep_ratio = False, allow_stretch = False))
                button_parent.add_widget(button_label)
                parent.add_widget(button_parent)
        
        
        self.add_widget(self.colors_manager)
        self.add_widget(parent)
        
    def animate(self,x):
        animate_anim = Animation(opacity = 1.,height = sp(14), d = .25, t = 'in_out_circ')
        animate_anim1 = Animation(width = dp(Window.width/4 + 36),d = .25, t = 'in_out_circ')
        animate_anim2 = Animation(opacity = .91,d = .25, t = 'in_out_circ')
        animate_anim.start(x)
        animate_anim1.start(x.parent)
        animate_anim2.start(x.parent.children[1])
        otros = x.parent.parent.children
        count = 0
        for i in otros:
            if (count == 9) or (count == 9) :
                pass
            else:
                if i == x.parent: pass
                else:
                    animate_anim = Animation(opacity = 0.,height = sp(0), d = .20, t = 'in_out_circ')
                    animate_anim1 = Animation(width = dp(Window.width/4 - 12),d = .25, t = 'in_out_circ')
                    animate_anim2 = Animation(opacity = .54,d = .25, t = 'in_out_circ')
                    animate_anim.start(i.children[0])
                    animate_anim2.start(i.children[1])
                    animate_anim1.start(i)
            count += 1
            
        self.colors_manager.current = self.colors_manager.next()

                
    
    def funcion(self):
        print("hola")
