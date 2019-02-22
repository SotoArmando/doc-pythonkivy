#!/usr/bin/env python
# -*- coding: utf-8 -*-

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



from utils import GridButton,TwoLineItem,SearchItem,MateriaTitle,TopNavigationS,Datingscreen,BottomNavigation

resource_add_path(os.path.dirname(__file__))

from kivy.uix.behaviors import ButtonBehavior
from kivy.animation import Animation
from kivy.uix.widget import Widget
from kivy.uix.stencilview import StencilView
from kivy.metrics import dp
from kivy.clock import Clock
from kivy.uix.dropdown import DropDown
from kivy.properties import (ObjectProperty, NumericProperty, OptionProperty,
                             BooleanProperty, StringProperty)
from kivy.resources import resource_add_path
from kivy.lang import Builder
import os.path
from utils import CustTextInput
from loading import Loading
Window.size = (360,640)
Window.clearcolor = (1,1,1,1)
#CARPETAS DEL PROYECTO
patch = os.path.dirname(os.path.abspath(__file__))
asset = patch + '/assets/drawable-mdpi/'
color = patch + '/colors/'
font = patch + '/fonts/'
C1 = "[color=#13C0C7]"
C4 = "[color=#000000]"
C2 = "[color=#404040]"
C3 = "[color=#ff3333]"
C5 = "[color=#f2f2f2]"
C6 = "[color=#95989A]"
EC = "[/color]"
kv = '''
<MyButton>:
    size_hint: None, 1
    size: self.texture_size
'''
Builder.load_string(kv)
class MyDropdown(DropDown):
    def __init__(self,**kwargs):
        super(MyDropdown, self).__init__(**kwargs)
        pass
    def dismiss(self, *largs):
        anim = Animation(d = .155, t = 'out_expo', opacity = 0)
        def hola(a,b):
            Clock.schedule_once(lambda dt: self._real_dismiss(),
                            self.min_state_time)
        anim.bind(on_complete = hola)
        anim.start(self)
        
        
    def open(self, widget):
        anim = Animation(d = .155, t = 'in_expo', opacity = 1)
        '''Open the dropdown list and attach it to a specific widget.
        Depending on the position of the widget within the window and
        the height of the dropdown, the dropdown might be above or below
        that widget.
        '''

        # ensure we are not already attached
        if self.attach_to is not None:
            self.dismiss()

        # we will attach ourself to the main window, so ensure the
        # widget we are looking for have a window
        self._win = widget.get_parent_window()
        if self._win is None:
            raise DropDownException(
                'Cannot open a dropdown list on a hidden widget')

        self.attach_to = widget
        widget.bind(pos=self._reposition, size=self._reposition)
        self._reposition()

        # attach ourself to the main window
        self._win.add_widget(self)     
        #anim.bind(on_complete = hola)
        anim.start(self)
class ImageButton(ButtonBehavior, Image): pass
class MyButton(Button):
    pass

