#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __init__ import *
#CARPETAS DEL PROYECTO
patch = os.path.dirname(os.path.abspath(__file__))
asset = patch + '/assets/drawable-mdpi/'
color = patch + '/colors/'
font = patch + '/fonts/'
class WorkerThread(threading.Thread):
    def __init__(self,*args):
        super(WorkerThread,self).__init__()


        self.stop = False
    def stop_it(self): 
        self.stop = True
        print "me he detenido"
    def run(self):




        if self.stop:
            return


class Enemy(RelativeLayout):
    def __init__(self,**kwargs):
        super(Enemy, self).__init__(**kwargs) 
        self.size_hint = (None,None)
        self.size = (70,75)
        self.lives = 3
        self.notmob = Image(size_hint = (.9,.9),pos_hint = {'center_x':.5,'center_y':.5},source =  "en.png", keep_ratio = False, allow_stretch = True)
        self.notmob1 = Image(opacity = 0,size_hint = (.9,.9),pos_hint = {'center_x':.5,'center_y':.5},source =  "en2.png", keep_ratio = False, allow_stretch = True)
        self.add_widget(self.notmob)
        self.add_widget(self.notmob1)
        Clock.schedule_interval(self.animation, .5)
		
    def impacto(self,**kwargs):
        self.notmob1.opacity = 1
        a = Animation(opacity = 0 , d = .5 , t = 'out_quart')

        if kwargs["destroy"] == True:
            a.start(self.notmob)


        a.start(self.notmob1)
        


    def animation(self,*args):
        my_animation = Animation(size_hint = (.95,.95), d = .25, t = 'out_quart') + Animation(size_hint = (.9,.9), d = .25, t = 'out_quart')
        my_animation.start(self.notmob)
        
class Ammo(RelativeLayout):
    def __init__(self,**kwargs):
        super(Ammo, self).__init__(**kwargs)
        self.activo = True
        self.exploding = False
        self.size_hint = (None,None)
        self.size = (10,12)
        self.img = Image(size_hint = (None,None), size = (20,22), pos_hint = {'center_x':.5, 'center_y':.5},source =  "d.png", keep_ratio = False, allow_stretch = True)
        self.add_widget(self.img)
        self.alimit = kwargs["alimit"]
        self.pos = kwargs["player"].pos
        self.y += kwargs["player"].height
        self.x += kwargs["player"].width /2 - 5
        self.jugador =kwargs["player"]
        #Clock.schedule_interval(self.check_area, 1.0)
        self.explode = Image(opacity = 0,size_hint = (None,None), size = (76,76), pos_hint = {'center_x':.5, 'center_y':.5},source =  "explode.png", keep_ratio = False, allow_stretch = True)
        self.add_widget(self.explode)
        #Clock.schedule_interval(self.update, 1.0/60.0)
        
        t = threading.Thread(target=Clock.schedule_interval(self.update, 1.0/60.0))
    def impacto(self,*args):
        def hide(*args): self.img.source = color + "None.png"
        def hide1(*args): self.exploding = False
        self.img.opacity = 0
        
        
        b = Animation(opacity = 1 , d = .225     , t= 'out_quart') +  Animation(opacity = 0 , d = .150 , t= 'out_quart')
        b.bind(on_complete =  hide1)
        t = threading.Thread(target=b.start(self.explode))
        
        self.exploding = True
		
    def repos(self):
        self.pos = self.jugador.pos
        self.y += self.jugador.height
        self.x += self.jugador.width /2 - 5
        
    def check_area(self,*args):
        print self.y, self.alimit
        if int(self.y) > (self.alimit - 50):
            try:
                self.parent.remove_widget(self)
            except:
                pass
            
    def update(self,*args):
        
        if self.exploding == True:
            pass
        else:
            self.y += 3.5
        
            
class Player(RelativeLayout):#COMPLEMENTO 'PARENT' EL PROYECTO
    def __init__(self, **kwargs):
        super(Player, self).__init__(**kwargs)
        self.ammos = []
        self.alimit = kwargs["ammo_lim"]
        self.size_hint = (None,None)
        self.size = (78,56)
        self.add_widget(Image(source = "123.png", keep_ratio = True, allow_stretch = True))
        #Clock.schedule_interval(self.animation, .5)
        Clock.schedule_interval(self.shooting, .5)
        
    def shooting(self,*args):
        if len(self.ammos) <= 20:
            
            shoot = Ammo(player = self,alimit = self.alimit) 
            self.ammos.append(shoot)
            self.parent.add_widget(shoot)
        else:
            self.ammos[0].repos()
            self.ammos[0].img.source = "d.png"
            self.ammos[0].img.opacity = 1
            self.ammos[0].img.size = (20,22)
            self.ammos[0].activo = True
            self.ammos.append(self.ammos.pop(self.ammos.index(self.ammos[0])))

        
    def animation(self,*args):
        my_animation = Animation(width = 55,height = 70, d = .25, t = 'out_quart') + Animation(width = 50,height = 75, d = .25, t = 'out_quart')
        my_animation.start(self)
        
    def move_x(self,**kwargs):
        self.x += kwargs["amount"]
        
    

    
    
    
    
    