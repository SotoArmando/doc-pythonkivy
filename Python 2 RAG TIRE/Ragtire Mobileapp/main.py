#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __init__ import *

Config.set('graphics', 'borderless', 1)
Config.set('graphics', 'position', 'custom')
Config.set('graphics', 'window_state', 'visible')
Config.set('graphics', 'resizable', 0)
Config.set('graphics', 'left', 800)
Config.set('graphics', 'top', 25)

reload(sys)
resource_add_path(os.path.dirname(__file__))

Window.size = (426,700)
Window.clearcolor =  (1,1,1,1)

class ImageButton(ButtonBehavior, AsyncImage):
    pass
C1 = "[color=#13C0C7]"
C4 = "[color=#000000]"
C2 = "[color=#404040]"
C3 = "[color=#ff3333]"
C5 = "[color=#FF0000]"
C6 = "[color=#C0C0C0]"
ENDC = "[/color]"

def_textsize = (Window.width-50,50)
patch = os.path.dirname(os.path.abspath(__file__))
hud = patch + '/hud/'
asset = patch + '/mysis/assets/drawable-mdpi/'
icon = patch + '/icons/'
textb = patch + '/textbox/'
database = patch + '/database/'
color = patch + '/mysis/colors/'
barra = patch + '/hud/barras/'
Window.clearcolor = (1, 1, 1, 1)


