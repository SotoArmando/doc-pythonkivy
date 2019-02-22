# -*- coding: utf-8 -*-

from os import path
from os.path import exists,dirname, join
from functools import partial
import time
import json
import datetime

class Table:
    # def __init__(self):
        # self._dict = {}
        # self.rows = []
        # self.IsFileLoaded = False
        # self.domain = "https://codicooktimerdatabase.herokuapp.com/route"
        # self.separator = "[ AND ]"
        # self.inchanges = []
        # self.outsaved = []
        # self.actualcallback = None
        # self.requestresult = None
        # self.req = None
        # self.sending = []
        
    def kivygot(req, result): return result
    def SubmitChanges(self):
        
        print ('','[!] Writing on cloud.')
        for row in self.rows:
            if row['state'] == 'Saved':
                pass
            elif row['state'] == 'Edited':
                try:
                    EditedRow = row
                    self.SendPut(EditedRow)
                except: pass
            elif row['state'] == 'Created':
                try:
                    CreatedRow = row
                    self.sending.append(self.rows.index(row))
                    self.SendPost(CreatedRow)
                except: pass
        
        self._SaveLocally()
   
    def Syncronize(self):
        print ('','[!] Loading Data from Cloud.')
        print('','[!] Sending Get.')
        self.SendGet()
        
    def SendGet(self): 
        self.req = UrlRequest(self.domain +"/"+self.__class__.__name__+"/", self.EndSyncronize, on_redirect = self.gotcha, on_failure = self.gotcha, on_error = self.gotcha)
        
    def Request(self,load,params):
        #print (self.domain+"/"+self.__class__.__name__+"/"+load+"?x="+params)
        self.req = UrlRequest(self.domain +"/"+self.__class__.__name__+"/"+load+"/?x="+params, self.RequestReturnLoad, on_redirect = self.gotcha, on_failure = self.gotcha, on_error = self.gotcha) 
        
    def RequestReturnLoad(self,req,result): 
        print ('',"[!] Load Catched")
        self.requestresult = result
        #print (result)
    
    def EndSyncronize(self,req,result):
        #print (result)
        print ('','[!] Data Loaded Successfully')
        print('',"[!] Ending Get.")
        try:
            print ('',"[get:Request][!]"+self.domain+"/"+self.__class__.__name__)
            self.rows[:] = []
            for row in result: 
                row['state'] = 'Saved'
                self.rows.append(row)
               
                
            print ('',"[Success][!] "+str(len(self.rows))+" rows loaded successfully.")
            
        except: print ("There is not an URL for this table.")
        print ('','[!] Loading Data from Local.')
        self._LoadLocally()
        print ('','[!] Data Loaded Successfully')
        print ('\n')
        #self.Fetch()
        pass
        if (self.actualcallback == None): pass
        else: self.actualcallback(self)
        
    def gotcha(self,req,result):
        print (req)
        print (result)
        self.requestresult = result

    def Fetch(self): 
        self.inchanges = []
        self.outsaved = []
        
        print ('\n')
        
        for row in self.rows:
            if row['state'] == "Saved":
                self.outsaved.append(row)
            else:
                self.inchanges.append(row)
                
        print ('',">>\tCOMING IN")
        for row in self.outsaved: print ('',"["+str(self.rows.index(row))+"]"+str(row))
        print ('\n'*1)  
        print ('',">>\tGOING OUT")
        
        if self.inchanges == []:
            print ('','No Changes.')
        else:
            for row in self.inchanges: print ('',"["+str(self.rows.index(row))+"]"+str(row))
        print ('\n'*1)    
   
    def ClearTable(self): self.rows[:] = [] 
    
    def _SaveLocally(self):
        
        for row in self.rows:
            if 'state' in row:
                if row['state'] == "Edited":
                    thisrow = row
                    for _row in self.rows:
                        if _row != thisrow:
                            if ('id' in _row) and ('id' in thisrow):
                                if _row['id'] == thisrow['id']:
                                    if self.rows.index(_row) > self.rows.index(thisrow):
                                        _row['state'] = 'ToDelete'
            else:
                row['state'] = 'Created'

        for row in self.rows:
            if 'state' in row:
                if row['state'] == 'ToDelete': 
                    self.rows.remove(row)
            else:
                row['state'] = 'Created'
        # self.rows.pop(self.rows.index(_row))
        try:
            print ('',"[!] Looking for .:[File] " +self.__class__.__name__ + ".txt")
            file = open(self.__class__.__name__ + ".txt","r")
            print ('',"[!] There is a file.")
            os.remove(self.__class__.__name__ + ".txt")
            #print ('',"[Deleted File][!] "+self.__class__.__name__ + ".txt was removed.")
            self._SaveLocally();
        except: 
            
            file = open(self.__class__.__name__ + ".txt","w")
            
            for row in self.rows:
                addon = self.separator
                if self.rows.index(row) == len(self.rows)-1: addon = ""
                if not row['state'] == 'Saved': file.write(str(row)+addon)
            file.close()
            
        print ('',"[New Load][!] " + self.__class__.__name__ + ".txt was Saved.")
    
    def _LoadLocally(self):
        try:
            print ('',"[!] Looking for .:[File] " +self.__class__.__name__ + ".txt")
            file = open(self.__class__.__name__ + ".txt","r")
            print ('',"[!] There is a file.")
            for row in file.read().split(self.separator): 
                try:
                    newrow = eval(row)
                    if not newrow['state'] == "Edited": newrow['state'] = "Created"
                    if not newrow in self.rows:
                        if ("{" in row) and ("}" in row):self.rows.append(newrow)
                        print('','[Change][!]'+newrow)
                    
                except: 
                    pass
            
            print ('',"[Loaded File][!] "+self.__class__.__name__ + ".txt was Loaded Successfully.")
        except:
            print ('',"[NotFound File][!] "+self.__class__.__name__ + ".txt was Not Found.")
    



    def GotSuccess(self,req,result):
        result['state'] = "Saved"
        self.rows.pop(self.sending[0])
        self.rows.append(result)
        self._SaveLocally()
        
    def SendPost(self, Entitie):
        registro = {}
        for i in self.dict():
            try:
                print ('',i, Entitie[i])
                registro[str(i)] = Entitie[i]
            except:
                print('',"Asegurese de usar los Campos correspondientes.")
                
        registro = json.dumps(registro)
        
        print ('',registro)
        print ('',"[post:Request][!]" + self.domain+"/"+self.__class__.__name__+"/" )
        response = UrlRequest(self.domain+"/"+self.__class__.__name__+"/" ,self.GotSuccess, on_redirect = self.gotcha, on_failure = self.gotcha, on_error = self.gotcha, req_body = registro, req_headers = {'Content-Type': 'application/json'}, )
        print(response.text)
        
    def SendPut(self, Entitie):
        registro = { 'id': Entitie['id'] }
        for i in self.dict():
            try:
                print ('',i, Entitie[i])
                registro[str(i)] = Entitie[i]
            except:
                print('',"Asegurese de usar los Campos correspondientes.")
                
        registro = json.dumps(registro)
        
        print('',registro)
        print('',"[put:Request][!]" + self.domain+"/"+self.__class__.__name__+"/"+str(Entitie['id'])+"/" )
        response = UrlRequest(self.domain+"/"+self.__class__.__name__+"/"+str(Entitie['id'])+"/" ,method = "PUT",req_body = registro, req_headers = {'Content-Type': 'application/json'})
        print(response.text)
           
    def CreateEntitie(self, _entitie): 
        if self.IsEntitie(_entitie) == True: self.Create(row = _entitie.dict())
        
    def EditEntitie(self, _entitie): 
        if self.IsEntitie(_entitie): self.Edit(index = _entitie.dict()['id'], new_dict = _entitie.dict())
    
    def DeleteEntitie(self, _entitie): 
        if self.IsEntitie(_entitie): self.Edit(index = self.rows.index(_entitie))
    
    def IsEntitie(self, _entitie): 
        for i in _entitie:
            try:
                x = self.dict()[i]
            except:
                print ("This is not an entitie for this table.")
                return False
        return True
                
    def FirstorDefault(self,**kwargs):
        if ('col' in kwargs) and ('val' in kwargs):
            for row in self.rows:
                print (row)
                if kwargs['val'] == row[kwargs['col']]: 
                    print (row)
                    return row
                
    
        else: 
            kwargs['col'] = str(input("[col?][I]: "))
            kwargs['val'] = str(input("[val?][I]: "))
            print ('\n')
            for row in self.rows:
                try:
                    if kwargs['val'] in row[kwargs['col']]: 
                        print ('',row)
                        if row['State'] == 'Saved': return result
                except:
                    print ('',"[!] There is no field "+kwargs['col'])
                    break
    
    def GetbyId(self,**kwargs):
        if ('id' in kwargs):
            for row in self.rows:
                if kwargs['id'] == row['id']: 
                    if row['state'] == 'Saved': return row
                
    
        else: 
            kwargs['id'] = int(input("[id?][I]: "))
            for row in self.rows:
                if kwargs['id'] == row['id']: 
                    print ('\n',row)
                    if row['state'] == 'Saved': return row
                
    def Create(self,**kwargs): 
        if 'row' in kwargs:
            if (self.IsEntitie(kwargs['row'])): 
                self.rows.append(kwargs['row'])
            self._SaveLocally()
        else:
            newrow = { }
            for i in self.dict(): 
                newrow[i] = input("[C:"+i+"][I]: ")
            print ('\n',"[New Row][!]"+ str(newrow))
            newrow['state'] = 'Created'
            self.rows.append(newrow)
            self._SaveLocally()
            return newrow
        
    def Delete(self,**kwargs): 
        if ('index' in kwargs):
            self._SaveLocally()
            return self.rows.pop(kwargs['index'])
        else:
            kwargs["index"] = int(input("[Index?][I]: "))
            
            if self.rows[kwargs['index']]['state'] == 'Saved':
                self.rows[kwargs['index']]['state'] = 'Deleted'
            else:
                row = self.rows.pop(kwargs['index'])
            print (".: ",row)
            self._SaveLocally()
            return row
                 
    def Edit(self,**kwargs):
        if ('index' in kwargs) and ('new_dict' in kwargs):
            selectedrow = kwargs["index"]
            editargs = kwargs["new_dict"]
            if (self.IsEntitie(kwargs["new_dict"])): 
                for i in editargs: self.rows[selectedrow][i] = editargs[i]
            else:
                print ('\n',"[!] There is a Field that should'n be there")
                return None
            if self.rows[selectedrow]['state'] == "Created": 
                self.rows[selectedrow]['state'] = 'Created'
            else: 
                self.rows[selectedrow]['state'] = 'Edited'
            self._SaveLocally()
            print ('\n',"[R:Result][!]"+str(self.rows[selectedrow]), "Successfully Edited.")
        else:
            kwargs["index"] = int(input("[Index?][I]: "))
            print ('\n',"[R:Selected][!]"+str(self.rows[kwargs["index"]])+'\n')
            kwargs["new_dict"] = {}
            for i in self.dict():
                kwargs["new_dict"][i] = input("[C:"+i+"][I]: ")
                
            selectedrow = kwargs["index"]
            editargs = kwargs["new_dict"]
            if (self.IsEntitie(kwargs["new_dict"])): 
                for i in editargs: self.rows[selectedrow][i] = editargs[i]
            else:
                print ('\n' "[!] There is a Field that should'n be there")
                return None
            if self.rows[selectedrow]['state'] == "Created": 
                self.rows[selectedrow]['state'] = 'Created'
            else: 
                self.rows[selectedrow]['state'] = 'Edited'
            print ('\n',"[R:Result][!]"+str(self.rows[selectedrow]), "Successfully Edited.")
            self._SaveLocally()       

    def Where(self,**kwargs):
        if ('col' in kwargs) and ('val' in kwargs):
            result = []
            for row in self.rows:
                if kwarg['val'] in row['col']: 
                    if row['State'] == 'Saved': result.append(row)
            return result
        else: 
            
            result = []
            print ('',self.dict())
            kwargs['col'] = str(input("[col?][I]: "))
            kwargs['val'] = str(input("[val?][I]: "))
            print ('\n')
            for row in self.rows:
                try:
                    if kwargs['val'] in row[kwargs['col']]: 
                        result.append(row)
                        print ('',row)
                except:
                    print ('',"[!] There is no field "+kwargs['col'])
                    break
                
                
            return result
    
    def GetAll(self,**kwargs): return(self.rows)
    
