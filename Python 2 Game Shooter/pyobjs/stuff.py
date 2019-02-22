from __init__ import *


class Objeto(RelativeLayout):
    def __init__(self,**kwargs):
        super(Objeto, self).__init__(**kwargs)
        self.img = Image(size_hint = (None,None),source = kwargs["source"],size = kwargs["size"], keep_ratio = False, allow_stretch = True)
        self.add_widget(self.img)
        
        Clock.schedule_interval(lambda x: self.move(), 1.0/60.0)
        
    def move(self): self.y += 3
    def repos(self):
        self.x = randint(0, 500)
        self.y = 0

class Fondo(RelativeLayout):
    def __init__(self, **kwargs):
        super(Fondo, self).__init__(**kwargs)
        self.asteroids = []
        #Clock.schedule_interval(lambda x: self.new_stuff(), 1)
        t = threading.Thread(target=Clock.schedule_interval(self.new_stuff, 1.0))
        
 
        
        
        
        
        


    def new_stuff(self,*args):
        if len(self.asteroids) <= 10:
            imgs = ["asteroid.png","asteroid1.png","asteroid2.png"]
            img = Objeto(x = randint(0, 500), size = (75,75), source = (random.choice(imgs)))
            self.add_widget(img)
            self.asteroids.append(img)
        else:
            self.asteroids[0].repos()
            self.asteroids.append(self.asteroids.pop(self.asteroids.index(self.asteroids[0])))
class Level(Widget):
    def __init__(self, **kwargs):
        super(Level, self).__init__(**kwargs)
        self.enemies = kwargs["foes"]
        self.winsize = None
        dificultad = kwargs["dificultad"]
        

        

        
    def begin(self):
        from players import Enemy
        pos = 1.0 / (self.enemies+1)
        print pos, "POS"
        for i in range(self.enemies):
            print (pos*(i+1))
            enemie = Enemy(y = 400,pos_hint = {'center_x':(pos+(pos*(i)))})

            
            
            self.parent.add_widget(enemie)
            self.parent.enemies.append(enemie)
            
        
    
        
class MyApp(App):
    def build(self):
        x = Fondo()
        return x
    

if __name__ in ('__main__', '__android__'):
    MyApp().run()
        
        
    
        
        
        