from tkinter import *
import Rompecabezas
import configuracion

def mostrar_menu_principal(ventana):
    for w in ventana.winfo_children():
        w.destroy()

    frame = Frame(ventana, bg="gray10")
    frame.place(relx=0.5, rely=0.5, anchor="center")

    # --- Menú superior: selección de tamaño ---
    Label(frame, text="Tamaño del Grid:", font=("Arial", 20), fg="white", bg="gray10").pack(pady=10)
    grid_var = StringVar(value="6x6")
    opciones = ["2x2", "4x4", "6x6", "8x8", "10x10"]
    OptionMenu(frame, grid_var, *opciones).pack(pady=10)

    # --- Seleccion de patrones ---
    canvas = Canvas(frame, width=800, height=200, bg="gray15", highlightthickness=0)
    canvas.pack(pady=60)
    patrones = [f"Patron{i}.gif" for i in range(1, 6)]
    Label(frame, text="Selecciona un patrón", fg="white", bg="gray10", font=("Arial", 18)).pack()

    indice = IntVar(value=0)
    img_refs = []

    def mostrar_patron():
        canvas.delete("all")
        ruta = Rompecabezas.obtener_patron(indice.get() + 1)
        img = PhotoImage(file=ruta)
        img_refs.clear()
        img_refs.append(img)
        canvas.create_image(400, 100, image=img)

    def anterior(): indice.set((indice.get() - 1) % len(patrones)); mostrar_patron()
    def siguiente(): indice.set((indice.get() + 1) % len(patrones)); mostrar_patron()

    Button(frame, text="<", font=("Arial", 20), command=anterior).place(relx=0.25, rely=0.5, anchor="center")
    Button(frame, text=">", font=("Arial", 20), command=siguiente).place(relx=0.75, rely=0.5, anchor="center")

    mostrar_patron()

    # --- Botones inferiores ---
    Button(frame, text="Configuración", font=("Arial", 20),
           command=lambda: configuracion.mostrar_configuracion(ventana)).pack(pady=40)

    Button(frame, text="Jugar", font=("Arial", 24),
           command=lambda: iniciar_juego(ventana, grid_var, indice)).pack(pady=20)

def iniciar_juego(ventana, grid_var, indice):
    tamanio = int(grid_var.get().split("x")[0])
    Rompecabezas.GRID = tamanio
    Rompecabezas.mezclar_piezas()
    patron = Rompecabezas.obtener_patron(indice.get() + 1)
    Rompecabezas.cargar_frames(patron)
    Rompecabezas.crear_grid(ventana)
    Rompecabezas.animar(ventana)