class Entitie:
    _dict = {}
    def __init__(self, **kwargs):
        for kwarg in kwargs:
            for arg in self._dict:
                if kwarg == arg: 
                    self._dict[kwarg] = kwargs[kwarg]
                    exec("".join(["self.",kwarg,"='",str(kwargs[kwarg]),"'"]))
        for key in self._dict: 
            exec("".join(["self.",key,"=''"]))

        self._dict = {}
        self.rows = []
        self.IsFileLoaded = False
        self.domain = "https://codicooktimerdatabase.herokuapp.com/route"
        self.separator = "[ AND ]"
        self.inchanges = []
        self.outsaved = []
        self.actualcallback = None
        self.requestresult = None
        self.req = None
        self.sending = []
        
    def dict(self):
        for key in self._dict:
            exec("".join(['self._dict["',key,'"]=self.',key]))
        return self._dict

class Role(Entitie): 
    _dict = {
    'Name': "",
    'PrivilegeId': ""
    }
    
class Recipe(Entitie): 	
    _dict ={
    "Titulo": "",
    "Descripcion": "",
    "Ingredientes": "",
    "Instrucciones": "",
    "UserId": "",
    "IMG0": "",
    "IMG1": "",
    "IMG2": ""
    }

class Privilege(Entitie):
    _dict = {
    'Name': "",
    'CanAdministrate': False,
    'CanAccessUserContent': False 
    }
   
