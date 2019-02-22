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
Window.size = (640,360)

class Asteroide(RelativeLayout):
    rotation = NumericProperty(0)
    def __init__(self,**kwargs):
        super(Asteroide, self).__init__(**kwargs)
        self.activado = True
        self.punto = [0,0]
        import random
        self.Display = ScatterLayout() 
       
 
        self.add_widget(self.Display)

        posicion1 = (0 - self.width, random.random() * Window.height)#pos , random
        posicion2 = (Window.width + self.width, random.random() * Window.height)#pos , random
        posicion3 = (random.random() * Window.width , 0 - self.height)#random , pos
        posicion4 = (random.random() * Window.width , Window.height + self.height)#random , pos
        posiciones = [posicion1,posicion2,posicion3,posicion4]
        direcciones = [-90.0 +(random.random() *180.0),
                        90.0 +(random.random() *180.0),
                              (random.random() *180.0),
                        180.0+(random.random() *180.0)
        ]
        
        if (direcciones[0] +  90.0) < 45.0: direcciones[0] += 45.0
        if (direcciones[1] -  90.0) < 45.0: direcciones[1] += 45.0
        if (direcciones[2]        ) < 45.0: direcciones[2] += 45.0
        if (direcciones[3] - 180.0) < 45.0: direcciones[3] += 45.0
        
        if (direcciones[0] +  90.0) > 135.0: direcciones[0] -= 45.0
        if (direcciones[1] -  90.0) < 135.0: direcciones[1] -= 45.0
        if (direcciones[2]        ) < 135.0: direcciones[2] -= 45.0
        if (direcciones[3] - 180.0) < 135.0: direcciones[3] -= 45.0
        
        print direcciones
        
        hey = random.random()
        r = int(( hey/ 0.25))

        self.direccion = direcciones[r]
        self.pos = posiciones[r]
        with self.Display.canvas:
            Color(1.0, 1.0, 1.0)
            #self.player1 = Rectangle(pos = (0,0), size = (64,64))
            Rectangle(size = self.size, pos = (0,0))

            # self.thispoint0 = Ellipse(pos = self.pos , size = (2,2))
            # self.thispoint1 = Ellipse(pos = (0,self.size[0]) , size = (2,2))
            # self.thispoint2 = Ellipse(pos = (self.size[0],0) , size = (2,2))
            # self.thispoint3 = Ellipse(pos = self.size , size = (2,2))
       
  
        self.a = Animation(rotation = 360*1000, d = 10*1000, t = 'out_expo')
        self.a.start(self.Display)
        
        self.mymovement = Clock.schedule_interval(self.go, 1.0 / 60.0)
        
    def go(self,*args):
        if self.activado == True:
            radianes = math.radians(self.direccion)
            self.x = (self.x + math.cos(radianes)*4);
            self.y = (self.y + math.sin(radianes)*4);
            if (self.x > Window.width + self.width) or (self.y > Window.height + self.height):
                self.a.stop_property(self.Display, 'rotation')
                self.mymovement.cancel()
                self.Display.canvas.clear()
                self.parent.remove_widget(self)
                self.activado = False
            if (self.x < 0 - self.width*2) or (self.y < 0 - self.height*2):
                self.a.stop_property(self.Display, 'rotation')
                self.mymovement.cancel()
                self.Display.canvas.clear()
                try:
                    self.parent.remove_widget(self)
                except: pass
                self.activado = False
        else: 
            pass
         
        
    def on_pos(self,*args):
        if self.activado == True:
            try:
                #print self.to_local(0,0, relative=True)

                radianes = math.radians(self.Display.rotation)

                self.punto = [math.cos(radianes) * 50, math.sin(radianes) * 50]
                
                dibujo = [self.punto[0] + self.size[0]/2 - 2, self.punto[1] + self.size[1]/2 - 2]
                self.punto = self.puntero.to_window(dibujo[0],dibujo[1],relative = False)
                self.puntero.pos = dibujo
            except:
                pass
        else: 
            pass
     

 


        

 

class Generador(RelativeLayout):
    def __init__(self,**kwargs):
        super(Generador, self).__init__(**kwargs)
        Clock.schedule_interval(self.agregar_asteroide, 0.675 )
        
    def agregar_asteroide(self,*args):
        import random
        r = random.random()
        self.add_widget(Asteroide(size_hint = (None,None), size = (r*64,r*64) ))
        
class Crud(App):
    def build(self):
        return Generador()

if __name__ == '__main__':
    Crud().run()
        
        
    
    
        