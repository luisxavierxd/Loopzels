from tkinter import *
import pantalla_titulo

ventana = Tk()
ventana.title("Rompecabezas Animado")
ventana.state('zoomed')
ventana.attributes('-fullscreen', True)

pantalla_titulo.mostrar_pantalla_titulo(ventana)
ventana.mainloop()
    