class infopage(RelativeLayout):
    def __init__(self, **kwargs):
        super(infopage, self).__init__(**kwargs)
        parent_scroll = ScrollView()
        #self.add_widget(Image(source = color +'16b.png', keep_ratio = False, allow_stretch = True))
        self.enuso = -1
        parent = RelativeLayout(size_hint_y = None, height = dp(700))
        
        
        parent.add_widget(Image(y = dp(-7-(Window.height/2)),source = color + '16.png', keep_ratio = False , allow_stretch = True))
        parent.add_widget(Image(y = dp(700-7-(Window.height/2)),source = asset + 'shadup.png', keep_ratio = False, allow_stretch = True, size_hint_y = None, height = dp(7)))
        
        parent_w = GridLayout(cols = 1, padding = [dp(0),0,0,0])
        parent_w.add_widget(Button(on_release = lambda x: self.togglepos(),opacity = .01,size_hint_y = None, height = Window.height/2))
        dim = GridLayout(cols = 2)
       
       
        dim.add_widget(Label(opacity = .40,source = asset + 'ic_place_black_24px (1).png', keep_ratio = True, allow_stretch = False, size_hint = (None,None), size = (dp(100), dp(75))))
        dim.add_widget(Label(size_hint_y = None,text_size = (Window.width - dp(50), dp(75)),valign = 'bottom',halign = 'left', height = dp(75),text = C4 + 'Dandelion Chocolate', markup = True, font_size = '24sp'))
        
        dim.add_widget(Label(opacity = .40,source = asset + 'ic_place_black_24px (1).png', keep_ratio = True, allow_stretch = False, size_hint = (None,None), size = (dp(100), dp(50))))
        dim.add_widget(Label(size_hint_y = None,text_size = (Window.width - dp(50), dp(50)),valign = 'middle',halign = 'left', height = dp(50),text = C4 + 'Estrellas : 4.7', markup = True, font_size = '16sp'))
        
        dim.add_widget(Label(opacity = .40,source = asset + 'ic_place_black_24px (1).png', keep_ratio = True, allow_stretch = False, size_hint = (None,None), size = (dp(100), dp(1))))
        dim.add_widget(Image(source = color +'16b.png', keep_ratio = False, allow_stretch = True, size_hint_y = None , height = dp(1) ))
        
        
        dim.add_widget(Label(opacity = .40,source = asset + 'ic_place_black_24px (1).png', keep_ratio = True, allow_stretch = False, size_hint = (None,None), size = (dp(100), dp(50))))
        dim.add_widget(Label(size_hint_y = None,text_size = (Window.width - dp(50), dp(50)),valign = 'middle',halign = 'left', height = dp(50),text = C1 + '12 min de trajecto', markup = True, font_size = '16sp'))
        
        
        dim.add_widget(Label(opacity = .40,source = asset + 'ic_place_black_24px (1).png', keep_ratio = True, allow_stretch = False, size_hint = (None,None), size = (dp(100), dp(1))))
        dim.add_widget(Image(source = color +'16b.png', keep_ratio = False, allow_stretch = True, size_hint_y = None , height = dp(1) ))
        
        
        a =Label(size_hint_y = None,text_size = (Window.width - dp(50), dp(50)),valign = 'middle',halign = 'left', height = dp(50),text = C4 + 'Los Restauradores, Norberto Torres', markup = True, font_size = '16sp')
        b = Label(size_hint_y = None,text_size = (Window.width - dp(50), dp(50)),valign = 'middle',halign = 'left', height = dp(50),text = C4 + '849 - 353 - 2487', markup = True, font_size = '16sp')
        c = Label(size_hint_y = None,text_size = (Window.width - dp(50), dp(50)),valign = 'middle',halign = 'left', height = dp(50),text = C4 + '05/08/2017 - 15:05 PM', markup = True, font_size = '16sp')
        
        
        dim.add_widget(Image(opacity = .40,source = asset + 'ic_place_black_24px (1).png', keep_ratio = True, allow_stretch = False, size_hint = (None,None), size = (dp(75), dp(50))))
        dim.add_widget(a)
        dim.add_widget(Image(opacity = .40,source = asset + 'ic_call_black_24px.png', keep_ratio = True, allow_stretch = False, size_hint = (None,None), size = (dp(75), dp(50))))
        dim.add_widget(b)
        dim.add_widget(Image(opacity = .40,source = asset + 'ic_access_time_black_24px.png', keep_ratio = True, allow_stretch = False, size_hint = (None,None), size = (dp(75), dp(50))))
        dim.add_widget(c)
        parent_w.add_widget(dim)
            
        #parent.add_widget(Image(opacity = .40,source = asset + 'ic_place_black_24px (1).png', keep_ratio = True, allow_stretch = False, size_hint = (None,None), size = (dp(100), dp(50))))
        #parent.add_widget(Image(opacity = .40,y = b_y,source = asset + 'ic_call_black_24px.png', keep_ratio = True, allow_stretch = False, size_hint = (None,None), size = (dp(75), dp(50))))
        #parent.add_widget(Image(opacity = .40,y = c_y,source = asset + 'ic_access_time_black_24px.png', keep_ratio = True, allow_stretch = False, size_hint = (None,None), size = (dp(75), dp(50))))
        parent.add_widget(parent_w)
        parent_scroll.add_widget(parent)
        self.add_widget(parent_scroll)
    def hello(self): print "hello"
    def togglepos(self):
    
        print "hola"
        if self.opacity == 1:
            animate = Animation(y = dp(-250), opacity = 0, d = .5 , t = 'out_expo')
            animate.start(self)
            try:
                if self.enuso == -1:
                    self.enuso *= -1
                    def c(): self.enuso *= -1
                    def remover():
                        try:
                            self.parent.remove_widget(self)
                        except:
                            print "Error al eliminar"
                    Clock.schedule_once(lambda x:remover(),.4)
                    Clock.schedule_once(lambda x:c(),.4)
            except:
                pass
        elif self.opacity == 0:
            animate = Animation(y = dp(0), opacity = 1, d = .5 , t = 'out_expo')
            animate.start(self)
    
