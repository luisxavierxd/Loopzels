# main.py
import tkinter as tk
import pantalla_titulo
import audio

# --- Inicialización de la ventana ---
ventana = tk.Tk()
ventana.attributes('-fullscreen', True)
ventana.title("Loopzels")

# Inicializar audio de forma segura
audio.inicializar_audio()

# Mostrar pantalla de título
pantalla_titulo.mostrar_pantalla_titulo(ventana)

while True:
    ventana.mainloop()
