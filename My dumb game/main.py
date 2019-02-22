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
from kivy.uix.image import Image
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.clock import Clock
from joystick.joystick import Joystick
from kivy.graphics.transformation import Matrix
from kivy.uix.scatter import Scatter
from kivy.metrics import *
from kivy.properties import NumericProperty
from asteroides import Asteroide
import math
Window.size = (640,360)

    

        
class Point(Widget):
    def __init__(self,**kwargs):
        super(Point, self).__init__(**kwargs)
        self.size = (8,8)
        with self.canvas:
            Color(1,0,0,1)
            Ellipse(size = self.size , pos = (64-4,32-4))
    def on_pos(self,*args):
        print args
            
class Disparo(RelativeLayout):
    direccion = NumericProperty(0)
    rotation = NumericProperty(0)
    def __init__(self, **kwargs):
        super(Disparo, self).__init__(**kwargs)
        self.activado = True
        self.rotation = kwargs["rotation"]
        self.pos = kwargs["pos"]; self.pos[0] -= kwargs["size"][0]/2; self.pos[1] -= kwargs["size"][1]/2
        self.Display = ScatterLayout( size = self.size) 
        self.Display.children[0].size = self.size

        self.add_widget(self.Display)
        #self.add_widget(Button())
        with self.Display.children[0].canvas:

            #self.player1 = Rectangle(pos = (0,0), size = (64,64))
            Rectangle(size = self.size, pos = (0,0), source = "laserBlue04.png")
    
            # self.thispoint0 = Ellipse(pos = self.pos , size = (2,2))
            # self.thispoint1 = Ellipse(pos = (0,self.size[0]) , size = (2,2))
            # self.thispoint2 = Ellipse(pos = (self.size[0],0) , size = (2,2))
            # self.thispoint3 = Ellipse(pos = self.size , size = (2,2))
            
        self.Display.rotation = self.rotation
        self.mymovement = Clock.schedule_interval(self.go, 1.0/60.0)
        
    def go(self,*args):     
        if self.activado == True:
            #print self.direccion
            radianes = math.radians(self.direccion)
            self.x = (self.x + math.cos(radianes)*7.0);
            self.y = (self.y + math.sin(radianes)*7.0);
            if (self.x > Window.width) or (self.y > Window.height):
                
                
                self.Display.children[0].canvas.clear()
                self.parent.remove_widget(self)
                self.activado = False
            if (self.x < 0 - self.width*2) or (self.y < 0 - self.height*2):
                    
                self.Display.children[0].canvas.clear()
                try:
                    self.parent.remove_widget(self)
                except: 
                    pass
                self.activado = False
                
        else: pass
            
         

    def on_pos(self,*args):
        pass
        #print args 
        # try:
            # self.canvas.clear()
            # with self.canvas:
                # Color(0.09803921568627451, 1.0, 0.3215686274509804, 1.0)
                # self.player1 = Rectangle(pos = (0,0), size = (32,32))
        # except: pass
            
class Jugador(RelativeLayout):
    rotation = NumericProperty(0)
    def __init__(self,**kwargs):
        super(Jugador, self).__init__(**kwargs)
        self.disparos = []
        self.punto = [0,0]
        self.last_anim = None
        self.Display = ScatterLayout() 
        self.puntero = Widget(size = (4,4) , size_hint = (None,None) )
        self.add_widget(self.puntero)
        self.add_widget(self.Display)
        #self.animate_player()
        
        with self.Display.canvas:
            
            #Color(0.09803921568627451, 1.0, 0.3215686274509804, 1.0)
            #self.player1 = Rectangle(pos = (0,0), size = (64,64))
            Rectangle(size = self.size, pos = (0,0), source = "playerShip3_red.png")
            #Color(0, 0, 0.3215686274509804, 1.0)
            # self.thispoint0 = Ellipse(pos = self.pos , size = (2,2))
            # self.thispoint1 = Ellipse(pos = (0,self.size[0]) , size = (2,2))
            # self.thispoint2 = Ellipse(pos = (self.size[0],0) , size = (2,2))
            # self.thispoint3 = Ellipse(pos = self.size , size = (2,2))
       
        
        Clock.schedule_interval(self.Disparar, 1.0 / 3.0)   
        Clock.schedule_interval(self.DisparosActivos, 1.0 / 3.0)   
        
        #self.Display.add_widget(Point(size_hint = (None,None)))
        self.on_pos()
    def DisparosActivos(self, *args):
        activos = 0
        for disparo in self.disparos:
            if disparo.activado == True:
                activos += 1
            else:
                pass
        print "DISPAROS ACTIVOS", activos
                
    def on_pos(self,*args):
        try:
            radianes = math.radians(self.Display.rotation)

            self.punto = [math.cos(radianes) * 50, math.sin(radianes) * 50]
            
            dibujo = [self.punto[0] + self.size[0]/2 - 2, self.punto[1] + self.size[1]/2 - 2]
            self.punto = self.puntero.to_window(dibujo[0],dibujo[1],relative = False)
            self.puntero.pos = dibujo
        except:
            pass
     
    def Disparar(self, *args):
        print self.punto
        nuevoDisparo = Disparo(pos = self.punto,rotation = self.rotation, direccion = self.Display.rotation, size = (37*0.50,13*0.50), size_hint = (None,None))
        self.disparos.append(nuevoDisparo)
        self.parent.parent.add_widget(nuevoDisparo)
        try: self.last_anim.stop_property(self.Display, 'rotation')
        except: pass
        #self.animate_player()
        
    def on_rotation(self, *args):
        self.Display.rotation = args[1]
      
       
        radianes = math.radians(args[1])
        #print math.degrees(radianes)
        if str(math.degrees(radianes)) == "360.0": radianes = 0
        self.punto = [math.cos(radianes) * 50, math.sin(radianes) * 50]
        
        dibujo = (self.punto[0] + self.size[0]/2 - 2, self.punto[1] + self.size[1]/2 - 2)
        self.punto = self.puntero.to_window(dibujo[0],dibujo[1],relative = False)
        self.puntero.pos = dibujo

        #int self.puntero.to_window(dibujo[0],dibujo[1],relative = True)

        
        # with self.canvas:
            # Color(0,1,1,1)
            # Ellipse(size = (4,4), pos = dibujo)
            # Ellipse(size = (4,4), pos = (200,200))
        #print dibujo
        
    def animate_player(self, *args):
        a = Animation(scale = .9 , d = 1.0 / 3.0 , t = 'in_expo') + Animation(scale = 1 , d = 1.0 / 3.0 , t = 'out_expo')
        a.start(self.Display)
        self.last_anim = a
        
        
