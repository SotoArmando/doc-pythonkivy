#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __init__ import *
import os   
import os.path
Window.size = (1024,640)
Window.clearcolor = (1,1,1,1)
#CARPETAS DEL PROYECTO
patch = os.path.dirname(os.path.abspath(__file__))
asset = patch + '/assets/drawable-mdpi/'
color = patch + '/colors/'
font = patch + '/fonts/'
C1 = "[color=#13C0C7]"
C4 = "[color=#000000]"
C2 = "[color=#404040]"
C3 = "[color=#ff3333]"
C5 = "[color=#f2f2f2]"
C6 = "[color=#95989A]"
EC = "[/color]"
class ImageButton(ButtonBehavior, Image): pass


class Inspeccion_Layobj(RelativeLayout):
    def __init__(self, **kwargs):
        super(Inspeccion_Layobj, self).__init__(**kwargs)
        self.size_hint_y = None
        self.height = dp(200)
        self.pariente = GridLayout(cols = 1)
        
        self.data = kwargs["data"]

        diminfotxt = RelativeLayout(size_hint_y = None, height = dp(200))
        infotxt = GridLayout(cols = 2, padding = [16,0,16,0])
        diminfotxt.add_widget(infotxt)
        diminfotxt.add_widget(Button(opacity = .04, on_release = lambda x: self.open()))
        
        i = 0



        infotxt.add_widget(Label(opacity = .84,font_size = dp(14),text = "[b]"+"FECHA CREACION"+"[/b]:\n"+self.data["FECHA CREACION"], text_size=(Window.width/2,50), halign = 'left', valign = 'middle', markup = True))
        infotxt.add_widget(Label(opacity = .84,font_size = dp(14),text = "[b]"+"HORA CREACION"+"[/b]:\n"+self.data["HORA CREACION"], text_size=(Window.width/2,50), halign = 'right', valign = 'middle',  markup = True))
      
        
        infotxt.add_widget(Label(opacity = .84,font_size = dp(14),text = "[b]"+"NOMBRES Y APPELLIDOS"+"[/b]:\n"+self.data["NOMBRES Y APPELLIDOS"], text_size=(Window.width/2,50), halign = 'left', valign = 'middle', markup = True))
        infotxt.add_widget(Label())
        infotxt.add_widget(Label(opacity = .84,font_size = dp(14),text = "[b]"+"FECHA DE NACIMIENTO"+"[/b]:\n"+self.data["FECHA DE NACIMIENTO"], text_size=(Window.width/2,50), halign = 'left', valign = 'middle', markup = True))
        infotxt.add_widget(Label())
        
        infotxt.add_widget(Label(opacity = .84,font_size = dp(14),text = "[b]"+"NACIONALIDAD"+"[/b]:\n"+self.data["NACIONALIDAD"], text_size=(Window.width/2,50), halign = 'left', valign = 'middle', markup = True))
        infotxt.add_widget(Label())
        
        infotxt.add_widget(Label(opacity = .84,font_size = dp(14),text = "[b]"+"DNI"+"[/b]:\n"+self.data["DNI"], text_size=(Window.width/2,50), halign = 'left', valign = 'middle', markup = True))
        infotxt.add_widget(Label())
        
        self.t1 = TextInput(text = self.data["DATOS ADICIONALES"],font_size = dp(18),padding = [15,15,0,0],hint_text = "DATOS ADICIONALES",background_normal = color + "3.png",background_active = color + "2.png",size_hint_y = 1 , opacity = 0, foreground_color = (1,1,1,1))
        self.pariente.add_widget(diminfotxt)
        self.pariente.add_widget(self.t1)
        self.add_widget(Image(source = color + "3.png", keep_ratio = False , allow_stretch = True))
        self.add_widget(self.pariente)
        self.add_widget(Image(size_hint_y = None, height = 1, pos_hint = {'center_y': 1}, source = color + "16.png", keep_ratio = False, allow_stretch = True))
    def open(self):
        if self.height == dp(200+250):
        
            a1 = Animation(opacity = 0, d = .5, t = "out_quart")
            a2 = Animation(height = dp(200), d = .5, t= "out_quart")
            a1.start(self.t1)
            a2.start(self)
        else:
            a1 = Animation(opacity = 1, d = .5, t = "out_quart")
            a2 = Animation(height = dp(200+250), d = .5, t= "out_quart")
            a1.start(self.t1)
            a2.start(self)
        
