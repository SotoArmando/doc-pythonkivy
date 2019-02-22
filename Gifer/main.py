from activities import *

patch = os.path.dirname(os.path.abspath(__file__))
asset = patch + '/activities/_assets/drawable-mdpi/'
color = patch + '/activities/_colors/'
font = patch + '/activities/_fonts/'

print (".: ASSETS DIR",asset)
print (".: COLORS DIR",color)
print (".: FONTS DIR" ,font)

class Program(RelativeLayout):
    def __init__(self, **kwargs):
        super(Program, self).__init__(**kwargs)
        self.LoadWelcomeActivitie()
        self.add_widget(Button(opacity = 0, on_release = lambda x:self.Switch(), on_press = lambda x: self.LoadWorkboard()))
        
    def LoadWelcomeActivitie(self):
        self.add_widget(WelcomeActivitie(root = self, y = -50, opacity = .50))
        a = Animation(opacity = 1,y = 0, d = 1, t = 'out_back')
        a.start(self.children[0])
        
    def LoadWorkboard(self):
        x = Workboard(root = self, y = -50, opacity = .50)
        self.add_widget(x)
        a = Animation(opacity = 1,y = 0, d = 1, t = 'out_back')
        a.start(self.children[0])
        
        
    def Switch(self):
        a = Animation(opacity = 0, d = .5, t = 'out_quart')
        a.bind(on_complete = lambda x,y:self.remove_widget(self.children[1]))
        a.start(self.children[-1])
        
class Gipher(App):
    def build(self):
        return Program() 

if __name__ == '__main__':
    Gipher().run()
