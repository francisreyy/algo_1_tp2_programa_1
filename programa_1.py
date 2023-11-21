import requests
import tkinter
import base64
from io import BytesIO
from PIL import Image, ImageTk
import os
from reportlab.pdfgen import canvas
import json
from datetime import datetime
import qrcode


ASIENTOS_LIBRES: int = 40


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

VALOR_ENTRADA: int = 1500


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


def accion_del_boton(id_pelicula_elegida: int, pantalla_principal) -> None:
    """
    PRE: Procedimiento que realiza el botón imagen de la página principal al ser presionado
    Guarda la id de la película clickeada en un diccionario para ser pasado a ventanas posteriores
    """
    pantalla_principal.destroy()
    condicion: bool = True
    pantalla_secundaria(id_pelicula_elegida, condicion)

    ##################################
    ## LLAMAR A PANTALLA SECUNDARIA ##
    #pantalla_secundaria(info_ticket)#


def iniciar_pantalla_principal() -> None:
    """
    PRE: Procedimiento que recibe un diccionario con la información de ticket para ir completando y pasando
    por ventanas
    Muestra la pantalla principal del programa, se crea barra de búsqueda y se hacen los botones con imágenes    
    """

    cantidad_peliculas = cantidad_de_elementos_json(PELICULAS)

    pantalla_principal= tkinter.Tk()
    pantalla_principal.title("Totem cine")

    """
    scrollbar = tkinter.Scrollbar(pantalla_principal)
    c = tkinter.Canvas(pantalla_principal, yscrollcommand= scrollbar.set)
    scrollbar.config(command= c.yview)
    scrollbar.pack(side= tkinter.RIGHT, fill= tkinter.Y)
    pantalla_principal = tkinter.Frame(c)
    c.pack(side= "left", fill= "both", expand= True)
    c.create_window(0,0, window= pantalla_principal, anchor= "nw")
    """

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
        boton = tkinter.Button(cuerpo_pagina, image = imagen_tk, command= lambda i=i: accion_del_boton(i, pantalla_principal))
        boton.grid(column= columna, row = fila)

        botones.append(boton)

        columna += 1

        if columna > 1:
            columna = 0
            fila += 1

    pantalla_principal.mainloop()



#funciones para la pantalla secundaria#


def pantalla_secundaria(pelicula_id: int, condicion: bool)->None:

    pelicula_id_str = f"{pelicula_id}/"
    informacion_pelicula = obtener_endpoint_json(PELICULAS, pelicula_id_str)
    poster = info_poster(pelicula_id_str)
    creacion_pantalla(informacion_pelicula, poster, pelicula_id, condicion)


def info_poster(pelicula_id: int)->str:
    
    archivo = requests.get(URL + POSTERS + pelicula_id, headers= HEADERS)
    poster_pelicula: dict = archivo.json()
    imagen_poster: str = poster_pelicula["poster_image"]
    imagen_poster = imagen_poster[imagen_poster.index(",")+1:]

    return imagen_poster


def creacion_pantalla(informacion_pelicula: str, poster, pelicula_id: int, condicion: bool)->None:

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
    nombre_pelicula: str = informacion_pelicula["name"]

    if condicion:

        imagen = base64.b64decode(portada)
        imagen_final = Image.open(BytesIO(imagen))
        jpg= imagen_final.convert("RGB")
        jpg.save('portada.png')
    
    pantalla_2 = tkinter.Tk()
    pantalla_2.title("pantalla secundaria")
        
    TOP0_MID = tkinter.Label(pantalla_2, text="SALA 7",
                            font= "Helvetica 20 bold")#numero de sala
    TOP0_DER = tkinter.Button(pantalla_2, text="VOLVER ATRAS",
                            font= "Helvetica 15 bold", command= lambda: boton_atras_principal(pantalla_2))#boton volver atras
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
                            font= "Helvetica 15 bold", command= lambda: boton_reservar(pantalla_2, nombre_pelicula, pelicula_id))#boton RESERVAR

    TOP0_MID.grid(row=0, column=0)
    TOP0_DER.grid(row=0, column=2)
    TOP1_IZQ.grid(row= 1, column=0)
    TOP1_DER.grid(row=1, column=1)
    TOP1_ARRIBA.grid(row= 0, column=0)
    TOP1_ABAJO.grid(row=1, column=0)
    TOP2_IZQ.grid(row=2, column=0)
    BOTTOM.grid(row= 3 ,column=1)
    pantalla_2.mainloop()


