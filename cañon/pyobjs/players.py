#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __init__ import *
#CARPETAS DEL PROYECTO
patch = os.path.dirname(os.path.abspath(__file__))
asset = patch + '/assets/drawable-mdpi/'
color = patch + '/colors/'
font = patch + '/fonts/'

class Enemy(RelativeLayout):
    def __init__(self,**kwargs):
        super(Enemy, self).__init__(**kwargs) 
        self.size_hint = (None,None)
        self.size = (50,75)
        self.lives = 3
        self.notmob = Image(size_hint = (.9,.9),pos_hint = {'center_x':.5,'center_y':.5},source = color + "8.png", keep_ratio = False, allow_stretch = True)
        self.add_widget(self.notmob)
        Clock.schedule_interval(self.animation, .5)
		
    def impacto(self,*args):
		self.notmob.source = color + "10.png"
		def cambio():
			print "pass"
			self.notmob.source = color + "8.png"
		Clock.schedule_once(lambda x:cambio() , 0.05)
		
    def animation(self,*args):
        my_animation = Animation(size_hint = (.95,.95), d = .25, t = 'out_quart') + Animation(size_hint = (.9,.9), d = .25, t = 'out_quart')
        my_animation.start(self.notmob)
        
class Ammo(RelativeLayout):
    def __init__(self,**kwargs):
        super(Ammo, self).__init__(**kwargs)
        
        self.size_hint = (None,None)
        self.size = (10,20)
        self.img = Image(source = color + "7.png", keep_ratio = False, allow_stretch = True)
        self.add_widget(self.img)
        self.alimit = kwargs["alimit"]
        self.pos = kwargs["player"].pos
        self.y += kwargs["player"].height
        self.x += kwargs["player"].width /2 - 5
        self.jugador =kwargs["player"]
        #Clock.schedule_interval(self.check_area, 1.0)
        Clock.schedule_interval(self.update, 1.0/60.0)
    def impacto(self,*args):
		self.img.source = color + "None.png"
		
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
        self.y += 5
            
class Player(RelativeLayout):#COMPLEMENTO 'PARENT' EL PROYECTO
    def __init__(self, **kwargs):
        super(Player, self).__init__(**kwargs)
        self.ammos = []
        self.alimit = kwargs["ammo_lim"]
        self.size_hint = (None,None)
        self.size = (50,75)
        self.add_widget(Image(source =  color + "5.png", keep_ratio = False, allow_stretch = True))
        Clock.schedule_interval(self.animation, .5)
        Clock.schedule_interval(self.shooting, 1)
        
    def shooting(self,*args):
        if len(self.ammos) <= 20:
            
            shoot = Ammo(player = self,alimit = self.alimit) 
            self.ammos.append(shoot)
            self.parent.add_widget(shoot)
        else:
            self.ammos[0].repos()
            self.ammos[0].img.source = color + "7.png"
            self.ammos.append(self.ammos.pop(self.ammos.index(self.ammos[0])))

        
    def animation(self,*args):
        my_animation = Animation(width = 55,height = 70, d = .25, t = 'out_quart') + Animation(width = 50,height = 75, d = .25, t = 'out_quart')
        my_animation.start(self)
        
    def move_x(self,**kwargs):
        self.x += kwargs["amount"]
        
    

    
    
    
    
    