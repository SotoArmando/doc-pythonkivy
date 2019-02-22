import sys, os
from os.path import dirname, join, abspath
sys.path.insert(0, dirname(dirname(abspath(__file__))))
from mind import *

#CARPETAS DEL PROYECTO
patch = dirname(dirname(abspath(__file__)))
asset = patch + '/_assets/drawable-mdpi/'
font = patch + '/_fonts/'
sound = patch + '/_sounds/'
behavior = patch + '/_behavior/'

print (".: ASSETS DIR",asset)
print (".: FONTS DIR" ,font)
print (".: SOUND DIR" ,sound)
print (".: BEHAVIOR DIR" ,behavior)
class Label(Label):
    font_name = StringProperty(font + "Roboto-Regular.ttf")
class Relatstencil(RelativeLayout,StencilView): pass



class especialbutton(RelativeLayout):
    posx = NumericProperty(0)
    posy = NumericProperty(0)
    opa = NumericProperty(.35)
    size_hint_y = NumericProperty(None)
  
    height = NumericProperty(dp(36))
   
    
    def __init__(self,**kwargs):
        super().__init__()
        thelabel = Label(markup = True,text = "[b]Dale un Icono",)
        self.wid = Relatstencil(size = (125,self.height), size_hint = (None,None))


        Clock.schedule_interval(lambda x: self.animate(), 3.0)
        
        with self.wid.canvas.before:
            Color(1.0, 0.396078431372549, 0.6235294117647059, 1.0)
            RoundedRectangle(size = (125,self.height),segments = 4, pos = (0,0),group = "asd")
            Color(1,1,1,1)
            Mesh(vertices=[self.posx+0, self.posy+0, 0, 0,self.posx+75, self.posy+50, 0, 0,self.posx+125, self.posy+50, 0, 0,self.posx+50, self.posy+0, 0, 0], indices=[0,1,2,3], mode = 'triangle_fan',group = "asd")
       
        

    
        self.add_widget(self.wid)
        self.wid.add_widget(thelabel)
  
  

        self.thelabel = thelabel
    def animate(self,*args):
        Animation.stop_all(self, 'posx')
        Animation.stop_all(self, 'opa')
        Animation.stop_all(self.thelabel, 'opacity')
        
        
        x = (Animation(posx = 125, opa = .10, d = .75, t = 'in_expo' ) 
        + Animation(posx = 250, opa = .35, d = .75, t = 'out_expo' )
        + Animation(posx = -125, d = 0 ))
        
        
        y = (
        Animation(opacity = .5, d = .75, t = 'in_expo' ) 
        + Animation(opacity = 1, d = .75, t = 'out_expo' )) 
        y.start(self.thelabel)
        x.start(self)   
    def change_mode(self, mode, *largs):
        self.mesh.mode = mode

    def on_posx(self,*args):
        self.wid.canvas.before.remove_group("asd")
   
        with self.wid.canvas.before:
            Color(1.0, 0.396078431372549, 0.6235294117647059, 1.0)
            RoundedRectangle(size = (125,self.height),segments = 4, pos = (0,0),group = "asd")
            Color(1,1,1,self.opa)
            Mesh(vertices=[self.posx+0, self.posy+0, 0, 0,self.posx+75, self.posy+50, 0, 0,self.posx+125, self.posy+50, 0, 0,self.posx+50, self.posy+0, 0, 0], indices=[0,1,2,3], mode = 'triangle_fan',group = "asd")
            
class DisplayMenu(GridLayout):
    size_hint = (1,None)
    height = NumericProperty(dp(64))
    rows = 1
    class DisplayMenuItem(ButtonBehavior, RelativeLayout):
        size_hint = (None, 1)
        width = NumericProperty(dp(64))
        insideimgsize = ListProperty([dp(64),dp(64)])
        def __init__(child,**kwargs):
            super().__init__()
            
            with child.canvas:
                Color(1,1,.5,1)
                Rectangle(source = kwargs["source"], size = child.insideimgsize, pos = (32 - child.insideimgsize[0]/2, 47 - child.insideimgsize[1]/2 ))
            
            child.bind(on_release = lambda x: child.animate())
            child.source = kwargs["source"]
            
        def animate(child, *args): (Animation(insideimgsize = [dp(64*.70),dp(64*.70)] , d = .25/2.5, t = 'out_quart') + Animation(insideimgsize = [dp(64),dp(64)] , d = .5*.90, t = 'out_back')).start(child)
        def on_insideimgsize(child, *args):
            child.canvas.clear()
            with child.canvas:
                Color(1,1,.5,1)
                Rectangle(source = child.source, size = child.insideimgsize, pos = (32 - child.insideimgsize[0]/2, 47 - child.insideimgsize[1]/2 ))

    def __init__(this,**kwargs):
        super().__init__(**kwargs)
        three = ["hud15","hud14","hud16"]
        this.add_widget(Label())
        for i in range(3): this.add_widget(this.DisplayMenuItem(source = asset + three[i] + ".png"))
        this.add_widget(Label())
        