def boton_reservar(pantalla_2, nombre_pelicula: str, pelicula_id: int)->None:
    pantalla_2.destroy()

    pantalla_reseva(nombre_pelicula, pelicula_id)


def boton_atras_principal(pantalla_2)->None:
    pantalla_2.destroy()
    os.remove('portada.png')

    iniciar_pantalla_principal()



#funciones para la pantalla de reserva#

def pantalla_reseva(nombre_pelicula: str, pelicula_id: int):

    root = tkinter.Tk()

    PANTALLA_D = tkinter.Frame(root, width=500, height=620)
    PANTALLA_C = tkinter.Frame(root, width=500, height=620)
    TOP0 = tkinter.Frame(PANTALLA_C, width=500, height=100)
    TOP1 = tkinter.Frame(PANTALLA_C, width=500, height=150)
    TOP1_IZQ = tkinter.Frame(TOP1, width=200, height=150)
    TOP1_DER = tkinter.Frame(TOP1, width=300, height=150)
    TOP2 = tkinter.Frame(PANTALLA_C, width=500, height=70)
    BOTTOM0 = tkinter.Frame(PANTALLA_C, width=500, height=300)
    BOTTOM0_IZQ = tkinter.Frame(BOTTOM0 , width=200, height=300)
    BOTTOM0_IZQ_TOP = tkinter.Frame(BOTTOM0_IZQ, width=200, height=50)
    BOTTOM0_IZQ_BOT = tkinter.Frame(BOTTOM0_IZQ, width=200, height=250)
    BOTTOM0_DER = tkinter.Frame(BOTTOM0, width=300, height=300)
    PANTALLA_C.grid()
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

    distribucion_pantalla: dict = {"PANTALLA_D": PANTALLA_D, "PANTALLA_C": PANTALLA_C, "TOP0": TOP0, "TOP1": TOP1, "TOP1_IZQ": TOP1_IZQ, "TOP1_DER": TOP1_DER, "TOP2": TOP2,
                                    "BOTTOM0": BOTTOM0, "BOTTOM0_IZQ": BOTTOM0_IZQ, "BOTTOM0_IZQ_TOP": BOTTOM0_IZQ_TOP, "BOTTOM0_IZQ_BOT": BOTTOM0_IZQ_BOT,
                                     "BOTTOM0_DER": BOTTOM0_DER, "root": root}
    
    pagina_c(distribucion_pantalla, nombre_pelicula, pelicula_id)


def sumar(cantidad_seleccionada, snack, cant, comprado) -> list:
    cantidad_seleccionada[0] += 1
    print(f"mas {snack}")
    agregar_comprado(comprado, snack, False)

    cant.config( text= f"{cantidad_seleccionada[0]}")


def restar(cantidad_seleccionada, snack, cant, comprado) -> None:
    cantidad_seleccionada[0] -= 1
    if cantidad_seleccionada[0] < 0:
        cantidad_seleccionada[0] = 0
    print(f"menos {snack}")
    agregar_comprado(comprado, snack, True)
    cant.config( text= f"{cantidad_seleccionada[0]}")


def agregar_comprado(comprado, elemento_comprado, fue_eliminado) -> None:
    if len(comprado) == 0 and fue_eliminado == False:
        comprado[elemento_comprado] = 1
    else:
        no_fue_cumplido: bool = False
        for i in comprado:
            if i == elemento_comprado:
                no_fue_cumplido = True
                if fue_eliminado == True:
                    comprado[elemento_comprado] -= 1
                    if comprado[elemento_comprado] < 0:
                        comprado[elemento_comprado] = 0
                else:
                    if comprado[elemento_comprado] != 0:
                        comprado[elemento_comprado] += 1
        if no_fue_cumplido == False:
            comprado[elemento_comprado] = 1


