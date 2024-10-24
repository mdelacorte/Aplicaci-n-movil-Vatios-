from kivy.uix.gridlayout import GridLayout 
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.label import MDLabel
from kivy.uix.image import Image
from kivy.graphics import Color, Rectangle
import kivy.utils

class ScrollViewPrecios(GridLayout):
    rows = 1
    def __init__(self, **kwargs):
        super().__init__()
        #Editar apariencia canvas
        self.padding = 5
        self.size_hint = (0.2, 0.15)
        with self.canvas.before:
            Color(rgb=(kivy.utils.get_color_from_hex('FFFFFF')))
            self.radius = [18]
            self.size_hint = (0.2, 0.15)
            self.rect = Rectangle(size=self.size, pos=self.pos, radius=[18])
        self.bind(pos=self.update_rect, size=self.update_rect)

        #se necesita left layout HORA
        izq = MDFloatLayout()
        label_izq = MDLabel(text = str(kwargs['hour'])+ ' h',halign =  'left', valign='middle', font_style = "Caption", color=(181,178,178,0.75), size_hint=(1, 1),  pos_hint={'center_x': 0.7,'center_y': 0.5})
        #añadirlo al widget
        izq.add_widget(label_izq)

        #float layout en el medio PRECIO
        medio = MDFloatLayout()
        medio_label = MDLabel(text = str(kwargs['price'])+ ' €/Mwh',halign =  'center', valign='middle', font_style = "Subtitle1", bold=True, color=(0,0,0,1), size_hint=(1, 1), pos_hint={'center_x': 0.5,'center_y': 0.5})
        #añadirlo al widget
        medio.add_widget(medio_label)

        #float layout en la dcha IMAGEN
        dcha = MDFloatLayout()
        dcha_image = Image(source='iconos/' + kwargs['imagen_precio'], size_hint=(0.3, 0.3), pos_hint={'center_x': 0.75,'center_y': 0.5})
        #añadirlo al widget
        dcha.add_widget(dcha_image)
        
        self.add_widget(izq)
        self.add_widget(medio)
        self.add_widget(dcha)

    #se vaya cambiando el tamaño
    def update_rect(self,*args):
        self.rect.pos = self.pos
        self.rect.size = self.size