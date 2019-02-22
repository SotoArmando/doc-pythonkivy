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
        
        
        self.size_hint_y = None ; self.height = dp(114)
        parent = GridLayout(cols = 2, spacing = dp(8))
        paren1 = SHRelativeLayout()
        paren2 = SHRelativeLayout()
        texting1 = Button(font_name = font + "Roboto-Medium.ttf" ,padding_y = dp(8),halign = 'left', valign = 'top',text = kwargs["text1"], markup = True, background_normal = color + "16.png",background_down = color + "16.png",)
        texting2 = Button(font_name = font + "Roboto-Medium.ttf" ,padding_y = dp(8),halign = 'left', valign = 'top',text = kwargs["text2"], markup = True, background_normal = color + "16.png",background_down = color + "16.png",)
        
        texting1.text_size = (dp(154-16),dp(96))
        texting2.text_size = (dp(154-16),dp(96))
        
        texting1.texture_update() 
        texting2.texture_update() 
        paren1.add_widget(texting1)
        paren2.add_widget(texting2)
        parent.add_widget(paren1)
        parent.add_widget(paren2)
        self.add_widget(parent)
        
class Comp3(RelativeLayout):
    def __init__(self, **kwargs):
        super(Comp3, self).__init__(**kwargs)
        parent = Gridlayout(cols = 2)
        
        
        



    def funcion(self):
        print("hola")
        
class MyApp(App):
    def build(self):
        return Comp3()
 

if __name__ in ('__main__', '__android__'):
    MyApp().run()

    
    
    
    
    