import tkinter
root = tkinter.Tk()

NOMBRE_DEL_CINE:str = "cine"
SUCURSAL: str = "abasto"
PELICULA_SELECCIONADA: str = "marvel"
POSTER_PELICULA: str = ""
ASIENTOS_LIBRES: int = 0
SNACKS: dict = {'doritos': '2500.00', 
                'popcorn_xl': '3000.00', 
                'popcorn_xxl': '4300.00', 
                'papas_fritas': '1800.00',
                'coca_cola_xl': '1500.00',
                'coca_cola_xxl': '2350.00',
                'chocolate 250g': '1100.00'}

def add_cantidad_de_snacks(comprado, contador_row, valores_nuevos, add_boton) -> None:
    valor_total_snacks: int = 0
    print(comprado)
    for i in SNACKS:
        for j in comprado:
            if i == j:
                if not comprado[i] == 0:
                    valor_unitario = float(SNACKS[i])
                    valor_total = valor_unitario * comprado[i]
                    valores_nuevos[j] = valor_total
    print(valores_nuevos)
    for i in valores_nuevos:
        valor_total_snacks += valores_nuevos[i]
    print(valor_total_snacks)
    mostrar_por_pantalla(valor_total_snacks,contador_row, valores_nuevos, comprado)
    valores_nuevos.clear()
    comprado.clear()
    crear_denuevo(comprado, contador_row)
    add_boton.config(state=tkinter.DISABLED)

def mostrar_por_pantalla(valor_total_snacks, count_rows, valores_nuevos, comprado)-> None:
    count_rows[0] += 1
    for i in valores_nuevos:
        snack_comprado = tkinter.Label(root, text=f"{i}")
        por = tkinter.Label(root, text=f" X{comprado[i]}")
        precio_snack_comprado = tkinter.Label(root, text=f"{valores_nuevos[i]}")
        snack_comprado.grid(row= count_rows[0], column= 0)
        por.grid(row= count_rows[0], column= 1)
        precio_snack_comprado.grid(row= count_rows[0], column= 2)
        count_rows[0] += 1
    total_precio = tkinter.Label(root, text=f"TOTAL: {valor_total_snacks}")
    total_precio.grid(row=count_rows[0])
    
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

def contadores(comprado, i, contador_row):
    texto = tkinter.Label(root, text=f"{i}")
    texto.grid(row= contador_row[0], column= 0)
    locals()['cant_seleccionada_{}'.format(i)] = [0]
    cat_seleccionada =  locals()['cant_seleccionada_{}'.format(i)]
    locals()['mas_boton_{}'.format(i)] = tkinter.Button(root, text="+", command= lambda: sumar(cat_seleccionada, i, cant, comprado))
    locals()['mas_boton_{}'.format(i)].grid(row= contador_row[0], column= 1)
    locals()['cant_{}'.format(i)] = tkinter.Label(root, text=f"{cat_seleccionada[0]}")
    locals()['cant_{}'.format(i)].grid(row= contador_row[0], column= 2)
    cant = locals()['cant_{}'.format(i)] 
    locals()['menos_boton_{}'.format(i)] = tkinter.Button(root, text="-", command= lambda: restar(cat_seleccionada, i, cant, comprado))
    locals()['menos_boton_{}'.format(i)].grid(row= contador_row[0], column= 3)
    return i

def crear_denuevo(comprado, contador_row)->None:
    contador_row[0] = 0
    for i in SNACKS:
        contadores(comprado, i, contador_row)
        contador_row[0] += 1
def main() -> None:
    root.title("Contadores App")
    comprado: dict = {}
    valores_nuevos_con_precios = {}
    contador_row = [0]
    crear_denuevo(comprado, contador_row)
    add_boton = tkinter.Button(root, text="add", command= lambda: add_cantidad_de_snacks(comprado, 
                                                                                        contador_row,
                                                                                        valores_nuevos_con_precios,
                                                                                        add_boton))
    add_boton.grid()
    root.mainloop()

main()