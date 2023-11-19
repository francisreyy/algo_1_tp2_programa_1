import json
import tkinter
import json
import pagina_c
root = tkinter.Tk()

PANTALLA_D = tkinter.Frame(root, width=500, height=620)
PANTALLA_D.grid()

def main() -> None:
    diccionario ={}
    with open("data_json", "r") as archivo:
        l = archivo.read()
        diccionario = json.loads(l)
    count_row = 0
    contador_total_valor = 0
    for i in diccionario:
        text = tkinter.Label(PANTALLA_D, text=f"{i}")
        text.grid(row= count_row, column=0)
        cantidad_dict = diccionario[i]["cantidad"]
        cantidad = tkinter.Label(PANTALLA_D, text=f"x{cantidad_dict}")
        cantidad.grid(row= count_row, column=1)
        valor_total_dict = diccionario[i]["valor total"]
        valor_total = tkinter.Label(PANTALLA_D, text=f" ${valor_total_dict}")
        valor_total.grid(row= count_row, column=2)
        contador_total_valor += diccionario[i]["valor total"]
        count_row += 1
    total = tkinter.Label(PANTALLA_D, text=f"TOTAL: ${contador_total_valor}")
    total.grid(row= count_row, column=0)
    root.mainloop()
main()

