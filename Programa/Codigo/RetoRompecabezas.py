from tkinter import *
from PIL import Image, ImageTk, ImageEnhance
import random, os, pygame

GRID = 3
RETARDO = 80
ARCHIVO = os.path.join(os.path.dirname(__file__), "patron.gif")

FACTOR_BRILLO = 0.9  # Modifica el brillo de la imagen
FACTOR_COLOR = 1 # Modifica el color de la imagen

POS_X = .5 # posición horizontal (0.0 izquierda, 0.5 centro, mas o menos 0.85 derecha)
POS_Y = 0.5 # posición vertical (0.0 arriba, 0.5 centro, , mas o menos 0.75 abajo)

# --- Variables globales ---
frames_general = []       # grid general
frames_brillante = []    # al seleccionar
frames_originales =[]   # referencia original
orden_correcto = []
orden_actual = []
botones = []
pieza_seleccionada = None
cuadros_totales = 0
frame_actual = []        # índice de frame actual para cada pieza

# --- Cargar frames del GIF y recortar ---
def cargar_frames(ruta):
    global frames_general, frames_brillante, frames_originales, cuadros_totales, frame_actual
    gif = Image.open(ruta)
    cuadros_totales = gif.n_frames
    ancho, alto = gif.size
    pw, ph = ancho // GRID, alto // GRID

    frames_general = [[] for _ in range(GRID**2)]
    frames_brillante = [[] for _ in range(GRID**2)]
    frames_originales = [[] for _ in range(GRID**2)]
    frame_actual = [0] * (GRID**2)

    for f in range(cuadros_totales):
        gif.seek(f)
        frame = gif.convert("L")
        for r in range(GRID):
            for c in range(GRID):
                idx = r*GRID + c
                recorte = frame.crop((c*pw, r*ph, (c+1)*pw, (r+1)*ph))

                # original
                img_tk = ImageTk.PhotoImage(recorte)
                frames_originales[idx].append(img_tk)

                # oscuro
                oscuro = ImageEnhance.Brightness(recorte).enhance(FACTOR_BRILLO)
                frames_general[idx].append(ImageTk.PhotoImage(oscuro))

                # brillante
                brillante = ImageEnhance.Brightness(recorte).enhance(1.3)
                frames_brillante[idx].append(ImageTk.PhotoImage(brillante))

# --- Crear grid de Canvas ---
def crear_grid(ventana):
    

    global botones
    for w in ventana.winfo_children():
        w.destroy()
    botones = []

    contenedor = Frame(ventana, bg=ventana.cget("bg"))
    contenedor.place(relx=POS_X, rely=POS_Y, anchor="center") #Ubicacion del rompezabezas

    for i, pieza in enumerate(orden_actual):
        r, c = divmod(i, GRID)
        frame_boton = Frame(contenedor,
                            width=frames_general[0][0].width(),
                            height=frames_general[0][0].height(),
                            bg=ventana.cget("bg"))
        frame_boton.grid_propagate(False)
        frame_boton.grid(row=r, column=c)

        canvas = Canvas(frame_boton, width=frames_general[pieza][0].width(),
                        height=frames_general[pieza][0].height(), highlightthickness=0)
        canvas.pack()
        img_id = canvas.create_image(0, 0, anchor="nw", image=frames_general[pieza][0])
        canvas.img_id = img_id
        canvas.border_id = None
        canvas.bind("<Button-1>", lambda e, i=i: click_pieza(i))
        botones.append(canvas)

# --- Mezclar piezas ---
def mezclar_piezas():
    global orden_actual

    orden_correcto = list(range(GRID**2))
    orden_actual = list(range(GRID**2))
    random.shuffle(orden_actual)

# --- Click de pieza con borde interno ---
def click_pieza(i):
    global pieza_seleccionada, orden_actual
    canvas = botones[i]

    if pieza_seleccionada is None:
        pieza_seleccionada = i
        # borde interno
        w = canvas.winfo_width()
        h = canvas.winfo_height()
        canvas.border_id = canvas.create_rectangle(2, 2, w-2, h-2, outline="white", width=4)

        # asignar versión brillante precalculada
        canvas.itemconfig(canvas.img_id, image=frames_brillante[orden_actual[i]][frame_actual[orden_actual[i]]])
        canvas.image = frames_brillante[orden_actual[i]][frame_actual[orden_actual[i]]]

    else:
        # intercambiar piezas
        orden_actual[pieza_seleccionada], orden_actual[i] = orden_actual[i], orden_actual[pieza_seleccionada]

        for idx, c in enumerate(botones):
            # borrar borde interno si existe
            if c.border_id:
                c.delete(c.border_id)
                c.border_id = None
            # restaurar imagen oscura precalculada
            c.itemconfig(c.img_id, image=frames_general[orden_actual[idx]][frame_actual[orden_actual[idx]]])
            c.image = frames_general[orden_actual[idx]][frame_actual[orden_actual[idx]]]

        pieza_seleccionada = None

# --- Animación continua ---
def animar():
    global frame_actual
    for i, idx in enumerate(orden_actual):
        frame_actual[idx] = (frame_actual[idx] + 1) % cuadros_totales
        canvas = botones[i]
        # actualizar imagen sin recalcular brillo
        if pieza_seleccionada == i:
            canvas.itemconfig(canvas.img_id, image=frames_brillante[idx][frame_actual[idx]])
            canvas.image = frames_brillante[idx][frame_actual[idx]]
        else:
            canvas.itemconfig(canvas.img_id, image=frames_general[idx][frame_actual[idx]])
            canvas.image = frames_general[idx][frame_actual[idx]]
    ventana.after(RETARDO, animar)

# --- Inicialización ---
ventana = Tk() #Crea la ventana 
ventana.title("Rompecabezas Animado")
ventana.state('zoomed') #Acomoda todo segun tamaño de pantalla
ventana.attributes('-fullscreen', True) #Pantalla completa

mezclar_piezas()
cargar_frames(ARCHIVO)
crear_grid(ventana)
animar()

ventana.mainloop()
