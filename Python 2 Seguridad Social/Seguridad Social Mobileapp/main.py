from behave.__init__ import *
import os   
import os.path
from plyer import gps
os.environ['KIVY_TEXT'] = 'pil'
#Window.size = (360,640)
Window.clearcolor = (1,1,1,1)
#CARPETAS DEL PROYECTO
patch = os.path.dirname(os.path.abspath(__file__))
asset = patch + '/behave/assets/drawable-mdpi/'
color = patch + '/behave/colors/'
font = patch + '/behave/fonts/'
from kivy.garden.mapview import MapView, MapMarker, MarkerMapLayer, MapSource, MapLayer,MapMarkerPopup


Builder.load_string('''
<NavigationDrawer>:
    size_hint: (1,1)
    _side_panel: sidepanel
    _main_panel: mainpanel
    _join_image: joinimage
    side_panel_width: '100dp'
    BoxLayout:
        id: sidepanel
        y: root.y
        x: root.x - \
           (1-root._anim_progress)* \
           root.side_panel_init_offset*root.side_panel_width
        height: root.height
        width: root.side_panel_width
        opacity: root.side_panel_opacity + \
                 (1-root.side_panel_opacity)*root._anim_progress
        canvas:
            Color:
                rgba: (1,1,1,.04)
            Rectangle:
                pos: self.pos
                size: self.size
        canvas.after:
            Color:
                rgba: (1,1,1,(1-root._anim_progress)*root.side_panel_darkness)
            Rectangle:
                size: self.size
                pos: self.pos
    BoxLayout:
        id: mainpanel
        x: root.x + \
           root._anim_progress * \
           root.side_panel_width * \
           root.main_panel_final_offset
        y: root.y
        size: root.size
        canvas:
            Color:
                rgba: (0,0,0,1)
            Rectangle:
                pos: self.pos
                size: self.size
        canvas.after:
            Color:
                rgba: (0,0,0,root._anim_progress*root.main_panel_darkness)
            Rectangle:
                size: self.size
                pos: self.pos
    Image:
        id: joinimage
        opacity: min(sidepanel.opacity, 0 if root._anim_progress < 0.00001 \
                 else min(root._anim_progress*40,1))
        source: root._choose_image(root._main_above, root.separator_image)
        mipmap: False
        width: 1
        height: root._side_panel.height
        x: (mainpanel.x - self.width + 1) if root._main_above \
           else (sidepanel.x + sidepanel.width - 1)
        y: root.y
        allow_stretch: True
        keep_ratio: False
''')
class NavigationDrawerException(Exception):
    '''Raised when add_widget or remove_widget called incorrectly on a
    NavigationDrawer.

    '''

