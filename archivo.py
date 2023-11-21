import requests
import tkinter
import base64
from io import BytesIO
from PIL import Image, ImageTk
import os


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


#funciones para la pantalla de finalizar compra#


def pagina_d (info_ticket) -> None:

    pantalla_final = tkinter.Tk()
    pantalla_d = tkinter.Frame(pantalla_final, width=500, height=620)
    pantalla_d.grid()
    count_row: int = 0

    if len(info_ticket['SNACKS_COMPRADOS']) > 0:
        for snacks in info_ticket['SNACKS_COMPRADOS']:
            for nombre_snack in snacks:
                text = tkinter.Label(pantalla_d, text=f"{nombre_snack}")
                text.grid(row= count_row, column=0)
                cantidad_comprada = snacks[nombre_snack]
                cantidad_etiqueta = tkinter.Label(pantalla_d, text=f"x{cantidad_comprada}")
                cantidad_etiqueta.grid(row= count_row, column=1)
                valor_snack: float = float(obtener_endpoint_json(SNACKS)[nombre_snack])
                total_por_cada_snack = cantidad_comprada * valor_snack
                total_snack_etiqueta = tkinter.Label(pantalla_d, text=f" ${total_por_cada_snack}")
                total_snack_etiqueta.grid(row= count_row, column=2)
                count_row += 1

    total = tkinter.Label(pantalla_d, text=f"TOTAL: ${info_ticket['PRECIO_TOTAL']}")
    total.grid(row= count_row, column=0)


#funciones para la pantalla de reserva#


def suma_valor_snacks(info_ticket: dict) -> int:
    total_por_snacks: float = 0
    diccionario_snacks: dict = obtener_endpoint_json(SNACKS)

    #info_ticket['SNACKS_COMPRADOS'] = [{'snack_1' : cantidad}, {'snack_2' : cantidad}, ... ]

    if len(info_ticket['SNACKS_COMPRADOS']) > 0:
        for snacks_comprados in info_ticket['SNACKS_COMPRADOS']:
            for snack in snacks_comprados:
                cant: int = snacks_comprados[snack]
                valor: float = float(diccionario_snacks[snack])

                total_por_snacks = cant * valor    

    return total_por_snacks


def confirmar_compra(pantalla_c, info_ticket: dict) -> None:

    info_ticket['VALOR_TOTAL_ENTRADAS'] = info_ticket['CANT_ENTRADAS'] * info_ticket['VALOR_CADA_ENTRADA']

    info_ticket['VALOR_TOTAL_SNACKS'] = suma_valor_snacks(info_ticket)

    info_ticket['PRECIO_TOTAL'] = info_ticket["VALOR_TOTAL_ENTRADAS"] + info_ticket["VALOR_TOTAL_SNACKS"]

    pantalla_c.destroy()
    pagina_d(info_ticket)


def sumar_snack(cantidad_seleccionada: list, nombre_snack: str, cant_a_mostrar, info_ticket: dict) -> None:
    cantidad_seleccionada[0] += 1
    
    #info_ticket['SNACKS_COMPRADOS']: list = [{'snack_1' : cantidad}, {'snack_2' : cantidad}, ... ]

    snack_nombre_y_cantidad: dict = {nombre_snack: cantidad_seleccionada[0]}

    if cantidad_seleccionada[0] == 1:    
        info_ticket['SNACKS_COMPRADOS'].append(snack_nombre_y_cantidad)
    else:
        for i in range (len(info_ticket['SNACKS_COMPRADOS'])):
            if nombre_snack in info_ticket['SNACKS_COMPRADOS'][i].keys():
                info_ticket['SNACKS_COMPRADOS'][i][nombre_snack] += 1

    #print(info_ticket['SNACKS_COMPRADOS'])

    cant_a_mostrar.config( text= f"{cantidad_seleccionada}")


