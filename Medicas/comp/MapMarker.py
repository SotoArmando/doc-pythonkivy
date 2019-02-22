from os.path import join, dirname
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.image import Image, AsyncImage
from kivy.uix.scatter import Scatter
from kivy.uix.behaviors import ButtonBehavior
from kivy.properties import NumericProperty, ObjectProperty, ListProperty, \
    AliasProperty, BooleanProperty, StringProperty
from kivy.graphics import Canvas, Color, Rectangle
from kivy.animation import Animation
from kivy.graphics.transformation import Matrix
from kivy.lang import Builder
from kivy.compat import string_types
from math import ceil
from kivy.garden.mapview import MapView, MapMarker, MarkerMapLayer, MapSource, MapLayer,MapMarkerPopup

class Custom_MapMarker(ButtonBehavior, AsyncImage):
    """A marker on a map, that must be used on a :class:`MapMarker`
    """

    anchor_x = NumericProperty(0.5)
    """Anchor of the marker on the X axis. Defaults to 0.5, mean the anchor will
    be at the X center of the image.
    """

    anchor_y = NumericProperty(0)
    """Anchor of the marker on the Y axis. Defaults to 0, mean the anchor will
    be at the Y bottom of the image.
    """

    lat = NumericProperty(0)
    """Latitude of the marker
    """

    lon = NumericProperty(0)
    """Longitude of the marker
    """

    source = StringProperty(join(dirname(__file__), "icons", "marker.png"))
    """Source of the marker, defaults to our own marker.png
    """

    # (internal) reference to its layer
    _layer = None

    def detach(self):
        if self._layer:
            self._layer.remove_widget(self)
            self._layer = None


class MapMarkerPopup(MapMarker):
    is_open = BooleanProperty(False)
    placeholder = ObjectProperty(None)
    popup_size = ListProperty([100, 100])
    def close(self):
        self.is_open = False
        self.refresh_open_status()
    def add_widget(self, widget):
        if not self.placeholder:
            self.placeholder = widget
            if self.is_open:
                super(MapMarkerPopup, self).add_widget(self.placeholder)
        else:
            self.placeholder.add_widget(widget)

    def remove_widget(self, widget):
        if widget is not self.placeholder:
            self.placeholder.remove_widget(widget)
        else:
            super(MapMarkerPopup, self).remove_widget(widget)

    def on_is_open(self, *args):
        self.refresh_open_status()

    def on_release(self, *args):
        self.is_open = not self.is_open

    def refresh_open_status(self):
        if not self.is_open and self.placeholder.parent:
            a = Animation(opacity = 0, d = .5 , t = 'out_quart')
            a.bind(on_complete = lambda x,z: super(MapMarkerPopup, self).remove_widget(self.placeholder))
            a.start(self.placeholder)
        elif self.is_open and not self.placeholder.parent:
            super(MapMarkerPopup, self).add_widget(self.placeholder)
            self.placeholder.opacity = 0
            a = Animation(opacity = 1, d = .5 , t = 'out_quart')
            
            b = Animation(opacity = 0, d = .10 , t = 'in_expo') + Animation(opacity = 1, d = .25 , t = 'out_expo')
            b.bind(on_complete = lambda x,y: a.start(self.placeholder))
            b.start(self)
            
            
            
            