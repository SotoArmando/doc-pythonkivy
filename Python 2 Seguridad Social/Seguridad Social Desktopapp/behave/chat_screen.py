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
kv = '''
<MyButton>:
    size_hint: 1, None
    size: self.texture_size
'''
Builder.load_string(kv)
class ImageButton(ButtonBehavior, Image): pass

class MyButton(Button):
    pass
    
class MensajeRecibido(RelativeLayout):
    def __init__(self, **kwargs):
        super(MensajeRecibido, self).__init__(**kwargs)
        self.height = dp(54)

        self.size_hint_y = None
        pariente = GridLayout(rows = 1)
       
        self.add_widget(pariente)
        subdim_text = RelativeLayout()
        subdim_text.add_widget(Image(source = color + "10.png", keep_ratio = False, allow_stretch = True))
        self.mensaje = MyButton(pos_hint = {'center_x':.5,'center_y':.5},background_normal = color + "10.png",background_down = color + "10.png",text_size = (Window.width/2-dp(25),None) , keep_ratio = False , allow_stretch = True, text = kwargs["text"], halign = 'left', valign = 'middle', markup = True)
        subdim_text.add_widget(self.mensaje)

        pariente.add_widget(subdim_text)
        pariente.add_widget(Label())
        
        
        self.mensaje.texture_update() 
        print self.mensaje.texture_size , "H"
        self.size = self.mensaje.texture_size
        self.height += 16
        self.width += 16
        self.opacity = 0
    def animate(self):
        a = Animation(opacity = 1 , d = .5 , t = 'out_expo')
        a.start(self)
class MensajeEnviado(RelativeLayout):
    def __init__(self, **kwargs):
        super(MensajeEnviado, self).__init__(**kwargs)
        self.height = dp(54)

        self.size_hint_y = None
        pariente = GridLayout(rows = 1)
       
        self.add_widget(pariente)
        subdim_text = RelativeLayout()
        subdim_text.add_widget(Image(source = color + "12.png", keep_ratio = False, allow_stretch = True))
        self.mensaje = MyButton(pos_hint = {'center_x':.5,'center_y':.5},background_normal = color + "12.png",background_down = color + "12.png",text_size = (Window.width/2-dp(25),None) , keep_ratio = False , allow_stretch = True,font_size = '18sp', text = kwargs["text"], halign = 'left', valign = 'middle', markup = True)
        subdim_text.add_widget(self.mensaje)
        print self.mensaje.texture_size
        pariente.add_widget(Label())
        pariente.add_widget(subdim_text)
        
        self.mensaje.texture_update() 
        print self.mensaje.texture_size , "H"
        self.size = self.mensaje.texture_size
        self.height += 16
        self.width += 16
        self.opacity = 0
    def animate(self):
        a = Animation(opacity = 1 , d = .5 , t = 'out_quart')
        a.start(self)
class Contacto(RelativeLayout):
    def __init__(self, **kwargs):
        super(Contacto, self).__init__(**kwargs)
        pariente = GridLayout(rows = 1)
        self.nombre = kwargs["Nombre"]
        self.add_widget(Image(source = color + "16.png", keep_ratio = False ,allow_stretch = True))
        self.size_hint_y = None
        self.height = dp(64)

        sub_dim = RelativeLayout(size_hint_x = None, width = dp(80))
        sub_dim.add_widget(Image(source = color + "16.png", keep_ratio = False ,allow_stretch = True))
        sub_dim.add_widget(AsyncImage(size_hint = (.9,.9), pos_hint = {'center_x':.5,'center_y':.5} ,source =  "http://127.0.0.1:8000/media/Group_571.png" ))
        pariente.add_widget(sub_dim)
        pariente.add_widget(Label(text = "[b][color=#000000]"+self.nombre+"[/b]\n[size=14sp][color=#009900][b]En Servicio[/b][/color][color=#000000][/size]\n[size=12sp]50 metros de distancia", text_size = (Window.width - dp(64) - dp(80) - dp(32), self.height ),markup = True, halign = 'left', valign = 'middle'))
        pariente.add_widget(Label(markup = True,opacity = .74,text = "10:45 AM\n50", size_hint_x = None,text_size = (dp(80) - dp(16), dp(50)), width = dp(80), halign = 'right', valign = 'top'))
        self.add_widget(pariente)
        self.add_widget(Image(opacity = .04,size_hint = (1,None), height = dp(1),keep_ratio = False, allow_stretch = True, source = color + "16.png"))
        self.behx = Button(opacity = .14)
        self.add_widget(self.behx)

