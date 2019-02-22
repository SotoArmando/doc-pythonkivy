import kivy
from kivy.config import Config
Config.set('graphics','borderless',1)
Config.set('graphics','resizable',0)
Config.set('graphics','position','custom')
Config.set('graphics','left',1000)
Config.set('graphics','top',35)
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.textinput import TextInput    
Window.size = (426,640)
from kivy.garden.mapview import MapView, MapMarker, MarkerMapLayer,MapSource
import json, requests
from kivy.uix.button import Button
from plyer import gps
from kivy.properties import StringProperty
from kivy.clock import Clock, mainthread

from kivy.uix.relativelayout import RelativeLayout
from kivy.app import App


m1 = MapMarker(lat = 18.454651 , lon = -69.971119)
m2 = MapMarker(lat = 18.434651 , lon = -69.981119)

accesstoken = "pk.eyJ1IjoiYXJtYW5kbzI5IiwiYSI6ImNpd282ZHJ3azAwMWoydHFuZmJudnNzYzEifQ.12vIF51BCThjrut4Q56sGg"
url = "https://api.mapbox.com/directions/v5/mapbox/driving/"+str(m1.lon)+"%2C"+str(m1.lat)+"%3B"+str(m2.lon)+"%2C"+str(m2.lat)+".json?access_token="+accesstoken+"&steps=true"

print url

resp = requests.get(url=url)
data = json.loads(resp.text)
#print data
guardados = []
for route in data['routes']:
        for leg in route['legs']:
            for step in leg['steps']:
                for intersection in step['intersections']:
                    print intersection['location']
                    guardados.append(intersection['location'])





class InterfaceManager(RelativeLayout):
    gps_location = StringProperty()
    gps_status = StringProperty('Click Start to get GPS location updates')
    
    def __init__(self, **kwargs):
        super(InterfaceManager, self).__init__(**kwargs)
        try: 
            gps.configure(on_location=self.on_location,on_status=self.on_status)
        except:
            import traceback
            traceback.print_exc()
            self.gps_status = 'GPS is not implemented for your platform'

        
        accesstoken = "pk.eyJ1IjoiYXJtYW5kbzI5IiwiYSI6ImNpd282ZHJ3azAwMWoydHFuZmJudnNzYzEifQ.12vIF51BCThjrut4Q56sGg"
        sourcex = MapSource(url="https://api.mapbox.com/styles/v1/mapbox/streets-v10/tiles/256/{z}/{x}/{y}@2x?access_token="+accesstoken,
        cache_key="custom_map1s",tile_size=512,
        image_ext="jpg", attribution="@Armando Jose Soto Melo")
        self.mv = MapView(zoom = 15, lat = 18.454651 , lon = -69.971119, map_source = sourcex)
        

        
        for i in guardados:
            print i[0]
            print i[1]
            self.mv.add_widget(MapMarker(lon = i[0],lat = i[1], source = "octicons_f052(0)_64.png"))

            
        self.add_widget(self.mv)
        self.grid = GridLayout(cols = 3, size_hint = (None,None),width = (Window.width), height = 64   , pos=(0,Window.height-64),spacing = 0)
        self.grid2 = GridLayout(cols = 3, size_hint = (None,None),width = (Window.width), height = 110   , pos=(0,15),spacing = 0)
        

        
        self.add_widget(self.grid)
        self.add_widget(self.grid2)
        self.grid.add_widget(Button(size =(64,75), size_hint = (None,1), background_normal = "octicons_f05e(2)_64.png", border =  [1,1,1,1], background_down = "octicons_f05e(2)_64.png"  ))
        self.grid.add_widget(TextInput(size =(150,75), size_hint = (1,1), background_normal = "A4.png", font_size = 17,multiline = False, background_active = "A4.png", padding = [15,25,0,0]))
        self.grid.add_widget(Button(size =(64,75), size_hint = (None,1), background_normal = "octicons_f02e(3)_64.png", background_down = "octicons_f02e(3)_64.png"))
        #self.grid.add_widget(Button(size =(64,75), size_hint = (None,1), background_normal = "octicons_f0c6(0)_64.png", background_down = "octicons_f0c6(0)_64.png"))
        Button1 = Button(size =(64,75), size_hint = (None,1), background_normal = "A8.png", background_down = "A8.png")
        Button1.bind(on_press =self.start(0,0))
        self.grid2.add_widget(Button1)
        self.grid2.add_widget(TextInput(size =(150,75), size_hint = (1,1), background_normal = "A5.png", font_size = 17,multiline = False, background_active = "A5.png", padding = [15,20,0,0]))
        self.grid2.add_widget(Button(size =(64,75), size_hint = (None,1), background_normal = "A10.png", background_down = "A10.png"))       
        
        self.grid2.add_widget(Button(size =(64,75), size_hint = (None,1), background_normal = "A9.png", background_down = "A9.png"))        
        self.grid2.add_widget(TextInput(size =(150,75), size_hint = (1,1), background_normal = "A5.png", font_size = 17,multiline = False, background_active = "A5.png", padding = [15,20,0,0]))
        self.grid2.add_widget(Button(size =(64,75), size_hint = (None,1), background_normal = "A10.png", background_down = "A10.png"))
        
        self.add_widget(Button(size =(Window.width,5),height = 5, size_hint = (None,None), background_normal = "A7.png", background_down = "A7.png",pos=(0,0)))
        
    def start(self, minTime, minDistance):
        gps.start()

    def stop(self):
        gps.stop()

    @mainthread
    def on_location(self, **kwargs):
        self.gps_location = '\n'.join([
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

    
    
    
    
    