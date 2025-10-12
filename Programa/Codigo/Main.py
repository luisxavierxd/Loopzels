# main.py
import tkinter as tk
import pantalla_titulo

# --- Inicialización de la ventana ---
ventana = tk.Tk()
ventana.attributes('-fullscreen', True)
ventana.configure(bg="#383838")
ventana.title("Rompecabezas Animado")

# Mostrar pantalla de título
pantalla_titulo.mostrar_pantalla_titulo(ventana)

ventana.mainloop()
