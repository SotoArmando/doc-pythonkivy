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
class Comp2(RelativeLayout):
    def __init__(self, **kwargs):
        super(Comp2, self).__init__(**kwargs)
        self.add_widget(Image(source = color + "16.png", keep_ratio = False , allow_stretch = True))
        parent = GridLayout(rows = 1)
        parent.add_widget(Label())
        for i in range(3):parent.add_widget(Button(size_hint_x = None, width = dp(64)))
        parent.add_widget(Label())
        self.add_widget(parent)
        self.size_hint_y = None
        self.height = dp(52)
        
        

class MyApp(App):
    def build(self):
        return Comp2()
 

if __name__ in ('__main__', '__android__'):
    MyApp().run()

    
    
    
    
    