class PlayScreen(RelativeLayout):
    def __init__(self, **kwargs):
        super(PlayScreen, self).__init__(**kwargs)
        
        #self.add_widget(Asteroide(size = (dp(64),dp(64)) ))
        #self.add_widget(Asteroide(size = (dp(124),dp(124)), pos = (100,100) ))
        #self.add_widget(Image(size = (2000,2000),size_hint = (None,None), pos_hint = {'center_y':.5, 'center_x':.5}))
        self.arrows_states = [False,False,False,False]
        self.pad = [0,0]
        self.player1pos = (0,0)
        self.angle = 0
        self.Display_root = StencilView(size = (Window.size)); self.add_widget(self.Display_root)
        
        self.player = Jugador(size = (75 * 0.60,98 * 0.60), pos = (25,25), size_hint = (None,None))

        self.add_widget(self.player)
        

       
        
        #self.Display.Anchor = (.5,.5)
        #x = Animation(rotation = 90 , d = 1 , t = 'out_expo') + Animation(rotation = 0 , d = 1 , t = 'out_expo')
        #x.start(self.Display)
        #x.repeat = True
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self.RightJoystick = Joystick(size_hint = (.40,.40), pos = (Window.width * .60,dp(24)), opacity = 1)
        self.LeftJoystick = Joystick(size_hint = (.40,.40), pos = (0,dp(24)), opacity = 1)
        self.RightJoystick.bind(pad=lambda *args: self.R_update_coordinates(*args))
        self.LeftJoystick.bind(pad=lambda *args: self.L_update_coordinates(*args))
        self.add_widget(self.RightJoystick)
        self.add_widget(self.LeftJoystick)
        Clock.schedule_interval(self.update, 1.0 / 60.0)
        Clock.schedule_interval(self.agregar_asteroide, 0.675 )
        
    def agregar_asteroide(self,*args):
        import random
        r = random.random()
        self.add_widget(Asteroide(size_hint = (None,None), size = (r*64,r*64) ))
    def R_update_coordinates(self, joystick, pad):

        self.angle = str(joystick.angle)[0:5]
        if float(self.angle) == 0:
            pass
        else:
            self.player.rotation = float(self.angle)
      
    def L_update_coordinates(self, joystick, pad):
        self.pad[0] = str(pad[0])[0:5]
        self.pad[1] = str(pad[1])[0:5]
        #print self.pad
        if float(self.pad[0]) > 1.2: self.pad[0] = str(float(self.pad[0]) % 1)
        if float(self.pad[1]) > 1.2: self.pad[1] = str(float(self.pad[1]) % 1)
     


     
    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def update(self,*args):
        self.player.pos = (self.player.pos[0] + (float(self.pad[0])*4),self.player.pos[1] + (float(self.pad[1])*4))
        
       
        # with self.Display.canvas:
            # Color(0.09803921568627451, 1.0, 0.3215686274509804, 1.0)
            # self.player1 = Rectangle(pos = (self.player1pos[0],self.player1pos[1]), size = (64,64))
            

            

 
            
    
        

        
        
        
        
class Crud(App):
    def build(self):
        return PlayScreen()

if __name__ == '__main__':
    Crud().run()
