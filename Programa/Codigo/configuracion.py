from tkinter import *
from tkinter import colorchooser

color_actual = "#FFFFFF"

def mostrar_configuracion(ventana):
    overlay = Toplevel(ventana)
    overlay.attributes("-fullscreen", True)
    overlay.configure(bg="#000000")
    overlay.attributes("-alpha", 0.6)
    overlay.focus_set()

    panel = Frame(overlay, bg="gray20", bd=4, relief="ridge")
    panel.place(relx=0.5, rely=0.5, anchor="center")

    Label(panel, text="Configuración", font=("Arial", 26, "bold"), fg="white", bg="gray20").pack(pady=15)

    # --- Volumen ---
    vol_frame = Frame(panel, bg="gray20")
    vol_frame.pack(pady=10)
    Label(vol_frame, text="Volumen:", font=("Arial", 18), fg="white", bg="gray20").pack(side=LEFT, padx=10)

    volumen = DoubleVar(value=50)
    Scale(vol_frame, from_=0, to=100, orient=HORIZONTAL, variable=volumen, length=200).pack(side=LEFT)

    Button(vol_frame, text="🔇", font=("Arial", 16), command=lambda: volumen.set(0)).pack(side=LEFT, padx=10)

    # --- Color ---
    def elegir_color():
        global color_actual
        color = colorchooser.askcolor(title="Elegir color")[1]
        if color:
            color_actual = color

    Button(panel, text="Cambiar color de patrón", font=("Arial", 18), command=elegir_color).pack(pady=20)

    Button(panel, text="Cerrar", font=("Arial", 18), command=overlay.destroy).pack(pady=10)
