import kivy
from kivy.app import App
from kivy.uix.widget import Widget
import cython
import kivent_core

class TestGame(Widget):
    def __init__(self, **kwargs):
        super(TestGame, self).__init__(**kwargs)
        self.gameworld.init_gameworld([], callback=self.init_app)
        self.static = {}
    def init_app(self):
        self.setup_states()
        self.set_state()
    def load_activities(self):
        from activities import Activites
    def setup_states(self):
        self.gameworld.add_state(state_name='main', 
            systems_added=[],
            systems_removed=[], systems_paused=[],
            systems_unpaused=[],
            screenmanager_screen='main')

    def set_roles(self):
        self.static{"roles"} = [
        {Nivel:'Estandar'},
        {Nivel:'Programador'},
        {Nivel:'Usuario'},
        {Nivel:'Administrador'},
        ]
    
    def set_state(self):
        self.gameworld.state = 'main'

class YourAppNameApp(App):
    def build(self):
        pass

if __name__ == '__main__':
    YourAppNameApp().run()
