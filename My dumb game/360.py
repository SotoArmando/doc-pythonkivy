from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.scatterlayout import ScatterLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.graphics import *
from kivy.vector import Vector
from kivy.animation import Animation
from kivy.uix.stencilview import StencilView
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.graphics.transformation import Matrix
from kivy.uix.scatter import Scatter
from kivy.metrics import *
from kivy.properties import NumericProperty
import math

class Main(RelativeLayout):
    radianes = 0.0
    def __init__(self,**kwargs):
		super(Main, self).__init__(**kwargs)
		self.punto = [0.0,100.0]
		centro = [50,50]
		with self.canvas:
			Color(0,0,1,1)
			Ellipse(size = (4,4), pos = self.punto)
		Clock.schedule_interval(self.siguiente, 1.0/60)   
		tx = TextInput(size_hint_x = .2, height = dp(54),text = "90", size_hint_y = None)
		tx.bind(text = lambda x,t: self.dibujar_withdegrees(x.text))
		self.add_widget(tx)

    def dibujar_withdegrees(self,degrees):
        print "x"
        self.canvas.clear()
        self.radianes = math.radians(float(degrees))

        print math.radians(degrees)
        if str(math.degrees(self.radianes)) == "360.0": self.radianes = 0

        self.punto = [math.cos(self.radianes) * 100, math.sin(self.radianes) * 100]

        dibujo = [self.punto[0] + 200 , self.punto[1] + 200]
        with self.canvas:
            Color(0,1,1,1)
            Ellipse(size = (4,4), pos = dibujo)
            Color(0,0,1,1)
            Ellipse(size = (4,4), pos = (200,200))
            
        print self.punto
    def siguiente(self,*args):
        self.canvas.clear()
        

        self.radianes += math.radians(1)
        print math.degrees(self.radianes)
        if str(math.degrees(self.radianes)) == "360.0": self.radianes = 0
        self.punto = [math.cos(self.radianes) * 100, math.sin(self.radianes) * 100]
        
        dibujo = [self.punto[0] + 200 , self.punto[1] + 200]
        with self.canvas:
            Color(0,1,1,1)
            Ellipse(size = (4,4), pos = dibujo)
            Ellipse(size = (4,4), pos = (200,200))
        print self.punto
        
class Crud(App):
    def build(self):
        return Main()

if __name__ == '__main__':
    Crud().run()
        
        
    
    
        