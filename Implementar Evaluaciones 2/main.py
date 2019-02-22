from __init__ import *

Asset = join(dirname(dirname(abspath(__file__))), '_Assets')
Color = join(dirname(dirname(abspath(__file__))), '_Colors')
Font = join(dirname(dirname(abspath(__file__))), '_Fonts')
from kivy.graphics import Color, Ellipse, Rectangle, RoundedRectangleprint "Assets DIR",Asset
print "Colors DIR",Color
print "Fonts DIR",Font

class ImageButton(ButtonBehavior, Image): pass

class Entidad(Scatter):
    z = NumericProperty(0)# entre 1 a 100
    
    aceleracion_gravedad = NumericProperty(9.8) #pixeles
    velocidad_gravedad = NumericProperty(0)
    
    aceleracion_x = NumericProperty(3)
    aceleracion_y = NumericProperty(0)
    aceleracion_z = NumericProperty(0)
    
    velocidad_z = NumericProperty(50)
    velocidad_x = NumericProperty(20)
    velocidad_y = NumericProperty(-150)
    
    def __init__(self,**kwargs):
        super(Entidad, self).__init__(**kwargs)
        self.size_hint = (None,None)
        Clock.schedule_interval(lambda x: self.update() , 1.0/60.0)
        Clock.schedule_interval(lambda x: self.d3movement() , 1.0/60.0)
        self.add_widget(Button())
        self.inicial = self.pos
        print self.pos, 'posicion inicial'
        #self.funcion_de_movimiento_x()
    def update(self,*args):
        self.velocidad_gravedad += -1*self.aceleracion_gravedad/60.0
        
        self.velocidad_z += self.velocidad_gravedad 
        self.velocidad_x += self.aceleracion_x
        self.velocidad_y += self.aceleracion_y
        
    def d3movement(self,*args):
        # if (self.scale < 2) and (self.scale >= 1):
            # self.scale += (self.velocidad_z/60.0) /30.0

        if self.y >  0:
            self.x += self.velocidad_x/60.0
            self.y += self.velocidad_z/60.0
    def funcion_de_movimiento_x(self):
        segundo = 0
        x = self.inicial[0]
        y = self.inicial[1]
        z = self.z
        
        while True:
            velocidad_gravedad = self.velocidad_gravedad + -1*(self.aceleracion_gravedad/60.0)*segundo 
            evaluar_x = x + (self.velocidad_x + (self.aceleracion_x*segundo))
            evaluar_y = y + (self.velocidad_y + (self.aceleracion_y*segundo))
            evaluar_z = z + (self.velocidad_z + (self.aceleracion_z*segundo) + velocidad_gravedad)
            
            print "segundo:",segundo,";",evaluar_x, evaluar_y, evaluar_z
            segundo += 1
            
            

    def on_pos(self , *args):
        print self.x, self.y
class TestGame(RelativeLayout):
    def __init__(self, **kwargs):
        super(TestGame, self).__init__(**kwargs)
        
        self.add_widget(Entidad(pos = (300,500), size = (50,50)))
                
class YourAppNameApp(App):
    def build(self):
        return TestGame()

if __name__ == '__main__':
    YourAppNameApp().run()
