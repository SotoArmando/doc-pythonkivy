# -*- coding: utf-8 -*-

import kivy

from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.garden.mapview import MapView, MapMarker, MapSource

class KVMaps(App):
  def build(self):
    layout = FloatLayout()
    accesstoken = "pk.eyJ1IjoiYXJtYW5kbzI5IiwiYSI6ImNpd282ZHJ3azAwMWoydHFuZmJudnNzYzEifQ.12vIF51BCThjrut4Q56sGg"
    sourcex = MapSource(url="https://api.mapbox.com/styles/v1/mapbox/streets-v10/tiles/256/{z}/{x}/{y}?access_token=pk.eyJ1IjoibWFjYXR1cyIsImEiOiJjaXlubGRkdXAwMDJ1MzNwZjdwanhkdnd6In0.eYV9WVlCsI44Ku0HSup7Pg",
    cache_key="custom_map1s",tile_size=256,
    image_ext="jpg", attribution="@Armando Jose Soto Melo")
    self.mv = MapView(zoom = 15, lat = 18.454651 , lon = -69.971119, map_source = sourcex)
    
    m1 = MapMarker(lat = 18.454651 , lon = -69.971119)  # Lille


    self.mv.add_marker(m1)

    #self.mv.customBounds  = "Enable"
    
    layout.add_widget(self.mv)
    return layout
    
if __name__ in ('__android__','__main__'):
  KVMaps().run()