def restar_snack(cantidad_seleccionada: list, nombre_snack: str, cant_a_mostrar, info_ticket: dict) -> None:
    cantidad_seleccionada[0] -= 1

    snack_nombre_y_cantidad: dict = {nombre_snack: cantidad_seleccionada[0]}

    if cantidad_seleccionada[0] < 0:
        cantidad_seleccionada[0] = 0

    snacks: list = list(info_ticket['SNACKS_COMPRADOS'])

    #info_ticket['SNACKS_COMPRADOS'] = [{'snack_1' : cantidad}, {'snack_2' : cantidad}, ... ]
    if cantidad_seleccionada[0] == 0:
        for i in range (len(snacks)):
            if nombre_snack in snacks[i].keys():
                del info_ticket['SNACKS_COMPRADOS'][i]

    if cantidad_seleccionada[0] > 0:
        for i in range (len(info_ticket['SNACKS_COMPRADOS'])):
            if nombre_snack in info_ticket['SNACKS_COMPRADOS'][i].keys():
                info_ticket['SNACKS_COMPRADOS'][i][nombre_snack] -= 1

    #print(info_ticket['SNACKS_COMPRADOS'])

    cant_a_mostrar.config( text= f"{cantidad_seleccionada[0]}")


def contadores(BOTTOM0_IZQ_BOT, info_ticket: dict, snack: str, contador_row: list, snacks_dict: list) -> None:
    texto = tkinter.Label(BOTTOM0_IZQ_BOT, text=f"{snack}")
    precio = tkinter.Label(BOTTOM0_IZQ_BOT, text=f"{snacks_dict[snack]}$")
    texto.grid(row= contador_row[0], column= 1)
    precio.grid(row= contador_row[0], column= 2)
    locals()['cant_seleccionada_{}'.format(snack)] = [0]
    cant_seleccionada =  locals()['cant_seleccionada_{}'.format(snack)]
    print(cant_seleccionada)
    locals()['mas_boton_{}'.format(snack)] = tkinter.Button(BOTTOM0_IZQ_BOT, text="+", command= lambda: sumar_snack(cant_seleccionada, snack, cant_a_mostrar, info_ticket))
    locals()['mas_boton_{}'.format(snack)].grid(row= contador_row[0], column= 5)
    locals()['cant_{}'.format(snack)] = tkinter.Label(BOTTOM0_IZQ_BOT, text=f"{cant_seleccionada[0]}")
    locals()['cant_{}'.format(snack)].grid(row= contador_row[0], column= 4)
    cant_a_mostrar = locals()['cant_{}'.format(snack)]
    locals()['menos_boton_{}'.format(snack)] = tkinter.Button(BOTTOM0_IZQ_BOT, text="-", command= lambda: restar_snack(cant_seleccionada, snack, cant_a_mostrar, info_ticket))
    locals()['menos_boton_{}'.format(snack)].grid(row= contador_row[0], column= 3)


def crear_lista_snacks(BOTTOM0_IZQ_BOT, info_ticket: dict) -> None:
    snacks_dict: dict = obtener_endpoint_json(SNACKS)

    contador_row: list = [0]

    for snack in snacks_dict:
        contadores(BOTTOM0_IZQ_BOT, info_ticket, snack, contador_row, snacks_dict)
        contador_row[0] += 1


def restar_entradas(pantalla_c, info_ticket: dict, contador_asientos, add_boton) -> None:
    info_ticket['CANT_ENTRADAS'] -= 1

    if info_ticket['CANT_ENTRADAS'] < 0:
        info_ticket['CANT_ENTRADAS'] = 0

    contador_asientos.config(text=f"{info_ticket['CANT_ENTRADAS']}")

    if info_ticket['CANT_ENTRADAS'] > 0:
        add_boton.config(state= "active",command= lambda: confirmar_compra(pantalla_c, info_ticket))
    else:
        add_boton.config(state= "disabled")


