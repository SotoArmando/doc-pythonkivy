from kivy.app import App
from kivy.uix.stacklayout import StackLayout
from kivy.lang import Builder

Builder.load_string("""
<Example>:
    Image:
        source: 'creditcard.png'
        size_hint: None,None
        size: 64,64
    Scatter:
        pos: 0,0
        size_hint: None,None
        size: 64,64
        do_rotation: False
        do_scale: False
        do_translation: False
        rotation: 90
        Image:
            source: 'creditcard.png'
            size_hint: None,None
            size: 64,64

""")

class Example(App, StackLayout):
    def build(self):
        return self

if __name__ == "__main__":
    Example().run()
