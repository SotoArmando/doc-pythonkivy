import sys, os
from docs.mind import *

patch = os.path.dirname(os.path.abspath(__file__))
asset = patch + '/docs/_assets/drawable-mdpi/'
sound = patch + '/docs/_sounds/'
behavior = patch + '/docs/_behavior/'
font = patch + '/docs/_fonts/'

print (".: ASSETS DIR",asset)
print (".: FONTS DIR" ,font)
print (".: SOUND DIR" ,sound)
print (".: BEHAVIOR DIR" ,behavior)

Window.size = (360,640)
Window.clearcolor = (1,1,1,1)
class FirstScreen(RelativeLayout): 
    def horizontal(*args):
        texture = Texture.create(size=(len(args), 1), colorfmt='rgba')
        buf = bytes([ int(v * 255)  for v in chain(*args) ])  # flattens

        texture.blit_buffer(buf, colorfmt='rgba', bufferfmt='ubyte')
        return texture

    def vertical(*args):
        texture = Texture.create(size=(1, len(args)), colorfmt='rgba')
        buf = bytes([ int(v * 255)  for v in chain(*args) ])  # flattens

        texture.blit_buffer(buf, colorfmt='rgba', bufferfmt='ubyte')
        return texture


class BottomOption(ButtonBehavior, RelativeLayout): 
    def switch(self):
        if self.mycolor == "[color=ffffff]":
            self.mycolor = "[color=000000]"
        else:   
            self.mycolor = "[color=ffffff]"
        
        self.ids.leftlabel.text = self.mycolor + self.ids.leftlabel.text[len("[color=ffffff]"):]
        self.ids.rightlabel.text = self.mycolor + self.ids.rightlabel.text[len("[color=ffffff]"):]

class Main(RelativeLayout):
    def __init__(this,**kwargs):
        super(Main, this).__init__(**kwargs)
       
        
        this.add_widget(FirstScreen())
        
            

        
   
        
class CodiCookingTimerApp(App):
    def build(this):
        return Main()

CodiCookingTimerApp().run()