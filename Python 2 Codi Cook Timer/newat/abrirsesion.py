from __init__ import *
asset = patch + '/new_assets/'

class AbrirSesion(Screen):
    def __init__(self,**kwargs):
        super(AbrirSesion, self).__init__(**kwargs)

                
class MyApp(App):
    def build(self):
        return AbrirSesion()
 

if __name__ in ('__main__', '__android__'):
    MyApp().run()