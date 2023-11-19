import base64
import tkinter
from PIL import Image
from io import BytesIO
import os
import requests

def pantalla_secundaria(info_request: dict, pelicula_id: int)->None:

    informacion_pelicula = recopilar_informacion_pelicula(info_request, pelicula_id)
    poster = info_poster(info_request, pelicula_id)
    creacion_pantalla(informacion_pelicula, poster)


def recopilar_informacion_pelicula(info_request: dict, pelicula_id: int)->dict:

    MOVIES: str = f"/movies/{pelicula_id}/"
    archivo = requests.get(info_request["url"] + MOVIES, headers=info_request["headers"])
    informacion_pelicula: dict = archivo.json()

    return informacion_pelicula


def info_poster(info_request: dict, pelicula_id: int)->str:
    
    POSTER: str = f"/posters/{pelicula_id}/"
    archivo = requests.get(info_request["url"] + POSTER, headers=info_request["headers"])
    poster_pelicula: dict = archivo.json()
    imagen_poster: str = poster_pelicula["poster_image"]
    imagen_poster = imagen_poster[imagen_poster.index(",")+1:]

    return imagen_poster


def creacion_pantalla(informacion_pelicula, poster)->None:

    #sinopsis: str = informacion_pelicula["synopsis"]
    sinopsis: str = """Sadie Harper, una estudiante del colegio secundario y su hermana
pequeña, Sawyer, están conmocionadas por la reciente muerte de su madre y no
reciben mucho apoyo de su padre, Will, un terapeuta que está lidiando con su propio
dolor. Cuando un paciente desesperado se presenta inesperadamente en su casa en
busca de ayuda, deja tras de sí una aterradora entidad sobrenatural que se
aprovecha de las familias y se alimenta del sufrimiento de sus víctimas.
"""
    actores: str = informacion_pelicula["actors"]
    director: str = informacion_pelicula["directors"]
    duracion: str = informacion_pelicula["duration"]
    genero: str = informacion_pelicula["gender"]
    portada: str = poster

    imagen = base64.b64decode(portada)
    imagen_final = Image.open(BytesIO(imagen))
    jpg= imagen_final.convert("RGB")
    jpg.save('portada.png')
    pantalla_2 = tkinter.Tk()

    TOP0_MID = tkinter.Label(pantalla_2, text="SALA 7",
                            font= "Helvetica 20 bold")#numero de sala
    TOP0_DER = tkinter.Button(pantalla_2, text="VOLVER ATRAS",
                            font= "Helvetica 15 bold")#boton volver atras
    IMAGEN = tkinter.PhotoImage(file= 'portada.png')
    TOP1_IZQ = tkinter.Label(pantalla_2, image= IMAGEN,
                            width=200, height=200)#portada pelicula
    TOP1_DER = tkinter.Frame(pantalla_2,
                            width=200, height=200)
    TOP1_ARRIBA = tkinter.Label(TOP1_DER, text= f"SINOPSIS \n {sinopsis}",
                                font= "Helvetica 10 bold", justify= "left")#sinopsis
    TOP1_ABAJO = tkinter.Label(TOP1_DER, text= f"ACTORES: {actores}\nDIRECTOR: {director}\nDURACION DE LA PELICULA: {duracion}",
                                font= "Helvetica 10 bold", justify= "left")#actores, director, duracion
    TOP2_IZQ = tkinter.Label(pantalla_2, text= f"GENERO: {genero}",
                            font= "Helvetica 15 bold", justify= "left")#genero
    BOTTOM = tkinter.Button(pantalla_2, text= "RESERVAR",
                            font= "Helvetica 15 bold")#boton RESERVAR

    TOP0_MID.grid(row=0, column=0)
    TOP0_DER.grid(row=0, column=2)
    TOP1_IZQ.grid(row= 1, column=0)
    TOP1_DER.grid(row=1, column=1)
    TOP1_ARRIBA.grid(row= 0, column=0)
    TOP1_ABAJO.grid(row=1, column=0)
    TOP2_IZQ.grid(row=2, column=0)
    BOTTOM.grid(row= 3 ,column=1)
    pantalla_2.mainloop()
    os.remove('portada.png')


def main()-> None:

    url: str = "http://vps-3701198-x.dattaweb.com:4000"
    token: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.DGI_v9bwNm_kSrC-CQSb3dBFzxOlrtBDHcEGXvCFqgU"
    headers: dict = {"Authorization": "Bearer " + token}
    pelicula_id: int = 3

    info_request: dict = {"url": url,
                           "token": token,
                             "headers": headers}

    pantalla_secundaria(info_request, pelicula_id)

main()