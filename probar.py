import sys, os
from docs.mind import *

patch = os.path.dirname(os.path.abspath(__file__))
asset = patch + '/docs/_assets/drawable-mdpi/'
sound = patch + '/docs/_sounds/'
behavior = patch + '/docs/_behavior/'
font = patch + '/docs/_fonts/'

print (".: ASSETS DIR",asset)
print (".: FONTS DIR" ,font)
print (".: SOUND DIR" ,sound)
print (".: BEHAVIOR DIR" ,behavior)

Window.size = (360,640)
Window.clearcolor = (1,1,1,1)

class Relatstencil(RelativeLayout,StencilView): pass


class Main(RelativeLayout):
    posx = NumericProperty(0)
    posy = NumericProperty(0)
    opa = NumericProperty(1)
    size_hint_y = NumericProperty(1)
    height = NumericProperty(50)
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        thelabel = Label(markup = True,text = "[b]Añadir Widget", pos = (0,0))
        self.wid = Relatstencil(size = (125,36), size_hint = (None,None), pos = (0,0))
        x = (Animation(posx = 125, opa = .5, d = .5, t = 'in_expo' ) 
        + Animation(posx = 250, opa = 1, d = .5, t = 'out_expo' )
        + Animation(posx = -25, d = 0 ))
        x.repeat = True
        
        y = (
        Animation(y = 0+2.0, d = .25, t = 'in_quart' )
        + Animation(y = 0+4.0, d = .25, t = 'out_quart' ) 
        + Animation(y = 0, d = 1, t = 'out_quart' ) + Animation(y = 0, d = 2 ) )
        
        y.repeat = True
        y.start(thelabel)
        x.start(self)
        
        
        with self.wid.canvas.before:
            Color(1,0,0,1)
            Rectangle(size = (125,100), pos = (0,0),group = "asd")
            Color(1,1,1,1)
            Mesh(vertices=[self.posx+0, self.posy+0, 0, 0,self.posx+75, self.posy+50, 0, 0,self.posx+125, self.posy+50, 0, 0,self.posx+50, self.posy+0, 0, 0], indices=[0,1,2,3], mode = 'triangle_fan',group = "asd")
       
        

    
        self.add_widget(self.wid)
        self.wid.add_widget(thelabel)
  
        
    def change_mode(self, mode, *largs):
        self.mesh.mode = mode

    def on_posx(self,*args):
        self.wid.canvas.before.remove_group("asd")
      
        with self.wid.canvas.before:
            Color(1,0,0,1)
            Rectangle(size = (125,100), pos = (100,100),group = "asd")
            Color(.89,.89,.89,self.opa)
            Mesh(vertices=[self.posx+0, self.posy+0, 0, 0,self.posx+75, self.posy+50, 0, 0,self.posx+125, self.posy+50, 0, 0,self.posx+50, self.posy+0, 0, 0], indices=[0,1,2,3], mode = 'triangle_fan',group = "asd")
            
        
class CodiCookingTimer(App):
    def build(this):
        return Main()

CodiCookingTimer().run()