class Display(ButtonBehavior,RelativeLayout):
    size_hint = (1,None)
    height = NumericProperty(dp(64))
    def __init__(this,**kwargs):
        super().__init__(**kwargs)
        this.add_widget(Label(text = "[color=#000000]00:00:00",markup = True, font_size = 64))
        
    
        
class LyricsDisplay(RelativeLayout):
    size_hint = (1,None)
    height = NumericProperty(dp(20))
    def __init__(this,**kwargs):
        super().__init__(**kwargs)
        this.add_widget(Label(text = "[color=#000000]0 Horas, 0 Minutos y 0 Segundos",markup = True, font_size = 20))
        
class BottomNavigatorScroll(ScrollView):
    NoItems = NumericProperty(0)
    catch_Scrollposx = NumericProperty(0)
    CurrentAnimation = None
    
    def __init__(this,**kwargs):
        super().__init__(**kwargs)
        
        this.bind(on_touch_down = lambda u,z: this.prepare())
        this.bind(on_scroll_stop = this.getcloser)
        this.bind(on_scroll_start = lambda u,z: setattr(this, 'catch_Scrollposx', this.scroll_x))
        
        
    def prepare(this,*args):
        try:
            Animation.stop_all(this, 'scroll_x')
            print("Canceled.")
        except:
            print("There is no Currentanimation to cancel.")
            
    def getcloser(this, *args):
        straight = -1
        print(straight)
        if this.scroll_x > this.catch_Scrollposx: straight *= -1
        
        print (this.NoItems)
        unit = 1.0 / (this.NoItems)
        print (straight)
        list = []
        c = 0
        list.append(0)
        for i in range(this.NoItems):
            list.append((unit) * (i+1) + ((unit/(this.NoItems-1)) * (i+1)))
            c += 1
        list = list[:-1]
        import pprint
        pp = pprint.PrettyPrinter(depth=6)
        
 
        prox = min(list, key=lambda x:abs(x-(this.scroll_x+(.25*.30*straight))))
        this.CurrentAnimation = Animation(scroll_x = prox, d = .25, t = 'out_back')
        this.CurrentAnimation.start(this)
        print(list)

