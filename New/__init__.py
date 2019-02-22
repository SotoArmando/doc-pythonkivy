import os
import os.path
import sys
import threading
import time
from threading import *
from threading import Timer
from datetime import datetime
import pytz
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
from kivy.graphics.instructions import InstructionGroup
from kivy.metrics import MetricsBase, dp,sp
from kivy.parser import parse_color
from kivy.properties import (BooleanProperty, ListProperty, NumericProperty,
                             ObjectProperty, OptionProperty, StringProperty)
from kivy.resources import resource_add_path
from kivy.uix.accordion import Accordion, AccordionItem
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.bubble import Bubble
from kivy.uix.button import Button
from kivy.uix.checkbox import CheckBox
from kivy.uix.dropdown import DropDown
from kivy.uix.spinner import Spinner
from kivy.uix.floatlayout import FloatLayout
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
from kivy.utils import get_color_from_hex, get_hex_from_color, platform
from kivy.core.audio import SoundLoader,Sound
from kivy.properties import (ObjectProperty, NumericProperty, OptionProperty, BooleanProperty, StringProperty)
from kivy.lang import Builder


from Topnavbar import TopNavigationS
from Linemaplayer import LineMapLayer
from mdata3 import LineMapLayer as mdata3LineMapLayer
from lateralmenu import LateralMenu
from mdata2 import Asistente2 
import os   
import os.path
patch = os.path.dirname(os.path.abspath(__file__))
from alarmarpop import AlarmarPop
asset = patch + 'behave/assets/drawable-mdpi/'
font = patch + '/fonts/'
color = patch + '/colors/'
import wave
import contextlib
C1 = "[color=#13C0C7]"
C4 = "[color=#000000]"
C2 = "[color=#404040]"
C3 = "[color=#ff3333]"
C5 = "[color=#f2f2f2]"
C6 = "[color=#95989A]"
C7 = "[color=#ff0000]"
from  kivy.uix.filechooser import FileChooserListView
# class Label(Label):
    # def __init__(self,**kwargs):
        # self._trigger_texture = Clock.create_trigger(self.texture_update, -1)
        # super(Label, self).__init__(**kwargs)

        # # bind all the property for recreating the texture
        # d = Label._font_properties
        # fbind = self.fbind
        # update = self._trigger_texture_update
        # fbind('disabled', update, 'disabled')
        # for x in d:
            # fbind(x, update, x)

        # self._label = None
        # self._create_label()

        # # force the texture creation
        # self._trigger_texture()
        
        # if self.font_name == "Roboto": self.font_name = font + "Raleway-SemiBold.ttf"


from kivy.uix.stencilview import StencilView
from kivy.properties import (ObjectProperty, NumericProperty, OptionProperty, BooleanProperty, StringProperty)
from kivy.lang import Builder

from kivy.clock import Clock
from kivy.animation import Animation

from pygeocoder import Geocoder
from mdata import Asistente as Connect
import pandas as pd
import numpy as np
#from googlemaps import GoogleMaps