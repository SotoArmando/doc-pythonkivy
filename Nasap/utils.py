from kivy.uix.stencilview import StencilView
from kivy.properties import (ObjectProperty, NumericProperty, OptionProperty, BooleanProperty, StringProperty)
from kivy.lang import Builder

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
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.checkbox import CheckBox
from kivy.uix.scatterlayout import ScatterLayout as Scatter
from kivy.uix.textinput import TextInput
from kivy.graphics import Color, Line, Rectangle
from kivy.uix.behaviors import ButtonBehavior
from kivy.animation import Animation
from kivy.uix.widget import Widget
from kivy.metrics import dp
from kivy.uix.togglebutton import ToggleButton
from kivy.clock import Clock
from kivy.resources import resource_add_path
import os
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
C7 = "[color=#b3b3b3]"
EC = "[/color]"


class ImageButton(ButtonBehavior,Image):pass
class MateriaTitle(RelativeLayout):
    def __init__(self, **kwargs):
        super(MateriaTitle, self).__init__(**kwargs)
        self.add_widget(Image(keep_ratio = False, allow_stretch = True , source = color + "16.png"))
        self.size_hint_y = None
        self.height = dp(69)
        self.add_widget(Image(source = color + "16.png", keep_ratio = False, allow_stretch = True))
        
        anim_p = GridLayout(cols = 1)
        self.pariente = GridLayout(rows = 1)
        self.ImgB1 = ImageButton(on_release = lambda x: self.anim_parent(x.parent.parent),source = asset + "ic_expand_more_black_24px.png")
        self.ImgB2 = ImageButton(on_release = lambda x: self.anim_parent(x.parent.parent),opacity = .54,source = asset + "ic_delete_black_24px.png" )
        self.Imgp1 = Scatter()
        self.Imgp1_parent = GridLayout(cols =1,size_hint_x = None , width = dp(50))
        self.Imgp2 = Scatter()
        self.Imgp2_parent = GridLayout(cols =1,size_hint_x = None , width = dp(55))
        
        self.Imgp1_parent.add_widget(self.Imgp1)
        self.Imgp1.add_widget(self.ImgB1)
        self.Imgp2_parent.add_widget(self.Imgp2)
        self.Imgp2.add_widget(self.ImgB2)
        
        self.pariente.add_widget(self.Imgp1_parent)
        self.pariente.add_widget(Label(opacity = .84,haligh = 'left', text_size = (dp(250), dp(69)),markup = True,font_name = font + "Roboto-Medium.ttf",font_size = '14sp', text = C4+"Logica de Programacion\n[size=12sp]Lorenzo[/size]\n"+EC+C7+"L MX V 2:00 PM - 4:00 PM"))
        self.pariente.add_widget(self.Imgp2_parent)
        
        
        anim_p.add_widget(self.pariente)
        anim_p.add_widget(Image(source = "2.png", keep_ratio = False, allow_stretch = True, size_hint_y = None , height = dp(1), opacity = .24))
        
        self.add_widget(anim_p)

    def leftbutton(self): return self.ImgB1
    def righbutton(self): return self.ImgB2
    def anim_parent(self,x):
        dur = .225
        parent_anim = Animation(scale = .75, d = dur/2, t = "in_circ")
        parent_anim1 = Animation(scale = 1., d = dur/2, t = "out_circ")
        parent_anim.bind(on_complete = lambda t,p: parent_anim1.start(x))
        parent_anim.start(x)
            
