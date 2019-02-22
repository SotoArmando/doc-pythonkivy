
import sys
from os.path import dirname, join, abspath
sys.path.insert(0, dirname(dirname(abspath(__file__))))
from __dep__ import *




#CARPETAS DEL PROYECTO
patch = dirname(abspath(__file__))
asset = patch + '/assets/drawable-mdpi/'
color = patch + '/colors/'
font = patch + '/fonts/'

class WelcomeActivitie(RelativeLayout):
    def __init__(self,**kwargs):
        super(WelcomeActivitie, self).__init__(**kwargs)
        Relat0 = RelativeLayout()
        with Relat0.canvas:
            Color(1,1,1,1)
            Rectangle(size = (64,64), pos = (0,0))
        Scatter0 = Scatter(on_rotation = lambda x: self.calc()); Scatter0.add_widget(Relat0)
        Float0 = RelativeLayout(size_hint = (None,None), size = (64,64), pos_hint = {'center_x':.5, 'center_y':.5}); Float0.add_widget(Scatter0)
        self.add_widget(Float0)
        Label0 = Label(text = "[b]100%", markup = True, font_size = '21sp', size_hint = (None,None), size = (dp(124),dp(124)), pos_hint = {'center_x':.5, 'center_y':.4})
        self.add_widget(Label0)
        
        self.anim = Animation(rotation = 361, d = 1 , t = 'in_expo') + Animation(rotation = 361, d = 1 , t = 'out_expo')
        self.anim.repeat = True
        self.anim.start(Scatter0)
    def calc(self,*args):
        print(args)

class YourAppNameApp(App):
    def build(self):
        return WelcomeActivitie()

if __name__ == '__main__':
    YourAppNameApp().run()
