from kivy.app import App
from kivymd.app import MDApp
from kivy.lang import Builder
from kivymd.uix.floatlayout import MDFloatLayout
from kivy.uix.screenmanager import Screen, ScreenManager
from kivymd.icon_definitions import md_icons
from kivymd.app import MDApp
from datetime import datetime
from kivy.uix.button import ButtonBehavior
from kivy.uix.image import Image
from kivymd.uix.pickers import MDTimePicker
from kivy.lang import Builder
from kivymd.uix.dialog import MDDialog 
from kivymd.uix.button import MDRectangleFlatButton
# it will allow us to make interval calls
from kivy.clock import Clock
import requests
import json
import os
import plyer
from scrollviewprecios import ScrollViewPrecios
from scrollprecioseconomicos import ScrollPreciosEconomicos
from scrollelectrodomesticos import ScrollElectrodomesticos
from apiprecioluz import preciosPVPC
import time
import setuptools


#CONSTANTES APLICACION
notificaciones = ['boolean_precios_dia','boolean_precio_mas_bajo_x','boolean_horas_mas_baratas_dia','boolean_tramo_horas_mas_baratas_dia','boolean_mostrar_todos_los_precios','boolean_editar_imagen_precios']
id_notificaciones = ['switch_precios_dia','switch_precio_mas_bajo_x','switch_horas_mas_baratas_dia','switch_tramo_horas_mas_baratas_dia','switch_mostrar_todos_los_precios','switch_editar_imagen_precios']
horas_notificaciones = ['hora_precios_dia','tiempo_bajo_x','precios_bajo_x','numero_precios_dia_barato_x','hora_precios_dia_barato_x','tramo_horas_baratas','rango_horas_baratas_para_tramo','precio_minimo_imagen','precio_maximo_imagen','numero_precios_economicos']

precio_hora_electrodomesticos = 0


#DATOS ALARMAS en datosPrecios/configuracionNotificaciones.txt
def get_constantes():
    with open('datosPrecios/constantes.txt') as file:
        data = file.read()
    js = json.loads(data)
    return js
    #editar .txt para las notificaciones
def set_constantes(datoEditar,estado): #editar los datos
    with open('datosPrecios/constantes.txt') as file:
        data = file.read()
    js = json.loads(data) #cargar el str como diccionario
    js.update({datoEditar:estado}) #cambiar a el dato que quiero sobreescribir
    #y reescribo lo que queria
    with open('datosPrecios/constantes.txt', 'w') as file:
        file.write(json.dumps(js))  

def get_datos_dia():
    with open('datosPrecios/datosDia.txt') as file:
        data = file.read()
    js = json.loads(data)
    return js #devuelve todos los datos del dia
#GUARDAR DATOS MAXIMO en datosPrecios/maximosPeninsula.txt
def get_datos_maximo():
    with open('datosPrecios/maximos.txt') as file:
        data = file.read()
    js = json.loads(data)
    return js
#GUARDAR DATOS MINIMO en datosPrecios/minimosPeninsula.txt
def get_datos_minimo():
    with open('datosPrecios/minimos.txt') as file:
        data = file.read()
    js = json.loads(data)
    return js
#GUARDAR DATOS + ECONOMICOS EN datosPrecios/preciosDiaEconomico.txt 
def get_datos_precio_economico():
    with open('datosPrecios/preciosEconomicos.txt') as file:
        data = file.read()
    js = json.loads(data)
    return js 
#DATOS ALARMAS en datosPrecios/interruptor.txt
def get_datos_notificaciones():
    with open('datosPrecios/interruptor.txt') as file:
        data = file.read()
    js = json.loads(data)
    return js
#DATOS ALARMAS en datosPrecios/configuracionNotificaciones.txt
def get_horas_notificaciones():
    with open('datosPrecios/configuracionNotificaciones.txt') as file:
        data = file.read()
    js = json.loads(data)
    return js
    #editar .txt para las notificaciones
def set_horas_notificaciones(datoEditar,tiempo_alarma): #editar los datos
    with open('datosPrecios/configuracionNotificaciones.txt') as file:
        data = file.read()
    js = json.loads(data) #cargar el str como diccionario
    js.update({datoEditar:tiempo_alarma}) #cambiar a el dato que quiero sobreescribir
    #y reescribo lo que queria
    with open('datosPrecios/configuracionNotificaciones.txt', 'w') as file:
        file.write(json.dumps(js))  
def set_datos_notificaciones(datoEditar,datoSobreescribir): #editar los datos
        with open('datosPrecios/interruptor.txt') as file:
            data = file.read()
        js = json.loads(data) #cargar el str como diccionario
        js.update({datoEditar:datoSobreescribir}) #cambiar a el dato que quiero sobreescribir
        #y reescribo lo que queria
        with open('datosPrecios/interruptor.txt', 'w') as file:
            file.write(json.dumps(js))    
#DATOS ALARMAS en datosPrecios/interruptor.txt
def get_datos_notificaciones():
    with open('datosPrecios/interruptor.txt') as file:
        data = file.read()
    js = json.loads(data)
    return js
# PARA LA BASE DE DATOS DE LOS ELECTRODOMESTICOS
def get_electrodomesticos():
    with open('datosPrecios/electrodomesticos.txt') as file:
        data = file.read()
    js = json.loads(data)
    return js
    #editar .txt para las notificaciones
def update_electrodomesticos(id,nombre,gasto): #editar los datos
    js = get_electrodomesticos()
    js[id].update({'nombre':nombre})
    js[id].update({'gasto':gasto})
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
    dic_electrodomesticos = {'nombre': nombre, 'gasto': gasto,'borrarDato': False}
    js.append(dic_electrodomesticos)
    #y reescribo lo que queria
    with open('datosPrecios/electrodomesticos.txt', 'w') as file:
        file.write(json.dumps(js)) 

def set_zona_horaria(ubicacion): #editar los datos
    zona_horaria = {'zona_horaria': ubicacion}
    with open('datosPrecios/zonaHoraria.txt', 'w') as file:
        file.write(json.dumps(zona_horaria)) 
    
def get_zona_horaria():
    with open('datosPrecios/zonaHoraria.txt') as file:
        data = file.read()
    js = json.loads(data)
    return js
#clases DIALOG
class MinutosAntesPrecioBajo(MDFloatLayout):
    pass
class PrecioMasBajo(MDFloatLayout):
    pass
class PrecioEconomico(MDFloatLayout):
    pass
class PrecioMinimoImagen(MDFloatLayout):
    pass
class PrecioMaximoImagen(MDFloatLayout):
    pass
class NumeroPrecioEconomico(MDFloatLayout):
    pass
class NombreElectrodomestico(MDFloatLayout):
    pass
class GastoElectrodomestico(MDFloatLayout):
    pass
class VistaElectrodomestico(MDFloatLayout):
    pass
#Controlador de ventanas
class WindowManager(ScreenManager):
    pass
class HomeScreen(Screen):
    pass
class AlarmaScreen(Screen):
    pass
