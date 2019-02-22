#!/usr/bin/env python
# -*- coding: utf-8 -*-


















from comp.__init__ import *


patch = os.path.dirname(os.path.abspath(__file__))

color = patch + '/colors/'
font = patch + '/fonts/'

os.environ['KIVY_IMAGE'] = 'pil,sdl2'
metrics = MetricsBase()
try:
    android_dpi = metrics.dpi_rounded()
except:
    android_dpi = metrics.dpi_rounded
print android_dpi
asset_dpi = [120,160,240,320,480,640]
asset_dpi2 = ['ldpi','mdpi','hdpi','xhdpi','xxhdpi','xxxhdpi']
patch = os.path.dirname(os.path.abspath(__file__))

color = patch + '/colors/'
sound = patch + '/sounds/'
font = patch + '/comp/fonts/'
hud = patch + '/hud/'

asset = ''
for i in asset_dpi:
    if android_dpi == i:
        asset = patch + '/asset/drawable-'+str(asset_dpi2[asset_dpi.index(i)])+'/'
asset = patch + '/comp/assets/drawable-mdpi/'
        
class InterfaceManager(RelativeLayout):
    def __init__(self, **kwargs):
        super(InterfaceManager, self).__init__(**kwargs)

        from comp.comp0 import Comp0
        from comp.comp1 import Comp1
        from comp.comp2 import Comp2
        from comp.shadowedrelatlayout import SHRelativeLayout
        self.sc = ScreenManager()
        sc1 = Screen(name = "1")
        sc1.add_widget(Comp1())
        self.bottomnav = Comp0()
        self.bottomnav.x0.behavior.bind(on_release = lambda x: self.PaquetesShow())
        self.bottomnav.x1.behavior.bind(on_release = lambda x: self.SolAdscripcionShow())
    
        self.sc.add_widget(sc1)
        self.add_widget(self.sc)
        self.add_widget(self.bottomnav)
        self.add_widget(Comp2())
        
        #---------------------------------------------------------------------------------------------------------------
        self.paquetes = SHRelativeLayout(opacity = 1); layout = GridLayout(cols = 1,padding = [dp(0),dp(0),dp(0),dp(0)])
        self.paquetes.add_widget(Image(source = color + "16.png", keep_ratio = False , allow_stretch = True))
        
        self.paquetes.add_widget(layout)
        
        self.scroll = ScrollView(opacity = 0,size_hint_x = .95, pos_hint = {'center_x':.5}, bar_color = [1,1,1,0])
        parent = GridLayout(cols = 1, size_hint_y = None , height = 1000)
        
        self.paquetes.children[0].add_widget(Label(font_name = font + "Roboto-Bold.ttf" ,markup = True,text = "[color=#39939A][size=18sp][b]Paquetes",size_hint_y = None, height = dp(39), text_size = ((Window.width * .95) - dp(16) , dp(39)),  halign = 'center', valign = 'bottom'))
        self.paquetes.children[0].add_widget(Label(size_hint_y = None, height = dp(8)))
        self.paquetes.children[0].add_widget(Image(opacity = .24,source = color + "3.png", keep_ratio = False ,allow_stretch = True , size_hint = (1,None), height  = dp(1)))
        self.paquetes.children[0].add_widget(Image(opacity = .24,source = color + "3.png", keep_ratio = False ,allow_stretch = True , size_hint = (1,None), height  = dp(1)))
        parent.add_widget(Label(size_hint_y = None, height = dp(120)))
        parent.add_widget(self.paquetes)
        self.scroll.add_widget(parent)
        #---------------------------------------------------------------------------------------------------------------
        
        
        
        self.Notify(N = "Cobrar Paquete")   
        
    def Notify(self,**kwargs):
        if kwargs["N"] == "Cobrar Paquete":
            y = Animation(y = dp(-65), d = .5, t = 'in_back')
            parent = RelativeLayout(pos_hint = {'center_x':.5},y = dp(-65),size_hint = (None,None), size = (dp(327),dp(65)) )
            parent.add_widget(Image(source = color + "17.png",keep_ratio = False, allow_stretch = True))
            parent.add_widget(Label(text_size = (dp(327-48),dp(65)), valign = 'middle',markup = True, line_height = 1.2,text = "[b]Cobrar Paquete\n[i]Orden 10249"))
            button0 = Button(background_normal = asset + "Symbol 1.png",background_down = asset + "Symbol 2.png",size_hint = (None,None), size = (dp(40),dp(40)), pos_hint = {'center_x': .9, 'center_y':.5}, on_release = lambda x: y.start(parent))
            parent.add_widget(button0)
            button0.bind(on_release = lambda x: self.PaymentShow())
            self.add_widget(parent)
            x = Animation(y = dp(110), d = .5, t = 'out_expo') + Animation(y = dp(110), d = 1, t = 'in_expo')# + Animation(y = dp(-65), d = .5, t = 'out_quad')
            x.start(parent) 
        if kwargs["N"] == "Cobrar Ruta":
            y = Animation(y = dp(-65), d = .5, t = 'in_back')
            parent = RelativeLayout(pos_hint = {'center_x':.5},y = dp(-65),size_hint = (None,None), size = (dp(327),dp(65)) )
            parent.add_widget(Image(source = asset + "Path 242.png",keep_ratio = False, allow_stretch = True))
            parent.add_widget(Label(text_size = (dp(327-48),dp(65)), valign = 'middle',markup = True, line_height = 1.2,text = "[color=#39939A][b]Desde mi posicion\n[i]Los Restauradores"))
            parent.add_widget(Button(background_normal = asset + "Symbol 2.png",background_down = asset + "Symbol 2.png",size_hint = (None,None), size = (dp(40),dp(40)), pos_hint = {'center_x': .9, 'center_y':.5}, on_release = lambda x: y.start(parent)))
            self.add_widget(parent)
            x = Animation(y = dp(110), d = .5, t = 'out_expo') + Animation(y = dp(110), d = 1, t = 'in_expo')# + Animation(y = dp(-65), d = .5, t = 'out_quad')
            x.start(parent)
            
    def SolAdscripcionShow(self):
        from comp.comp5 import Comp5
        SolAdscripcion = Comp5(size_hint = (.9,.9), y = -Window.height, pos_hint = {'center_x':.5})
        x = Animation(y = -dp(0), d = .5 , t = 'out_expo')
        self.add_widget(SolAdscripcion)
        x.start(SolAdscripcion)
        
        from comp.behavior import CloseBehavior
        self.add_widget(CloseBehavior(R = self, object = SolAdscripcion))
    def PaymentShow(self):
        from comp.comp4 import Comp4
        payment = Comp4(size_hint = (.9,1), y = -Window.height, pos_hint = {'center_x':.5})
        x = Animation(y = -dp(0), d = .5 , t = 'out_expo')
        self.add_widget(payment)
        x.start(payment)
        
        from comp.behavior import CloseBehavior
        self.add_widget(CloseBehavior(R = self))
    def PaquetesShow(self):
        x = Animation(opacity = 1, d = .5 , t = 'out_expo')
        x.start(self.scroll)
        self.add_widget(self.scroll)
        
        layout1 = GridLayout(cols = 1, spacing = dp(8), padding = [dp(8),dp(8),dp(8),0])
        from comp.comp3 import Details
        self.paquetes.children[0].remove_widget(self.paquetes.children[0].children[0])
        self.paquetes.children[0].add_widget(layout1)
        for i in range(4):
            mytext1 = "[color=#39939A][size=16sp][b]Orden 10246[/size][/b][/color][color=#000000][size=12dp]\n\n3 de Noviembre, 2017\nTotal .: $445.00 RD$\nEstado .: [/color][color=#55D45E]Entregada"
            mytext2 = "[color=#39939A][size=16sp][b]Direccion[/b][/size][/color][color=#000000][size=12dp]\nArmando Jose Soto\nLos Restauradores, Av..\nSanto Domingo\nDistrito Nacional"
            layout1.add_widget(Details(text1 = mytext1,text2 = mytext2))
            
        from comp.behavior import CloseBehavior
        self.add_widget(CloseBehavior(R = self))

    
    def funcion(self):
        print("hola")
        
class MyApp(App):
    def build(self):
        Window.size = (360,640)
        return InterfaceManager()
 

if __name__ in ('__main__', '__android__'):
    MyApp().run()

    
    
    
    
    