#TP2
import requests
import tkinter


###########################################################################
############################# CONSTANTES ##################################
###########################################################################


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


def imprimir_endpoint_json(endpoint: str, id_pelicula_o_cine: str = "", pelicula_o_cine : str = "") -> None:
    """
    PRE: Procedimiento que recibe strings (la id tiene que ser casteada a string con "1" por ejemplo)
    y printea el json del endpoint
    """
    r = requests.get(URL + endpoint + id_pelicula_o_cine + pelicula_o_cine , headers=headers)

    print(r.json())


def main() -> None:

    imprimir_endpoint_json(PELICULAS, "2", CINES)
    imprimir_endpoint_json(POSTERS, "1")


main()