class ElectrodomesticoScreen(Screen):
    hora = 0
    minuto = 0
    tiempo_alarma = ''
    tiempo_ahora = ''
    horas = ['00-01','01-02','02-03','03-04','04-05','05-06','06-07','07-08','08-09',
    '09-10','10-11','11-12','12-13','13-14','14-15','15-16','16-17','17-18','18-19',
    '19-20','20-21','21-22','22-23','23-24']

    def get_time(self,instance, time):
        #guardamos en la base de datos el dato de la hora
        self.hora = int(time.hour)
        self.minuto = int(time.minute)
        constantes = get_constantes()
        self.guardar_tiempo_alarma()
        actual = self.get_datos_dia_actual(self.hora)
        precio_hora_electrodomesticos = int(actual['price'])
        cambio_hora_electrodomesticos_label = self.ids['datos_hora_electrodomestico']
        cambio_hora_electrodomesticos_label.text = "Precio a las " + constantes["hora_electrodomesticos"] + 'h ' 
        cambio_hora_electrodomesticos_label.otroText = str(precio_hora_electrodomesticos) +' €/Mwh'
    def get_datos_dia_actual(self,hora):
        rango_hora = int(hora)
        with open('datosPrecios/datosDia.txt') as file:
            data = file.read()
        js = json.loads(data)
        return js[rango_hora] #devuelve todos los datos de la hora en la que estamos
    #funcion adicional para obtener el mes dependiendo del numero que haya
    def on_cancel(self,instance, time):
        pass
    def guardar_tiempo_alarma(self):
        if self.hora <10:
            if self.minuto < 10:
                notificacion = '0'+str(self.hora)+':0'+str(self.minuto)
            else:
                notificacion = '0'+str(self.hora)+':'+str(self.minuto)
        else:
            if self.minuto < 10:
                notificacion = str(self.hora)+':0'+str(self.minuto)
            else:
                notificacion = str(self.hora)+':'+str(self.minuto)
        self.tiempo_alarma = notificacion
        set_constantes("hora_electrodomesticos",notificacion)
        print("DENTRO", notificacion)
        set_constantes("cambio_hora_electrodomesticos", True)
    def guardar_tiempo_ahora(self,hora,minutos):
        if hora <10:
            if minutos < 10:
                notificacion = '0'+str(hora)+':0'+str(minutos)
            else:
                notificacion = '0'+str(hora)+':'+str(minutos)
        else:
            if minutos< 10:
                notificacion = str(hora)+':0'+str(minutos)
            else:
                notificacion = str(hora)+':'+str(minutos)
        self.tiempo_ahora = notificacion
        
    def show_time_picker(self): 
        constantes = get_constantes()
        
        actual_time = time.asctime()
        minutos = actual_time[14] + actual_time[15]
        hora =  actual_time[11] + actual_time[12]
        self.guardar_tiempo_ahora(int(hora),int(minutos))
        #establece como el default el que tenemos guardado en los .txt
        dafault_time = datetime.strptime(self.tiempo_ahora,'%H:%M').time()
        time_dialog = MDTimePicker()
        time_dialog.set_time(dafault_time)
        time_dialog.bind(on_cancel= self.on_cancel,time = self.get_time)
        time_dialog.open()

class AnadirElectrodomestico(Screen):
    nombre = ''
    gasto = ''
    dialog = None
    dialog1 = None
    dialog2 = None

    def show_custom_dialog(self,objeto,id):
        if id == 1:
            content_cls = NombreElectrodomestico()
            self.dialog1 = MDDialog(title='Nombre del electrodoméstico',
                            content_cls=content_cls,
                            type='custom',
                            buttons = [MDRectangleFlatButton(text="Cancel",on_release=self.close_dialog,size_hint=(0.5,0.5)), 
                            MDRectangleFlatButton(text="Ok",size_hint=(0.5,0.5),on_release=lambda x:self.get_data_dialog1(x,content_cls))
                            ]
                            )
            self.dialog1.open()
        else:
            content_cls = GastoElectrodomestico()
            self.dialog2 = MDDialog(title='Gastos por hora del electrodoméstico',
                            content_cls=content_cls,
                            type='custom',
                            buttons = [MDRectangleFlatButton(text="Cancel",on_release=self.close_dialog,size_hint=(0.5,0.5)), 
                            MDRectangleFlatButton(text="Ok",size_hint=(0.5,0.5),on_release=lambda x: self.get_data_dialog2(x,content_cls))
                            ]
                            )
            self.dialog2.open()
    def close_and_delete(self, instance_btn):
        self.nombre = ''
        self.gasto = ''
        if self.dialog1:
            self.dialog1.dismiss()
        if self.dialog2:
            self.dialog2.dismiss()
        if self.dialog:
            self.dialog.dismiss()
        self.set_dato_nombre()
        self.set_dato_gasto()
    def close_dialog(self, instance):
        if self.dialog1:
            self.dialog1.dismiss()
        if self.dialog2:
            self.dialog2.dismiss()
        if self.dialog:
            self.dialog.dismiss()
    def get_data_dialog1(self, instance_btn, content_cls):
        textfield = content_cls.ids.nombre_electrodomestico
        valor = textfield._get_text()
        self.nombre =  str(valor)
        self.set_dato_nombre()
        #set_datos_electrodomesticos()
        #self.update_database(valor,'nombre_electrodomestico')
        self.close_dialog(instance_btn)
    def get_data_dialog2(self, instance_btn, content_cls):
        textfield = content_cls.ids.gasto_electrodomestico
        valor = textfield._get_text()
        self.gasto =  str(valor)
        self.set_dato_gasto()
        #self.update_database(valor,'precios_bajo_x')
        self.close_dialog(instance_btn)
    def update_database(self, instance_btn):
        print(self.nombre, self.gasto)
        if self.nombre != '' and self.gasto != '':
            set_datos_electrodomesticos(self.nombre,self.gasto)
            self.nombre = ''
            self.gasto = ''
            nombre_electrodomestico_label = self.ids['nombre_electrodomestico']
            nombre_electrodomestico_label.text = "Nombre: " 
            nombre_electrodomestico_label = self.ids['gasto_electrodomestico']
            nombre_electrodomestico_label.text = "Gasto por Hora: "
            #valor global, añadir widget true
            set_constantes("añadir_electrodomestico", True)
            return True
        else:
            return False
    def set_dato_nombre(self):
        nombre_electrodomestico_label = self.ids['nombre_electrodomestico']
        nombre_electrodomestico_label.text = "Nombre: " + self.nombre
    def set_dato_gasto(self):
        nombre_electrodomestico_label = self.ids['gasto_electrodomestico']
        nombre_electrodomestico_label.text = "Gasto por Hora: " + self.gasto
    def dialogo_informacion_mal_insertada(self, instance_btn):
        self.dialog = MDDialog(title='¡¡ Información Incompleta !!',
                        buttons = [ MDRectangleFlatButton(text="Ok",size_hint=(0.5,0.5),on_release=self.close_dialog)
                        ]
                        )
        self.dialog.open()
class HorasEconomicas(Screen):
    dialog = None
                
    def show_custom_dialog(self,objeto):
        content_cls = NumeroPrecioEconomico()
        self.dialog = MDDialog(title='¿Cuántos precios económicos de hoy desea ver?',
                            content_cls=content_cls,
                            type='custom',
                            buttons = [MDRectangleFlatButton(text="Cancel",on_release=self.close_dialog,size_hint=(0.5,0.5)), 
                            MDRectangleFlatButton(text="Ok",size_hint=(0.5,0.5),on_release=lambda x:self.get_data_dialog(x,content_cls))
                            ]
                            )
        self.dialog.open()
    def close_dialog(self, instance):
        self.dialog.dismiss()
    def get_data_dialog(self, instance_btn, content_cls):
        textfield = content_cls.ids.numero_precios_economicos
        valor = textfield._get_text()
        self.update_database(valor,'numero_precios_economicos')
        self.close_dialog(instance_btn)
    def update_database(self,valor,edicion):
        set_constantes("cambio_numero_precios_economicos",True)
        if valor != '':
            if (int(valor) >=0):
                set_horas_notificaciones(edicion,str(valor))
