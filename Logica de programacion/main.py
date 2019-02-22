#!/usr/bin/env python
# -*- coding: latin-1 -*-

import sys  
reload(sys)  
sys.setdefaultencoding('latin-1')

from kivy.config import Config
Config.set('graphics','borderless', 1)
Config.set('graphics','position','custom')
Config.set('graphics','window_state','visible')
Config.set('graphics','resizable',0)
Config.set('graphics','left',500)
Config.set('graphics','top',35)

from kivy.core.window import Window
from kivy.animation import Animation
from kivy.metrics import dp,sp, MetricsBase
from kivy.resources import resource_add_path
from kivy.uix.screenmanager import ScreenManager, Screen,CardTransition,SwapTransition, NoTransition,SlideTransition,FadeTransition,WipeTransition,FallOutTransition,NoTransition ,RiseInTransition 
from kivy.uix.button import Button
from kivy.uix.relativelayout import RelativeLayout
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.image import Image,AsyncImage
from kivy.uix.scrollview import ScrollView
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.checkbox import CheckBox
from kivy.uix.scatterlayout import ScatterLayout as Scatter
from kivy.uix.textinput import TextInput
from kivy.graphics import Color, Line, Rectangle
import os   
import os.path
import datetime


from navigator import ImageButton,NavigationDrawer
from utils import GridButton,TwoLineItem,SearchItem,MateriaTitle,TopNavigationS,Datingscreen,BottomNavigation,CustTextInput

resource_add_path(os.path.dirname(__file__))

from kivy.uix.behaviors import ButtonBehavior
from kivy.animation import Animation
from kivy.uix.widget import Widget
from kivy.uix.stencilview import StencilView
from kivy.metrics import dp
from kivy.clock import Clock
from kivy.properties import (ObjectProperty, NumericProperty, OptionProperty,
                             BooleanProperty, StringProperty)
from kivy.resources import resource_add_path
from kivy.lang import Builder
import os.path

Window.size = (360,640)


C1 = "[color=#13C0C7]"
C4 = "[color=#000000]"
C2 = "[color=#404040]"
C3 = "[color=#ff3333]"
C5 = "[color=#f2f2f2]"
C6 = "[color=#95989A]"
C7 = "[color=#cccccc]"
EC = "[/color]"



patch = os.path.dirname(os.path.abspath(__file__))
asset = patch + '/assets/drawable-mdpi/'
color = patch + '/colors/'
font = patch + '/fonts/'
unidades = patch + '/unidades/'
unidades_imagenes = patch + '/unidades/imagenes/'

Window.clearcolor = (1,1,1,1)

alerta_content = GridLayout(cols = 1)
alerta_content.add_widget(Button(size_hint_y = None, height = dp(50),text_size = (dp(250),dp(50)),font_size = '16sp',valign = 'top',font_name = font+"Roboto-Regular.ttf",markup = True,text = C4+"Deseas descargar el material de apoyo de esta materia?", background_normal = color + "16.png"))
alerta_content.add_widget(Button(text_size = (dp(250),dp(30)),font_size = '16sp',valign = 'top',font_name = font+"Roboto-Light.ttf",markup = True,text = C4+"Si", background_normal = color + "16.png"))
alerta_content.add_widget(Button(text_size = (dp(250),dp(30)),font_size = '16sp',valign = 'top',font_name = font+"Roboto-Light.ttf",markup = True,text = C4+"No", background_normal = color + "16.png"))
alerta0 = Popup(title_size = '20sp',title_color = [0,0,0,1], title = "Descargar Contenido",content = alerta_content, size_hint = (None,None), size = ('300dp','200dp'),
separator_color = (0,0,0,0),background = color + "16.png")


