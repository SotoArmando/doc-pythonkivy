#!/usr/bin/env python
# -*- coding: utf-8 -*-
from kivy.config import Config
Config.set('graphics','resizable',0)
import kivy
from kivy.core.window import Window


Window.borderless = True
from kivy.app import App
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.button import Button
import os
from kivy.clock import Clock, mainthread
#CARPETAS DEL PROYECTO
patch = os.path.dirname(os.path.abspath(__file__))
asset = patch + '/assets/drawable-mdpi/'
color = patch + '/colors/'
font = patch + '/fonts/'
import threading
import time
#VARIABLES GLOBALES
Hola = "Hola a todos"

class ThreadingExample(object):
    """ Threading example class
    The run() method will be started and it will run in the background
    until the application exits.
    """
    
    def __init__(self, interval=5,**kwargs):
        """ Constructor
        :type interval: int
        :param interval: Check interval, in seconds
        """
        self.interval = interval
        self.ruun = kwargs["ruun"]
        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True                            # Daemonize thread
        thread.start()                                  # Start the execution

    def run(self):
        """ Method that runs forever """
        while True:
            # Do something
            print('Doing something imporant in the background')
            self.ruun()
            time.sleep(self.interval)

class InterfaceManager(RelativeLayout):
    def __init__(self, **kwargs):
        super(InterfaceManager, self).__init__(**kwargs)

        self.add_widget(Button())
        

      




    def funcion(self):
        print("hola")

class MyApp(App):
    title = 'Basic Application'
    def build(self):
        #Clock.schedule_interval(lambda x: self.dothing(), 3)
        x = ThreadingExample(ruun = self.dothing)
        return InterfaceManager()
    def dothing(self):
        print "hey"
        from pywinauto.findwindows    import find_window
        from pywinauto.win32functions import SetForegroundWindow

        while True:
            try:
                SetForegroundWindow(find_window(title='Basic Application'))
            except:
                print "my faults"

if __name__ in ('__main__', '__android__'):
    MyApp().run()

    
    
    
    
    