class GridButton(RelativeLayout):
    def __init__(self, **kwargs):
        super(GridButton, self).__init__(**kwargs)
        self.size_hint_y = None
        self.height = dp(68)
        anim_parent = GridLayout(rows = 1)
        self.pariente = GridLayout(rows = 1,padding = [16,30,16,16])
        pariente_dim = GridLayout(cols = 1, size_hint_y = 1 )
        pariente_dim_sublabel = GridLayout(rows = 1,size_hint_y = None , height = dp(24))
        self.eliminar_pop = GridLayout(opacity = .0,rows = 1, size_hint_x = None, width = 0)
        
        self.pariente.add_widget(pariente_dim)
        self.pariente.add_widget(ImageButton(on_release = lambda x: self.eliminar(),source = asset + "ic_expand_close.png",size_hint_x = None, width = dp(24)))
        
        pariente_dim.add_widget(Label(halign = 'left',valign = 'top',text_size = (Window.width - dp(24+32),dp(42)),font_size = '16sp',markup = True ,text = C4 +  "Presentacion de Google"))
        pariente_dim.add_widget(pariente_dim_sublabel)
        self.Img = Image(source = asset + "ic_schedule_black_24px.png",size_hint_x = None, width = dp(24))
        pariente_dim_sublabel.add_widget(self.Img)
        pariente_dim_sublabel.add_widget(Label(halign = 'left',valign = 'middle',text_size = (Window.width - dp(24+44+24),dp(50)),font_size = '16sp',markup = True ,text = C4 +  "3 Mayo, 2:00 PM - 4:00 PM"))
        
        
        
        
        self.add_widget(Image(keep_ratio = False, allow_stretch = True, source = color + "16.png"))
        self.add_widget(anim_parent)
        anim_parent.add_widget(self.pariente)
        anim_parent.add_widget(self.eliminar_pop)
        
        
        
        self.eliminar_pop.add_widget(Button(on_release = lambda x: self.eliminar(),markup = True ,text = C4 +  "CANCEL", background_normal = color + "16.png", background_down = color + "16.png"))
        self.eliminar_pop.add_widget(Button(on_release = lambda x: self.eliminar(),markup = True ,text = C4 +  "OK", background_normal = color + "16.png", background_down = color + "16.png"))
        
        
    def eliminar(self):
        if self.eliminar_pop.width == Window.width:
            eliminar_anim = Animation(width = 0, d = .5, t = 'in_out_quart')
            eliminar_anim1 = Animation(opacity = 0, d = .5, t = 'in_out_quart')
            eliminar_anim2 = Animation(opacity = 1, d = .5, t = 'in_out_quart')
            eliminar_anim.start(self.eliminar_pop)
            eliminar_anim1.start(self.eliminar_pop)
            eliminar_anim2.start(self.pariente)
        elif self.eliminar_pop.width == 0:
            eliminar_anim = Animation(width = Window.width, d = .5, t = 'in_out_quart')
            eliminar_anim1 = Animation(opacity = 1, d = .5, t = 'in_out_quart')
            eliminar_anim2 = Animation(opacity = 0, d = .5, t = 'in_out_quart')
            eliminar_anim.start(self.eliminar_pop)
            eliminar_anim1.start(self.eliminar_pop)
            eliminar_anim2.start(self.pariente)