def contadores(comprado, i, contador_row, snacks, distribucion_pantalla: dict):
    texto = tkinter.Label(distribucion_pantalla['BOTTOM0_IZQ_BOT'], text=f"{i}")
    precio = tkinter.Label(distribucion_pantalla['BOTTOM0_IZQ_BOT'], text=f"{snacks[i]}$")
    texto.grid(row= contador_row[0], column= 1)
    precio.grid(row= contador_row[0], column= 2)
    locals()['cant_seleccionada_{}'.format(i)] = [0]
    cat_seleccionada =  locals()['cant_seleccionada_{}'.format(i)]
    locals()['mas_boton_{}'.format(i)] = tkinter.Button(distribucion_pantalla['BOTTOM0_IZQ_BOT'], text="+", command= lambda: sumar(cat_seleccionada, i, cant, comprado))
    locals()['mas_boton_{}'.format(i)].grid(row= contador_row[0], column= 5)
    locals()['cant_{}'.format(i)] = tkinter.Label(distribucion_pantalla['BOTTOM0_IZQ_BOT'], text=f"{cat_seleccionada[0]}")
    locals()['cant_{}'.format(i)].grid(row= contador_row[0], column= 4)
    cant = locals()['cant_{}'.format(i)] 
    locals()['menos_boton_{}'.format(i)] = tkinter.Button(distribucion_pantalla['BOTTOM0_IZQ_BOT'], text="-", command= lambda: restar(cat_seleccionada, i, cant, comprado))
    locals()['menos_boton_{}'.format(i)].grid(row= contador_row[0], column= 3)


def crear_lista_snacks(comprado, contador_row, distribucion_pantalla: dict)->None:
    contador_row[0] = 0
    for i in obtener_endpoint_json(SNACKS):
        contadores(comprado, i, contador_row, obtener_endpoint_json(SNACKS), distribucion_pantalla)
        contador_row[0] += 1
    contador_row.clear()

def confirmar_compra(valores_nuevos_con_precios, comprado, snacks, cantidad_asientos, distribucion_pantalla: dict, nombre_pelicula: str, pelicula_id: int)-> None:
    for i in snacks:
        for j in comprado:
            if i == j:
                if comprado[j] != 0:
                    valores_nuevos_con_precios[j] = {"cantidad": comprado[j], "valor total": float(snacks[i]) * comprado[j]}
    valores_nuevos_con_precios[nombre_pelicula] = {"cantidad": cantidad_asientos[0], 
                                                        "valor total": VALOR_ENTRADA * cantidad_asientos[0]}
    comprado.clear()
    cantidad_asientos.clear()
    distribucion_pantalla['PANTALLA_C'].grid_forget()
    print(valores_nuevos_con_precios)
    pagina_d(valores_nuevos_con_precios, distribucion_pantalla, nombre_pelicula, pelicula_id)
    #valores_nuevos_con_precios.clear()


def restar_asientos(cantidad_asientos, contador_asientos, add_boton,  valores_nuevos_con_precios, comprado, distribucion_pantalla: dict, nombre_pelicula: str, pelicula_id: int) -> None:
    cantidad_asientos[0] -= 1
    if cantidad_asientos[0] < 0:
        cantidad_asientos[0] = 0
    contador_asientos.config(text=f"{cantidad_asientos[0]}")
    if cantidad_asientos[0] > 0:
        add_boton.config(state= "active",command= lambda: confirmar_compra(valores_nuevos_con_precios, comprado, obtener_endpoint_json(SNACKS), cantidad_asientos, distribucion_pantalla, nombre_pelicula, pelicula_id))
    else:
        add_boton.config(state= "disabled")


def sumar_asientos(cantidad_asientos, contador_asientos, add_boton, valores_nuevos_con_precios, comprado, distribucion_pantalla: dict, nombre_pelicula: str, pelicula_id: int) -> None:
    cantidad_asientos[0] += 1
    if cantidad_asientos[0] > ASIENTOS_LIBRES:
        cantidad_asientos[0] = ASIENTOS_LIBRES
    contador_asientos.config(text=f"{cantidad_asientos[0]}")
    if cantidad_asientos[0] > 0:
        add_boton.config(state= "active",command= lambda: confirmar_compra(valores_nuevos_con_precios, comprado, obtener_endpoint_json(SNACKS), cantidad_asientos, distribucion_pantalla, nombre_pelicula, pelicula_id))
    else:
        add_boton.config(state= "disabled")


