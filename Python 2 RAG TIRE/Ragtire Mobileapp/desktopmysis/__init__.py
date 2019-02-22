import sys  
reload(sys)  
sys.setdefaultencoding('latin-1')

from kivy.graphics import Color, Line
from kivy.graphics.transformation import Matrix
from kivy.graphics.context_instructions import Translate, Scale
from kivy.effects.opacityscroll import OpacityScrollEffect
from kivy.effects.scroll import ScrollEffect
from kivy.garden.mapview import MapView, MapMarker, MarkerMapLayer, MapSource, MapLayer,MapMarkerPopup
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
from kivy.uix.screenmanager import ScreenManager, Screen,SwapTransition, NoTransition,SlideTransition,FadeTransition,WipeTransition,FallOutTransition,RiseInTransition 
from kivy.uix.behaviors import ButtonBehavior
from kivy.lang import Builder
from kivy.garden.mapview import MapView, MapMarker, MarkerMapLayer,MapSource
from kivy.uix.button import Button
from kivy.clock import Clock, mainthread
from kivy.uix.relativelayout import RelativeLayout
from kivy.app import App
import os   
import os.path
import datetime


from desktopmysis.mdata import Asistente

resource_add_path(os.path.dirname(__file__))

from kivy.uix.behaviors import ButtonBehavior
from kivy.animation import Animation
from kivy.uix.widget import Widget
from kivy.uix.stencilview import StencilView
from kivy.metrics import dp
from kivy.clock import Clock
from kivy.properties import (ObjectProperty, NumericProperty, OptionProperty,
                             BooleanProperty, StringProperty)
from kivy.resources import resource_add_path
from kivy.lang import Builder
import os.path


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


class ImageButton(ButtonBehavior, Image): pass
class ClassicTexInput(RelativeLayout):#COMPLEMENTO 'PARENT' EL PROYECTO
    def __init__(self, **kwargs):
        super(ClassicTexInput, self).__init__(**kwargs)
        self.campo = kwargs["campo"]
        self.size_hint_y = None
        self.height = 45
        pariente = GridLayout(rows = 1)
        pariente.add_widget(Label(size_hint_x = None, width = 150,markup = True, text = C4 + kwargs["campo"] + ":"))
        self.intext = TextInput(padding = [0,14,0,0], password = kwargs["passw"],hint_text = kwargs["campo"],background_normal = color + "None.png", background_active = color + "None.png")
        pariente.add_widget(self.intext)
        self.add_widget(pariente)
class Button(Button):
    def __init__(self,**kwargs):
        super(Button, self).__init__(**kwargs)
        self.markup = True
        #self.font_name = fonts + "PTS55F.TTF"   
        self.background_normal  = color + "16bb.png"  
class A_Button(Button):
    def __init__(self,**kwargs):
        super(Button, self).__init__(**kwargs)
        self.markup = True
class Dualbutton(RelativeLayout):
    def __init__(self, **kwargs):
        super(Dualbutton, self).__init__(**kwargs)
        self.size_hint_y = 1
        self.height = 120
        pariente = GridLayout(rows = 1)
        self.b1 = Button(markup = True,text = C4+"[b]Agregar",background_normal = color + "None.png", background_down = color + "10.png")
        self.b2 = Button(markup = True,text = C4+"Cancelar",background_normal = color + "None.png", background_down = color + "10.png")
        pariente.add_widget(self.b1)
        pariente.add_widget(self.b2)
        self.add_widget(pariente) 