def sumar_entradas(pantalla_c, info_ticket: dict, contador_asientos, add_boton) -> None:
    info_ticket['CANT_ENTRADAS'] += 1

    if info_ticket['CANT_ENTRADAS'] > asientos_disponibles(ID_UBICACION):
        info_ticket['CANT_ENTRADAS'] = asientos_disponibles(ID_UBICACION)

    contador_asientos.config(text=f"{info_ticket['CANT_ENTRADAS']}")

    if info_ticket['CANT_ENTRADAS'] > 0:
        add_boton.config(state= "active",command= lambda: confirmar_compra(pantalla_c, info_ticket))
    else:
        add_boton.config(state= "disabled")


def mostrar(snacks, toggle, info_ticket: dict) -> None:
    if snacks.winfo_ismapped():
        snacks.grid_forget()
        toggle.config(text= "MOSTRAR SNACKS")
        info_ticket['SNACKS_COMPRADOS'].clear()
        print(info_ticket['SNACKS_COMPRADOS'])
    else:
        snacks.grid()
        toggle.config(text= "OCULTAR SNACKS")
        crear_lista_snacks(snacks, info_ticket)


def crear_lista_pelicula(pantalla_c, TOP1_DER, TOP2, info_ticket: dict, add_boton) -> None:
    nombre_pelicula: str = consultar_info_pelicula(info_ticket['ID_PELICULA'],'name')

    titulo_pelicula = tkinter.Label(TOP1_DER, text=f"{nombre_pelicula}")
    valor_asientos_etiqueta = tkinter.Label(TOP1_DER, text=f"{info_ticket['VALOR_CADA_ENTRADA']}$ c/u")
    
    asientos_disponibles_etiqueta = tkinter.Label(TOP1_DER, text=f"Asientos disponibles: {asientos_disponibles(ID_UBICACION)}")
    texto =tkinter.Label(TOP2, text=f"ELIJA LA CANTIDAD DE ENTRADAS: ")
    if info_ticket['CANT_ENTRADAS'] > 0:
        add_boton.config(state= "active",command= lambda: confirmar_compra(pantalla_c, info_ticket))
    else:
        add_boton.config(state= "disabled")

    boton_mas_pelicula = tkinter.Button(TOP2, text="+", command= lambda: sumar_entradas(pantalla_c, info_ticket, contador_asientos, add_boton))
    boton_menos_pelicula = tkinter.Button(TOP2, text="-", command= lambda: restar_entradas(pantalla_c, info_ticket, contador_asientos, add_boton))
    contador_asientos = tkinter.Label(TOP2, text=f"{info_ticket['CANT_ENTRADAS']}")
    titulo_pelicula.grid(row= 0, column=0)
    valor_asientos_etiqueta.grid(row= 1, column=0)
    asientos_disponibles_etiqueta.grid(row=2, column=0)
    texto.grid(row= 0, column=1)
    boton_menos_pelicula.grid(row= 1, column=0)
    contador_asientos.grid(row= 1, column=1)
    boton_mas_pelicula.grid(row=1, column=2)


def volver_pagina_secundaria(root, info_ticket: dict) -> None:
    """
    root.destroy()

    info_ticket['CANT_ENTRADAS'] = 0
    info_ticket['SNACKS_COMPRADOS'].clear()
    info_ticket['VALOR_POR_SNACKS'] = 0
    info_ticket['PRECIO_TOTAL'] = 0

    pantalla_secundaria(info_ticket)
    """
    #no anda


