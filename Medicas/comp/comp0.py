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
        self.size_hint_x = None
        self.width = dp(64)
        self.sel = None
        self.img = Image(size_hint = (.75,.90), pos_hint = {'center_x':.5, 'center_y':.65}, source = kwargs["source"], keep_ratio = True, allow_stretch = True)
        self.label = Label(font_size = sp(12),markup = True,text = "[color=#000000]"+kwargs["text"],size_hint = (1,None), height = dp(50), pos_hint = {"center_y":.25})
        self.add_widget(self.img)
        self.add_widget(self.label)
    
    
        self.behavior = Button(opacity = 0, on_release = lambda x: self.animate())
        self.add_widget(self.behavior)
        
    def animate(self):
        print "hola"
        x = Animation(size_hint = (1,1), d = .1 , t = 'in_quad') + Animation(size_hint = (.75,.90), d = .1 , t = 'out_quad')
        x.start(self.img)
        
class Comp0(RelativeLayout):
    def __init__(self, **kwargs):
        super(Comp0, self).__init__(**kwargs)
        
        self.add_widget(Image(source = color + "16.png", keep_ratio = False , allow_stretch = True))
        parent = GridLayout(rows = 1, padding = [dp(20),0,dp(20),0])
        self.x0 = Boton(text = "[b]Paquetes",source = asset + "Group 68.png")
        self.x1 = Boton(text = "[b]Ruta",source = asset + "Group 69.png")
        self.x2 = Boton(text = "[b]Perfil",source = asset + "Group 72.png")
        self.x3 = Boton(text = "[b]Otros",source = asset + "Group 73.png")

        parent.add_widget(Label())
        parent.add_widget(self.x0)
        parent.add_widget(self.x1)
        #parent.add_widget(Boton(text = "[b]Cobrar",source = asset + "Group 70.png"))
        #parent.add_widget(Boton(text = "[b]Depositar",source = asset + "Group 71.png"))
        parent.add_widget(self.x2)
        parent.add_widget(self.x3)
        parent.add_widget(Label())
        self.size_hint_y = None
        self.height = dp(87)
        self.add_widget(parent)
        self.add_widget(Image(pos_hint = {"y":1},source = asset + "Repeat Grid 2.png",size_hint_y = None , height = dp(5), keep_ratio = False ,allow_stretch = True))
        #self.add_widget(Image(source = asset + "Repeat Grid 2.png",size_hint_x = None , height = dp(10), keep_ratio = False ,allow_stretch = True))
            
        




    def funcion(self):
        print("hola")
        
class MyApp(App):
    def build(self):
        return Comp0()
 

if __name__ in ('__main__', '__android__'):
    MyApp().run()

    
    
    
    
    