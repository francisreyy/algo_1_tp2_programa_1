import base64
import tkinter
from PIL import Image
from io import BytesIO
import os

sinopsis: str = """Sadie Harper, una estudiante del colegio secundario y su hermana
pequeña, Sawyer, están conmocionadas por la reciente muerte de su madre y no
reciben mucho apoyo de su padre, Will, un terapeuta que está lidiando con su propio
dolor. Cuando un paciente desesperado se presenta inesperadamente en su casa en
busca de ayuda, deja tras de sí una aterradora entidad sobrenatural que se
aprovecha de las familias y se alimenta del sufrimiento de sus víctimas."""
actores: str = "Chris Messina, David Dastmalchian, Sophie Thatcher"
director: str = "Rob Savage"
duracion: str = "98min"
genero: str = "Terror"
portada: str = """iVBORw0KGgoAAAANSUhEUgAAAA4AAAAQCAYAAAAmlE46AAAAAXNSR0IArs4c
6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsEAAA7BAbiRa+0AAAASdEVYdFNvZnR3YXJlAEdyZWVuc2h
vdF5VCAUAAAEKSURBVDhPnZJLjkVAGIWP7rGRGWNbYAXm7MCYFRCDTsQOMLQF5naAsR2wjds5f5T2yu3kfk
lFVanzvzXbtl94g6Zp2+7M1/Y9Eccx5nlG3/eIomi7PXMT8qHjOPA8D2EYwnVdFEWx/f3jJvR9H2VZYlkWW
UmSiKErj6EesSxL1pVvwzB+tr2g6zqCIMC6rnJO0xRt22IcRzkrblU1TVPCpZh0XYe6rmV/5ON2PHpkTiwI
w1VFUqErdqEKkYuPmBPv6JFGhmFAVVW7gV3YNA2mabrlQ+Exb/aXSDvyPJfDUxEIvfAfvXKqiAgZSpZlcvE
OVlgNgwgZyjX5J1gkNQz/Ts4RGlfCD/sI/AKSVG+qpsfzygAAAABJRU5ErkJggg=="""
imagen = base64.b64decode(portada)
imagen_final = Image.open(BytesIO(imagen))
jpg= imagen_final.convert("RGB")
jpg.save('portada.png')

pantalla_2 = tkinter.Tk()
TOP0_MID = tkinter.Label(pantalla_2, text="SALA 7",
                          font= "Helvetica 20 bold")#numero de sala

TOP0_DER = tkinter.Button(pantalla_2, text="VOLVER ATRAS",
                           font= "Helvetica 15 bold")#boton volver atras

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
                         font= "Helvetica 15 bold")#boton RESERVAR


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