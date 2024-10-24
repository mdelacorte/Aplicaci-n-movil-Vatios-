from kivy.app import App
from kivymd.app import MDApp
from kivy.uix.button import Button
import plyer
import requests
import json

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
        dic_electrodomesticos = {'nombre': nombre, 'gasto': gasto}
        js.append(dic_electrodomesticos)
        #y reescribo lo que queria
        with open('datosPrecios/electrodomesticos.txt', 'w') as file:
            file.write(json.dumps(js)) 

update_electrodomesticos(0,'termomix','123')
set_datos_electrodomesticos('television', '33')
set_datos_electrodomesticos('risto', '1234')
set_datos_electrodomesticos('lol', '90')