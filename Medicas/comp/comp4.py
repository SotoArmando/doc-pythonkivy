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
class MyButton(Button):
    pass
class Details(RelativeLayout):
    def __init__(self, **kwargs):
        super(Details, self).__init__(**kwargs)

Window.size = (360,640)
class Comp4_TXI(RelativeLayout):
    def __init__(self, **kwargs):
        super(Comp4_TXI, self).__init__(**kwargs)
        print self.width
        if self.size_hint_x == None:
            self.TXI = TextInput(hint_text = kwargs["hint_text"],padding = [dp(5+24),dp(49-25),0,0],font_size = sp(20),background_normal = color + "16.png",background_active = color + "16.png",multiline = False);self.add_widget(self.TXI)
            self.add_widget(Image(source = color + "17.png",size_hint = (None,None), size = (self.width - dp(10) - dp(24*2),dp(1)),y = dp(13), pos_hint = {'center_x':.5}, keep_ratio = False , allow_stretch = True))
            self.add_widget(Label(text = "[color=#39939A]"+kwargs["text"],markup = True,size_hint = (None,None), size = (self.width - dp(10),dp(20)), text_size = (self.width - dp(10) - dp(24*2),dp(20)),y = self.height - dp(14),halign = 'left',valign = 'bottom', pos_hint = {'center_x':.5}, keep_ratio = False , allow_stretch = True))
        else:
            self.TXI = TextInput(hint_text = kwargs["hint_text"],padding = [dp(5+24),dp(49-25),0,0],font_size = sp(20),background_normal = color + "16.png",background_active = color + "16.png",multiline = False);self.add_widget(self.TXI)
            self.add_widget(Image(source = color + "17.png",size_hint = (None,None), size = (Window.width - dp(10) - dp(24*2),dp(1)),y = dp(13), pos_hint = {'center_x':.5}, keep_ratio = False , allow_stretch = True))
            self.add_widget(Label(text = "[color=#39939A]"+kwargs["text"],markup = True,size_hint = (None,None), size = (Window.width - dp(10),dp(20)), text_size = (Window.width - dp(10) - dp(24*2),dp(20)),y = self.height - dp(14),halign = 'left',valign = 'bottom', pos_hint = {'center_x':.5}, keep_ratio = False , allow_stretch = True))
        