class SettingScreen(Screen):
    checks = []
    #switch click precios del dia
    def switch_click(self,butonObj,identificator): 
        switch_actual = self.ids[id_notificaciones[identificator]]
        if switch_actual.source == 'iconos/boton_on.png':
            #y añado en un diccionario que esta variable es "false"
            set_datos_notificaciones(notificaciones[identificator],False)
            switch_actual.source = 'iconos/boton_off.png'
            set_constantes("cambio_ver_precio_todos_los_dias", True)
        else:
           switch_actual.source = 'iconos/boton_on.png'
           set_datos_notificaciones(notificaciones[identificator],True)
           set_constantes("cambio_ver_precio_todos_los_dias", True)
           #y añado en un diccionario que esta variable es "true"

    def checkbox_click(self, instance, value, ubicacion):
        set_zona_horaria(ubicacion)
        if value == True:
            self.checks.append(ubicacion)
            tops = ''
            for x in self.checks:
                tops = f'{tops} {x}'
            set_constantes("cambio_ubicacion", True)
        else:
            self.checks.remove(ubicacion)
            tops = ''
            for x in self.checks:
                tops = f'{tops} {x}'

#CLASES AJUSTES
class EditarImagenPrecios(Screen):
    dialog1 = None
    dialog2 = None
    #switch click precios del dia
    def switch_click(self,butonObj,identificator): 
        switch_actual = self.ids[id_notificaciones[identificator]]
        if switch_actual.source == 'iconos/boton_on.png':
            #y añado en un diccionario que esta variable es "false"
            set_datos_notificaciones(notificaciones[identificator],False)
            switch_actual.source = 'iconos/boton_off.png'
            set_constantes("switch_editar_imagen_precios", True)
        else:
           switch_actual.source = 'iconos/boton_on.png'
           set_datos_notificaciones(notificaciones[identificator],True)
           set_constantes("switch_editar_imagen_precios", True)
           #y añado en un diccionario que esta variable es "true"
    def show_custom_dialog(self,objeto,id):
        if id == 1:
            content_cls = PrecioMinimoImagen()
            self.dialog1 = MDDialog(title='Inserte el Precio Minimo',
                            content_cls=content_cls,
                            type='custom',
                            buttons = [MDRectangleFlatButton(text="Cancel",on_release=self.close_dialog,size_hint=(0.5,0.5)), 
                            MDRectangleFlatButton(text="Ok",size_hint=(0.5,0.5),on_release=lambda x:self.get_data_dialog1(x,content_cls))
                            ]
                            )
            self.dialog1.open()
        else:
            content_cls = PrecioMaximoImagen()
            self.dialog2 = MDDialog(title='Inserte el Precio Máximo',
                            content_cls=content_cls,
                            type='custom',
                            buttons = [MDRectangleFlatButton(text="Cancel",on_release=self.close_dialog,size_hint=(0.5,0.5)), 
                            MDRectangleFlatButton(text="Ok",size_hint=(0.5,0.5),on_release=lambda x:self.get_data_dialog2(x,content_cls))
                            ]
                            )
            self.dialog2.open()
    def close_dialog(self, instance):
        if self.dialog1:
            self.dialog1.dismiss()
        if self.dialog2:
            self.dialog2.dismiss()
    def get_data_dialog1(self, instance_btn, content_cls):
        textfield = content_cls.ids.precio_minimo_imagen
        valor = textfield._get_text()
        self.update_database(valor,'precio_minimo_imagen')
        self.close_dialog(instance_btn)
    def get_data_dialog2(self, instance_btn, content_cls):
        textfield = content_cls.ids.precio_maximo_imagen
        valor = textfield._get_text()
        self.update_database(valor,'precio_maximo_imagen')
        self.close_dialog(instance_btn)       
    def update_database(self,valor,edicion):
        set_constantes("cambio_editar_imagen_precios", True)
        if valor != '':
            if (int(valor) >=0):
                set_horas_notificaciones(edicion,str(valor))
#CLASES NOTIFICACIONES
class MinimosYMaximosDia(Screen):
    hora = 0
    minuto = 0
    tiempo_alarma = ''
    id = 0
    #switch click precios del dia
    def switch_click(self,butonObj,identificator): 
        switch_actual = self.ids[id_notificaciones[identificator]]
        if switch_actual.source == 'iconos/boton_on.png':
            #y añado en un diccionario que esta variable es "false"
            set_datos_notificaciones(notificaciones[identificator],False)
            switch_actual.source = 'iconos/boton_off.png'
            set_constantes("cambio_ver_precio_todos_los_dias",True)
        else:
            switch_actual.source = 'iconos/boton_on.png'
            set_datos_notificaciones(notificaciones[identificator],True)
            set_constantes("cambio_ver_precio_todos_los_dias",True)
#y añado en un diccionario que esta variable es "true"
        #get time
    def get_time(self,instance, time):
        #guardamos en la base de datos el dato de la hora
        self.hora = int(time.hour)
        self.minuto = int(time.minute)
        self.guardar_tiempo_alarma()
        self.ids[horas_notificaciones[self.id]].text = "Hora Alarma: " + str(time) + ' h'
        set_horas_notificaciones(horas_notificaciones[self.id],self.tiempo_alarma)
    
    def on_cancel(self,instance, time):
        pass
    def guardar_tiempo_alarma(self):
        if self.hora <10:
            if self.minuto < 10:
                notificacion = '0'+str(self.hora)+':0'+str(self.minuto)
            else:
                notificacion = '0'+str(self.hora)+':'+str(self.minuto)
        else:
            if self.minuto < 10:
                notificacion = str(self.hora)+':0'+str(self.minuto)
            else:
                notificacion = str(self.hora)+':'+str(self.minuto)
        self.tiempo_alarma = notificacion

    def show_time_picker(self,id): 
        #0 hora_precios_dia, #1hora_precios_dia_barato_x 
        #2 tramo_horas_baratas, rango_horas_baratas_para_tramo
        notificaciones = get_horas_notificaciones()
        self.id = id
        #abre los datos guardados de las notificaciones
        hora_notificacion = str(notificaciones[horas_notificaciones[id]])
        #establece como el default el que tenemos guardado en los .txt
        dafault_time = datetime.strptime(hora_notificacion,'%H:%M').time()
        time_dialog = MDTimePicker()
        tiempo = time_dialog.time
        time_dialog.set_time(dafault_time)
        self.id_usado = id       
        time_dialog.bind(on_cancel= self.on_cancel,time = self.get_time)
        time_dialog.open()

