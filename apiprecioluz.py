import requests
import json
import statistics
from datetime import datetime
import sys

# Configurar geolocalizacion del precio Mediande el GeoID: 8741 - Peninsula, 8742 - Canarias, 8743 - Baleares, 8744 - Ceuta, 8745 - Melilla

class preciosPVPC():

    token = "bb7a390d79c2e34fd5fe4ad814cf378b5728f74ef5a952e6240245d8f7de3912"
    ## PREPARAR LA LLAMADA A LA API
    url = 'https://api.esios.ree.es/indicators/1001'
    headers = {'Accept':'application/json; application/vnd.esios-api-v2+json','Content-Type':'application/json','Host':'api.esios.ree.es','x-api-key': 'bb7a390d79c2e34fd5fe4ad814cf378b5728f74ef5a952e6240245d8f7de3912'}
    accedido = False
    response = requests
    json_data = json
    bajomedia =  0
    proximahorabm = 0
    itemsbajomedia = int(0)
    horaejecucion = datetime.now().hour
    migeoid = 8741

    def get_zona_horaria(self):
        with open('datosPrecios/zonaHoraria.txt') as file:
            data = file.read()
        js = json.loads(data)
        return js


    def __init__(self, horaEjecucion):
        horaEjecucion = horaEjecucion
        self.response = requests.get(self.url, headers=self.headers)
        if self.response.status_code == 200:
            self.accedido = True
            self.json_data = json.loads(self.response.text)
            zona_horaria = self.get_zona_horaria()
            if zona_horaria['zona_horaria'] == 'peninsula':
                self.migeoid = 8741
            else:
                self.migeoid = 8744
            self.vaciarDatosDelDia()
            self.obtenerDatos()
            self.setPreciosEconomicos()
            #vaciar datos del dia
    
    def vaciarDatosDelDia(dato):
        #peninsula
        with open('datosPrecios/datosDia.txt') as file:
            data = file.read()
        js = json.loads(data) #cargar el str como diccionario
        js = []
        #y reescribo lo que queria
        with open('datosPrecios/datosDia.txt', 'w') as file:
            file.write(json.dumps(js)) 

    def obtenerDatos(self):
        zona_horaria = self.get_zona_horaria()
        if zona_horaria['zona_horaria'] == 'peninsula':
            self.migeoid = 8741
        else:
            self.migeoid = 8744
        ## QUEDARME CON EL LISTADO DE VALORES SOLO
        valores = self.json_data['indicator']['values']
        ## FILTRAR LOS VALORES POR GEOID
        valores_geoid = [x for x in valores if x['geo_id'] == self.migeoid ]
        ## SACAR DENTRO DEL LISTADO DE VALORES SOLO EL PRECIO
        precios = [x['value'] for x in valores_geoid ]
        obtenerFecha = valores_geoid[0]['datetime']
        fecha = self.obtenerFecha(obtenerFecha)
        ## SACAR MAX MIN Y MED DEL LISTADO DE VALORES
        valor_min = min(precios)
        valor_max = max(precios)
        valor_med = round(statistics.mean(precios),2)

        ## Recorrer los valores uno por uno para sacar la informacion que me interesa
        for t_valor in valores_geoid:
            ## Sacar la hora del valor y convertirla a objeto datetime
            t_valor_date = datetime.fromisoformat(t_valor['datetime'])
            ## Si el precio esta por debajo de la media ...
            if t_valor['value'] < valor_med:
                ## Incremento el contador de numero de horas por debajo de la media
                self.itemsbajomedia += 1
                ## Si ademas es en el futuro y no he pillado aun la proxima hora bajo la media ....
                if t_valor_date.hour > self.horaejecucion and not self.proximahorabm:
                    ## Me apunto en mi variable la hora 
                    self.proximahorabm = t_valor_date
            ## Si la hora del precio es ahora
            if t_valor_date.hour == self.horaejecucion:
                ## Me lo apunto como valor actual
                valor_act = t_valor['value']
                ## Y pongo en la variable bajomedia true o false para saber si esta por debajo de la media
                self.bajomedia =  valor_act < valor_med
            #guardar hora maximo
            if valor_max == t_valor['value']:
                hour_maximo = t_valor_date.hour
            #guardar hora minimo
            if valor_min == t_valor['value']:
                hour_minimo = t_valor_date.hour

            valor_act = t_valor['value']
            barato = valor_act < valor_med

            t_valor['datetime']
            #antes de guardar la hora la pasamos a un rango
            hora = self.cambioHoraString(t_valor_date.hour)

            #"date": "27-04-2023"
            self.setDatosDiaPeninsula(fecha,hora, barato, t_valor['value'])
        #AHORA AÑADIR A MAXIMOSPENINSULA.TXT, {"hour": "STR", "is-cheap": false, "price": 251.45}
        self.setMaximos(fecha,hour_maximo,False,valor_max)
        self.setMinimo(fecha,hour_minimo,True,valor_min)

    def ordenarPrecios(self):
        listaPrecios = self.get_datos_dia()
        n = len(listaPrecios)
        for i in range(n):
            # Encontrar el mínimo elemento restante en la lista desordenada
            minimo = i
            for j in range(i+1, n):
                if listaPrecios[j]['price'] < listaPrecios[minimo]['price']:
                    minimo = j
            # Intercambiar el mínimo con el primer elemento de la lista desordenada
            listaPrecios[i]['price'], listaPrecios[minimo]['price'] = listaPrecios[minimo]['price'], listaPrecios[i]['price']
            listaPrecios[i]['hour'], listaPrecios[minimo]['hour'] = listaPrecios[minimo]['hour'], listaPrecios[i]['hour']
        
        print(listaPrecios)
        return listaPrecios

    def obtenerFecha(self,fecha):
        now = datetime.now().date()
        palabras = fecha.split('-')
        dia = palabras[2].split('T')
        final = [palabras[0],'-',palabras[1],'-',dia[0]]
        fecha = ''
        for elem in final:
            fecha += elem
        return fecha  
    def cambioHoraString(self,hora):
        if hora < 10:
            if (hora+1)<10:
                hora = '0'+str(hora)+'-'+'0'+str(hora+1)
            else:
                hora = '0'+str(hora)+'-'+str(hora+1)
        else:
            hora = str(hora)+'-'+str(hora+1)
        return hora
    def setMaximos(self,fecha,hour,is_cheap,price):
        hour = self.cambioHoraString(hour)
        dic_maximosPeninsula = {'fecha':fecha,'hour': hour, 'is-cheap': is_cheap,'price': price}
        #y reescribo lo que queria
        with open('datosPrecios/maximos.txt', 'w') as file:
            file.write(json.dumps(dic_maximosPeninsula)) 
    def setMinimo(self,fecha,hour,is_cheap,price):
        hour = self.cambioHoraString(hour)
        dic_minimosPeninsula = {'fecha':fecha,'hour': hour, 'is-cheap': is_cheap,'price': price}
        #y reescribo lo que queria
        with open('datosPrecios/minimos.txt', 'w') as file:
            file.write(json.dumps(dic_minimosPeninsula)) 
    def setDatosDiaPeninsula(self,fecha,hour,is_cheap,price):
        with open('datosPrecios/datosDia.txt') as file:
            data = file.read()
        js = json.loads(data) #cargar el str como diccionario
        dic_datosDiaPeninsula = {'fecha':fecha,'hour': hour, 'is-cheap': is_cheap,'price': price}
        js.append(dic_datosDiaPeninsula)
        #y reescribo lo que queria
        with open('datosPrecios/datosDia.txt', 'w') as file:
            file.write(json.dumps(js)) 
    def setPreciosEconomicos(self):
        dic_datosEconomicos = self.ordenarPrecios()
        with open('datosPrecios/preciosEconomicos.txt', 'w') as file:
            file.write(json.dumps(dic_datosEconomicos)) 
    def get_datos_dia(self):
        with open('datosPrecios/datosDia.txt') as file:
            data = file.read()
        js = json.loads(data)
        return js #devuelve todos los datos del dia
horaejecucion = datetime.now().hour
jello = preciosPVPC(horaejecucion)
jello.vaciarDatosDelDia()
jello.obtenerDatos()