def pantalla_reseva(info_ticket: dict) -> None:

    root = tkinter.Tk()

    pantalla_c = tkinter.Frame(root, width=500, height=620)
    TOP0 = tkinter.Frame(pantalla_c, width=500, height=100)
    TOP1 = tkinter.Frame(pantalla_c, width=500, height=150)
    TOP1_IZQ = tkinter.Frame(TOP1, width=200, height=150)
    TOP1_DER = tkinter.Frame(TOP1, width=300, height=150)
    TOP2 = tkinter.Frame(pantalla_c, width=500, height=70)
    BOTTOM0 = tkinter.Frame(pantalla_c, width=500, height=300)
    BOTTOM0_IZQ = tkinter.Frame(BOTTOM0 , width=200, height=300)
    BOTTOM0_IZQ_TOP = tkinter.Frame(BOTTOM0_IZQ, width=200, height=50)
    BOTTOM0_IZQ_BOT = tkinter.Frame(BOTTOM0_IZQ, width=200, height=250)
    BOTTOM0_DER = tkinter.Frame(BOTTOM0, width=300, height=300)
    pantalla_c.grid()
    TOP0.grid(row=0)
    TOP1.grid(row=1)
    TOP1_IZQ.grid(row= 0, column=0)
    TOP1_DER.grid(row= 0, column=1)
    TOP2.grid(row=2)
    BOTTOM0.grid(row= 3)
    BOTTOM0_IZQ.grid(row= 0 ,column=0)
    BOTTOM0_IZQ_TOP.grid(row= 0 ,column=0)
    BOTTOM0_IZQ_BOT.grid(row= 1 ,column=0)
    BOTTOM0_DER.grid(row= 0, column=1)

    distribucion_pantalla: dict = {"PANTALLA_D": "PANTALLA_D", "PANTALLA_C": pantalla_c, "TOP0": TOP0, "TOP1": TOP1, "TOP1_IZQ": TOP1_IZQ, "TOP1_DER": TOP1_DER, "TOP2": TOP2,
                                    "BOTTOM0": BOTTOM0, "BOTTOM0_IZQ": BOTTOM0_IZQ, "BOTTOM0_IZQ_TOP": BOTTOM0_IZQ_TOP, "BOTTOM0_IZQ_BOT": BOTTOM0_IZQ_BOT,
                                     "BOTTOM0_DER": BOTTOM0_DER}

    BOTTOM0_IZQ_BOT.grid_forget()
    root.title("3er pagina")

    volver_buton = tkinter.Button(TOP0, text="VOLVER", command= volver_pagina_secundaria(root, info_ticket))
    volver_buton.place(relx=0.5, rely=0.3, anchor="center")

    toggle = tkinter.Button(BOTTOM0_IZQ_TOP, text= "MOSTRAR SNACKS", command= lambda: mostrar(BOTTOM0_IZQ_BOT, toggle, info_ticket))
    add_boton = tkinter.Button(BOTTOM0_DER, text="FINALIZAR")
    crear_lista_pelicula(pantalla_c, TOP1_DER, TOP2, info_ticket, add_boton)
    toggle.grid()
    add_boton.place(relx=0.8, rely=0.8, anchor="center")
    root.mainloop()


#funciones para la pantalla secundaria#


def pantalla_secundaria(info_ticket: dict) -> None:
    #pelicula_id = f"{pelicula_id}/"
    poster = info_poster(info_ticket['ID_PELICULA'])
    creacion_pantalla(poster, info_ticket)


def info_poster(pelicula_id: int) -> str:

    archivo = requests.get(URL + POSTERS + pelicula_id, headers= HEADERS)
    poster_pelicula: dict = archivo.json()
    imagen_poster: str = poster_pelicula["poster_image"]
    imagen_poster = imagen_poster[imagen_poster.index(",")+1:]

    return imagen_poster


