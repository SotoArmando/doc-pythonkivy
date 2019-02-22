from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Rectangle
from kivy.graphics.texture import Texture


def horizontal(rgba_left, rgba_right):
    texture = Texture.create(size=(2, 1), colorfmt="rgba")
    pixels = rgba_left + rgba_right
    pixels = [chr(int(v * 255)) for v in pixels]
    buf = ''.join(pixels)
    texture.blit_buffer(buf, colorfmt='rgba', bufferfmt='ubyte')
    return texture


def vertical(rgba_top, rgba_bottom):
    texture = Texture.create(size=(1, 2), colorfmt="rgba")
    pixels = rgba_bottom + rgba_top
    pixels = [chr(int(v * 255)) for v in pixels]
    buf = ''.join(pixels)
    texture.blit_buffer(buf, colorfmt='rgba', bufferfmt='ubyte')
    return texture
    
class MyWidget(Widget):
    def __init__(self, **args):
        super(MyWidget, self).__init__(**args)


        with self.canvas:
            Rectangle(pos=self.pos, size=(1000,1000), texture= horizontal((1, 1, 1, .85), (1, 1, 1, 1)))


class TestApp(App):
    def build(self):
        return MyWidget(size=(200, 200))


if __name__ == '__main__':
    TestApp().run()