#algo 1 tp 2

PROGRAMA 1

......................................................................................

configurar editar notas en visual studio code minuto 10:36 https://youtu.be/VdGzPZ31ts8?si=9NMA9-yGUOGbgMda&t=636

qué son las apis? https://www.youtube.com/watch?v=u2Ms34GE14U

requests https://www.youtube.com/watch?v=TMxmkHdhfr8

https://www.youtube.com/watch?v=tb8gHvYlCFs

documentacion requests https://requests.readthedocs.io/en/latest/ guía rápida https://requests.readthedocs.io/en/latest/user/quickstart/#make-a-request

......................................................................................

import requests

url = "http://vps-3701198-x.dattaweb.com:4000"

token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.DGI_v9bwNm_kSrC-CQSb3dBFzxOlrtBDHcEGXvCFqgU"

headers = {"Authorization": "Bearer " + token}

SNACKS = "/snacks/"

r = requests.get(url + SNACKS, headers=headers)

print(r.json())

..........................................................................................

tutorial tkinter https://www.youtube.com/watch?v=jqRHhWjKDD8

generar pdf con QR e ID https://docs.reportlab.com/reportlab/userguide/ch2_graphics/

..........................................................................................

generar qr https://pypi.org/project/qrcode/

ID = hora_actual / cantidad_entradas / nombre_pelicula / sucursal
..........................................................................................


PROGRAMA 2
..........................................................................................
usar la WebCam para leer QR 
https://www.youtube.com/watch?v=oXlwWbU8l2o&t=9766s
https://opencv.org/
..........................................................................................