class Inspeccion_Screen(Screen):
    def __init__(self, **kwargs):
        super(Inspeccion_Screen, self).__init__(**kwargs)
        controlesroot = RelativeLayout(size_hint_y = None, height = dp(54), pos_hint = {'y':.0})
        controles = GridLayout(rows = 1)
        controlesroot.add_widget(Image(source = color + "T50.png", keep_ratio = False ,allow_stretch = True ))
        self.add_widget(Image(source = color + "3.png", keep_ratio = False ,allow_stretch = True ))
        textos = ["Agregar","Archivo"]
        for i in range(2):
            dim = RelativeLayout()
            dim.add_widget(Image(source = "attachment.png",size_hint = (None,None), size = (dp(24),dp(24)), keep_ratio = True , allow_stretch = True , pos_hint = {'center_x':.5, 'center_y':.65} ))
            dim.add_widget(ToggleButton(text = str(i),on_release = lambda x: self.dummycurrent(current = x.text),opacity = .24,group = "controles"))
            dim.add_widget(Label(text = textos[i],size_hint = (1,None),height = 50, text_size = (100,50), pos_hint = {'y':.05} , halign = 'center', valign = 'bottom'))
            controles.add_widget(dim)


        self.sc = ScreenManager()
        self.screen0 = Screen(name = "0"); self.sc.add_widget(self.screen0)
        
        
        parientescroll = ScrollView(); self.screen0.add_widget(parientescroll)
        pariente = GridLayout(cols = 1, size_hint_y = None, height = 1000)
        pariente.add_widget(Label(size_hint_y = None, height = dp(79)))
        pariente.add_widget(Button(font_size = dp(18),text = "CONTROL SOCIAL",background_normal = color + "3.png",background_down = color + "3.png",size_hint_y = None , height = dp(54), multiline = False, foreground_color = (1,1,1,1)))
        self.t1 = TextInput(font_size = dp(18),padding = [15,15,0,0],hint_text = "NOMBRES Y APELLIDOS",background_normal = color + "3.png",background_active = color + "2.png",size_hint_y = None , height = dp(54), multiline = False, foreground_color = (1,1,1,1))
        pariente.add_widget(self.t1)
        self.t2 = TextInput(font_size = dp(18),padding = [15,15,0,0],hint_text = "DNI",background_normal = color + "3.png",background_active = color + "2.png",size_hint_y = None , height = dp(54), multiline = False, foreground_color = (1,1,1,1))
        pariente.add_widget(self.t2)
        self.t3 = TextInput(font_size = dp(18),padding = [15,15,0,0],hint_text = "FECHA DE NACIMIENTO",background_normal = color + "3.png",background_active = color + "2.png",size_hint_y = None , height = dp(54), multiline = False, foreground_color = (1,1,1,1))
        pariente.add_widget(self.t3)
        self.t4 = TextInput(font_size = dp(18),padding = [15,15,0,0],hint_text = "NACIONALIDAD",background_normal = color + "3.png",background_active = color + "2.png",size_hint_y = None , height = dp(54), multiline = False, foreground_color = (1,1,1,1))
        pariente.add_widget(self.t4)
        trigrid = GridLayout(rows = 1, size_hint_y = None, height = dp(74))
        trigrid.add_widget(ToggleButton(group = "Gravedad", background_down = color + "2.png",font_size = sp(18),background_normal = color + "3.png", text = "FALTA"))
        trigrid.add_widget(ToggleButton(group = "Gravedad", background_down = color + "2.png",font_size = sp(18),background_normal = color + "3.png", text = "DELITO"))
        trigrid.add_widget(ToggleButton(group = "Gravedad", background_down = color + "2.png",font_size = sp(18),background_normal = color + "3.png", text = "CRIMEN"))
        
        pariente.add_widget(trigrid)
        self.t5 = TextInput(font_size = dp(18),padding = [15,15,0,0],hint_text = "DATOS ADICIONALES",background_normal = color + "3.png",background_active = color + "2.png",size_hint_y = None , height = dp(250), foreground_color = (1,1,1,1))
        pariente.add_widget(self.t5)
        pariente.add_widget(Label(opacity = .14,size_hint_y = None, height = 0 , font_size = dp(18), text_size = (dp(Window.width-25),dp(54)),halign = 'left', valign = 'top', text = "01:55 AM, 15 DE NOVIEMBRE, 2017", markup = True ))

        self.b1 = Button(background_normal = color + "2.png",size_hint_y = None , height = dp(74), text = "CONFIRMAR", font_size = sp(18))
        pariente.add_widget(self.b1)

        pariente.add_widget(Button(background_normal = color + "3.png"))
        parientescroll.add_widget(pariente)
        self.add_widget(self.sc)
        controlesroot.add_widget(controles)
        self.add_widget(controlesroot)
        
        self.screen1 = Screen(name = "1"); self.sc.add_widget(self.screen1)
        self.screen1_scroll = ScrollView()
        self.screen1_pariente = GridLayout(cols = 1, size_hint_y = None, height = 1200)
        self.screen1_scroll.add_widget(self.screen1_pariente)
        self.screen1.add_widget(self.screen1_scroll)
        self.jsondata = kwargs["datarequest"]()
        self.screen1_pariente.add_widget(Label(size_hint_y = None, height = dp(74)))
        
        for i in self.jsondata:self.screen1_pariente.add_widget(Inspeccion_Layobj(data = i))
        
    def dummycurrent(self,**kwargs): self.sc.current = kwargs["current"]
    def json(self):
        data = {}
        data["FECHA CREACION"] = time.strftime("%d/%m/%Y")
        data["HORA CREACION"] = time.strftime("%H:%M:%S %p")
        data["NOMBRES Y APPELLIDOS"] = self.t1.text
        data["DNI"] = self.t2.text
        data["FECHA DE NACIMIENTO"] = self.t3.text
        data["NACIONALIDAD"] = self.t4.text
        data["DATOS ADICIONALES"] = self.t5.text
        
        return data
class MyApp(App):
    def build(self):
        return Inspeccion_Screen()
 

if __name__ in ('__main__', '__android__'):
    MyApp().run()

    
    
    
    
    