class InterfaceManager(RelativeLayout):
    def __init__(self, **kwargs):
        super(InterfaceManager, self).__init__(**kwargs)
        self.constant = []
        self.opened = []
        self.acciones = []
        self.Armando = Asistente()
        self.Armando.seturl("http://127.0.0.1:8000/Router")
        self.cliente_jsonrequest_textwidgets = []
        self.Armando2 = Asistente2()
        self.state1 = 1 #top mainbutton
        self.state2 = 1 #botton mainbutton
        self.state5 = 1 #botton mainbutton
        self.state8 = 1 #pregunta
        self.countstate1 = 0 #Nuevo Pedido
        self.buscados = []
        self.tabla0_filter = ""
        self.tabla1_filter = ""
        self.tabla2_filter = ""
        self.tabla3_filter = ""
        self.tabla4_filter = ""
        self.tablasfilter = [self.tabla0_filter,
        self.tabla1_filter,
        self.tabla2_filter,
        self.tabla3_filter,
        self.tabla4_filter]
        self.pantalla_principall = ScreenManager()
        self.pantalla_principall.transition.duration = .225
        self.historial = ["a"]
        self.backcount = 0
        self.temp = self.Armando.returntablesdata()
        self.ROOT_Navitagiondrawer1 = NavigationDrawer(size_hint  = (1,None), size = (Window.width, Window.height -55))
        self.ROOT_Navitagiondrawer1.anim_type = 'slide_above_anim'
        #self.ROOT_Navitagiondrawer1.toggle_main_above()
        self.leftroot = RelativeLayout()
        self.leftroot.add_widget(Image(source = color + "16.png", keep_ratio = False, allow_stretch = True))
        self.ROOT_Navitagiondrawer1.add_widget(self.leftroot)
        self.ROOT_Navitagiondrawer1.add_widget(self.pantalla_principall)
        
        self.add_widget(self.ROOT_Navitagiondrawer1)
        
        #self.screen7widget()
        #self.screen8widget()
        
        self.screen1widget()
        self.topmenu();self.screen2widget()
        self.screen3widget()
        self.screen4widget()
        self.screen5widget()
        self.screen6widget()
        self.screen9widget()
        self.screen_configuracion()
        
        self.shopcartscreen()
        self.historialscreen()
        self.form_crearcliente()
        self.entregasscreen()
        self.recordatoriosscreen()
        self.vendedoresscreen()
        
        self.screen7parent()
        self.screen2parent()

        arriba = (0,Window.height)
        abajo = (0,-100)
        self.tablasroot = [self.tabla0_grid,"",self.tabla2_grid,self.tabla2_grid,self.tabla3_grid]
        
        self.button1 = Button(size_hint = (None,None) , size = (375,71), background_normal = asset + "Group 56.png",background_down = asset + "Group 56.png" )
        button1scatter = Scatter(rows = 1 , size_hint = (None,None),size = (Window.width,71), height = 71,  pos = (0,Window.height))
        dim1 = GridLayout(rows = 1 , size_hint = (None,None),size = (Window.width,71), height = 71)
        button1scatter.add_widget(dim1)
        dim1.add_widget(Button(border = [0,0,0,0],background_normal = asset + "a1.png"))
        dim1.add_widget(self.button1)
        dim1.add_widget(Button(border = [0,0,0,0],background_normal = asset + "a1.png"))
        
        self.button2 = Button(size_hint = (None,None) , size = (374,71), background_normal = asset + "mainbutton2.png" ,background_down = asset + "mainbutton2.png" )
        self.button2.bind(on_release = lambda x:self.current("screen7"))
        button2scatter = Scatter(rows = 1 , pos = (0,-55), size_hint = (None,None),size = (Window.width,71), height = 71)
        dim2 = GridLayout(rows = 1 , size_hint = (None,None),size = (Window.width,71), height = 71)
        button2scatter.add_widget(dim2)
        dim2.add_widget(Button(border = [0,0,0,0],background_normal = asset + "a2.png"))
        dim2.add_widget(self.button2)
        dim2.add_widget(Button(border = [0,0,0,0],background_normal = asset + "a2.png"))
        #self.add_widget(button1scatter)
        #self.add_widget(button2scatter)
        
        #self.button1.bind(on_release = lambda x:self.buttonstate1(x.parent.parent))
        self.button1.bind(on_release = lambda x:self.topmenu_state())
        self.button2.bind(on_release = lambda x:self.buttonstate2(x.parent.parent))
        #self.topmenu()
        parent1 = GridLayout(rows = 1, size_hint_y = None, height = 55, pos = (0,Window.height-55))
        button7 = Button(font_size = 24 , text = "",size_hint_x = None ,background_normal =asset+"Group 55.png",width = 50 )
        button7.bind(on_release = lambda x: self.backspace())
        parent1.add_widget(button7)
        parent1.add_widget(Image(font_size = 24 , text = "",size_hint_x = 1 , source =asset+"Rectangle 25.png" , allow_stretch = True, keep_ratio = False))
        hello = TopNavigationS()
        hello.Img.bind(on_release = lambda x: self.ROOT_Navitagiondrawer1.toggle_state())
        self.add_widget(hello)
        gps_location = StringProperty()
        gps_status = StringProperty('press to get GPS location updates')

        try: 
            gps.configure(on_location=self.on_location,on_status=self.on_status)
            
        except NotImplementedError:
            import traceback
            
            try:
                self.shopcart.returnmappos().text = str(self.getpos())
                self.crearusuario_screen.input13.input0.text = str(self.getpos())
                print self.crearusuario_screen.input13.input0.text
            except:
                print "Error al tomar la posicion sin gps."
                traceback.print_exc()
            #OUTTEXT = C4 + self.gps_status
            #print OUTTEXT
            print 'GPS is not implemented for your platform'

        #self.line.draw_line()

    def principal_current(self,env):
        try:
            if (self.Armando.buscar(2,0,self.Usertext.input0.text)) and (self.Armando.buscar1(2,10,self.Passtext.input0.text)[0]) :
                self.Constant = self.Armando.buscar(2,0,self.Usertext.input0.text)[1]
                self.backcount = 0
                self.userlabel.text = '[b]'+ self.Constant["email"]
                self.shopcart.vendedor = self.Constant["id"]
                #self.entregas.Vendedortxt.input0.text = self.temp[2][0][self.Constant["id"]-1]["username"] 
                if self.pantalla_principall.current == "b" : 
                    if self.state5 == -1:self.topmenu_state()
                    if self.state1 == -1:self.buttonstate1(self.button1.parent.parent)
                    if self.state2 == -1:self.buttonstate2(self.button2.parent.parent)
                else:
                
                    if self.state1 == 1:self.buttonstate1(self.button1.parent.parent)
                    if self.state2 == 1:self.buttonstate2(self.button2.parent.parent)   
                if env == 1:
                    self.pantalla_principall.current = self.pantalla_principall.next()
                elif env == 2:
                    self.pantalla_principall.current = self.pantalla_principall.before()              
                self.historial.append(self.pantalla_principall.current)
            else:
                pass
        except:
            pass
    def form_crearcliente(self):
        
        self.crearusuario_screen = CrearUsuario(data = self.temp,connect = self.data_base_connecttions,name = "dimCliente")
        self.pantalla_principall.add_widget(self.crearusuario_screen)
        
        #self.crearusuario_screen.aceptarbtn().bind(on_release = lambda x: self.agregarcliente())
    def current(self,env,animate = True):  
        self.backcount = 0
        self.pantalla_principall.current = env
        self.historial.append(self.pantalla_principall.current)
        if self.x_parent.y == dp(-400): self.anim_hstate_root()
        if self.ROOT_Navitagiondrawer1.state == 'open':
            if animate:
                self.ROOT_Navitagiondrawer1.anim_to_state('closed')
            else:
                self.ROOT_Navitagiondrawer1.state = 'closed'

        if self.pantalla_principall.current == "b" : 
            if self.state5 == 1:self.topmenu_state()
            if self.state1 == 1:self.buttonstate1(self.button1.parent.parent)
            if self.state2 == 1:self.buttonstate2(self.button2.parent.parent)
        else:
            if self.state5 == -1:self.topmenu_state()
            if self.state1 == -1:self.buttonstate1(self.button1.parent.parent)
            if self.state2 == -1:self.buttonstate2(self.button2.parent.parent)   


    def screen1widget(self): 
        self.screen1 = Screen(name = "a")
        self.pantalla_principall.add_widget(self.screen1)           
        x = self.screen1
        self.x_parent = RelativeLayout()
        x.add_widget(self.x_parent)
        self.x_parent.add_widget(Image(size_hint = (None,None), size = (1223,917), source = asset + "fondo.png", keep_ratio = False, allow_stretch = True))
        x_child = RelativeLayout()
        ##NCN

        C = GridLayout(cols = 1,pos_hint = {'center_x':.5,'center_y':.5}, size_hint_x = None, width = '300dp', size_hint_y = None, height = '400dp')
        
        self.x_parent.add_widget(C)

        #x_child.add_widget(C)

        
        
        
        loginbtn = Button(font_size = 20,markup = True,text = C4+"Iniciar Sesion",size_hint_y = None, height = 46,background_normal= asset+"Group 29.png",background_down= asset+"Group 29.png")
        quitbtn = Button(font_size = 20,markup = True,text = C4+"Salir",size_hint_y = None, height = 46,background_normal= asset+"Group 30.png",background_down= asset+"Group 30.png")
        
        loginbtn.bind(on_release = lambda x: self.principal_current(1))
        
        
        C.add_widget(Image(source = color+"None.png", keep_ratio= False, allow_stretch = True))
        #---------------------------------------------------

        self.Usertext = CustTextInput("Usuario","Credencial","Usuario")     
        self.Usertext.errortxt.text_size = (dp(300)-dp(50),dp(20))
        self.Usertext.label0.text_size = (dp(300)-dp(50),dp(75))
        self.Usertext.input0.text = "royal"
        self.Passtext = CustTextInput("Contraseña","Credencial","Contraseña")
        self.Passtext.errortxt.text_size = (dp(300)-dp(50),dp(20))
        self.Passtext.label0.text_size = (dp(300)-dp(50),dp(75))
        self.Passtext.input0.password = True
        self.Passtext.input0.text = "000000"
        C.add_widget(Label(font_size = 24,markup = True,size_hint_y = None , height = 75,text = C4+"[b]Inicio"))
        C.add_widget(self.Usertext)
        C.add_widget(Image(size_hint_y = None, height = 15,source = color+"None.png", keep_ratio= False, allow_stretch = True))
        C.add_widget(self.Passtext)
        C.add_widget(Label(markup = True,size_hint_y = None , height = 25,text = C4+""))
        
        C.add_widget(loginbtn)
        C.add_widget(Image(size_hint_y = None, height = 1,source = color+"None.png", keep_ratio= False, allow_stretch = True))
        #C.add_widget(quitbtn)
        
        
        
        
        #---------------------------------------------------
        C.add_widget(Image(size_hint_y = None, height = 40,source = color+"None.png", keep_ratio= False, allow_stretch = True))
    def buscar(self):

        self.searcherm.animate1()
        Clock.schedule_interval(lambda x: self.searcherm.animate2(), 1)
        pos = self.getpos()
        object = self.searcherm.clean(pos)
        marcador = MapMarkerPopup(lat=pos[0],lon=pos[1], source = asset + "placeholder.png")
        marcador.bind(on_release = lambda x: self.searcherm.infor.togglepos())
        #self.x_mapview.add_marker(marcador)
        #self.buscados.append(marcador)
        
        object.returnbehavior().bind(on_release = lambda x:self.maphelper(object.position[0],object.position[1]))
        for i in self.temp[0][0]:
            
            item  = self.searcherm.add_new(position = (18.4923863,-69.9371557),cuenta = i["no_factura"], fecha = i["vencto"] , cliente = (self.temp[3][0][(i["cliente"])]["cliente"]))
            bubble = Bubble()
            item.returnbehavior().bind(on_release = lambda x:self.maphelper(item.position[0],item.position[1]))
            #self.x_mapview.add_marker(MapMarkerPopup(lat=item.position[0],lon=item.position[1], placeholder= bubble, source = asset + "Group 5.png"))
            self.buscados.append(item)
        
    def cargar_marcas(self):
        pos = self.getpos()
        object = self.searcherm.clean(pos)
        

        marcador = MapMarkerPopup(lat=pos[0],lon=pos[1], source = asset + "placeholder.png")
        dim = GridLayout(rows = 1)
        dim.add_widget(Button(on_release = lambda x: self.searcherm.toggleinfor(),opacity = .74,background_normal  = color + '16.png', markup = True,text =C4+"[b]Boton1", size_hint = (None,None), size = (dp(100),dp(56))))
        dim.add_widget(Button(on_release = lambda x: self.searcherm.toggleinfor(),opacity = .74,background_normal  = color + '16.png', markup = True,text =C4+"[b]Boton2", size_hint = (None,None), size = (dp(100),dp(56))))
        marcador.add_widget(dim)
        self.x_mapview.add_marker(marcador)

        for i in self.temp[0][0]: 
            bubble = Bubble()
            marcador = MapMarkerPopup(lat=18.4923863,lon=-69.9371557, source = asset + "Group 5.png")
            dim = GridLayout(rows = 1)
            dim.add_widget(Button(on_release = lambda x: self.searcherm.toggleinfor(),opacity = .74,background_normal  = color + '16.png', markup = True,text =C4+"[b]Boton1", size_hint = (None,None), size = (dp(100),dp(56))))
            dim.add_widget(Button(on_release = lambda x: self.searcherm.toggleinfor(),opacity = .74,background_normal  = color + '16.png', markup = True,text =C4+"[b]Boton2", size_hint = (None,None), size = (dp(100),dp(56))))
            marcador.add_widget(dim)
            self.x_mapview.add_marker(marcador)
 
    def getpos(self):
        return (18.461612,-69.922775)
        
    def maphelper(self,a,b):
        self.x_mapview.center_on(a,b)
        
        
        
        self.searcherm.dropdown_dismiss()
        self.line.reposition()
        self.line.draw_line()
      
        
    def screen2widget(self):
        self.screen2 = Screen(name = "b")
        
        self.pantalla_principall.add_widget(self.screen2) 
        x = self.screen2
        self.x_parent = RelativeLayout(opacity = 0)
        accesstoken = "pk.eyJ1IjoiYXJtYW5kbzI5IiwiYSI6ImNpd282ZHJ3azAwMWoydHFuZmJudnNzYzEifQ.12vIF51BCThjrut4Q56sGg"
        sourcex = MapSource(url="https://api.mapbox.com/styles/v1/mapbox/streets-v10/tiles/256/{z}/{x}/{y}?access_token=pk.eyJ1IjoibWFjYXR1cyIsImEiOiJjaXlubGRkdXAwMDJ1MzNwZjdwanhkdnd6In0.eYV9WVlCsI44Ku0HSup7Pg",
        cache_key="custom_map1s",tile_size=256,
        image_ext="jpg", attribution="@Armando Jose Soto Melo")
        self.x_mapview = MapView(lat = 18.454651 , lon = -69.971119, zoom = 16, map_source = sourcex)
            
        
        self.screen2.add_widget(self.x_mapview)
        
        self.theimage = Image(source = color+"16b.png", keep_ratio = False , allow_stretch = True)
        self.searcherm = Searcher()
        self.searcherm.getpos2.bind(on_release = lambda x: self.dibujardirecciones(self.searcherm.posicion0[1:-1].split(','),self.searcherm.posicion1[1:-1].split(',')))
        self.searcherm.behavior().bind(on_text_validate = lambda x: self.buscar())
        self.screen2.add_widget(self.searcherm)
        self.screen2.add_widget(self.theimage)
        
        x.add_widget(self.x_parent)
        self.line = LineMapLayer()
        self.marker = MarkerMapLayer()

        self.x_mapview.add_layer(self.line, mode="scatter")
        self.line.reposition()
        self.x_mapview.add_layer(self.marker)  

        self.cargar_marcas()
        

        button3 =  Button(size_hint = (None,None),size = (81,89), background_normal = asset +"group 33.png",           pos = (0,100) )
        button4 =  Button(size_hint = (None,None),size = (81,89), background_normal = asset +"group 34.png",           pos = (0,200) )
        self.x_parent.add_widget(button3)
        self.x_parent.add_widget(button4)      
        self.locationtext = Button(border = [0,0,0,0],markup = True,background_normal = barra + "barrarad1.png",background_down = barra + "barrarad1.png",size_hint = (None,None), size = (Window.width,50),text_size = (Window.width,50),halign = "center",valign = "middle", pos = (0,350))
        self.x_parent.add_widget(self.locationtext)
        self.hstate_root = RelativeLayout(size_hint = (1,None), height = 350, pos = (0,0))
        
        self.hstate = ScrollView(size_hint = (1,None), height = 350, pos = (0,0))
        
        self.hstate_child = GridLayout(cols = 1, size_hint = (1,None))
        self.hstate.add_widget(self.hstate_child)
        self.hstate_child.bind(minimum_height = self.hstate_child.setter('height'))
        self.hstate_root.add_widget(Button(background_normal = color + "16.png"))
        self.hstate_root.add_widget(self.hstate)
        self.x_parent.add_widget(self.hstate_root)
        menusetx3 = []
        for i in self.temp[0][0]:
            menusetx3.append([3.05,i["no_factura"],i["posicion_mapa"]])
        self.MasterWidget(self.hstate_child,menusetx3) 
        self.hstate_child.add_widget(Image(size_hint_y = None,height = 50,source = color + "16.png", keep_ratio = False, allow_stretch = True))    

        


        self.Inicio_Menu = Inicio(acciones = self.acciones)
        for i in range(10):
            if i == 0 :self.Inicio_Menu.bindings[i].bind(on_release = lambda x: self.current("b")) 
            if i == 1 :self.Inicio_Menu.bindings[i].bind(on_release = lambda x: self.current("shopcart"))
            if i == 2 :self.Inicio_Menu.bindings[i].bind(on_release = lambda x: self.current("entregas"))
            if i == 3 :self.Inicio_Menu.bindings[i].bind(on_release = lambda x: self.current("screen9"))
            if i == 4 :self.Inicio_Menu.bindings[i].bind(on_release = lambda x: self.current("screen5"))
            if i == 5 :self.Inicio_Menu.bindings[i].bind(on_release = lambda x: self.current("dimCliente"))
            if i == 6 :self.Inicio_Menu.bindings[i].bind(on_release = lambda x: self.current("recordatorio"))
            if i == 7 :
                #self.Inicio_Menu.bindings[i].bind(on_release = lambda x: self.current("screen5"))
                self.Inicio_Menu.bindings[i].bind(on_release = lambda x:self.anim_hstate_root()) 
            if i == 8 :self.Inicio_Menu.bindings[i].bind(on_release = lambda x: self.current("config"))
            if i == 9 :self.Inicio_Menu.bindings[i].bind(on_release = lambda x: self.current("vendedores"))
            if i == 10 :self.Inicio_Menu.bindings[i].bind(on_release = lambda x: self.current("config"))

        menusetx1 = [
        [3.04,"Inicio","Tocar para ir."],
        [3.04,"Pedido Actual","Tocar para abrir."],
        [3.04,"Entregas Realizadas","Tocar para abrir."],
        [3.04,"Inventario","Tocar para abrir."],
        [3.04,"Ventas","Cuentas por Cobrar"],
       #[3.04,"Clientes","Tocar para abrir"],
        [3.04,"Añadir Cliente","Tocar para abrir."],
        [3.04,"Recordatorios","Tocar para abrir."],
        [3.04,"Mostrar Ruta","Tocar para mostrar."],
        [3.04,"Configuracion","Tocar para mostrar."],
        [3.04,"Vendedores","Tocar para mostrar."],
        [3.04,"Ayuda","Tocar para mostrar."],
        ]

        
        self.screen2.add_widget(self.Inicio_Menu)
    def anim_hstate_root(self,animate = True):
        if self.ROOT_Navitagiondrawer1.state == 'open':
            if animate:
                self.ROOT_Navitagiondrawer1.anim_to_state('closed')
            else:
                self.ROOT_Navitagiondrawer1.state = 'closed'

                
        if self.x_parent.y == dp(0):
            anim = Animation(y = dp(-400), d = .5, t = "in_out_back")
            anim1 = Animation(opacity = 0, d = .5, t = "out_expo")
            anim.start(self.x_parent)
            anim1.start(self.theimage)
            anim1.start(self.Inicio_Menu)
            try:
                self.Inicio_Menu.parent.remove_widget(self.Inicio_Menu)
            except:
                pass
        elif self.x_parent.y == dp(-400):
            anim = Animation(y = dp(0), d = .5, t = 'out_back')
            anim1 = Animation(opacity = 1, d = .5, t = "out_expo")
            anim.start(self.x_parent)
            anim1.start(self.theimage)
            anim1.start(self.Inicio_Menu)
            try:
                self.screen2.add_widget(self.Inicio_Menu)
            except:
                pass
    def openfilter1(self,object):
        print "hola"
        print object.parent.height
        if object.parent.height == dp(56):
            anim1 = Animation(height = dp(300), d = .225 , t = 'out_expo')
            anim2 = Animation(opacity = 1, d = .225 , t = 'out_expo')
            anim1.start(object.parent)
            anim2.start(object.parent.children[0])
        elif object.parent.height == dp(300):
            anim1 = Animation(height = dp(56), d = .225 , t = 'out_expo')
            anim2 = Animation(opacity = 0, d = .225 , t = 'out_expo')
            anim1.start(object.parent)
            anim2.start(object.parent.children[0])
    def screen_configuracion(self):
        self.screen_conf = Screen(name = "config")
        self.screen_conf.add_widget(Image(source = color + "16.png", keep_ratio = False ,allow_stretch = True))
        screen_conf_layouts = Configuracion()
        
        self.screen_conf.add_widget(screen_conf_layouts)
        self.pantalla_principall.add_widget(self.screen_conf)
        def cambiar_contrasena():
            from django.contrib.auth.hashers import check_password, make_password
            from django.conf import settings
            try:
                settings.configure()
            except:
                pass
            new_pass = make_password(screen_conf_layouts.text2.text)
            json_data = self.Constant
            json_data["password"] = new_pass
            self.Armando.put("User/"+str(json_data['id']), json_data)
        
        screen_conf_layouts.button0.bind(on_release = lambda x: cambiar_contrasena())
    def screen3widget(self):
        self.screen3 = Screen(name = "Screen3")
        self.pantalla_principall.add_widget(self.screen3)
        self.screen3_parent =  GridLayout(cols = 1,size_hint_y = None)
        self.screen3_parent.bind(minimum_height = self.screen3_parent.setter('height'))
        self.screen3_scroll = ScrollView()
        self.screen3_scroll.add_widget(self.screen3_parent)
        self.screen3.add_widget(Image(source = color+"16.png", keep_ratio = False , allow_stretch = True))
        self.screen3.add_widget(self.screen3_scroll)
        self.screen3_parent.add_widget(Image(source = color + "16.png", keep_ratio = False, allow_stretch = True,size_hint_y = None, height = 25))
        self.screen3_parent.add_widget(Label(size_hint_y = None, height = dp(71)))
        self.screen3_parent.add_widget(Label(text = C4+"Ventas",text_size = (Window.width - 50 , dp(50)),valign = 'middle', halign = 'left',size_hint_y = None , height = '50dp', markup = True, font_size = '24sp'))
        #self.screen3_parent.add_widget(Image(size_hint_y = None, height = dp(1), keep_ratio = False, allow_stretch = True, source = color+'3.png', opacity = .14))
        
        
        menusetx1 = [["buscador","Buscar Pedido","10"]]
        self.MasterWidget(self.screen3_parent,menusetx1) 
        open_filtros = Button(on_release = lambda x: self.openfilter1(x),markup = True, text = C4+"[b]Criterios",font_size = dp(18), background_normal = color + '16.png', background_down = color + '16.png',valign = 'middle',text_size = (Window.width - dp(25),dp(56)), size_hint_y = None, height = dp(56))
        
        
        self.lay = GridLayout(cols = 1, size_hint_y = None , height = dp(56))
        self.lay_dim = GridLayout(cols = 2, opacity = 0.)
 
        self.lay.add_widget(open_filtros)
        self.lay.add_widget(self.lay_dim)
        for i in self.temp[0][1]:
            newwidget = ToggleButton(background_normal = color +"16.png",markup = True,group = "Account_Receivable", text =C4+i,valign = 'middle',text_size = (Window.width/2 -dp(25), dp(36)), font_size = 16)
            
            newwidget.bind(on_press = lambda x: self.set_FiltrarCampo(0,x.text[len(C4):]))
            self.lay_dim.add_widget(newwidget)

        self.calendar_0 = Calendar()
        self.calendar_0.conf.bind(on_release = lambda x: self.Filtrar_entrefechas())
        self.screen3_parent.add_widget(self.lay)
        self.screen3_parent.add_widget(self.calendar_0)
        self.screen3_parent.add_widget(Image(size_hint_y = None, height = dp(6), keep_ratio = False, allow_stretch = True, source = asset +'shaddown.png', opacity = 1))
        #self.MasterWidget(self.screen3_parent,[[3.03,"Agregar Pedido",""]])
        
        self.tabla0_grid = GridLayout(cols = 1, size_hint_y = None)

        self.screen3_parent.add_widget(self.tabla0_grid)
        
        for i in self.temp[0][0]:
            
            #self.MasterViews(self.tabla0_grid,[[0,C4+str()+"\n"+ENDC+C6++ENDC,C4+[:10]+"\n"+ENDC++ENDC]])
            
            #self.tabla0_grid.add_widget(Image(size_hint_y = None , height = 1, source = color + "16b.png", keep_ratio= False , allow_stretch = True))
            pariente_parent = RelativeLayout(size_hint_y = None, height = dp(74))
            pariente_dim = GridLayout(cols = 2, spacing = 0, padding = [0,0,0,0])
            pariente_dim.add_widget(Image(size_hint_x = None, width = dp(56), keep_ratio = False, allow_stretch = False, opacity = .54, source = asset + "ic_account_balance_black_36px.png"))
            pariente = GridLayout(cols = 2, spacing = 0, padding = [0,0,0,0])
            pariente_dim.add_widget(pariente)
            pariente.add_widget(Label(text_size = ((Window.width/2) - dp(25) - dp(56), dp(74/2)),valign = 'middle',halign = 'left' ,text = C4 + "[b]" + str(self.temp[3][0][int(i["cliente"]) - 1]["cliente"]),markup = True,))
            pariente.add_widget(Label(text_size = ((Window.width/2) - dp(25) - dp(56), dp(74/2)),valign = 'middle',halign = 'left' ,text = C4 + i["emision"][:10],markup = True,))
            pariente.add_widget(Label(text_size = ((Window.width/2) - dp(25) - dp(56), dp(74/2)),valign = 'middle',halign = 'left' ,text = C4 + "[b]" + i["no_factura"],markup = True,))
            pariente.add_widget(Label(text_size = ((Window.width/2) - dp(25) - dp(56), dp(74/2)),valign = 'middle',halign = 'left' ,text = C5 + i["vencto"][:10],markup = True,))
            pariente_parent.add_widget(pariente_dim)
            pariente_parent.add_widget(Button(opacity = 0  , on_release = lambda x: self.current("Screen4")))
            
            self.tabla0_grid.add_widget(pariente_parent)
            self.tabla0_grid.add_widget(Image(size_hint_y = None , height = 1, source = color + "16b.png", keep_ratio= False , allow_stretch = True))
            self.tabla0_grid.add_widget(Label(size_hint_y = None, height = dp(14)))


            self.tabla0_grid.height += 74
            
            valores = i['emision'][:10].split('-')
            valor = (int(valores[1]),int(valores[2]))
            print valor

        pass        
    def screen4widget(self):
        self.screen4 = Screen(name = "Screen4")
        self.pantalla_principall.add_widget(self.screen4)
        self.screen4_parent = GridLayout(cols =1, size_hint_y = None,height = Window.height)
        self.screen4.add_widget(Image(source = color + "16.png", allow_stretch = True, keep_ratio = False))
        self.screen4.add_widget(self.screen4_parent)
        self.screen4_scrollview = ScrollView(size_hint_y = None, height = dp(300))
        self.scrollview_parent = GridLayout(cols = 1,size_hint_y = None)
        self.scrollview_parent.bind(minimum_height = self.scrollview_parent.setter('height'))
        self.screen4_scrollview.add_widget(self.scrollview_parent)
        
        self.screen4_parent.add_widget(Label(size_hint_y = None, height = 55))
        self.screen4_parent.add_widget(self.screen4_scrollview)
        for i in range(10):
            self.MasterViews(self.scrollview_parent,[[0.01]])
            self.scrollview_parent.add_widget(Image(source = color + "16.png",size_hint_y = None,height = 1, keep_ratio = False, allow_stretch = True))
        parent2 = GridLayout(rows = 1,size_hint_y = None , height = 58)
        #self.screen4_parent.add_widget(Image(source = color + "16b.png", size_hint_y = None , height = 1, keep_ratio = False, allow_stretch = True))
        self.screen4_parent.add_widget(Label(text = C4+"Cuenta por Cobrar",text_size = (Window.width - 50 , dp(50)),valign = 'middle', halign = 'left',size_hint_y = None , height = '50dp', markup = True, font_size = '24sp'))
        self.screen4_parent.add_widget(Image(size_hint_y = None, height = dp(1), keep_ratio = False, allow_stretch = True, source = color+'3.png', opacity = .14))
        self.screen4_parent.add_widget(Image(size_hint_y = None, height = dp(6), keep_ratio = False, allow_stretch = True, source = asset+'shaddown.png', opacity = 1))
                
        
        
        for i in range(4):
            texset = ["Hace 1 Semana", "Calle Norberto Torres 19, Los Restauradores", "Emitida el 19/02/2017","Se Vence el 21/02/2017"]
            imgset = ["7","8","10","9"]
            parent3 = GridLayout(rows = 1, size_hint_y = None , height = 50)
            #parent3.add_widget(Image(source = color +"16.png", size_hint_x = None, width = 75, allow_stretch = True , keep_ratio= False))
            parent3.add_widget(Image(opacity = .54,source = color + "16.png", size_hint_x = None, width = dp(25)))
            parent3.add_widget(Button(font_size = 16,text =C4+ texset[i], size_hint_y = None  ,height = 50,background_normal = color + "16.png",markup= True, text_size = (Window.width/2,35)))
            self.screen4_parent.add_widget(parent3)
            #self.screen4_parent.height += 50
            if i == (3):
                self.screen4_parent.add_widget(Image(source = color + "16.png",size_hint_y = None,height = 300, keep_ratio = False, allow_stretch = True))
    def screen5widget(self):
        def managinx(x,y):
            print x,y
            self.screen5sc.current = y
        self.screen5 = Screen(name = "screen5")
        self.pantalla_principall.add_widget(self.screen5)
        self.screen5_parent = GridLayout(cols = 1, size_hint_y = None)
        self.screen5_parent.bind(minimum_height = self.screen5_parent.setter('height'))
        self.screen5_parentroot = ScrollView()
        self.screen5.add_widget(Image(source = color+"16.png", keep_ratio = False , allow_stretch = True))
        self.screen5sc= ScreenManager()
        screen0 = Screen(name = "main")
        screen1 = Screen(name = "Examinar Documento")
        scroll9 = ScrollView()
        screen1_parent = GridLayout(cols = 1,size_hint_y = None, height = 300)
        scroll9.add_widget(screen1_parent)
        screen1.add_widget(scroll9)
        self.parent_scrollview2 = ScrollView(do_scroll_x = True, do_scroll_y = False, size_hint_y = None, height = 300)
        self.scrollview2_parent = GridLayout(rows = 4, cols = 6, size_hint_x = None, width = 700)
        self.scrollview2_parent.bind(minimum_width = self.scrollview2_parent.setter('width'))
        self.parent_scrollview2.add_widget(self.scrollview2_parent)
        i = self.temp[3][0][0]
        client = ClientShow(item = i, temp = self.temp, managing = managinx)
        
        
        screen1_parent.height += 290
        rowsset1 = [
        ["M","0 30","31 60","61 90","91 120","121 +"],
        ["Balance","470,000.00","80,000.00","","","15,000.00"],
        ["Porciento","83.40%","14.00%","","","2.60%"],
        ]
        for row in rowsset1:
            for i in row:
                settimg = color + "16bb.png" 
                if (i == "M")or(i == "Balance")or(i=="Porciento"): 
                    b = ''
                    settimg = color + "16b.png" 
                else:
                    b = '[b]'
                self.scrollview2_parent.add_widget(Button(background_normal = settimg,text = C4+b+i,markup= True,font_size = 16))
        #screen1_parent.add_widget(Label(size_hint_y = None, height = dp(71)))
        screen1_parent.add_widget(self.parent_scrollview2)
        screen1_parent.add_widget(client)
        
        self.screen5sc.add_widget(screen0)
        self.screen5sc.add_widget(screen1)

        self.screen5.add_widget(self.screen5sc)
        screen0.add_widget(self.screen5_parentroot)
        self.screen5_parentroot.add_widget(self.screen5_parent)
        #self.screen5_parent.add_widget(Image(source = color + "16.png", size_hint_y = None, height = 25,keep_ratio = False, allow_stretch = True))
        #self.screen5_parent.add_widget(Image(source = color + "16.png", keep_ratio = False, allow_stretch = True,size_hint_y = None, height = 25))
        self.screen5_parent.add_widget(Label(size_hint_y = None, height = dp(71)))
        self.screen5_parent.add_widget(Label(text = C4+"Clientes",text_size  = (Window.width - 50 , dp(50)),valign = 'middle', halign = 'left',size_hint_y = None , height = '50dp', markup = True, font_size = '24sp'))
        
        relat1 = RelativeLayout(size_hint_y = None, height = 100)
        relat1.add_widget(SizeButton(background_normal = "None",text = C4+"Seleccione un cliente y a continuacion se le mostrara todas las compras respectivas del mismo.",pos_hint = {'center_x':.5, 'center_y':.5},text_size = (Window.width *.75 , 100),valign = 'middle', halign = 'center',size_hint_y = None , height = '50dp', markup = True))
        self.screen5_parent.add_widget(relat1)
        #self.screen5_parent.add_widget(Image(size_hint_y = None, height = dp(1), keep_ratio = False, allow_stretch = True, source = color+'3.png', opacity = .14))
        
        
        self.MasterWidget(self.screen5_parent,[["buscador","Buscar Cliente"]])

        open_filtros = Button(on_release = lambda x: self.openfilter1(x),markup = True, text = C4+"[b]Criterios",font_size = dp(18), background_normal = color + '16.png', background_down = color + '16.png',valign = 'middle',text_size = (Window.width - dp(25),dp(56)), size_hint_y = None, height = dp(56))
            
        self.lay = GridLayout(cols = 1, size_hint_y = None , height = dp(56))
        self.lay_dim = GridLayout(cols = 2, opacity = 0.)
        self.lay.add_widget(open_filtros)
        
        self.lay.add_widget(self.lay_dim)
        
        for i in self.temp[3][1]:
            newwidget = ToggleButton(background_normal = color +"16.png",markup = True,group = "Clientes", text =C4+i,valign = 'middle',text_size = (Window.width/2 -dp(25), dp(36)), font_size = 16)
            
            newwidget.bind(on_press = lambda x: self.set_FiltrarCampo(3,x.text[len(C4):]))
            self.lay_dim.add_widget(newwidget)
            
        self.screen5_parent.add_widget(self.lay)
        self.screen5_parent.add_widget(Image(size_hint_y = None, height = dp(6), keep_ratio = False, allow_stretch = True, source = asset+'shaddown.png', opacity = 1))
        self.screen5_parent.add_widget(Image(source = color + "16.png", size_hint_y = None, height = 25,keep_ratio = False, allow_stretch = True))
        def calcular_suma(val1):
            calcx = 0
            for dim in self.temp[0][0]:
                if val1 == dim["cliente"]:
                    calcx += float(dim["balance_original"])
            return str(calcx)
        
        self.tabla2_grid = GridLayout(cols = 1 , size_hint_y = None)
        self.screen5_parent.add_widget(self.tabla2_grid)
        for i in self.temp[3][0]:
            client = ClientShow(item = i, temp = self.temp, managing = managinx)
            self.tabla2_grid.add_widget(client)
            
            self.tabla2_grid.height += 290
    def screen6widget(self):
        self.screen6 = Screen(name = "screen6")
        self.pantalla_principall.add_widget(self.screen6)
        self.screen6_parent = GridLayout(cols = 1)
        self.screen6.add_widget(Image(source = color + "16.png", keep_ratio = False, allow_stretch = True))
        self.screen6.add_widget(self.screen6_parent)
        self.screen6_parent.add_widget(Label(size_hint_y = None, height = 1))
        self.parent_scrollview1 = ScrollView()
        self.parent_scrollview2 = ScrollView(do_scroll_x = True, do_scroll_y = False, size_hint_y = None, height = 300)
        self.scrollview2_parent = GridLayout(rows = 4, cols = 6, size_hint_x = None, width = 660)
        self.scrollview2_parent.bind(minimum_width = self.scrollview2_parent.setter('width'))
        #self.MasterViews(self.screen6_parent,[[0.02]])
        #-------------------------------------------------------
        i = self.temp[0][0][0]
        self.screen6_object0 = RelativeLayout(size_hint_y = None, height = dp(74))
        pariente_dim = GridLayout(cols = 2, spacing = 0, padding = [0,0,0,0])
        pariente_dim.add_widget(Image(size_hint_x = None, width = dp(56), keep_ratio = False, allow_stretch = False, opacity = .54, source = asset + "ic_account_balance_black_36px.png"))
        pariente = GridLayout(cols = 2, spacing = 0, padding = [0,0,0,0])
        pariente_dim.add_widget(pariente)
        pariente.add_widget(Label(text_size = ((Window.width/2) - dp(25) - dp(56), dp(74/2)),valign = 'middle',halign = 'left' ,text = C4 + "[b]" + str(self.temp[3][0][int(i["cliente"]) - 1]["cliente"]),markup = True,))
        pariente.add_widget(Label(text_size = ((Window.width/2) - dp(25) - dp(56), dp(74/2)),valign = 'middle',halign = 'left' ,text = C4 + i["emision"][:10],markup = True,))
        pariente.add_widget(Label(text_size = ((Window.width/2) - dp(25) - dp(56), dp(74/2)),valign = 'middle',halign = 'left' ,text = C4 + "[b]" + i["no_factura"],markup = True,))
        pariente.add_widget(Label(text_size = ((Window.width/2) - dp(25) - dp(56), dp(74/2)),valign = 'middle',halign = 'left' ,text = C5 + i["vencto"][:10],markup = True,))
        self.screen6_object0.add_widget(pariente_dim)
        self.screen6_parent.add_widget(Label(size_hint_y = None, height = dp(14)))
        self.screen6_parent.add_widget(ClientButton("str1","str2"))
        Datos1 = C4+"Cliente 004\nCooperativa de Camioneros de Santo Domingo\n30/11/2016\n\nCantidad de Documentos: 15"
        self.screen6_datos = Button(line_height = 1.4,text_size = (Window.width-dp(25),150),valign = "middle",markup = True,font_size = 16,size_hint_y =None , height = 150, text = Datos1, background_normal = color +"16.png")
        #-------------------------------------------------------------
        
        
        
        self.screen6_parent.add_widget(Image(source = color + "16b.png", keep_ratio= False, allow_stretch = True, size_hint_y = None , height = 1))
        self.screen6_parent.add_widget(self.parent_scrollview2)
        self.parent_scrollview2.add_widget(self.scrollview2_parent)
        rowsset1 = [
        ["M","0 30","31 60","61 90","91 120","121 +"],
        ["Balance","470,000.00","80,000.00","","","15,000.00"],
        ["Porciento","83.40%","14.00%","","","2.60%"],
        ]
        for row in rowsset1:
            for i in row:
                settimg = color + "16bb.png" 
                if (i == "M")or(i == "Balance")or(i=="Porciento"): settimg = color + "16b.png" 
                self.scrollview2_parent.add_widget(Button(background_normal = settimg,text = C4+i,markup= True,font_size = 16))
        
        self.screen6_parent.add_widget(self.screen6_datos)
        self.screen6_parent.add_widget(Button(background_normal = color + "16.png",background_down = color + "16.png",on_release = lambda x: self.current("historial"),text = C4+"Historial de Direcciones",markup = True, text_size = (Window.width - dp(25), dp(56)), size_hint_y = None, height = dp(56), halign = 'left', valign = 'middle' ))
        
    
    def screen7widget(self):
        self.screen7 = Screen(name = "screen7")
        self.pantalla_principall.add_widget(self.screen7)
        self.nuevo_cliente = GridLayout(cols = 1, size_hint = (None,None), size = (Window.width,Window.height), spacing = 0)
        self.screen7.add_widget(self.nuevo_cliente)
        self.nuevo_cliente.add_widget(Button(size_hint= (1,None), height = 55,background_normal = barra + "barra1.png"))

        menuset1 = ["Nuevo Cliente",[1,"Cliente"],[1,"Identificacion"],
        [2,"RNC","CEDULA"],[1,"Contacto"],[1,"Telefono1"],
        [1,"Telefono2"],[1,"Direccion1"],[1,"Sector1"],
        [1,"Ciudad1"],[1,"Direccion 2"],[1,"Sector2"],[1,"Ciudad2"]]
        self.cliente_jsonrequest = {}
        
        for i in range(13):
            try:
                if menuset1[i][0] == 1:
                    dim1 = GridLayout(rows = 1,size_hint_y = None, height = 50)
                    widget = Button(font_size = 19,text_size = (100,60), halign = "left", valign = "middle",size_hint_y = None,size_hint_x = None, width = 150, height = 50,markup = True,text = C4+menuset1[i][1]+":", background_normal = color+"16.png")
                    widgettext = TextInput(padding = [25,15,0,0],size_hint_y = None,size_hint_x = 1, width = 100, height = 50,markup = True,text = "", background_normal = color+"16b.png", background_active = color+"16b.png")
                    dim1.add_widget(widget)
                    dim1.add_widget(widgettext)
                    self.nuevo_cliente.add_widget(dim1)
                    self.nuevo_cliente.add_widget(Image(source = color + "16c.png", size_hint_y = None, height = 1, allow_stretch = True , keep_ratio = False))
                    

                elif menuset1[i][0] == 2:
                    dim1 = GridLayout(rows = 1,size_hint_y = None, height = 50)
                    dim1.add_widget(ToggleButton(text_size = (Window.width/2 -50,60), halign = "center", valign = "middle",size_hint_y = None,size_hint_x = 1, width = 150, height = 50,markup = True,text = "[b]"+C4+menuset1[i][1]+"", background_normal = color+"16.png",background_down = color+"1.png",group = "a"))
                    dim1.add_widget(ToggleButton(text_size = (Window.width/2 -50,60), halign = "center", valign = "middle",size_hint_y = None,size_hint_x = 1, width = 150, height = 50,markup = True,text = "[b]"+C4+menuset1[i][2]+"", background_normal = color+"16.png",background_down = color+"1.png",group = "a"))
                    self.nuevo_cliente.add_widget(dim1)
                    self.nuevo_cliente.add_widget(Image(source = color + "16c.png", size_hint_y = None, height = 1, allow_stretch = True , keep_ratio = False))

                else:
                    
                    Button1 =Button(font_size = 19,size_hint_y = None, height = 50,markup = True,text =C4+ menuset1[i], background_normal = color+"16.png", background_down = color+"16.png")
                    self.nuevo_cliente.add_widget(Button1)
                    self.nuevo_cliente.add_widget(Image(source = color + "16c.png", size_hint_y = None, height = 1, allow_stretch = True , keep_ratio = False))
            except:
                
                Button1 =Button(font_size = 19,size_hint_y = None, height = 50,markup = True,text =C4+ menuset1[i], background_normal = color+"16.png", background_down = color+"16.png")
                self.nuevo_cliente.add_widget(Button1)
                self.nuevo_cliente.add_widget(Image(source = color + "16c.png", size_hint_y = None, height = 1, allow_stretch = True , keep_ratio = False))
            
            if i == 0:
                pass
                ##Button1.bind(on_release = lambda x: self.Animate1(self.screenmanager,(0,-Window.height+70),(0,0)))
            if i == 12:
                dim2 = GridLayout(rows = 1, height = 50, size_hint_y = None )
                buttonset = ["Aprobar","Cancelar"]
                colorset = ["16","16"]
                for x in range(2):
                    button2 =Button(font_size = 19,text_size = (Window.width/2 -50,60), halign = "center", valign = "middle",size_hint_y = None,size_hint_x = 1, width = 150, height = 50,markup = True,text = C4+buttonset[x]+"", background_normal = color+colorset[x]+".png")
                    dim2.add_widget(button2)
                    if x == 1:button2.bind(on_release = lambda x: self.Animate1(self.screenmanager,(0,-Window.height+70),(0,0)))
                    elif x == 0:button2.bind(on_release = lambda x: self.agregarcliente())
                        
                    
                    
                self.nuevo_cliente.add_widget(dim2)
        
    def manymenu(self,item,objecto):
        try:
            for i in self.opened: i.parent.remove_widget(i)
            self.opened[:] = []
            def plus(x): 
                item.text = C4 + str(int(item.text[len(C4):]) + 1)
                objecto.unidades += 1
            def less(x): 
                item.text = C4 + str(int(item.text[len(C4):]) - 1)
                objecto.unidades -= 1
            manymenu_parent = GridLayout(y = dp(-56),rows = 1, size_hint_y = None, height = dp(56), opacity = .94)
            manymenu_parent.add_widget(Button(background_normal = color + "3.png",background_down = color + "2.png",text = "-", on_release = lambda x: less(x)))
            def close(x):
                anim = Animation(y = dp(-56), d = .225 , t = 'in_expo')
                def eliminate_x(): x.parent.parent.remove_widget(x.parent)
                #anim.bind(on_complete = lambda a,b: eliminate_x())
                anim.start(x.parent)

                
            manymenu_parent.add_widget(Button(background_normal = color + "3.png",background_down = color + "2.png",text = "close", on_release = lambda x: close(x)))
            manymenu_parent.add_widget(Button(background_normal = color + "3.png",background_down = color + "2.png",text = "+", on_release = lambda x: plus(x)))
            self.add_widget(manymenu_parent)
            anim = Animation(y = 0, d = .225 , t = 'out_expo')
            anim.start(manymenu_parent)
            self.opened.append(manymenu_parent)
        
            
            
            
        except:
            pass
    def dibujardirecciones(self, pos1,pos2):
        def Done():
            try:
                for n in range(2):
                    if pos1[n][0] == ' ':
                        pos1[n] = float(pos1[n][1:])
                    if pos2[n][0] == ' ':
                        pos2[n] = float(pos2[n][1:])
                
                    
                print pos1,pos2
                direcciones = self.Armando2.returngeo(pos1[::-1],pos2[::-1])
                self.line.clear()
                marker0 = MapMarker(anchor_y = 0.5 ,lat= float(direcciones[0][1]), lon= float(direcciones[0][0]), source = "here.png")
                self.x_mapview.add_marker(marker0, layer = self.marker )
                
                marker1 = MapMarker(anchor_y = 0.5 ,lat= float(direcciones[-1][1]), lon= float(direcciones[-1][0]), source = "here.png")
                self.x_mapview.add_marker(marker1, layer = self.marker )
                for i in direcciones:
                    
                    self.line.newpointgeo(i)
                self.line.draw_line()
            except:
                pass
        Clock.schedule_once(lambda x: Done(), .330)
    def historialscreen(self):
        self.historial_screen = Historial(name = "historial")
        self.pantalla_principall.add_widget(self.historial_screen)
    def entregasscreen(self):    
        self.entregas = Entregas(connect = self.data_base_connecttions,s = self,name = "entregas", temp = self.temp)
        self.pantalla_principall.add_widget(self.entregas)
    def vendedoresscreen(self):    
        self.vendedores = Vendedores(r = self,name = "vendedores", temp = self.temp, connect = self.data_base_connecttions)
        self.pantalla_principall.add_widget(self.vendedores)
    
    def recordatoriosscreen(self):    
        self.recordatorio = Recordatorio(e = self.entregas ,name = "recordatorio",root = self, temp = self.temp)
        self.pantalla_principall.add_widget(self.recordatorio)
        
    def shopcartscreen(self):
        self.shopcart = ShopCart(root = self,name = "shopcart",temp = self.temp,connect = self.data_base_connecttions)
        self.pantalla_principall.add_widget(self.shopcart)
        def managinx(x,y):
            print x,y
            self.screen5sc.current = y
        for i in self.temp[3][0]:
            cliente = ClientShow_B(item = i, temp = self.temp, managing = managinx)
            #cliente.return_behavior().bind(on_release = lambda x: self.shopcart.advice(x))
            self.shopcart.clientes_root().add_widget(cliente)
            def seleccionar(x):
                self.shopcart.seleccionado = x
                print x, "seleccionado"
            cliente.return_behavior().bind(on_release = lambda x : seleccionar(x.text))
            self.shopcart.clientes_root().height += 250
       
            
    def screen8widget(self):
        self.screen8 = Screen(name = "screen8")
        self.pantalla_principall.add_widget(self.screen8)
        self.screen8_parent = GridLayout(cols = 1)
        screen8widgetset = [[1,"Documento No.",True],[1,"Posicion del Mapa",True],[1,"Cliente",True],[1,"Emision",True],[1,"Vencto",True],[1,"Dias"],[1,"Balance Original",True],[1,"Creditos o Pagos"],[1,"Balance Actual",True]]
        self.screen8.add_widget(self.screen8_parent)
        self.MasterWidget(self.screen8_parent,screen8widgetset)
    def screen9widget(self):
        self.screen9 = Screen(name = "screen9")
        self.pantalla_principall.add_widget(self.screen9)
        self.screen9_parent = GridLayout(cols = 1,size_hint_y = None )
        self.screen9_parent.bind(minimum_height = self.screen9_parent.setter('height'))
        screen9widgetset = []
        self.screen9_scroll = ScrollView()
        self.screen9_scroll.add_widget(self.screen9_parent)
        self.screen9.add_widget(Image(source = color + "16.png", keep_ratio = False, allow_stretch = True))
        self.screen9.add_widget(self.screen9_scroll)
        #self.MasterWidget(self.screen9_parent,screen9widgetset)
        self.screen9_parent.add_widget(Image(source = color + "16.png", keep_ratio = False, allow_stretch = True,size_hint_y = None, height = 25))
        self.screen9_parent.add_widget(Label(size_hint_y = None, height = dp(71)))
        self.screen9_parent.add_widget(Label(text = C4+"Inventario",text_size = (Window.width - 50 , dp(50)),valign = 'middle', halign = 'left',size_hint_y = None , height = '50dp', markup = True, font_size = '24sp'))
        
        relat1 = RelativeLayout(size_hint_y = None, height = 100)
        relat1.add_widget(SizeButton(background_normal = "None",text = C4+"Puede añadir objetos a la compra actual presionando el boton de cada objeto.",pos_hint = {'center_x':.5, 'center_y':.5},text_size = (Window.width *.75 , 100),valign = 'middle', halign = 'center',size_hint_y = None , height = '50dp', markup = True))
        self.screen9_parent.add_widget(relat1)
        
        #self.screen9_parent.add_widget(Image(size_hint_y = None, height = dp(1), keep_ratio = False, allow_stretch = True, source = color+'3.png', opacity = .14))
        
        self.MasterWidget(self.screen9_parent,[["buscador","Buscar en Inventario"]])
        
        open_filtros = Button(on_release = lambda x: self.openfilter1(x),markup = True, text = C4+"[b]Criterios",font_size = dp(18), background_normal = color + '16.png', background_down = color + '16.png',valign = 'middle',text_size = (Window.width - dp(25),dp(56)), size_hint_y = None, height = dp(56))
        self.lay = GridLayout(cols = 1, size_hint_y = None , height = dp(56))
        self.lay_dim = GridLayout(cols = 2, opacity = 0.)
        self.lay.add_widget(open_filtros)
       
        self.lay.add_widget(self.lay_dim)
        
        for i in self.temp[4][1]:
            newwidget = ToggleButton(background_normal = color +"16.png",markup = True,group = "Clientes", text =C4+i,valign = 'middle',text_size = (Window.width/2 -dp(25), dp(36)), font_size = 16)
            
            newwidget.bind(on_press = lambda x: self.set_FiltrarCampo(4,x.text[len(C4):]))
            self.lay_dim.add_widget(newwidget)
            
        self.screen9_parent.add_widget(self.lay)
        self.screen9_parent.add_widget(Image(size_hint_y = None, height = dp(6), keep_ratio = False, allow_stretch = True, source = asset+'shaddown.png', opacity = 1))
        self.tabla3_grid = GridLayout(cols = 1, size_hint_y = None)

        self.screen9_parent.add_widget(self.tabla3_grid)
        for i in self.temp[4][0]:
            #Marca,Descripcion,clasificacion, precio_1, precio_2,precio_3
            objeto = StockItem(i["marca"]+"[/b] "+i["item_name"],i["descripcion"],i["clasificacion"],i["precio_1"],i["precio_2"],i["precio_3"],item = i)
            #objeto.returntext().text = C4+"[b]"+i["marca"]+"[/b]\n"+i["descripcion"]+"\n\n[b]"+i["precio_1"]+" RD$"
            objeto.returntext().line_height = 1
            objeto.returntext().font_size = 16
            objeto.getbehavior().bind(on_release = lambda x: objeto.actualizarcantidad())
            objeto.getbehavior().bind(on_release = lambda x: self.shopcart.agregarcarrito(objeto.marca,objeto.descripcion,objeto.clasificacion,objeto.precio_1,objeto.precio_2,objeto.precio_3,objeto.unidades, item = x.parent.parent.item))
            objeto.returncuanty().bind(on_release = lambda x: self.manymenu(x,objeto))

            self.tabla3_grid.height += objeto.height
            self.screen9_parent.height += objeto.height
            self.tabla3_grid.add_widget(objeto)   
            
            
    def screen10widget(self):
        self.screen10 = Screen(name = "Screen10")
        self.pantalla_principall.add_widget(self.screen9)




    def screen2parent(self):
        self.nuevopedido = GridLayout(cols = 1, size_hint_y = None , height  = 100, pos = (Window.width,Window.height/2))
        textset3_un = ["Usar un cliente existente.","Crear un nuevo cliente.","Cancelar"]
        textset3 = []
        for i in textset3_un:
            if i == "Cancelar":
                textset3.append([6,i,0.03])
            else:
                textset3.append([6,i])
        self.MasterWidget(self.nuevopedido,textset3)
        self.add_widget(self.nuevopedido)
    def screen7parent(self):
        self.pregunta = GridLayout(cols = 1, size_hint_y = None , height  = 100, pos = (Window.width,Window.height/2))
        textset4_un = ["Desea crear un pedido con el usuario nuevo?","Si","No"]
        textset4 = []
        for i in textset4_un:
            if i == "No":
                textset4.append([6,i,0.02])
            elif i == "Si":
                textset4.append([6,i,0.04])
            else:
                textset4.append([6,i])
                
        #print textset4
        self.MasterWidget(self.pregunta,textset4)
        self.add_widget(self.pregunta)
    def Pregunda1(self):
        
        if self.state8 == 1:
            a = Animation(pos = (0,Window.height/2),d = .5, t= 'in_out_sine')
            a.start(self.pregunta)
        else:
            a = Animation(pos = (Window.width,Window.height/2),d = .5, t= 'in_out_sine')
            a.start(self.pregunta)
        self.state8 *= -1
    def buttonstate1(self,button):
        self.state1 = self.state1 * -1
        a = Animation(pos = (button.pos[0],button.pos[1]+(118*self.state1)) ,d = .4,t='in_out_back')
        a.start(button)
    def buttonstate2(self,button):
        self.state2 *= -1
        a = Animation(pos = (button.pos[0],button.pos[1]+(48*self.state2*-1)) ,d = .4,t='in_out_back')
        a.start(button)
    def topmenu(self):
        self.topmenunew = GridLayout(cols = 1, size_hint_y = None, height = 0,spacing = 0)
        self.topmenu = GridLayout(cols = 1, size_hint_y = 1)
        menusetx1 = [
        [3.04,"Inicio","Tocar para ir."],
        [3.04,"Pedido Actual","Tocar para abrir."],
        [3.04,"Entregas Realizadas","Tocar para abrir."],
        [3.04,"Inventario","Tocar para abrir."],
        [3.04,"Ventas","Cuentas por Cobrar"],
       #[3.04,"Clientes","Tocar para abrir"],
        [3.04,"Añadir Cliente","Tocar para abrir."],
        [3.04,"Recordatorios","Tocar para abrir."],
        [3.04,"Mostrar Ruta","Tocar para mostrar."],
        [3.04,"Vendedores","Tocar para mostrar."],
        [3.04,"Configuracion","Tocar para mostrar."],
        [3.04,"Ayuda","Tocar para mostrar."],
        ]
        dim_root = RelativeLayout(size_hint_y = None, height = dp(104))
        dim_root.add_widget(Image(source = color + '3.png', keep_ratio = False , allow_stretch = True))
        dim = GridLayout(rows = 1, padding = [0,33,0,0])
        dim.add_widget(Label(source =  "user-silhouette.png", keep_ratio = True, allow_stretch = False , size_hint = (None,1), width = dp(16)))
        dim.add_widget(Image(source =  "user-silhouette.png", keep_ratio = True, allow_stretch = False , size_hint = (None,1), width = dp(34)))
        self.userlabel = Button(size_hint_y = None, height = dp(71),background_normal = color + "3.png",halign = 'left',markup = True, valign = 'middle',text_size = ((Window.width*.75) -dp(55 + 25), dp(71)), text = "[b][Usuario]")
        dim.add_widget(self.userlabel)
        dim_root.add_widget(dim)
        self.topmenunew.add_widget(dim_root)
        self.MasterWidget(self.topmenunew,menusetx1) 
        self.newscroll = ScrollView()
        self.relat2 = RelativeLayout()
        
        imagerelat2A = Image(size_hint_y = .5, y = Window.height/2,source = color + "3.png", keep_ratio = False, allow_stretch = True)
        #imagerelat2B = Image(source = color + "16.png", keep_ratio = False, allow_stretch = True)
        self.relat2.add_widget(imagerelat2A)
        #self.relat2.add_widget(imagerelat2B)
        self.newscroll.add_widget(self.topmenunew)
        self.relat2.add_widget(self.newscroll)
        self.leftroot.add_widget(self.relat2)
        self.topmenunew.pos = (0,0)
        
        
    def topmenu_state(self):
        self.state5 = self.state5 * -1
        if self.state5 == -1 : self.topmenu.pos = (0,Window.height)
        if self.state5 == 1 : self.topmenu.pos = (0,Window.height-self.topmenu.height-105)
        
        a = Animation(pos = (self.topmenu.pos[0],self.topmenu.pos[1]+((self.topmenu.height+104)*self.state5)) ,d = .9,t='out_expo')
        a.start(self.topmenu)
    def MasterWidget(self,widget,texset):
        menuset2 = texset
        for i in range(len(menuset2)):

            try:
                if menuset2[i][0] == 1:
                    try:
                        guarda = menuset2[i][2]
                    except:
                        guarda = False
                        
                    dim1 = GridLayout(rows = 1,size_hint_y = None, height = 50)
                    dim1.add_widget(Button(font_size = 19,text_size = (100,60), halign = "left", valign = "middle",size_hint_y = None,size_hint_x = None, width = 150, height = 50,markup = True,text = C4+menuset2[i][1]+":", background_normal = color+"16.png"))
                    dim1.add_widget(TextInput(padding = [25,15,0,0],size_hint_y = None,size_hint_x = 1, width = 100, height = 50,markup = True,text = "", background_normal = color+"16b.png", background_active = color+"16b.png", disabled = guarda))
                    widget.add_widget(dim1)
                    widget.add_widget(Image(source = color + "16c.png", size_hint_y = None, height = 1, allow_stretch = True , keep_ratio = False))
                elif menuset2[i][0] == 2:
                    dim1 = GridLayout(rows = 1,size_hint_y = None, height = 50)
                    dim1.add_widget(ToggleButton(text_size = (Window.width/2 -50,60), halign = "center", valign = "middle",size_hint_y = None,size_hint_x = 1, width = 150, height = 50,markup = True,text = "[b]"+C4+menuset2[i][1]+"", background_normal = color+"16.png",background_down = color+"1.png",group = "a"))
                    dim1.add_widget(ToggleButton(text_size = (Window.width/2 -50,60), halign = "center", valign = "middle",size_hint_y = None,size_hint_x = 1, width = 150, height = 50,markup = True,text = "[b]"+C4+menuset2[i][2]+"", background_normal = color+"16.png",background_down = color+"1.png",group = "a"))
                    widget.add_widget(dim1)
                    widget.add_widget(Image(source = color + "16c.png", size_hint_y = None, height = 1, allow_stretch = True , keep_ratio = False))
                elif menuset2[i][0] == 3:
                    dim1 = GridLayout(rows = 1,size_hint_y = None, height = 50)
                    dim1.add_widget(Button(font_size = 19,markup = True,text = menuset2[i][1],background_normal = color +"3.png", slide_hint_y = None, height = 50))
                    widget.add_widget(dim1)
                    widget.add_widget(Image(source = color + "16c.png", size_hint_y = None, height = 1, allow_stretch = True , keep_ratio = False))                    
                elif menuset2[i][0] == "buscador":
                    dim1 = RelativeLayout(size_hint_y = None, height = 52)
                    dim1.add_widget(Image(source = color+"16.png", allow_stretch = True , keep_ratio = False))
                    
                    dim1b = GridLayout(rows = 1 , size_hint_y = None , height = 50)
                    dim1b.add_widget(Label(size_hint_x = None, width = ((Window.width-382)/2)))
                    
                    dim1b.add_widget(Button(border = [0,0,0,0],background_normal = asset+"1.png",background_down = asset+"1.png",size_hint_x = None, width = 64))
                    textwidget = TextInput(multiline=False,size_hint_x = None, width =254,font_size = 16, hint_text = menuset2[i][1],padding = [0,dp(18),0,0],background_normal = asset+"2.png",background_active = asset+"2.png")
                    dim1b.add_widget(textwidget)
                    dim1b.add_widget(Button(border = [0,0,0,0],background_normal = asset+"3.png",background_down = asset+"3.png",size_hint_x = None, width = 64))
                    
                    image1_parent = RelativeLayout(cols = 1, size_hint = (None,None), size = (50,50))
                    dim1b.add_widget(image1_parent)
                    dim1b.add_widget(Label(size_hint_x = None, width = ((Window.width-382)/2)))
                    
                    dim1.add_widget(Image(pos_hint = {'y': 1},opacity = .12,source = color + "3.png", keep_ratio = False , allow_stretch = True, size_hint_y = None, height = dp(1)))
                    dim1.add_widget(dim1b)
                    dim1.add_widget(Image(source = color + "3.png",opacity = .12, keep_ratio = False , allow_stretch = True, size_hint_y = None, height = dp(1)))
                    try:
                        if menuset2[i][1] == "Buscar Cliente": textwidget.bind(on_text_validate = lambda x: self.Filtrar(3,x.text))
                        elif menuset2[i][1] == "Buscar Pedido": textwidget.bind(on_text_validate = lambda x: self.Filtrar(0,x.text))
                        elif menuset2[i][1] == "Buscar en Inventario": textwidget.bind(on_text_validate = lambda x: self.Filtrar(4,x.text))
                    except:
                        import traceback
                        traceback.print_exc()
                        
                    widget.add_widget(Image(source = color + "16.png", height = 25,size_hint_y = None, keep_ratio= False, allow_stretch = True))
                    widget.add_widget(dim1)
                    widget.add_widget(Image(source = color + "16.png", height = 25,size_hint_y = None, keep_ratio= False, allow_stretch = True))
                    
                elif menuset2[i][0] == 3.04:
                    dim1 = GridLayout(rows = 1,size_hint_y = None, height = dp(56), spacing = 0)
                    dim1a = RelativeLayout(size_hint_x = None , width = 75 )
                    dim1a.add_widget(Image(source = color+"16.png",size_hint_x = None , width = 75 ))
                    dim1a.add_widget(Image(source = icon+"folder-11.png",size = (40,40) ,size_hint = (None,None),pos = (75/2 -20,75/2 -20)))
                    
                    dim1_dim = GridLayout(cols = 1)
                    #dim1.add_widget(dim1a)
                    dim1.add_widget(dim1_dim)
                   
                    button5 = Button(text_size = ((Window.width*.75)-dp(80),75),valign = "middle",font_size = 16,background_normal = "16.png", text = C4+menuset2[i][1]+'\n'+"[size=13sp]"+menuset2[i][2],markup = True)
                    dim1_dim.add_widget(button5)
                    widget.height += 74
                    widget.add_widget(dim1)
                    widget.add_widget(Image(opacity = 1,source = color + "16bb.png", size_hint_y = None, height = 1, allow_stretch = True , keep_ratio = False))
                    if menuset2[i][1] == "Ventas": button5.bind(on_release = lambda x: self.current("screen5"))#Screen3
                    if menuset2[i][1] == "Clientes": button5.bind(on_release = lambda x: self.current("screen5"))
                    if menuset2[i][1] == "Inventario": button5.bind(on_release = lambda x: self.current("screen9"))
                    if menuset2[i][1] == "Inicio": button5.bind(on_release = lambda x: self.current("b"))
                    if menuset2[i][1] == "Pedido Actual": button5.bind(on_release = lambda x: self.current("shopcart"))
                    if menuset2[i][1] == "Añadir Cliente": button5.bind(on_release = lambda x: self.current("dimCliente"))
                    if menuset2[i][1] == "Mostrar Ruta": button5.bind(on_release = lambda x: self.anim_hstate_root())
                    if menuset2[i][1] == "Mostrar Ruta": button5.bind(on_release = lambda x: self.current("b"))
                    if menuset2[i][1] == "Configuracion": button5.bind(on_release = lambda x: self.current("config"))
                    if menuset2[i][1] == "Recordatorios": button5.bind(on_release = lambda x: self.current("recordatorio"))
                    if menuset2[i][1] == "Entregas Realizadas": button5.bind(on_release = lambda x: self.current("entregas"))
                    if menuset2[i][1] == "Vendedores": button5.bind(on_release = lambda x: self.current("vendedores"))
                    self.acciones.append(button5)
                elif menuset2[i][0] == 3.05:
                    dim1 = GridLayout(rows = 1,size_hint_y = None, height = 74, spacing = 0)
                    dim1a = RelativeLayout(size_hint_x = None , width = 75 )
                    dim1a.add_widget(Image(source = color+"16.png",size_hint_x = None , width = 75 ))
                    dim1a.add_widget(Image(source = icon+"briefcase.png",size = (40,40) ,size_hint = (None,None),pos = (75/2 -20,75/2 -20)))
                    dim1_dim = GridLayout(cols = 1,size_hint_y = None , height =75)
                    dim1.add_widget(dim1a)
                    dim1.add_widget(dim1_dim)
                    dim1_dim.add_widget(Button(text_size = (Window.width-75,75),valign = "middle",font_size = 16,background_normal = "16.png", text = C4+menuset2[i][1]+'\n[b]'+"[size=15]"+menuset2[i][2],markup = True))
                    
                    #dim1_dim.add_widget(Button(text_size = (Window.width-75,75/2),valign = "top", font_size = 17,background_normal = "16.png", text = C4+"texto",markup = True))
                    

                    widget.add_widget(dim1)
                    widget.add_widget(Image(source = color + "16c.png", size_hint_y = None, height = 1, allow_stretch = True , keep_ratio = False))
                elif menuset2[i][0] == 3.06:
                    dim1 = GridLayout(cols = 1, size_hint_y = None , height = 65)
                    dim1.add_widget(Button(size_hint_y= None, text_size = (200,65), text = "Objeto\nx"))
                    widget.add_widget(dim1)
                    widget.add_widget(Image(source = color + "16c.png", size_hint_y = None, height = 1, allow_stretch = True , keep_ratio = False))
                
                elif menuset2[i][0] == 3.03:
                    dim1 = GridLayout(rows = 1,size_hint_y = None, height = 50)
                    dim1.add_widget(Button(font_size = 16,markup = True,text =C4+ menuset2[i][1],background_normal = color +menuset2[i][2]+".png", slide_hint_y = None, height = 50))
                    widget.add_widget(dim1)
                    widget.add_widget(Image(source = color + "16c.png", size_hint_y = None, height = 1, allow_stretch = True , keep_ratio = False))
                elif menuset2[i][0] == 3.01:
                    dim1 = GridLayout(rows = 1,size_hint_y = None, height = 100)
                    dim1.add_widget(Button(font_size = 19,markup = True, text_size = (Window.width/2 -50,100) ,valign = "middle", halign = "left",text = menuset2[i][1],background_normal = color +"3.png", slide_hint_y = None, height = 100))
                    widget.add_widget(dim1)
                elif menuset2[i][0] == 3.02:
                    dim1 = GridLayout(rows = 1,size_hint_y = None, height = 50)
                    dim1.add_widget(Button(font_size = 19,markup = True,text = menuset2[i][1],background_normal = color +"3.png", slide_hint_y = None, height = 50))
                    widget.add_widget(dim1)
                elif menuset2[i][0] == "b":
                    
                    bar = Image(source = color+menuset2[i][2]+".png", size_hint_y = None, height = 1 )
                    widget.add_widget(bar)
                elif menuset2[i][0] == 4:

                    dim1 = GridLayout(rows = 1,size_hint_y = None, height = 50)
                    dim1.add_widget(Button(font_size = 19,text_size = (100,60), halign = "left", valign = "middle",size_hint_y = None,size_hint_x = None, width = 150, height = 50,markup = True,text = C4+menuset2[i][1]+":", background_normal = color+"16.png"))
                    
                    TextInput1 =TextInput(padding = [25,15,0,0],size_hint_y = None,size_hint_x = 1, width = 100, height = 50,markup = True,text = "", background_normal = color+"16b.png", background_active = color+"16b.png")
                    dim1.add_widget(TextInput1)
                    
                    ToggleButton1 = ToggleButton(font_size = 0,text_size = (50,50),group = "x", halign = "left", valign = "middle",size_hint_y = None,size_hint_x = None, width = 50, height = 50,markup = True,text = str(menuset2[i][2]), background_normal = color+"16.png", background_down = color+"7.png")
                    self.rangodetexto_cond4.append(TextInput1)
                    ToggleButton1.bind(on_press = lambda x :self.in_state(x.text))
                    dim1.add_widget(ToggleButton1)
                    
                    widget.add_widget(dim1)
                    widget.add_widget(Image(source = color + "16c.png", size_hint_y = None, height = 1, allow_stretch = True , keep_ratio = False))
                elif menuset2[i][0] == 5:
                        
                    dim1 = GridLayout(rows = 1,size_hint_y = None, height = 50)
                    Button6 = Button(font_size = 19,text_size = (100,60), halign = "left", valign = "middle",size_hint_y = None,size_hint_x = 1, width = 150, height = 50,markup = True,text = C4+"Ingresar", background_normal = color+"16b.png", background_down = color+"16b.png")
                    dim1.add_widget(Button6)
                    Button6.bind(on_release = lambda x:self.Main_Removewidget())
                    dim1.add_widget(Button(font_size = 19,text_size = (100,60), halign = "left", valign = "middle",size_hint_y = None,size_hint_x = 1, width = 150, height = 50,markup = True,text = C4+"Salir", background_normal = color+"1.png", background_down = color+"1.png"))
                    widget.add_widget(dim1)
                elif menuset2[i][0] == 7: 
                    dim1_image = Image(size_hint_y = None , height = 20 , source = barra+"barra1.png", keep_ratio = False, allow_stretch = True)
                    widget.add_widget(dim1_image)
                elif menuset2[i][0] == 7.01: 
                    dim1_image = Image(size_hint_y = None , height = 20 , source = barra+"barra2.png", keep_ratio = False, allow_stretch = True)
                    widget.add_widget(dim1_image)
                elif menuset2[i][0] == 6: 
                    
                    dim1 = GridLayout(cols =1,height=50,size_hint_y=None)
                    button6 =Button(font_size = 19,text = C4+menuset2[i][1],text_size = def_textsize, valign = "middle",markup = True,background_normal = color + "16.png")
                    dim1.add_widget(button6)
                    widget.add_widget(dim1)
                    
                    try:    
                        if menuset2[i][2] == 0.01:
                            button6.bind(on_release = lambda x: self.Nuevopedido())

                        elif menuset2[i][2] == 0.02:
                            print ("asdasdasd")
                            button6.bind(on_release = lambda x: self.Pregunda1())
                        elif menuset2[i][2] == 0.03:
                            print ("asdasdasd")
                            button6.bind(on_release = lambda x: self.Nuevopedido())
                        elif menuset2[i][2] == 0.04:
                            print ("asdasdasd")
                            button6.bind(on_release = lambda x: self.PedidoETC1())
                        
                        
                    
     
                    except:
                        pass
                elif menuset2[i][0] == 6.01: 
                    dim1 = GridLayout(rows =1,height=50,size_hint_y=None)
                    dim1.add_widget(Button(font_size = 19,text = C4+menuset2[i][1],text_size = (Window.width/2 -50,50), valign = "middle",markup = True,background_normal = color + "16.png"))
                    adjev = Button(font_size = 19,text = C4+menuset2[i][2],text_size =(100,50) ,size_hint_x = None, width = 100,halign = "center", valign = "middle",markup = True,background_normal = color + "6.png")
                    dim1.add_widget(adjev)
                    widget.add_widget(dim1)
                    adjev.bind(on_release = lambda x: self.adjetivo())
                else:
                    
                    Button1 =Button(size_hint_y = None, height = 50,markup = True,text =C4+ menuset2[i], background_normal = color+"16.png", background_down = color+"16.png")
                    widget.add_widget(Button1)
                    widget.height += 50
                    if menuset2[i] == "Realizar Busqueda":
                        Button1.bind(on_release = lambda x:self.filtrar_tabla(0,int(self.state4),self.rangodetexto_cond4))                                       
            except Exception as e:
                import traceback
                traceback.print_exc()
                #print str(e)
                #
                Button1 =Button(size_hint_y = None, height = 50,markup = True,text =C4+ menuset2[i], background_normal = color+"16.png", background_down = color+"16.png")
                widget.add_widget(Button1)
    
    def set_FiltrarCampo(self, Tabla, CampoX):
        
        self.tablasfilter[Tabla] = CampoX
        #print self.tablasfilter[Tabla] 
        
    def Filtrar_entrefechas(self):
        
        self.tablasroot[0].clear_widgets()
        self.tablasroot[0].height = 300
        for i in self.temp[0][0]:
            valores = i['emision'][:10].split('-')
            valor = (int(valores[1]),int(valores[2]))
            print (self.calendar_0.date0 , valor , self.calendar_0.date1)
            print valor 
            if (self.calendar_0.date0 < valor < self.calendar_0.date1):
                self.MasterViews(self.tabla0_grid,[[0,"a"]])
                
                #self.tabla0_grid.add_widget(Image(size_hint_y = None , height = 1, source = color + "16b.png", keep_ratio= False , allow_stretch = True))
                pariente_parent = RelativeLayout(size_hint_y = None, height = dp(74))
                pariente_dim = GridLayout(cols = 2, spacing = 0, padding = [0,0,0,0])
                pariente_dim.add_widget(Image(size_hint_x = None, width = dp(56), keep_ratio = False, allow_stretch = False, opacity = .54, source = asset + "ic_account_balance_black_36px.png"))
                pariente = GridLayout(cols = 2, spacing = 0, padding = [0,0,0,0])
                pariente_dim.add_widget(pariente)
                pariente.add_widget(Label(text_size = ((Window.width/2) - dp(25) - dp(56), dp(74/2)),valign = 'middle',halign = 'left' ,text = C4 + "[b]" + str(self.temp[3][0][int(i["cliente"]) - 1]["cliente"]),markup = True,))
                pariente.add_widget(Label(text_size = ((Window.width/2) - dp(25) - dp(56), dp(74/2)),valign = 'middle',halign = 'left' ,text = C4 + i["emision"][:10],markup = True,))
                pariente.add_widget(Label(text_size = ((Window.width/2) - dp(25) - dp(56), dp(74/2)),valign = 'middle',halign = 'left' ,text = C4 + "[b]" + i["no_factura"],markup = True,))
                pariente.add_widget(Label(text_size = ((Window.width/2) - dp(25) - dp(56), dp(74/2)),valign = 'middle',halign = 'left' ,text = C5 + i["vencto"][:10],markup = True,))
                pariente_parent.add_widget(pariente_dim)
                self.tabla0_grid.add_widget(pariente_parent)
                self.tabla0_grid.add_widget(Image(size_hint_y = None , height = 1, source = color + "16b.png", keep_ratio= False , allow_stretch = True))
    def Filtrar(self, Tabla, Valor):
        def calcular_suma(val1):
            calcx = 0
            for dim in self.temp[0][0]:
                if val1 == dim["cliente"]:
                    calcx += float(dim["balance_original"])
            return str(calcx)
        try:
            print("Filtrar")
            
            print Tabla, self.tablasfilter[Tabla], Valor
            datos = self.Armando.filtrar(Tabla,self.tablasfilter[Tabla],Valor)
            self.tablasroot[Tabla].clear_widgets()
            self.tablasroot[Tabla].height = 300

            for i in datos:
                if Tabla == 0:
                    self.MasterViews(self.tabla0_grid,[[0,"a"]])
                    
                    #self.tabla0_grid.add_widget(Image(size_hint_y = None , height = 1, source = color + "16b.png", keep_ratio= False , allow_stretch = True))
                    pariente_parent = RelativeLayout(size_hint_y = None, height = dp(74))
                    pariente_dim = GridLayout(cols = 2, spacing = 0, padding = [0,0,0,0])
                    pariente_dim.add_widget(Image(size_hint_x = None, width = dp(56), keep_ratio = False, allow_stretch = False, opacity = .54, source = asset + "ic_account_balance_black_36px.png"))
                    pariente = GridLayout(cols = 2, spacing = 0, padding = [0,0,0,0])
                    pariente_dim.add_widget(pariente)
                    pariente.add_widget(Label(text_size = ((Window.width/2) - dp(25) - dp(56), dp(74/2)),valign = 'middle',halign = 'left' ,text = C4 + "[b]" + str(self.temp[3][0][int(i["cliente"]) - 1]["cliente"]),markup = True,))
                    pariente.add_widget(Label(text_size = ((Window.width/2) - dp(25) - dp(56), dp(74/2)),valign = 'middle',halign = 'left' ,text = C4 + i["emision"][:10],markup = True,))
                    pariente.add_widget(Label(text_size = ((Window.width/2) - dp(25) - dp(56), dp(74/2)),valign = 'middle',halign = 'left' ,text = C4 + "[b]" + i["no_factura"],markup = True,))
                    pariente.add_widget(Label(text_size = ((Window.width/2) - dp(25) - dp(56), dp(74/2)),valign = 'middle',halign = 'left' ,text = C5 + i["vencto"][:10],markup = True,))
                    pariente_parent.add_widget(pariente_dim)
                    self.tabla0_grid.add_widget(pariente_parent)
                    self.tabla0_grid.add_widget(Image(size_hint_y = None , height = 1, source = color + "16b.png", keep_ratio= False , allow_stretch = True))


                    self.tabla0_grid.height += 74
                elif Tabla == 3:
                    def managinx(x,y):
                        print x,y
                        self.screen5sc.current = y
                    client = ClientShow(opacity = 0,item = i, temp = self.temp, managing = managinx)
                    self.tabla2_grid.add_widget(client)
                    self.tabla2_grid.height += 290
                    a = Animation(opacity = 1 , d = .5 , t = 'out_quad')
                    a.start(client)
                elif Tabla == 4:
                    #Marca,Descripcion,clasificacion, precio_1, precio_2,precio_3
                    objeto = StockItem(i["marca"]+"[/b] "+i["item_name"],i["descripcion"],i["clasificacion"],i["precio_1"],i["precio_2"],i["precio_3"],item = i,opacity = 0)
                    #objeto.returntext().text = C4+"[b]"+i["marca"]+"[/b]\n"+i["descripcion"]+"\n\n[b]"+i["precio_1"]+" RD$"
                    objeto.returntext().line_height = 1
                    objeto.returntext().font_size = 16
                    objeto.getbehavior().bind(on_release = lambda x: objeto.actualizarcantidad())
                    objeto.getbehavior().bind(on_release = lambda x: self.shopcart.agregarcarrito(objeto.marca,objeto.descripcion,objeto.clasificacion,objeto.precio_1,objeto.precio_2,objeto.precio_3,objeto.unidades, item = x.parent.parent.item))
                    objeto.returncuanty().bind(on_release = lambda x: self.manymenu(x,objeto))

                    self.tabla3_grid.height += objeto.height
                    self.screen9_parent.height += objeto.height
                    self.tabla3_grid.add_widget(objeto)
                    a = Animation(opacity = 1 , d = .5 , t = 'out_quad')
                    a.start(objeto)                    

                else:
                    pass
        except:
            import traceback
            traceback.print_exc()

            
    def MasterViews(self,widget,index):
        try:    
            for i in index: 
                if i[0] == 0:
                    childwidget = GridLayout(rows = 1,size_hint_y = None, height = 81)
                    childwidget.add_widget(Image(source= color + "16.png",allow_stretch = True, keep_ratio = False))
                    childwidget.add_widget(Image(source = asset + "cxcview/1.png", size_hint_x = None, width = 79))
                    childwidget.add_widget(Button(font_size = 20,markup = True,text = i[1],background_normal = asset + "cxcview/2.png", size_hint_x = None, width = 102))
                    childwidget.add_widget(Button(font_size = 20,markup = True,text = i[2],background_normal = asset + "cxcview/3.png", size_hint_x = None, width = 120))
                    button8 = Button(font_size = 30,markup = True,text= C4+">",background_normal = asset + "cxcview/4.png", size_hint_x = None, width = 51)
                    childwidget.add_widget(button8)
                    childwidget.add_widget(Image(source= color + "16.png",allow_stretch = True, keep_ratio = False))
                    widget.add_widget(childwidget)
                    widget.height += 81
                    button8.bind(on_release = lambda x: self.current("Screen4"))
                if i[0] == 0.01:
                   childwidget = GridLayout(rows =1, height = 50, size_hint_y = None)
                   #childwidget.add_widget(Image(source = asset  + "2.png",size_hint_x = 1, keep_ratio = False, allow_stretch = True))
                   #childwidget.add_widget(Image(source = asset + "1.png",size_hint_x = None, width = 60))
                   childwidget.add_widget(Button(font_size = 16,markup = True, text = C4+"[b]Objeto",background_normal = color + "16bb.png",size_hint_x = 1, width = 121))
                   #childwidget.add_widget(Image(source = asset + "3.png",size_hint_x = None, width = 52))
                   childwidget.add_widget(Button(font_size = 16,markup = True, text = C4+"5 Unidades",background_normal = color + "16bb.png",size_hint_x = 1, width = 97))
                   childwidget.add_widget(Button(font_size = 16,markup = True, text = C4+"200.00 [b]RD$",background_normal = color + "16bb.png",size_hint_x = 1, width = 97))
                   childwidget.add_widget(Button(font_size = 16,markup = True, text = C4+"1000.00 [b]RD$",background_normal = color + "16bb.png",size_hint_x = 1, width = 97))
                   #childwidget.add_widget(Image(source = asset  + "2.png",size_hint_x = 1, keep_ratio = False, allow_stretch = True))
                   widget.add_widget(childwidget)
                if i[0] == 0.02:
                    try:
                        v1,v2,v3,v4 = i[1],i[2],i[3],i[4]
                    except:
                        v1,v2,v3,v4 = "","","",""
        
                    childwidget = GridLayout(rows = 1, size_hint_y = None, height = 153)
                    childwidget.add_widget(Image(source = asset  + "screen5/3.png",size_hint_x = 1, keep_ratio = False, allow_stretch = True))
                    childwidget_parent = GridLayout(cols = 1,size_hint_x = None , width = 353,spacing = 0)
                    button7 = Button(font_size = 16,text_size = (353,65), valign = "middle",size_hint_y = None,markup = True,text = C2+v1+" | "+v2, height = 65, background_normal = asset +"screen5/1.png")
                    childwidget_parent.add_widget(button7)
                    childwidget_parent.add_widget(Button(font_size = 16,text_size = (353,88), valign = "top",size_hint_y = None,markup = True, text = C2+v3+"\n       "+v4+" RD$", height = 88,background_normal = asset +"screen5/2.png"))
                    childwidget.add_widget(childwidget_parent)
                    childwidget.add_widget(Image(source = asset  + "screen5/3.png",size_hint_x = 1, keep_ratio = False, allow_stretch = True))
                    widget.add_widget(childwidget)
                    button7.bind(on_release = lambda x: self.current("screen6"))
                   
        except:
            pass
    def backspace(self): 
        a = len(self.historial)
        self.pantalla_principall.current = self.historial[a-(2+self.backcount)]
        self.backcount += 2
        #print self.historial[a-(2+self.backcount)] 
        self.historial.append(self.pantalla_principall.current)
        if self.pantalla_principall.current == "b" : 
            if self.state5 == 1:self.topmenu_state()
            if self.state1 == 1:self.buttonstate1(self.button1.parent.parent)
            if self.state2 == 1:self.buttonstate2(self.button2.parent.parent)
        else:
            if self.state5 == -1:self.topmenu_state()
            if self.state1 == -1:self.buttonstate1(self.button1.parent.parent)
            if self.state2 == -1:self.buttonstate2(self.button2.parent.parent)   
            



     

    def start(self, minTime, minDistance):
        gps.start()
    def stop(self):
        gps.stop()
    @mainthread
    def on_location(self, **kwargs):
        self.gps_location = '\n'.join([
            '{}={}'.format(k, v) for k, v in kwargs.items()])
            
        a = '\n'.join([
            '{}={}'.format(k, v) for k, v in kwargs.items()])
        for k, v in kwargs.items():
            if (k == "lon") or (k == "lat"):
                print str(k)+"="+str(v)
        self.shopcart.returnmappos().text = C4 + self.gps_location
        self.crearusuario_screen.input13.input0.text = C4 + self.gps_location
    @mainthread
    def on_status(self, stype, status):
        self.gps_status = 'type={}\n{}'.format(stype, status)
        self.shopcart.returnmappos().text = C4 + self.gps_location
        self.crearusuario_screen.input13.input0.text = C4 + self.gps_location
    @mainthread
    def on_pause(self):
        gps.stop()
        return True
    def on_resume(self):
        gps.start(1000, 0)
        pass
        
        
        


    def data_base_connecttions(self,**kwargs):
        data_connect = self.Armando
        print ("\n")*5
        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(kwargs["jsondata"]) 
        print ("\n")*5        
        data_connect.insertar(kwargs["tableid"],kwargs["jsondata"])
        








class MyApp(App):
    def build(self):
        return InterfaceManager()
 

if __name__ in ('__main__', '__android__'):
    MyApp().run()

    
    
    
    
    