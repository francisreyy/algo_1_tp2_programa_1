import tkinter
import archivo
import requests
root = tkinter.Tk()

NOMBRE_DEL_CINE:str = "cine"
SUCURSAL: str = "abasto"
PELICULA_SELECCIONADA: str = "nombre de la pelicula"
VALOR_ASIENTOS: int = 1
POSTER_PELICULA: str = ""
ASIENTOS_LIBRES: int = 3
SNACKS_INFO = archivo.SNACKS
SNACKS_DICT: dict = archivo.imprimir_endpoint_json(SNACKS_INFO)


TOP0 = tkinter.Frame(root, width=500, height=100)
TOP1 = tkinter.Frame(root, width=500, height=150)
TOP1_IZQ = tkinter.Frame(TOP1, width=200, height=150)
TOP1_DER = tkinter.Frame(TOP1, width=300, height=150)
TOP2 = tkinter.Frame(root, width=500, height=70)
BOTTOM0 = tkinter.Frame(root, width=500, height=200)
BOTTOM0_IZQ = tkinter.Frame(BOTTOM0 , width=200, height=300)
BOTTOM0_DER = tkinter.Frame(BOTTOM0, width=300, height=300)

TOP0.grid(row=0)
TOP1.grid(row=1)
TOP1_IZQ.grid(row= 0, column=0)
TOP1_DER.grid(row= 0, column=1)
TOP2.grid(row=2)
BOTTOM0.grid(row= 3)
BOTTOM0_IZQ.grid(row= 0 ,column=0)
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
    texto = tkinter.Label(BOTTOM0_IZQ, text=f"{i}")
    precio = tkinter.Label(BOTTOM0_IZQ, text=f"{snacks[i]}$")
    texto.grid(row= contador_row[0], column= 1)
    precio.grid(row= contador_row[0], column= 2)
    locals()['cant_seleccionada_{}'.format(i)] = [0]
    cat_seleccionada =  locals()['cant_seleccionada_{}'.format(i)]
    locals()['mas_boton_{}'.format(i)] = tkinter.Button(BOTTOM0_IZQ, text="+", command= lambda: sumar(cat_seleccionada, i, cant, comprado))
    locals()['mas_boton_{}'.format(i)].grid(row= contador_row[0], column= 5)
    locals()['cant_{}'.format(i)] = tkinter.Label(BOTTOM0_IZQ, text=f"{cat_seleccionada[0]}")
    locals()['cant_{}'.format(i)].grid(row= contador_row[0], column= 4)
    cant = locals()['cant_{}'.format(i)] 
    locals()['menos_boton_{}'.format(i)] = tkinter.Button(BOTTOM0_IZQ, text="-", command= lambda: restar(cat_seleccionada, i, cant, comprado))
    locals()['menos_boton_{}'.format(i)].grid(row= contador_row[0], column= 3)
    return i

def crear_lista_snacks(comprado, contador_row)->None:
    contador_row[0] = 0
    for i in SNACKS_DICT:
        contadores(comprado, i, contador_row, SNACKS_DICT)
        contador_row[0] += 1

def confirmar_compra(valores_nuevos_con_precios, comprado, snacks, cantidad_asientos)-> None:
    for i in snacks:
        for j in comprado:
            if i == j:
                valores_nuevos_con_precios[j] = {"cantidad": comprado[j], "valor total": snacks[i]}
    valores_nuevos_con_precios[f"asientos para {PELICULA_SELECCIONADA}"] = {"cantidad": cantidad_asientos[0], 
                                                        "valor total": VALOR_ASIENTOS * cantidad_asientos[0]}
    
    print(valores_nuevos_con_precios)

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

#def crear_lista_pelicula(cantidad_asientos, contador_row_peliculas) -> None:
def crear_lista_pelicula(cantidad_asientos, add_boton,  valores_nuevos_con_precios, comprado) -> None:

    titulo_pelucula = tkinter.Label(TOP1_DER, text=f"{PELICULA_SELECCIONADA}")
    valor_asientos_pelicula = tkinter.Label(TOP1_DER, text=f"{VALOR_ASIENTOS}$ c/u")
    asientos_disponibles = tkinter.Label(TOP1_DER, text=f"Asientos disponibles: {ASIENTOS_LIBRES}")
    texto =tkinter.Label(TOP2, text=f"ELIJA LA CANTIDAD DE ENTRADAS: ")
    #codigo repetido ->  hacer funcion
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
def main() -> None:
    root.title("3er pagina")
    #### GRID


    comprado: dict = {}
    valores_nuevos_con_precios = {}
    volver_buton = tkinter.Button(TOP0, text="VOLVER")
    volver_buton.place(relx=0.5, rely=0.3, anchor="center")
    contador_row_snacks = [0]
    cantidad_asientos = [0]
    #añadir_snacks = tkinter.Checkbutton(BOTTOM0_DER, onvalue= lambda: dejar_comprar_snacks(), offvalue= lambda: no_permitir_comprar_snacks())
    add_boton = tkinter.Button(BOTTOM0_DER, text="FINALIZAR")
    crear_lista_pelicula(cantidad_asientos, add_boton,  valores_nuevos_con_precios, comprado)
    crear_lista_snacks(comprado, contador_row_snacks)
    #recivo = {}
    # for i in valores_nuevos_con_precios:
    #     recivo[i] = valores_nuevos_con_precios[i]
    #print(POSTERS_DICT)
    add_boton.place(relx=0.8, rely=0.8, anchor="center")
    root.mainloop()
    
main()