class Tag(Entitie): 
    _dict = {
    'Name': "",
    'Color': ""
    }
                
class Profile(Entitie):
    _dict = {
    'Nombres': "",
    'Apellidos': "",
    'IMG0': "",
    
    }
      
class User(Entitie): 
    _dict = {
    "UCrendential": "",
    "PCrendential": "",
    "Mail": "",
    "IsActive": False,
    "DateCreated": ""
}

class PrivilegeIndex(Privilege,Table): pass
class RecipesIndex(Recipe,Table): pass
class RoleCatalog(Role,Table): pass
class TagIndex(Tag,Table): pass
class UserIndex(User,Table): pass
class ProfileIndex(Profile,Table): pass

from kivy.clock import Clock
from kivy.animation import Animation
from kivy.uix.stencilview import StencilView
from kivy.properties import (ObjectProperty, NumericProperty, OptionProperty, BooleanProperty, StringProperty, ListProperty, DictProperty, ObjectProperty)
from kivy.metrics import MetricsBase, dp
from kivy.graphics.texture import Texture
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.scatter import Scatter
from kivy.uix.scrollview import ScrollView
from kivy.uix.widget import Widget
from kivy.core.audio import SoundLoader,Sound
from kivy.utils import platform
from kivy.lang import Builder
from kivy.network.urlrequest import UrlRequest
from kivy.uix.screenmanager import ScreenManager, Screen	

