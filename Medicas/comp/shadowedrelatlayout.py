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
class MyButton(Button):
    pass
class Details(RelativeLayout):
    def __init__(self, **kwargs):
        super(Details, self).__init__(**kwargs)
        self.size_hint_y = None ; self.height = dp(114)
        parent = GridLayout(cols = 2, spacing = dp(-8))
        texting1 = Button(font_name = font + "Roboto-Medium.ttf" ,padding_y = dp(8),halign = 'left', valign = 'top',text = kwargs["text1"], markup = True, background_normal = asset + "Rectangle 1366.png",background_down = asset + "Rectangle 1366.png",)
        texting2 = Button(font_name = font + "Roboto-Medium.ttf" ,padding_y = dp(8),halign = 'left', valign = 'top',text = kwargs["text2"], markup = True, background_normal = asset + "Rectangle 1366.png",background_down = asset + "Rectangle 1366.png",)
        
        texting1.text_size = (dp(154-16),dp(96))
        texting2.text_size = (dp(154-16),dp(96))
        
        texting1.texture_update() 
        texting2.texture_update() 
        parent.add_widget(texting1)
        parent.add_widget(texting2)
        self.add_widget(parent)
        
class SHRelativeLayout(RelativeLayout):
    def __init__(self, **kwargs):
        super(SHRelativeLayout, self).__init__(**kwargs)
        self.add_widget(Image(source = asset + "U.png", size_hint_y = None, height = dp(3),keep_ratio = False, allow_stretch = True , pos_hint = {"y":1} ) )
        self.add_widget(Image(source = asset + "D.png", size_hint_y = None, height = dp(9),keep_ratio = False, allow_stretch = True , y = dp(-9) ) )
        self.add_widget(Image(source = asset + "L.png", size_hint_x = None, width = dp(6),keep_ratio = False, allow_stretch = True , x = dp(-6) ) )
        self.add_widget(Image(source = asset + "R.png", size_hint_x = None, width = dp(6),keep_ratio = False, allow_stretch = True, pos_hint = {"x":1} ) )
        
        self.add_widget(Image(source = asset + "LU.png", size_hint = (None,None), size = (dp(6),dp(3)), width = dp(6),keep_ratio = False, allow_stretch = True, x = dp(-3), pos_hint = {"y":1} ) )
        
        self.add_widget(Image(source = asset + "RU.png", size_hint = (None,None), size = (dp(6),dp(3)), width = dp(6),keep_ratio = False, allow_stretch = True, y = dp(-3), pos_hint = {"x":1} ) )
        
        self.add_widget(Image(source = asset + "LD.png", size_hint = (None,None), size = (dp(6),dp(9)), width = dp(6),keep_ratio = False, allow_stretch = True, x = dp(-6), y = dp(-9) ) )
        
        self.add_widget(Image(source = asset + "RD.png", size_hint = (None,None), size = (dp(7),dp(9)), width = dp(6),keep_ratio = False, allow_stretch = True, pos_hint = {"x":1}, y = dp(-9) ) )

        
        
        



    def funcion(self):
        print("hola")
        
class MyApp(App):
    def build(self):
        return SHRelativeLayout()
 

if __name__ in ('__main__', '__android__'):
    MyApp().run()

    
    
    
    
    