import tkinter
import json
import cv2
from datetime import datetime
import os

### VERSION 1.0 ###

def leer_datos_compra(compras_qr: dict) -> dict:
    """
    PRE: recibe un diccionario vacío.
    POST: devuelve, en ese diccionario, la información recibida en el json del programa 1.
    """
    with open ("datos_compra.json", "r") as datos:
        compras_qr = json.load(datos)

    return compras_qr


def informacion_qr_en_txt(id_ingresado: str, total: int) -> None:
    """
    PRE: escribe una cadena en un archivo de texto (registro.txt). Esta cadena contiene la informacion mas relevante
    de la compra, todo separado por comas.
    """
    ahora = datetime.now()
    horario_actual: str = ahora.strftime("%Y-%m-%d_%H:%M:%S")
    partes: list = id_ingresado.split("/")
    cant_entradas: str = partes[1]
    nombre_peli: str = partes[2]
    cadena = horario_actual + "," + id_ingresado + "," + nombre_peli + "," + cant_entradas + "," + str(total) + "\n"
    with open("registro.txt", "a") as archivo:
        archivo.write(cadena)


def mostrar_compra(root, compra: dict, id_ingresado: str) -> None:
    """
    PRE: devuelve en pantalla los datos de la compra del programa 1.
    """
    nueva_pantalla = tkinter.Frame(root)
    nueva_pantalla.grid()

    total: int = 0
    count_row: int = 0 

    for i in compra:
        if i == id_ingresado:
            for x in compra[i]:
                total += compra[i][x]['valor total']
                text = tkinter.Label(nueva_pantalla, text=f"{x}", font= "Helvetica 10 bold")
                text.grid(row=count_row, column=0)
                cantidad = tkinter.Label(nueva_pantalla, font= "Helvetica 10 bold", text=f"x{compra[i][x]['cantidad']}")
                cantidad.grid(row=count_row, column=1)
                valor = tkinter.Label(nueva_pantalla, font= "Helvetica 10 bold", text=f" ${compra[i][x]['valor total']}")
                valor.grid(row=count_row, column=2)
                count_row += 1
            total_pagado = tkinter.Label(nueva_pantalla, font= "Helvetica 10 bold", text=f"TOTAL PAGADO: {total}")
            total_pagado.grid(row=count_row)
            informacion_qr_en_txt(id_ingresado, total)

    boton_atras = tkinter.Button(nueva_pantalla, text="VOLVER", font= "Helvetica 20 bold",command=lambda: volver_menu(nueva_pantalla))
    boton_atras.grid()


def volver_menu(pantalla_actual) -> None:
    """
    PRE: Procedimiento vuelve al menú, necesita la pantalla actual para ser destruida
    """
    pantalla_actual.destroy()
    menu()


def obtener_id(root, input_id, pantalla_id, texto) -> None:
    """
    PRE: si el id existe en el json, mustra los datos de la compra, y si no es así, salta un error, aún así el usuario
    puede seguir intentando ingresar el id denuevo. El mensaje no desaparecerá hasta que lo haga.
    """
    id_ingresado: str = input_id.get()
    compra: dict = {}
    compra = leer_datos_compra(compra)
    hay_id: bool = False
    for i in compra:
        if id_ingresado == i:
            validacion: bool = verificar_id_qr_no_sean_repetidos(root, pantalla_id, id_ingresado)
            hay_id = True
            if validacion == True:
                mostrar_compra(root, compra, id_ingresado)
    if hay_id == False:
        if texto.winfo_ismapped():
            pass
        else:
            texto.grid()


def verificar_id_qr_no_sean_repetidos(root, pantalla, id_ingresado: str) -> bool:
    """
    PRE: Función que recibe la pantalla actual para ser destruida y el id ingresado como string
    para verificar si las ids ingresadas se repiten o no, modificando registro.txt o no 
    dependiendo el caso
    POST: Devuelve un booleano indicando si la id es repetida o no
    """
    validacion: bool = True

    pantalla.destroy()

    datos_registrados: list = []
    archivo_registro="registro.txt"

    if not os.path.isfile(archivo_registro):
        with open(archivo_registro, "w") as archivo:
            pass

    with open(archivo_registro, "r") as archivo:
        datos_registrados= archivo.readlines()
    ids_qrs_registrados: list = []
    print(datos_registrados)

    if len(datos_registrados) != 0:
        for dato in datos_registrados:
            dato = dato.strip()
            datos_completos: list = dato.split(',')
            ids_qrs_registrados.append(datos_completos[1])

        for id_qr in ids_qrs_registrados:
            if id_qr == id_ingresado:
                pantalla_err = tkinter.Frame(root)
                pantalla_err.grid()
                texto_err = tkinter.Label(pantalla_err, text="este id ya ha sido ingresado", 
                                        font= "Helvetica 10 bold")
                texto_err.grid(row=0,column=0)
                volver_inicio = tkinter.Button(pantalla_err, text= "volver al inicio",
                                            font= "Helvetica 20 bold", 
                                            command=lambda:volver_menu(pantalla_err))
                volver_inicio.grid(row=1, column=0)
                validacion = False

    return validacion