class PrecioBajo(Screen):
    dialog1 = None
    dialog2 = None
    def switch_click(self,butonObj,identificator): 
        switch_actual = self.ids[id_notificaciones[identificator]]
        if switch_actual.source == 'iconos/boton_on.png':
            #y añado en un diccionario que esta variable es "false"
            set_datos_notificaciones(notificaciones[identificator],False)
            switch_actual.source = 'iconos/boton_off.png'
        else:
           switch_actual.source = 'iconos/boton_on.png'
           set_datos_notificaciones(notificaciones[identificator],True)
           #y añado en un diccionario que esta variable es "true"
    def show_custom_dialog(self,objeto,id):
        if id == 1:
            content_cls = MinutosAntesPrecioBajo()
            self.dialog1 = MDDialog(title='¿Cuántos Minutos Antes?',
                            content_cls=content_cls,
                            type='custom',
                            buttons = [MDRectangleFlatButton(text="Cancel",on_release=self.close_dialog,size_hint=(0.5,0.5)), 
                            MDRectangleFlatButton(text="Ok",size_hint=(0.5,0.5),on_release=lambda x:self.get_data_dialog1(x,content_cls))
                            ]
                            )
            self.dialog1.open()
        else:
            content_cls = PrecioMasBajo()
            self.dialog2 = MDDialog(title='Precio mínimo desde el que sonará la alarma?',
                            content_cls=content_cls,
                            type='custom',
                            buttons = [MDRectangleFlatButton(text="Cancel",on_release=self.close_dialog,size_hint=(0.5,0.5)), 
                            MDRectangleFlatButton(text="Ok",size_hint=(0.5,0.5),on_release=lambda x:self.get_data_dialog2(x,content_cls))
                            ]
                            )
            self.dialog2.open()
    def close_dialog(self, instance):
        if self.dialog1:
            self.dialog1.dismiss()
        if self.dialog2:
            self.dialog2.dismiss()
    def get_data_dialog1(self, instance_btn, content_cls):
        textfield = content_cls.ids.tiempo_bajo_x
        valor = textfield._get_text()
        self.update_database(valor,'tiempo_bajo_x')
        self.close_dialog(instance_btn)
    def get_data_dialog2(self, instance_btn, content_cls):
        textfield = content_cls.ids.precios_bajo_x
        valor = textfield._get_text()
        self.update_database(valor,'precios_bajo_x')
        self.close_dialog(instance_btn)
    def update_database(self,valor,edicion):
        set_constantes("cambio_precio_bajo_x", True)
        if valor != '':
            if (int(valor) >=0):
                set_horas_notificaciones(edicion,str(valor))
class HorasBaratas(Screen):
    hora = 0
    minuto = 0
    tiempo_alarma = ''
    id = 0
    dialog = None
    def switch_click(self,butonObj,identificator): 
        switch_actual = self.ids[id_notificaciones[identificator]]
        if switch_actual.source == 'iconos/boton_on.png':
            #y añado en un diccionario que esta variable es "false"
            set_datos_notificaciones(notificaciones[identificator],False)
            switch_actual.source = 'iconos/boton_off.png'
        else:
           switch_actual.source = 'iconos/boton_on.png'
           set_datos_notificaciones(notificaciones[identificator],True)
           #y añado en un diccionario que esta variable es "true"

    def show_custom_dialog(self,objeto):
        content_cls = PrecioEconomico()
        self.dialog = MDDialog(title='¿Cuántas Horas?',
                            content_cls=content_cls,
                            type='custom',
                            buttons = [MDRectangleFlatButton(text="Cancel",on_release=self.close_dialog,size_hint=(0.5,0.5)), 
                            MDRectangleFlatButton(text="Ok",size_hint=(0.5,0.5),on_release=lambda x:self.get_data_dialog(x,content_cls))
                            ]
                            )
        self.dialog.open()
    def close_dialog(self, instance):
        self.dialog.dismiss()
    def get_data_dialog(self, instance_btn, content_cls):
        textfield = content_cls.ids.numero_precios_dia_barato_x
        valor = textfield._get_text()
        self.update_database(valor,'numero_precios_dia_barato_x')
        self.close_dialog(instance_btn)
    def update_database(self,valor,edicion):
        set_constantes("cambio_numero_economico",True)
        if valor != '':
            if (int(valor) >=0):
                set_horas_notificaciones(edicion,str(valor))
    #ahora hora
    def get_time(self,instance, time):
        #guardamos en la base de datos el dato de la hora
        self.hora = int(time.hour)
        self.minuto = int(time.minute)
        self.guardar_tiempo_alarma()
        self.ids[horas_notificaciones[self.id]].text = "Hora Alarma: " + str(self.tiempo_alarma) + ' h'
        set_horas_notificaciones(horas_notificaciones[self.id],self.tiempo_alarma) 
    def on_cancel(self,instance, time):
        pass
    def guardar_tiempo_alarma(self):
        if self.hora <10:
            if self.minuto < 10:
                notificacion = '0'+str(self.hora)+':0'+str(self.minuto)
            else:
                notificacion = '0'+str(self.hora)+':'+str(self.minuto)
        else:
            if self.minuto < 10:
                notificacion = str(self.hora)+':0'+str(self.minuto)
            else:
                notificacion = str(self.hora)+':'+str(self.minuto)
        self.tiempo_alarma = notificacion
    def show_time_picker(self,boton,id): 
        #0 hora_precios_dia, #1hora_precios_dia_barato_x 
        #2 tramo_horas_baratas, rango_horas_baratas_para_tramo
        notificaciones = get_horas_notificaciones()
        self.id = id
        #abre los datos guardados de las notificaciones
        hora_notificacion = str(notificaciones[horas_notificaciones[id]])
        #establece como el default el que tenemos guardado en los .txt
        dafault_time = datetime.strptime(hora_notificacion,'%H:%S').time()
        time_dialog = MDTimePicker()
        tiempo = time_dialog.time
        time_dialog.set_time(dafault_time)
        self.id_usado = id       
        time_dialog.bind(on_cancel= self.on_cancel,time = self.get_time)
        time_dialog.open()

#Imagenes que funcionan como botones
class ImageButton(ButtonBehavior, Image):
    pass
