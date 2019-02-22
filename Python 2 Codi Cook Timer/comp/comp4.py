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
class Comp4(RelativeLayout):
    def __init__(self, **kwargs):
        super(Comp4, self).__init__(**kwargs)
        
        self.add_widget(Button(size_hint = (None,None), size = (dp(64),dp(64)), pos_hint = {'center_x':.5, 'y':0}))
        
        
        
        parent = ScrollView(); self.add_widget(parent)
        parentrelat = RelativeLayout(size_hint_y = None, height = dp(800)); parent.add_widget(parentrelat)
        parentgrid = GridLayout(size_hint_x = .9, pos_hint ={'center_x':.5},cols = 1,size_hint_y = 1); parentrelat.add_widget(parentgrid)
        parentgrid.add_widget(Label(size_hint_y = None, height = dp(300)))
        SHR = SHRelativeLayout(size_hint_y = 1, height = dp(700)); parentgrid.add_widget(SHR)
        #SHR.add_widget(Button())

        parentgrid.add_widget(Label(size_hint_y = None, height = dp(8)))   

        
        

class MyApp(App):
    def build(self):
        return Comp4()
 

if __name__ in ('__main__', '__android__'):
    MyApp().run()

    
    
    
    
    