class TwoLineItem(RelativeLayout):
    def __init__(self,i_text,sub_text, **kwargs):
        super(TwoLineItem, self).__init__(**kwargs)
        self.doc = ""
        self.add_widget(Image(keep_ratio = False, allow_stretch = True , source = color + "16.png"))
        self.size_hint_y = None
        self.height = dp(70)
        anim_parent = GridLayout(cols = 1)
        pariente_p = RelativeLayout(size_hint_y = None, height = dp(68))
        pariente = GridLayout(rows = 1, padding = [16,8,16,0], spacing = [8,])
        pariente.add_widget(Image(source = asset + "Group 571.png", keep_ratio = False, allow_stretch = True, size_hint = (None,1), size = (dp(64),dp(64))))
        dim = GridLayout(cols = 1)
        dim.add_widget(Label(halign = 'left', valign = 'bottom',text_size = (dp(200),dp(40)),markup = True,text = C4+i_text,font_size = '16sp'))
        dim.add_widget(Label(opacity =.74,halign = 'left', valign = 'middle',text_size = (dp(200),dp(20)),markup = True,text = C4+sub_text,font_size = '14sp'))
        pariente.add_widget(dim)
        pariente.add_widget(ImageButton(on_release = lambda x: self.openme(),opacity = .54,source = asset + "ic_info_black_24px.png", keep_ratio = True, allow_stretch = False, size_hint = (None,1), size = (dp(24),dp(64))))
        
        button_anim = RelativeLayout()
        self.new_asset_parent = RelativeLayout()
        self.new_asset = Scatter(opacity = 0)
        self.new_asset_parent.add_widget(self.new_asset)
        self.img = Image(source = asset + "Group 571.png")
        self.new_asset.add_widget(self.img)
        button_anim.add_widget(self.new_asset_parent)
        self.btn = Button(size_hint_y = None, height = dp(72), y = -4,background_normal = color + "10.png",on_release = lambda x: self.animbutton(),opacity = .0)
        button_anim.add_widget(self.btn)
        pariente_p.add_widget(button_anim)
        
        
        
        
        pariente_p.add_widget(pariente)
        anim_parent.add_widget(pariente_p)
        self.add_widget(anim_parent)
        
        self.secondbutton = GridLayout(opacity = 0.,height = 0,rows = 1, size_hint_y = 1, padding = [0,0,0,0])
        self.secondbutton.add_widget(Label())
        self.secondbutton.add_widget(ImageButton(size_hint_x= None ,allow_stretch = True, width = dp(100), source = asset + "Group 572.png"))
        anim_parent.add_widget(self.secondbutton)
    def returndoc(self): return self.doc
    def returngo(self): return self.btn
    def animbutton(self):
        d = .225
        animbutton_anim = Animation(d = d,opacity =.24, t = 'out_circ', scale = 5.)
        animbutton_anim1 = Animation(d = d,opacity =.0, scale = 1., t = 'in_circ')
        animbutton_anim.bind(on_complete = lambda x,y: animbutton_anim1.start(self.new_asset))
        #animbutton_anim.start(self.new_asset)
        animbutton_anim2 = Animation(d = d,opacity =.34, t = 'out_circ')
        animbutton_anim3 = Animation(d = d,opacity =.0, t = 'in_circ')
        animbutton_anim4 = animbutton_anim2 + animbutton_anim3
        animbutton_anim4.start(self.btn)

        
    def openme(self):
        if self.height == dp(70):
            openme_anim = Animation(height = dp(110), d = .3 ,t = "out_circ")
            openme_anim1 = Animation(opacity = 1., d = .3 ,t = "out_circ")
            openme_anim.start(self)
            openme_anim1.start(self.secondbutton)
        if self.height == dp(110):
            openme_anim = Animation(height = dp(70), d = .3 ,t = "out_circ")
            openme_anim1 = Animation(opacity = 0., d = .3 ,t = "out_circ")
            openme_anim.start(self)
            openme_anim1.start(self.secondbutton)            
class SearchItem(RelativeLayout):
    def __init__(self, **kwargs):
        super(SearchItem, self).__init__(**kwargs)
        self.size_hint_y = None
        self.height = dp(64)
        self.add_widget(Image(source = color + "16.png", keep_ratio = False, allow_stretch = True))
        self.pariente = GridLayout(rows = 1, padding = [8,0,16,0])
        self.pariente2 = GridLayout(rows = 1, padding = [8,0,16,0],size_hint_y = None, height = 0 , opacity = 0.)
        anim_pariente = GridLayout(cols = 1)
        
        
        self.pariente.add_widget(Button(size_hint_y = 1 , height = dp(64),opacity = 1,size_hint_x = None ,background_normal = asset + "Ellipse 2.png", width = dp(64),font_name = font + "Roboto-Medium.ttf",markup = True ,font_size = '13sp',text = "INS\n203"))
        self.pariente.add_widget(Label(size_hint_x = None , width = dp(8)))
        self.pariente.add_widget(Label(opacity = .91,font_name = font + "Roboto-Medium.ttf",markup = True ,text = C4 + "Introduccion a la Programacion\n[size=12sp]Hirujo"))
        Imgbutton_parent_parent = RelativeLayout(size_hint_x = None , width = 48)
        Imgbutton_parent = Scatter()
        Imgbutton = ImageButton(on_release = lambda x: self.anim_parent(x.parent.parent),on_press = lambda x: self.anim_parent1(), markup = True ,text = C4 + "+", source = asset + "ic_code_black_24px.png")
        
        
        Imgbutton_parent.add_widget(Imgbutton)
        Imgbutton_parent_parent.add_widget(Imgbutton_parent)
        self.pariente.add_widget(Imgbutton_parent_parent)
        anim_pariente.add_widget(self.pariente)
        anim_pariente.add_widget(self.pariente2)
        
        text = ["L","M","MX","J","V","S"]
        for i in text:
            self.pariente2.add_widget(ToggleButton(background_normal = color + "16.png",background_down = color + "16b.png",markup = True,text = C4+i))
        self.button0 = ImageButton(on_press = lambda x: self.anim_parent1(),source = asset + "ic_done_black_24px.png",markup = True,text = C4+"Ok")
        self.pariente2.add_widget(self.button0 )
        
        self.add_widget(anim_pariente)
    
    def dbutton(self): return self.button0    
    def anim_parent(self,x):
        parent_anim = Animation(scale = .5, d = .25, t = "in_circ")
        parent_anim1 = Animation(scale = 1., d = .25, t = "out_circ")
        parent_anim.bind(on_complete = lambda t,p: parent_anim1.start(x))
        parent_anim.start(x)
        
    def anim_parent1(self):
        if self.pariente2.height == dp(64):
            parent_anim = Animation(height = dp(0),d = .25 , t = "out_circ")
            parent_anim1 = Animation(opacity = 0.,d = .25 , t = "out_circ")
            parent_anim2 = Animation(opacity = 1.,d = .25 , t = "out_circ")
            parent_anim.start(self.pariente2)
            parent_anim1.start(self.pariente2)
            parent_anim2.start(self.pariente)
        elif self.pariente2.height == dp(0):
            parent_anim = Animation(height = dp(64),d = .25 , t = "out_circ")
            parent_anim1 = Animation(opacity = 1.,d = .25 , t = "out_circ")
            parent_anim2 = Animation(opacity = 0.,d = .25 , t = "out_circ")
            parent_anim.start(self.pariente2)
            parent_anim1.start(self.pariente2)
            parent_anim2.start(self.pariente)
            
