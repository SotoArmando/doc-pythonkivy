#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __init__ import *

import random

from kivy.graphics import Color, Ellipse, Rectangle, RoundedRectangle
Window.size = (360,640)
Window.clearcolor = (1,1,1,1)

__Asset__ = join(dirname(dirname(abspath(__file__))), '_Assets\\')
__Color__ = join(dirname(dirname(abspath(__file__))), '_Colors\\')
__Font__ = join(dirname(dirname(abspath(__file__))), '_Fonts\\')

print "Assets DIR",__Asset__
print "Colors DIR",__Color__
print "Fonts DIR" ,__Font__

C1 = "[color=#13C0C7]"
C4 = "[color=#000000]"
C2 = "[color=#404040]"
C3 = "[color=#ff3333]"
C5 = "[color=#f2f2f2]"
C6 = "[color=#95989A]"
EC = "[/color]"
Builder.load_string('''
#:import os os
<BButton@Button>:
    id: z
    background_normal:''
    background_down:''
    background_disabled_normal: ''
    markup: True


    
<Optionselect@RelativeLayout>:
    id: Optionslelect
    Scatter:
        canvas:
            Color: 
                rgb: (1,1,1,.24)
            Rectangle:
                size: self.size

    Button:
        id: vivo
        markup: True
        background_normal:''
        background_color:(1,1,1,.05)
        text: '[color=#000000]Open Selector'
        on_release: Optionslelect.open_selector(vivo)

        
''')
class ImageButton(ButtonBehavior, Image): pass
class BButton(Button):
    inital = 0
    mycoloropacity = NumericProperty(inital)
    
    def __init__(self, **kwargs):
        super(BButton, self).__init__(**kwargs)





        

        
class Optionselect(RelativeLayout):
    
    def __init__(self, **kwargs):
        super(Optionselect, self).__init__(**kwargs)
        self.added = False
        self.selected = None
        self.opened = False
        self.scroll = ScrollView(size_hint_x = .8, pos_hint = {'center_x':.5},opacity = .50, y = dp(-50), scroll_y = .5, bar_color = [0,0,0,0])
        self.grid = GridLayout(cols = 1, size_hint_y = None, pos_hint = {'center_y':.5}, spacing = 1)
        self.gridr = RelativeLayout(size_hint_y = None)
        self.gridr.add_widget(self.grid)
        self.scroll.add_widget(self.gridr)
        if "range" in kwargs:
            for i in range(kwargs["range"]):
                RelativeLayou0 = RelativeLayout()
                Scater = RelativeLayout(size_hint_y = None, height = dp(54))
                thebutton = BButton(size_hint = (None,None),size =   (Window.width*.8, dp(54)),text = "[color=#ffffff][b]Opcion Numero."+ str(i),background_color = (1,1,1,0),background_normal = '', on_release = lambda x: self.close_selector(x.text))
                with Scater.canvas:
                    Color(0,0,0,.74)
                    
                    if i == 0: RoundedRectangle(pos= (0,0),size =   (Window.width*.8, dp(54)), radius= [12,12,0,0]) ; pass
                    elif i == kwargs["range"]-1: RoundedRectangle(pos= (0,0),size =   (Window.width*.8, dp(54)), radius= [0,0,12,12]) ; pass
                    else : RoundedRectangle(pos= (0,0),size = (Window.width*.8, dp(54)), radius= [0,0,0,0]); pass
            
                Scater.add_widget(thebutton)
          
                self.grid.add_widget(Scater)
                self.grid.height += 54
                self.gridr.height += 54
        
        if self.grid.height < Window.height: self.gridr.height = Window.height
    def on_opened(self,*args): print self.opened
    def open_selector(self,b):
        self.selected = b
        if self.added == False: self.get_root_window().add_widget(self.scroll); self.added = True
        self.scroll.pos_hint = {'center_x':.5}
        x =  Animation(opacity = 1, y = 0, x = 0, d = 1 , t = 'out_expo') 
        x.start(self.scroll)
        

    def get_away(self):
        self.scroll.pos_hint = {'center_x': 1.5}
        
    def close_selector(self,*args):
        print self.scroll
        print args
        self.selected.text = "[color=#000000]"+ (args[0].replace('[b]','')) 
        self.selected.text = self.selected.text.replace('ffffff','000000')
        x = Animation(opacity = 0, y = dp(-50), d = .5 , t = 'out_expo') 
        x.bind(on_complete = lambda x,y:self.get_away())
        x.start(self.scroll)
   
    

            
class MyApp(App):
    def build(self):
        scroll = ScrollView()
        grid = GridLayout(cols = 1, size_hint_y = None, height = dp(1000))
        scroll.add_widget(grid)
        grid.add_widget(Label(text = "[color=#0000000][b]Formulario",size_hint_y = None, height = dp(54),font_size = sp(21), markup = True))
        grid.add_widget(Label(text = "[color=#0000000][b]1.Pregunta?",size_hint_y = None,text_size = (Window.width - dp(18),dp(24)), valign = 'middle', height = dp(24),font_size = sp(17), markup = True))
        grid.add_widget(Optionselect(size_hint_y = None, height = dp(54), range = 20))
        grid.add_widget(Label(text = "[color=#0000000][b]2.Pregunta?",size_hint_y = None,text_size = (Window.width - dp(18),dp(24)), valign = 'middle', height = dp(24),font_size = sp(17), markup = True))
        grid.add_widget(Optionselect(size_hint_y = None, height = dp(54), range = 5))
        grid.add_widget(Label(text = "[color=#0000000][b]3.Pregunta?",size_hint_y = None,text_size = (Window.width - dp(18),dp(24)), valign = 'middle', height = dp(24),font_size = sp(17), markup = True))
        grid.add_widget(Optionselect(size_hint_y = None, height = dp(54), range = 15))
        grid.add_widget(Label(text = "[color=#0000000][b]4.Pregunta?",size_hint_y = None,text_size = (Window.width - dp(18),dp(24)), valign = 'middle', height = dp(24),font_size = sp(17), markup = True))
        grid.add_widget(Optionselect(size_hint_y = None, height = dp(54), range = 2))
        grid.add_widget(Label(text = "[color=#0000000][b]5.Pregunta?",size_hint_y = None,text_size = (Window.width - dp(18),dp(24)), valign = 'middle', height = dp(24),font_size = sp(17), markup = True))
        grid.add_widget(Optionselect(size_hint_y = None, height = dp(54), range = 7))
        grid.add_widget(Button(size_hint_y = None, height = dp(54), range = 7))

        return scroll
 

if __name__ in ('__main__', '__android__'):
    MyApp().run()

    
    
    
    
    