# main.py
import tkinter as tk
import pantalla_titulo

# Variable global para color de fondo
BG_COLOR = "#383838"

# --- Inicialización de la ventana ---
ventana = tk.Tk()
ventana.attributes('-fullscreen', True)
ventana.configure(bg="#383838")
ventana.title("Rompecabezas Animado")

# Mostrar pantalla de título
pantalla_titulo.mostrar_pantalla_titulo(ventana)

ventana.mainloop()