class TopNavigationS(RelativeLayout):
    def __init__(self, **kwargs):
        super(TopNavigationS, self).__init__(**kwargs)
        self.size_hint_y = None 
        self.height = dp(79)
        self.y = Window.height - self.height
        background = Image(opacity= 1.,source = color + "16.png", keep_ratio = False, allow_stretch = True)
        self.add_widget(background)
        self.add_widget(Image(y = dp(-27), size_hint_y = None, height = dp(27),opacity= 1.,source = asset + "Repeat Grid 19.png", keep_ratio = False, allow_stretch = True))
        parent = GridLayout(rows = 1)
        self.parent_child = GridLayout(rows = 1, padding = [dp(12),dp(6),dp(12),dp(10)])
        self.search_parent = RelativeLayout(size_hint_x = None, width = dp(55))
        self.search_parent_grid = GridLayout(rows = 1, padding = [0,dp(6),0,dp(10)]);self.search_parent.add_widget(self.search_parent_grid)
        
        self.Img = ImageButton(on_release = lambda x: self.bar_animate(),source = asset + "Group 569.png",size_hint = (None,None), size = ('55dp','55dp'))
        self.Img_parent = Scatter(do_translation_y=False, size_hint = (None,None), size = (dp(55),dp(55)))
        self.Img_parent_parent = RelativeLayout(size_hint = (None,1), width = dp(55))
        self.Img_parent.add_widget(self.Img)
        self.Img_parent_parent.add_widget(self.Img_parent)
        
        
        self.parent_child.add_widget(self.Img_parent_parent)
        self.parent_child.add_widget(Label(halign = 'left',valign = 'bottom',text_size = (Window.width - dp(110) - 50,dp(30)),markup = True,text = C4+"Page Title",font_name = font + "Roboto-Medium.ttf" ,font_size = '20sp'))
        self.Img1 = ImageButton(size_hint = (None,1), size = ('55dp','55dp'),source = asset + "Group 570.png", on_release = lambda x: self.search_animate())
        self.search_parent_grid.add_widget(self.Img1)
        self.TextInput0 =TextInput(hint_text_color = (0,0,0,.91),cursor_color = (0,0,0,.91),foreground_color = [0,0,0,.91],padding = [dp(5),dp(27),0,0],hint_text = "Busca piezas o departamento",font_size = '16sp',background_normal = color + "None.png",background_active = color + "None.png", multiline = False)
        self.search_parent_grid.add_widget(self.TextInput0)
        
        parent.add_widget(self.parent_child)
        parent.add_widget(self.search_parent)
        
        
        
        #self.add_widget(background)    
        self.add_widget(parent)
    def leftbutton(self): return self.Img
    def rightbutton(self): return self.Img1
    def textinput(self): return self.TextInput0
        
    def bar_animate(self):

        animate_d = .5
        if self.Img_parent.rotation == 360:
            animate_anim = Animation(rotation = 0, d = animate_d, t = 'in_out_quart')
            animate_anim1 = Animation(opacity = 1 , d = animate_d/2., t = 'in_out_quart')
            animate_anim2 = Animation(opacity = 1 , d = animate_d/2., t = 'in_out_quart')
            def ch(): 
                if self.Img.source == asset + "Group 568.png":
                    self.Img.source = asset + "Group 569.png"
                else:
                    self.Img.source = asset + "Group 568.png"
            animate_anim1.bind(on_complete= lambda x,y: ch())
            animate_anim2 = animate_anim1 + animate_anim2
            animate_anim.start(self.Img_parent)
            animate_anim2.start(self.Img_parent)
        elif self.Img_parent.rotation == 0:
            animate_anim = Animation(rotation = 360, d = animate_d, t = 'in_out_quart')
            animate_anim1 = Animation(opacity = 1 , d = animate_d/2., t = 'in_out_quart')
            animate_anim2 = Animation(opacity = 1 , d = animate_d/2., t = 'in_out_quart')
            def ch(): 
                if self.Img.source == asset + "Group 568.png":
                    self.Img.source = asset + "Group 569.png"
                else:
                    self.Img.source = asset + "Group 568.png"
            animate_anim1.bind(on_complete= lambda x,y: ch())
            animate_anim2 = animate_anim1 + animate_anim2
            animate_anim.start(self.Img_parent)
            animate_anim2.start(self.Img_parent)
        #animate_anim1.start(self.Img_parent)
    def search_animate(self):
        animate_d = .5
        if self.search_parent.width == dp(55):
            animate_anim = Animation(width = Window.width, d = animate_d, t = 'in_out_quart')
            animate_anim1 = Animation(opacity = 0., d = animate_d, t = 'in_out_quart')
            animate_anim2 = Animation(padding = [12,6,12,10], d = animate_d, t = 'in_out_quart')
            animate_anim1.start(self.parent_child)
            animate_anim.start(self.search_parent)
            animate_anim2.start(self.search_parent_grid)
        else:
            animate_anim = Animation(width = dp(55), d = animate_d, t = 'in_out_quart')
            animate_anim1 = Animation(opacity = 1., d = animate_d, t = 'in_out_quart')
            animate_anim2 = Animation(padding = [0,6,0,10], d = animate_d/2, t = 'in_out_quart')
            animate_anim.start(self.search_parent)
            animate_anim2.start(self.search_parent_grid)
            #animate_anim.bind(on_complete = lambda x,y:animate_anim1.start(self.parent_child))
            animate_anim1.start(self.parent_child)


