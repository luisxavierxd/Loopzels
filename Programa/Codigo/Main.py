from tkinter import *
from PIL import Image, ImageTk, ImageEnhance
import random, os
import Rompecabezas
import UI


# --- Inicialización ---
ventana = Tk() #Crea la ventana 
ventana.title("Rompecabezas Animado")
ventana.state('zoomed') #Acomoda todo segun tamaño de pantalla
ventana.attributes('-fullscreen', True) #Pantalla completa

patron_escogido = Rompecabezas.obtener_patron(1)

Rompecabezas.mezclar_piezas()
Rompecabezas.cargar_frames(patron_escogido)
Rompecabezas.crear_grid(ventana)
Rompecabezas.animar(ventana)

ventana.mainloop()