class TopChooser(RelativeLayout):
    size_hint = (1,None)
    height = NumericProperty(dp(94))
    
    class TopChooserTimericon(RelativeLayout):
        size_hint = (None,None)
        height = NumericProperty(dp(24))
        width = NumericProperty(dp(24))
        pos_hint = DictProperty({'center_y':.75})
        def __init__(child, **kwargs):
            super().__init__()
            with child.canvas:
                Color(1,1,1,1)
                Rectangle(source = asset + "clock.png", size = (child.width, child.height))
            
        def on_pos(child, *args):
            child.canvas.clear()
            with child.canvas:
                Rectangle(source = asset + "clock.png", size = (child.width, child.height))
                
    class TopChooserItem(ButtonBehavior, RelativeLayout):
        size_hint = (None, 1)
        width = NumericProperty(dp(64))
        insideimgsize = ListProperty([dp(64),dp(64)])
        def __init__(child,**kwargs):
            super().__init__()
            
            with child.canvas:
                Color(1,1,1,1)
                Rectangle(source = kwargs["source"], size = child.insideimgsize, pos = (32 - child.insideimgsize[0]/2, 47 - child.insideimgsize[1]/2 ))
            
            child.bind(on_release = lambda x: child.animate())
            child.source = kwargs["source"]

        def animate(child, *args): (Animation(insideimgsize = [dp(32),dp(32)] , d = .25/2, t = 'out_quart') + Animation(insideimgsize = [dp(64),dp(64)] , d = .25/2, t = 'out_expo')).start(child)
        def on_insideimgsize(child, *args):
            child.canvas.clear()
            with child.canvas:
                Color(1,1,1,1)
                Rectangle(source = child.source, size = child.insideimgsize, pos = (32 - child.insideimgsize[0]/2, 47 - child.insideimgsize[1]/2 ))

    
    def __init__(this,**kwargs):
        super().__init__(**kwargs)
        
        relativelayoutgrid = GridLayout(rows = 1, spacing = dp(16))
        
        for i in range(18): relativelayoutgrid.add_widget(this.NewChooserItem(source = asset + "bread.png"))
        
        scrollrelativelayout = RelativeLayout(size_hint_x = None, width = 1500); scrollrelativelayout.add_widget(relativelayoutgrid); scrollrelativelayout.add_widget(this.TopChooserTimericon())
        scroll = ScrollView(bar_color = (1,1,1,0),bar_inactive_color = (1,1,1,0)); scroll.add_widget(scrollrelativelayout)
        this.add_widget(scroll)
        
    def NewChooserItem(this, **kwargs):  
        TopChooseritem = this.TopChooserItem(**kwargs)
        TopChooseritem.bind(on_release = lambda z:Animation(x = z.x , d = 1, t = 'out_back').start(this.children[0].children[0].children[0]))
        
        return TopChooseritem
        
class Tag(RelativeLayout):
    def __init__(self, **kwargs):
        super().__init__()
        self.size_hint_y = kwargs["size_hint_y"]
        self.size_hint_x = None
        self.height = kwargs["height"]
        self.width = dp(64+8)
        with self.canvas:
            Color(1.0, 0.5, 0.875, 1.0)
            RoundedRectangle(size = (dp(64), dp(24)), pos = (4,0))
        self.label = Label(text = kwargs["tag_text"], markup = True ,size_hint = (None,None),size = (dp(64), dp(24)), pos = (0,0))
        self.add_widget(self.label)
class BottomNavigator(GridLayout):
        rows = 1
        height = NumericProperty(dp(64))
        width = NumericProperty(0)
        size_hint_x = NumericProperty(None)
        backcolor1 = ListProperty([.1,.1,.1,1])
        backcolor2 = ListProperty([.11,.11,.11,1])
        opened = BooleanProperty(False)
        class BottomNavigatorItem(ButtonBehavior,RelativeLayout):
            cols = 1
            opacity = NumericProperty(.96)
            opened = BooleanProperty(False)
            class Layer1(RelativeLayout):
                def __init__(child, **kwargs):
                    super().__init__()
                    
                    with child.canvas:
                        Color(1.0, 0.5, 0.875, 1.0)
                        RoundedRectangle(size = (dp(64), dp(24)), pos = (Window.width*.725 - dp(32), dp(64)*.30 - dp(12)))
                    child.label = Label(text = kwargs["tag_text"], markup = True ,size_hint = (None,None),size = (dp(64), dp(24)), pos = (Window.width*.725 - dp(32), dp(64)*.30 - dp(12)))
                    child.add_widget(child.label)
                    
    
                    
            def __init__(child, **kwargs):
                super().__init__()
                child.SmallLabel = Label(text = kwargs["text"], text_size = (Window.width/2, dp(64)), valign = 'middle' , halign = 'left',markup = True, font_size = 18)
                child.Biglabel = Label(text = kwargs["timetext"],markup = True, font_size = 30)
                insidegrid = GridLayout(rows = 1); insidegrid.add_widget(child.Biglabel); insidegrid.add_widget(child.SmallLabel)
                rootgrid = GridLayout(cols = 1); rootgrid.add_widget(insidegrid)
                
                child.add_widget(rootgrid)
                for tagtext in kwargs["tags"]:
                    child.add_widget(child.Layer1(tag_text = tagtext))
                    
            
                child.bind(on_release = lambda x: child.switch())
            def switch(child,*args):
                if child.opened == True: 
                    child.close()
                    child.opened = False
                elif child.opened == False: 
                    child.open()
                    child.opened = True
            def open(child,*args):
                print("PROBANDO")
                child.Biglabel.text = child.Biglabel.text.replace("ffffff","000000")
                child.SmallLabel.text = child.SmallLabel.text.replace("ffffff","000000")
        
            def close(child,*args):
                print("PROBANDO")
                child.Biglabel.text = child.Biglabel.text.replace("000000","ffffff")
                child.SmallLabel.text = child.SmallLabel.text.replace("000000","ffffff")
                
        def __init__(this, **kwargs):   
            super().__init__(**kwargs)

            this.add_widget(this.BottomNavigatorItem(timetext = "[color=#ffffff]00M'00S",tags = ["tag"], text = "[color=#ffffff]Nueva Receta\n[/size][size=16sp][color=#898989ff]Autor[/color]"))
            for i in range(5): this.add_widget(this.BottomNavigatorItem(timetext = "[color=#ffffff]11M'30S",tags = ["Puerco"], text = "[color=#ffffff]Titulo de Receta\n[/size][size=16sp][color=#898989ff]Autor[/color]"))
            for children in this.children: this.width += Window.width
            with this.canvas.before:
                Color(1,1,1,1)
                Rectangle(size = (this.size[0]*1.5, this.size[1]) , pos = (-(this.size[0]*0.25), 0), texture = Gradient.vertical((.1,.1,.1,1),(.11,.11,.11,1)))
        def on_backcolor1(this,*args):
            this.canvas.before.clear()
            with this.canvas.before:
                Color(1,1,1,1)
                Rectangle(size = (this.size[0]*1.5, this.size[1]) , pos = (-(this.size[0]*0.25), 0),                                      texture = Gradient.vertical((this.backcolor1[0],this.backcolor1[1],this.backcolor1[2],this.backcolor1[3]),(this.backcolor2[0],this.backcolor2[1],this.backcolor2[2],this.backcolor2[3])))
        
        def switch(this,*args):
            if this.opened == True: 
                this.close()
                this.opened = False
            elif this.opened == False: 
                this.open()
                this.opened = True
        def open(this,*args):
            print ("a")
            Animation(backcolor1 = [1,1,1,1], backcolor2 = [.99,.99,.99,1], d = .5 , t ='out_circ').start(this)
            
        def close(this,*args):
            print ("a")
            Animation(backcolor1 = [.1,.1,.1,1], backcolor2 = [.11,.11,.11,1], d = .5 , t ='out_circ').start(this)
            


            
