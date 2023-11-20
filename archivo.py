import json
import requests
import tkinter
import base64
from io import BytesIO
from PIL import Image, ImageTk

###########################################################################
############################# CONSTANTES ##################################
###########################################################################

ID_CINE_CABALLITO: int = 0
ID_CINE_ABASTO: int = 1
ID_CINE_PUERTO_MADERO: int = 2
ID_CINE_VILLA_DEL_PARQUE: int = 3
ID_CINE_PALERMO: int = 4
ID_CINE_LINIERS: int = 5
ID_CINE_OLIVOS: int = 6

######## UBICACIÓN DEL TÓTEM #########
ID_UBICACION: int = ID_CINE_ABASTO
######################################

URL: str = "http://vps-3701198-x.dattaweb.com:4000"
PELICULAS: str = "/movies/"
POSTERS : str = "/posters/"
SNACKS: str = "/snacks/"
CINES: str = "/cinemas/"

TOKEN: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.DGI_v9bwNm_kSrC-CQSb3dBFzxOlrtBDHcEGXvCFqgU"

HEADERS: dict[str, str] = {"Authorization": "Bearer " + TOKEN}

###########################################################################
############################# FUNCIONES ###################################
###########################################################################

def obtener_endpoint_json(endpoint: str, id_pelicula_o_cine: str = "", pelicula_o_cine : str = "") -> str:
    """
    PRE: Función que recibe parte strings para formar el link del endpoint (la id tiene que ser casteada a string 
    con "1" por ejemplo)
    POST: Devuelve la información del endpoint en forma de lista o diccionario (depende el endpoint)
    """
    dato = requests.get(URL + endpoint + id_pelicula_o_cine + pelicula_o_cine , headers=HEADERS)

    return dato.json()


def consultar_info_pelicula(id_pelicula: int, clave_pelicula: str) -> str:
    """
    PRE: Función que recibe la id de una película como entero
    Y una clave del diccionario película como string
    POST: Devuelve por ejemplo la sinopsis de la película como string
    (todos los valores de las claves son strings)
    """
    info_pelicula: dict = obtener_endpoint_json(PELICULAS, str(id_pelicula))

    return info_pelicula[clave_pelicula]


def asientos_disponibles(id_cine: int) -> int:
    """
    PRE: Función que recibe id del cine en enteros
    POST: devuelve un entero indicando los asientos disponibles
    """
    info_cines: list = obtener_endpoint_json(CINES)
    info_cine: dict = info_cines[id_cine]
    asientos: int = info_cine['available_seats']

    return int(asientos)


def nombre_cine(id_cine: int) -> str:
    """
    PRE: Función que recibe id del cine en enteros
    POST: devuelve un string con el nombre de la ubicación
    """
    info_cines: list = obtener_endpoint_json(CINES)
    info_cine: dict = info_cines[id_cine]
    nombre_cine: str = info_cine['location']

    return nombre_cine


def obtener_imagen_base64(i: int):
    """
    PRE: Función que recibe una id como entero, pregunta a la API por su base64, la transforma a binario y luego a PhothoImage
    POST: Devuelve la imagen como PhotoImage
    """
    id_pelicula: str = str(i)

    imagen_json: str = str(obtener_endpoint_json(POSTERS, id_pelicula))
    imagen_string: str = imagen_json.split(";base64,")[1][:-2]
    
    imgagen_binario = base64.b64decode(imagen_string)

    imagen = Image.open(BytesIO(imgagen_binario))

    imagen_tk = ImageTk.PhotoImage(imagen)

    return imagen_tk


def cantidad_de_elementos_json(endpoint: str, id_pelicula_o_cine: str = "", pelicula_o_cine : str = "") -> int:
    """
    PRE: Función que recibe parte strings para formar el link del endpoint (la id tiene que ser casteada a string 
    con "1" por ejemplo)
    POST: Devuelve la cantidad de elementos de la lista
    """
    dato = requests.get(URL + endpoint + id_pelicula_o_cine + pelicula_o_cine , headers=HEADERS)
    cantidad_elementos: int = len(dato.json())

    return cantidad_elementos


def accion_del_boton(id_pelicula_elegida: int, info_ticket: dict) -> None:
    """
    PRE: Procedimiento que realiza el botón imagen de la página principal al ser presionado
    Guarda la id de la película clickeada en un diccionario para ser pasado a ventanas posteriores
    """
    info_ticket['ID_PELICULA'] = id_pelicula_elegida

    ##################################
    ## LLAMAR A PANTALLA SECUNDARIA ##
    #pantalla_secundaria(info_ticket)#


def iniciar_pantalla_principal(info_ticket: dict) -> None:
    """
    PRE: Procedimiento que recibe un diccionario con la información de ticket para ir completando y pasando
    por ventanas
    Muestra la pantalla principal del programa, se crea barra de búsqueda y se hacen los botones con imágenes    
    """
    pantalla_principal = tkinter.Tk()
    pantalla_principal.title("Totem cine")

    cantidad_peliculas = cantidad_de_elementos_json(PELICULAS)

    encabezado = tkinter.Frame(pantalla_principal, bg= "gray")
    encabezado.pack(expand = True, fill= "both")

    texto = tkinter.Label(encabezado, text = "ABASTO CINEMAS", justify= "center")
    texto.pack()

    barra_busqueda = tkinter.Button(encabezado, text = "Buscá la película", justify= "center")
    barra_busqueda.pack()

    cuerpo_pagina = tkinter.Frame(pantalla_principal, bg= "black")
    cuerpo_pagina.pack(expand= True, fill= "both")

    botones: list = []
    imagenes: list = []

    fila = 0
    columna = 0

    for i in range(1, cantidad_peliculas + 1):
        imagen_tk = obtener_imagen_base64(i)
        imagenes.append(imagen_tk)
        boton = tkinter.Button(cuerpo_pagina, image = imagen_tk, command= lambda i=i: accion_del_boton(i, info_ticket))
        boton.grid(column= columna, row = fila)

        botones.append(boton)

        columna += 1

        if columna > 1:
            columna = 0
            fila += 1

    pantalla_principal.mainloop()


def main() -> None:

    info_ticket: dict = {
        'LOCALIZACION'         : ID_UBICACION,
        'ID_PELICULA'          : 0,
        #'ASIENTOS_DISPONIBLES' : "",
        'CANT_ENTRADAS'        : 0,
        'VALOR_POR_ENTRADAS'   : 0,
        'SNACKS'               : [],
        'VALOR_POR_SNACKS'     : 0,
        'PRECIO_TOTAL'         : 0
    }

    iniciar_pantalla_principal(info_ticket)

main()
