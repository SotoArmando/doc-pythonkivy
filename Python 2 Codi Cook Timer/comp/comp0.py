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
from SHR import SHRelativeLayout
class MyButton(Button):
    pass
class Label(Label):
    markup = True
class ImageButton(ButtonBehavior, AsyncImage): pass
class Comp0(RelativeLayout):
    def __init__(self, **kwargs):
        super(Comp0, self).__init__(**kwargs)
 
        
        choose = ScrollView(bar_margin = 0,size_hint_y = 1,height = '120dp' ,do_scroll_y = False, do_scroll_x = True ,scroll_x = 0.5,bar_color = [0,0,0,0],bar_inactive_color = [.7,.7,.7,0],bar_width = 3, bar_pos_x = "top")
        chooseroot_root = RelativeLayout(opacity = .74,size_hint_y = 1, size_hint_x = None, width = dp(1100))
        chooseroot = GridLayout(rows = 1, size_hint_y = 1, size_hint_x = 1, spacing = dp(5))
        chooseroot_root.add_widget(chooseroot)
        choose.add_widget(chooseroot_root)
        
        self.medio = Image(source = asset + "clock.png", size_hint = (None,None), size = ('24dp','24dp'), pos = (0,dp(100)-dp(24)))
        chooseroot_root.add_widget(self.medio)
    
        imgset = ["bacon","bread","coffeex","fried-egg","meat","toaster","tea","teapot","pizza","shrimp"]
        
        for i in range(10):  
            if i == 0:
                chooseroot.add_widget(Image(source = color+"None.png",allow_stretch = True, keep_ratio = False,size_hint_x = None, width = '64dp')) 

            self.container = GridLayout(cols = 1, size_hint = (1,1))
            dpix = (dp(120)/2) - (dp(64)/2) 
            image = ImageButton(source = asset +imgset[i]+".png",size_hint = (None,None),width = '64dp', height = '64dp', allow_stretch = True,  keep_ratio = True,  pos = (0,dpix) )
            self.imagescatter = Scatter(scale = 1,do_translation_y=False,do_translation_x=False,source = asset +imgset[i],size_hint = (1,1) , allow_stretch = True,  keep_ratio = True)
            
            image.bind(on_press =lambda x: self.Animatesize(x.parent))
            self.imagescatter.add_widget(image)
            self.container.add_widget(self.imagescatter)
            chooseroot.add_widget(self.container)
            
            
            if i == 9:
                chooseroot.add_widget(Image(source = color+"None.png",allow_stretch = True, keep_ratio = False,size_hint_x = None, width = '64dp'))
                
        self.add_widget(choose)

    def Animatesize(self,button):
        try:
            if button.children[0].source == asset + "lock0.png":
                button.children[0].source = asset + "lock1.png"
            elif button.children[0].source == asset + "lock1.png" :
                button.children[0].source = asset + "lock0.png"
        except:
            pass
        print button.parent.pos

        
        anim3 = Animation(x = button.parent.pos[0], d = .75, t = "in_out_back")
        anim3.start(self.medio)
        button.scale = 1.0
        anim1 = Animation(scale = .75, d = .05,t = "in_circ")
        anim2 = Animation(scale = 1.0, d = .15,t = "out_circ")
        anim = anim1 + anim2
        anim.start(button)
        
        
        



    def funcion(self):
        print("hola")
        
class MyApp(App):
    def build(self):
        return Comp0()
 

if __name__ in ('__main__', '__android__'):
    MyApp().run()

    
    
    
    
    