class CodiApp():
    index = NumericProperty(0)
    

    def _timenow(self): return datetime.datetime.now()
    def _nextplace(self): return self.clock[:6].rfind("0") 
    def _len(self): return len(self.clock)
    def _format(self): 
        #print (self.clock)
        return (self.clock[0:2]+":"+self.clock[2:4]+":"+self.clock[4:6])
    def _format1(self):
        a = self.clock[0:2]
        b = self.clock[2:4]
        c = self.clock[4:6]
  
        if self.clock[0:2] == "00": a = '' 
        else: a = self.clock[0:2]+ " Horas "
        if self.clock[2:4] == "00": b = ''  
        else: b = self.clock[2:4]+ " Minutos "
        if self.clock[4:6] == "00": c = '' 
        else: c = self.clock[4:6]+ " Segundos "
        x = [str(a),str(b),str(c)]
        for _x in x:
            try: 
                if _x[0] == '0' and _x != '': 
                    _x = _x[1:]
            except:
                pass

        
        return (a + b + c)
    def _check(self,*args):
        actual = self._timenow()
        pasttime = actual - self.settledtime
        
        self.clockhours = int(self.clock[0:2])
        self.clockmin = int(self.clock[2:4])
        self.clockseconds = int(self.clock[4:6])
        
        d = divmod(pasttime.days * 86400 + pasttime.seconds,86400)
        h = divmod(d[1],3600) 
        m = divmod(h[1],60)  
        s = m[1]

        #print (h[0],m[0],s)
        #print (self.clockhours - h[0],self.clockmin - m[0] ,self.clockseconds - s)
        if (self.clockhours - h[0],self.clockmin - m[0] ,self.clockseconds - s) == (0,0,0):
            self.thelabel.text = '[color=#000000]Marca tu tiempo'
            self.stoptimer(self.thelabel,None)
 
        hstr = str(h[0])
        mstr = str(m[0])
        sstr = str(s)
        if len(str(h[0])) < 2: hstr =  "0" + str(h[0])
        if len(str(m[0])) < 2: mstr =  "0" + str(m[0])
        if len(str(s)) < 2: sstr =  "0" + str(s)
       
        if self.settled == True: self.thelabel.text = '[color=#000000]'+ hstr + ":" + mstr + ":" + sstr
        
    def write(self,**kwargs):
        if 'key' in kwargs:
            pass
        else:            
            kwargs['key'] = input("| [:key][I]: ")
            if kwargs['key'] == '': kwargs['key'] = 0
        self.text += kwargs['key']
        self.clock = self.clock[:self.cc-self._len()] + self.text[-6:]
        self.cc -= 1
        
        
    def start(self,**kwargs):
        if 'label' in kwargs: self.thelabel = kwargs['label']
        self.settled = True
        self.settledtime = self._timenow()
        self.timer = Clock.schedule_interval(self._check, 1.0/60.0)
        
    def stoptimer(self,x,y):
        Clock.unschedule(self.timer)
        self.settledhistory.append(self.clock)
        self.clock = '000000'
        self.text = ''
        self.cc = 5
        x.text = '[color=#000000]00:00:00'
        try:
            y.text = '[color=#1E97FF]0 Horas 0 Minutos y 0 Segundos'
        except: pass
        print ('|',"[!]Finish")
        
        
    def repeat(self):
        self.stoptimer(self.thelabel)
        self.clock = self.settledhistory[-1]
        self.start()

class NavigationDrawerException(Exception):

    '''Raised when add_widget or remove_widget called incorrectly on a

    NavigationDrawer.



    '''