class Keyboard(GridLayout):
    cols = 1
    size_hint_y = NumericProperty(None)
    state = BooleanProperty(False)
    height = NumericProperty(dp(54)*4)
    padding = [dp(33),0,dp(33),0]
    print((Window.width - 33)/ 3.0 , "ALINIACION","@Keyboard")
    CurrentAnimation = None
    
    
    class Key(ButtonBehavior,RelativeLayout):
        insideimgsize = ListProperty([dp(15),dp(32)])
        opacity = NumericProperty(1)
        strk = StringProperty("")
        source = StringProperty("")
        animationellipsesize = ListProperty([dp(0),dp(0)])
        animationellipseopacity = NumericProperty(1)
        animationellipsecolor = ListProperty([.91,.91,.91])
        def __init__(child,**kwargs):
            super().__init__(**kwargs)
            
            
            child.paper = RelativeLayout(size_hint = (None,None),pos_hint = {'center_x':.5, 'center_y':.5}, size = (dp(15),dp(30)))
            
            child.add_widget(child.paper)
            
            
            
            with child.paper.canvas:
                Color(child.animationellipsecolor[0],child.animationellipsecolor[1],child.animationellipsecolor[2],child.animationellipseopacity)
                Ellipse(size = child.animationellipsesize, pos = (dp(15)/2 - child.animationellipsesize[0]/2, dp(30)/2 - child.animationellipsesize[1]/2))
                
                Color(1,1,1,1)
                Rectangle(size = child.insideimgsize, source = child.source, pos = (dp(15)/2 - child.insideimgsize[0]/2, dp(30)/2 - child.insideimgsize[1]/2 ))
                
            child.bind(on_release = lambda x: child.animation())
                
        def on_animationellipsesize(child, *args):
            child.paper.canvas.clear()
            with child.paper.canvas:
                Color(child.animationellipsecolor[0],child.animationellipsecolor[1],child.animationellipsecolor[2],child.animationellipseopacity)
                Ellipse(size = child.animationellipsesize, pos = (dp(15)/2 - child.animationellipsesize[0]/2, dp(30)/2 - child.animationellipsesize[1]/2))
                Color(1,1,1,1)
                Rectangle(size = child.insideimgsize, source = child.source, pos = (dp(15)/2 - child.insideimgsize[0]/2, dp(30)/2 - child.insideimgsize[1]/2 ))
            
        def animation(child,*args):
            Animation.stop_all(child, 'animationellipseopacity')
            child.animationellipseopacity = 1
            child.animationellipsesize = (0,0)
            x = Animation(animationellipsesize = (dp(64),dp(64)), animationellipseopacity = 0, d = .5 , t = 'out_quart')
            x.start(child)
    
        def on_insideimgsize(child, *args):
            child.paper.canvas.clear()
            with child.paper.canvas:
                Rectangle(size = child.insideimgsize, source = child.source, pos = (dp(15)/2 - child.insideimgsize[0]/2, dp(30)/2 - child.insideimgsize[1]/2 ))
                
    def __init__(this, **kwargs):
        super().__init__(**kwargs)
        
        grid = GridLayout(cols = 3)
        
        for i in range(9): grid.add_widget(this.Key(source = asset + str(i+1) + ".png", strk = str(i+1)))
            
        grid.add_widget(Widget())
        grid.add_widget(this.Key(source = asset + str('0') + ".png", strk = str(0)))
        grid.add_widget(Widget())
        this.add_widget(grid)
        
        this.y = (dp(54)*-4)
        this.opacity = 0
        
    def switch(this, *args):
        this.prepare()
        if this.state == True:
            this.CurrentAnimation = Animation(y = dp(64 + 16), opacity = 0, d = .25 , t = 'out_quart') + Animation(y = -(this.height), d = 0.25/4 , t = 'out_expo')
            this.CurrentAnimation.start(this)
            this.state = False
        else:
            this.y = dp(64 + 16)
            this.opacity = 0
            this.CurrentAnimation = Animation(y = dp(64 + 16), opacity = 1, d = .25 , t = 'out_back')
            this.CurrentAnimation.start(this)
            this.state = True
            
    def prepare(this,*args):
        try:
            this.CurrentAnimation.cancel()
            print("Canceled.")
        except:
            print("There is no Currentanimation to cancel.")
            
            
            
