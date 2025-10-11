from tkinter import *
import menu_principal

def mostrar_pantalla_titulo(ventana):
    for w in ventana.winfo_children():
        w.destroy()

    frame = Frame(ventana, bg="black")
    frame.place(relx=0, rely=0, relwidth=1, relheight=1)  # Ocupa toda la pantalla

    Label(frame, text="ROMPECABEZAS ANIMADO",
          font=("Arial", 48, "bold"), fg="white", bg="black").pack(pady=120)

    Button(frame, text="JUGAR", font=("Arial", 26), width=12,
           command=lambda: menu_principal.mostrar_menu_principal(ventana)).pack(pady=40)

    Button(frame, text="SALIR", font=("Arial", 26), width=12,
           command=ventana.destroy).pack(pady=10)


