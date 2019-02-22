from __init__ import *
import os   
import os.path
patch = os.path.dirname(os.path.abspath(__file__))

asset = patch + '/new_assets/'
font = patch + '/fonts/'
color = patch + '/colors/'
C1 = "[color=#13C0C7]"
C4 = "[color=#000000]"
C2 = "[color=#404040]"
C3 = "[color=#ff3333]"
C5 = "[color=#f2f2f2]"
C6 = "[color=#95989A]"
C7 = "[color=#ff0000]"
Window.size = (360,640)
class Label(Label):
    def __init__(self,**kwargs):
        self._trigger_texture = Clock.create_trigger(self.texture_update, -1)
        super(Label, self).__init__(**kwargs)

        # bind all the property for recreating the texture
        d = Label._font_properties
        fbind = self.fbind
        update = self._trigger_texture_update
        fbind('disabled', update, 'disabled')
        for x in d:
            fbind(x, update, x)

        self._label = None
        self._create_label()

        # force the texture creation
        self._trigger_texture()
        
        if self.font_name == "Roboto": self.font_name = font + "Raleway-SemiBold.ttf"

class CustTextInput(RelativeLayout):
    def __init__(self,i_text,sub_text,hint_text, **kwargs):
        super(CustTextInput, self).__init__(**kwargs)
        self.size_hint_y = None
        self.height = dp(60)
        #self.add_widget(Image(source = color + "16.png", keep_ratio = False, allow_stretch = True))
        pariente = GridLayout(x = 18,pos_hint = {'center_y':.5},size_hint_y = None, height = dp(54),cols = 1,spacing = [0,0],padding = [dp(25),0,dp(25),dp(8)])
        left = 49
        self.label0 = Label(opacity = .54,text_size = (Window.width-dp(left),dp(75)),valign = 'bottom',size_hint_y = None,font_size = sp(16) , height = dp(25),markup = True,text = i_text,font_name = font + "Raleway-Bold.ttf")
        pariente.add_widget(self.label0)
        self.input0 = TextInput(opacity = 0.,text = "",on_text_validate = lambda x: self.on_click_onit(),font_size = '16sp',cursor_color = (0,0,0,1),padding = [dp(-2),dp(5),dp(8),0],multiline = False,size_hint_y = None, height = dp(29),background_normal = color + "None.png",background_disabled_normal = color + "None.png",background_active = color + "None.png",markup = True,hint_text = hint_text)
        self.input0.bind(focus = self.on_focus)
        pariente.add_widget(self.input0)
        self.errortxt= Label(font_size = '12sp',opacity = .63,valign = 'top',text_size = (Window.width-dp(left),dp(20)),size_hint_y = None, height = dp(25),markup = True,text = C4+sub_text)
        self.imageparent = RelativeLayout(size_hint = (None,None), width = 264,pos_hint = {'center_x':.5}, height = dp(2))
        self.image_animated1 =Image(opacity = .54,source = color + "2.png",keep_ratio = False, allow_stretch = True)
        self.image_animated2 =Image(opacity = 0.,source = color + "10.png",keep_ratio = False, allow_stretch = True)
        self.image_animated3 =Image(opacity = 0.,source = color + "1.png",keep_ratio = False, allow_stretch = True)
        self.imageparent.add_widget(self.image_animated1)
        self.imageparent.add_widget(self.image_animated2)
        self.imageparent.add_widget(self.image_animated3)
        
        
        pariente.add_widget(self.imageparent)
        pariente.add_widget(self.errortxt)
        
        self.add_widget(pariente)
        self.onit = Button(background_normal = color + "None.png",background_down = color + "None.png",disabled = False, on_release = lambda x: self.on_click_onit())
        self.add_widget(self.onit)
        #self.error("No jodas") 

    def selfTextInput(self): return self.input0
    def sizing(self):
        left = 49
        x = self.label0.text_size
        sizing_animate1 = Animation(opacity = 0., d = .235 , t = 'in_out_cubic')
        sizing_animate3 = Animation(opacity = .63, d = .235 , t = 'in_out_cubic')
        sanimate = Animation(height = dp(60), d = .235, t = 'in_out_cubic')
        sanimate.start(self)
        if self.input0.text == "":
            sizing_animate = Animation(font_size = sp(16),text_size = (x[0],dp(75)), d = .255 , t = 'out_cubic')
            sizing_animate.start(self.label0)
            sizing_animate1.start(self.input0)
            sizing_animate3.start(self.errortxt)

        else:
            pass
        
        sizing_animate1.start(self.image_animated2)
        
    def sizing1(self):
        left = 49
        x = self.label0.text_size
        sizing_animate3 = Animation(opacity = 0, d = .235 , t = 'in_out_cubic')
        sizing_animate = Animation(font_size = sp(15),text_size = (x[0],dp(20)), d = .255 , t = 'out_cubic')
        sizing_animate1 = Animation(opacity = 1., d = .235 , t = 'in_out_cubic')
        sanimate = Animation(height = dp(74), d = .235, t = 'in_out_cubic')
        sanimate.start(self)
        sizing_animate.start(self.label0)
        sizing_animate1.start(self.image_animated2)
        sizing_animate1.start(self.input0)
        sizing_animate3.start(self.errortxt)
        
    def error(self):self.errortxt.opacity = 1.
    def returninput(self): return self.input0
    def on_focus(self,instance, value):
        if value:
            print('User focused', instance)
            self.sizing1()
        else:
            print('User defocused', instance)
            self.sizing()

    def on_click_onit(self):
        try:
            self.add_widget(self.onit)
            anim_x = Animation(opacity = 0., d = .225 , t = 'out_circ')
            anim_x.start(self.image_animated2)
            anim_x.start(self.image_animated3)
            anim_x.start(self.errortxt)
        except:
            self.remove_widget(self.onit)
            
            self.input0.focus = True
            anim_x = Animation(opacity = 1., d = .225 , t = 'in_circ')
            anim_x.start(self.image_animated2)
            
    def error(self,text):
        try:
            self.add_widget(self.onit)
            anim_x = Animation(opacity = 0., d = .225 , t = 'out_circ')
            anim_x.start(self.image_animated3)
        except:
            self.remove_widget(self.onit)
            self.input0.focus = True
            anim_x = Animation(opacity = 1., d = .225 , t = 'in_circ')
            self.errortxt.text = C7+"text"
            anim_x.start(self.image_animated3)
            anim_x.start(self.errortxt)  

        
