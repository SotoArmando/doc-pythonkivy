from __init__ import *

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


class TopPanel(GridLayout):
    def __init__(self,**kwargs):
        super(TopPanel, self).__init__(**kwargs)
        
        self.opened = []
        self.rows = 1
        self.x_size = kwargs["wsize"]
        self.size_hint_y = None
        self.height = 33
        #b2 = Button(on_release = lambda x: self.b1_buttons(lamb = x),text = C4+"Archivo", markup = True , size_hint_x = None , width = 150)
        b1 = Button(on_release = lambda x: self.b1_buttons(lamb = x),text = C4+"Herramientas", markup = True , size_hint_x = None , width = 150)
        self.add_widget(b1)
        #self.add_widget(b2)
        self.add_widget(Button())
        self.root = kwargs["root"]
    def close(self):
        try:
            for i in self.opened: 
                i.parent.remove_widget(i)
        except:
            pass
    
    def b1_buttons(self,**kwargs):
        try:
            for i in self.opened: i.parent.remove_widget(i)
        except:
            pass
        self.opened[:] = []
        print self.pos, kwargs["lamb"].pos
        b1_buttons_pariente_parent = RelativeLayout(pos = kwargs["lamb"].pos,width = 200, height = 150, size_hint = (None,None))
        b1_buttons_pariente_parent.y = self.x_size[1] - 150 - 33
        b1_buttons_pariente = GridLayout(cols = 1)
        b1_buttons_pariente.add_widget(Image(size_hint_y = None, height = 1 , source =color + "16b.png",allow_stretch = True,keep_ratio = False))
        b1_buttons_pariente.add_widget(Button(text = C4+"Agregar Vendedor", markup= True))
        b1_buttons_pariente.add_widget(Image(size_hint_y = None, height = 1 , source =color + "16b.png",allow_stretch = True,keep_ratio = False))
        b1_buttons_pariente.add_widget(Button(text = C4+"Administrar Inventario", markup= True))
        b1_buttons_pariente.add_widget(Image(size_hint_y = None, height = 1 , source =color + "16b.png",allow_stretch = True,keep_ratio = False))
        b1_buttons_pariente.add_widget(Button(text = C4+"Administrar Entregas", markup= True))
        b1_buttons_pariente.add_widget(Image(size_hint_y = None, height = 1 , source =color + "16b.png",allow_stretch = True,keep_ratio = False))
        b1_buttons_pariente.add_widget(Button(text = C4+"Entregas Completadas", markup= True))
        b1_buttons_pariente.add_widget(Image(size_hint_y = None, height = 1 , source =color + "16b.png",allow_stretch = True,keep_ratio = False))
        b1_buttons_pariente_beh = Button(opacity = 0, background_down = color + "None.png")
        b1_buttons_pariente_parent.add_widget(b1_buttons_pariente)
        def endit():
            b1_buttons_pariente_parent.parent.remove_widget(b1_buttons_pariente_parent)
            b1_buttons_pariente_beh.parent.remove_widget(b1_buttons_pariente_beh)
        b1_buttons_pariente_beh.bind(on_release = lambda x: endit())
        for i in b1_buttons_pariente.children: 
            i.bind(on_release = lambda x: endit())
            i.bind(on_release = lambda x: self.root.simplycurrent(x.text[len(C4):]))
        try:
            
            self.parent.parent.add_widget(b1_buttons_pariente_beh)
            self.parent.parent.add_widget(b1_buttons_pariente_parent)
            self.opened.append(b1_buttons_pariente_beh)
            self.opened.append(b1_buttons_pariente)
        except:
            pass