def crear_lista_pelicula(cantidad_asientos, add_boton,  valores_nuevos_con_precios, comprado, distribucion_pantalla: dict, nombre_pelicula: str, pelicula_id: int) -> None:

    titulo_pelucula = tkinter.Label(distribucion_pantalla['TOP1_DER'], text=f"{nombre_pelicula}")
    valor_asientos_pelicula = tkinter.Label(distribucion_pantalla['TOP1_DER'], text=f"{VALOR_ENTRADA}$ c/u")
    asientos_disponibles = tkinter.Label(distribucion_pantalla['TOP1_DER'], text=f"Asientos disponibles: {ASIENTOS_LIBRES}")
    texto =tkinter.Label(distribucion_pantalla['TOP2'], text=f"ELIJA LA CANTIDAD DE ENTRADAS: ")
    if cantidad_asientos[0] > 0:
        add_boton.config(state= "active",command= lambda: confirmar_compra(valores_nuevos_con_precios, comprado, obtener_endpoint_json(SNACKS), cantidad_asientos, distribucion_pantalla, nombre_pelicula, pelicula_id))
    else:
        add_boton.config(state= "disabled")

    boton_mas_pelicula = tkinter.Button(distribucion_pantalla['TOP2'], text="+", command= lambda: sumar_asientos(cantidad_asientos, contador_asientos, add_boton,  valores_nuevos_con_precios, comprado, distribucion_pantalla, nombre_pelicula, pelicula_id))
    boton_menos_pelicula = tkinter.Button(distribucion_pantalla['TOP2'], text="-", command= lambda: restar_asientos(cantidad_asientos, contador_asientos, add_boton,  valores_nuevos_con_precios, comprado, distribucion_pantalla, nombre_pelicula, pelicula_id))
    contador_asientos = tkinter.Label(distribucion_pantalla['TOP2'], text=f"{cantidad_asientos[0]}")
    titulo_pelucula.grid(row= 0, column=0)
    valor_asientos_pelicula.grid(row= 1, column=0)
    asientos_disponibles.grid(row=2, column=0)
    texto.grid(row= 0, column=1)
    boton_menos_pelicula.grid(row= 1, column=0)
    contador_asientos.grid(row= 1, column=1)
    boton_mas_pelicula.grid(row=1, column=2)


def mostrar(snacks, toggle, comprado, contador_row_snacks, vm, distribucion_pantalla: dict):
    if snacks.winfo_ismapped():
        snacks.grid_forget()
        toggle.config(text= "MOSTRAR SNACKS")
        comprado.clear()
        vm.clear()
        print(comprado)
    else:
        snacks.grid()
        toggle.config(text= "OCULTAR SNACKS")
        crear_lista_snacks(comprado, contador_row_snacks, distribucion_pantalla)


# PAGINA D 


def pagina_d (diccionario, distribucion_pantalla: dict, nombre_pelicula: str, pelicula_id: int) -> None:
    distribucion_pantalla['PANTALLA_D'].grid()
    dentro_pantalla = tkinter.Label(distribucion_pantalla['PANTALLA_D'])
    dentro_pantalla.grid()
    count_row = 0
    contador_total_valor = 0
    #lista_variables = []
    for i in diccionario:
        count_row += 1
        #
        locals()['text_{}'.format(i)] = tkinter.Label(dentro_pantalla, text=f"{i}")
        locals()['text_{}'.format(i)].grid(row= count_row, column=0)
        cantidad_dict = diccionario[i]["cantidad"]
        #
        locals()['cantidad_{}'.format(i)] = tkinter.Label(dentro_pantalla, text=f"x{cantidad_dict}")
        locals()['cantidad_{}'.format(i)].grid(row= count_row, column=1)
        valor_total_dict = diccionario[i]["valor total"]
        #
        locals()['valor_total_{}'.format(i)] = tkinter.Label(dentro_pantalla, text=f" ${valor_total_dict}")
        locals()['valor_total_{}'.format(i)].grid(row= count_row, column=2)
        contador_total_valor += diccionario[i]["valor total"]
    count_row += 1
    total = tkinter.Label(dentro_pantalla, text=f"TOTAL: ${contador_total_valor}")
    total.grid(row= count_row, column=0)
    count_row += 1
    boton_mostrar_qr = tkinter.Button(dentro_pantalla, text= "GENERAR QR", command= lambda: generar_qr(diccionario, boton_mostrar_qr, nombre_pelicula))
    boton_mostrar_qr.grid(row= count_row, column=0)
    count_row += 1
    boton_atras = tkinter.Button(dentro_pantalla, text="VOLVER ATRÁS", command= lambda: llamar_pagina_c(diccionario, dentro_pantalla, distribucion_pantalla, nombre_pelicula, pelicula_id))
    boton_atras.grid(row= count_row)


