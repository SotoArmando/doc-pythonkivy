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
        self.sel = None
        img = Image(size_hint = (.75,.90), pos_hint = {'center_x':.5, 'center_y':.65}, source = kwargs["source"], keep_ratio = True, allow_stretch = True)
        label = Label(font_size = sp(12),markup = True,text = "[color=#000000]"+kwargs["text"],size_hint = (1,None), height = dp(50), pos_hint = {"center_y":.25})
        self.img = img
        self.label = label
        self.add_widget(img)
        self.add_widget(label)
    
    
        behavior = Button(opacity = 0, on_release = lambda x: self.animate())
        self.b = behavior
        self.add_widget(behavior)
        
    def animate(self):
        print "hola"
        x = Animation(size_hint = (1,1), d = .1 , t = 'in_quad') + Animation(size_hint = (.75,.90), d = .1 , t = 'out_quad')
        x.start(self.img)
        
class Comp2(RelativeLayout):
    def __init__(self, **kwargs):
        super(Comp2, self).__init__(**kwargs)
        self.size_hint_y = 1
      
        parentroot = RelativeLayout(height = dp(80), size_hint_y = None,)
        parentroot.add_widget(Image(height = dp(80), size_hint_y = None,opacity = .18,source = color + "3.png", keep_ratio = False ,allow_stretch = True))
        parent = GridLayout(rows = 1, padding = [dp(8),dp(8),dp(8),dp(8)], spacing = 8)
        parent.add_widget(Image(size_hint = (None,1), width = dp(64),source = asset + "Path 234.png", keep_ratio = False, allow_stretch = True))
        
        textinglay = GridLayout(rows = 1,spacing = 1)
        textinglay.add_widget(Button(markup = True,text = "[size=16sp]Farmacia Carol[/size]\n[size=12sp]Lo Mejor para tu Salud y tu bienestar",text_size = (dp(122),dp(64)) ,background_normal = color + "17.png",background_down = color + "17.png",valign = "middle" ))
        textinglay.add_widget(Button(halign = 'center', valign = 'middle',font_size = sp(12),text = "Salud Digital\n809-274-7688",text_size = (dp(100), dp(50)),background_normal = color + "17.png",background_down = color + "17.png"))
        parent.add_widget(textinglay)
        grid = GridLayout(cols = 1)
        parentroot.add_widget(parent)
        grid.add_widget(parentroot)
        grid.add_widget(Label())
        self.add_widget(grid)
        



    def funcion(self):
        print("hola")
        
class MyApp(App):
    def build(self):
        return Comp2()
 

if __name__ in ('__main__', '__android__'):
    MyApp().run()

    
    
    
    
    