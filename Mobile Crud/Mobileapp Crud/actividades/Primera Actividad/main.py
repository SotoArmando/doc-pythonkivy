#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __init__ import *

    
class entrada(StencilView):
    def __init__(self,**kwargs):
        super(entrada, self).__init__(**kwargs)
        
        if "pos_hint" in kwargs: self.pos_hint = kwargs["pos_hint"]
        self.mypos_hint()
        self.canvas = Canvas()
        
        with self.canvas:
            self.fbo = Fbo(size=self.size, pos = self.pos)
            self.fbo_color = Color(0.19607843137254902, 0.396078431372549, 1.0, 1.0)
            self.fbo_rect = Rectangle(size= self.size, pos =self.pos )
            

        
        self.pariente = RelativeLayout(); self.add_widget(self.pariente)
     
        self.font_size = dp(17)
        self.entradaTexto = TextInput(text = "asasd", size = self.size, size_hint = (None,None), pos = self.pos, padding = [9,9,0,0],password = kwargs["password"])
        self.entradaTexto.background_normal = color + "None.png"
        self.entradaTexto.background_active = color + "None.png"
        self.entradaTexto.multiline = False
        self.pariente.add_widget(self.entradaTexto)
        self.myon_size()
        
        self.bind(on_size = self.myon_size)
        self.entradaTexto.foreground_color = [1,1,1,1]
        
    def mypos_hint(self):
        try:
            if self.pos_hint["center_x"] : self.x = (Window.width * self.pos_hint["center_x"]) - self.width/2
            if self.pos_hint["center_y"] : self.y = (Window.height * self.pos_hint["center_y"]) - self.height/2
            if (self.x) and (self.y): self.pos = (self.x,self.y)
        except:pass
        
    def myon_size(self,*args): 
        print "gol"
        self.fbo.size = self.size
        self.mypos_hint()
        xpos = self.to_window(0, 0, initial=False, relative=True)
    
        self.entradaTexto.pos = self.pos
        self.entradaTexto.canvas.clear()


        self.fbo = Fbo(size=self.size)
        self.fbo_color = Color(1, 0, 0, 1)
        self.fbo_rect = Rectangle(size= self.size)

    def on_text(self,*args):
        print args

class Main(RelativeLayout):#COMPLEMENTO 'PARENT' EL PROYECTO
    def __init__(self, **kwargs):
        super(Main, self).__init__(**kwargs)
        self.canvas = Canvas()
        with self.canvas:
            Color(0.19607843137254902, 0.396078431372549, 1.0, 1.0)
            Rectangle(size= Window.size, pos =self.pos  ,texture = Gradient.vertical((1, 1, 1, .75), (1, 1, 1, 1) ))
            Rectangle(size = (dp(70),dp(66)), source = asset + "chef.png", pos = (dp(9),Window.height - dp(70) - dp(6)))
        cuadro1 = entrada(size_hint = (None,None),size = (dp(300),dp(34)), pos_hint = {'center_x':.5, 'center_y':.5}, password = False)
        cuadro2 = entrada(size_hint = (None,None),size = (dp(300),dp(34)), pos_hint = {'center_x':.5, 'center_y':.39}, password = True)
       
        
    

        self.add_widget(Label(text = "[size=17]Codicookingtimer\n[size=14]Inicio",markup = True , top = Window.height, size_hint_y = None , height = dp(54*2), text_size = (Window.width/2, dp(54)), halign = 'left', valign = 'top'))
        
        self.add_widget(Label(text = "Usuario",pos_hint = {'center_x':.5, 'center_y':.55},text_size = (dp(300) - dp(9), None), halign = 'left'))
        self.add_widget(cuadro1)
        self.add_widget(Label(text = "Contraseña",pos_hint = {'center_x':.5, 'center_y':.44},text_size = (dp(300) - dp(9), None), halign = 'left'))
        self.add_widget(cuadro2)
        self.add_widget(Label(text = "Has olvidado tu contraseña?[b] recuperala", markup = True,pos_hint = {'center_x':.5, 'center_y':.30}, background_normal = color + "None.png", size_hint = (None,None), size = (dp(124),dp(64))))
        self.add_widget(Button(text = "Iniciar Sesion",pos_hint = {'center_x':.5, 'center_y':.21},background_down = color +"10.png", background_normal = color + "None.png", size_hint = (None,None), size = (dp(124),dp(64))))




        # x = Animation(height = dp(54), d = .5 , t = 'out_expo') + Animation(height = dp(34), d = .5 , t = 'out_expo')
        # x.repeat = True
        # x.bind(on_progress = cuadro1.myon_size)
        # x.start(cuadro1)

class MainApp(App):
    def build(self):
        return Main()
 

if __name__ in ('__main__', '__android__'):
    MainApp().run()

    
    
    
    
    