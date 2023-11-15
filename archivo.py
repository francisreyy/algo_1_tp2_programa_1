import json
import requests
import tkinter


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

headers: dict[str, str] = {"Authorization": "Bearer " + TOKEN}


###########################################################################
############################# FUNCIONES ###################################
###########################################################################


def imprimir_endpoint_json(endpoint: str, id_pelicula_o_cine: str = "", pelicula_o_cine : str = "") -> dict:
    """
    PRE: Procedimiento que recibe parte del link en strings (la id tiene que ser casteada a string 
    con "1" por ejemplo) y printea el json del endpoint
    """
    r = requests.get(URL + endpoint + id_pelicula_o_cine + pelicula_o_cine , headers=headers)

    return r.json()


def asientos_disponibles(id_cine: int) -> int:
    """
    PRE: Función que recibe id del cine en enteros
    POST: devuelve un entero indicando los asientos disponibles
    """
    r = requests.get(URL + CINES , headers=headers)
    info_cines: list = r.json()
    info_cine: dict = info_cines[id_cine]
    asientos: int = info_cine['available_seats']
    return int(asientos)


def nombre_cine(id_cine) -> str:
    """
    PRE: Función que recibe id del cine en enteros
    POST: devuelve un string con el nombre de la ubicación
    """
    r = requests.get(URL + CINES , headers=headers)
    info_cines: list = r.json()
    info_cine: dict = info_cines[id_cine]
    nombre_cine: str = info_cine['location']
    return nombre_cine


def main() -> None:

    info_ticket: dict = {
        'LOCALIZACION'         : ID_UBICACION,
        'ID_PELICULA'          : "",
        #'ASIENTOS_DISPONIBLES' : "",
        'CANT_ENTRADAS'        : 0,
        'VALOR_POR_ENTRADA'    : 0,
        'SNACKS'               : [],
        'VALOR_POR_SNACKS'     : 0,
        'PRECIO_TOTAL'         : 0
    }

    print(f"¡Hola! Estás usando el tótem de {nombre_cine(ID_UBICACION)} Cinemas")

    #ejemplos (todos los endpoints del PDF chequeados)
    #imprimir_endpoint_json(PELICULAS, "2", CINES) 
    #imprimir_endpoint_json(POSTERS, "1")
    #imprimir_endpoint_json(CINES, "1", PELICULAS)
    #imprimir_endpoint_json(PELICULAS, "2")

    #r = imprimir_endpoint_json(SNACKS)
    #print(r)
    print(asientos_disponibles(ID_CINE_ABASTO))

main()
