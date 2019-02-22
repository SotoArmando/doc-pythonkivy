#!/usr/bin/env python
# -*- coding: utf-8 -*-


















from __init__ import *


patch = os.path.dirname(os.path.abspath(__file__))
asset = patch + '/assets/drawable-mdpi/'
color = patch + '/colors/'
font = patch + '/fonts/'
#Window.size = (360,640)
Window.clearcolor = (1,1,1,1)
class Boton(RelativeLayout):
    def __init__(self, **kwargs):
        super(Boton, self).__init__(**kwargs)
        self.sel = None
        img = Image(size_hint = (.75,.90), pos_hint = {'center_x':.5, 'center_y':.65}, source = kwargs["source"], keep_ratio = True, allow_stretch = True)
        label = Label(font_size = sp(12),markup = True,text = "[color=#000000]"+kwargs["text"],size_hint = (1,None), height = dp(50), pos_hint = {"center_y":.25})
        self.img = img
        self.label = label
        self.add_widget(img)
        self.add_widget(label)
    
    
        behavior = Button(opacity = 0, on_release = lambda x: self.animate())
        self.b = behavior
        self.add_widget(behavior)
        
    def animate(self):
        print "hola"
        x = Animation(size_hint = (1,1), d = .1 , t = 'in_quad') + Animation(size_hint = (.75,.90), d = .1 , t = 'out_quad')
        x.start(self.img)
class ImageButton(ButtonBehavior,AsyncImage): pass
class Comp1(RelativeLayout):
    def __init__(self, **kwargs):
        super(Comp1, self).__init__(**kwargs)
        from mdata2 import Asistente
        self.asist = Asistente()
        accesstoken = "pk.eyJ1IjoiYXJtYW5kbzI5IiwiYSI6ImNpd282ZHJ3azAwMWoydHFuZmJudnNzYzEifQ.12vIF51BCThjrut4Q56sGg"
        sourcex = MapSource(url="https://api.mapbox.com/styles/v1/mapbox/streets-v10/tiles/256/{z}/{x}/{y}?access_token=pk.eyJ1IjoibWFjYXR1cyIsImEiOiJjaXlubGRkdXAwMDJ1MzNwZjdwanhkdnd6In0.eYV9WVlCsI44Ku0HSup7Pg",
        cache_key="custom_map1s",tile_size=256,
        image_ext="jpg", attribution="@Armando Jose Soto Melo")
        self.x_mapview = MapView(lat = 18.454651 , lon = -69.971119, zoom = 16, map_source = sourcex)
            
    
        self.add_widget(self.x_mapview)
        
        from comp.MapMarker import MapMarkerPopup as x1
        from shadowedrelatlayout import SHRelativeLayout
        marcador = x1(popup_size= (dp(200), dp(50)),size_hint = (None,None), size = (dp(50),dp(50)),opacity = 1,lat = 18.454651 , lon = -69.971119, source = asset + "placeholder.png", anim_delay = 0)#anchor_y = .5
        marcador1 = x1(popup_size= (dp(200), dp(50)),size_hint = (None,None), size = (dp(50),dp(50)),opacity = 1,lat = 18.455751 , lon = -69.971119, source = asset + "Group 296.png", anim_delay = 0)#anchor_y = .5
        marcador2 = x1(popup_size= (dp(200), dp(50)),size_hint = (None,None), size = (dp(50),dp(50)),opacity = 1,lat = 18.450751 , lon = -69.971119, source =  "mypos.zip",anchor_y = .5, anim_delay = 0)#anchor_y = .5
        dimroot = SHRelativeLayout(pos_hint = {"x":.5})
        
        dim = GridLayout(rows = 1)
        dim.add_widget(Button(opacity = 1,markup = True,text_size = (dp(150)-dp(16),dp(50)),background_normal = color + "17.png",background_down = color + "17.png",text = "[size=14sp][b]Farmacia Carol[/b][size=12sp]\nAv 27 de Febrero 221", halign = 'left', valign = 'middle'))
        subdim = RelativeLayout(size_hint_x = None, width = dp(50))
        subdim.add_widget(Button(on_release=  lambda x: marcador.close(),background_normal = asset + "Group 294.png",background_down = asset + "Group 295.png", keep_ratio = False , allow_stretch = True))
        #subdim.add_widget(ImageButton(on_release = lambda x: self.dibujardirecciones(str((marcador.lat, marcador.lon))[1:-1].split(','),str((marcador1.lat, marcador1.lon))[1:-1].split(',')), source = color + "16.png"))
        dim.add_widget(subdim)
        dimroot.add_widget(dim)
        dimroot.add_widget(Image(source = asset + "Ellipse 2.png", size_hint = (None,None),size = (dp(26),dp(26)), pos = (dp(-13),dp(-16))))
        marcador.add_widget(dimroot)
        
        
        self.x_mapview.add_marker(marcador2)
        self.x_mapview.add_marker(marcador1)
        self.x_mapview.add_marker(marcador)
        from mdata3 import LineMapLayer as mdata3LineMapLayer
        self.line = mdata3LineMapLayer()
        self.x_mapview.add_layer(self.line, mode="scatter")
        self.line.reposition()
        
        self.marker = MarkerMapLayer()
        self.x_mapview.add_layer(self.marker) 
        
    def dibujardirecciones(self, pos1,pos2):

        def Done():

            for n in range(2):
                if pos1[n][0] == ' ':
                    pos1[n] = float(pos1[n][1:])
                if pos2[n][0] == ' ':
                    pos2[n] = float(pos2[n][1:])
            
                
            print pos1,pos2
            direcciones = self.asist.returngeo(pos1[::-1],pos2[::-1])
            self.line.clear()
            marker0 = MapMarker(anchor_y = 0.5 ,lat= float(direcciones[0][1]), lon= float(direcciones[0][0]))
            #self.x_mapview.add_marker(marker0, layer = self.marker )
            
            marker1 = MapMarker(anchor_y = 0.5 ,lat= float(direcciones[-1][1]), lon= float(direcciones[-1][0]))
            #self.x_mapview.add_marker(marker1, layer = self.marker )
            for i in direcciones:
                
                self.line.newpointgeo(i)
            self.line.draw_line()

        Clock.schedule_once(lambda x: Done(), .330)
        
    def funcion(self):
        print("hola")
        
class MyApp(App):
    def build(self):
        return Comp1()
 

if __name__ in ('__main__', '__android__'):
    MyApp().run()

    
    
    
    
    