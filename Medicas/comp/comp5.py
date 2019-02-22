#!/usr/bin/env python
# -*- coding: utf-8 -*-


















from __init__ import *


patch = os.path.dirname(os.path.abspath(__file__))
asset = patch + '/assets/drawable-mdpi/'
color = patch + '/colors/'
font = patch + '/fonts/'
#Window.size = (360,640)
Window.clearcolor = (1,1,1,1)
kv = '''
<MyButton>:
    size_hint: 1, None
    size: self.texture_size
'''
Builder.load_string(kv)
from shadowedrelatlayout import SHRelativeLayout
Window.size = (360,640)
class MyButton(Button):
    pass
class Comp5_TXI(RelativeLayout):
    def __init__(self, **kwargs):
        super(Comp5_TXI, self).__init__(**kwargs)
        self.N = False
        try:
            if kwargs["N"] != False: self.N = True
        except:
            pass
        self.size_hint_y = None

        self.height = dp(65)
        if self.N == False:
            parentgrid = GridLayout(cols = 1); self.add_widget(parentgrid)
            TXI = TextInput(padding = [dp(20),dp(16),0,0], size_hint_x = .9, pos_hint = {'center_x':.5},size_hint_y = None, height = dp(48), background_normal = asset + "Rectangle 1425.png",background_active = asset + "Rectangle 1425.png"); self.add_widget(TXI)
            Title = Label(text = "[color=#39939A][b][size=10sp]"+kwargs["text"],size_hint_x = self.size_hint_x,width = Window.width*self.size_hint_x, y = self.height - dp(15), markup = True,size_hint_y = None, height = dp(15), text_size = ((Window.width*.8) , dp(15)), halign = 'left', valign = 'middle'); self.add_widget(Title)
        else:
            parentgrid = GridLayout(cols = 1); self.add_widget(parentgrid)
            TXI = TextInput(padding = [dp(20),dp(16),0,0], size_hint_x = .7, pos_hint = {'x':.15},size_hint_y = None, height = dp(48), background_normal = asset + "Rectangle 1425.png",background_active = asset + "Rectangle 1425.png"); self.add_widget(TXI)
            Title = Label(text = "[color=#39939A][b][size=10sp]"+kwargs["text"],size_hint_x = self.size_hint_x,width = Window.width*self.size_hint_x, y = self.height - dp(15), markup = True,size_hint_y = None, height = dp(15), text_size = ((Window.width*.6) , dp(15)), halign = 'left', valign = 'middle'); self.add_widget(Title)
            
        