class InterfaceManager(RelativeLayout):
    def __init__(self, **kwargs):
        self.data = {}
        self.data['usuarios'] = []
        super(InterfaceManager, self).__init__(**kwargs)
        self.state0 = -1
        self.state1 = -1
        self.state2 = -1
        self.state3 = -1
        self.navigatorwid = NavigationDrawer()
        
        self.navbar = RelativeLayout()
        self.navbar.add_widget(Image(size_hint = (None,None), size = (1000,1000),source = "16.png", keep_ratio = False, allow_stretch = True))
        
        self.navbar_parent = GridLayout(padding = [20,0,0,0],cols = 3, spacing = [20,0])
        self.navbar.add_widget(self.navbar_parent)
        self.navbar_parent.add_widget(Label(size_hint_y = None , height = dp(90), size_hint_x = None, width = '25dp'))
        self.navbar_parent.add_widget(Label(size_hint_y = None , height = dp(90), size_hint_x = None, width = '25dp'))
        self.navbar_parent.add_widget(Label(size_hint_y = None , height = dp(90)))
        #self.navbar_parent.add_widget(Label(size_hint_y = None , height = dp(90)))

        self.navigatorwid.add_widget(self.navbar)
        buttons = ["Inicio","Agenda","Carpetas","Busqueda","Papelera","Cerrar Session"]
        buttons_img = ["home.png","history-button.png","garbage.png","heart.png","continuous-line-clock.png"]

        for i in range(6): 
            self.navbar_parent.add_widget(Label(size_hint_y = None , height = dp(49), size_hint_x = None, width = '25dp'))
            #self.navbar_parent.add_widget(Image(size_hint_x = None,size_hint_y = None , height = '60dp', width ='25dp', source = asset + buttons_img[i]))
            button3 =Button(valign = "middle",opacity = .84,text_size = (dp(120),dp(60)),size_hint_x = None, width = dp(90),font_name = font + "Roboto-Medium.ttf",markup = True,font_size = '14sp',background_normal = color+"16.png",background_down = color+"16.png",text = C4+buttons[i],size_hint_y = None, height = dp(60))

            if i == 0:button3.bind(on_release = lambda x: self.choose("1"))#inicio
            elif i == 1:button3.bind(on_release = lambda x: self.choose("4"))#Agenda
            elif i == 2:button3.bind(on_release = lambda x: self.choose("1"))#Carpetas
            elif i == 3:button3.bind(on_release = lambda x: self.animarbuscador())#Busqueda
            elif i == 4:button3.bind(on_release = lambda x: self.choose("6"))#Papelera
            elif i == 5:button3.bind(on_release = lambda x: self.choose("5"))#Cerrar Cesion
            self.navbar_parent.add_widget(button3)
            self.navbar_parent.add_widget(Label(size_hint_y = None, height = '49dp'))
            button3.bind(on_release = lambda x: self.navigatorwid.toggle_state())
        
        
        #self.add_widget(self.navigatorwid)  

        
        main_parent = RelativeLayout()

        
        days = ["Lunes","Martes","Miercoles","Jueves","Viernes","Sabado","Domingo"]
        self.label1 =Label(opacity = 0.,font_size = "32sp",size_hint = (1,None),width = dp(200) , height = 0 ,text_size = (Window.width - dp(50), dp(150)),pos_hint = {'x': 0., 'center_y':.75},halign = 'right', valign = 'top',markup = True, text =  C4+days[datetime.datetime.today().weekday()])
        main_parent.add_widget(Image(opacity = .74,y = Window.height - dp(300),source = asset + "student-graduation-cap-shape.png", keep_ratio = True, allow_stretch = False, size_hint_y = None , height = Window.height*.35))
        main_parent.add_widget(Image(opacity = .24,source = color + "3.png", keep_ratio = False, allow_stretch = True, size_hint_y = 1 , height = Window.height*.35))
        
        self.main = ScreenManager() 
        main_parent.add_widget(self.label1)
        main_parent.add_widget(Label(opacity = .54,font_size = "24sp",size_hint = (1,None),width = dp(200) , height = 0 ,text_size = (Window.width - dp(50), dp(150)),pos_hint = {'x': 0., 'center_y':.525},halign = 'right', valign = 'top',markup = True, text =  C4+"Armando Jose Soto")) 
        main_parent.add_widget(Label(opacity = .54,font_size = "20sp",size_hint = (1,None),width = dp(200) , height = 0 ,text_size = (Window.width - dp(50), dp(150)),pos_hint = {'x': 0., 'center_y':.475},halign = 'right', valign = 'top',markup = True, text =  C4+"1066320"))
        
        main_parent.add_widget(self.main)
        self.add_widget(main_parent)

        #self.add_widget(Button(font_name = font + "Roboto-Light.ttf", font_size = '17sp',halign = "left",text = C4 + "",markup = True,text_size = (dp(200), dp(45)),pos = (0,Window.height - dp(95)), size_hint = (1,None), height = dp(95), background_normal = asset + "Repeat Grid 8.png", background_down = asset + "Repeat Grid 8.png", keep_ratio = False, allow_stretch = True))
        #self.add_widget(ImageButton(,pos = (0,Window.height - dp(84)), size_hint = (None,None),width = dp(49), height = dp(49), source = asset + "Group 55.png"))
        #self.add_widget(ImageButton(opacity = .54,on_release = lambda x: self.animarbuscador(),pos = (Window.width - dp(49),Window.height - dp(84)), size_hint = (None,None),width = dp(50), height = dp(50), source = asset + "Group 100.png"))
        self.titulo = Label(opacity = .74,font_name = font + 'segoescb.ttf',font_size = '20sp',text = C4+"Codi", markup = True, pos_hint = {'center_x':.5}, y = Window.height - dp(85), size_hint = (None,None), size = (dp(100),dp(50)))
        #self.add_widget(self.titulo)
        self.buscador1 = TextInput(padding = [15,7,0,0],background_normal = asset+'Rectangle 7.png', background_active = asset+'Rectangle 7.png',opacity = 0,font_size = '14sp',multiline = False,hint_text = "Materia", markup = True, pos_hint = {'center_x':.5}, y = Window.height - dp(75), size_hint = (None,None), size = (dp(226),dp(29)))
        #self.add_widget(self.buscador1)
        #self.add_widget(ImageButton(source = asset+"Group 33.png",size_hint = (None,None), pos_hint = {'center_x': .15,'center_y': .15}))
        self.buscador = TopNavigationS()
        self.buscador.leftbutton().bind(on_release = lambda x: self.navigatorwid.toggle_state())
        self.buscador.textinput().bind(on_text_validate = lambda x: self.buscarmaterias())
        self.buscador.rightbutton().bind(on_release = lambda x: self.choose("busqueda"))
        self.add_widget(self.buscador)
        self.bottommenu = BottomNavigation(opacity = 0.)
        screens = ["1","4","3","5"]

        self.bottommenu.buttons()[0].bind(on_release = lambda x: self.choose("1"))
        self.bottommenu.buttons()[1].bind(on_release = lambda x: self.choose("4"))
        self.bottommenu.buttons()[2].bind(on_release = lambda x: self.choose("6"))
        self.bottommenu.buttons()[3].bind(on_release = lambda x: self.choose("5"))
        self.add_widget(self.bottommenu)
        #self.add_widget(ImageButton(source = asset+"Group 33.png",size_hint = (None,None), pos_hint = {'center_x': .15,'center_y': .15}))
        self.mainmenu = RelativeLayout(cols = 1, pos = (0,'-350dp'), height = '400dp', size_hint_y = None) ;# self.add_widget(self.mainmenu)
        self.mainmenu_backgroundcolor = Image(y = dp(-50),source = color + "16.png", keep_ratio = False, allow_stretch = True);self.mainmenu.add_widget(self.mainmenu_backgroundcolor)
        self.screen1()
        self.screen2()
        self.screen3()
        self.screen4()
        self.screen5()
        self.screen6()
        self.screen7()
        self.busquedascreen()
        self.main.transition = NoTransition()
        self.main.current = '5'
        self.main.transition = SlideTransition()
        
        button0_parent = RelativeLayout(size_hint_y = None , height = '50dp')
        #self.button0 = ImageButton(size_hint = (1,1),width = '31dp' ,height = '7dp', source = asset + "Group 54.png")
        

        mainmenu_parent = GridLayout(cols = 1);  self.mainmenu.add_widget(mainmenu_parent)
        imagebutton0 = ImageButton(keep_ratio = False, allow_stretch = True,size_hint = (1,None) ,height = '50dp', source = asset + "Repeat Grid 17.png",)
        button0_parent.add_widget(imagebutton0)
        #button0_parent.add_widget(self.button0)
        imagebutton0.bind(on_release = lambda x: self.Openmainmenu())
        mainmenu_scroll = ScrollView()
        mainmenu_parent.add_widget(button0_parent) 
        mainmenu_parent.add_widget(Image(source = color + "16bb.png", size_hint_y = None, height = 1, keep_ratio = False, allow_stretch = True)) 
        mainmenu_parent.add_widget(mainmenu_scroll)
        mainmenu_scrollparent1 = GridLayout(cols = 2, size_hint_y = None, height = 150) ; mainmenu_scroll.add_widget(mainmenu_scrollparent1)
        
        
        Unidades = ["Funciones","Variables","Constantes","Clases","Que es Lambda"]
        #Agregar Buscador
        mainmenu_scrollparent1.add_widget(Button(size_hint_x = None,font_size = '40sp',size_hint_y = None , height = '90dp', font_name = font + "Bevan.ttf", width = '75dp', background_normal = color + "None.png", text = "[color=#000000]", markup = True ))
        mainmenu_scrollparent1.add_widget(Button(font_size = '12sp',markup = True,font_name = font+"Roboto-Regular.ttf",text = C4+"[size=20sp]"+"Buscador"+"[/size]\nTocar para abrir Buscador.",background_normal = color + "None.png",size_hint_y = None , height = '75dp', line_height = 1.4, text_size = (Window.width - dp(75),dp(75)),halign='left', valign = 'middle'))
        
        x = 1
        for i in Unidades: #Agregar Unidad
            if Unidades.index(i) % 2 == 1: background = color + "16.png"
            if Unidades.index(i) % 2 == 0: background = color + "16bb.png"
            mainmenu_scrollparent1.add_widget(Button(size_hint_x = None,font_size = '40sp',size_hint_y = None , height = '75dp', font_name = font + "Bevan.ttf", width = '75dp', background_normal = background, text = "[color=#000000]i", markup = True ))
            mainmenu_scrollparent1.add_widget(Button(font_size = '12sp',markup = True,font_name = font+"Roboto-Regular.ttf",text = C4+"[size=20sp]"+i+"[/size]\n[color=#000000]Tocar para ver contenido.",background_normal = background,size_hint_y = None , height = '75dp', line_height = 1.4, text_size = (Window.width - dp(75),dp(75)),halign='left', valign = 'middle'))
            mainmenu_scrollparent1.height += dp(90) 

    def favorito(self,button):
        self.state2 *= -1
        if self.state2 == 1:
            x_anim = Animation(opacity = 1., d = .10)
            x_anim.start(button)
            print 0
        else:
            x_anim = Animation(opacity = 0., d = .10)
            x_anim.start(button)
            pass
    def sumpos(self,x):
        listadepos = []
        for i in x: listadepos.append([i[0],i[1]])
        newpos = [-100,-100]
        for i in listadepos:
            print i
            newpos[0] += i[0]
            newpos[1] += i[1]
        print (newpos[0],newpos[1])
        return (newpos[0],newpos[1])
    def newpos(self): self.boxwidget_parent.pos = (0,0)
    def animarbuscador(self):

    
        x_anim = Animation(opacity = .54,d = .30,t = 'in_quart')
        
        x_anim1 = Animation(opacity = .74,d = .30,t = 'in_quart')
        x_anim2 = Animation(opacity = 0.,d = .30,t = 'out_quart')
        x_anim3 = Animation(opacity = 0.,d = .30,t = 'out_quart')
        if self.buscador1.opacity == .74:
            x_anim2.start(self.buscador1)
            x_anim2.bind(on_complete = lambda x,y:x_anim1.start(self.titulo))
            x_anim1.bind(on_complete = lambda x,y:x_anim.start(self.label0))
            x_anim.bind(on_complete = lambda x,y:self.choose('1'))
        else:
            x_anim2.start(self.titulo)
            
            x_anim2.bind(on_complete = lambda x,y:x_anim1.start(self.buscador1))
            x_anim2.bind(on_complete = lambda x,y:x_anim3.start(self.label0))
            x_anim3.bind(on_complete = lambda x,y:self.choose('busqueda'))
            
        self.choose("busqueda")
    def next(self): self.main.current = self.main.next()
    def back(self): self.main.current = self.main.previous()
    def choose(self,str): 
        if str == "1": 
            anim = Animation(opacity = .54, d = .325 , t = 'in_circ')
            anim1 = Animation(opacity = 1, d = .325 , t = 'in_circ')
            anim.start(self.label1)
            anim1.start(self.bottommenu)
        else:
            anim = Animation(opacity = 0., d = .325 , t = 'out_circ')
            anim.start(self.label1)
        self.main.current = str; print str
        if str == "3":
            self.screen3_scrollview.scroll_y = 1
            
    
    
    def Openmainmenu(self):
        self.state0 *= -1
        
        if self.state0 == 1 : A1 = Animation(pos = (0,0)); opac = .2
        else: A1 = Animation(pos = (0,dp(-350))) ; opac = 1
        
        A1.start(self.mainmenu)
        #with self.button0.canvas:
        #    A2 = Animation(opacity = opac )
        #    A2.start(self.button0)
        
    def busquedascreen(self):
        busqueda_screen = Screen(name = 'busqueda')
        busqueda_screen.add_widget(Image(source = color + "16.png", keep_ratio = False , allow_stretch = True))
        self.main.add_widget(busqueda_screen)
        self.busqueda_pariente = ScrollView()
        busqueda_screen.add_widget(self.busqueda_pariente)
        self.busqueda_pariente_hijo = GridLayout(cols = 1, size_hint_y = None, height = dp(1000), spacing = 0)
        self.busqueda_pariente.add_widget(self.busqueda_pariente_hijo)
        self.busqueda_pariente_hijo.add_widget(Label(size_hint_y = None , height = dp(150)))
        
    def screen1(self):
        screen = Screen(name = "1")
        
        self.screen_parent = GridLayout(cols = 1, size_hint_y = None, height = dp(1200))
        
        a = Label(size_hint_y = None , height = '80dp')  
        b_backgroundcolor = Image(y = dp(300),source = color + "16.png", keep_ratio = False, allow_stretch = True)
        
        self.screen_parent.add_widget(a)
        self.screen_parent.add_widget(Label(size_hint_y = None , height = Window.height*.30))
        self.screen_parent.add_widget(Image(y = dp(-27), size_hint_y = None, height = dp(27),opacity= 1.,source = asset + "Repeat Grid 27.png", keep_ratio = False, allow_stretch = True))
        self.screen_parent.add_widget(Image(opacity = .14,source = color + "2.png", size_hint_y = None , height = '1dp', keep_ratio = False, allow_stretch = True))
        self.screen_parent.add_widget(Datingscreen())
        
        self.main.add_widget(screen)
        parent_scrollview = ScrollView(do_scroll_x = False)
        parent_scrollview.add_widget(self.screen_parent)
        screen.add_widget(parent_scrollview)
        self.label0 = Button(background_normal = color + "16.png",opacity = 1,font_name = font+'segoe-ui.ttf',halign = 'center',font_size = '20sp',size_hint_y = None ,text_size = (dp(250),dp(100)), height = '200dp', text = '[color=#595959]'+'No tienes ninguna materia agregada',markup = True)
        self.screen_parent.add_widget(self.label0)
        self.screen_parent.add_widget(Image(source = color + "16.png", keep_ratio = False, allow_stretch = True))
        #screen.add_widget(Button(opacity = .91,background_normal = asset + 'ic_add.png',background_down = asset + 'ic_add.png',pos_hint = {'center_x':.8, 'center_y':.1},size_hint = (None,None), size = (dp(81),dp(89))))
        
    def agregarmateria(self):   
        BC1 = '[color=#0090FF]'
        BC2 = '[color=#F45D5D]'
        try:
            self.label0.parent.remove_widget(self.label0)
        except:
            pass
        
        pariente = GridLayout(rows = 2, size_hint_y = None, height = dp(69))
        pariente_titulo_dim = RelativeLayout(size_hint_y = None, height = dp(69))
        pariente_titulo = GridLayout(rows = 1, size_hint_y = None, height = dp(69))
        pariente_hijos = GridLayout(opacity = 0.,cols = 1,size_hint_y = None , height = 0)
        
        pariente_titulo_dim.add_widget(Image(source = color + '3.png',keep_ratio = False, allow_stretch = True))
        pariente_titulo_dim.add_widget(pariente_titulo)
        titulo1 = MateriaTitle()
        pariente.add_widget(titulo1)
        pariente.add_widget(pariente_hijos)
        
        def open(x):
            print "hola"
            print x
            print x.children
            x_height = 0

            for i in pariente_hijos.children:
                x_height += i.height
            
            if pariente_hijos.height == 0:
                
                x_anim1 = Animation(opacity = 1.,height = x_height ,d = .5, t = 'out_quart')
                x_anim2 = Animation(height = x_height+dp(69), d = .5, t = 'out_quart')
                x_anim1.start(x)
                x_anim2.start(x.parent)
            elif pariente_hijos.height == x_height:
                
                x_anim1 = Animation(opacity = .24,height = 0, d = .5, t = 'out_quart')
                x_anim2 = Animation(height = dp(69), d = .5, t = 'out_quart')
                x_anim1.start(x)
                x_anim2.start(x.parent)
                

                
        titulo1.leftbutton().bind(on_release = lambda x: open(x.parent.parent.parent.parent.parent.parent.parent.children[0]))
        pariente_titulo.add_widget(ImageButton(on_release = lambda x: open(x.parent.parent.parent.children[0]),size_hint_x = None ,width = dp(50), source = asset + "Group 126.png"))
        pariente_titulo.add_widget(Label(halign = 'center',text_size = (dp(200),None),markup = True ,font_name = font + 'Roboto-Light.ttf',font_size = '14sp', text = "Logica de Programacion", size_hint_x = None, width = '180dp'))
        pariente_titulo.add_widget(Label(halign = 'center',text_size = (dp(65),None),markup = True ,font_name = font + 'Roboto-Medium.ttf',font_size = '14sp', text = BC1 + "@Lorenzo", size_hint_x = None, width = '50dp'))
        pariente_titulo.add_widget(Label())
        pariente_titulo.add_widget(Button(size_hint_x = None ,width = dp(69),background_normal = asset + "Group 127.png"))
        
        #DOCUMENTOS DE LA MATERIA
        def documento():
            pariente2 = GridLayout(cols = 3, size_hint_y = 1)
            pariente2.add_widget(Label(opacity = .54,text_size = (dp(71),dp(50)),valign = 'bottom',halign = 'left',text = C4+'1m', markup = True))
            pariente2_hijo = GridLayout(cols = 1)
            pariente2_hijo.add_widget(Label(opacity = .54,text_size = (dp(200),dp(25)),valign = 'bottom',halign = 'left',text = C4+'@Lorenzo', markup = True))
            pariente2_hijo.add_widget(Label(opacity = .54,text_size = (dp(200),dp(25)),valign = 'bottom',halign = 'left',text = C4+'Archivo Importante', markup = True))
            pariente2_hijo_botones = GridLayout(opacity = .54,rows = 1)
            pariente2_hijo_botones.add_widget(ImageButton(source = asset + 'like.png'))
            pariente2_hijo_botones.add_widget(ImageButton(source = asset + 'retweet.png', markup = True))
            pariente2_hijo_botones.add_widget(Label())
            pariente2.add_widget(pariente2_hijo);pariente2_hijo.add_widget(pariente2_hijo_botones)
            pariente2.add_widget(Label(opacity = .54,text_size = (dp(71),dp(50)),valign = 'bottom',halign = 'center',text = C4+'.Doc', markup = True))
            return pariente2
        
        boton = TwoLineItem("Clase 6","Archivo.txt")
        boton.returngo().bind(on_release = lambda x: self.choose("3"), on_press = lambda x: self.abrirdoc("U5.txt"))
        boton1 = TwoLineItem("Clase 7","Archivo.txt")
        boton1.returngo().bind(on_release = lambda x: self.choose("3"), on_press = lambda x: self.abrirdoc("U6.txt"))
        boton2 = TwoLineItem("Clase 8","Archivo.txt")
        boton2.returngo().bind(on_release = lambda x: self.choose("3"), on_press = lambda x: self.abrirdoc("U7.txt"))
        boton3 = TwoLineItem("Clase 1","Archivo.txt")
        boton3.returngo().bind(on_release = lambda x: self.choose("3"), on_press = lambda x: self.abrirdoc("U1.txt"))
        
        boton4 = TwoLineItem("Clase 2","Archivo.txt")
        boton4.returngo().bind(on_release = lambda x: self.choose("3"), on_press = lambda x: self.abrirdoc("U2.txt"))
        boton5 = TwoLineItem("Clase 3","Archivo.txt")
        boton5.returngo().bind(on_release = lambda x: self.choose("3"), on_press = lambda x: self.abrirdoc("U3.txt"))
        boton6 = TwoLineItem("Clase 4","Archivo.txt")
        boton6.returngo().bind(on_release = lambda x: self.choose("3"), on_press = lambda x: self.abrirdoc("U4.txt"))
        
        
        pariente_hijos.add_widget(boton3)
        pariente_hijos.add_widget(Image(opacity = .24,size_hint_y = None , height = dp(1) , source = color + '3.png', keep_ratio = False, allow_stretch = True))
        
        pariente_hijos.add_widget(boton4)
        pariente_hijos.add_widget(Image(opacity = .24,size_hint_y = None , height = dp(1) , source = color + '3.png', keep_ratio = False, allow_stretch = True))
        pariente_hijos.add_widget(boton5)
        pariente_hijos.add_widget(Image(opacity = .24,size_hint_y = None , height = dp(1) , source = color + '3.png', keep_ratio = False, allow_stretch = True))
        pariente_hijos.add_widget(boton6)
        pariente_hijos.add_widget(Image(opacity = .24,size_hint_y = None , height = dp(1) , source = color + '3.png', keep_ratio = False, allow_stretch = True))
        
        pariente_hijos.add_widget(boton)
        pariente_hijos.add_widget(Image(opacity = .24,size_hint_y = None , height = dp(1) , source = color + '3.png', keep_ratio = False, allow_stretch = True))
        #pariente_hijos.add_widget(Image(size_hint_y = None, height = dp(100),source = color + "16.png", keep_ratio = False, allow_stretch = True))
        pariente_hijos.add_widget(boton1)
        pariente_hijos.add_widget(Image(opacity = .24,size_hint_y = None , height = dp(1) , source = color + '3.png', keep_ratio = False, allow_stretch = True))
        #pariente_hijos.add_widget(Image(size_hint_y = None, height = dp(100),source = color + "16.png", keep_ratio = False, allow_stretch = True))
        pariente_hijos.add_widget(boton2)
        pariente_hijos.add_widget(Image(opacity = .24,size_hint_y = None , height = dp(1) , source = color + '3.png', keep_ratio = False, allow_stretch = True))
        pariente_hijos.add_widget(TwoLineItem("Clase 9","Archivo.txt"))
        pariente_hijos.add_widget(Image(opacity = .24,size_hint_y = None , height = dp(1) , source = color + '3.png', keep_ratio = False, allow_stretch = True))
        pariente_hijos.add_widget(TwoLineItem("Clase 10","Archivo.txt"))
        pariente_hijos.add_widget(Image(opacity = .24,size_hint_y = None , height = dp(1) , source = color + '3.png', keep_ratio = False, allow_stretch = True))
        pariente_hijos.add_widget(TwoLineItem("Clase 11","Archivo.txt"))
        pariente_hijos.add_widget(Image(opacity = .24,size_hint_y = None , height = dp(1) , source = color + '3.png', keep_ratio = False, allow_stretch = True))
        
        
        
        
        #pariente_hijos.add_widget(Image(size_hint_y = None, height = dp(100),source = color + "16.png", keep_ratio = False, allow_stretch = True))
        pariente_hijos.add_widget(Image(size_hint_y = None, height = dp(100),source = color + "16.png", keep_ratio = False, allow_stretch = True))
        
        self.screen_parent.remove_widget(self.screen_parent.children[0])
        self.screen_parent.add_widget(pariente)
        self.screen_parent.add_widget(Image(source = color + "16.png", keep_ratio = False, allow_stretch = True))
        self.choose('1')
        self.buscador.search_animate()
        
    def buscarmaterias(self):
        BC1 = '[color=#0090FF]'
        BC2 = '[color=#F45D5D]'
        self.busqueda_pariente_hijo.clear_widgets()
        self.busqueda_pariente_hijo.add_widget(Label(size_hint_y = None , height = dp(100)))
        for i in range(1): 
            self.busqueda_pariente_hijo.add_widget(self.searchitem())
        self.busqueda_pariente_hijo.add_widget(Image(opacity =  1,source = color + '16.png', keep_ratio = False, allow_stretch = True, size_hint_y = 1, height = dp(1)))
    
    def screen2(self):
    
        screen2 = Screen(name = "2"); self.main.add_widget(screen2)
        screen2_scrollview = ScrollView();screen2.add_widget(screen2_scrollview)
        screen2_parent = GridLayout(height = dp(250),cols = 1, size_hint_y = None); screen2_scrollview.add_widget(screen2_parent)
        title_text = "[size=30sp][color=#000000]Unidad[/color][/size]\n"+C4+"contenido"
        title = Button(font_name = font + "Roboto-Regular.ttf",valign = "top",text_size = (Window.width-50, dp(80)),markup = True,background_normal = asset + 'Repeat Grid 8.png',font_size = '20sp',size_hint_y = None, height = '100dp', text = title_text)
        
        
        a = RelativeLayout(size_hint_y = None , height = '105dp'); screen2_parent.add_widget(a) 
        #screen2_parent.add_widget(Button(font_size = '17sp',valign = "middle",font_name = font+"Roboto-Light.ttf",text_size = (dp(Window.width-50)-dp(65),dp(125)),line_height = 1.5,markup = True, text = (C4+"[size=21sp][font="+font+"Roboto-Medium]Logica de Programacion[/font][/size]\nLorenzo"),size_hint_y = None , height = '150dp', background_normal = asset + "Repeat Grid 12.png"))
        
        button_text = C4+"[size=21sp][font="+font+"Roboto-Medium]Agregar una Materia[/font][/size]\n@Profesor"
        buttonparent = RelativeLayout(size_hint = (1,None), height = '150dp')
        button = Button(font_size = '17sp',valign = "middle",font_name = font+"Roboto-Light.ttf",text_size = (dp(Window.width-50)-dp(65),dp(125)),line_height = 1.5,markup = True, text = button_text,size_hint_y = None , height = '150dp', background_normal = asset + "Repeat Grid 12.png") 
        button.bind(on_release = lambda x:self.next())
        buttonparent.add_widget(button)
        buttonchilds = GridLayout(rows = 1,pos_hint = {'center_x':.7, 'center_y': .2},size_hint = (None,None), size = ('100dp','50dp'))
        
        dimbutton = RelativeLayout()

        
        button1 = Button(background_normal = asset + "Group 58.png");dimbutton.add_widget(button1)
        self.button2 = Button(background_down = asset + "Group 59.png",opacity = 0.,background_normal = asset + "Group 59.png");dimbutton.add_widget(self.button2)
        self.button2.bind(on_release = lambda x: self.favorito(x))
        buttonchilds.add_widget(dimbutton)
        
        este0 = Button(background_normal = asset + "Group 56.png")
        este0.bind(on_release = lambda x: alerta0.open())
        buttonchilds.add_widget(este0)
        #este = Button(background_normal = asset + "Group 57.png")
        #este.bind(on_release = lambda x:self.positate(x))
        #buttonchilds.add_widget(este)
        buttonparent.add_widget(buttonchilds)
        
        screen2_parent.add_widget(buttonparent)
        #screen2_parent.add_widget(title)
        
        for i in range(4):
            button_text = C4+"Unidad "+str(i)+"\n[size=18sp][font="+font+"Roboto-medium.ttf]Experiencias Geniales"; screen2_parent.height += dp(125)
            button = Button(font_name = font+"Roboto-Light.ttf",valign = 'middle',text_size = (Window.width-50, dp(125)),font_size = '25sp',markup = True,background_normal = color + '16.png',background_down = color + '16.png',text = button_text,size_hint_y = None, height = '125sp')
            button.bind(on_release = lambda x: self.next())
            screen2_parent.add_widget(button)
            screen2_parent.add_widget(Image(source = color + "16b.png", size_hint_y = None, height = 1 , keep_ratio = False, allow_stretch = True))
        
    def screen3(self):
        screen3 = Screen(name = "3"); self.main.add_widget(screen3)
        screen3.add_widget(Image(source = color + "16.png", keep_ratio = False, allow_stretch = True))
        self.screen3_scrollview = ScrollView(); screen3.add_widget(self.screen3_scrollview)
        self.pariente = RelativeLayout(size_hint_y = None , height = dp(0),size_hint_x = None , width = dp(500))
        self.screen3_parent = GridLayout(pos_hint = {'center_x': .5, 'center_y':.5},cols = 1,size_hint_x = None , width = dp(500), size_hint_y = 1 , height = dp(300))
        self.pariente.add_widget(self.screen3_parent)
        self.screen3_scrollview.add_widget(self.pariente)
        a = RelativeLayout(size_hint_y = None , height = '90dp'); self.screen3_parent.add_widget(a) 
        #self.screen3_parent.add_widget(Button(font_name = font+"Roboto-Light.ttf",valign = 'middle',text_size = (dp(450), dp(125)),font_size = '25sp',markup = True,background_normal = color + '16.png',text = button_text,size_hint_y = None, height = '125sp'))
    
        self.screen3_parent.add_widget(Image(source = color + "16bb.png",keep_ratio = False, allow_stretch = True , size_hint_y = None, height = 1))
        
        

            
    def abrirdoc(self,i_doc):
        self.screen3_parent.clear_widgets()
        self.screen3_parent.width = dp(100)
        self.screen3_parent.add_widget(Label(size_hint_y = None , height = dp(100)))
   
       
        

        f_unidades = []
        with open(unidades + i_doc) as f:
            
            for line in f:
                try:
                    exec("f_unidades.append("+line+")")
                except:
                    pass
        #for i in f_unidades: print i
        
     
        for i in f_unidades:
            if i[0] == "p":widget = Label(height = dp(len(i[1]))*0.60  ,size_hint_y = None,halign ='left',valign = 'top',text_size = (dp(450),dp(len(i[1]))*0.60),font_size = '16sp',markup = True,text = C4+i[1] , background_normal = color + "16.png")
            elif i[0] == "i":widget = Image(allow_stretch = True, keep_ratio = True,size_hint = (1,None), height = dp(300), source =unidades_imagenes+ i[1] + '.png')  
            elif i[0] == "t":widget = Label(height = dp(60),size_hint_y = None,font_name = font + "Roboto-medium.ttf",valign = 'bottom',text_size = (dp(450),dp(60)),font_size = '20sp',markup = True,text = "[color=#0066ff]"+str(i[1]) , background_normal = color + "16.png")
            self.screen3_parent.add_widget(widget)
            
            if i[0] == "p":self.pariente.height += dp(len(i[1]))*0.60
            elif i[0] == "i": self.pariente.height += dp(500)
            elif i[0] == "t": self.pariente.height += dp(60)
            
    def screen4(self):
        BC2 = '[color=#F45D5D]'
        screen4 = Screen(name = "4"); self.main.add_widget(screen4)
        
        
        screen4_parent_back = RelativeLayout();
        screen4_parent_back.add_widget(Image(source = color + "10.png", keep_ratio = False, allow_stretch = True))
        
        screen4_parent = GridLayout(cols = 1,size_hint_y = 1)
        screen4_parent_back.add_widget(screen4_parent)
        screen4.add_widget(screen4_parent_back)
        #screen4.add_widget(Button(opacity = .91,background_normal = asset + 'ic_add.png',background_down = asset + 'ic_add.png',pos_hint = {'center_x':.8, 'center_y':.1},size_hint = (None,None), size = (dp(81),dp(89))))
        screen4_parent.add_widget(Label(size_hint_y = None , height = '125dp'))
        #screen4_parent.add_widget(Label(opacity = .74,font_size = '20sp',text = C4 + "Octubre, 2017", markup = True, size_hint_y = None, height = dp(35)))
        dim = GridLayout(rows = 1, size_hint_y = None, height = dp(30))
        i_text = ["Lun","Mar","Mié","Jue","Vie","Sab","Dom"]
        dim.add_widget(Label())
        for i in i_text:  
            if i == "Jue":
                dim.add_widget(Label(opacity = 1,text = i , markup = True, size_hint = (None,None),height = dp(25) ,width = dp(50)))
            else:
                dim.add_widget(Label(opacity = .54,text = i , markup = True, size_hint = (None,None),height = dp(25) ,width = dp(50)))
        dim.add_widget(Label())
        
        dim2 = GridLayout(rows = 1, size_hint_y = None, height = dp(60))
        dim2.add_widget(Label(opacity = 1,size_hint_x = None ,valign = 'bottom',halign = 'right',font_name = font + 'Roboto-Regular.ttf',font_size = '48sp',text_size = (dp(150),dp(50)), width = '100dp', markup = True, text = "Hoy"))
        dim2.add_widget(Label())
        dim2.add_widget(Label(opacity = 1,size_hint_x = None ,halign = 'center',font_name = font + 'Roboto-Medium.ttf',font_size = '20sp', width = '100dp', markup = True, text = "06\n10-2017"))
        screen4_parent.add_widget(dim2)
        screen4_parent.add_widget(dim)
        screen4_parent.add_widget(Image(keep_ratio = False, allow_stretch= True,source = asset + "Repeat Grid 19.png", size_hint_y = None, height = dp(27), width = dp(360)))
        self.screen4_parent2 = GridLayout(cols = 1,spacing = 0, size_hint_y = None, height = 1000)
        screen4_pariente3 = RelativeLayout()
        screen4_parent.add_widget(Image(size_hint_y = None ,keep_ratio= False, allow_stretch = True, height = 1 , source = color + '3.png', opacity = .24))
        screen4_pariente3.add_widget(Image(source = color + "16.png", keep_ratio = False , allow_stretch = True))
        screen4scrollparent = ScrollView()
        screen4scrollparent.add_widget(self.screen4_parent2)
        screen4_pariente3.add_widget(screen4scrollparent)
        
        screen4_parent.add_widget(screen4_pariente3)
        
        def objeto():
            BC2 = '[color=#F45D5D]'
            pariente_parent = RelativeLayout(size_hint_y = None, height = '60dp')
            pariente = GridLayout(padding = [30,5,0,5],cols = 2)
            pariente.add_widget(Label(opacity = .74,halign = 'left',font_size = '16sp',text_size = (dp(200), 25),font_name = font + 'Roboto-Regular.ttf',text = C4+"Tutoria de Calculo Lineal", markup = True, size_hint_y = 1, height = dp(25)))
            pariente.add_widget(Label(text = C4 + "", markup = True, size_hint_y = 1, height = dp(25)))
            pariente.add_widget(Label(opacity = .54,halign = 'left',text_size = (dp(200), 25),font_size = '14sp',text = C4 + "Mar. 03 Feb. 2015 - 10:30", markup = True, size_hint_y = 1, height = dp(25)))
            pariente.add_widget(Label(font_size = '14sp',valign = 'middle',text = C4+"2 horas", markup = True, size_hint_y = 1, height = dp(25)))
            pariente_parent.add_widget(Image(opacity = .94,source = color + '16.png', keep_ratio = False , allow_stretch = True))
            pariente_parent.add_widget(pariente)
            return pariente_parent
        
        
        self.screen4_parent2.add_widget(Label(size_hint_y = None, height = '10dp'))
        self.screen4_parent2.add_widget(GridButton())
        self.screen4_parent2.add_widget(Image(opacity = .10,source = color + '3.png', size_hint_y = None , height = 1, keep_ratio = False, allow_stretch = True))
        self.screen4_parent2.add_widget(GridButton())
        self.screen4_parent2.add_widget(Image(opacity = .10,source = color + '3.png', size_hint_y = None , height = 1, keep_ratio = False, allow_stretch = True))
        self.screen4_parent2.add_widget(GridButton())
        self.screen4_parent2.add_widget(Image(opacity = .10,source = color + '3.png', size_hint_y = None , height = 1, keep_ratio = False, allow_stretch = True))
        self.screen4_parent2.add_widget(GridButton())
        self.screen4_parent2.add_widget(Image(opacity = .10,source = color + '3.png', size_hint_y = None , height = 1, keep_ratio = False, allow_stretch = True))
        self.screen4_parent2.add_widget(Button(size_hint_y = None ,markup = True, height = dp(50),background_normal = color + "16.png", text = C4 + "Agregar"))
        

            
    def screen5(self):
        screen5 = Screen(name = '5'); self.main.add_widget(screen5)
        screen5_background = Image(source = asset + "None.png",keep_ratio=  False, allow_stretch = True, size_hint = (1,None), size = (dp(360),dp(940)) ,y = dp(-940) + Window.height, pos_hint = {'center_x':.5})
        screen5_background2 = Image(opacity = .94,source = asset + "Rectangle 8.png",background_down = asset + "Rectangle 8.png", size_hint = (.95,.95), pos_hint = {'center_x':.5, 'center_y' : .5})
        screen5.add_widget(screen5_background)
        #screen5.add_widget(screen5_background2)
        
        screen5_layout = GridLayout(cols = 1, padding = [20,0,20,0]);screen5.add_widget(screen5_layout)
        screen5_layout.add_widget(Label())
        screen5_layout.add_widget(Label(size_hint_y = None, height = '50dp',markup = True,text = C4+"Codi",font_name = font+'segoescb.ttf', font_size = '40sp', opacity = .64))
        
        screen5_layout.add_widget(Label(size_hint_y = None , height = '25dp'))
        
        dim1 = RelativeLayout(size_hint_y = None, height = '50dp')
        dim2 = RelativeLayout(size_hint_y = None, height = '50dp')
        
        dim1.add_widget(Button(opacity = .54,pos_hint = {'center_x':.5},background_normal = asset + 'Group 94.png', size = ('268dp','50dp'), size_hint = (None,None) , background_down = asset + 'Group 94.png'))
        self.logusu = TextInput(cursor_color = [0,0,0,.54],cursor_width = '2sp',pos_hint = {'center_x':.5},padding = [30,19,0,0],multiline = False,hint_text_color = [0,0,0,.54],hint_text = "Usuario",size_hint = (None,None) ,width = '267dp', height = '50dp', background_normal = color + 'None.png', background_active = color + 'None.png')
        dim1.add_widget(self.logusu)
        
        dim2.add_widget(Button(opacity = .54,pos_hint = {'center_x':.5},background_normal = asset + 'Group 94.png', size = ('268dp','50dp'), size_hint = (None,None) , background_down = asset + 'Group 94.png'))
        self.logpw = TextInput(cursor_color = [0,0,0,.54],cursor_width = '2sp',password = True,pos_hint = {'center_x':.5},multiline = False,padding = [30,19,0,0],hint_text_color = [0,0,0,.54],hint_text = "Contraseña",size_hint = (None,None) ,width = '267dp', height = '50dp', background_normal = color + 'None.png', background_active = color + 'None.png')
        dim2.add_widget(self.logpw)
        dim2.add_widget(Button(password = True,pos_hint = {'center_x':.8},hint_text_color = [0,0,0,.54],hint_text = "Contraseña",size_hint = (None,None) ,width = '50dp', height = '50dp', background_normal = asset + 'Group 93.png', background_down = asset + 'Group 93.png'))

        
        
        screen5_layout.add_widget(dim1)
        screen5_layout.add_widget(Label(size_hint_y = None , height = '20dp'))
        screen5_layout.add_widget(dim2)
        
        
        
        dim3 = RelativeLayout(opacity = .54,size_hint_y = None, height = '50dp')
        dim3.add_widget(Button(on_release = lambda x: self.log_in(),border = [20,20,20,20],markup = True,font_name = font + 'Roboto-Medium.ttf',font_size = '16sp', text = C4 + "Iniciar Session",pos_hint = {'center_x':.5, 'center_y':.5},size_hint_x = None, width = '219dp', background_normal = asset+'NuevoR.png', background_down = asset+'NuevoR.png'))
        dim4 = RelativeLayout(opacity = .54,size_hint_y = None, height = '50dp')
        dim4.add_widget(Button(on_release = lambda x: self.choose('7'),border = [20,20,20,20],markup = True,font_name = font + 'Roboto-Medium.ttf',font_size = '16sp', text = C4 + "Crear Cuenta",pos_hint = {'center_x':.5, 'center_y':.5},size_hint_x = None, width = '219dp', background_normal = asset+'NuevoR.png', background_down = asset+'NuevoR.png'))
        dim5 = GridLayout(rows = 1, size_hint_y = None, height = '50dp')
        dim5.add_widget(Label())
        dim5.add_widget(CheckBox(size_hint_x = None ,width = '50dp'))
        dim5.add_widget(Label(markup = True,opacity = .64,text = C4+'Recordar contraseña.',size_hint_x = None ,width = '150dp'))
        dim5.add_widget(Label())
        
        #screen5_layout.add_widget(dim5)
        screen5_layout.add_widget(Label(size_hint_y = None , height = '25dp'))
        
        
        screen5_layout.add_widget(dim3)
        screen5_layout.add_widget(Label(size_hint_y = None , height = '10dp'))
        screen5_layout.add_widget(dim4)
        screen5_layout.add_widget(Label(size_hint_y = None , height = '25dp'))
        screen5_layout.add_widget(Button(opacity = .64,size_hint_y = None, height = '35dp', text = C4+'Has olvidado tu contraseña?', markup = True, background_normal = color + 'None.png', background_down = color + 'None.png' ))
        screen5_layout.add_widget(Label())
        
        
        
    
    def screen6(self):
        screen6 = Screen(name = '6')
        self.main.add_widget(screen6)
        screen6_parent = GridLayout(cols = 1); screen6.add_widget(screen6_parent)
        screen6_parent.add_widget(Label(size_hint_y = None , heigh = '90dp'))
        screen6_parent.add_widget(self.papeleraitem())
        screen6_parent.add_widget(Image(opacity = .14,source = color + '3.png', keep_ratio = False, allow_stretch = True, size_hint_y = None, height = dp(1)))
        screen6_parent.add_widget(self.papeleraitem())
        screen6_parent.add_widget(Image(opacity = .14,source = color + '3.png', keep_ratio = False, allow_stretch = True, size_hint_y = None, height = dp(1)))
    def log_in(self):
        for i in self.data['usuarios']:
            if (i['user'] == self.logusu.text) and (i['pw'] == self.logpw.text):
               self.choose("1")

    def crear_usuario(self):
        usuario = {'user': self.usutxt.text,
                   'pw':self.pwtxt.text,
                   'cpw':self.pwtxt.text,
                   }
        self.data['usuarios'].append(usuario)
        self.choose("5")
    def screen7(self):
        screen7 = Screen(name = '7')
        self.main.add_widget(screen7)
        screen7_parent = GridLayout(cols = 1); 
        screen7_background = Image(source = color + '16.png')
        screen7.add_widget(screen7_background)
        screen7.add_widget(screen7_parent)
        dim = GridLayout(rows = 1, size_hint_y = None, height = 50)

        dim.add_widget(TextInput(hint_text = "Appellidos", size_hint_y = None, height = 50))
        dim.add_widget(TextInput(hint_text = "Appellidos", size_hint_y = None, height = 50))
        screen7_parent.add_widget(Label(size_hint_y = None , height = dp(100)))
        screen7_parent.add_widget(CustTextInput("Nombres","nombres"))
        self.usutxt = CustTextInput("Usuario","usuario")
        self.pwtxt = CustTextInput("Contraseña","***")
        screen7_parent.add_widget(self.usutxt)
        screen7_parent.add_widget(CustTextInput("E-Mail","@hotmail.com"))
        screen7_parent.add_widget(self.pwtxt)
        screen7_parent.add_widget(CustTextInput("Confirmar Contraseña","***"))
        screen7_parent.add_widget(Button(on_release = lambda x: self.crear_usuario(),text = 'crear cuenta', size_hint_y = None, height = 50))
        
        
        dim2 = RelativeLayout()
        dim2.add_widget(Image(source = color +'3.png', keep_ratio = False, allow_stretch = True))
        dim2_parent = GridLayout(cols = 1)
        dim2.add_widget(dim2_parent)
        dim2_parent.add_widget(Label())
        dim2_parent.add_widget(Label(text = C4+"ya tienes una cuenta?", markup = True))
        dim2_parent.add_widget(Button(text = C4+"Inicia Sesión", markup = True, size_hint_y = None, height = 50))
        dim2_parent.add_widget(Label())
        screen7_parent.add_widget(dim2)
        
            
        
        
    def searchitem(self):
        BC1 = '[color=#0090FF]'
        BC2 = '[color=#F45D5D]'
        pariente =  SearchItem()
        pariente.dbutton().bind(on_release = lambda x: self.agregarmateria())
        return pariente
        
    def papeleraitem(self):
        BC1 = '[color=#0090FF]'
        BC2 = '[color=#F45D5D]'
        pariente =  GridLayout(opacity = .54,padding = [10,0,0,0],rows = 1,size_hint_y = None , height = dp(50))
        pariente.add_widget(Label(halign = 'center',text_size = (dp(60),None),markup = True ,font_name = font + 'Roboto-Medium.ttf',font_size = '13sp', text = C4 + "INS203", size_hint_x = None, width = '60dp'))
        pariente.add_widget(Label(halign = 'center',text_size = (dp(200),None),markup = True ,font_name = font + 'Arial_Italic.ttf',font_size = '13sp', text = C4 + "Logica de Programacion", size_hint_x = None, width = '180dp'))
        pariente.add_widget(Label(halign = 'center',text_size = (dp(65),None),markup = True ,font_name = font + 'Roboto-Medium.ttf',font_size = '13sp', text = C4 + "@Lorenzo", size_hint_x = None, width = '50dp'))
        pariente.add_widget(Button(on_release = lambda x: self.agregarmateria(),background_normal = asset + 'Group 132.png',background_down = asset + 'Group 132.png', size_hint_x = None, width = '50dp'))
        return pariente
    

class MyApp(App):
    def build(self):
        return InterfaceManager()
 

if __name__ in ('__main__', '__android__'):
    MyApp().run()

    
    
    
    
    