class NavigationDrawer(StencilView):

    # Internal references for side, main and image widgets
    _side_panel = ObjectProperty()
    _main_panel = ObjectProperty()
    _join_image = ObjectProperty()

    side_panel = ObjectProperty(None, allownone=True)
    main_panel = ObjectProperty(None, allownone=True)


    # Appearance properties
    side_panel_width = NumericProperty()

    separator_image = StringProperty('')


    # Touch properties
    touch_accept_width = NumericProperty('14dp')
    _touch = ObjectProperty(None, allownone=True)  # The currently active touch

    # Animation properties
    state = OptionProperty('closed', options=('open', 'closed'))
    anim_time = NumericProperty(0.3)
    min_dist_to_open = NumericProperty(0.7)
    _anim_progress = NumericProperty(0)  # Internal state controlling
                                         # widget positions
    _anim_init_progress = NumericProperty(0)

    # Animation controls
    top_panel = OptionProperty('main', options=['main', 'side'])
    _main_above = BooleanProperty(True)

    side_panel_init_offset = NumericProperty(0.5)

    side_panel_darkness = NumericProperty(0.8)

    side_panel_opacity = NumericProperty(1)

    main_panel_final_offset = NumericProperty(1)

    main_panel_darkness = NumericProperty(0)

    opening_transition = StringProperty('out_cubic')

    closing_transition = StringProperty('in_cubic')

    anim_type = OptionProperty('reveal_from_below',
                               options=['slide_above_anim',
                                        'slide_above_simple',
                                        'fade_in',
                                        'reveal_below_anim',
                                        'reveal_below_simple',
                                        ])

    def __init__(self, **kwargs):
        super(NavigationDrawer, self).__init__(**kwargs)
        Clock.schedule_once(self.on__main_above, 0)

    def on_anim_type(self, *args):
        anim_type = self.anim_type
        if anim_type == 'slide_above_anim':
            self.top_panel = 'side'
            self.side_panel_darkness = 0
            self.side_panel_opacity = 1
            self.main_panel_final_offset = 0.5
            self.main_panel_darkness = 0.5
            self.side_panel_init_offset = 1
        if anim_type == 'slide_above_simple':
            self.top_panel = 'side'
            self.side_panel_darkness = 0
            self.side_panel_opacity = 1
            self.main_panel_final_offset = 0
            self.main_panel_darkness = 0
            self.side_panel_init_offset = 1
        elif anim_type == 'fade_in':
            self.top_panel = 'side'
            self.side_panel_darkness = 0
            self.side_panel_opacity = 0
            self.main_panel_final_offset = 0
            self.main_panel_darkness = 0
            self.side_panel_init_offset = 0.5
        elif anim_type == 'reveal_below_anim':
            self.top_panel = 'main'
            self.side_panel_darkness = 0.8
            self.side_panel_opacity = 1
            self.main_panel_final_offset = 1
            self.main_panel_darkness = 0
            self.side_panel_init_offset = 0.5
        elif anim_type == 'reveal_below_simple':
            self.top_panel = 'main'
            self.side_panel_darkness = 0
            self.side_panel_opacity = 1
            self.main_panel_final_offset = 1
            self.main_panel_darkness = 0
            self.side_panel_init_offset = 0

    def on_top_panel(self, *args):
        if self.top_panel == 'main':
            self._main_above = True
        else:
            self._main_above = False

    def on__main_above(self, *args):
        newval = self._main_above
        main_panel = self._main_panel
        side_panel = self._side_panel
        self.canvas.remove(main_panel.canvas)
        self.canvas.remove(side_panel.canvas)
        if newval:
            self.canvas.insert(0, main_panel.canvas)
            self.canvas.insert(0, side_panel.canvas)
        else:
            self.canvas.insert(0, side_panel.canvas)
            self.canvas.insert(0, main_panel.canvas)

    def toggle_main_above(self, *args):
        if self._main_above:
            self._main_above = False
        else:
            self._main_above = True

    def add_widget(self, widget):
        if len(self.children) == 0:
            super(NavigationDrawer, self).add_widget(widget)
            self._side_panel = widget
        elif len(self.children) == 1:
            super(NavigationDrawer, self).add_widget(widget)
            self._main_panel = widget
        elif len(self.children) == 2:
            super(NavigationDrawer, self).add_widget(widget)
            self._join_image = widget
        elif self.side_panel is None:
            self._side_panel.add_widget(widget)
            self.side_panel = widget
        elif self.main_panel is None:
            self._main_panel.add_widget(widget)
            self.main_panel = widget
        else:
            raise NavigationDrawerException(
                'Can\'t add more than two widgets'
                'directly to NavigationDrawer')

    def remove_widget(self, widget):
        if widget is self.side_panel:
            self._side_panel.remove_widget(widget)
            self.side_panel = None
        elif widget is self.main_panel:
            self._main_panel.remove_widget(widget)
            self.main_panel = None
        else:
            raise NavigationDrawerException(
                'Widget is neither the side or main panel, can\'t remove it.')

    def set_side_panel(self, widget):
        '''Removes any existing side panel widgets, and replaces them with the
        argument `widget`.
        '''
        # Clear existing side panel entries
        if len(self._side_panel.children) > 0:
            for child in self._side_panel.children:
                self._side_panel.remove(child)
        # Set new side panel
        self._side_panel.add_widget(widget)
        self.side_panel = widget

    def set_main_panel(self, widget):
        '''Removes any existing main panel widgets, and replaces them with the
        argument `widget`.
        '''
        # Clear existing side panel entries
        if len(self._main_panel.children) > 0:
            for child in self._main_panel.children:
                self._main_panel.remove(child)
        # Set new side panel
        self._main_panel.add_widget(widget)
        self.main_panel = widget

    def on__anim_progress(self, *args):
        if self._anim_progress > 1:
            self._anim_progress = 1
        elif self._anim_progress < 0:
            self._anim_progress = 0
        if self._anim_progress >= 1:
            self.state = 'open'
        elif self._anim_progress <= 0:
            self.state = 'closed'

    def on_state(self, *args):
        Animation.cancel_all(self)
        if self.state == 'open':
            self._anim_progress = 1
        else:
            self._anim_progress = 0

    def anim_to_state(self, state):
        '''If not already in state `state`, animates smoothly to it, taking
        the time given by self.anim_time. State may be either 'open'
        or 'closed'.

        '''
        if state == 'open':
            anim = Animation(_anim_progress=1,
                             duration=self.anim_time,
                             t=self.closing_transition)
            anim.start(self)
        elif state == 'closed':
            anim = Animation(_anim_progress=0,
                             duration=self.anim_time,
                             t=self.opening_transition)
            anim.start(self)
        else:
            raise NavigationDrawerException(
                'Invalid state received, should be one of `open` or `closed`')

    def toggle_state(self, animate=True):
        '''Toggles from open to closed or vice versa, optionally animating or
        simply jumping.'''
        if self.state == 'open':
            if animate:
                self.anim_to_state('closed')
            else:
                self.state = 'closed'
        elif self.state == 'closed':
            if animate:
                self.anim_to_state('open')
            else:
                self.state = 'open'

    def on_touch_down(self, touch):
        col_self = self.collide_point(*touch.pos)
        col_side = self._side_panel.collide_point(*touch.pos)
        col_main = self._main_panel.collide_point(*touch.pos)

        if self._anim_progress < 0.001:  # i.e. closed
            valid_region = (self.x <=
                            touch.x <=
                            (self.x + self.touch_accept_width))
            if not valid_region:
                self._main_panel.on_touch_down(touch)
                return False
        else:
            if col_side and not self._main_above:
                self._side_panel.on_touch_down(touch)
                return False
            valid_region = (self._main_panel.x <=
                            touch.x <=
                            (self._main_panel.x + self._main_panel.width))
            if not valid_region:
                if self._main_above:
                    if col_main:
                        self._main_panel.on_touch_down(touch)
                    elif col_side:
                        self._side_panel.on_touch_down(touch)
                else:
                    if col_side:
                        self._side_panel.on_touch_down(touch)
                    elif col_main:
                        self._main_panel.on_touch_down(touch)
                return False
        Animation.cancel_all(self)
        self._anim_init_progress = self._anim_progress
        self._touch = touch
        touch.ud['type'] = self.state
        touch.ud['panels_jiggled'] = False  # If user moved panels back
                                            # and forth, don't default
                                            # to close on touch release
        touch.grab(self)
        return True

    def on_touch_move(self, touch):
        if touch is self._touch:
            dx = touch.x - touch.ox
            self._anim_progress = max(0, min(self._anim_init_progress +
                                            (dx / self.side_panel_width), 1))
            if self._anim_progress < 0.975:
                touch.ud['panels_jiggled'] = True
        else:
            super(NavigationDrawer, self).on_touch_move(touch)
            return

    def on_touch_up(self, touch):
        if touch is self._touch:
            self._touch = None
            init_state = touch.ud['type']
            touch.ungrab(self)
            jiggled = touch.ud['panels_jiggled']
            if init_state == 'open' and not jiggled:
                if self._anim_progress >= 0.975:
                        self.anim_to_state('closed')
                else:
                    self._anim_relax()
            else:
                self._anim_relax()
        else:
            super(NavigationDrawer, self).on_touch_up(touch)
            return

    def _anim_relax(self):
        '''Animates to the open or closed position, depending on whether the
        current position is past self.min_dist_to_open.

        '''
        if self._anim_progress > self.min_dist_to_open:
            self.anim_to_state('open')
        else:
            self.anim_to_state('closed')

    def _choose_image(self, *args):
        '''Chooses which image to display as the main/side separator, based on
        _main_above.'''
        if self.separator_image:
            return self.separator_image
        if self._main_above:
            return 'navigationdrawer_gradient_rtol.png'
        else:
            return 'navigationdrawer_gradient_ltor.png'
