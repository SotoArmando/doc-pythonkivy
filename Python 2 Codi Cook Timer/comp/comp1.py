#!/usr/bin/env python
# -*- coding: utf-8 -*-


















from __init__ import *


patch = os.path.dirname(os.path.abspath(__file__))
asset = patch + '/assets/drawable-mdpi/'
color = patch + '/colors/'
font = patch + '/fonts/'
Window.size = (360,640)

kv = '''
<MyButton>:
    size_hint: 1, None
    size: self.texture_size
'''
Builder.load_string(kv)
C4 = "[color=#000000]"
from SHR import SHRelativeLayout
class MyButton(Button):
    pass
class Label(Label):
    markup = True
class ImageButton(ButtonBehavior, AsyncImage): pass
class Comp1(RelativeLayout):
    def __init__(self, **kwargs):
        super(Comp1, self).__init__(**kwargs)
        self.add_widget(Image(source = color + "16.png", keep_ratio = False , allow_stretch = True))
        parent = GridLayout(cols = 1)
        rowlay = GridLayout(rows = 1); parent.add_widget(rowlay)
        self.size_hint_y = None
        self.height = dp(100)
        text = "00:00:00"
        rowlay.add_widget(Label())
        for s in text: rowlay.add_widget(Label(text = C4+s, font_size = '57sp', size_hint_x = None, width = dp(37)))
        rowlay.add_widget(Label())
        parent.add_widget(Label(text = C4 + "0 horas 0 minutos y 0 segundos", font_size = '19sp'))
        self.add_widget(parent)
        
        

class MyApp(App):
    def build(self):
        return Comp1()
 

if __name__ in ('__main__', '__android__'):
    MyApp().run()

    
    
    
    
    