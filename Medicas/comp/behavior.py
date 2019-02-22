#!/usr/bin/env python
# -*- coding: utf-8 -*-


















from __init__ import *


patch = os.path.dirname(os.path.abspath(__file__))
asset = patch + '/assets/drawable-mdpi/'
color = patch + '/colors/'
font = patch + '/fonts/'
#Window.size = (360,640)
Window.clearcolor = (1,1,1,1)

        
class CloseBehavior(RelativeLayout):
    def __init__(self, **kwargs):
        super(CloseBehavior, self).__init__(**kwargs)
        try:
            self.object = kwargs["object"]
            self.toggled = False
            self.R = kwargs["R"]
            self.size_hint = (None,None)
            self.size = (dp(0),dp(0))
            self.pos_hint = {"center_x":.9,"center_y":.1}
            self.add_widget(Image(source = asset + "Ellipse 1.png", size_hint = (1,1),pos_hint = {"center_x":.5,"center_y":.5}))
            self.Especial = Image(source = asset + "Group 2.png",allow_stretch = True, keep_ratio = False, size_hint = (None,None), size = (dp(0),dp(0)),pos_hint = {"center_x":.5,"center_y":.53})
            self.add_widget(self.Especial)
            self.b = Button(opacity = 0 , on_release = lambda x: self.toggle())
            self.b.bind(on_release = lambda x: self.CloseObject() )
            self.add_widget(self.b)
            self.toggle()
            #Clock.schedule_interval(lambda x: self.toggle(), 1)
            
        except:
            self.toggled = False
            self.R = kwargs["R"]
            self.size_hint = (None,None)
            self.size = (dp(0),dp(0))
            self.pos_hint = {"center_x":.9,"center_y":.1}
            self.add_widget(Image(source = asset + "Ellipse 1.png", size_hint = (1,1),pos_hint = {"center_x":.5,"center_y":.5}))
            self.Especial = Image(source = asset + "Group 2.png",allow_stretch = True, keep_ratio = False, size_hint = (None,None), size = (dp(0),dp(0)),pos_hint = {"center_x":.5,"center_y":.53})
            self.add_widget(self.Especial)
            self.b = Button(opacity = 0 , on_release = lambda x: self.toggle())
            self.b.bind(on_release = lambda x: self.Close() )
            self.add_widget(self.b)
            self.toggle()
            #Clock.schedule_interval(lambda x: self.toggle(), 1)
            
    def Close(self):
        x = Animation(opacity = 0, d = .25 , t = 'out_quart')
        x.bind(on_complete = lambda x,y: self.R.remove_widget(self.R.children[1]) )
        x.start(self.R.children[1])
    def CloseObject(self):
        x = Animation(opacity = 0, d = .25 , t = 'out_quart')
        x.bind(on_complete = lambda x,y: self.object.parent.remove_widget(self.object) )
        x.start(self.object)
        
        
    def toggle(self):
        if self.toggled == False:
            x = Animation(size = (dp(72),dp(72)), d = .25 , t = 'out_expo')
            y = Animation(size = (dp(24),dp(24)), d = .25 , t = 'out_expo')
            x.start(self)
            y.start(self.Especial)
            self.toggled = True
        elif self.toggled == True:
            x = Animation(size = (dp(0),dp(0)), d = .25 , t = 'out_quart')
            y = Animation(size = (dp(0),dp(0)), d = .25 , t = 'out_quart')
            x.start(self)
            y.start(self.Especial)
            self.toggled = False
        

    def funcion(self):
        print("hola")
        
class MyApp(App):
    def build(self):
        return CloseBehavior()
 

if __name__ in ('__main__', '__android__'):
    MyApp().run()

    
    
    
    
    