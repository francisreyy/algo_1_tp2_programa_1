import tkinter
import json
import cv2
from datetime import datetime
root = tkinter.Tk()


def leer_datos_compra(compra) -> dict:
    with open ("datos_compra", "r") as datos:
        compra = json.load(datos)
    return compra

def imprimir_qr(id_ingresado, total) -> None:
    ahora = datetime.now()
    horario_actual = ahora.strftime("%Y-%m-%d_%H:%M:%S")
    partes = id_ingresado.split("/")
    cant_entradas = partes[1]
    nombre_peli = partes[2]
    cadena = horario_actual + "," + id_ingresado + "," + nombre_peli + "," + cant_entradas + "," + str(total) + "\n"
    with open("registro.txt", "a") as archivo:
        archivo.write(cadena)

def mostrar_compra(compra, pantalla_activa, id_ingresado) -> None:
    pantalla_activa.grid_forget()
    nueva_pantalla=tkinter.Frame(root)
    nueva_pantalla.grid()
    total = 0
    count_row= 0 
    for i in compra:
        if i == id_ingresado:
            for x in compra[i]:
                total += compra[i][x]['valor total']
                text = tkinter.Label(nueva_pantalla, text=f"{x}")
                text.grid(row=count_row, column=0)
                cantidad = tkinter.Label(nueva_pantalla, text=f"x{compra[i][x]['cantidad']}")
                cantidad.grid(row=count_row, column=1)
                valor = tkinter.Label(nueva_pantalla, text=f" ${compra[i][x]['valor total']}")
                valor.grid(row=count_row, column=2)
                count_row += 1
        total_pagado = tkinter.Label(nueva_pantalla, text=f"TOTAL PAGADO: {total}")
        total_pagado.grid(row=count_row)
        imprimir_qr(id_ingresado, total)
    boton_atras = tkinter.Button(nueva_pantalla, text="VOLVER", command=lambda: volver_menu(nueva_pantalla))
    boton_atras.grid()

def volver_menu(pantalla_actual) -> None:
    pantalla_actual.destroy()
    menu()

def obtener_id(input_id, pantalla_id, texto) -> None:
    id_ingresado = input_id.get()
    compra = {}
    compra=leer_datos_compra(compra)
    hay_id = False
    for i in compra:
        if id_ingresado == i:
            hay_id = True
            mostrar_compra(compra, pantalla_id, id_ingresado)
    if hay_id == False:
        if texto.winfo_ismapped():
            pass
            #texto.destroy()
        else:
            texto.grid()


def ingrese_id (menu) -> None:
    menu.grid_forget()
    pantalla_id= tkinter.Frame(root)
    pantalla_id.grid()
    input_id = tkinter.Entry(pantalla_id, width=20)
    input_id.grid(row= 0)
    texto = tkinter.Label(pantalla_id, text="El id ingresado no existe")
    boton_ingresar = tkinter.Button(pantalla_id, text="INGRESAR", command= lambda:obtener_id(input_id, pantalla_id, texto))
    boton_ingresar.grid(row= 1)

def compra_qr (id_ingresado, pantalla_qr) -> None:
    compra_qr = {}
    compra_qr = leer_datos_compra(compra_qr)
    print(compra_qr)
    hay_id = False
    for i in compra_qr:
        if id_ingresado == i:
            print(compra_qr[i])
            hay_id = True
            mostrar_compra(compra_qr, pantalla_qr, id_ingresado)
    if hay_id == False:
        menu()

def leer_qr(menu) -> None:
    menu.grid_forget()
    pantalla_qr =tkinter.Frame(root)
    pantalla_qr.grid()
    capturar = cv2.VideoCapture(0)
    while capturar.isOpened():
        success, img = capturar.read()
        if cv2.waitKey(1)==ord("s"):
            break
        qr_detector = cv2.QRCodeDetector()
        data, box, rectified_image = qr_detector.detectAndDecode(img)
        if len(data)>0:
            print(data)
            compra_qr(data, pantalla_qr)
            cv2.destroyAllWindows()
            #capturar.release()
            break 
            #cv2.imshow("webCam", rectified_image)
        else:
            cv2.imshow("webCam", img)
    capturar.release()
    #capturar.destroyAllWindows()
    #capturar.

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