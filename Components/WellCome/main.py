#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __init__ import *

import random

Window.size = (360,640)
Window.clearcolor = (0,0,0,1)

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

class ImageButton(ButtonBehavior, Image): pass

class Optionselect(RelativeLayout):
    exact_height = NumericProperty()
    exact_width = NumericProperty()
    r = NumericProperty(0.6980392156862745)
    g = NumericProperty(1.0)
    b = NumericProperty(1.0)
    a = NumericProperty(1.0)
    current_slide = NumericProperty(0)
    centros = [0, Window.width*-2, Window.width*-1]
    def __init__(self, **kwargs):
        super(Optionselect, self).__init__(**kwargs)
        
        self.piz = Scatter()
        self.add_widget(self.piz)
        with self.piz.canvas:
            c = Color(self.r, self.g, self.b, self.a)
            rect = Rectangle(size = self.determine_size(**kwargs) , pos = self.pos)
            
        x = Animation(r = random.uniform(0.0,1.0), g = random.uniform(0.0,1.0), b = random.uniform(0.0,1.0),a = 1.0, d = 3, t = "out_quart") + Animation(r = random.uniform(0.0,1.0), g = random.uniform(0.0,1.0), b = random.uniform(0.0,1.0),a = 1.0, d = 3, t = "out_quart") + Animation(r = random.uniform(0.0,1.0), g = random.uniform(0.0,1.0), b = random.uniform(0.0,1.0),a = 1.0, d = 3, t = "out_quart") + Animation(r = random.uniform(0.0,1.0), g = random.uniform(0.0,1.0), b = random.uniform(0.0,1.0),a = 1.0, d = 3, t = "out_quart") + Animation(r = random.uniform(0.0,1.0), g = random.uniform(0.0,1.0), b = random.uniform(0.0,1.0),a = 1.0, d = 3, t = "out_quart") 
        
        
        self.parent1 = GridLayout(size_hint_x = 3, cols = 3,opacity = .91, x = self.centros[self.current_slide])
        a = RelativeLayout()
        a.add_widget(Image(source = "projection.png", size_hint = (None,None) , size = (dp(124),dp(124)), pos_hint=  {'center_x':.5, 'center_y':.75} ))
        a.add_widget(Label(text = "[b]Detras de ti!! \nUn Puto avestrus!.", markup = True,text_size = (dp(124*2),dp(64)), halign = 'center', valign = 'middle', pos_hint=  {'center_x':.5, 'center_y':.5} ))
        b = RelativeLayout()
        b.add_widget(Image(source = "thought.png", size_hint = (None,None) , size = (dp(124),dp(124)), pos_hint=  {'center_x':.5, 'center_y':.75} ))
        b.add_widget(Label(text = "[b]Detras de ti!! \nUn Puto avestrus!.", markup = True,text_size = (dp(124*2),dp(64)), halign = 'center', valign = 'middle', pos_hint=  {'center_x':.5, 'center_y':.5} ))
        c = RelativeLayout()
        c.add_widget(Image(source = "graph.png", size_hint = (None,None) , size = (dp(124),dp(124)), pos_hint=  {'center_x':.5, 'center_y':.75} ))
        c.add_widget(Label(text = "[b]Detras de ti!! \nUn Puto avestrus!.", markup = True,text_size = (dp(124*2),dp(64)), halign = 'center', valign = 'middle', pos_hint=  {'center_x':.5, 'center_y':.5} ))
        self.parent1.add_widget(a)

        self.parent1.add_widget(b)
        self.parent1.add_widget(c)
        self.add_widget(self.parent1)

        x.repeat = True
        x.start(self)
        self.next_slide()
        print rect.size
        Clock.schedule_interval(self.next_slide , 3)
    def next_slide(self, *args):
        print self.current_slide
        self.current_slide -= 1
        self.current_slide %= 3
        a = Animation(x = self.centros[self.current_slide] , d = 3, t = 'out_quart')
        a.start(self.parent1)
        
    def on_r(self,*args,**kwargs):
        self.piz.canvas.clear()
        with self.piz.canvas:
            c = Color(self.r, self.g, self.b, self.a)
            rect = Rectangle(size = self.determine_size(**kwargs) , pos = self.pos)    
            
    def determine_size(self,**kwargs):
        if self.size_hint == [1,1]:
            self.exact_width = Window.width
            self.exact_height = Window.height
            return (self.exact_width,self.exact_height)
        else:
            print "size_hint != (1,1) FALSE"
            if "size_hint" in kwargs: self.exact_width = self.size_hint[0] * Window.width
            elif "size_hint_x" in kwargs: self.exact_width = self.size_hint_x * Window.width
            else: 
                if "size" in kwargs: self.exact_height = self.size[0]
                elif "width" in kwargs: self.exact_height = self.width
            
            if "size_hint" in kwargs: self.exact_height = self.size_hint[1] * Window.height
            elif "size_hint_y" in kwargs: self.exact_height = self.size_hint_y * Window.height
            else: 
                if "size" in kwargs: self.exact_height = self.size[1]
                elif "height" in kwargs: self.exact_height = self.height
                
            return (self.exact_width,self.exact_height)
            
class MyApp(App):
    def build(self):
        return Optionselect()
 

if __name__ in ('__main__', '__android__'):
    MyApp().run()

    
    
    
    
    