class NavigationDrawer(StencilView):
    '''Widget taking two children, a side panel and a main panel,

    displaying them in a way that replicates the popular Android

    functionality. See module documentation for more info.



    '''



    # Internal references for side, main and image widgets

    _side_panel = ObjectProperty()

    _main_panel = ObjectProperty()

    _join_image = ObjectProperty()

    Trigged = BooleanProperty(False)

    side_panel = ObjectProperty(None, allownone=True)

    '''Automatically bound to whatever widget is added as the hidden panel.'''

    main_panel = ObjectProperty(None, allownone=True)

    '''Automatically bound to whatever widget is added as the main panel.'''



    # Appearance properties

    side_panel_width = NumericProperty()

    '''The width of the hidden side panel. Defaults to the minimum of

    250dp or half the NavigationDrawer width.'''

    separator_image = StringProperty('')

    '''The path to an image that will be placed between the side and main

    panels. If set to `''`, defaults to a gradient from black to

    transparent in an appropriate direction (left->right if side panel

    above main, right->left if main panel on top).'''

    separator_image_width = NumericProperty(dp(10))

    '''The width of the separator image. Defaults to 10dp'''



    # Touch properties

    touch_accept_width = NumericProperty('14dp')

    '''Distance from the left of the NavigationDrawer in which to grab the

    touch and allow revealing of the hidden panel.'''

    _touch = ObjectProperty(None, allownone=True)  # The currently active touch



    # Animation properties

    state = OptionProperty('closed', options=('open', 'closed'))

    '''Specifies the state of the widget. Must be one of 'open' or

    'closed'. Setting its value automatically jumps to the relevant state,

    or users may use the anim_to_state() method to animate the

    transition.'''

    anim_time = NumericProperty(0.3)

    '''The time taken for the panel to slide to the open/closed state when

    released or manually animated with anim_to_state.'''

    min_dist_to_open = NumericProperty(0.7)

    '''Must be between 0 and 1. Specifies the fraction of the hidden panel

    width beyond which the NavigationDrawer will relax to open state when

    released. Defaults to 0.7.'''

    _anim_progress = NumericProperty(0)  # Internal state controlling

                                         # widget positions

    _anim_init_progress = NumericProperty(0)



    # Animation controls

    top_panel = OptionProperty('main', options=['main', 'side'])

    '''Denotes which panel should be drawn on top of the other. Must be

    one of 'main' or 'side'. Defaults to 'main'.'''

    _main_above = BooleanProperty(True)



    side_panel_init_offset = NumericProperty(0.5)

    '''Intial offset (to the left of the widget) of the side panel, in

    units of its total width. Opening the panel moves it smoothly to its

    final position at the left of the screen.'''



    side_panel_darkness = NumericProperty(0.8)

    '''Controls the fade-to-black of the side panel in its hidden

    state. Must be between 0 (no fading) and 1 (fades to totally

    black).'''



    side_panel_opacity = NumericProperty(1)

    '''Controls the opacity of the side panel in its hidden state. Must be

    between 0 (fade to transparent) and 1 (no transparency)'''



    main_panel_final_offset = NumericProperty(1)

    '''Final offset (to the right of the normal position) of the main

    panel, in units of the side panel width.'''



    main_panel_darkness = NumericProperty(0)

    '''Controls the fade-to-black of the main panel when the side panel is

    in its hidden state. Must be between 0 (no fading) and 1 (fades to

    totally black).

    '''



    opening_transition = StringProperty('in_quart')

    '''The name of the animation transition type to use when animating to

    an open state. Defaults to 'out_cubic'.'''



    closing_transition = StringProperty('out_quart')

    '''The name of the animation transition type to use when animating to

    a closed state. Defaults to 'out_cubic'.'''



    anim_type = OptionProperty('reveal_from_below',

                               options=['slide_above_anim',

                                        'slide_above_simple',

                                        'fade_in',

                                        'reveal_below_anim',

                                        'reveal_below_simple',

                                        ])

    '''The default animation type to use. Several options are available,

    modifying all possibly animation properties including darkness,

    opacity, movement and draw height. Users may also (and are

    encouaged to) edit these properties individually, for a vastly

    larger range of possible animations. Defaults to reveal_below_anim.

    '''


    def on_size(self, *args):
        if self.Trigged == False:
            Clock.schedule_once(self.on__main_above, 0)
            self.Trigged == True

        


    
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
class SideMenu(RelativeLayout): pass

class MaterialButton(Button):
    canvasformscale = NumericProperty(1)
    gotpos = ListProperty([-1,-1])
    coloropacity = NumericProperty(0)
    def on_last_touch(self,x,Motion): 
        print (self.coloropacity,self.gotpos,self.canvasformscale )
        self.gotpos = Motion.pos
        if Motion.grab_state == False:
            Anim = Animation(canvasformscale = Window.width,coloropacity = 0, d = .85 , t ='out_quart')
            setattr(self, 'canvasformscale', 1)
            setattr(self, 'coloropacity', .54)
            Anim.start(self)

        else:
            pass
            
        print (self.gotpos)
        print (Motion.grab_state)
        
class Pelota(): 
    scale = NumericProperty(1)