class Searcher_item(RelativeLayout):
    def __init__(self, **kwargs):
        super(Searcher_item, self).__init__(**kwargs)
        self.position = kwargs["position"]
        self.size_hint_y = None
        self.height = dp(65)
        item = GridLayout(rows = 1)
        self.add_widget(item)
        item.add_widget(Image(opacity = 1,source = asset + "ic_place_black_24px (1).png",size_hint_x = None, width = dp(75)))
        item.add_widget(Label(opacity = .74,font_size = '14sp',shalign = 'left', valign = 'top',markup = True,text_size = (Window.width/2 - dp(25), dp(45)), text = C4 + kwargs["cuenta"] + "\n[b]" + kwargs["cliente"]+"[/b]"))
        item.add_widget(Label(opacity = .34,font_size = '13sp',shalign = 'right', valign = 'bottom',markup = True,text_size = (Window.width/2 - dp(50), dp(45)), text = C4 + "V:"+kwargs["fecha"]))
        self.heybutton = Button(on_release = lambda x: self.hey(),size_hint_x = None,pos_hint = {'center_x':.5}, width = Window.width - dp(18),background_normal = color + "None.png",background_down = color + "10.png", opacity = .54 )
        self.add_widget(self.heybutton)
    def hey(self):
        print self.position
    def returnbehavior(self): return self.heybutton
    
class Searcher_bottom(RelativeLayout):
    def __init__(self, **kwargs):
        super(Searcher_bottom, self).__init__(**kwargs)
        self.opened = -1
        self.size_hint_y = 1
        self.height = dp(56)
        pariente = GridLayout(rows = 1)
        pariente_root = RelativeLayout()
        self.image0 = Image(source = asset + "ic_directions_"+kwargs['stcolor']+"_24px.png", size_hint_x = None, width = dp(0))
        self.button0 = Button(valign = 'middle',text_size = (Window.width - dp(25), dp(56)),background_normal = color + "None.png", opacity = .54,markup = True, text = C4+kwargs['text'])
        pariente.add_widget(self.image0)
        pariente.add_widget(self.button0)
        self.add_widget(pariente_root)
        pariente_root.add_widget(Image(opacity = .90,source = color + '16.png', keep_ratio = False, allow_stretch = True))
        pariente_root.add_widget(pariente)
        self.button1 = Button(group = 'jholjhaoajsdoiqjwoqiwhdoqowidhqwoidhqwoidhqoiwdhqoiwdhqwoidhqwoidhqwiodhqwoi ncojqw cijwjjbbcweicbewkcjwebio i',background_normal = color + "None.png",background_down = color + "10.png",on_release = lambda x: self.animate(), opacity = .24)
        pariente_root.add_widget(self.button1)
        
    def returntoggle(self): return self.button1
    def returntext(self): return self.button0
    def animate(self):
        if self.image0.width == dp(0):
            anim0 = Animation(d = .225 , t = 'out_expo', text_size = (Window.width - dp(60), dp(112/2)))
            anim1 = Animation(d = .225 , t = 'out_expo', width = dp(60))
            anim0.start(self.button0)
            anim1.start(self.image0)
            self.opened *= -1
        elif self.image0.width == dp(60):
            anim0 = Animation(d = .225 , t = 'out_expo', text_size = (Window.width - dp(25), dp(112/2)))
            anim1 = Animation(d = .225 , t = 'out_expo', width = dp(0))
            anim0.start(self.button0)
            anim1.start(self.image0)
            self.opened *= -1
        
