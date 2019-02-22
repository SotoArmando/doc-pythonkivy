from kivy.garden.mapview import MapView, MapMarker, MarkerMapLayer
import json, requests
import kivy
from kivy.uix.relativelayout import RelativeLayout
from kivy.app import App


m1 = MapMarker(lat = 18.454651 , lon = -69.971119)
m2 = MapMarker(lat = 18.434651 , lon = -69.981119)
puntos = [m1,m2]
puntoA = puntos[0]
puntoB = puntos[1]
url = 'https://api.mapbox.com/directions/v5/mapbox/driving/'+str(puntoA.lat)+","+str(puntoA.lon)+';-77.03,38.91?steps=true&alternatives=true&access_token=your-access-token'
params = dict(
    origin=str(puntoA.lat)+","+str(puntoA.lon),
    destination=str(puntoB.lat)+","+str(puntoB.lon),
    sensor='false'
)

resp = requests.get(url=url, params=params)
data = json.loads(resp.text)
for route in data['routes']:
        for leg in route['legs']:
            for step in leg['steps']:
                print step['html_instructions']
                

puntos_lat = []
puntos_lot = []

for route in data['routes']:
        for leg in route['legs']:
            for step in leg['steps']:
                print step['start_location']  
                puntos_lat.append(step['start_location']['lat'])
                puntos_lot.append(step['start_location']['lng'])
                print step['end_location']     
                puntos_lat.append(step['end_location']['lat'])
                puntos_lot.append(step['end_location']['lng'])
                
print ("")
print ("")
print ("")
print ("")
print ("")
print ("")

path = ""
print len(puntos_lat)
for i in range(len(puntos_lat)):
    print puntos_lat[i]
    print puntos_lot[i]
    path = path + str(puntos_lat[i])+","+str(puntos_lot[i])+"|"

path = path[:-1]
print path
url = 'https://roads.googleapis.com/v1/snapToRoads'

params = dict(
    path=path,
    interpolate = True,
    key = "AIzaSyAEEPqE645oiHa2POH_CfLU0b9i_vcuaAY"
)

resp = requests.get(url=url, params=params)
data = json.loads(resp.text)

for a in data['snappedPoints']:
    print a['location']




class InterfaceManager(RelativeLayout):
    def __init__(self, **kwargs):
        super(InterfaceManager, self).__init__(**kwargs)
        self.mv = MapView(zoom = 15, lat = 18.454651 , lon = -69.971119)

        for a in data['snappedPoints']:
            print a['location']
            self.mv.add_widget(MapMarker(lat = a['location']['latitude'] , lon = a['location']['longitude'], source = "marker.png"))

            
        self.add_widget(self.mv)
        
        
class MyApp(App):
    def build(self):
        return InterfaceManager()


if __name__ in ('__main__', '__android__'):
    MyApp().run()

    
    
    
    
    