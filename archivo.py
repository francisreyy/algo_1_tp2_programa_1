import requests
import tkinter
import base64
from io import BytesIO
from PIL import Image, ImageTk
import os
from datetime import datetime
import qrcode
from reportlab.pdfgen import canvas
import json


URL: str = "http://vps-3701198-x.dattaweb.com:4000"
PELICULAS: str = "/movies/"
POSTERS : str = "/posters/"
SNACKS: str = "/snacks/"
CINES: str = "/cinemas/"
TOKEN: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.DGI_v9bwNm_kSrC-CQSb3dBFzxOlrtBDHcEGXvCFqgU"
HEADERS: dict[str, str] = {"Authorization": "Bearer " + TOKEN}

PRECIO_ENTRADAS: int = 2000

#funciones para la pantalla de finalizar compra#


def pantalla_loop(info_ticket: dict) -> None:
    """
    PRE: simplemente pantalla que agradece la compra y permite volver a la pantalla de seleccion de 
    sucursal.
    """
    info_ticket['ASIENTOS_DISPONIBLES'][f"{nombre_cine(info_ticket['ID_CINE'])}"][info_ticket['NUM_SALA_PELICULA']-1] -= info_ticket['CANT_ENTRADAS']

    ventana = tkinter.Tk()
    ventana.title("GRACIAS!!")
    mensaje = tkinter.Label(ventana, text= "GRACIAS POR SU COMPRA!!", font= "Helvetica 20 bold")
    mensaje.grid(column=0, row=0)
    boton = tkinter.Button(ventana, text= "VOLVER AL INICIO", font= "Helvetica 20 bold",
                            command= lambda: accion_volver_bienvenida(info_ticket, ventana))
    boton.grid(column=0, row=1)
  
    ventana.mainloop()


def generar_qr(info_ticket: dict, diccionario: dict, pantalla_final) -> None:
    """
    PRE: una vez se confirma la compra, se procede a generar el qr y id de la misma con la informacion
    necesaria para el siguiete programa. Ademas genera un json con esa informacion.
    """
    pantalla_final.destroy()

    hora_actual = datetime.now().strftime("%d.%m.%y_%H:%M")
    id_code = f"{hora_actual}/{info_ticket['CANT_ENTRADAS']}/{consultar_info_pelicula(info_ticket['ID_PELICULA'],'name')}/{info_ticket['LOCALIZACION']}"
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    
    carpeta_qr = "qr"
    if not os.path.exists(carpeta_qr):
        os.makedirs(carpeta_qr)
        print(f"Se ha creado la carpeta '{carpeta_qr}'.")
    else:
        print(f"La carpeta '{carpeta_qr}' ya existe.")
    
    qr.add_data(id_code)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="black", back_color="white")
    qr_img.save("qr/codigo_qr.png")
    texto: str = f"QR_ID: {id_code}"

    with open("qr/codigo_qr.pdf", "wb") as pdf_file:
        c = canvas.Canvas(pdf_file)
        c.drawInlineImage("qr/codigo_qr.png", 100, 500, width=200, height=200)
        c.drawString(100, 500, texto)
        c.save()

    compra_total_qr: dict = {f"{id_code}": diccionario}

    if os.path.exists("datos_compra.json"):
        with open ("datos_compra.json", "r") as datos_compra:
            datos = json.load(datos_compra)

        datos[f"{id_code}"] = diccionario

        with open ("datos_compra.json", "w") as datos_compra:
            json.dump(datos, datos_compra, indent= 4)
    else:
        with open ("datos_compra.json", "w") as datos_compra:
            json.dump(compra_total_qr, datos_compra, indent= 4)

    diccionario.clear()
    pantalla_loop(info_ticket)


def llamar_pagina_c (info_ticket, pantalla_final) -> None:
    """
    PRE: regresa a la pantalla de reserva vacia los valores de cantidad de entradas, snacks y demas para no pisar los valores
    al volver atras. 
    """

    pantalla_final.destroy()

    info_ticket['CANT_ENTRADAS'] = 0
    info_ticket['SNACKS_COMPRADOS'].clear()
    info_ticket['VALOR_POR_SNACKS'] = 0
    info_ticket['PRECIO_TOTAL'] = 0
    
    pantalla_reseva(info_ticket)


