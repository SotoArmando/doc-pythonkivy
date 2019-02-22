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

class jsonlabel(RelativeLayout):
    def __init__(self,**kwargs):
        super(jsonlabel, self).__init__(**kwargs)
        pariente =  GridLayout(rows = 1) ; self.add_widget(pariente)
        pariente.add_widget(Label(markup = True,text_size = (125, self.height),size_hint_x = None, width = 125, text = C4+"[b]"+kwargs["field"], halign = 'left' , valign = 'middle'))
        pariente.add_widget(Label(markup = True,size_hint_x = 1, width = 100, text = C4+kwargs["text"]))

        
class Administrar_Entregas(RelativeLayout):
    def __init__(self, **kwargs):
        super(Administrar_Entregas, self).__init__(**kwargs)
        pariente = GridLayout(cols = 2)   
        registros_parent = GridLayout(cols = 1,spacing = 5, size_hint_y = None, height = 1500)
        registros_parentscroll = ScrollView()
        registro_detailparent = GridLayout(cols = 1)
        
        leftcolumn = GridLayout(cols = 1)
        
        leftcolumn.add_widget(registros_parentscroll)
        registros_parentscroll.add_widget(registros_parent)

        leftcolumn.add_widget(Button(markup = True,text = C4+"Autorizar Entrega", size_hint_y = None, height = 51))
        pariente.add_widget(leftcolumn)
        pariente.add_widget(registro_detailparent)
        
        self.add_widget(pariente)
        for i in kwargs["temp"][0][0]:
            fself = RelativeLayout(size_hint_y = None, height = 200)
            fself.add_widget(Image(source = color + "16bb.png", keep_ratio = False , allow_stretch = True))
            fselfpariente = GridLayout(cols = 2) ; fself.add_widget(fselfpariente)
            
            for field in i:
                fselfpariente.add_widget(jsonlabel(field = field , text = str(i[field])))
            registros_parent.add_widget(fself)
        
        #---------------------------
        accesstoken = "pk.eyJ1IjoiYXJtYW5kbzI5IiwiYSI6ImNpd282ZHJ3azAwMWoydHFuZmJudnNzYzEifQ.12vIF51BCThjrut4Q56sGg"
        sourcex = MapSource(url="https://api.mapbox.com/styles/v1/mapbox/streets-v10/tiles/256/{z}/{x}/{y}?access_token=pk.eyJ1IjoibWFjYXR1cyIsImEiOiJjaXlubGRkdXAwMDJ1MzNwZjdwanhkdnd6In0.eYV9WVlCsI44Ku0HSup7Pg",
        cache_key="custom_map1s",tile_size=256,
        image_ext="jpg", attribution="@Armando Jose Soto Melo")
        self.x_mapview = MapView(size_hint_y = None, height = 350,lat = 18.454651 , lon = -69.971119, zoom = 16, map_source = sourcex)
        
        registro_detailparent.add_widget(self.x_mapview)