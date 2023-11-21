import tkinter
import archivo
from datetime import datetime
import qrcode
from reportlab.pdfgen import canvas
import json
root = tkinter.Tk()

#PAGINA D
PANTALLA_D = tkinter.Frame(root, width=500, height=620)

NOMBRE_DEL_CINE:str = "cine"
SUCURSAL: str = "abasto"
PELICULA_SELECCIONADA: str = "nombre"
VALOR_ASIENTOS: int = 1
POSTER_PELICULA: str = ""
ASIENTOS_LIBRES: int = 3
SNACKS_INFO = archivo.SNACKS
SNACKS_DICT: dict = archivo.imprimir_endpoint_json(SNACKS_INFO)

#
#PAGINA C GRID
#
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
#PANTALLA_C.grid()
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

def contadores(comprado, i, contador_row, snacks):
    texto = tkinter.Label(BOTTOM0_IZQ_BOT, text=f"{i}")
    precio = tkinter.Label(BOTTOM0_IZQ_BOT, text=f"{snacks[i]}$")
    texto.grid(row= contador_row[0], column= 1)
    precio.grid(row= contador_row[0], column= 2)
    locals()['cant_seleccionada_{}'.format(i)] = [0]
    cat_seleccionada =  locals()['cant_seleccionada_{}'.format(i)]
    locals()['mas_boton_{}'.format(i)] = tkinter.Button(BOTTOM0_IZQ_BOT, text="+", command= lambda: sumar(cat_seleccionada, i, cant, comprado))
    locals()['mas_boton_{}'.format(i)].grid(row= contador_row[0], column= 5)
    locals()['cant_{}'.format(i)] = tkinter.Label(BOTTOM0_IZQ_BOT, text=f"{cat_seleccionada[0]}")
    locals()['cant_{}'.format(i)].grid(row= contador_row[0], column= 4)
    cant = locals()['cant_{}'.format(i)] 
    locals()['menos_boton_{}'.format(i)] = tkinter.Button(BOTTOM0_IZQ_BOT, text="-", command= lambda: restar(cat_seleccionada, i, cant, comprado))
    locals()['menos_boton_{}'.format(i)].grid(row= contador_row[0], column= 3)

def crear_lista_snacks(comprado, contador_row)->None:
    contador_row[0] = 0
    for i in SNACKS_DICT:
        contadores(comprado, i, contador_row, SNACKS_DICT)
        contador_row[0] += 1
    contador_row.clear()

def confirmar_compra(valores_nuevos_con_precios, comprado, snacks, cantidad_asientos)-> None:
    for i in snacks:
        for j in comprado:
            if i == j:
                if comprado[j] != 0:
                    valores_nuevos_con_precios[j] = {"cantidad": comprado[j], "valor total": float(snacks[i]) * comprado[j]}
    valores_nuevos_con_precios[PELICULA_SELECCIONADA] = {"cantidad": cantidad_asientos[0], 
                                                        "valor total": VALOR_ASIENTOS * cantidad_asientos[0]}
    comprado.clear()
    cantidad_asientos.clear()
    PANTALLA_C.grid_forget()
    print(valores_nuevos_con_precios)
    pagina_d(valores_nuevos_con_precios)
    #valores_nuevos_con_precios.clear()
    
def restar_asientos(cantidad_asientos, contador_asientos, add_boton,  valores_nuevos_con_precios, comprado) -> None:
    cantidad_asientos[0] -= 1
    if cantidad_asientos[0] < 0:
        cantidad_asientos[0] = 0
    contador_asientos.config(text=f"{cantidad_asientos[0]}")
    if cantidad_asientos[0] > 0:
        add_boton.config(state= "active",command= lambda: confirmar_compra(valores_nuevos_con_precios, comprado, SNACKS_DICT, cantidad_asientos))
    else:
        add_boton.config(state= "disabled")

def sumar_asientos(cantidad_asientos, contador_asientos, add_boton, valores_nuevos_con_precios, comprado) -> None:
    cantidad_asientos[0] += 1
    if cantidad_asientos[0] > ASIENTOS_LIBRES:
        cantidad_asientos[0] = ASIENTOS_LIBRES
    contador_asientos.config(text=f"{cantidad_asientos[0]}")
    if cantidad_asientos[0] > 0:
        add_boton.config(state= "active",command= lambda: confirmar_compra(valores_nuevos_con_precios, comprado, SNACKS_DICT, cantidad_asientos))
    else:
        add_boton.config(state= "disabled")