def pagina_d (info_ticket, root) -> None:
    """
    PRE: genera la pantalla de confirmar compra, listando el resumen de la compra.
    """

    root.destroy()
    
    pantalla_final = tkinter.Tk()
    
    #pantalla_d = tkinter.Frame(pantalla_final, width=500, height=620)
    pantalla_d = tkinter.Frame(pantalla_final)
    pantalla_d.grid()

    count_row: int = 0
    diccionario: dict = {}

    diccionario[f"{consultar_info_pelicula(info_ticket['ID_PELICULA'],'name')}"] = {}
    diccionario[f"{consultar_info_pelicula(info_ticket['ID_PELICULA'],'name')}"]["cantidad"] = info_ticket['CANT_ENTRADAS']
    diccionario[f"{consultar_info_pelicula(info_ticket['ID_PELICULA'],'name')}"]["valor total"] = info_ticket['VALOR_TOTAL_ENTRADAS']

    if len(info_ticket['SNACKS_COMPRADOS']) > 0:
        for snacks in info_ticket['SNACKS_COMPRADOS']:
            for nombre_snack in snacks:
                diccionario[f"{nombre_snack}"] = {"cantidad": 0, "valor total": 0}
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
                diccionario[f"{nombre_snack}"]["cantidad"]= cantidad_comprada
                diccionario[f"{nombre_snack}"]["valor total"]= total_por_cada_snack

    count_row +=1 
    text = tkinter.Label(pantalla_d, text= consultar_info_pelicula(info_ticket['ID_PELICULA'],'name'))
    text.grid(row= count_row, column=0)
    cantidad_etiqueta = tkinter.Label(pantalla_d, text= f"x{info_ticket['CANT_ENTRADAS']}")
    cantidad_etiqueta.grid(row= count_row, column=1)
    total_snack_etiqueta = tkinter.Label(pantalla_d, text=f" ${info_ticket['VALOR_TOTAL_ENTRADAS']}")
    total_snack_etiqueta.grid(row= count_row, column=2)
    count_row +=1 
    total = tkinter.Label(pantalla_d, text=f"TOTAL: ${info_ticket['PRECIO_TOTAL']}")
    total.grid(row= count_row, column=0)
    count_row += 1
   
    boton_mostrar_qr = tkinter.Button(pantalla_d, text= "GENERAR QR",  command= lambda: generar_qr(info_ticket, diccionario, pantalla_final))
    boton_mostrar_qr.grid(row= count_row, column=0)


#funciones para la pantalla de reserva#


def suma_valor_snacks(info_ticket: dict) -> int:
    """
    PRE: suma el valor de cada snack seleccionado y entre su cantidad y el valor del mismo.
    """
    total_por_snacks: float = 0
    diccionario_snacks: dict = obtener_endpoint_json(SNACKS)

    if len(info_ticket['SNACKS_COMPRADOS']) > 0:
        for snacks_comprados in info_ticket['SNACKS_COMPRADOS']:
            for snack in snacks_comprados:
                cant: int = snacks_comprados[snack]
                valor: float = float(diccionario_snacks[snack])

                total_por_snacks += cant * valor    

    return total_por_snacks


def confirmar_compra(root, info_ticket: dict) -> None:
    """
    PRE: al confirmar la compra guarda toda la informacion, numero de entradas y snacks, el valor de todo por separado,
    ya sea por cada snack junto con su cantidad, y lo mismo con las entradas. Abre la pagina de confirmar compra.
    """
    info_ticket['VALOR_TOTAL_ENTRADAS'] = info_ticket['CANT_ENTRADAS'] * info_ticket['VALOR_CADA_ENTRADA']
    info_ticket['VALOR_TOTAL_SNACKS'] = suma_valor_snacks(info_ticket)
    info_ticket['PRECIO_TOTAL'] = info_ticket["VALOR_TOTAL_ENTRADAS"] + info_ticket["VALOR_TOTAL_SNACKS"]

    pagina_d(info_ticket, root)


def sumar_snack(cantidad_seleccionada: list, nombre_snack: str, cant_a_mostrar, info_ticket: dict) -> None:
    """
    PRE: se ejecuta al presionar el boton "+" del apartado de snacks, y suma la cantidad en 1 mostrandolo al usuario,
    se puede seleccionar la cantidad que quiera.
    """
    cantidad_seleccionada[0] += 1
    snack_nombre_y_cantidad: dict = {nombre_snack: cantidad_seleccionada[0]}

    if cantidad_seleccionada[0] == 1:    
        info_ticket['SNACKS_COMPRADOS'].append(snack_nombre_y_cantidad)
    else:
        for i in range (len(info_ticket['SNACKS_COMPRADOS'])):
            if nombre_snack in info_ticket['SNACKS_COMPRADOS'][i].keys():
                info_ticket['SNACKS_COMPRADOS'][i][nombre_snack] += 1

    cant_a_mostrar.config( text= f"{cantidad_seleccionada[0]}")


