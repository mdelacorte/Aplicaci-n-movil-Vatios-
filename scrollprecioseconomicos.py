from kivy.uix.gridlayout import GridLayout 
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.label import MDLabel
from kivy.uix.image import Image
from kivy.graphics import Color, Rectangle
import kivy.utils


class ScrollPreciosEconomicos(GridLayout):
    cols = 1
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

        #float layout en el medio Numero  y PRECIO
       
        arriba = MDFloatLayout()
        #arribisima_label = MDLabel(text = str(kwargs['numero']),halign =  'left', font_style = "Subtitle1", color=(0,0,0,1), size_hint=(1, 1), pos_hint={'center_x': 0.6,'center_y': 0.7})
        arriba_label = MDLabel(text = str(kwargs['numero']) + '. Entre las ' +str(kwargs['hour'])+ ' horas el precio será de '+str(kwargs['price'])+ ' €/Mwh',halign =  'left', font_style = "Subtitle1", multiline = True, text_color =(181,178,178,0.75), size_hint=(0.9, 0.9), pos_hint={'center_x': 0.5,'center_y': 0.5})
        #arriba.add_widget(arribisima_label)
        arriba.add_widget(arriba_label)
        self.add_widget(arriba)

    #se vaya cambiando el tamaño
    def update_rect(self,*args):
        self.rect.pos = self.pos
        self.rect.size = self.size