class Contac_Screen(Screen):
    def __init__(self, **kwargs):
        super(Contac_Screen, self).__init__(**kwargs)
        self.add_widget(Image(source = color + "16.png", keep_ratio = False, allow_stretch = True))
        root = GridLayout(cols = 1)
        root.add_widget(Label(size_hint_y = None, height = dp(65*2)))
        self.parientescroll = ScrollView()
        self.pariente = GridLayout(cols = 1,size_hint_y = None, height = 1000)

        


        self.parientescroll.add_widget(self.pariente)
        root.add_widget(self.parientescroll)
        self.add_widget(root)
        self.add_widget(Button(background_normal = color + "3.png",background_down = color + "3.png",size_hint_y = None, height = dp(54), text = "[size= 18sp][b]Chats", markup = True, text_size = (Window.width - dp(50), dp(54)), halign = 'center', valign = 'middle', y = Window.height - dp(54) - dp(74)))
        
class Chat_Screen(Screen):
    def __init__(self, **kwargs):
        super(Chat_Screen, self).__init__(**kwargs)
        self.rootp = kwargs["root"]
        self.add_widget(Image(source = color + "3.png", keep_ratio = False , allow_stretch = True))
        
        pariente = GridLayout(cols = 1)
        self.add_widget(pariente)
        subdim = GridLayout(rows = 1,size_hint_y = None , height = dp(54))
        parent0 = RelativeLayout(size_hint_x = None, width = dp(44))
        parent0.add_widget(Image(source = color + "2.png", keep_ratio = False, allow_stretch = True))
        self.back = ImageButton(source = asset + "ic_arrow_back_white_24dp.png")
        parent0.add_widget(self.back)
        subdim.add_widget(parent0)
        self.title = Button(background_normal = color + "2.png",background_down = color + "2.png",font_size = sp(20),text = "Armando Jose Soto Melo",markup = True, text_size = (Window.width - dp(44) - dp(16) - dp(48) , dp(54-28)), halign = 'center', valign = 'bottom',)
        subdim.add_widget(self.title)
        #subdim.add_widget(Button(background_normal = color + "2.png",size_hint_x = None, width = dp(64)))
        parent1 = RelativeLayout(size_hint_x = None, width = dp(48))
        parent1.add_widget(Image(source = color + "2.png", keep_ratio = False, allow_stretch = True))
        spinner = Spinner(
        # default value shown
        text='SEND',
        values=('PIC', 'VID', 'SND'),
        # available values
        # just for positioning in our example
        pos_hint={'center_x': .5, 'center_y': .5})
        spinner.bind(text=self.show_selected_value)
        parent1.add_widget(spinner)
        #parent1.add_widget(ImageButton(source = asset + "ic_more_vert_white_24dp.png",on_release= lambda x: xdrop.open(x) ))
        subdim.add_widget(parent1)
        
        pariente.add_widget(Label(size_hint_y = None, height = dp(74)))
        pariente.add_widget(subdim)
        
        self.pariente_sms = GridLayout(cols = 1, size_hint_y = None, height = dp(1000))
        smsscroll = ScrollView()
        smsscroll.add_widget(self.pariente_sms)
        pariente.add_widget(smsscroll)
        
        mensajes = 3

        subdim1 = RelativeLayout(size_hint_y = None, height = dp(54))
        text_dim = GridLayout(rows= 1,size_hint_x = .75, pos_hint = {'center_x':.5, 'center_y':.5})
        self.input = TextInput(padding = [16,16,0,0],background_normal = color + "T50.png",background_active = color + "T50.png",font_size = sp(18),hint_text = "Escribir Mensaje",foreground_color = (1,1,1,1))
        text_dim.add_widget(self.input)
        subdim1_1 = RelativeLayout(size_hint = (None,1), size = (dp(50),dp(50)), pos_hint = {'x':.75, 'center_y':.5})
        subdim1_1.add_widget(Image(source = color + "T50.png", keep_ratio = False , allow_stretch = True))
        self.behavior = ImageButton(source = asset + "ic_send_white_24dp.png",on_release = lambda x: self.Agregarenvio(text = "Prueba"))
        subdim1_1.add_widget(self.behavior)
        text_dim.add_widget(subdim1_1)
        subdim1.add_widget(text_dim)
        
        pariente.add_widget(subdim1)
        pariente.add_widget(Label(size_hint_y = None, height = dp(16)))
        
    def Agregarenvio(self,**kwargs):
        if self.input.text == "":
            pass
        else:
            msg = MensajeEnviado(text = self.input.text)
            self.pariente_sms.add_widget(msg)
            msg.animate()
            self.input.text = ""
    def Agregaraudio(self,**kwargs):
        from sound import SoundBox
        parentx = GridLayout(rows = 1, size_hint_y = None, height = dp(54))
        parentx.add_widget(Label())
        s = SoundBox()
        parentx.add_widget(s)
        s.show()
        self.pariente_sms.add_widget(parentx)
        
    def Agregarrecibido(self,**kwargs):
        self.pariente_sms.add_widget(MensajeRecibido(text = kwargs["text"]))
       
    def show_selected_value(self, text, text1):
        print( 'have text', text1 , text)
        if text1 == "PIC": 
            self.rootp.parent3.opacity = 0
            self.rootp.fileChooser.bind(on_submit = lambda x,y,z: self.showpathname(x,y,z))
            self.rootp.add_widget(self.rootp.parent3)
            a = Animation(opacity = 1, d = .5, t = 'out_quart')
            a.start(self.rootp.parent3)
            
        elif text1 == "SND":
            self.Agregaraudio()
    def showpathname(self,*args):
        archivo = str(args[1][0])
        if (archivo[-3:].upper() == "BMP") or (archivo[-3:].upper() == "PNG") or (archivo[-3:].upper() == "JPG") or (archivo[-3:].upper() == "JPEG") or (archivo[-3:].upper() == "GIF") or (archivo[-3:].upper() == "TIF"):
            self.Agregarimagen(source = archivo)
        print archivo
    def Agregarimagen(self,**kwargs):
        x = Image(source = kwargs["source"], size_hint_x = None, width = 200)
        x.size_hint = (None,1)
        x.keep_ratio = False
        x.allow_stretch = True
      
        parentx = GridLayout(rows = 1, size_hint_y = None, height = 250)
        parentx.add_widget(Label())
        parentx.add_widget(x)
        self.pariente_sms.add_widget(parentx)
        
        self.rootp.parent3.parent.remove_widget(self.rootp.parent3)
        
        
        
        
        
    def fill_chat(self,**kwargs):
        chat = kwargs["data"]
        # for mensaje in chat:
            # 
            # 
            
class Main_Screen(Screen):
    def __init__(self, **kwargs):
        super(Main_Screen, self).__init__(**kwargs)
        self.sc = ScreenManager()
        self.contacscreen = Contac_Screen(name = "1", root = kwargs["root"])
        self.chatscreen = Chat_Screen(name = "2", root = kwargs["root"])
        self.chatscreen.back.bind(on_release = lambda x: self.dummycurrent(current = "1"))
        self.sc.add_widget(self.contacscreen)
        self.sc.add_widget(self.chatscreen)
        self.add_widget(self.sc)
        for i in range(4):  
            x = Contacto(Nombre = "Nombre "+str(i))
            x.behx.bind(on_release = lambda x: self.dummycurrent(current = "2", title = x.parent.nombre) )
            self.contacscreen.pariente.add_widget(x)
            
            
        self.contacscreen.pariente.add_widget(Label())
        
        
    def dummycurrent(self,**kwargs): 
        self.sc.current = kwargs["current"]
        if kwargs["current"] == "2":
            self.chatscreen.title.text = "[b]"+kwargs["title"]
            
class MyApp(App):
    def build(self):
        return Main_Screen()
 

if __name__ in ('__main__', '__android__'):
    MyApp().run()

    
    
    
    
    