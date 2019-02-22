from kivy.lang import Builder
from plyer import gps
from kivy.app import App
from kivy.properties import StringProperty
from kivy.clock import Clock, mainthread

class GpsTest():
    gps_location = StringProperty()
    gps_status = StringProperty('Click Start to get GPS location updates')
    lat = ""
    lon = ""
    
    def __init__(self,**kwargs):
        try:
            gps.configure(on_location=self.on_location,
                          on_status=self.on_status)
            self.start(1000, 0)
        except NotImplementedError:
            import traceback
            traceback.print_exc()
            self.gps_status = 'GPS is not implemented for your platform'

        return Builder.load_string(kv)
        
    def start(self, minTime, minDistance):
        try:
            gps.start(minTime, minDistance)
        except:
            gps.start()
        

    def stop(self):
        gps.stop()

    @mainthread
    def on_location(self, **kwargs):

        self.lat = kwargs["lat"]
        self.lon = kwargs["lon"]
        print "AQUIAQUIAQUIAQUIAQUIAQUIAQUI"
        print "AQUIAQUIAQUIAQUIAQUIAQUIAQUI"
        print "AQUIAQUIAQUIAQUIAQUIAQUIAQUI"
        print "AQUIAQUIAQUIAQUIAQUIAQUIAQUI"
        print ""
        print self.lat,self.lon
        print ""
        print "AQUIAQUIAQUIAQUIAQUIAQUIAQUI"
        print "AQUIAQUIAQUIAQUIAQUIAQUIAQUI"
        print "AQUIAQUIAQUIAQUIAQUIAQUIAQUI"
        print "AQUIAQUIAQUIAQUIAQUIAQUIAQUI"
        self.gps_location = '\n'.join([
            '{}={}'.format(k, v) for k, v in kwargs.items()])

    @mainthread
    def on_status(self, stype, status):
        self.gps_status = 'type={}\n{}'.format(stype, status)

    def on_pause(self):
        gps.stop()
        return True

    def on_resume(self):
        gps.start(1000, 0)
        pass