class Layer1(RelativeLayout):
    typingstateopacity = NumericProperty(1)
    typestateopacity = NumericProperty(1)
    typestate = BooleanProperty(False)
    
    class LockedStateButton(ButtonBehavior, RelativeLayout):
        source = StringProperty(asset + "lock0.png")
        xscale = NumericProperty(1.0)
        
        def __init__(child,**kwargs):
            super().__init__(**kwargs)
            with child.canvas: 
                Color(1,1,1,1)
                Rectangle(source = child.source, size = (dp(50),dp(50)))
                
            child.bind(on_release = lambda x: child.Animatesize())
            
        def on_xscale(child,*args):
            print (child.xscale)
            child.canvas.clear()
            xsize = dp(50)*child.xscale,dp(50)*child.xscale
            with child.canvas: 
                Color(1,1,1,1)
                Rectangle(source = child.source, size = xsize , pos = (dp(50)/2 - xsize[0]/2,dp(50)/2 - xsize[1]/2))
                
            
        def Animatesize(child,*args):
            print("animating")
            try:
                if child.source == asset + "lock0.png":
                    child.source = asset + "lock1.png"
                elif child.source == asset + "lock1.png" :
                    child.source = asset + "lock0.png"
            except:
                pass

            child.xscale = 1.0
            anim1 = Animation(xscale = .75, d = .05,t = "in_circ")
            anim2 = Animation(xscale = 1.0, d = .15,t = "out_circ")
            anim = anim1 + anim2
            anim.start(child)
        
        
    
    def __init__(this,**kwargs):
        super().__init__(**kwargs)
       
        grid = GridLayout(cols = 1);
        
        this.add_widget(grid);
        
        Space0 = Widget(size_hint_y = None , height = dp(16))
        Space1 = Widget(size_hint_y = None , height = dp(32-15))
        Space2 = Widget(size_hint_y = None , height = dp(64))
        Space3 = Widget(size_hint_y = None , height = dp(64))
        
        locksize = (dp(50),dp(50))
        this.lock = this.LockedStateButton(pos = (Window.width*.9 - (locksize[0]/2), dp(94) - (locksize[1]/2)))
        Topchooserlayer = RelativeLayout(height = dp(94), size_hint_y = None)
        this.Displaylayer = RelativeLayout(height = dp(94), size_hint_y = None); this.Displaylayer.add_widget(this.lock)
        
        grid.add_widget(Topchooserlayer);
        grid.add_widget(Space2);
        grid.add_widget(this.Displaylayer);

    
        
        with this.Displaylayer.canvas:
            Color(1,1,1,this.typestateopacity)
            Rectangle(group = 'a',source = asset + "typing.png", size = (locksize), pos = (Window.width*.8 - (locksize[0]/2), dp(94) - (locksize[1]/2)))
    
    def on_typestateopacity(this,*args):
        
        locksize = (dp(50),dp(50))
        this.Displaylayer.canvas.remove_group('a')
            
        with this.Displaylayer.canvas:
            Color(1,1,1,this.typestateopacity)
            Rectangle(group = 'a',source = asset + "typing.png", size = (locksize), pos = (Window.width*.8 - (locksize[0]/2), dp(94) - (locksize[1]/2)))
        
        

    def switchtypestate(this,*args):
        if this.typestate == True:
            Animation(typestateopacity = 0, d = .5, t = 'out_circ').start(this)
            this.typestate = False
        else:
            Animation(typestateopacity = 1, d = .5, t = 'out_circ').start(this)
            this.typestate = True
        
        