class Comp5(SHRelativeLayout):
    def __init__(self, **kwargs):
        super(Comp5, self).__init__(**kwargs)
        self.add_widget(Image(source = color + "16.png", keep_ratio = False, allow_stretch = True))
        scrollview = ScrollView(); self.add_widget(scrollview)
        parentgrid = GridLayout(cols = 1,spacing = dp(14),padding = [0,dp(91),0,0], size_hint_y = None, height = dp(2300)); scrollview.add_widget(parentgrid)
        
        parentgrid.add_widget(Label(text = "[color=#39939A][b][size=20sp]Solicitar Adscripcion[/b][size=16sp]\n[size=14sp]\nRellena el siguiente formulario para poder \nrealizar tu solicitud.",text_size = ((Window.width*self.size_hint_x) , dp(78)),halign = 'center', valign = 'middle',markup = True,size_hint_y = None, height = dp(78)))
        parentgrid.add_widget(Label(text = "[color=#39939A][b]Datos personales y demograficos Del Solicitante",markup = True,size_hint_y = None, height = dp(40),halign = 'center', text_size = ((Window.width*self.size_hint_x),dp(40))))
        parentgrid.add_widget(Comp5_TXI(text = "1.Cedula"))
        parentgrid.add_widget(Comp5_TXI(text = "2.Nombre"))
        parentgrid.add_widget(Comp5_TXI(text = "3.Apellidos"))
        parentgrid.add_widget(Label(text = "[color=#39939A][b]Direccion", text_size = ((Window.width*self.size_hint_x)*.9,dp(16)),markup = True,size_hint_y = None, height = dp(16)))
        parentgrid.add_widget(Comp5_TXI(text = "4.1 Calle",N = False))
        parentgrid.add_widget(Comp5_TXI(text = "4.2 No.Casa",N = False))
        parentgrid.add_widget(Comp5_TXI(text = "4.3 Sector",N = False))
        parentgrid.add_widget(Comp5_TXI(text = "4.4 Provincia",N = False))
        parentgrid.add_widget(Label(text = "[color=#39939A][b]Telefonos", text_size = ((Window.width*self.size_hint_x)*.9,dp(16)),markup = True,size_hint_y = None, height = dp(16)))
        parentgrid.add_widget(Comp5_TXI(text = "5.1 Celular",N = True))
        parentgrid.add_widget(Comp5_TXI(text = "5.2 Residencial",N = True))
        parentgrid.add_widget(Comp5_TXI(text = "6.Correo Electronico",N = False))
        parentgrid.add_widget(Label(text = "[color=#39939A][b]Referencias Personales", text_size = ((Window.width*self.size_hint_x)*.9,dp(16)),markup = True,size_hint_y = None, height = dp(16)))
        scrollview1 = ScrollView(size_hint_y = None, height = dp(250)); parentgrid.add_widget(scrollview1)
        parentgrid1 = GridLayout(cols = 7,size_hint = (None,None), width = dp(700), height = dp(300),spacing = dp(1)); scrollview1.add_widget(parentgrid1)
        fields = ["Cedula","Nombre","Apellidos","Telefono Celular","Telefono Residencial","Telefono Oficina","Correo Electronico"]
        for field in fields: parentgrid1.add_widget(Button(text = "[b][size=14sp]"+field , markup = True, text_size = (dp(100),dp(20)) , halign = 'center', valign = 'middle', size_hint_y = None, height =dp(20), background_normal = color + "17.png", background_down = color + "17.png")) 
        for i in range(parentgrid1.cols): parentgrid1.add_widget(Image(size_hint_y = None, height = dp(1), source = color + "17.png", keep_ratio = False, allow_stretch = True))
        
        parentgrid.add_widget(Button(on_release = lambda x: self.AddReferencia(),text = "Añadir referencia personal",size_hint_y = None, height = dp(54), background_normal = color + "17.png", background_down = color + "17b.png"))
        
        parentgrid.add_widget(Label(text = "[color=#39939A][b]Referencias Laborales", text_size = ((Window.width*self.size_hint_x)*.9,dp(16)),markup = True,size_hint_y = None, height = dp(16)))
        scrollview1 = ScrollView(size_hint_y = None, height = dp(250)); parentgrid.add_widget(scrollview1)
        parentgrid1 = GridLayout(cols = 7,size_hint = (None,None), width = dp(700), height = dp(300),spacing = dp(1)); scrollview1.add_widget(parentgrid1)
        fields = ["Cedula","Nombre","Apellidos","Telefono Celular","Telefono Residencial","Telefono Oficina","Correo Electronico"]
        for field in fields: parentgrid1.add_widget(Button(text = "[b][size=14sp]"+field , markup = True, text_size = (dp(100),dp(20)) , halign = 'center', valign = 'middle', size_hint_y = None, height =dp(20), background_normal = color + "17.png", background_down = color + "17.png")) 
        for i in range(parentgrid1.cols): parentgrid1.add_widget(Image(size_hint_y = None, height = dp(1), source = color + "17.png", keep_ratio = False, allow_stretch = True))
        
        parentgrid.add_widget(Button(on_release = lambda x: self.AddReferencia(),text = "Añadir referencia Laboral",size_hint_y = None, height = dp(54), background_normal = color + "17.png", background_down = color + "17b.png"))
        parentgrid.add_widget(Label(text = "[color=#39939A][b]Referencias Comerciales", text_size = ((Window.width*self.size_hint_x)*.9,dp(16)),markup = True,size_hint_y = None, height = dp(16)))
        scrollview1 = ScrollView(size_hint_y = None, height = dp(250)); parentgrid.add_widget(scrollview1)
        parentgrid1 = GridLayout(cols = 7,size_hint = (None,None), width = dp(700), height = dp(300),spacing = dp(1)); scrollview1.add_widget(parentgrid1)
        fields = ["Cedula","Nombre","Apellidos","Telefono Celular","Telefono Residencial","Telefono Oficina","Correo Electronico"]
        for field in fields: parentgrid1.add_widget(Button(text = "[b][size=14sp]"+field , markup = True, text_size = (dp(100),dp(20)) , halign = 'center', valign = 'middle', size_hint_y = None, height =dp(20), background_normal = color + "17.png", background_down = color + "17.png")) 
        for i in range(parentgrid1.cols): parentgrid1.add_widget(Image(size_hint_y = None, height = dp(1), source = color + "17.png", keep_ratio = False, allow_stretch = True))
        
        parentgrid.add_widget(Button(on_release = lambda x: self.AddReferencia(),text = "Añadir referencia Comercial",size_hint_y = None, height = dp(54), background_normal = color + "17.png", background_down = color + "17b.png"))
        parentgrid.add_widget(Button(text = "[color=#245F64][b]CONFIRMAR SOLICITUD",markup = True,size_hint_y = None, height = dp(54), background_normal = color + "17.png", background_down = color + "17b.png"))
    def AddReferencia(self,**kwargs):
        scrollview = ScrollView(size_hint = (1,1)) ; self.parent.add_widget(scrollview)
        parent_r = RelativeLayout(size_hint_y = None, height = dp(700)) ; scrollview.add_widget(parent_r)
        parent_cols = GridLayout(cols = 1,padding = [dp(20),dp(0),dp(20),0]) ; parent_r.add_widget(parent_cols)
        parent_cols.add_widget(Label(size_hint_y = None , height = dp(54)))
        parent = SHRelativeLayout(opacity = 0,size_hint = (1,1),pos_hint = {'center_x':.5}) ; parent_cols.add_widget(parent)
        parent_cols.add_widget(Label(size_hint_y = None , height = dp(54)))
        parent.add_widget(Image(source = color + "16.png", keep_ratio = False , allow_stretch = True))
        x = Animation(opacity = 1, d = .5 , t = 'out_expo') ; x.start(parent)
        
        fields = ["Cedula","Nombre","Apellidos","Telefono Celular","Telefono Residencial","Telefono Oficina","Correo Electronico"]
        colgrid = GridLayout(cols = 1,padding = [0,dp(20),0,0]); parent.add_widget(colgrid)
        colgrid.add_widget(Label(text = "[color=#39939A][b][size=20sp]Añadir Referencia[/b][size=16sp]\n[size=14sp]\nRellena el siguiente formulario para poder \nrealizar tu solicitud.",text_size = ((Window.width*self.size_hint_x) , dp(78)),halign = 'center', valign = 'middle',markup = True,size_hint_y = None, height = dp(78)))
        for field in fields:  colgrid.add_widget(Comp5_TXI(text = field,N = False))
        colgrid.add_widget(Label(size_hint_y = None, height = dp(24)))
        colgrid.add_widget(Button(text = "[color=#245F64][b]CONFIRMAR SOLICITUD",markup = True,size_hint_y = None, height = dp(54), background_normal = color + "17.png", background_down = color + "17b.png"))

        from behavior import CloseBehavior
        self.parent.add_widget(CloseBehavior(R = self.parent))
        
class MyApp(App):
    def build(self):
        return Comp5()
 

if __name__ in ('__main__', '__android__'):
    MyApp().run()

    
    
    
    
    