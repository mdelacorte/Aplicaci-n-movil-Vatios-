from kivy.uix.gridlayout import GridLayout 
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.label import MDLabel, MDIcon
from kivymd.uix.card import MDCard
from kivy.uix.image import Image
from kivymd.uix.button import MDRectangleFlatButton, MDIconButton
from kivy.graphics import Color, Rectangle
import kivy.utils
import kivy.uix.layout
from kivymd.uix.dialog import MDDialog 
import json
from kivy.lang import Builder

# PARA LA BASE DE DATOS DE LOS ELECTRODOMESTICOS
def get_electrodomesticos():
    with open('datosPrecios/electrodomesticos.txt') as file:
        data = file.read()
    js = json.loads(data)
    return js
    #editar .txt para las notificaciones
def update_electrodomesticos(id,dato): #editar los datos
    js = get_electrodomesticos()
    js[id].update({'borrarDato':dato})
    #y reescribo lo que queria d
    with open('datosPrecios/electrodomesticos.txt', 'w') as file:
        file.write(json.dumps(js))  
def delete_electrodomesticos(id):
    js = get_electrodomesticos()
    del js[id]
    with open('datosPrecios/electrodomesticos.txt', 'w') as file:
        file.write(json.dumps(js)) 
def set_datos_electrodomesticos(nombre,gasto): #editar los datos
        with open('datosPrecios/electrodomesticos.txt') as file:
            data = file.read()
        js = json.loads(data) #cargar el str como diccionario
        dic_electrodomesticos = {'nombre': nombre, 'gasto': gasto}
        js.append(dic_electrodomesticos)
        #y reescribo lo que queria
        with open('datosPrecios/electrodomesticos.txt', 'w') as file:
            file.write(json.dumps(js)) 

datoBorrarElectrodomestico = False
class ScrollElectrodomesticos(GridLayout):
    cols = 1
    id = ''
    nombre = ''
    dialog = None
    borrarDato = False
    def __init__(self, **kwargs):
        super().__init__()
        #Editar apariencia canvas
        self.padding = 5
        self.size_hint = (1, 1)
        self.id = str(kwargs['id'])
        self.nombre = str(kwargs['nombre'])
        with self.canvas.before:
            Color(rgb=(kivy.utils.get_color_from_hex('FFFFFF')))
            self.radius = [18]
            self.size_hint = (0.2, 0.15)
            self.rect = Rectangle(size=self.size, pos=self.pos, radius=[18])
        self.bind(pos=self.update_rect, size=self.update_rect)
        
        #float layout en el medio Numero  y PRECIO
        mdCard = MDCard(size_hint_y =None, height = "70dp",orientation="vertical",radius=20, padding  = "10dp")
        layout = MDFloatLayout()
        a = kwargs['imagen_precio']
        #arribisima_label = MDLabel(text = str(kwargs['numero']),halign =  'left', font_style = "Subtitle1", color=(0,0,0,1), size_hint=(1, 1), pos_hint={'center_x': 0.6,'center_y': 0.7})
        nombre_label = MDLabel(text = self.nombre,halign =  'left', font_style = "Subtitle1", bold = True, multiline = True, text_color =(181,178,178,0.75), size_hint=(1, 1), pos_hint={'center_x': 0.5,'center_y': 0.85})
        gastos_introducidos_label = MDLabel(text = "Consumo: " + str(kwargs['gasto']) + "kwh", halign =  'left', font_style = "Caption", multiline = True, text_color =(181,178,178,0.75), size_hint=(0.8, 1), pos_hint={'center_x': 0.4,'center_y': 0.5})
        gastos_ahora_label = MDLabel(text = "Gasto Estimado: " + str(kwargs['gasto_ahora']) + " €/h", halign =  'left', font_style = "Caption", multiline = True, text_color =(181,178,178,0.75), size_hint=(0.8, 1), pos_hint={'center_x': 0.4,'center_y': 0.14})
        #imagen_gastos = Image(source='iconos/' + kwargs['imagen_precio'], size_hint=(0.3, 0.3), pos_hint={'center_x': 0.01,'center_y': 0.5})      
        button = MDIconButton(icon="trash-can",size_hint=(0.3, 0.3), pos_hint={'center_x': 0.89,'center_y': 0.5})

        #arriba.add_widget(arribisima_label)
        layout.add_widget(nombre_label)
        layout.add_widget(gastos_introducidos_label)
        layout.add_widget(gastos_ahora_label)
        
        #layout.add_widget(imagen_gastos)
        button.bind(on_press=self.on_button_press)
        layout.add_widget(button)
        mdCard.add_widget(layout)
        self.add_widget(mdCard)

    #se vaya cambiando el tamaño
    def update_rect(self,*args):
        self.rect.pos = self.pos
        self.rect.size = self.size
        
    def on_button_press(self,instance):
        #eliminar elemento de la lista con confirmacion previa
        print(self.id + " El botón ha sido pulsado")
        self.show_custom_dialog(instance)

    def show_custom_dialog(self,objeto):
        self.dialog = MDDialog(title='¿Desea Borrar el dispositivo ' +self.nombre+ '?',
                            type='custom',
                            buttons = [MDRectangleFlatButton(text="Cancel",on_release=self.close_dialog,size_hint=(0.5,0.5)), 
                            MDRectangleFlatButton(text="Ok",on_release=self.get_data_dialog,size_hint=(0.5,0.5))
                            ]
                            )
        self.dialog.open()

    def close_dialog(self, instance):
        self.dialog.dismiss()

    def get_data_dialog(self, instance_btn):
        print(self.id)
        datos = get_electrodomesticos() 
        update_electrodomesticos(int(self.id),True)
        self.dialog.dismiss()


    