class Searcher(RelativeLayout): 
    def __init__(self, **kwargs):
        super(Searcher, self).__init__(**kwargs)
        self.items = []
        self.posicion0 = 'Vacio'
        self.posicion1 = 'Vacio'
        
        top_parent = RelativeLayout(size_hint_y = None, height = dp(75), pos_hint = {'center_y': .9})
        top_parent.add_widget(Button(background_normal = asset + "Searcher.png",background_down = asset + "Searcher.png", keep_ratio = True, allow_stretch = True))
        top_wids = GridLayout(rows = 1, padding = [dp(10),dp(12),dp(10),dp(12)])
        top_wids.add_widget(Image(opacity = .54,source = asset + "ic_search_black_24px.png", size_hint_x = None, width = dp(56)))
        self.busqueda = TextInput(multiline = False,hint_text = "Buscar Destino",font_size = sp(16.5),padding = [dp(0),dp(14),0,0],background_normal = color + "16.png",background_active = color + "16.png",opacity = 1)
        top_wids.add_widget(self.busqueda)
        top_wids.add_widget(ImageButton(opacity = .54,source = asset + "ic_close_black_24px.png", size_hint_x = None, width = dp(56)))
        dim = GridLayout(rows = 1, padding = [dp(0),dp(12),dp(0),dp(12)])
        self.thebutton = Button(opacity = 0,disabled = True, on_release = lambda x: self.dropdownlist.open(x))
        dim.add_widget(self.thebutton)
        self.loading = Loading(pos_hint = {'center_x':.75}, opacity = 0.)
        top_parent.add_widget(dim)
        top_parent.add_widget(top_wids)
        top_parent.add_widget(self.loading)
 
        self.add_widget(top_parent)
        self.getpos1 = ImageButton(opacity = 1,allow_stretch = True, keep_ratio = True,on_release = lambda x: self.animate(x) ,pos_hint = {'center_x':.5 }, y = dp(125),source = asset + "ic_adjust_black_24px.png", size_hint = (None,None))
        self.getpos2 = ImageButton(opacity = 1,allow_stretch = False, keep_ratio = True,on_release = lambda x: self.animate(x) ,pos_hint = {'center_x':.75, 'center_y':.5 }, y = dp(125),source = asset + "road-split.png", size_hint = (None,None))
        self.getpos1.size = self.getpos1.texture_size
        self.getpos2.size = self.getpos2.texture_size
        print self.getpos2.size
        #self.add_widget(self.getpos1)
        #self.add_widget(self.getpos2)
        
        self.dropdownlist = MyDropdown(spacing = 0)
        self.dropdownroot = RelativeLayout(size_hint_y = None, height = dp(13), opacity = 1)
        self.dropdownroot.add_widget(Button(background_normal = asset + "Searcherresult.png",background_down = asset + "Searcherresult.png"))
        self.gridlist = GridLayout(cols = 1)
        self.dropdownroot.add_widget(self.gridlist)
        
        def arreglar():
            self.busqueda.focus=True
        
        self.dropdownlist.add_widget(self.dropdownroot)
        self.busqueda.bind(on_text_validate = lambda x: self.open() )
        #self.busqueda.bind(on_text_validate = Clock.schedule_once(lambda x: arreglar(),0.5 ))
        self.verdadero = RelativeLayout(size_hint_y = None, height = dp(56*2))
        self.verdadero_dim = GridLayout(cols = 1)
        self.verdadero.add_widget(self.verdadero_dim)
        self.verdadero_dim.add_widget(Image(source = asset + "shadup.png", keep_ratio = False, allow_stretch = True, size_hint_y = None, height = dp(7)))
        dim1 = GridButton(rows = 1)
        dim2 = GridButton(rows = 1)
        
        hola = Searcher_bottom(stcolor = 'green',text = "[b]Desde[/b]:")
        hola1 = Searcher_bottom(stcolor = 'red',text = "[b]Hasta[/b]:")
        self.seleccionado = 0
        hola.returntoggle().bind(on_release = lambda x: self.advice(hola))
        hola.returntoggle().bind(on_release = lambda x: self.setseleccionado(0))

        hola1.returntoggle().bind(on_release = lambda x: self.advice(hola1))
        hola1.returntoggle().bind(on_release = lambda x: self.setseleccionado(1))

        self.objetos = [hola,hola1]
        self.verdadero_dim.add_widget(hola)
        self.verdadero_dim.add_widget(hola1)
        self.add_widget(self.verdadero)
        self.verdadero.add_widget(self.getpos2)
        self.infor = infopage(opacity = 0, y = dp(-250))
    def toggleinfor(self):
        if self.infor.opacity == 1:
            self.infor.togglepos()

        elif self.infor.opacity == 0:
            self.add_widget(self.infor)
            self.infor.togglepos()
    def setposicion(self, str):
        print str
        formato = ['[b]Desde:[/b] ','[b]Hasta:[/b] ']
        posiciones = [self.posicion0,self.posicion1]
        self.objetos[self.seleccionado].returntext().text = C4+formato[self.seleccionado] + str
        if self.seleccionado == 0: self.posicion0 = str
        if self.seleccionado == 1: self.posicion1 = str
    def setseleccionado(self,int):
        print 'hola'
        self.seleccionado = int
    def animate1(self):
        anim = Animation(opacity = .54, d = .225 , t ='out_expo')
        anim.start(self.loading)
    def animate2(self):
        anim = Animation(opacity = 0., d = .225 , t ='in_expo')
        anim.start(self.loading) 
    
            
    def open(self):
        self.thebutton.trigger_action(duration=0.01)
        anim = Animation(d = .225 , t = 'out_expo', opacity = 1.)
        #anim.start(self.dropdownroot)
    def dropdown_dismiss(self): 
        self.dropdownlist.dismiss()
        
    def advice(self,objecto):
        for i in self.objetos:
            if i == objecto:
                #Clock.schedule_once(despuest,0.255)
                pass
            else:
                if i.opened == 1:
                    i.animate()
        
    def behavior(self): return self.busqueda
    def animate(self,item):
        print "hola"
        anim = Animation(size = (dp(40),dp(40)), d =.165, t = 'in_quart') + Animation(size = item.texture_size, d =.165, t = 'out_quart') 
        anim1 = Animation(opacity = .44, d =.165, t = 'in_quart') + Animation(opacity = 1, d =.165, t = 'out_quart') 
        anim.start(item)
        anim1.start(item)
    def clean(self,x_pos):
        for i in self.items:
            i.parent.remove_widget(i)
        self.items[:] = []
        object = self.add_new(position = x_pos,cuenta = "Mi Posicion", fecha = "30/07/2017 23:17" , cliente = "[Usuario]")
        return object
    def add_new(self, **kwargs):
        new_item = Searcher_item(position = kwargs["position"],cuenta = kwargs["cuenta"], fecha = kwargs["fecha"], cliente = kwargs["cliente"])
        item1 = GridLayout(rows = 1,size_hint_y = None, height = dp(1), padding = [dp(10),dp(0),dp(10),dp(0)])
        self.gridlist.add_widget(item1)
        self.gridlist.add_widget(new_item)
        self.dropdownroot.height = dp(13)
        for i in self.gridlist.children: self.dropdownroot.height += i.height
        self.items.append(item1)
        self.items.append(new_item)
        new_item.returnbehavior().bind(on_release = lambda x:self.setposicion(str(new_item.position)))
        return new_item
class MyApp(App):
    def build(self):
        return infopage()
 

if __name__ in ('__main__', '__android__'):
    MyApp().run()

    
    
    
    
    