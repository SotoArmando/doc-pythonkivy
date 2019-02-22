
import sys
from os.path import dirname, join, abspath
sys.path.append(dirname(dirname(abspath(__file__))))
from __dep__ import *
from itertools import chain
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
    
#CARPETAS DEL PROYECTO
asset = join(dirname(dirname(abspath(__file__))), '_assets\\')
color = join(dirname(dirname(abspath(__file__))), '_colors\\')
font = join(dirname(dirname(abspath(__file__))), '_fonts\\')

class Button(Button):
    font_name = font + "segoeui.ttf" 
    font_size = 13
class SpriteShow(RelativeLayout):
    def __init__(self,**kwargs):
        super(SpriteShow, self).__init__(**kwargs)
        self.size_hint_x = None
        self.width = 124
        title = Label(text = "[color=#000000]"+kwargs["text"], markup = True, size_hint_y = None, height = 34)
        button = Image(source = kwargs["source"])
        grid = GridLayout(cols = 1,padding = [8,8,8,0]); grid.add_widget(button); grid.add_widget(title)
        self.add_widget(grid)
class Container(RelativeLayout): pass
    
        
        
class Workboard(Container):
    def __init__(self,**kwargs):
        super(Workboard, self).__init__(**kwargs)
        columnlefttitle = Button(text = "[color=#000000]Personal Space",background_normal = color + "16b.png",markup = True, size_hint_y = None, height = 32)
        columnlefttitle1 = Button(text = "[color=#000000]Choose Folder DIR",background_normal = color + "16b.png",markup = True, size_hint_y = None, height = 32)
        columnlefttrelatgrid = GridLayout(cols = 1, padding = [0,0,0,0]);columnlefttrelatgrid.add_widget(columnlefttitle);columnlefttrelatgrid.add_widget(columnlefttitle1)
        columnlefttrelat = RelativeLayout(size_hint_x = .3);columnlefttrelat.add_widget(Image(x = -1, opacity = .04,source = color + "3.png", keep_ratio = False, allow_stretch = True));columnlefttrelat.add_widget(columnlefttrelatgrid)
        columncenterworktablegrid = GridLayout(rows = 1, size_hint_x = None, width = 300)
        columncentermenubutton1 = Button(opacity = .54,text = "[color=#000000]Split in",background_normal = color + "16b.png",markup = True, size_hint_y = None, height = 32)
        columncentermenubutton2 = Button(opacity = .54,text = "[color=#000000]Settings",background_normal = color + "16b.png",markup = True, size_hint_y = None, height = 32)
        columncentermenubutton3 = Button(opacity = .54,text = "[color=#000000]",background_normal = color + "16b.png",markup = True, size_hint_y = None, height = 32)
        columncentermenu = GridLayout(rows = 1, size_hint_y =  1);columncentermenu.add_widget(columncentermenubutton1);columncentermenu.add_widget(columncentermenubutton2);columncentermenu.add_widget(columncentermenubutton3);
        columncentermenuback = RelativeLayout(size_hint_y =  None, height = dp(54));columncentermenuback.add_widget(columncentermenu)
        columncentertitle = Button(text = "[color=#000000]Preview",background_normal = color + "16b.png",markup = True, size_hint_y = None, height = 32)
        columncenterbox = RelativeLayout(); columncenterbox.add_widget(Image(source =  "giphy.gif", anim_delay = 0.25/15.0));columncenterbox.add_widget(Label(text = "[color=#000000][size=38]60 \n[/size][size=18]Fotogramas",line_height = .80, markup= True, size_hint = (None,None), size = (150,300), pos_hint = {'center_x':.9,'center_y':.1},text_size = (150,300), valign = 'middle', halign = 'center'))#0.25 = 4FPS
        columncenterscroll = ScrollView(); columncenterscroll.add_widget(columncenterworktablegrid)
        columncenterworktable = RelativeLayout(size_hint_y = .33); columncenterworktable.add_widget(Image(opacity = .04,source = color + "3.png", keep_ratio = False, allow_stretch = True)); columncenterworktable.add_widget(columncenterscroll)
        columncenter = GridLayout(cols = 1);columncenter.add_widget(columncentertitle);columncenter.add_widget(columncentermenuback);columncenter.add_widget(columncenterbox);columncenter.add_widget(columncenterworktable)
        columnrighttitle = Button(text = "[color=#000000]Properties",background_normal = color + "16b.png",markup = True, size_hint_y = None, height = 32)
        columnrightrelatgrid = GridLayout(cols = 1); columnrightrelatgrid.add_widget(columnrighttitle)
        columnrightrelat = RelativeLayout(size_hint_x = .3);columnrightrelat.add_widget(Image(x = 1, opacity = .04,source = color + "3.png", keep_ratio = False, allow_stretch = True));columnrightrelat.add_widget(columnrightrelatgrid);
        workspace = GridLayout(cols = 3); workspace.add_widget(columnlefttrelat);workspace.add_widget(columncenter);workspace.add_widget(columnrightrelat);
        self.workspacerelat = RelativeLayout()
        workspacerelatparent = RelativeLayout();workspacerelatparent.add_widget(self.workspacerelat); workspacerelatparent.add_widget(workspace); 

        button0 = (Button(text = "[color=#000000]Archivo",markup = True,size_hint_x = None,width = 100,opacity = .84,background_normal = color+'16.png',background_down = color+'16bb.png'))
        button1 = (Button(text = "[color=#000000]Editar",markup = True,size_hint_x = None,width = 100,opacity = .84,background_normal = color+'16.png',background_down = color+'16bb.png'))
        button2 = (Button(text = "[color=#000000]Extra",markup = True,size_hint_x = None,width = 100,opacity = .84,background_normal = color+'16.png',background_down = color+'16bb.png'))
        bargrid = GridLayout(rows = 1, y = 1 , spacing = 1); bargrid.add_widget(button0);bargrid.add_widget(button1);bargrid.add_widget(button2);
        backgroundsource = Image(source = color + "16bb.png", size_hint_x = None, width = 3000, keep_ratio  = False, allow_stretch  = True)
        bargridpiz = RelativeLayout(size_hint_y = None, height = 32); bargridpiz.add_widget(backgroundsource); bargridpiz.add_widget(bargrid)
        grid = GridLayout(cols = 1);grid.add_widget(bargridpiz); grid.add_widget(workspacerelatparent)
        
        self.add_widget(grid)

        with self.workspacerelat.canvas:
            Color(1,1,1,1)
            Rectangle(size = (Window.width, Window.height - 32), pos = (0,0), texture = vertical((1,1,1, .75),(1,1,1,1)))
        
        
        self.receptordesprites = columncenterworktablegrid
        self.load_sprites()
        
    def load_sprites(self,*args):
        from workingcode.splitimages import SplitImages
        
        spliter = SplitImages()
    
        
        rutas = spliter.processImage('giphy.gif')
        for i in rutas: self.receptordesprites.add_widget(SpriteShow(source = i, text = os.path.basename(i))); self.receptordesprites.width += 124
        
    def on_size(self,*args):
        self.workspacerelat.canvas.clear()
        with self.workspacerelat.canvas:
            Color(1,1,1,1)
            Rectangle(size = (Window.width, Window.height - 32), pos = (0,0), texture = vertical((1,1,1, .75),(1,1,1,1)))
            
class YourAppNameApp(App):
    def build(self):
        return Workboard()

if __name__ == '__main__':
    YourAppNameApp().run()