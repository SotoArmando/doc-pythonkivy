#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pyobjs.__init__ import *
#CARPETAS DEL PROYECTO
patch = os.path.dirname(os.path.abspath(__file__))
asset = patch + '/pyobs/assets/drawable-mdpi/'
color = patch + '/pyobs/colors/'
font = patch + '/pyobs/fonts/'




class InterfaceManager(RelativeLayout):
    def __init__(self, **kwargs):
        super(InterfaceManager, self).__init__(**kwargs)
        self.objs = []
        self.enemies = []
        self.objs1 = []
        self.config = {"Floor": 100,
                       "Player_speed":5,
                       "Gravity":3,
                       "Player1":None,
                       "Limite": Window.height - 300
                      
                       
        }
        self.states = {"Moving": -1,
                       "Side": -1,
        }
        self.init_game()
        Clock.schedule_interval(self.update, 1.0/60.0)
        
        
        
    def on_touch_up(self, touch):
        self.states["Moving"] = -1
            
    def on_touch_down(self, touch):
        print touch.pos
        y_middle  = Window.height /2 
        x_middle  = Window.width /2 
        
        if touch.pos[0] > x_middle:
            self.states["Side"] = 1
        else:
            self.states["Side"] = -1
        self.states["Moving"] = 1
            
            
    def update(self,*args):
    
        for i in self.objs:
            try:
                if i.y > self.config["Floor"]:  
                    i.y -= self.config["Gravity"]
            except:
                pass
        if self.states["Moving"] == 1:
            self.config["Player1"].move_x(amount = self.config["Player_speed"] * self.states["Side"])
 
        for i in self.enemies:
            for x in self.new_player.ammos:
                if x.collide_widget(i):
                    try:
                        #x.parent.remove_widget(x)
                        #i.parent.remove_widget(i)
                        #self.enemies.remove(i)

                        if x.img.source[-5:] == (color + "7.png")[-5:]:
                            i.lives -= 1
                            if i.lives == 0:
                                i.parent.remove_widget(i)
                                self.enemies.remove(i)
                            i.impacto()
                            x.impacto()
                        elif x.img.source == "None.png":
                            pass
                    except:
                        pass


    def init_game(self,**kwargs):
        from pyobjs.players import Player, Enemy
        self.new_player = Player(y = self.config["Floor"]+200,ammo_lim = self.config["Limite"])
        self.objs.append(self.new_player)
        self.add_widget(self.new_player)
        self.config["Player1"] = self.new_player
        pos_init = Window.width / 8

        for i in range(8):
            enemie = Enemy(y = 500,x = (pos_init *(i))+25)
            self.enemies.append(enemie)
            self.add_widget(enemie)
         
        


    
    
    
    
    