def ingrese_id(root, menu) -> None:
    """
    PRE: Se llama a esta función solo si el usuario desea acceder a su compra a través de un id, ademas
    muestra por pantalla la opción de ingresar un string y un botón de "ingresar".
    """
    menu.grid_forget()
    pantalla_id= tkinter.Frame(root)
    pantalla_id.grid()
    input_id = tkinter.Entry(pantalla_id, width=80)
    input_id.grid(row= 0)
    texto = tkinter.Label(pantalla_id, text="El id ingresado no existe", font= "Helvetica 10 bold")
    boton_ingresar = tkinter.Button(pantalla_id, text="INGRESAR",
                                    font= "Helvetica 20 bold", 
                                    command= lambda:obtener_id(root, input_id, pantalla_id, texto))
    boton_ingresar.grid(row= 1)
    volver_inicio = tkinter.Button(pantalla_id, text="menu",
                                font= "Helvetica 20 bold",
                                command= lambda: volver_menu(pantalla_id))
    volver_inicio.grid(row=2)


def compra_qr(root, id_ingresado: str, pantalla_qr) -> None:
    """
    PRE: Procedimiento que recibe el la id ingresada como string y el root y su frame pantalla_qr
    Muestra si el id ingresado corresponde a una id de una compra o no
    """
    compras_qr: dict = {}
    compras_qr = leer_datos_compra(compras_qr)
    print(compras_qr)

    hay_id: bool = False

    for ids_compras in compras_qr:
        if id_ingresado == ids_compras:
            print(compras_qr[ids_compras])
            hay_id = True
            validacion: bool = verificar_id_qr_no_sean_repetidos(root, pantalla_qr, id_ingresado)
            if validacion == True:
                mostrar_compra(compras_qr, id_ingresado)

    if hay_id == False:
        pantalla_qr.destroy()
        pantalla_error_qr_inval = tkinter.Frame(root)
        mensaje_err = tkinter.Label(pantalla_error_qr_inval, 
                                    text= "El qr ingresado no está registrado", 
                                    font= "Helvetica 10 bold")
        mensaje_err.grid(row=0)
        volver_inicio = tkinter.Button(pantalla_error_qr_inval, 
                                        text="menu",
                                        font= "Helvetica 20 bold", 
                                        command=lambda:volver_menu(pantalla_error_qr_inval))
        volver_inicio.grid(row=1)
        pantalla_error_qr_inval.grid()


def leer_qr(root, menu) -> None:
    """
    PRE: Se llama a esta función solo si el usuario desea acceder a su compra a través de un qr,
    lee el qr con la webcam de la computadora, solo si un qr valido fue detectado, llamará a la función
    "comprar_qr"
    """
    menu.grid_forget()
    pantalla_qr =tkinter.Frame(root)
    pantalla_qr.grid()
    capturar = cv2.VideoCapture(0)

    while capturar.isOpened():
        success, img = capturar.read()
        if cv2.waitKey(1) == ord("s"):
            volver_menu(pantalla_qr)
            cv2.destroyAllWindows()
            break
        qr_detector = cv2.QRCodeDetector()
        data, box, rectified_image = qr_detector.detectAndDecode(img)
        if len(data)>0:
            print(data)
            compra_qr(root, data, pantalla_qr)
            cv2.destroyAllWindows()
            break 
        else:
            cv2.putText(img, "presione la tecla 's' para cerrar ", 
                        (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, 
                        (255, 255, 255), 2, cv2.LINE_AA)
            cv2.imshow("SCANEA EL QR DE SU COMPRA", img)

    capturar.release()


def menu() -> None:
    """
    PRE: Procedimiento que muestra el menú del programa con los botones para elegir
    si ingresar el id o leerlo con la cámara
    """
    root = tkinter.Tk()
    root.title("INGRESE COMPRA")

    menu = tkinter.Frame(root)
    menu.grid()

    text = tkinter.Label(menu, text="¿Como desea ingresar?", font= "Helvetica 20 bold")
    boton_qr_id = tkinter.Button(menu, text="ID", font= "Helvetica 10 bold", command= lambda: ingrese_id(root, menu))
    boton_qr = tkinter.Button(menu, text="WebCam", font= "Helvetica 10 bold", command=lambda: leer_qr(root, menu))
    text.grid()
    boton_qr_id.grid()
    boton_qr.grid()

    root.mainloop()


def main() -> None:

    menu()

main()