def restar_snack(cantidad_seleccionada: list, nombre_snack: str, cant_a_mostrar, info_ticket: dict) -> None:
    """
    PRE: se ejecuta al presionar el boton "-" del apartado de snacks, y resta la cantidad en 1 mostrandolo al usuario,
    no deja seleccionar menos de 0.
    """
    cantidad_seleccionada[0] -= 1

    if cantidad_seleccionada[0] < 0:
        cantidad_seleccionada[0] = 0

    snacks: list = list(info_ticket['SNACKS_COMPRADOS'])

    if cantidad_seleccionada[0] == 0:
        for i in range (len(snacks)):
            if nombre_snack in snacks[i].keys():
                del info_ticket['SNACKS_COMPRADOS'][i]

    if cantidad_seleccionada[0] > 0:
        for i in range (len(info_ticket['SNACKS_COMPRADOS'])):
            if nombre_snack in info_ticket['SNACKS_COMPRADOS'][i].keys():
                info_ticket['SNACKS_COMPRADOS'][i][nombre_snack] -= 1

    cant_a_mostrar.config( text= f"{cantidad_seleccionada[0]}")


def contadores(BOTTOM0_IZQ_BOT, info_ticket: dict, snack: str, contador_row: list, snacks_dict: list) -> None:
    """
    PRE: se encarga de la creacion de los botones "+" y "-" de cada snack.
    """
    texto = tkinter.Label(BOTTOM0_IZQ_BOT, text=f"{snack}")
    precio = tkinter.Label(BOTTOM0_IZQ_BOT, text=f"{snacks_dict[snack]}$")
    texto.grid(row= contador_row[0], column= 1)
    precio.grid(row= contador_row[0], column= 2)
    cantidad_seleccionada = [0]
    cant_seleccionada =  cantidad_seleccionada
    #print(cant_seleccionada)
    mas_boton = tkinter.Button(BOTTOM0_IZQ_BOT, text="+", command= lambda: sumar_snack(cant_seleccionada, snack, cant_a_mostrar, info_ticket))
    mas_boton.grid(row= contador_row[0], column= 5)
    cant = tkinter.Label(BOTTOM0_IZQ_BOT, text=f"{cant_seleccionada[0]}")
    cant.grid(row= contador_row[0], column= 4)
    cant_a_mostrar = locals()['cant_{}'.format(snack)]
    menos_boton = tkinter.Button(BOTTOM0_IZQ_BOT, text="-", command= lambda: restar_snack(cant_seleccionada, snack, cant_a_mostrar, info_ticket))
    menos_boton.grid(row= contador_row[0], column= 3)


def crear_lista_snacks(BOTTOM0_IZQ_BOT, info_ticket: dict) -> None:
    """
    PRE: crea la lista de snacks disponibles mediante la API y los muestra.
    """
    snacks_dict: dict = obtener_endpoint_json(SNACKS)

    contador_row: list = [0]

    for snack in snacks_dict:
        contadores(BOTTOM0_IZQ_BOT, info_ticket, snack, contador_row, snacks_dict)
        contador_row[0] += 1


def restar_entradas(root, info_ticket: dict, contador_asientos, add_boton) -> None:
    """
    PRE: se ejecuta al presionar el boton "-" del apartado de entradas, y resta la cantidad en 1 mostrandolo al usuario,
    no deja seleccionar menos de 0.
    """
    info_ticket['CANT_ENTRADAS'] -= 1

    if info_ticket['CANT_ENTRADAS'] < 0:
        info_ticket['CANT_ENTRADAS'] = 0

    contador_asientos.config(text=f"{info_ticket['CANT_ENTRADAS']}")

    if info_ticket['CANT_ENTRADAS'] > 0:
        add_boton.config(state= "active",command= lambda: confirmar_compra(root, info_ticket))
    else:
        add_boton.config(state= "disabled")


def sumar_entradas(root, info_ticket: dict, contador_asientos, add_boton) -> None:
    """
    PRE: se ejecuta al presionar el boton "+" del apartado de entradas, y suma la cantidad en 1 mostrandolo al usuario,
    no deja seleccionar mas de la cantidad de asientos de la sala.
    """

    info_ticket['CANT_ENTRADAS'] += 1
    num_asientos: int = info_ticket['ASIENTOS_DISPONIBLES'][f"{nombre_cine(info_ticket['ID_CINE'])}"][info_ticket['NUM_SALA_PELICULA']-1]

    if info_ticket['CANT_ENTRADAS'] > num_asientos :
        info_ticket['CANT_ENTRADAS'] = num_asientos

    contador_asientos.config(text=f"{info_ticket['CANT_ENTRADAS']}")

    if info_ticket['CANT_ENTRADAS'] > 0:
        add_boton.config(state= "active",command= lambda: confirmar_compra(root, info_ticket))
    else:
        add_boton.config(state= "disabled")