class kv(RelativeLayout):
    def __init__(self,**kwargs):
        super(kv, self).__init__(**kwargs)
        
        pariente = GridLayout(cols = 1, padding = [0,'32dp',0,0] ) ; background0 = Image(source = color + "16.png", size_hint = (1,1), pos_hint = {'center_x':.5 , 'y': .0}, allow_stretch = True , keep_ratio = False) ;background = Image(source = asset + "Capa 1.png", size_hint = (1,1), pos_hint = {'center_x':.5 , 'y': .0}, allow_stretch = True , keep_ratio = False) ; background.size = background.texture.size ; self.add_widget(background0); self.add_widget(background)
        
        dim = GridLayout(padding = ['34dp',0,0,0] ,rows = 1, size_hint_y = None, height = '81dp'); dim.add_widget(Image(size_hint = (None,1), width = '87dp', keep_ratio = False ,allow_stretch = False, source = asset + "chef2.png")); dim.add_widget(Label());pariente.add_widget(dim)
        
        pariente.add_widget(Label(size_hint_y = None, height = '32dp'))
        
        dim1 = GridLayout(padding = ['34dp',0,0,0] ,rows = 1, height = '50dp', size_hint_y = None); dim1.add_widget(Label(padding_x = '19dp',text_size = (dp(350), dp(50)),halign = 'left', valign = 'bottom',font_size = sp(16), size_hint = (1,1),text = "Busca y crea las recetas a tu\ncomodidad y perfeccion."));pariente.add_widget(dim1)
        
        
        dim5 = GridLayout(padding = ['0dp',0,0,0] ,rows = 2, height = '120dp', size_hint_y = None); dim5.add_widget(Label(size_hint_x = None , width = 35)); pariente.add_widget(CustTextInput("Correo","a","a"));dim5.add_widget(Label(size_hint_x = None , width = 35)); pariente.add_widget(CustTextInput("Contrasena","b","b")); #pariente.add_widget(dim5)
        
        
        pariente.add_widget(Label(size_hint_y = None,font_size = sp(16), height = dp(74),markup = True,text = "[color=#3b53f1]"+"No Tienes una cuenta?[/color]"+" [font="+font+"Raleway-Bold.ttf"+"]Registrate!"))
        
        dim3 = RelativeLayout(size_hint = (1 , None), height = dp(54)); ingfacebook = Button(background_normal = asset + "Rectangulo 2.png",size_hint = (None,1), size = (dp(270), dp(54)), background_down = asset + "Rectangulo 2.png",pos_hint = {'center_x':.5, 'center_y':.5}) ; dim3.add_widget(ingfacebook) ; pariente.add_widget(dim3)
         
        pariente.add_widget(Label(size_hint_y = None, height = '16dp'))
        
        dim4 = RelativeLayout(size_hint = (1 , None), height = dp(54))
        ingfacebook = Button(background_normal = asset + "Rectangulob 2@0,5x.png",size_hint = (None,1), size = (dp(270), dp(54)), background_down = asset + "Rectangulob 2@0,5x.png",pos_hint = {'center_x':.5, 'center_y':.5})
        dim4.add_widget(ingfacebook)
        pariente.add_widget(dim4)
        
        
        dim3.add_widget(Image(source = asset + "facebook-logo@0,5x.png",pos_hint = {'center_x':.2, 'center_y':.5}));dim3.add_widget(Label(source = asset + "facebook-logo@0,5x.png",text ="Ingresar con facebook" ,font_size = sp(16),pos_hint = {'center_x':.5, 'center_y':.5}));
        dim4.add_widget(Image(source = asset + "search@0,5x.png",pos_hint = {'center_x':.2, 'center_y':.5}));dim4.add_widget(Label(source = asset + "facebook-logo@0,5x.png",markup = True, text ="[color=#000000]Ingresar con Google" ,font_size = sp(16),pos_hint = {'center_x':.5, 'center_y':.5}));


        ingGoogle = Button()
        
        self.add_widget(pariente)
        
                
class MyApp(App):
    def build(self):
        return kv()

 

if __name__ in ('__main__', '__android__'):
    MyApp().run()