class Opcion(RelativeLayout,Pelota):
    Animation_ScaleTo = NumericProperty(1.1) 
    Animation_OpacityTo = NumericProperty(1)
    
    def Activar(self):
        Animation(opacity = self.Animation_OpacityTo,scale = self.Animation_ScaleTo, d = .5, t = 'out_quart').start(self)
    def Desactivar(self):
        Animation(opacity = .54,scale = 1, d = .5, t = 'out_quart').start(self)   
            
class CompWidget(GridLayout):
    opciones =ListProperty([])
    n = NumericProperty(None) 
    trigged = BooleanProperty(False)
    cursor = NumericProperty(0)

    def on_pos(self,*args):
        if self.trigged == False:
            self.trigged = True
            self.sumarizeN()
            
    def sumarizeN(self):
        self.clear_widgets()
        self.size_hint_x = None
        self.width = (dp(8) * self.n) + (self.spacing[0] * (self.n-1))

        for i in range(self.n):
            opcion = Opcion()
            self.add_widget(opcion)
            self.opciones.append(opcion)
                               
    def on_cursor(self,*args):
        print args
        self.opciones[self.cursor].Activar()
        if self.cursor-1 >= 0: self.opciones[self.cursor-1].Desactivar()
        if self.cursor+1 <= self.n-1: self.opciones[self.cursor+1].Desactivar()
		
class Alert(RelativeLayout): pass
class Container(RelativeLayout): pass
class Tag(RelativeLayout): pass

class NewTagScreen(Screen): pass
class Recipe(Screen):pass
class PhotoEditorScreen(Screen): pass
class IngredientPOSTView(RelativeLayout): pass
class RecipeListItem(RelativeLayout): pass


class Alert(RelativeLayout):
    def show(self): self.showme.start(self)