def mostrar(snacks, toggle, info_ticket: dict) -> None:
    """
    PRE: se ejecuta al usar el boton "MOSTRAS/OCULTAR SNACKS", si los snacks estan desplegados,
    los oculta y vacia los snacks seleccionados, caso contrario obtiene la informacion de la API y muestra
    los snacks.
    """
    if snacks.winfo_ismapped():
        snacks.grid_forget()
        toggle.config(text= "MOSTRAR SNACKS")
        info_ticket['SNACKS_COMPRADOS'].clear()
        print(info_ticket['SNACKS_COMPRADOS'])
    else:
        snacks.grid()
        toggle.config(text= "OCULTAR SNACKS")
        crear_lista_snacks(snacks, info_ticket)


def crear_lista_pelicula(root, TOP1_DER, TOP2, info_ticket: dict, add_boton) -> None:
    """
    PRE: genera la parte superior de la pantalla de reserva, con la informacion como nombre de la pelicula, valor de las entradas,
    ubicacion, etc, genera los botones para sumar/restar entradas.
    """

    nombre_pelicula: str = consultar_info_pelicula(info_ticket['ID_PELICULA'],'name')
    titulo_pelicula = tkinter.Label(TOP1_DER, text=f"{nombre_pelicula}")
    valor_asientos_etiqueta = tkinter.Label(TOP1_DER, text=f"{info_ticket['VALOR_CADA_ENTRADA']}$ c/u")
    num_asientos: int = info_ticket['ASIENTOS_DISPONIBLES'][f"{nombre_cine(info_ticket['ID_CINE'])}"][info_ticket['NUM_SALA_PELICULA']-1]
    asientos_disponibles_etiqueta = tkinter.Label(TOP1_DER, text=f"Asientos disponibles: {num_asientos}") #asientos_disponibles(ID_UBICACION)
    texto =tkinter.Label(TOP2, text=f"ELIJA LA CANTIDAD DE ENTRADAS: ")

    if info_ticket['CANT_ENTRADAS'] > 0:
        add_boton.config(state= "active",command= lambda: confirmar_compra(root, info_ticket))
    else:
        add_boton.config(state= "disabled")

    boton_mas_pelicula = tkinter.Button(TOP2, text="+", 
                                        command= lambda: sumar_entradas(root, info_ticket, contador_asientos, add_boton))
    boton_menos_pelicula = tkinter.Button(TOP2, text="-", 
                                        command= lambda: restar_entradas(root, info_ticket, contador_asientos, add_boton))
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
    PRE: se ejecuta de despues de presionar "volver atras" desde la pantalla de reserva, vacia los valores de snacks,
    cantidad de entradas, y los valores en caso de que se hayan guardado, y vuelve a generar la pantalla secundaria.
    """

    root.destroy()

    info_ticket['CANT_ENTRADAS'] = 0
    info_ticket['SNACKS_COMPRADOS'].clear()
    info_ticket['VALOR_POR_SNACKS'] = 0
    info_ticket['PRECIO_TOTAL'] = 0

    pantalla_secundaria(info_ticket)


def pantalla_reseva(info_ticket: dict) -> None:
    """
    PRE: se ejecuta luego de presionar el boton de reservar y dimensiona la pantalla de reserva.
    """

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
    BOTTOM0_IZQ_BOT.grid_forget()

    root.title("3er pagina")

    volver_buton = tkinter.Button(TOP0, text="VOLVER", command= lambda: volver_pagina_secundaria(root, info_ticket))
    volver_buton.place(relx=0.5, rely=0.3, anchor="center")

    toggle = tkinter.Button(BOTTOM0_IZQ_TOP, text= "MOSTRAR SNACKS", command= lambda: mostrar(BOTTOM0_IZQ_BOT, toggle, info_ticket))
    add_boton = tkinter.Button(BOTTOM0_DER, text="FINALIZAR")
    crear_lista_pelicula(root, TOP1_DER, TOP2, info_ticket, add_boton)
    toggle.grid()
    add_boton.place(relx=0.8, rely=0.8, anchor="center")
    root.mainloop()


#funciones para la pantalla secundaria#


def info_poster(pelicula_id: int) -> str:
    """
    PRE: segun el id de la pelicula busca el poster.

    POST: devuelve el str base64 del poster.
    """

    archivo = requests.get(URL + POSTERS + pelicula_id, headers= HEADERS)
    poster_pelicula: dict = archivo.json()
    imagen_poster: str = poster_pelicula["poster_image"]
    imagen_poster = imagen_poster[imagen_poster.index(",")+1:]

    return imagen_poster


def creacion_pantalla(poster: str, info_ticket: dict) -> None:
    """
    PRE: crea la pantalla secundaria con toda la informacion de la pelicula seleccionada, mediante su id.
    Primero ve si el numero de sala de la pelicula posee asientos disponibles en su posicion de la lista segun el nombre de sucursal,
    si tiene asientos disponibles deja reservar, caso contrario muestra "ENTRADAS AGOTADAS",
    en este caso la sala se otorga segun su orden en la lista de la API
    (si la pelicula seleccionada es la primera en la lista de la API se le otorga la sala 1, y asi sucesivamente)
    """

    sinopsis: str = consultar_info_pelicula(info_ticket['ID_PELICULA'],'synopsis') #muy largo, hay que hacerlo por renglones
    actores: str = consultar_info_pelicula(info_ticket['ID_PELICULA'],'actors')
    director: str = consultar_info_pelicula(info_ticket['ID_PELICULA'],'directors')
    duracion: str = consultar_info_pelicula(info_ticket['ID_PELICULA'],'duration')
    genero: str = consultar_info_pelicula(info_ticket['ID_PELICULA'],'gender')
    portada: str = poster
    nombre_pelicula: str = consultar_info_pelicula(info_ticket['ID_PELICULA'],'name')
    asientos_disponibles_sala: int = info_ticket['ASIENTOS_DISPONIBLES'][f"{nombre_cine(info_ticket['ID_CINE'])}"][info_ticket['NUM_SALA_PELICULA']-1]

    imagen = base64.b64decode(portada)
    imagen_final = Image.open(BytesIO(imagen))
    jpg= imagen_final.convert("RGB")
    jpg.save('portada.png')
    pantalla_2 = tkinter.Tk()
    pantalla_2.title(f"{nombre_pelicula}")

    TOP0_MID = tkinter.Label(pantalla_2, text= f"SALA {info_ticket['NUM_SALA_PELICULA']}",
                            font= "Helvetica 20 bold")#numero de sala
    TOP0_DER = tkinter.Button(pantalla_2, text="VOLVER ATRAS",
                            font= "Helvetica 15 bold", command= lambda: boton_atras_principal(pantalla_2, info_ticket))#boton volver atras
    IMAGEN = tkinter.PhotoImage(file= 'portada.png')
    TOP1_IZQ = tkinter.Label(pantalla_2, image= IMAGEN)#,
                            #width=200, height=200)# dimensiones portada
    TOP1_DER = tkinter.Frame(pantalla_2,
                            width=200, height=200)
    TOP1_ARRIBA = tkinter.Label(TOP1_DER, text= f"SINOPSIS \n {sinopsis}",
                                font= "Helvetica 10 bold", justify= "left", wraplength= 400)#sinopsis mayor a 400 más ancho, menor más angosto
    TOP1_ABAJO = tkinter.Label(TOP1_DER, text= f"ACTORES: {actores}\nDIRECTOR: {director}\nDURACIÓN DE LA PELICULA: {duracion}",
                                font= "Helvetica 10 bold", justify= "left")#actores, director, duracion
    TOP2_IZQ = tkinter.Label(pantalla_2, text= f"GÉNERO: {genero}",
                            font= "Helvetica 15 bold", justify= "left")#genero
    
    if asientos_disponibles_sala > 0:
        BOTTOM = tkinter.Button(pantalla_2, text= "RESERVAR",
                            font= "Helvetica 15 bold", command= lambda: boton_reservar(pantalla_2, info_ticket))#boton RESERVAR
    else: BOTTOM = tkinter.Label(pantalla_2, text= "ENTRADAS AGOTADAS", font= "Helvetica 15 bold")

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


def pantalla_secundaria(info_ticket: dict) -> None:
    """
    PRE: crea la pantalla secundaria y obtiene el poster de la pelicula seleccionada.
    """

    poster = info_poster(info_ticket['ID_PELICULA'])
    creacion_pantalla(poster, info_ticket)


def boton_reservar(pantalla_2, info_ticket: dict) -> None:
    """
    PRE: te lleva de la pantalla secundaria a la pantalla de reserva, luego de presionar el boton "reservar".
    """

    pantalla_2.destroy()

    pantalla_reseva(info_ticket)


def boton_atras_principal(pantalla_2, info_ticket: dict) -> None:
    """
    PRE: procedimiento que cierra la pantalla secundaria y abre la pantalla principal luego de
    ejecutar el boton "volver atras"
    """

    pantalla_2.destroy()
    
    iniciar_pantalla_principal(info_ticket)


def obtener_endpoint_json(endpoint: str, id_pelicula_o_cine: str = "", pelicula_o_cine : str = "") -> str:
    """
    PRE: Función que recibe parte strings para formar el link del endpoint (la id tiene que ser casteada a string 
    con "1" por ejemplo).

    POST: Devuelve la información del endpoint en forma de lista o diccionario (depende el endpoint).
    """
    texto: str ="""
    Se podrujo un error de
    conexion con la API
    """
    try:
        dato = requests.get(URL+ endpoint + id_pelicula_o_cine + pelicula_o_cine, headers=HEADERS)
        return dato.json()
    except requests.exceptions.RequestException as e:
        error_pagina = tkinter.Tk()
        error_pagina.grid()
        texto_sin_conexion = tkinter.Label(error_pagina, text=texto, font= "Helvetica 40 bold", justify="center")
        texto_sin_conexion.grid(row= 0, column=0)
        error_pagina.mainloop()


def consultar_info_pelicula(id_pelicula: int, clave_pelicula: str) -> str:
    """
    PRE: Función que recibe la id de una película como entero y
    una clave del diccionario película como string.

    POST: Devuelve por ejemplo la sinopsis de la película como string
    (todos los valores de las claves son strings).
    """
    info_pelicula: dict = obtener_endpoint_json(PELICULAS, str(id_pelicula))

    return info_pelicula[clave_pelicula]


def asientos_disponibles(id_cine: int) -> int:
    """
    PRE: Función que recibe id del cine en enteros.

    POST: devuelve un entero indicando la cantidad de asientos que dispone el cine(en este caso, tomamos que
    el numero indica a la cantidad de asientos por sala)
    """
    info_cines: list = obtener_endpoint_json(CINES)
    info_cine: dict = info_cines[id_cine-1]
    asientos: int = info_cine['available_seats']

    return int(asientos)


def nombre_cine(id_cine: int) -> str:
    """
    PRE: Función que recibe id del cine en entero.

    POST: devuelve un string con el nombre de la ubicación.
    """

    info_cines: list = obtener_endpoint_json(CINES)
    info_cine: dict = info_cines[id_cine-1]
    nombre_cine: str = info_cine['location']

    return nombre_cine.upper()


def obtener_imagen_base64(i: int):
    """
    PRE: Función que recibe una id como entero, pregunta a la API por su base64, la transforma a binario y luego a PhothoImage.

    POST: Devuelve la imagen como PhotoImage.
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
    con "1" por ejemplo).

    POST: Devuelve la cantidad de elementos de la lista.
    """

    dato = requests.get(URL + endpoint + id_pelicula_o_cine + pelicula_o_cine , headers=HEADERS)
    cantidad_elementos: int = len(dato.json())

    return cantidad_elementos


def accion_del_boton(id_pelicula_elegida: int, info_ticket: dict, pantalla_principal, num_sala: int) -> None:
    """
    PRE: Procedimiento que realiza el botón imagen de la página principal al ser presionado
    Guarda la id de la película clickeada en el diccionario principal para usarlo en pantallas posteriores, ademas
    realiza la accion de ejecutar la siguiente pantalla.
    """

    pantalla_principal.destroy()

    info_ticket['ID_PELICULA'] = str(id_pelicula_elegida)
    info_ticket['NUM_SALA_PELICULA'] = num_sala

    pantalla_secundaria(info_ticket)


def accion_volver_bienvenida(info_ticket: dict, pantalla)->None:
    """
    PRE: se ejecuta luego de presionar el boton de volver atras en la pantalla con las carteleras(principal),
    vuelve a la pantalla de seleccion de sucursal, y vacia toda la informacion sobre la sucursal anterior del diccionario.
    """
    pantalla.destroy()

    info_ticket['LOCALIZACION'] = ""
    info_ticket['ID_CINE'] = ""
    info_ticket['CANT_SALAS'] = 0
    info_ticket['CANT_ENTRADAS'] = 0
    info_ticket['SNACKS_COMPRADOS'].clear()
    info_ticket['VALOR_POR_SNACKS'] = 0
    info_ticket['PRECIO_TOTAL'] = 0

    bienvenida(info_ticket)


def crear_lista_nombres_peliculas(peliculas_proyec: list) -> list:
    """
    PRE: mediante la lista de peliculas proyectadas, obtiene el nombre de todas ellas y las guarda en una lista.

    POST: devuelve dicha lista con el nombre de las peliculas.
    """

    nombres_peliculas: list = []

    for id_pelicula in peliculas_proyec:  
        id: int = int(id_pelicula)

        nombre_pelicula: str = consultar_info_pelicula(id, 'name')

        nombres_peliculas.append(nombre_pelicula)
 
    return nombres_peliculas


def buscar_pelicula(entrada, info_ticket: dict, pantalla_principal) -> None:
    """
    PRE: busca la pelicula mediante la entrada obtenida de la barra de busqueda y compara esa entrada con todos los 
    nombres de las peliculas.
    """

    peliculas_proyec: list = peliculas_proyectadas(info_ticket)[0]['has_movies']
    nombres_peliculas: list = crear_lista_nombres_peliculas(peliculas_proyec)
    copia: list = peliculas_proyec.copy()
    buscado: str = entrada.get()
    texto: str = buscado.upper()
    peliculas_proyec.clear()

    for nombre in nombres_peliculas:
        if texto in nombre:
            posicion: int = nombres_peliculas.index(nombre)
            peliculas_proyec.append(copia[posicion])

    info_ticket['PELICULAS_PROYECTADAS'] = peliculas_proyec

    pantalla_principal.destroy()

    iniciar_pantalla_principal(info_ticket)


def peliculas_proyectadas(info_ticket: dict)-> dict:
    """
    PRE: funcion que obtiene de la API el id de las peliculas proyectadas en la sucursal mediante su id.

    POST: devuelve el diccionario de la API con id del cine y la lista de id de peliculas.
    """
    
    info_cine: dict = obtener_endpoint_json(CINES, f"{info_ticket['ID_CINE']}", PELICULAS)

    return info_cine


def iniciar_pantalla_principal(info_ticket: dict) -> None:
    """
    PRE: inicia la pantalla principal, mostrando la ubicacion y la cartelera de la sucursal elegida previamente, incluyendo
    la barra de busqueda de una pelicula. Cada cartelera de pelicula es un boton que lleva a mostrar toda la informacion de la misma.
    """
    pantalla_principal = tkinter.Tk()
    pantalla_principal.title("Totem cine")
    cantidad_peliculas = cantidad_de_elementos_json(PELICULAS)
    encabezado = tkinter.Frame(pantalla_principal, bg= "gray")
    encabezado.pack(expand = True, fill= "both")
    volver_atras = tkinter.Button(encabezado, text = "Volver Atras",
                                   command= lambda: accion_volver_bienvenida(info_ticket, pantalla_principal))
    volver_atras.pack()
    texto = tkinter.Label(encabezado, text = f"{info_ticket['LOCALIZACION']} CINEMA")
    texto.pack()
    entrada = tkinter.Entry(encabezado, justify= "center")
    entrada.pack()
    barra_busqueda = tkinter.Button(encabezado, text = "Buscá la película", justify= "center",
                                     command= lambda: buscar_pelicula(entrada, info_ticket, pantalla_principal))
    barra_busqueda.pack()
    cuerpo_pagina = tkinter.Frame(pantalla_principal, bg= "black")
    cuerpo_pagina.pack(expand= True, fill= "both")
    imagenes: list = []
    fila: int = 0
    columna: int = 0
    contador_sala: int = 0

    if len(info_ticket['PELICULAS_PROYECTADAS']) == 0:
        etiqueta_de_peliculas_no_encontradas = tkinter.Label(cuerpo_pagina, text = "No se han encontrado resultados o se ha perdido la conexión con el servidor")
        etiqueta_de_peliculas_no_encontradas.pack()
        etiqueta = tkinter.Label(cuerpo_pagina, text = "Intente otra vez")
        etiqueta.pack()

    else:
        for i in range(1, cantidad_peliculas + 1):
            if f"{i}" in info_ticket['PELICULAS_PROYECTADAS']:
                contador_sala +=1 
                imagen_tk = obtener_imagen_base64(i)
                imagenes.append(imagen_tk)
                boton = tkinter.Button(cuerpo_pagina, image = imagen_tk, command= lambda i=i, contador_sala=contador_sala: accion_del_boton(i, info_ticket, pantalla_principal, contador_sala))
                boton.grid(column= columna, row = fila)
                columna += 1

            if columna > 5:
                columna = 0
                fila += 1

    pantalla_principal.mainloop()


def accion_ir_principal(info_ticket: dict, pantalla_bienvenida, id_cine: int) -> None:
    """
    PRE: se ejecuta una vez se presiona el boton de una sucursal, pasando la informacion necesaria de la misma, mediante
    el diccionario principal(info_ticket), como id, nombre, peliculas proyectadas y cantidad de salas.
    """
    pantalla_bienvenida.destroy()
    info_ticket['ID_CINE'] = id_cine
    info_ticket['LOCALIZACION'] = nombre_cine(id_cine)

    info_ticket['PELICULAS_PROYECTADAS'] = peliculas_proyectadas(info_ticket)[0]['has_movies']   
    info_ticket['CANT_SALAS'] = len(info_ticket['PELICULAS_PROYECTADAS'])

    iniciar_pantalla_principal(info_ticket)


def bienvenida(info_ticket: dict) -> None:
    """
    PRE: este procedimiento genera la pantalla de seleccion de sucursal, y pasara a la pantalla principal.
    """

    mensaje: str = """
    BIENVENIDO, SELECCIONE EL 
    COMPLEJO PARA INICIAR UNA COMPRA
    """
    pantalla_bienvenida = tkinter.Tk()
    pantalla_bienvenida.title("BIENVENIDO")
    pantalla_bienvenida.config(bg="black")
    mensaje = tkinter.Label(pantalla_bienvenida, text= mensaje,
                             font= "Helvetica 20 bold")
    mensaje.grid(row=0)
    frame_button = tkinter.Frame(pantalla_bienvenida, bg="black")
    frame_button.grid(row=1)

    fila: int = 1
    columna: int = 0
    for i in range(1, 7+1):

        boton = tkinter.Button(frame_button, text= nombre_cine(i), bg= "gray", font= "Helvetica 40 bold", fg= "white", width= 17, height=1,
                                 command= lambda i=i: accion_ir_principal(info_ticket, pantalla_bienvenida, i))
        boton.grid(column= columna, row = fila)
        columna += 1
        
        if columna > 1:
            columna = 0
            fila += 1

    pantalla_bienvenida.mainloop()


def calculadora_cantsalas_cine(info_ticket: dict)->None:
    """
    PRE: se encarga de crear una lista de n salas, n es la cantidad de peliculas que tiene el establecimiento, que a su vez es la cantidad
    de salas, para cada sucursal cada sala va a tener el valor de cantidad de asientos que tiene la sucursal en la API. 
    Cada lista se guardara un un diccionario con clave igual al nombre de la sucursal, y este diccionario estara en el
    diccionario principal(info_ticket) con clave 'ASIENTOS_DISPONIBLES'
    """

    cant_cines: int = 7
    lista_asientos_salas: tuple = []

    for i in range(1, cant_cines+1):
        info_ticket['ID_CINE'] = i
        nom_cine = nombre_cine(i)
        peliculas_proyec: list = peliculas_proyectadas(info_ticket)[0]['has_movies']
        cant_salas: int = len(peliculas_proyec)
        info_ticket['ASIENTOS_DISPONIBLES'][f'{nom_cine}']: list = []
        for j in range(0, cant_salas):
            lista_asientos_salas.append(asientos_disponibles(i))
            info_ticket['ASIENTOS_DISPONIBLES'][f'{nom_cine}'].append(asientos_disponibles(i))

    #print(info_ticket['ASIENTOS_DISPONIBLES'])


#MAIN#

def main() -> None:
   
    info_ticket: dict = {
        'LOCALIZACION'         : "",
        'ID_CINE'              : 0,
        'CANT_SALAS'           : 0,
        'NUM_SALA_PELICULA'    : 0,
        'PELICULAS_PROYECTADAS': [],
        'ASIENTOS_DISPONIBLES' : {},
        'CANT_ENTRADAS'        : 0,
        'ID_PELICULA'          : "",
        'VALOR_CADA_ENTRADA'   : PRECIO_ENTRADAS,
        'VALOR_TOTAL_ENTRADAS' : 0,
        'SNACKS_COMPRADOS'     : [],
        'VALOR_TOTAL_SNACKS'   : 0,
        'PRECIO_TOTAL'         : 0
    }

    calculadora_cantsalas_cine(info_ticket)
    bienvenida(info_ticket)

main()