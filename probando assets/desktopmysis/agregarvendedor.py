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


class Agregar_Vendedor(RelativeLayout):
    def __init__(self, **kwargs):
        super(Agregar_Vendedor, self).__init__(**kwargs)
        self.add_widget(Image(source = color + "16.png", keep_ratio = False, allow_stretch = True))
        new_vendedor = {
            "is_active": False,
            "is_superuser": False,
            "is_staff": False,
            "last_login": None,
            "date_joined": None,
            "groups": [],
            "user_permissions": [],
            "username": "",
            "first_name": "",
            "last_name": "",
            "password": "",
            "email": "",
        }
        fields = [
        "first_name",
        "last_name",
        "email",
        "password",
        "username",
        "user_permissions",
        "is_active",
        "is_superuser",
        "is_staff",
        "last_login",
        "date_joined",
        "groups",
        ]
        otherdata = {

        }
        pariente = GridLayout(cols = 1)
        for i in fields:
            if i == "password":
                pariente.add_widget(ClassicTexInput(campo = i, passw = True))
            elif new_vendedor[i] == "":
                pariente.add_widget(ClassicTexInput(campo = i, passw = False))
            else:
                x = ClassicTexInput(campo = i, passw = False)
                x.intext.text = str(new_vendedor[i])
                x.intext.disabled = True
                pariente.add_widget(x)
                
        pariente.add_widget(Label())
        pariente.add_widget(Button(text = C4+"[b]Confirmar",markup = True,size_hint = (None,None), height = 51, width = 300))
        self.add_widget(pariente)