class MainActivitie(RelativeLayout):
    CurrentAnimation = None
    
    class Layer2(GridLayout):
        cols = NumericProperty(1)
        size_hint_y = NumericProperty(2)
        pos_hint = DictProperty({'y':-1})
        opened = BooleanProperty(False)
        backcolor = ListProperty([.1,.1,.1,1])
        def __init__(child,**kwargs):
            super().__init__()
            child.space = Widget(size_hint_y = None, height = Window.height - dp(64))
            child.add_widget(child.space)
            BottomNav = BottomNavigator()
            BottomScroll = BottomNavigatorScroll(size_hint_y = None, height = dp(64), NoItems = 6); BottomScroll.add_widget(BottomNav)
            child.add_widget(BottomScroll)
            child.pizzarra = RelativeLayout(size_hint_y = None, height = Window.height )
            child.newcanvas = Widget()
            child.pizzarra.add_widget(child.newcanvas)
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            container = GridLayout(rows = 1, size_hint_y = None, height = dp(36));container.add_widget(Label());container.add_widget(especialbutton());container.add_widget(Label())
            facecanvas = RelativeLayout(size_hint_y = None, height = dp(64+16)*1.5)
            tagsgrid = GridLayout(rows = 1, size_hint_y = None, height = dp(24))
            tagsgrid.add_widget(Widget())
            tagsgrid.add_widget(Tag(tag_text = "Tag1", size_hint_y = None, height = dp(24)))
            tagsgrid.add_widget(Tag(tag_text = "Tag2", size_hint_y = None, height = dp(24)))
            tagsgrid.add_widget(Tag(tag_text = "Tag3", size_hint_y = None, height = dp(24)))
            tagsgrid.add_widget(Tag(tag_text = "Tag4", size_hint_y = None, height = dp(24)))
            tagsgrid.add_widget(Widget())

            grid = GridLayout(cols = 1, opacity = 0)
            grid.add_widget(Widget(size_hint_y = None, height = dp(16)))
            grid.add_widget(Label(text = "[size=24][color=#000000]Nueva Receta", markup = True, size_hint_y = None, height = dp(24)))
            grid.add_widget(Widget(size_hint_y = None, height = dp(8)));grid.add_widget(tagsgrid)
            grid.add_widget(facecanvas)
            grid.add_widget(Widget(size_hint_y = None, height = dp(8)));grid.add_widget(container);grid.add_widget(Widget(size_hint_y = None, height = dp(8)))
 
            grid.add_widget(Label(text = "[size=16][color=#000000]Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.\n \n.<Ingredient>\n.<Ingredient>\n.<Ingredient>\n.<Ingredient>\n \n.<Step>\n.<Step>\n.<Step>\n.<Step>\n.<Step>",text_size = (Window.width*.8, dp(64*4)), halign = 'justify', valign = 'top', markup = True, size_hint_y = None, height = dp(64*4)))
            
            
            
            
            child.pizzarra.add_widget(grid)
            child.add_widget(child.pizzarra)
            child.newcanvas.canvas.clear()
            with child.newcanvas.canvas:
                Color(child.backcolor[0],child.backcolor[1],child.backcolor[2],child.backcolor[3])
                Rectangle(size = (Window.width, Window.height), group = "color")
                
            facecanvas.canvas.clear()
            with facecanvas.canvas:
                Color(.89,.89,.89,1)
                Ellipse(size = (64*1.5,64*1.5), pos = (Window.width/2 - 32*1.5, 8))
                
            for children in BottomScroll.children[0].children:
                children.bind(on_release = lambda x: child.switch())
                children.bind(on_release = lambda x: BottomNav.switch())
                print (children)
                
            child.grid = grid
            
        def say_hello(child,*args): print ("hola")
        def on_backcolor(child,*args):
            child.newcanvas.canvas.remove_group("color")
            with child.newcanvas.canvas:
                Color(child.backcolor[0],child.backcolor[1],child.backcolor[2],child.backcolor[3])
                Rectangle(size = (Window.width, Window.height), group = "color")
            
            
        def switch(child):
            if child.opened == True: 
                child.close()
                child.opened = False
            elif child.opened == False: 
                child.open()
                child.opened = True
                
            print (child.opened)
        def open(child):
            Animation(height = Window.height ,  d = .5 , t ='out_quart').start(child.space)
            Animation(pos_hint = {'y':0} ,  d = .5 , t ='out_cubic').start(child)
            Animation(backcolor = [1,1,1,1] ,  d = .5 , t ='out_cubic').start(child)
            Animation(opacity = .54 ,  d = .25 , t ='out_cubic').start(child.parent.children[-1])
            (Animation(opacity = 0 ,  d = .25 , t ='out_cubic')+Animation(opacity = 1 ,  d = .5 , t ='out_cubic')).start(child.grid)
            
        def close(child):
            Animation(height = Window.height - dp(64) ,  d = .5 , t ='out_quart').start(child.space)
            Animation(pos_hint = {'y':-1} ,  d = .5 , t ='out_quart').start(child)
            Animation(backcolor = [.11,.11,.11,1] ,  d = .5 , t ='out_cubic').start(child)
            Animation(opacity = 1 ,  d = .5 , t ='out_cubic').start(child.parent.children[-1])
            
            (Animation(opacity = 0 ,  d = .5 , t ='out_cubic')).start(child.grid)
            
            
            
    def __init__(this,**kwargs):
        super().__init__(**kwargs)
        
        with this.canvas:
            Rectangle(size = Window.size, texture = Gradient.vertical((1,1,1,1),(.95,.95,.95,1)))
        
        
        
        Space0 = Widget(size_hint_y = None , height = dp(16))
        Space1 = Widget(size_hint_y = None , height = dp(32-15))
        Space2 = Widget(size_hint_y = None , height = dp(64))
        Space3 = Widget(size_hint_y = None , height = dp(64))

        grid = GridLayout(cols = 1);
        keyboard = Keyboard(y = dp(64+16))
        layer1 = Layer1()
        this.layer2 = this.Layer2()
        this.add_widget(grid); this.add_widget(keyboard); this.add_widget(layer1); this.add_widget(this.layer2)
 
        def build(buildable = True):
            this.display = Display()
            this.display.bind(on_release = lambda x: keyboard.switch()) 
            this.display.bind(on_release = lambda x: layer1.switchtypestate()) 
            
            grid.add_widget(TopChooser());
            grid.add_widget(Space2);
            grid.add_widget(this.display);
            grid.add_widget(Space0);
            grid.add_widget(LyricsDisplay());
            grid.add_widget(Space1);
            grid.add_widget(DisplayMenu());
            grid.add_widget(Widget())
            grid.add_widget(Widget())
            grid.add_widget(Space3);
            
        build()
        
    def shake(this,*args):
        this.CurrentAnimation = Animation(y = -4 , d = .25/2 ,  t = 'in_back') + Animation(y = 0 , d = .25/2 ,  t = 'out_back')
        this.CurrentAnimation.start(this.children[-1])
        
        
        
    
    

    
        
    

        
        
        
        
        