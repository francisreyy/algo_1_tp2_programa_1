import tkinter
import json
import cv2
from datetime import datetime
import os
root = tkinter.Tk()


def leer_datos_compra(compra: dict) -> dict:
    """
    PRE: recibe un diccionario vacío
    POST: devuelve, en ese diccionario, la información recibida en el json del programa 1
    """
    with open ("datos_compra", "r") as datos:
        compra = json.load(datos)
    return compra

def informacion_qr_en_txt(id_ingresado: str, total: int) -> None:
    """
    POST: escribe una cadena en un archivo de texto (registro.txt). Esta cadena contiene la informacion mas relevante
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

def mostrar_compra(compra: dict, pantalla_activa, id_ingresado: str) -> None:
    """
    POST: devuelve, en pantalla, los datos de la compra del programa 1
    """
    nueva_pantalla = tkinter.Frame(root)
    nueva_pantalla.grid()
    total: int = 0
    count_row: int = 0 
    for i in compra:
        if i == id_ingresado:
            for x in compra[i]:
                total += compra[i][x]['valor total']
                text = tkinter.Label(nueva_pantalla, text=f"{x}")
                text.grid(row=count_row, column=0)
                cantidad = tkinter.Label(nueva_pantalla, font= "Helvetica 10 bold", text=f"x{compra[i][x]['cantidad']}")
                cantidad.grid(row=count_row, column=1)
                valor = tkinter.Label(nueva_pantalla, font= "Helvetica 10 bold", text=f" ${compra[i][x]['valor total']}")
                valor.grid(row=count_row, column=2)
                count_row += 1
            total_pagado = tkinter.Label(nueva_pantalla, font= "Helvetica 10 bold", text=f"TOTAL PAGADO: {total}")
            total_pagado.grid(row=count_row)
            informacion_qr_en_txt(id_ingresado, total)
    boton_atras = tkinter.Button(nueva_pantalla, text="VOLVER", command=lambda: volver_menu(nueva_pantalla))
    boton_atras.grid()

def volver_menu(pantalla_actual) -> None:
    pantalla_actual.destroy()
    menu()

def obtener_id(input_id, pantalla_id, texto) -> None:
    """
    POST: si el id existe en el json, mustra los datos de la compra, y si no es así, salta un error. Aún así el usuario
    puede seguir intentando ingresar el id denuevo. El mensaje no desaparecerá hasta que lo haga.
    """
    id_ingresado: str = input_id.get()
    compra: dict = {}
    compra = leer_datos_compra(compra)
    hay_id: bool = False
    for i in compra:
        if id_ingresado == i:
            validacion: bool = varificar_id_qr_no_sean_repetidos(pantalla_id, id_ingresado)
            hay_id = True
            if validacion == True:
                mostrar_compra(compra, pantalla_id, id_ingresado)
    if hay_id == False:
        if texto.winfo_ismapped():
            pass
        else:
            texto.grid()

def varificar_id_qr_no_sean_repetidos(pantalla, id_ingresado: str) -> bool:
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
                pantalla_err = tkinter.Tk()
                pantalla_err.grid()
                texto_err = tkinter.Label(pantalla_err, text="este id ya ha sido ingresado")
                texto_err.grid(row=0,column=0)
                volver_inicio = tkinter.Button(pantalla_err, text= "volver al inicio", command=lambda:volver_menu(pantalla_err))
                volver_inicio.grid(row=1, column=0)
                validacion = False
    return validacion





def ingrese_id (menu) -> None:
    """
    PRE: Se llama a esta función solo si el usuario desea acceder a su compra a través de un id.
    POST: Muestra por pantalla la opción de ingresar un string y un botón de "ingresar"
    """
    menu.grid_forget()
    pantalla_id= tkinter.Frame(root)
    pantalla_id.grid()
    input_id = tkinter.Entry(pantalla_id, width=20)
    input_id.grid(row= 0)
    texto = tkinter.Label(pantalla_id, text="El id ingresado no existe")
    boton_ingresar = tkinter.Button(pantalla_id, text="INGRESAR", command= lambda:obtener_id(input_id, pantalla_id, texto))
    boton_ingresar.grid(row= 1)

def compra_qr (id_ingresado, pantalla_qr) -> None:
    compra_qr: dict = {}
    compra_qr = leer_datos_compra(compra_qr)
    print(compra_qr)
    hay_id = False
    for i in compra_qr:
        if id_ingresado == i:
            print(compra_qr[i])
            hay_id = True
            validacion: bool = varificar_id_qr_no_sean_repetidos(pantalla_qr, id_ingresado)
            if validacion == True:
                mostrar_compra(compra_qr, pantalla_qr, id_ingresado)
    if hay_id == False:
        menu()

def leer_qr(menu) -> None:
    """
    PRE: Se llama a esta función solo si el usuario desea acceder a su compra a través de un qr.
    POST: lee el qr con la webcam de la computadora, solo si un qr valido fue detectado, llamará a la función
    "comprar_qr"
    """
    menu.grid_forget()
    pantalla_qr =tkinter.Frame(root)
    pantalla_qr.grid()
    capturar = cv2.VideoCapture(0)
    while capturar.isOpened():
        success, img = capturar.read()
        if cv2.waitKey(1) == ord("s"):
            break
        qr_detector = cv2.QRCodeDetector()
        data, box, rectified_image = qr_detector.detectAndDecode(img)
        if len(data)>0:
            print(data)
            compra_qr(data, pantalla_qr)
            cv2.destroyAllWindows()
            break 
        else:
            cv2.imshow("SCANEA EL QR DE SU COMPRA", img)
    capturar.release()

def menu() -> None:
    menu = tkinter.Frame(root)
    menu.grid()
    text = tkinter.Label(menu, text="¿Como desea ingresar?")
    boton_qr_id = tkinter.Button(menu, text="ID", command= lambda: ingrese_id(menu))
    boton_qr = tkinter.Button(menu, text="WebCam", command=lambda: leer_qr(menu))
    text.grid()
    boton_qr_id.grid()
    boton_qr.grid()

def main() -> None:
    menu()
    root.mainloop()
main()