#MAIN CLASS 
class MainApp(MDApp):
    #datos fecha actual
    fecha_ahora = datetime.now()
    i = 0
    #url_precio_economico = requests.get("https://api.preciodelaluz.org/v1/prices/cheapests?zone=PCB&n=2").json()
    update_actual_minuto = 0
    update_actual_hora = 0
    update_notificacion_boolean_precios_dia = 0
    update_notificacion_boolean_precios_bajo_x = 0
    update_notificacion_boolean_precios_baratos =0
    
    horas = ['00-01','01-02','02-03','03-04','04-05','05-06','06-07','07-08','08-09',
        '09-10','10-11','11-12','12-13','13-14','14-15','15-16','16-17','17-18','18-19',
        '19-20','20-21','21-22','22-23','23-24']

    def build(self):
        self.icon = 'vatios_logo.png'
        self.theme_cls.theme_style = "Light"
        #Window.clearcolor= (1,1,1) #para que el fondo sea blanco
        GUI = Builder.load_file("mainWindow.kv") #pillar el diseño
        return GUI
        #return GUI
    def on_start(self):
        global precio_hora_electrodomesticos
        constantes = get_constantes()
        #Establecer FECHA app  
        fecha = str(self.fecha_ahora.day)+ " de " + self.get_mes(self.fecha_ahora.month)+ ", "+ str(self.fecha_ahora.year)
        fecha_label= self.root.get_screen('home_screen').ids.fecha_label
        fecha_label.text = fecha
        #obtener datos de hora
        actual_time = time.asctime()
        hora = actual_time[11] + actual_time[12]
        minutos = actual_time[14] + actual_time[15]
        self.guardar_tiempo_ahora(int(hora),int(minutos))

        #comprobar que el dia en el que estamos es el correcto
        dia = self.set_dia_hoy()
        if dia!= get_datos_maximo()['fecha']:
            #llamamos a la clase "apiprecio Luz, y la inicializamos"
            horaejecucion = datetime.now().hour
            actualizarDatos = preciosPVPC(horaejecucion)
            actualizarDatos.vaciarDatosDelDia()
            actualizarDatos.obtenerDatos()
        #Rellenar datos pantalla
        self.dato_actual(hora)
        self.add_widget_numero_precios_economicos()
        self.add_widget_electrodomesticos()
        self.set_imagen_precios()
        #al iniciar, ponemos dato hora como la hora a la que hemos abierto la app
        
        actual = self.get_datos_dia_actual(hora)
        precio_hora_electrodomesticos = int(actual['price'])
        cambio_hora_electrodomesticos_label = self.root.get_screen('electrodomestico_screen').ids['datos_hora_electrodomestico']
        cambio_hora_electrodomesticos_label.text = "Precio a las " + hora +":"+ minutos+ 'h ' 
        cambio_hora_electrodomesticos_label.otroText = str(precio_hora_electrodomesticos) +' €/Mwh'
        
        zona_horaria = get_zona_horaria()
        self.root.get_screen('setting_screen').ids[zona_horaria['zona_horaria']].active = True
        #rellenar datos
        self.datos_dia()
        self.set_datos_configurables()
        self.check_switch() #inserta todos los "switch" como se encuentran en la base de datos
        self.insertar_precios_dia()
        #Ir comprobando datos, para que se vayan actualizando
        Clock.schedule_interval(self.comprobar_datos, 1)
        return super().on_start()
    def comprobar_datos(self,*args):
        actual_time = time.asctime()
        dato = get_datos_notificaciones()
        
        minutos = actual_time[14] + actual_time[15]
        hora =  actual_time[11] + actual_time[12]
        constantes = get_constantes()
        global precio_hora_electrodomesticos
        #comprobar siempre si han decidido cambiar los colores minimos y maximos de los precios
        if constantes["cambio_ubicacion"]:
            horaejecucion = datetime.now().hour
            actualizarDatos = preciosPVPC(horaejecucion)
            actualizarDatos.vaciarDatosDelDia()
            actualizarDatos.obtenerDatos()
            #actualizar todos los demas datos visualmente:
            self.dato_actual(hora)
            self.add_widget_numero_precios_economicos()
            self.add_widget_electrodomesticos()
            self.insertar_precios_dia()
            #rellenar datos
            self.datos_dia()
            self.set_datos_configurables()
            set_constantes("cambio_ubicacion", False)


        self.set_imagen_precios()
        self.check_for_notifications(hora,minutos)
        id = self.check_electrodomesticos()
        if constantes["borrarDato"]:
            delete_electrodomesticos(id)
            self.add_widget_electrodomesticos()
            set_constantes("borrarDato", False)

        #ajustes alarmas
        if constantes["cambio_precio_bajo_x"] == True or constantes["cambio_numero_economico"] or constantes["cambio_editar_imagen_precios"]:
            self.set_datos_configurables()
            set_constantes("cambio_precio_bajo_x",False)
            set_constantes("cambio_numero_economico",False)
            set_constantes("cambio_editar_imagen_precios",False)
            
        if constantes["switch_editar_imagen_precios"]:
            self.insertar_precios_dia()
            set_constantes("switch_editar_imagen_precios", False)
        #precios del dia
        if constantes["cambio_ver_precio_todos_los_dias"] == True :
            self.insertar_precios_dia()
            set_constantes("cambio_ver_precio_todos_los_dias",False)
        
        if constantes["añadir_electrodomestico"] == True:
            self.add_widget_electrodomesticos()
            set_constantes("añadir_electrodomestico",False)
        #cambio enseñar numero precios economicos
        if constantes["cambio_numero_precios_economicos"] == True:
            self.set_datos_configurables()
            self.add_widget_numero_precios_economicos()
            set_constantes("cambio_numero_precios_economicos",False)
        
        if constantes["cambio_hora_electrodomesticos"] == True:
            dato = constantes["hora_electrodomesticos"]
            print(dato)
            hora = dato[0]+dato[1]
            actual = self.get_datos_dia_actual(hora)
            precio_hora_electrodomesticos = int(actual['price'])
            cambio_hora_electrodomesticos_label = self.root.get_screen('electrodomestico_screen').ids['datos_hora_electrodomestico']
            cambio_hora_electrodomesticos_label.text = "Precio a las " + constantes["hora_electrodomesticos"] + 'h: ' 
            cambio_hora_electrodomesticos_label.otroText = str(precio_hora_electrodomesticos) +' €/Mwh'
            set_constantes("cambio_hora_electrodomesticos", False)
            self.add_widget_electrodomesticos()

        #self.check_for_notifications(hora,minutos)
        #self.update_notificaciones()

        #si los minutos estan en 00, cambio de hora, por lo que hay que llamar a la aplicaion para que actualice la hora actual
        if minutos == '00':
            if self.update_actual_minuto == 0:
                self.update_actual_minuto +=1
                #tengo que comprobar primero si esta encendida la switch de ajustes
                self.insertar_precios_dia()
                self.dato_actual(hora)

            elif self.update_actual_minuto == 60: #por los 60 segundos hasta el proximo minuto
                self.update_actual_minuto =0
            else:
                self.update_actual_minuto +=1
            
        if hora == '00':
            if self.update_actual_hora == 0:
                self.update_actual_hora +=1
                horaejecucion = datetime.now().hour
                actualizarDatos = preciosPVPC(horaejecucion)
                actualizarDatos.vaciarDatosDelDia()
                actualizarDatos.obtenerDatosPeninsula()
                self.dato_actual(hora)
                self.datos_dia() #maximo y minimo  
            elif self.update_actual_hora == 3600: #por los 60 mins hasta la proxima hora
                self.update_actual_hora =0
            else:
                self.update_actual_hora +=1
    #Insertar precios del dia GRID
    def insertar_precios_dia(self):
        #obtener grid
        boolean_dato = get_datos_notificaciones()
        dato = get_horas_notificaciones()
        precio_minimo = int(dato['precio_minimo_imagen'])
        precio_maximo = int(dato['precio_maximo_imagen'])
        counter = -1
        actual_time = time.asctime()
        hora =  actual_time[11] + actual_time[12]
        datos_dia = get_datos_dia()
        indice_hora = int(hora) +1
        imagen = 'precio_malo.png'
        precios_del_dia = self.root.get_screen('home_screen').ids['informacion_precio_hora']
        precios_del_dia.clear_widgets()
        
        for dia in datos_dia:
            precios_dia = dia['price']
            hora_dia = dia['hour']
            barato_dia = dia['is-cheap']
            indice_hora = int(hora) +1
            counter += 1 #aumentamos el counterxw
            if boolean_dato['boolean_mostrar_todos_los_precios']:
                if boolean_dato['boolean_editar_imagen_precios']:
                    if int(precios_dia) <=precio_minimo:
                        imagen = "precio_bueno.png"  # PRECIO BARATO
                    else:
                        if int(precios_dia) <=precio_maximo:
                            
                            imagen = "precio_medio.png"  #PRECIO MEDIO 
                        else:
                            imagen = "precio_malo.png"  #PRECIO CARO
                else:
                    if barato_dia:
                        imagen = 'precio_bueno.png'
                    else:
                        imagen = 'precio_malo.png'
                precios = ScrollViewPrecios(price=str(precios_dia),
                hour=str(hora_dia),
                imagen_precio=imagen)
                precios_del_dia.add_widget(precios)

            elif boolean_dato['boolean_mostrar_todos_los_precios'] == False:
                if (counter >= indice_hora):
                    if boolean_dato['boolean_editar_imagen_precios']:
                        if (int(precios_dia) <= precio_minimo):
                            imagen = "precio_bueno.png"  # PRECIO BARATO
                        else:
                            if int(precios_dia) <=precio_maximo:
                                imagen = "precio_medio.png"  #PRECIO MEDIO 
                            else:
                                imagen = "precio_malo.png"  #PRECIO CARO
                    else:
                        if barato_dia:
                            imagen = 'precio_bueno.png'
                        else:
                            imagen = 'precio_malo.png'
                    precios = ScrollViewPrecios(price=str(precios_dia),
                    hour=str(hora_dia),
                    imagen_precio=imagen)
                    precios_del_dia.add_widget(precios)
        
        counter = -1
    #datos recuadro actual
    def dato_actual(self,hora):
        #Precio ACTUAL
        actual = self.get_datos_dia_actual(hora)
        precio_actual = actual['price']
        hora_actual = actual['hour']
        ahora_precio= self.root.get_screen('home_screen').ids.precio_actual
        ahora_precio.subtext = str(precio_actual) + " €/Mwh"
        ahora_precio.items_count = str(hora_actual) + " h"
    def check_electrodomesticos(self):
        constantes = get_constantes()
        electrodomesticos = get_electrodomesticos()
        count = 0
        for elem in electrodomesticos:
            if elem['borrarDato'] == True:
                id = count
                set_constantes("borrarDato",True)
            count +=1
        if constantes["borrarDato"]:
            return id
        else:
            return 9999
    #datos dia, maximo minimo medio...
    def datos_dia(self):
        #Precio MINIMO
        minimo = get_datos_minimo()
        precio_minimo = minimo['price']
        hora_minimo = minimo['hour']
        precio_minimo_label = self.root.get_screen('home_screen').ids.precio_minimo
        precio_minimo_label.subtext = str(precio_minimo) + " €/Mwh"
        precio_minimo_label.items_count = str(hora_minimo) + " h"
        #Precio MAXIMO
        maximo = get_datos_maximo()
        precio_maximo = maximo['price']
        hora_maximo = maximo['hour']
        precio_maximo_label = self.root.get_screen('home_screen').ids.precio_maximo
        precio_maximo_label.subtext = str(precio_maximo) + ' €/Mwh'
        precio_maximo_label.items_count = str(hora_maximo) + " h"  
    #check switch is correct when turning on application
    def check_switch(self):
        notif = get_datos_notificaciones()
        #switch precios del dia
        if notif[notificaciones[0]]:
            self.root.get_screen('minimosYmaximosDia').ids.switch_precios_dia.source = "iconos/boton_on.png"
        #switch precio mas bajo x
        if notif[notificaciones[1]]:
            self.root.get_screen('precioBajo').ids.switch_precio_mas_bajo_x.source = "iconos/boton_on.png"
        #switch horas mas baratas dia
        if notif[notificaciones[2]]:
            self.root.get_screen('horasBaratas').ids.switch_horas_mas_baratas_dia.source = "iconos/boton_on.png"
        #switch tramo horas baratas dia
        #if notif[notificaciones[1]]:
        #    self.root.get_screen('minimosYmaximosDia').ids.switch_tramo_horas_mas_baratas_dia.source = "iconos/boton_on.png"   
        #switch mostrar todos los precios
        if notif[notificaciones[4]]:
            self.root.get_screen('setting_screen').ids.switch_mostrar_todos_los_precios.source = "iconos/boton_on.png"  
        #switch mostrar todos los precios
        if notif[notificaciones[5]]:
            self.root.get_screen('editarImagenPrecios').ids.switch_editar_imagen_precios.source = "iconos/boton_on.png" #switch editar imagen precios             
    #DATOS inicio app
    def set_datos_configurables(self):
        datos = get_horas_notificaciones()
        self.set_datos_alarma(datos)
        self.set_datos_imagen_precio(datos)
        self.set_datos_numero_precios_economicos(datos)
        self.set_datos_electrodomesticos()
    def set_datos_electrodomesticos(self):
        pass
        #insertar datos
    def set_datos_numero_precios_economicos(self,datos):
        numero_precios_economicos = datos[horas_notificaciones[9]]
        numero_precios_economicos_label = self.root.get_screen('horasEconomicas').ids[horas_notificaciones[9]]
        numero_precios_economicos_label.text = "Precios a consultar: " + numero_precios_economicos
    def set_datos_imagen_precio(self,datos):
        precio_minimo_imagen = datos[horas_notificaciones[7]]
        precio_maximo_imagen = datos[horas_notificaciones[8]]
        #precio minimo
        precio_minimo_imagen_label = self.root.get_screen('editarImagenPrecios').ids[horas_notificaciones[7]]
        precio_minimo_imagen_label.text = "Precio Minimo: " + precio_minimo_imagen + ' €MKw/h'
        #precio maximo
        precio_maximo_imagen_label = self.root.get_screen('editarImagenPrecios').ids[horas_notificaciones[8]]
        precio_maximo_imagen_label.text = "Precio Maximo:  " + precio_maximo_imagen + ' €MKw/h'
    def set_datos_alarma(self, datos):
        #ALARMA
        hora_precios_dia = datos[horas_notificaciones[0]]
        tiempo_bajo_x = datos[horas_notificaciones[1]]
        precios_bajo_x = datos[horas_notificaciones[2]]
        numero_precios_dia_barato_x = datos[horas_notificaciones[3]]
        hora_precios_dia_barato_x = datos[horas_notificaciones[4]]
        tramo_horas_baratas = datos[horas_notificaciones[5]]
        rango_horas_baratas_para_tramo = datos[horas_notificaciones[6]]

        #ALARMA PRECIOS DEL DIA
        hora_precios_dia_label = self.root.get_screen('minimosYmaximosDia').ids[horas_notificaciones[0]]
        hora_precios_dia_label.text = "Hora Alarma: " + hora_precios_dia + ' h'

        #ALARMA PRECIO MAS BAJO DE X
        tiempo_bajo_x_label = self.root.get_screen('precioBajo').ids[horas_notificaciones[1]]
        tiempo_bajo_x_label.text = 'Minutos Antes: ' + tiempo_bajo_x + ' mins'
        precios_bajo_x_label = self.root.get_screen('precioBajo').ids[horas_notificaciones[2]]
        precios_bajo_x_label.text = 'Precio: ' + precios_bajo_x + ' €MKw/h'

        #ALARMA X PRECIOS MAS BARATOS DEL DIA
        numero_precios_dia_barato_x_label = self.root.get_screen('horasBaratas').ids[horas_notificaciones[3]]
        numero_precios_dia_barato_x_label.text = "Número: " + numero_precios_dia_barato_x
        hora_precios_dia_barato_x_label = self.root.get_screen('horasBaratas').ids[horas_notificaciones[4]]
        hora_precios_dia_barato_x_label.text = 'Hora: ' + hora_precios_dia_barato_x + ' h'

        #tramo_horas_baratas_label = self.root.get_screen('alarma_screen').ids[horas_notificaciones[5]]
        #tramo_horas_baratas_label.text = 'Minutos Antes: ' +tramo_horas_baratas + ' mins'

        #rango_horas_baratas_para_tramo_label = self.root.get_screen('alarma_screen').ids[horas_notificaciones[6]]
        #rango_horas_baratas_para_tramo_label.text = rango_horas_baratas_para_tramo  
    #funciones "extras"
    #NOTIFICACIONES
    def check_for_notifications(self,hora,minutos):
        notificaciones = get_datos_notificaciones()
        datos = get_horas_notificaciones()
        #NOTIFICACIONES PRECIOS MAXIMOS Y MINIMOS :)
        if notificaciones['boolean_precios_dia']: #si es true, notificar
            tiempoDato = datos['hora_precios_dia']
            horaDato = tiempoDato[0]+tiempoDato[1]
            minutoDato = tiempoDato[3]+tiempoDato[4]
            #boolean_precios_dia
            if str(hora) == horaDato and str(minutos)== minutoDato:#si son las 12 de la noche, precios del dia
                if self.update_notificacion_boolean_precios_dia == 0:
                    self.notification_boolean_precios_dia()
                    self.update_notificacion_boolean_precios_dia +=1
                elif self.update_notificacion_boolean_precios_dia == 60: #por los 60 segundos hasta el proximo minuto
                    self.update_notificacion_boolean_precios_dia =0
                else:
                    self.update_notificacion_boolean_precios_dia +=1
            else:
                self.update_notificacion_boolean_precios_dia = 0
        #NOTIFICACIONES MAS BAJO DE X :)
        if notificaciones['boolean_precio_mas_bajo_x']:#si es true, notificar
            tiempo_bajo_x = datos['tiempo_bajo_x'] #tiempo antes de que sea la hora del precio establecido
            precios_bajo_x = datos['precios_bajo_x'] #precio establecido para que suene la alarma
            horas_precio_bajo_x = self.horas_precio_bajo_x(precios_bajo_x)   
            for i in range(len(horas_precio_bajo_x)):
                #obtener una de las horas
                if i%2 == 0:
                    hora_precio = horas_precio_bajo_x[i]
                    hora_empieza = str(hora_precio[0]) + (hora_precio[1])
                    #si no ha puesto para que la alarma suene x tiempo antes
                    if tiempo_bajo_x == '0' or tiempo_bajo_x == '00':
                        if hora_empieza == hora:
                            if self.update_notificacion_boolean_precios_bajo_x == 0:
                                #al ser la misma hora a la que el precio baja, se manda notificacion
                                self.notification_boolean_precios_bajo_x(tiempo_bajo_x,precios_bajo_x)
                                self.update_notificacion_boolean_precios_bajo_x +=1
                                
                            elif self.update_notificacion_boolean_precios_bajo_x == 60: #por los 60 segundos hasta el proximo minuto
                                self.update_notificacion_boolean_precios_bajo_x =0
                            else:
                                self.update_notificacion_boolean_precios_bajo_x +=1
                        else:
                            self.update_notificacion_boolean_precios_bajo_x = 0
                    else:
                        #si son 10, o mas minutos antes, tenemos que mirar minimo 1 hora antes.
                        if int(hora_empieza)-1 == int(hora):
                            sesenta = int(minutos)+int(tiempo_bajo_x)
                            if sesenta == 60:
                                if self.update_notificacion_boolean_precios_bajo_x == 0:
                                #al ser la misma hora a la que el precio baja, se manda notificacion
                                    self.notification_boolean_precios_bajo_x(tiempo_bajo_x,precios_bajo_x)
                                    self.update_notificacion_boolean_precios_bajo_x +=1
                                elif self.update_notificacion_boolean_precios_bajo_x == 60: #por los 60 segundos hasta el proximo minuto
                                    self.update_notificacion_boolean_precios_bajo_x =0
                                else:
                                    self.update_notificacion_boolean_precios_bajo_x +=1
                            else:
                                self.update_notificacion_boolean_precios_bajo_x = 0
        #NOTIFICACIONES HORAS MAS BARATAS DEL DIA
        if notificaciones['boolean_horas_mas_baratas_dia']:
            hora_alarma = datos['hora_precios_dia_barato_x']
            numero = datos['numero_precios_dia_barato_x']
            horaDato = hora_alarma[0]+hora_alarma[1]
            minutoDato = hora_alarma[3]+hora_alarma[4]
            #boolean_precios_dia
            if str(hora) == horaDato and str(minutos)== minutoDato:#si son las 12 de la noche, precios del dia
                if self.update_notificacion_boolean_precios_baratos == 0:
                    self.notificacion_boolean_horas_mas_baratas_dia(numero)
                    self.update_notificacion_boolean_precios_baratos +=1
                elif self.update_notificacion_boolean_precios_baratos == 60: #por los 60 segundos hasta el proximo minuto
                    self.update_notificacion_boolean_precios_baratos =0
                else:
                    self.update_notificacion_boolean_precios_baratos +=1
            else:
                self.update_notificacion_boolean_precios_baratos = 0
        #añadir alarma cuando se inserten los precios del dia CONFIGURABLE, 
    def notification_boolean_precios_dia(self):
        #get e insertar en el mensaje los distintos precios del dia
        maximo = get_datos_maximo()
        minimo = get_datos_minimo()
        maximo_datos = 'Máximo: ' + str(maximo['price']) + '€/Mwh, de ' + str(maximo['hour'] + ' horas')
        minimo_datos = 'Mínimo: ' + str(minimo['price']) + '€/Mwh, de ' + str(minimo['hour']+ ' horas')
        datos = maximo_datos+'\n' + ' & ' + '\n'+minimo_datos
        plyer.notification.notify(title='¡Datos Máximos del Día!', app_name = 'Vatios', app_icon = r'vatios_logo.png',message=maximo_datos)
        plyer.notification.notify(title='¡Datos Mínimos del Día!', app_name = 'Vatios', app_icon = r'vatios_logo.png',message=minimo_datos)
    def notification_boolean_precios_bajo_x(self, minutos, precio):
        #get e insertar en el mensaje los distintos precios del dia
        dato = ''
        if minutos == '0':
            dato = 'El precio de la electricidad ha bajado de :' + str(precio) + '€/Mwh'
        else:
            dato = 'En ' + str(minutos) + ' minutos el precio bajará de : ' + str(precio) + '€/Mwh'
        plyer.notification.notify(title='¡El precio de la electricidad Baja!', app_name = 'Vatios', app_icon = r'vatios_logo.png',message=dato)
    def notificacion_boolean_horas_mas_baratas_dia(self,numero):
        hora_precios_dia_barato_x = get_datos_precio_economico()
        dato = ''
        i = 0
        for elem in hora_precios_dia_barato_x:
            datos = str(i+1) +": De "+ str(elem['hour']) +  "h, Habrá un precio de: " + str(elem['price'])
            dato += datos + "\n"
            i +=1
        plyer.notification.notify(title= 'Las ' + str(numero)+' horas mas baratas del día!', app_name = 'Vatios', app_icon = r'vatios_logo.png',message=dato)
    #añade a una lista las horas mas bajas de x
    def horas_precio_bajo_x(self,precios_bajo_x):
        datos = get_datos_dia()
        lista = []
        for elem in datos:
            if elem['price'] <= float(precios_bajo_x):
                lista.append(elem['hour'])
                lista.append(elem['price'])
        return lista
    #CAMBIO COLOR SEGUN EL PRECIO 
    def cambio_color_precio(self,actual,id): 
        barato = False
        precio_color_actual = self.root.get_screen('home_screen').ids[id]
        if (actual['is-cheap']):
            barato = True
        if barato == True:
            #si el precio es barato, cambiaremos la imagen por la precio_bueno
            precio_color_actual.image = "iconos/precio_bueno.png"   
        else:
            precio_color_actual.image = "iconos/precio_malo.png" 
    #añadir widget con datos economicos
    def add_widget_numero_precios_economicos(self):
        #primero obtener el json con los datos economicos
        datos = get_horas_notificaciones()
        numeroConfigurable = datos[horas_notificaciones[9]]
        #set_datos_precio_economico(numeroConfigurable)
        datosEconomicos = get_datos_precio_economico()
        count = 1
        precios_economicos = self.root.get_screen('horasEconomicas').ids['informacion_precio_economico']
        precios_economicos.clear_widgets()
        i = 0
        
        for dato in datosEconomicos:
            if i < int(numeroConfigurable):
                precio = dato['price']
                hora = dato['hour']
                precios = ScrollPreciosEconomicos(numero=str(count),
                                                price=str(precio),
                                                hour=hora)
                count +=1 
                precios_economicos.add_widget(precios)
                i +=1
        #añadir widget con datos economicos
    def add_widget_electrodomesticos(self):
        global precio_hora_electrodomesticos
        #primero obtener el json con los datos economicos
        electrodomesticos = get_electrodomesticos()

        electrodomesticos_screen = self.root.get_screen('electrodomestico_screen').ids['informacion_electrodomesticos']
        electrodomesticos_screen.clear_widgets()
        
        if precio_hora_electrodomesticos == 0:
            actual_time = time.asctime()
            hora = actual_time[11] + actual_time[12]
            actual = self.get_datos_dia_actual(hora)
            precio_hora_electrodomesticos = float(actual['price'])

        count = 0
        for dato in electrodomesticos:
            nombre = dato['nombre']
            gasto = dato['gasto']
            gasto_ahora = self.calculo_gasto_por_hora(float(gasto))
            electrodomestico = ScrollElectrodomesticos(
                                        id = str(count),
                                        nombre=str(nombre),
                                        gasto = str(gasto),
                                        gasto_ahora=str(gasto_ahora),
                                        imagen_precio='precio_medio_horizontal.png')
            count +=1 
            electrodomesticos_screen.add_widget(electrodomestico)
    def calculo_gasto_por_hora(self,gasto):
        global precio_hora_electrodomesticos
        cambio_a_mvh = float(gasto)/1000
        gasto = float(precio_hora_electrodomesticos) * cambio_a_mvh
        return gasto
    def set_imagen_precios(self):
        actual_time = time.asctime()
        #print(actual_time)
        hora =  actual_time[11] + actual_time[12]
        #solo vamos a cambiar las del ahora, minimo y maximo, 
        #ya que las del dia, se comprueban en insertar_precios_dia
        dato = get_datos_notificaciones()
        precio = get_horas_notificaciones()

        imagen_minimo = precio['precio_minimo_imagen']
        imagen_maximo = precio['precio_maximo_imagen']
        precio_ahora = self.get_datos_dia_actual(hora)
        precio_minimo = get_datos_minimo()
        precio_maximo = get_datos_maximo()

        precio_color_actual = self.root.get_screen('home_screen').ids.precio_actual
        precio_color_minimo = self.root.get_screen('home_screen').ids.precio_minimo
        precio_color_maximo = self.root.get_screen('home_screen').ids.precio_maximo

        if dato['boolean_editar_imagen_precios']: #si es true, los colores seran los establecidos por el usuario
            #ahora 
            if int(precio_ahora['price']) <=int(imagen_minimo):
                precio_color_actual.image = "iconos/precio_bueno.png"  # PRECIO BARATO
            else:
                if int(precio_ahora['price']) <=int(imagen_maximo):
                    precio_color_actual.image = "iconos/precio_medio.png"  #PRECIO MEDIO 
                else:
                    precio_color_actual.image = "iconos/precio_malo.png"  #PRECIO CARO 
            #minimo 
            if int(precio_minimo['price']) <=int(imagen_minimo):
                precio_color_minimo.image = "iconos/precio_bueno.png"  # PRECIO BARATO
            else:
                if int(precio_minimo['price']) <=int(imagen_maximo):
                    precio_color_minimo.image = "iconos/precio_medio.png"  #PRECIO MEDIO 
                else:
                    precio_color_minimo.image = "iconos/precio_malo.png"  #PRECIO CARO

            #maximo
            if int(precio_maximo['price']) <=int(imagen_minimo):
                precio_color_maximo.image = "iconos/precio_bueno.png"  
            else:
                if int(precio_maximo['price']) <=int(imagen_maximo):
                    precio_color_maximo.image = "iconos/precio_medio.png"  
                else:
                    precio_color_maximo.image = "iconos/precio_malo.png"  
        
        else: #los datos como habian sido establecidos
            #color del precio actual
            self.cambio_color_precio(precio_ahora,'precio_actual')
            self.cambio_color_precio(precio_minimo,'precio_minimo')
            self.cambio_color_precio(precio_maximo,'precio_maximo')
    def set_dia_hoy(self):
        now = datetime.now().date()
        palabras = str(now).split('-')
        final = [palabras[2],'-',palabras[1],'-',palabras[0]]
        fecha = ''
        for elem in final:
            fecha += elem
        return fecha    
    def get_datos_dia_actual(self,hora):
        if self.i == 1:
            rango_hora = self.horas[int(hora)+1]
        else:
            rango_hora = self.horas[int(hora)]
        with open('datosPrecios/datosDia.txt') as file:
            data = file.read()
        js = json.loads(data)
        data = dict
        for i in js:
            if i['hour'] == rango_hora:
                data = i
        return data #devuelve todos los datos de la hora en la que estamos
    #funcion adicional para obtener el mes dependiendo del numero que haya
    def get_mes(self,mes):
        fecha = ['Enero','Febrero','Marzo','Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiempre', 'Octubre', 'Noviembre']
        return (fecha[mes-1])
    def guardar_tiempo_ahora(self,hora,minuto):
        if hora <10:
            if minuto < 10:
                notificacion = '0'+str(hora)+':0'+str(minuto)
            else:
                notificacion = '0'+str(hora)+':'+str(minuto)
        else:
            if minuto < 10:
                notificacion = str(hora)+':0'+str(minuto)
            else:
                notificacion = str(hora)+':'+str(minuto)
        set_constantes("hora_electrodomesticos", notificacion)

    #SERVICIOS 
    def start_service():
        from jnius import autoclass #clases java de forma dinamica desde python
        service = autoclass("org.vatios.vatioservicesapp.ServiceVatios") 
        mActivity = autoclass("org.kivy.android.PythonActivity").mActivity
        argument = '' #esto es lo que se le pasa al servicio, lo ideal es un JSON
        service.start(mActivity, argument)
        return service
    
#para el kv precios
if __name__ == '__main__':
    MainApp().run()