def crear_lista_pelicula(cantidad_asientos, add_boton,  valores_nuevos_con_precios, comprado) -> None:

    titulo_pelucula = tkinter.Label(TOP1_DER, text=f"{PELICULA_SELECCIONADA}")
    valor_asientos_pelicula = tkinter.Label(TOP1_DER, text=f"{VALOR_ASIENTOS}$ c/u")
    asientos_disponibles = tkinter.Label(TOP1_DER, text=f"Asientos disponibles: {ASIENTOS_LIBRES}")
    texto =tkinter.Label(TOP2, text=f"ELIJA LA CANTIDAD DE ENTRADAS: ")
    if cantidad_asientos[0] > 0:
        add_boton.config(state= "active",command= lambda: confirmar_compra(valores_nuevos_con_precios, comprado, SNACKS_DICT, cantidad_asientos))
    else:
        add_boton.config(state= "disabled")

    boton_mas_pelicula = tkinter.Button(TOP2, text="+", command= lambda: sumar_asientos(cantidad_asientos, contador_asientos, add_boton,  valores_nuevos_con_precios, comprado))
    boton_menos_pelicula = tkinter.Button(TOP2, text="-", command= lambda: restar_asientos(cantidad_asientos, contador_asientos, add_boton,  valores_nuevos_con_precios, comprado))
    contador_asientos = tkinter.Label(TOP2, text=f"{cantidad_asientos[0]}")
    titulo_pelucula.grid(row= 0, column=0)
    valor_asientos_pelicula.grid(row= 1, column=0)
    asientos_disponibles.grid(row=2, column=0)
    texto.grid(row= 0, column=1)
    boton_menos_pelicula.grid(row= 1, column=0)
    contador_asientos.grid(row= 1, column=1)
    boton_mas_pelicula.grid(row=1, column=2)

def mostrar(snacks, toggle, comprado, contador_row_snacks, vm):
    if snacks.winfo_ismapped():
        snacks.grid_forget()
        toggle.config(text= "MOSTRAR SNACKS")
        comprado.clear()
        vm.clear()
        print(comprado)
    else:
        snacks.grid()
        toggle.config(text= "OCULTAR SNACKS")
        crear_lista_snacks(comprado, contador_row_snacks)


#
# PAGINA D 
#
def pagina_d (diccionario) -> None:
    PANTALLA_D.grid()
    dentro_pantalla = tkinter.Label(PANTALLA_D)
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
    boton_mostrar_qr = tkinter.Button(dentro_pantalla, text= "GENERAR QR", command= lambda: generar_qr(diccionario, boton_mostrar_qr))
    boton_mostrar_qr.grid(row= count_row, column=0)
    count_row += 1
    boton_atras = tkinter.Button(dentro_pantalla, text="VOLVER ATRÁS", command= lambda: llamar_pagina_c(diccionario, dentro_pantalla))
    boton_atras.grid(row= count_row)

def generar_qr(diccionario, boton_mostrar_qr) -> None:
    boton_mostrar_qr.config(state= "disabled")
    hora_actual = datetime.now().strftime("%d.%m.%y_%H:%M")
    id = f"{hora_actual}/{diccionario[PELICULA_SELECCIONADA]['cantidad']}/{PELICULA_SELECCIONADA}/{SUCURSAL}"
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
    with open ("datos_compra", "w") as datos_compra:
        json.dump(compra_total_qr, datos_compra, indent= 4)
    
    diccionario.clear()

def llamar_pagina_c (diccionario, dentro_pantalla) -> None:
    PANTALLA_D.grid_forget()
    dentro_pantalla.grid_forget()
    diccionario.clear()
    #PANTALLA_C.grid()
    pagina_c()

def pagina_c() -> None:
    PANTALLA_C.grid()
    BOTTOM0_IZQ_BOT.grid_forget()
    root.title("3er pagina")
    comprado: dict = {}
    #comprado.clear()
    valores_nuevos_con_precios: dict = {}
    #valores_nuevos_con_precios.clear()
    volver_buton = tkinter.Button(TOP0, text="VOLVER")
    volver_buton.place(relx=0.5, rely=0.3, anchor="center")
    contador_row_snacks: list = [0]
    #contador_row_snacks.clear()
    cantidad_asientos: list = [0]
    #cantidad_asientos.clear()
    toggle = tkinter.Button(BOTTOM0_IZQ_TOP, text= "MOSTRAR SNACKS", command= lambda: mostrar(BOTTOM0_IZQ_BOT, toggle, comprado, contador_row_snacks, valores_nuevos_con_precios))
    add_boton = tkinter.Button(BOTTOM0_DER, text="FINALIZAR")
    crear_lista_pelicula(cantidad_asientos, add_boton, valores_nuevos_con_precios, comprado)
    toggle.grid(row= 0, column=0)
    add_boton.place(relx=0.8, rely=0.8, anchor="center")

def main() -> None:
    #PANTALLA_C.grid()
    pagina_c()
    root.mainloop()
main()