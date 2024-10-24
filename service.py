from time import sleep
import requests
import json
import os
import plyer

def get_datos_maximo():
    with open('datosPrecios/precioMaximo.txt') as file:
        data = file.read()
    js = json.loads(data)
    return js

def get_datos_minimo():
    with open('datosPrecios/precioMinimo.txt') as file:
        data = file.read()
    js = json.loads(data)
    return js

if __name__ == '__main__':
    print("servicio runeando")
    sleep(5)        
    #get e insertar en el mensaje los distintos precios del dia
    #maximo = get_datos_maximo()
    #minimo = get_datos_minimo()
    #maximo_datos = 'Maximo: ' + str(maximo['price']) + '€/Mwh, de ' + str(maximo['hour'] + ' horas')
    #minimo_datos = 'Minimo: ' + str(minimo['price']) + '€/Mwh, de ' + str(minimo['hour']+ ' horas')
    #datos = maximo_datos+'\n' + ' & ' + '\n'+minimo_datos
    #plyer.notification.notify(title='¡Datos del Día!', app_name = 'Vatios', app_icon = r'vatios_logo.png',message=datos)