class Datingscreen(RelativeLayout):
    def __init__(self, **kwargs):
        super(Datingscreen, self).__init__(**kwargs)
        self.size_hint_y = None
        self.height = dp(48)
        self.add_widget(Image(source = color+"16.png", keep_ratio = False, allow_stretch = True))
        self.pariente_grid = GridLayout(spacing = [64,0],rows = 1, size_hint_x = None, width = dp(0), padding = [32,0,16,0])
        pariente = RelativeLayout()
        
        pariente.add_widget(self.pariente_grid)
        pariente.add_widget(ImageButton(opacity = .54,on_release = lambda x: self.move_left(),source = asset + "ic_keyboard_arrow_right_black.png",x = Window.width - dp(64)+16,size_hint_x = None , width = dp(64)))
        pariente.add_widget(ImageButton(opacity = .54,on_release = lambda x: self.move_right(),source = asset + "ic_keyboard_arrow_left_black_.png",x = -16,size_hint_x = None , width = dp(64)))
        self.add_line("Logica de Programacion")
        self.add_line("Fundamentos de Programacion")
        self.add_line("Calculo Integral")
        self.add_line("Lengua Espanola")
 


        self.add_widget(pariente)
    def move_left(self):
        move_anim = Animation(x = self.pariente_grid.x - Window.width/2, d = .65 , t = 'out_circ' )
        move_anim.start(self.pariente_grid)
        
    def move_right(self):
        move_anim = Animation(x = 0, d = .65 , t = 'in_out_back' )
        move_anim.start(self.pariente_grid)
        
    
    def add_line(self,text):
        i_width = (dp(8.5) * len(text)) + dp(48)

        children = RelativeLayout(size_hint_x = None)
        children.add_widget(Image(pos_hint = {'center_y':.5},x = 1,size_hint = (None,1), size = (dp(40),dp(38)) , height = '38dp',source = asset + "Ellipse 3.png", keep_ratio = False, allow_stretch = True))
        children.add_widget(Image(pos_hint = {'center_y':.5},x = i_width-1,size_hint = (None,1) , size = (dp(40),dp(38)),source = asset + "Ellipse 3.png", keep_ratio = False, allow_stretch = True))
        children.add_widget(Image(pos_hint = {'center_y':.5},x = dp(20),size_hint_y = 1 , height = '38dp',source = asset + "Rectangle 68.png", keep_ratio = False, allow_stretch = True))
        img0 = ImageButton(on_release = lambda x: self.anim_parent(x.parent.parent),opacity = .84,source = asset + "ic_assignment_late_black_24px.png", keep_ratio = True, allow_stretch = False)
        img0parent = Scatter()
        img0_parent_parent = RelativeLayout(cols = 1,pos_hint = {'center_y':.5},x = dp(15),size_hint_x = None , width = '24dp',size_hint_y = None , height = '38dp')
        
        img1 = ImageButton(on_release = lambda x: self.anim_parent(x.parent.parent),opacity = .84,source = asset + "ic_delete_black_24px.png", keep_ratio = True, allow_stretch = False)       
        img1parent = Scatter()
        img1_parent_parent = RelativeLayout(cols = 1,pos_hint = {'center_y':.5},x = i_width+4,size_hint_x = None , width = '24dp',size_hint_y = None , height = '38dp')
        
        
        img0parent.add_widget(img0)
        img0_parent_parent.add_widget(img0parent)
        img1parent.add_widget(img1)
        img1_parent_parent.add_widget(img1parent)
        
        
        children.add_widget(img0_parent_parent)
        children.add_widget(img1_parent_parent)
        children.add_widget(Label(pos_hint = {'center_y':.5},x = dp(30),text_size = (i_width - dp(36),dp(24)),valign = 'middle',halign = "left",markup = True, opacity = .84,text = C4+text))
        children.width = i_width
        self.pariente_grid.add_widget(children)
        self.pariente_grid.width += i_width+dp(75)
        
    def anim_parent(self,x):
        print x
        dur = .225
        parent_anim = Animation(scale = .75, d = dur/2, t = "in_circ")
        parent_anim1 = Animation(scale = 1., d = dur/2, t = "out_circ")
        parent_anim.bind(on_complete = lambda t,p: parent_anim1.start(x))
        parent_anim.start(x)
        
