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


class Administrar_Inventario(RelativeLayout):
    def __init__(self, **kwargs):
        super(Administrar_Inventario, self).__init__(**kwargs)
        self.add_widget(Image(source = color + "16.png", keep_ratio = False, allow_stretch = True))
        self.root = kwargs["root"]
        self.new_item = {
            "clasificacion": "",
            "item_name": "",
            "marca": "",
            "existencia_total": None,
            "precio_3": None,
            "descripcion": "",
            "precio_2": None,
            "precio_1": None,
            "codigo": "",
            "id": None
        }
        self.campos = [
            "id",
            "item_name",
            "codigo",
            "clasificacion",
            "marca",
            "existencia_total",
            "descripcion",
            "precio_1",
            "precio_2",
            "precio_3",

        ]
        pariente = GridLayout(cols = 1)
        pariente_parent = RelativeLayout()
        pariente_mirror_scroll = ScrollView(size_hint_y = 1, height = 300)
        pariente_mirror_parent = RelativeLayout(size_hint_y = None, height = 150)
        pariente_mirror_parent.add_widget(Image(source = color + "16bb.png", keep_ratio = False , allow_stretch = True))
        pariente_mirror = GridLayout(cols = 10, spacing = [0,1])
        pariente_mirror_parent.add_widget(pariente_mirror)
        pariente_mirror_scroll.add_widget(pariente_mirror_parent)
        pariente_mirror1 = GridLayout(rows = 1 , size_hint_y = None, height = 71)
        pariente_mirror1.add_widget(Button(text = C4+"[b]AGREGAR REGISTRO",on_release = lambda x: self.AGREGAR_REGRISTRO()))
        #pariente_mirror1.add_widget(Button(text = C4+"[b]EDITAR REGISTRO"))
        #pariente_mirror1.add_widget(Button(text = C4+"[b]BORRAR REGISTRO"))
        pariente_mirror1.add_widget(Button(text = C4+"[b]IMPORTAR REGISTROS",on_release = lambda x: self.IMPORTAR_REGISTRO()))
        pariente.add_widget(pariente_mirror_scroll)
        pariente.add_widget(pariente_mirror1)
        pariente_parent.add_widget(Image(source = color + "16bb.png", keep_ratio = False , allow_stretch = True))
        pariente_parent.add_widget(pariente)
        self.add_widget(pariente_parent)
        for i in kwargs["temp"][4][1]:
            if i == "id":
                pariente_mirror.add_widget(Button(size_hint_x = None, width = 50,size_hint_y = None ,text_size = (50, 75), halign = 'center', valign = 'middle', height = 75,markup = True, text = C4+"[b]"+str(i)))
            else:
                pariente_mirror.add_widget(Button(size_hint_y = None ,text_size = (Window.width/10 , 75), halign = 'center', valign = 'middle', height = 75,markup = True, text = C4+"[b]"+str(i)))

        for i in kwargs["temp"][4][0]:
            pariente_mirror_parent.height += 75
            for y in i:
                if y == "id":
                    pariente_mirror.add_widget(A_Button(background_normal = color + "16.png",size_hint_x = None, width = 50,size_hint_y = None ,text_size = (50 , 75), halign = 'center', valign = 'middle', height = 75,markup = True, text = C4+str(i[y])))
                    
                else:
                    pariente_mirror.add_widget(A_Button(background_normal = color + "16.png",size_hint_y = None ,text_size = (Window.width/10 , 75), halign = 'center', valign = 'middle', height = 75,markup = True, text = C4+str(i[y])))
                    
    def AGREGAR_REGRISTRO_on_text(self, x):
        self.new_item[x.parent.parent.campo] = x.text

        
    def AGREGAR_REGRISTRO(self):

        pariente = RelativeLayout(pos_hint = {'center_x':.5, 'center_y':.5},size_hint = (None,None), size = (400,550))
        pariente.add_widget(Image(source = color +"16.png", keep_ratio = False ,allow_stretch = True))
        pariente_gridlayout = GridLayout(cols = 1); pariente.add_widget(pariente_gridlayout)
        pariente_backfield = A_Button(opacity = .50, background_normal = color + "3.png", background_down = color + "3.png")
        for field in self.campos:
            textinput = ClassicTexInput(campo = field, passw = False)
            pariente_gridlayout.add_widget(textinput)
            textinput.intext.bind(text = lambda x,y:self.AGREGAR_REGRISTRO_on_text(x))
            self.new_item[field] = textinput.intext.text
        dualbutton = Dualbutton()
        def Cancelar(x): 
            pariente.parent.remove_widget(pariente)
            pariente_backfield.parent.remove_widget(pariente_backfield)
        def Agregar(x): 
            self.root.data_base_connecttions(tableid = 4, jsondata = self.new_item)
        dualbutton.b2.bind(on_release = Cancelar)
        dualbutton.b1.bind(on_release = Agregar)
        pariente_gridlayout.add_widget(dualbutton)
        self.parent.parent.parent.parent.add_widget(pariente_backfield)
        self.parent.parent.parent.parent.add_widget(pariente)
        
    def IMPORTAR_REGISTRO_ACEPTAR(self,data):
        for i in data:
            self.root.data_base_connecttions(tableid = 4, jsondata = i)
    def IMPORTAR_REGISTRO(self):
        import openpyxl
        from Tkinter import Tk
        from tkFileDialog import askopenfilename
        try:
            Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
            filename = askopenfilename() # show an "Open" dialog box and return the path to the selected file
            print(filename)
            wb = openpyxl.load_workbook(filename)
            sheet = wb.get_sheet_by_name('Hoja1')
            countyData = {}

            print('Reading rows...')
            data = []
            letters = ['A','B','C','D','E','F','G','H','I','J',]
            campos = []
            for row in range(1, sheet.max_row + 1):
                if row == 1:
                    for letter in letters:
                        campos.append(sheet[letter + str(row)].value)
                else:
                    n = {}
                    for letter in letters:
                        x = sheet[letter + str(row)].value
                        if type(x) is long:
                            x = int(x)
                            print x
                        n[campos[letters.index(letter)]] = x
                    data.append(n)

            for i in data: print i

                    
            pariente = RelativeLayout(pos_hint = {'center_x':.5, 'center_y':.5},size_hint = (.95,None), size = (300,550))
            pariente.add_widget(Image(source = color +"16.png", keep_ratio = False ,allow_stretch = True))
            pariente_backfield = A_Button(opacity = .50, background_normal = color + "3.png", background_down = color + "3.png")
            def Cancelar(): 
                pariente.parent.remove_widget(pariente)
                pariente_backfield.parent.remove_widget(pariente_backfield)

            pariente_mirror_scroll = ScrollView(size_hint_y = 1, height = 300)
            pariente_mirror_parent = RelativeLayout(size_hint_y = None, height = 1500)
            pariente_mirror_parent.add_widget(Image(opacity = .24,source = color + "3.png", keep_ratio = False, allow_stretch = True))
            pariente_mirror = GridLayout(cols = 10, spacing = [0,1])
            pariente_mirror_parent.add_widget(pariente_mirror)
            pariente_mirror_scroll.add_widget(pariente_mirror_parent)
            pariente_mirror1 = GridLayout(rows = 1 , size_hint_y = None, height = 71)
            pariente_mirror1.add_widget(Button(text = C4+"[b]ACEPTAR REGISTRO",on_release = lambda x: self.IMPORTAR_REGISTRO_ACEPTAR(data)))
            pariente_mirror1.add_widget(Button(text = C4+"[b]CANCELAR",on_release = lambda x: Cancelar()))
            pariente.add_widget(pariente_mirror_scroll)
            pariente.add_widget(pariente_mirror1)

            for i in self.root.temp[4][1]:
                if i == "id":
                    pariente_mirror.add_widget(Button(size_hint_x = None, width = 50,size_hint_y = None ,text_size = (50, 75), halign = 'center', valign = 'middle', height = 75,markup = True, text = C4+"[b]"+str(i)))
                else:
                    pariente_mirror.add_widget(Button(size_hint_y = None ,text_size = (Window.width/10 , 75), halign = 'center', valign = 'middle', height = 75,markup = True, text = C4+"[b]"+str(i)))

            for i in data:
                for y in i:
                    if y == "id":
                        pariente_mirror.add_widget(Button(size_hint_x = None, width = 50,size_hint_y = None ,text_size = (50 , 75), halign = 'center', valign = 'middle', height = 75,markup = True, text = C4+str(i[y])))
                    else:
                        pariente_mirror.add_widget(Button(size_hint_y = None ,text_size = (Window.width/10 , 75), halign = 'center', valign = 'middle', height = 75,markup = True, text = C4+str(i[y])))
        
            self.parent.parent.parent.parent.add_widget(pariente_backfield)
            self.parent.parent.parent.parent.add_widget(pariente)
        except:
            pass     
