'''
Se detecta lo siguiente: la API indica que para recuperar la información
meteorológica de un municipio necesitamos conocer el CODPROV de la provincia
y el ID del municipio
(https://www.el-tiempo.net/api/json/v2/provincias/[CODPROV]/municipios/[ID]).
El primero es devuelto en el listado de provincias
(https://www.el-tiempo.net/api/json/v2/provincias),
mientras que el ID no lo devuelve el listado de municipios.
Tras varias pruebas, llego a la conclusión de que el ID se corresponde con
los 5 primeros dígitos del CODIGOINE.
'''
from urllib.error import HTTPError
import requests

def api_request(url):
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(response.status_code)
    return response.json()

def select_option(options, field, message, error):
    i = 1
    for option in options:
        print(f"{i}. {option[field]}")
        i += 1
    user_input = input(message)
    position = int((0, user_input)[user_input.isdigit()])
    while(position < 1 or position > len(options)):
        user_input = input(error)
        position = int((0, user_input)[user_input.isdigit()])
    return options[position-1]

try:
    API_URL = 'https://www.el-tiempo.net/api/json/v2/provincias'
    PROVINCIAS = api_request(API_URL)['provincias']
    PROVINCIA = select_option(PROVINCIAS, 'NOMBRE_PROVINCIA',
                            "Introduzca su código de provincia ",
                            "Introduzca un código válido ")
    print(f"Usted ha escogido la provincia: {PROVINCIA['NOMBRE_PROVINCIA']}")
    MUNICIPIOS = api_request(f"{API_URL}/{PROVINCIA['CODPROV']}/municipios")['municipios']
    MUNICIPIO = select_option(MUNICIPIOS, 'NOMBRE',
                            "Introduzca el número su de municipio ",
                            "Introduzca un número dentro del rango de municipios ")
    print(f"Usted ha escogido el municipio: {MUNICIPIO['NOMBRE']}")
    MUNICIPIO_ID = MUNICIPIO['CODIGOINE'][0:5]
    PARTE = api_request(f"{API_URL}/{PROVINCIA['CODPROV']}/municipios/{MUNICIPIO_ID}")
    TEMPERATURAS = PARTE['temperaturas']
    print(
        f"Hoy en {MUNICIPIO['NOMBRE']},",
        f"la temperatura máxima será de {TEMPERATURAS['max']}ºC",
        f"y la mínima de {TEMPERATURAS['min']}ºC."
        )
except HTTPError:
    print('No ha sido posible recuperar la información del servidor')