def generar_qr(diccionario, boton_mostrar_qr, nombre_pelicula) -> None:
    boton_mostrar_qr.config(state= "disabled")
    hora_actual = datetime.now().strftime("%d.%m.%y_%H:%M")
    id = f"{hora_actual}/{diccionario[nombre_pelicula]['cantidad']}/{nombre_pelicula}/{ID_UBICACION}"
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(id)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="black", back_color="white")
    qr_img.save("qr\codigo_qr.png")
    texto = f"QR_ID: {id}"
    with open("qr\codigo_qr.pdf", "wb") as pdf_file:
        c = canvas.Canvas(pdf_file)
        c.drawInlineImage("qr\codigo_qr.png", 100, 500, width=200, height=200)
        c.drawString(100, 500, texto)
        c.save()
    compra_total_qr = {}
    compra_total_qr[id] = diccionario
    with open ("datos_compra.txt", "w") as datos_compra:
        json.dump(compra_total_qr, datos_compra)
    diccionario.clear()


def llamar_pagina_c (diccionario, dentro_pantalla, distribucion_pantalla: dict, nombre_pelicula: str, pelicula_id: int) -> None:
    distribucion_pantalla['PANTALLA_D'].grid_forget()
    dentro_pantalla.grid_forget()
    diccionario.clear()
    #PANTALLA_C.grid()
    pagina_c(distribucion_pantalla, nombre_pelicula, pelicula_id)


def pagina_c(distribucion_pantalla: dict, nombre_pelicula: str, pelicula_id: int) -> None:
    distribucion_pantalla['PANTALLA_C'].grid()
    distribucion_pantalla['BOTTOM0_IZQ_BOT'].grid_forget()
    distribucion_pantalla['root'].title("3er pagina")
    comprado: dict = {}
    #comprado.clear()
    valores_nuevos_con_precios: dict = {}
    #valores_nuevos_con_precios.clear()
    volver_buton = tkinter.Button(distribucion_pantalla['TOP0'], text="VOLVER ATRAS", command= lambda: volver_pantalla_secundaria(pelicula_id, distribucion_pantalla))
    volver_buton.place(relx=0.5, rely=0.3, anchor="center")
    contador_row_snacks: list = [0]
    #contador_row_snacks.clear()
    cantidad_asientos: list = [0]
    #cantidad_asientos.clear()
    toggle = tkinter.Button(distribucion_pantalla['BOTTOM0_IZQ_TOP'], text= "MOSTRAR SNACKS", command= lambda: mostrar(distribucion_pantalla['BOTTOM0_IZQ_BOT'], toggle, comprado, contador_row_snacks, valores_nuevos_con_precios, distribucion_pantalla))
    add_boton = tkinter.Button(distribucion_pantalla['BOTTOM0_DER'], text="FINALIZAR")
    crear_lista_pelicula(cantidad_asientos, add_boton, valores_nuevos_con_precios, comprado, distribucion_pantalla, nombre_pelicula, pelicula_id)
    toggle.grid(row= 0, column=0)
    add_boton.place(relx=0.8, rely=0.8, anchor="center")

def volver_pantalla_secundaria(pelicula_id: int, distribucion_pantalla: dict):
    distribucion_pantalla["PANTALLA_C"].grid_forget()
    condicion: bool = False
    pantalla_secundaria(pelicula_id, condicion)


#MAIN#

def main() -> None:

    iniciar_pantalla_principal()

main()