class BottomNavigation(RelativeLayout):
    def __init__(self, **kwargs):
        super(BottomNavigation, self).__init__(**kwargs)
        
        self.size_hint_y = None
        self.height = '56dp'
        self.background = Image(source = color + "3.png", keep_ratio = False, allow_stretch = True)
        self.add_widget(self.background)
        self.colors_manager = ScreenManager()
        parent = GridLayout(rows = 1)
        self.colors_manager.transition = FadeTransition(duration = .25)
     
        #eTransition,FadeTransition,WipeTransition,FallOutTransition,NoTransition ,RiseInTransition 
  
        colors = ["3","3","3","3"]
        text =  ["Inicio", "Agenda", "Portafolio", "Asignaciones"]
        img =  ["ic_alarm_black_24px", "ic_bookmark_border_black_24px", "ic_class_black_24px", "ic_copyright_black_24px"]
        for i in range(4):
            color_screen = Screen(name = str(i))
            color_screen.add_widget(Image(source = color + colors[i] + ".png", keep_ratio = False, allow_stretch = True))
            self.colors_manager.add_widget(color_screen)
        self.caja = []

        button_parent = GridLayout(size_hint_x = None, width = '96dp',cols = 1, padding = [12,6,12,10])
        button_label = Label(size_hint_y = None, height = '14sp',font = font + "Roboto-Regular.ttf",font_size = '14sp',text = text[0], markup = True, halign = 'center', valign = 'bottom')
        
        button_parent.add_widget(Label())
        self.Img2 = ImageButton(on_release = lambda x: self.animate(x.parent.children[0]),size_hint = (1,None), size = (dp(24),dp(24)), source = asset + img[0] +".png", keep_ratio = False, allow_stretch = False)
        button_parent.add_widget(self.Img2)
        
        button_parent.add_widget(button_label)
        parent.add_widget(button_parent)