def creacion_pantalla(poster, info_ticket) -> None:

    sinopsis: str = consultar_info_pelicula(info_ticket['ID_PELICULA'],'synopsis') #muy largo, hay que hacerlo por renglones
    actores: str = consultar_info_pelicula(info_ticket['ID_PELICULA'],'actors')
    director: str = consultar_info_pelicula(info_ticket['ID_PELICULA'],'directors')
    duracion: str = consultar_info_pelicula(info_ticket['ID_PELICULA'],'duration')
    genero: str = consultar_info_pelicula(info_ticket['ID_PELICULA'],'gender')
    portada: str = poster
    nombre_pelicula: str = consultar_info_pelicula(info_ticket['ID_PELICULA'],'name')

    imagen = base64.b64decode(portada)
    imagen_final = Image.open(BytesIO(imagen))
    jpg= imagen_final.convert("RGB")
    jpg.save('portada.png')
    pantalla_2 = tkinter.Tk()

    TOP0_MID = tkinter.Label(pantalla_2, text="SALA 7",
                            font= "Helvetica 20 bold")#numero de sala
    TOP0_DER = tkinter.Button(pantalla_2, text="VOLVER ATRAS",
                            font= "Helvetica 15 bold", command= lambda: boton_atras_principal(pantalla_2, info_ticket))#boton volver atras
    IMAGEN = tkinter.PhotoImage(file= 'portada.png')
    TOP1_IZQ = tkinter.Label(pantalla_2, image= IMAGEN)#,
                            #width=200, height=200)# dimensiones portada
    TOP1_DER = tkinter.Frame(pantalla_2,
                            width=200, height=200)
    TOP1_ARRIBA = tkinter.Label(TOP1_DER, text= f"SINOPSIS \n {sinopsis}",
                                font= "Helvetica 10 bold", justify= "left", wraplength= 400)#sinopsis     mayor a 400 más ancho, menor más angosto
    TOP1_ABAJO = tkinter.Label(TOP1_DER, text= f"ACTORES: {actores}\nDIRECTOR: {director}\nDURACIÓN DE LA PELICULA: {duracion}",
                                font= "Helvetica 10 bold", justify= "left")#actores, director, duracion
    TOP2_IZQ = tkinter.Label(pantalla_2, text= f"GÉNERO: {genero}",
                            font= "Helvetica 15 bold", justify= "left")#genero
    BOTTOM = tkinter.Button(pantalla_2, text= "RESERVAR",
                            font= "Helvetica 15 bold", command= lambda: boton_reservar(pantalla_2, info_ticket))#boton RESERVAR

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


def boton_reservar(pantalla_2, info_ticket: dict) -> None:
    pantalla_2.destroy()

    pantalla_reseva(info_ticket)


def boton_atras_principal(pantalla_2, info_ticket: dict) -> None:
    pantalla_2.destroy()

    iniciar_pantalla_principal(info_ticket)


def obtener_endpoint_json(endpoint: str, id_pelicula_o_cine: str = "", pelicula_o_cine : str = "") -> str:
    """
    PRE: Función que recibe parte strings para formar el link del endpoint (la id tiene que ser casteada a string 
    con "1" por ejemplo)
    POST: Devuelve la información del endpoint en forma de lista o diccionario (depende el endpoint)
    """
    dato = requests.get(URL + endpoint + id_pelicula_o_cine + pelicula_o_cine, headers=HEADERS)

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


def accion_del_boton(id_pelicula_elegida: int, info_ticket: dict, pantalla_principal) -> None:
    """
    PRE: Procedimiento que realiza el botón imagen de la página principal al ser presionado
    Guarda la id de la película clickeada en un diccionario para ser pasado a ventanas posteriores
    """
    pantalla_principal.destroy()
    info_ticket['ID_PELICULA'] = str(id_pelicula_elegida)

    pantalla_secundaria(info_ticket)


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

    fila: int = 0
    columna: int = 0

    for i in range(1, cantidad_peliculas + 1):
        imagen_tk = obtener_imagen_base64(i)
        imagenes.append(imagen_tk)
        boton = tkinter.Button(cuerpo_pagina, image = imagen_tk, command= lambda i=i: accion_del_boton(i, info_ticket, pantalla_principal))
        boton.grid(column= columna, row = fila)

        botones.append(boton)

        columna += 1

        if columna > 1:
            columna = 0
            fila += 1

    pantalla_principal.mainloop()


#MAIN#

def main() -> None:

    info_ticket: dict = {
        'LOCALIZACION'         : ID_UBICACION,
        #'ASIENTOS_DISPONIBLES': "",
        'CANT_ENTRADAS'        : 0,
        'ID_PELICULA'          : "",
        'VALOR_CADA_ENTRADA'   : 2000,
        'VALOR_TOTAL_ENTRADAS' : 0,
        'SNACKS_COMPRADOS'     : [],
        'VALOR_TOTAL_SNACKS'   : 0,
        'PRECIO_TOTAL'         : 0
    }

    iniciar_pantalla_principal(info_ticket)

main()