class zipScatter(Scatter):
    def __init__(self, **kwargs):
        super(zipScatter, self).__init__()
class ImageButton(ButtonBehavior, AsyncImage):
    pass
class Interface(RelativeLayout):
    def __init__(self, **kwargs):
        self.mypos = None
        self.Armando2 = Asistente2()
        self.inmap = []
        self.coneccion = Connect()
        self.coneccion.seturl("http://127.0.0.1:8000/router/")
        self.data = self.coneccion.returntablesdata()

        from behave.datamain import DatasetManager
        self.ArchivoDataset  = DatasetManager(table = "Archivo")
        #self.UsuarioDataset  = DatasetManager(table = "Usuario")
        super(Interface, self).__init__(**kwargs)
        self.posactive = False

        from behave.Topnavbar import TopNavigationS
        parienteroot = RelativeLayout()
        self.sc = ScreenManager()
        self.main_screen = Screen(name = "pariente"); self.sc.add_widget(self.main_screen)
        
        self.pariente = GridLayout(cols = 1, size_hint_y = None ); self.main_screen.add_widget(self.pariente)
        self.gps_location = StringProperty()
        self.gps_status = StringProperty('press to get GPS location updates')
        
        
        topnavbar = TopNavigationS(); topnavbar.y = Window.height - topnavbar.height
        self.pos_status0 = Button(background_normal = color + "T50.png",size_hint = (1,None), height = dp(45), y = dp(-45))
        topnavbar.add_widget(self.pos_status0)
        topnavbar.lbl0.text = "Seguridad Ciudadana"
        self.pariente.height = height = Window.height -topnavbar.height
        self.load_map()
        
        self.navdraw = NavigationDrawer()
        self.navdraw.anim_type = 'slide_above_simple' 
        topnavbar.Img.bind(on_release = lambda x: self.navdraw.toggle_state())
        parienteroot.add_widget(self.sc)
        lateral = LateralMenu()
        lateral.buttons[0].bind(on_release = lambda x :self.Dummycurrent(current = "2"))
        lateral.buttons[1].bind(on_release = lambda x :self.Dummycurrent(current = "pariente"))
        lateral.buttons[2].bind(on_release = lambda x :self.get_pos())
        lateral.buttons[3].bind(on_release = lambda x :self.Dummycurrent(current = "0"))
        lateral.buttons[5].bind(on_release = lambda x :self.Dummycurrent(current = "1"))
        self.navdraw.add_widget(lateral)
        self.navdraw.add_widget(parienteroot)
        self.add_widget(self.navdraw)
        parienteroot.add_widget(topnavbar)
        controler1 = GridLayout(cols = 1, size_hint = (None,None), width = dp(250), height = dp(125), pos_hint = {'center_x':.5,'y':.0})
        self.pos_status = Button(opacity = 1,text_size = (dp(250),dp(50)),background_normal = color + "T50.png",text = "Zona Universitaria ,Av. Jose Contreras #74", halign = 'center', valign = 'middle')
        controler1.add_widget(self.pos_status)
        
        self.emitir = Button(background_normal = color + "3.png",size_hint = (1,None),text = "Emitir Alarma",height = dp(75), font_size = 20, width=  '150dp', on_release = lambda x: self.emitir_alarma())
        controler1.add_widget(self.emitir)
        self.main_screen.add_widget(controler1)
        #controler = GridLayout(cols = 1 , size_hint = (None,None), size = (dp(50), dp(125)))
        #controler.add_widget(Button(background_normal = color + "3.png",size_hint = (1,1),text = "+", font_size = 20, width=  '150dp'))
        #controler.add_widget(Button(background_normal = color + "3.png",size_hint = (1,1),text = "-", font_size = 20, width=  '150dp'))
        #self.main_screen.add_widget(controler)
        self.GPS()
        self.OtherScreens()
        self.parent3 = RelativeLayout()
        self.parent3.add_widget(Image(source = color + "3.png", keep_ratio = False ,allow_stretch = True))
        self.fileChooser = FileChooserListView()
        self.parent3.add_widget(self.fileChooser)
        here = threading.Thread(target= Clock.schedule_interval(self.refresh, 5))
        here.start()

    
    
    def emitir_alarma(self):
        if self.indicador.opacity == 1:
            a = Animation(opacity = 0, t = 'out_quart', d = .225)
            a.start(self.indicador)
            a.start(self.alarmapos)
            newalarm = Button(opacity = 0,font_size = 18,text = "[b]Alarma Emitida", background_normal = color + "2.png",markup = True, background_down = color + "2.png", y = Window.height, size_hint_y = None, height = dp(74))
            self.add_widget(newalarm)
            b = Animation(opacity = 1,y = Window.height - dp(74), d = 1, t = 'out_expo') +Animation(y = Window.height,opacity = 0, d = 1, t = 'in_expo') 
            b.bind(on_complete = lambda x,y: newalarm.parent.remove_widget(newalarm))
            b.start(newalarm)
            json = self.alarmax.json
            json["POSICION"] = "("+str(self.x_mapview.lat)+","+str(self.x_mapview.lon) + ")"
            json["DIRECCION"] = "[!]Habilitar geopy"
            json["id"] = None
            
            self.coneccion.insertar(2, json)
            from behave.Mapmarker import MapMarkerPopup as x1
            opc = ["ACCIDENTE","DELITO","CRIMEN","TRAFICO"]
            opc1 = ["rosering","bluering","Ripple","yellowring"]
            marcador = x1(anchor_y = .5, popup_size= (dp(250), dp(50)),opacity = .74,lat = self.x_mapview.lat , lon = self.x_mapview.lon, source = opc1[opc.index(json["GRAVEDAD"])-1]+".zip", anim_delay = 0)
            dim = GridLayout(rows = 1)
            dim.add_widget(Button(opacity = 1,text_size = (dp(200),dp(50)),background_normal = color + "T50.png",text = "Zona Universitaria ,Av. Jose Contreras #74", halign = 'center', valign = 'middle'))
            subdim = RelativeLayout(size_hint_x = None, width = dp(50))
            subdim.add_widget(Image(source = color + "T50.png", keep_ratio = False , allow_stretch = True))
            subdim.add_widget(ImageButton(on_release = lambda x: self.dibujarmisdirecciones(str((marcador.lat, marcador.lon))[1:-1].split(',')), source = asset + "ic_directions_white_36dp.png"))
            dim.add_widget(subdim)
            marcador.add_widget(dim)
            self.x_mapview.add_marker(marcador)
            self.inmap.append(json)
        else:
            self.alarmax = AlarmarPop(root = self)
            self.add_widget(self.alarmax)
            self.alarmax.animate()
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
        
    def dibujarmisdirecciones(self,pos2):
    
        #pos1 = str(self.mypos)[1:-1].split(',')
        pos1 = [self.mypos[0], self.mypos[1]]
        print pos2
        try:
            for n in range(2):
                if pos1[n][0] == ' ':
                    pos1[n] = float(pos1[n][1:])
                if pos2[n][0] == ' ':
                    pos2[n] = float(pos2[n][1:])
    
        except:
            import traceback
            traceback.print_exc()
                        
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

    def Archivo_Insert(self): 
        self.ArchivoDataset.Insertar(jdata = self.screen0.json())
        self.ArchivoDataset.Archivar()  
        self.Dummycurrent(current = "pariente")
        
    def Usuario_Insert(self): 
        self.UsuarioDataset.Insertar(jdata = self.screen0.json())
        self.UsuarioDataset.Archivar()  
        self.Dummycurrent(current = "pariente")
        
    
    def GetcordInfos(self,**kwargs):
        results = Geocoder.reverse_geocode(kwargs["lat"], kwargs["lon"])
        returnx = {}
        returnx["city"] = results.city
        returnx["country"] = results.country
        returnx["street_address"] = results.street_address
        returnx["state"] = results.state
        return returnx
        
    def GetMapInfos(self,**kwargs):
        text = kwargs["search"]
        text.replace(" ","+")
        url ="https://maps.googleapis.com/maps/api/place/textsearch/json?query="+text+"&key=AIzaSyAEEPqE645oiHa2POH_CfLU0b9i_vcuaAY"
        
    def Dummycurrent(self,**kwargs): 
        self.sc.current = kwargs["current"]
        if self.sc.current != "pariente":
            a = Animation(opacity = 0,y = 100 , d = .5 , t = "out_quart")
            a.start(self.pos_status0)
        else:
            a = Animation(opacity = 1,y = -45 , d = .5 , t = "out_quart")
            a.start(self.pos_status0)
    def OtherScreens(self):
        from behave.inspeccion_screen import Inspeccion_Screen
        from behave.chat_screen import Main_Screen
        from behave.configuracion import Configuracion
        
        #self.screen1 = Chat_Screen(name = "1",root = self )
        #self.screen2 = Contac_Screen(name = "2",root = self)
        self.screen1 = Main_Screen(root = self, name = "1")
        self.screen2 = Configuracion(root = self, name = "2")
        self.screen0 = Inspeccion_Screen(name = "0",datarequest = self.ArchivoDataset.get_data)
        self.screen0.b1.bind(on_release = lambda x: self.Archivo_Insert())
        
        # self.sc.add_widget(self.screen1)
        self.sc.add_widget(self.screen2)
        self.sc.add_widget(self.screen0)
        self.sc.add_widget(self.screen1)
        
    def GPS(self,**kwargs):
        try: 
            gps.configure(on_location=self.on_location,on_status=self.on_status)
            
        except NotImplementedError:
            import traceback
            traceback.print_exc()
            self.gps_status = 'GPS is not implemented for your platform'
            self.pos_status0.text =  str((18.4823058,-69.9564484))
            self.mypos =  (18.4823058,-69.9564484)
            
    def start(self, minTime, minDistance):
        gps.start()
    def stop(self):
        gps.stop()
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
        self.pos_status0.text =  self.gps_location
        self.mypos = self.gps_location
    @mainthread
    def on_status(self, stype, status):
        self.gps_status = 'type={}\n{}'.format(stype, status)
        print self.gps_status
        self.pos_status0.text =  self.gps_status
  
    @mainthread
    def on_pause(self):
        gps.stop()
        return True
    def on_resume(self):
        gps.start(1000, 0)
        pass
    def refresh(self,*args):
        if self.sc.current == "pariente":
            self.coneccion.actualizar(2)
            
            for i in self.coneccion.tables_data[2][0]:
                try: 
                    print self.inmap.index(i)
                except:
                    pos = i["POSICION"][1:-1].split(",")
                    from behave.Mapmarker import MapMarkerPopup as x1
                    marcador = x1(anchor_y = .5, popup_size= (dp(250), dp(50)),opacity = .74,lat = pos[0] , lon = pos[1], source = "Ripple.zip", anim_delay = 0)
                    dim = GridLayout(rows = 1)
                    dim.add_widget(Button(opacity = 1,text_size = (dp(200),dp(50)),background_normal = color + "T50.png",text = "Zona Universitaria ,Av. Jose Contreras #74", halign = 'center', valign = 'middle'))
                    subdim = RelativeLayout(size_hint_x = None, width = dp(50))
                    subdim.add_widget(Image(source = color + "T50.png", keep_ratio = False , allow_stretch = True))
                    subdim.add_widget(ImageButton(on_release = lambda x: self.dibujarmisdirecciones(str((marcador.lat, marcador.lon))[1:-1].split(',')), source = asset + "ic_directions_white_36dp.png"))
                    dim.add_widget(subdim)
                    marcador.add_widget(dim)
                    self.x_mapview.add_marker(marcador)
                    self.inmap.append(i)
        else:
            pass
    def load_map(self,**kwargs):
        
        from behave.Mapmarker import MapMarkerPopup as x1
        accesstoken = "pk.eyJ1IjoiYXJtYW5kbzI5IiwiYSI6ImNpd282ZHJ3azAwMWoydHFuZmJudnNzYzEifQ.12vIF51BCThjrut4Q56sGg"
        sourcex = MapSource(url="https://api.mapbox.com/styles/v1/mapbox/streets-v10/tiles/256/{z}/{x}/{y}?access_token=pk.eyJ1IjoibWFjYXR1cyIsImEiOiJjaXlubGRkdXAwMDJ1MzNwZjdwanhkdnd6In0.eYV9WVlCsI44Ku0HSup7Pg",
        cache_key="custom_map1s",tile_size=256,
        image_ext="jpg", attribution="@Armando Jose Soto Melo")
        self.x_mapview = MapView(lat = 18.454651 , lon = -69.971119, zoom = 15, map_source = sourcex)
        self.x_mapview.bind(on_map_relocated = lambda x,y,z: self.mapmoving())
        #self.x_mapview.bind(on_lon = lambda x: self.mapmoving())
        self.line = mdata3LineMapLayer()
        self.x_mapview.add_layer(self.line, mode="scatter")
        self.line.reposition()
    
        for i in self.data[2][0]:
            pos = i["POSICION"][1:-1].split(",")
            print pos
            from behave.Mapmarker import MapMarkerPopup as x1
            opc = ["ACCIDENTE","DELITO","CRIMEN","TRAFICO"]
            opc1 = ["rosering","bluering","Ripple","yellowring"]
       
            marcador = x1(anchor_y = .5, popup_size= (dp(250), dp(50)),opacity = .74,lat = pos[0] , lon = pos[1], source = opc1[opc.index(i["GRAVEDAD"])-1]+".zip", anim_delay = 0)

            dim = GridLayout(rows = 1)
            dim.add_widget(Button(opacity = 1,text_size = (dp(200),dp(50)),background_normal = color + "T50.png",text = "Zona Universitaria ,Av. Jose Contreras #74", halign = 'center', valign = 'middle'))
            subdim = RelativeLayout(size_hint_x = None, width = dp(50))
            subdim.add_widget(Image(source = color + "T50.png", keep_ratio = False , allow_stretch = True))
            subdim.add_widget(ImageButton(on_release = lambda x: self.dibujarmisdirecciones(str((marcador.lat, marcador.lon))[1:-1].split(',')), source = asset + "ic_directions_white_36dp.png"))
            dim.add_widget(subdim)
            marcador.add_widget(dim)
            self.x_mapview.add_marker(marcador)
            self.inmap.append(i)
        self.marker = MarkerMapLayer()
        self.x_mapview.add_layer(self.marker) 
        self.main_screen.add_widget(self.x_mapview)
        self.indicador = Image(opacity = 0,source =  "Radio.zip", keep_ratio = False, allow_stretch = True, size_hint = (None,None),anim_delay = 0, size = (dp(32),dp(32)), pos_hint = {'center_y':.5, 'center_x':.5})
        self.alarmapos = Button(opacity = 0,background_normal = color + "T50.png", border = [0,0,0,0], background_down = color + "T50.png",text = "", size_hint = (None,None), size = (200,30), pos_hint = {'center_x':.5, 'center_y':.25})
        self.main_screen.add_widget(self.indicador)
        self.main_screen.add_widget(self.alarmapos)
    def mapmoving(self):
        self.alarmapos.text = str(self.x_mapview.lat)[:-5] + "," + str(self.x_mapview.lon)[:-5]

    def get_pos(self):
        from behave.Mapmarker import MapMarkerPopup as x1
        self.x_mapview.center_on(self.mypos[0],self.mypos[1])
        marcador = x1(anchor_y = .5, popup_size= (dp(200), dp(50)),opacity = 1,lat = self.mypos[0] , lon = self.mypos[1], source = "person.zip", anim_delay = 0,disabled = False)
        dim = GridLayout(rows = 1)
        dim.add_widget(Button(opacity = 1,text_size = (dp(200),dp(50)),background_normal = color + "T50.png",text = "Mi Posicion", halign = 'center', valign = 'middle'))
        subdim = RelativeLayout(size_hint_x = None, width = dp(50))
        subdim.add_widget(Image(source = color + "T50.png", keep_ratio = False , allow_stretch = True))
        subdim.add_widget(ImageButton(on_release = lambda x: self.Dummycurrent(current = "1"),source = asset + "ic_message_white_36dp.png"))
        dim.add_widget(subdim)
        marcador.add_widget(dim)
        self.x_mapview.add_marker(marcador)
        
class MyApp(App):
    def build(self):

        return Interface()
 

if __name__ in ('__main__', '__android__'):
    MyApp().run()