class Comp4(SHRelativeLayout):
    def __init__(self, **kwargs):
        super(Comp4, self).__init__(**kwargs)
        self.add_widget(Image(source = color + "16.png", keep_ratio = False, allow_stretch = True))
        
        parentgrid = GridLayout(cols = 1,padding = [0,dp(20),0,0]);self.add_widget(parentgrid)
        parentgrid_rowgrid_parent = RelativeLayout(size_hint_y = None, height = dp(48)); parentgrid.add_widget(parentgrid_rowgrid_parent)
        parentgrid_rowgrid = GridLayout(rows = 1); parentgrid_rowgrid_parent.add_widget(parentgrid_rowgrid)
        parentgrid_rowgrid.add_widget(Button(background_normal = asset + "Group 297.png",background_down = asset + "Group 297.png",size_hint_x = None , width = dp(48), on_release = lambda x: self.dummycurrent(current = "0")))
        self.title = Label(text = "[b][color=#39939A]SELECCIONAR METODO",markup = True, text_size = (Window.width,dp(48)) , halign = 'center', valign = 'middle')
        parentgrid_rowgrid_parent.add_widget(self.title)
        
        self.sc = ScreenManager(); parentgrid.add_widget(self.sc)
        sc_screen0 = Screen(name = "0"); self.sc.add_widget(sc_screen0)
        sc_screen0grid_colgrid = GridLayout(cols = 1,size_hint_y = 1,spacing = dp(4),padding = [0,dp(11),0,0]); sc_screen0.add_widget(sc_screen0grid_colgrid)
        sc_screen0grid_colgrid.add_widget(Button(background_normal = color + "17.png", background_down = color + "18.png",size_hint_y = None, height = dp(68), text ="[b]TARJETA",markup = True, on_release = lambda x: self.dummycurrent(current = "1")))
        sc_screen0grid_colgrid.add_widget(Button(background_normal = color + "17.png", background_down = color + "18.png",size_hint_y = None, height = dp(68), text ="[b]CONTRA ENTREGA",markup = True, on_release = lambda x: self.dummycurrent(current = "2")))
        sc_screen0grid_colgrid.add_widget(Button(background_normal = color + "17.png", background_down = color + "18.png",size_hint_y = None, height = dp(68), text ="[b]DEPOSITO",markup = True, on_release = lambda x: self.dummycurrent(current = "3")))
        
        sc_screen1 = Screen(name = "1"); self.sc.add_widget(sc_screen1)
        sc_screen1grid_colgrid = GridLayout(cols = 1,size_hint_y = 1,spacing = dp(4),padding = [dp(0),dp(11),dp(0),0]); sc_screen1.add_widget(sc_screen1grid_colgrid)
        sc_screen1grid_colgrid_rowgrid = GridLayout(rows = 1,padding = [dp(16),dp(0),dp(16),0],size_hint_y = None , height = dp(48)); sc_screen1grid_colgrid.add_widget(sc_screen1grid_colgrid_rowgrid)
        sc_screen1grid_colgrid_rowgrid.add_widget(Image(source = asset + "Group 303.png"))
        sc_screen1grid_colgrid_rowgrid.add_widget(Image(source = asset + "Group 302.png"))
        sc_screen1grid_colgrid_rowgrid.add_widget(Image(source = asset + "Group 301.png"))
        sc_screen1grid_colgrid.add_widget(Label(size_hint_y = None, height = dp(45)))
        sc_screen1grid_colgrid.add_widget(Comp4_TXI(text = "[b]CARD NUMBER" ,hint_text = "0000 0000 0000 0000", size_hint_y = None, height = dp(68)))
        sc_screen1grid_colgrid.add_widget(Comp4_TXI(text = "[b]CARDHOLDER NAME" ,hint_text = "NOMBRES APELLIDOS", size_hint_y = None, height = dp(68)))
        sc_screen1grid_colgrid_rowgrid1 = GridLayout(rows = 1,size_hint_y = None , height = dp(68)); sc_screen1grid_colgrid.add_widget(sc_screen1grid_colgrid_rowgrid1)
        sc_screen1grid_colgrid_rowgrid1.add_widget(Comp4_TXI(size_hint_x = None, width = (Window.width*self.size_hint_x)/2,text = "[b]EXPIRE DATE" ,hint_text = "00/00", size_hint_y = None, height = dp(68)))
        sc_screen1grid_colgrid_rowgrid1.add_widget(Comp4_TXI(size_hint_x = None, width = (Window.width*self.size_hint_x)/2,text = "[b]CVV" ,hint_text = "123", size_hint_y = None, height = dp(68)))
        sc_screen1grid_colgrid_rowgrid2 = GridLayout(rows = 1,size_hint_y = None , height = dp(50),padding = [dp(16),dp(0),dp(0),0]); sc_screen1grid_colgrid.add_widget(sc_screen1grid_colgrid_rowgrid2)
        sc_screen1grid_colgrid_rowgrid2.add_widget(CheckBox(background_checkbox_normal = asset + "Rectangle 1423.png",background_checkbox_down = asset + "uncheck.png",size_hint_x = None, width = dp(50),text = "[color=#0000000]recordar", markup = True))
        sc_screen1grid_colgrid_rowgrid2.add_widget(Label(text_size = ((Window.width*self.size_hint_x) - dp(50) - dp(32), dp(50)),halign = 'left', valign = 'middle',text = "[color=#39939A][b]Recordar targeta", markup = True))
        sc_screen1grid_colgrid.add_widget(Label())
        sc_screen1grid_colgrid.add_widget(Button(text = "[b]CONFIRMAR PAGO", size_hint_y = None, height = dp(124),markup = True, background_normal = color + "17.png",background_down = color + "18.png",))
        
        sc_screen2 = Screen(name = "2"); self.sc.add_widget(sc_screen2)
        sc_screen2grid_colgrid = GridLayout(cols = 1,size_hint_y = 1,spacing = dp(4),padding = [dp(0),dp(11),dp(0),0]); sc_screen2.add_widget(sc_screen2grid_colgrid)
        sc_screen2grid_colgrid.add_widget(Label(markup = True,size_hint_y = None, height = dp(150), text = "[color=#39939A][size=40]423.00 RD$\n[size=16]January 27, 2017 - 3:45 PM\n[size=14]Coffee & Tea", text_size = ((Window.width*self.size_hint_x), dp(150)), halign = 'center', valign = 'middle'))
        sc_screen2grid_colgrid.add_widget(Button(markup = True,size_hint_y = None, height = dp(54), text = "Zona Universitaria, Av.Jose Contreras #78",background_normal = color + "17.png", text_size = ((Window.width*self.size_hint_x), dp(54)), halign = 'center', valign = 'middle'))
        self.sc_screen2grid_colgrid1 = GridLayout(cols = 2,padding = [dp(25),0,dp(25),0]); sc_screen2grid_colgrid.add_widget(self.sc_screen2grid_colgrid1)
        sc_screen2grid_colgrid.add_widget(Button(text = "[b]CONFIRMAR PAGO", size_hint_y = None, height = dp(124),markup = True, background_normal = color + "17.png",background_down = color + "18.png"))
        
        
        
        sc_screen3 = Screen(name = "3"); self.sc.add_widget(sc_screen3)
        sc_screen3grid_colgrid = GridLayout(cols = 1,size_hint_y = 1,spacing = dp(4),padding = [0,dp(11),0,0]); sc_screen3.add_widget(sc_screen3grid_colgrid)
        sc_screen3relat = RelativeLayout(height = dp(268+40), size_hint_y = None); sc_screen3grid_colgrid.add_widget(sc_screen3relat)
        sc_screen3relat.add_widget(Image(source = color + "16b.png",keep_ratio = False, allow_stretch = True))
        sc_screen3relat_SH = SHRelativeLayout(size_hint = (.9,.9),pos_hint = {'center_x':.5, 'center_y':.5}); sc_screen3relat.add_widget(sc_screen3relat_SH)
        sc_screen3relat_SH.add_widget(Image(source = color + "16.png",keep_ratio = False, allow_stretch = True))
        sc_screen3relat_SH.add_widget(Image(source = asset + "Group 310.png", size_hint = (None,None), size = (dp(64),dp(64)), pos_hint = {'center_y':.5,'center_x':.5}))
        sc_screen3relat_SH.add_widget(Label(size_hint_y = .5,markup = True, text = "[color=#39939A][size=20]Envianos la foto del deposito.\n[size=14]2.45 MB, 09/09/2016",halign ='center', valign = 'middle',text_size = ((Window.width*self.size_hint_x)*.9 - dp(32), (dp(268+40)*.9)) ))
        self.sc_screen3grid_colgrid1 = GridLayout(cols = 2,padding = [dp(25),0,dp(25),0]); sc_screen3grid_colgrid.add_widget(self.sc_screen3grid_colgrid1)
        sc_screen3grid_colgrid.add_widget(Button(text = "[b]CONFIRMAR PAGO", size_hint_y = None, height = dp(124),markup = True, background_normal = color + "17.png",background_down = color + "18.png"))

        self.loaditems() #SOLO PARA PRUEBAS
    def loaditems(self):
        self.sc_screen2grid_colgrid1.clear_widgets()
        self.sc_screen3grid_colgrid1.clear_widgets()
        
        items = [{"item":"Item 1","price":"300.00"},{"item":"Item 2","price":"300.00"},{"item":"Item 3","price":"300.00"}]
        for i in items:
            self.sc_screen2grid_colgrid1.add_widget(Label(markup = True,text_size = (Window.width/2, dp(24)), size_hint_y = None, height = dp(24), text = "[color=#39939A]"+i["item"], halign = 'left', valign = 'middle'))
            self.sc_screen2grid_colgrid1.add_widget(Label(markup = True,text_size = (Window.width/2, dp(24)), size_hint_y = None, height = dp(24), text = "[color=#39939A][b]"+"$"+i["price"], halign = 'right', valign = 'middle'))
            
            self.sc_screen3grid_colgrid1.add_widget(Label(markup = True,text_size = (Window.width/2, dp(24)), size_hint_y = None, height = dp(24), text = "[color=#39939A]"+i["item"], halign = 'left', valign = 'middle'))
            self.sc_screen3grid_colgrid1.add_widget(Label(markup = True,text_size = (Window.width/2, dp(24)), size_hint_y = None, height = dp(24), text = "[color=#39939A][b]"+"$"+i["price"], halign = 'right', valign = 'middle'))
            
            
        res = ["Subtotal","ITBIS","Propina"]
        self.sc_screen2grid_colgrid1.add_widget(Label(markup = True,text_size = (Window.width/2, dp(24)), size_hint_y = None, height = dp(24), text = "[color=#39939A]", halign = 'left', valign = 'middle'))
        self.sc_screen2grid_colgrid1.add_widget(Label(markup = True,text_size = (Window.width/2, dp(24)), size_hint_y = None, height = dp(24), text = "[color=#39939A]", halign = 'right', valign = 'middle'))
        for i in res:
            self.sc_screen2grid_colgrid1.add_widget(Label(markup = True,text_size = (Window.width/2, dp(24)), size_hint_y = None, height = dp(24), text = "[color=#39939A]"+i, halign = 'left', valign = 'middle'))
            self.sc_screen2grid_colgrid1.add_widget(Label(markup = True,text_size = (Window.width/2, dp(24)), size_hint_y = None, height = dp(24), text = "[color=#39939A][b]"+"$"+"0", halign = 'right', valign = 'middle'))
            
            self.sc_screen3grid_colgrid1.add_widget(Label(markup = True,text_size = (Window.width/2, dp(24)), size_hint_y = None, height = dp(24), text = "[color=#39939A]"+i, halign = 'left', valign = 'middle'))
            self.sc_screen3grid_colgrid1.add_widget(Label(markup = True,text_size = (Window.width/2, dp(24)), size_hint_y = None, height = dp(24), text = "[color=#39939A][b]"+"$"+"0", halign = 'right', valign = 'middle'))
            
            
            
    def dummycurrent(self,**kwargs):
        somenames = ["[b][color=#39939A]SELECCIONAR METODO","[b][color=#39939A]PAGO POR TARJETA","[b][color=#39939A]PAGO CONTRA ENTREGA","[b][color=#39939A]PAGO POR DEPOSITO"]
        xa = Animation(opacity = 0, d = .25, t = 'out_quad' ) 
        xb = Animation(opacity = 1, d = .25, t = 'out_quad' )

        def change(): 
            self.title.text = somenames[int(kwargs["current"])]
            xb.start(self.title)
        xa.bind(on_complete = lambda x,y: change())
        xa.start(self.title)
        self.sc.current = kwargs["current"]
    def funcion(self):
        print("hola")
        
class MyApp(App):
    def build(self):
        return Comp4()
 

if __name__ in ('__main__', '__android__'):
    MyApp().run()

    
    
    
    
    