class CookingApp(App,CodiApp):
	privacypolicy = StringProperty("""Testing Policy""")

	asset = StringProperty( "" )
	sound = StringProperty( "".join([path.dirname(path.abspath(__file__)) , '/docs/_sounds/']) )
	behavior = StringProperty("".join([path.dirname(path.abspath(__file__)) , '/docs/_behavior/']))
	font = StringProperty("".join([path.dirname(path.abspath(__file__)) , '/docs/_fonts/']))

	clock = StringProperty('000000')
	keys = StringProperty('0123456789')
	text = StringProperty('')
	settled = BooleanProperty(False)
	settledtime = ObjectProperty(None)
	settledhistory = ListProperty([])
	timer = ObjectProperty(None)
	
	cc = NumericProperty(len('000000') - 1)

	_LoggedUser = NumericProperty(0)
	
	UserIndexTrigged = BooleanProperty(False)
	UserIndexResponseWaiter = ObjectProperty(None)
	smallstate = BooleanProperty(False)
	ReadingState = BooleanProperty(False)

	icmenucolor = ListProperty([1,1,1,.54])
	icmenubackcolor = ListProperty([0.1171875, 0.5937500000000002, 1.0, 1.0])
	
	reading = BooleanProperty(False)
	recipelistcreatecontrol = NumericProperty(0)

	waitingfor = ObjectProperty(None)
	cookwithrecipebuttoncontrol = NumericProperty(0)
	
	currentscreen = StringProperty("")

	index = NumericProperty(-1)
	screen_names = ListProperty([])

	class Gradient(object):
		@staticmethod
		def horizontal(rgba_left, rgba_right):
			texture = Texture.create(size=(1, 2), colorfmt="rgba")
			pixels = rgba_left + rgba_right
			pixels = [chr(int(v * 255)) for v in pixels]
			buf = ''.join(pixels)
			texture.blit_buffer(buf, colorfmt='rgba', bufferfmt='ubyte')
			return texture

		@staticmethod
		def vertical(rgba_top, rgba_bottom):
			texture = Texture.create(size=(2, 1), colorfmt="rgba")
			pixels = rgba_bottom + rgba_top
			pixels = [chr(int(v * 255)) for v in pixels]
			buf = ''.join(pixels)
			texture.blit_buffer(buf, colorfmt='rgba', bufferfmt='ubyte')
			return texture
            
	def build(self):
		self.PrivilegeIndex = ObjectProperty(PrivilegeIndex())
		self.RecipesIndex = ObjectProperty(RecipesIndex())
		self.RoleCatalog = ObjectProperty(RoleCatalog())
		self.TagIndex = ObjectProperty(TagIndex())
		self.UserIndex = ObjectProperty(UserIndex())
		self.ProfileIndex = ObjectProperty(ProfileIndex())
		
		Window.clearcolor = (1,1,1,1)
		self.asset = self.getdpiassets()
		print (".: ASSETS DIR",self.asset)
		print (".: FONTS DIR" ,self.font)
		print (".: SOUND DIR" ,self.sound)
		print (".: BEHAVIOR DIR" ,self.behavior)
		print (".: SCREEN RES" ,Window.size)

		if Window.size[1] <= 800: 
			print ('smallstate ON')
			self.smallstate = True

		self.screens = {}
		self.available_screens = sorted([
			'FirstScreen', 'CreateRecipeScreen', 'CreateAccountScreen', 'LoginScreen', 'PrivatePolicyScreen',
			'Recipe', 'UserRecipesIndex'])
		self.screen_names = self.available_screens
		curdir = dirname(__file__)
		self.available_screens = [join(curdir, 'data', 'screens',
			'{}.kv'.format(fn).lower()) for fn in self.available_screens]

		self.UserIndex.defaultvalue.Syncronize()
		Clock.schedule_once(self.switchtoread, .5)
		#activity.bind(on_activity_result=self.on_activity_result) 
		#self.go_next_screen()
		self.go_screen(2)

	def go_next_screen(self):
		self.index = (self.index + 1) % len(self.available_screens)
		screen = self.load_screen(self.index)
		sm = self.root.ids.sm
		sm.switch_to(screen, direction='left')

	def load_screen(self, index):
		if index in self.screens:
			return self.screens[index]
		screen = Builder.load_file(self.available_screens[index])
		self.screens[index] = screen
		print self.screens
    		return screen

	def go_screen(self, idx):
		self.index = idx
		self.root.ids.sm.switch_to(self.load_screen(idx), direction='left')
	   

	def scrolleronstart(self):
		if self.waitingfor != None:
			Clock.unschedule(self.waitingfor)
			Animation(cookwithrecipebuttoncontrol = 0, d = .5, t ='out_expo').start(self)
			
	def scrolleonennd(self):
		self.waitingfor = Clock.schedule_once(lambda x: Animation(cookwithrecipebuttoncontrol = 1, d = .5, t ='out_expo').start(self), .5)

	def on_pause(self):
		return True
		
	def switchtoread(self,*args):
		Animation(icmenucolor = [0.1171875, 0.5937500000000002, 1.0, 1.0],icmenubackcolor = [0.1171875, 0.5937500000000002, 1.0,0], d = 1 , t='out_expo').start(self)  
		self.reading = True
		
	def checkreaded(self):
		if self.reading == True:
			self.switchreadtofalse()
			self.reading = False
			
	def switchreadtofalse(self):
		Animation(icmenucolor = [1,1,1,.84],icmenubackcolor = [0.1171875, 0.5937500000000002, 1.0, 1.0], d = 1 , t='out_expo').start(self)  
		self.reading = False
	def showcreaterecipebutton(self):
		print "asd"
		x = Animation(recipelistcreatecontrol = 1, d = .5, t = 'out_back')
		Clock.schedule_once(lambda c:x.start(self),.5)
		
	def checkstatesOnCurrent(self):
		if self.recipelistcreatecontrol == 1:
			x = Animation(recipelistcreatecontrol = 0, d = .5, t = 'out_expo')
			x.start(self)
			
	def getdpiassets(self):
		metrics = MetricsBase()
		try:
			android_dpi = metrics.dpi_rounded()
		except:
			android_dpi = metrics.dpi_rounded
		asset_dpi =  [120,160,240,320,480,640]
		asset_dpi2 = ['ldpi','mdpi','hdpi','xhdpi','xxhdpi','xxxhdpi']
		patch = path.dirname(path.abspath(__file__))
		for i in asset_dpi:
			if android_dpi == i:
				return "".join([patch,'/docs/_assets/drawable-',str(asset_dpi2[asset_dpi.index(i)]),'/'])

	
	def login(self,widget):
		self.UserIndexTrigged = False
		row = self.UserIndex.FirstorDefault(col = "UCrendential", val = widget.ids["Serialized_UCrendential_Temp"].text)
		self.UserIndex.Request(load = "IsUser", params = widget.ids["Serialized_UCrendential_Temp"].text+"[AND]"+widget.ids["Serialized_PCrendential_Temp"].text )    
		self.UserIndexResponseWaiter = Clock.schedule_interval(lambda x: self.WaitForLoginRequest(self,widget.parent),.25)
		
	def WaitForUserIndex(self, *args):
		if self.UserIndexTrigged == False:
			if len(self.UserIndex.rows) == 0: 
				pass
			else:
				self.UserIndexTrigged = True
				self.__Container__.ids["Alerta"].showme.start(self.__Container__.ids["Alerta"])
				self.UserIndexResponseWaiter.cancel()
				self.UserIndexResponseWaiter = None
				
			
		
	
	
	def WaitForUserRecipesRequest(self, *args):
		print ('',"[!] Waiting Response","(WaitForUserRecipesRequest)")
		if self.UserIndexTrigged == False:
			
			if self.UserIndex.requestresult == None: 
				pass
			else:
				self.UserIndexTrigged = True    
				for result in self.UserIndex.requestresult: print ('','[! Got a Recipe]',result)
				self.UserIndex.requestresult = None
				self.UserIndexResponseWaiter.cancel()
				
	def WaitForLoginRequest(self,*args):
		print ('',"[!] Waiting Response","(WaitForLoginRequest)")
		if self.UserIndexTrigged == False:
			if self.UserIndex.requestresult == None: 
				pass
			else:
					
				self.UserIndexTrigged = True

				try:
					if len(self.UserIndex.requestresult) == 1:
						self._LoggedUser = self.UserIndex.requestresult[0]['id']
						self.__Container__.ids["Alerta"].message = "Has Iniciado sesion"
						self.__Container__.ids["Alerta"].type = "Info"
						self.__Container__.ids["Alerta"].showme.start(self.__Container__.ids["Alerta"])
						Clock.schedule_once(lambda x: setattr(args[1], 'current', 'First'),.2) 
						self.UserIndex.Request(load = "UserRecipes", params = str(self.UserIndex.requestresult[0]['id']))
						self.UserIndex.requestresult = None
						self.UserIndexTrigged = False
						self.UserIndexResponseWaiter.cancel()
						self.UserIndexResponseWaiter = Clock.schedule_interval(self.WaitForUserRecipesRequest,.25)
						
					else:
					   
						self.__Container__.ids["Alerta"].message = "Usuario o Contraseña incorrectos"
						self.__Container__.ids["Alerta"].type = "Error"
						self.__Container__.ids["Alerta"].showme.start(self.__Container__.ids["Alerta"])
					 
				except:
						self.__Container__.ids["Alerta"].message = "No hay conexion a internet."
						self.__Container__.ids["Alerta"].type = "Warning"
						self.__Container__.ids["Alerta"].showme.start(self.__Container__.ids["Alerta"])
					

				
 
	def SendRecipe(self, widget):
		forsafe = "[color=#000000]"
		setattr(widget.ids.Container_Parrafos,'textresult', "".join(widget.text + "[AND]" for widget in widget.ids.Container_Parrafos.children))
		setattr(widget.ids.Container_Ingredientes,'textresult', "".join(widget.text + "[AND]" for widget in widget.ids.Container_Ingredientes.children))
		setattr(widget.ids.Container_Instrucciones,'textresult', "".join(widget.text + "[AND]" for widget in widget.ids.Container_Instrucciones.children))
		widget.viewmodel['Titulo'] = widget.viewmodel['Titulo'][len(forsafe):]
		widget.viewmodel['UserId'] = self._LoggedUser
		for i in widget.viewmodel: 
			if widget.viewmodel[i] == '': widget.viewmodel[i] = 'N/A'
		print ("","[!] Sending Recipe")
		print (widget.viewmodel)
		self.RecipesIndex.Create(row = widget.viewmodel)
		self.RecipesIndex.SubmitChanges()
	   
		if 'BottomCarousel' in  self.__Container__.children[-1].children[1].children[0].children[0].ids:
			bottomcarrousel = self.__Container__.children[-1].children[1].children[0].children[0].ids.BottomCarousel
			bottomcarrousel.parent.switchstate0()
			bottomcarrousel.parent.switchstate1()
	   
		
	def get_filename(self):
		while True:
			self.index += 1
			fn = "".join[Environment.getExternalStorageDirectory().getPath() , '/takepicture{}.jpg'.format(self.index)]
			if not exists(fn):
				return fn

	def take_picture(self):
		intent = Intent(MediaStore.ACTION_IMAGE_CAPTURE)
		self.last_fn = self.get_filename()
		self.uri = Uri.parse('file://' + self.last_fn)
		self.uri = cast('android.os.Parcelable', self.uri)
		intent.putExtra(MediaStore.EXTRA_OUTPUT, self.uri)
		mActivity.startActivityForResult(intent, 0x123)

	def on_activity_result(self, requestCode, resultCode, intent):
		if requestCode == 0x123:
			Clock.schedule_once(partial(self.add_picture, self.last_fn), 0)

	def add_picture(self, fn, *args):
		im = Hola.open(fn)
		width, height = im.size
		im.thumbnail((width / 4, height / 4), Hola.ANTIALIAS)
		im.save(fn, quality=95)
		self.root.add_widget(Picture(source = fn))


if __name__ == '__main__':
    CookingApp().run()

# EMULAR: py main.py -m screen:note2,portrait,scale=1
# EMULAR: python2 main.py -m screen:onex,portrait,scale=1
# EMULAR: py main.py -m screen:onex,portrait,scale=1
# EMULAR: py main.py -m screen:note2,portrait,scale=.7
# EMULAR: python main.py -m screen:note2,portrait,scale=.5
# EMULAR: python alerts.py -m screen:note2,portrait,scale=.5
# EMULAR: python alerts.py -m screen:note2,portrait,scale=.8














