import os
import os.path
import sys
import threading
import time
from threading import *
from threading import Timer
import datetime
from kivy.uix.carousel import Carousel
from kivy.uix.effectwidget import EffectWidget
from kivy.uix.effectwidget import HorizontalBlurEffect,VerticalBlurEffect
from kivy.adapters.listadapter import ListAdapter
from kivy.adapters.models import SelectableDataItem
from kivy.adapters.simplelistadapter import SimpleListAdapter
from kivy.animation import Animation
from kivy.app import App
from kivy.base import runTouchApp
from kivy.clock import Clock, mainthread
from kivy.core.window import Window
from kivy.effects.opacityscroll import OpacityScrollEffect
from kivy.effects.scroll import ScrollEffect
from kivy.graphics import *
from kivy.graphics.instructions import InstructionGroup,Callback
from kivy.metrics import MetricsBase, dp,sp
from kivy.parser import parse_color

from kivy.resources import resource_add_path
from kivy.uix.accordion import Accordion, AccordionItem
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.bubble import Bubble
from kivy.uix.button import Button
from kivy.uix.checkbox import CheckBox
from kivy.uix.dropdown import DropDown
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics.vertex_instructions import RoundedRectangle
from kivy.uix.pagelayout import PageLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import AsyncImage, Image
from kivy.uix.label import Label
from kivy.uix.listview import (CompositeListItem, ListItemButton,
                               ListItemLabel, ListView)
from kivy.uix.popup import Popup
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.scatter import Scatter
from kivy.uix.screenmanager import (FadeTransition, FallOutTransition,
                                    NoTransition, RiseInTransition, Screen,
                                    ScreenManager, SlideTransition,
                                    SwapTransition, WipeTransition)
from kivy.uix.scrollview import ScrollView
from kivy.uix.stencilview import StencilView
from kivy.uix.textinput import TextInput
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.widget import Widget

from kivy.core.audio import SoundLoader,Sound
from kivy.properties import (ObjectProperty, NumericProperty, OptionProperty, BooleanProperty, StringProperty, ListProperty, DictProperty)
from kivy.lang import Builder
from time import gmtime, strftime
Window.clearcolor = (1,1,1,1)

from itertools import chain
from kivy.graphics.texture import Texture

class SHRelativeLayout(RelativeLayout):
    def __init__(self, **kwargs):
        super(SHRelativeLayout, self).__init__(**kwargs)
        self.add_widget(Image(source = asset + "U.png", size_hint_y = None, height = dp(3),keep_ratio = False, allow_stretch = True , pos_hint = {"y":1} ) )
        self.add_widget(Image(source = asset + "D.png", size_hint_y = None, height = dp(9),keep_ratio = False, allow_stretch = True , y = dp(-9) ) )
        self.add_widget(Image(source = asset + "L.png", size_hint_x = None, width = dp(6),keep_ratio = False, allow_stretch = True , x = dp(-6) ) )
        self.add_widget(Image(source = asset + "R.png", size_hint_x = None, width = dp(6),keep_ratio = False, allow_stretch = True, pos_hint = {"x":1} ) )
        
        self.add_widget(Image(source = asset + "LU.png", size_hint = (None,None), size = (dp(6),dp(3)), width = dp(6),keep_ratio = False, allow_stretch = True, x = dp(-3), pos_hint = {"y":1} ))
        
        self.add_widget(Image(source = asset + "RU.png", size_hint = (None,None), size = (dp(6),dp(3)), width = dp(6),keep_ratio = False, allow_stretch = True, y = dp(-3), pos_hint = {"x":1} ))
        
        self.add_widget(Image(source = asset + "LD.png", size_hint = (None,None), size = (dp(6),dp(9)), width = dp(6),keep_ratio = False, allow_stretch = True, x = dp(-6), y = dp(-9) ) )
        
        self.add_widget(Image(source = asset + "RD.png", size_hint = (None,None), size = (dp(7),dp(9)), width = dp(6),keep_ratio = False, allow_stretch = True, pos_hint = {"x":1}, y = dp(-9) ) )

class Gradient(object):
    @staticmethod
    def horizontal(*args):
        texture = Texture.create(size=(len(args), 1), colorfmt='rgba')
        buf = bytes([ int(v * 255)  for v in chain(*args) ])  # flattens

        texture.blit_buffer(buf, colorfmt='rgba', bufferfmt='ubyte')
        return texture

    @staticmethod
    def vertical(*args):
        texture = Texture.create(size=(1, len(args)), colorfmt='rgba')
        buf = bytes([ int(v * 255)  for v in chain(*args) ])  # flattens

        texture.blit_buffer(buf, colorfmt='rgba', bufferfmt='ubyte')
        return texture