#--------------------------------------------------------
        button_parent1 = GridLayout(size_hint_x = None, width = '96dp',cols = 1, padding = [12,6,12,10])
        button_label1 = Label(opacity = 0.,size_hint_y = None,height= 0, font = font + "Roboto-Regular.ttf",font_size = '14sp',text = text[1], markup = True, halign = 'center', valign = 'bottom')
        
        button_parent1.add_widget(Label())
        self.Img3 = ImageButton(on_release = lambda x: self.animate(x.parent.children[0]),size_hint = (1,None), size = (dp(24),dp(24)), source = asset + img[1] +".png", keep_ratio = False, allow_stretch = False)
        button_parent1.add_widget(self.Img3)
        button_parent1.add_widget(button_label1)
        parent.add_widget(button_parent1)
#--------------------------------------------------------
        button_parent2 = GridLayout(size_hint_x = None, width = '96dp',cols = 1, padding = [12,6,12,10])
        button_label2 = Label(opacity = 0.,size_hint_y = None,height= 0, font = font + "Roboto-Regular.ttf",font_size = '14sp',text = text[2], markup = True, halign = 'center', valign = 'bottom')
        
        button_parent2.add_widget(Label())
        self.Img4 = ImageButton(on_release = lambda x: self.animate(x.parent.children[0]),size_hint = (1,None), size = (dp(24),dp(24)), source = asset + img[2] +".png", keep_ratio = False, allow_stretch = False)
        button_parent2.add_widget(self.Img4)
        button_parent2.add_widget(button_label2)
        parent.add_widget(button_parent2)
#--------------------------------------------------------
        button_parent3 = GridLayout(size_hint_x = None, width = '96dp',cols = 1, padding = [12,6,12,10])
        button_label3 = Label(opacity = 0.,size_hint_y = None,height= 0, font = font + "Roboto-Regular.ttf",font_size = '14sp',text = text[3], markup = True, halign = 'center', valign = 'bottom')
        
        button_parent3.add_widget(Label())
        self.Img5 = ImageButton(on_release = lambda x: self.animate(x.parent.children[0]),size_hint = (1,None), size = (dp(24),dp(24)), source = asset + img[3] +".png", keep_ratio = False, allow_stretch = False)
        button_parent3.add_widget(self.Img5)
        button_parent3.add_widget(button_label3)
        parent.add_widget(button_parent3)


        
        
        self.add_widget(self.colors_manager)
        self.add_widget(parent)
    def buttons(self): return [self.Img2,self.Img3,self.Img4,self.Img5]
    def animate(self,x):
        animate_anim = Animation(opacity = 1.,height = sp(14), d = .25, t = 'in_out_circ')
        animate_anim1 = Animation(width = dp(Window.width/4 + 36),d = .25, t = 'in_out_circ')
        animate_anim2 = Animation(opacity = .91,d = .25, t = 'in_out_circ')
        animate_anim.start(x)
        animate_anim1.start(x.parent)
        animate_anim2.start(x.parent.children[1])
        otros = x.parent.parent.children
        count = 0
        for i in otros:
            if (count == 9) or (count == 9) :
                pass
            else:
                if i == x.parent: pass
                else:
                    animate_anim = Animation(opacity = 0.,height = sp(0), d = .20, t = 'in_out_circ')
                    animate_anim1 = Animation(width = dp(Window.width/4 - 12),d = .25, t = 'in_out_circ')
                    animate_anim2 = Animation(opacity = .54,d = .25, t = 'in_out_circ')
                    animate_anim.start(i.children[0])
                    animate_anim2.start(i.children[1])
                    animate_anim1.start(i)
            count += 1
            
        self.colors_manager.current = self.colors_manager.next()

                
    
    def funcion(self):
        print("hola")
