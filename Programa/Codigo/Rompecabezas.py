# Rompecabezas.py

from tkinter import *
from PIL import Image, ImageTk, ImageEnhance,ImageOps
import random, os, sys

# --- Configuración ---
GRID = 0
FRAMERATE = 80
FACTOR_BRILLO = 0.9
TAM_PUZZLE = 600
botones_activos = True

if getattr(sys, 'frozen', False):
    CARPETA_BASE = os.path.join(sys._MEIPASS, 'Assets', 'Patrones')
else:
    CARPETA_BASE = os.path.join(os.path.dirname(__file__), "..", "Assets", "Patrones")

frames_originales = []   # PIL.Images de cada pieza
orden_correcto = []
orden_actual = []
botones = []
frame_actual = []
pieza_seleccionada = None
cuadros_totales = 0
mostrar_victoria_callback = None
animacion_after_id = None
imagenes_canvas = []  # <-- lista global de referencias ImageTk

# --- Obtener patrón ---
def obtener_patron(n):
    ruta = os.path.join(CARPETA_BASE, f"Patron{n}.gif")
    if not os.path.exists(ruta):
        raise FileNotFoundError(f"No existe el archivo: {ruta}")
    return ruta

# --- Mezclar piezas ---
def mezclar_piezas():
    global orden_actual, orden_correcto
    orden_correcto = list(range(GRID**2))
    orden_actual = list(range(GRID**2))
    while orden_actual == orden_correcto:
        random.shuffle(orden_actual)

# --- Cargar frames ---
def cargar_frames(ruta):
    global frames_originales, cuadros_totales, frame_actual
    gif = Image.open(ruta)
    cuadros_totales = gif.n_frames

    pw, ph = TAM_PUZZLE // GRID, TAM_PUZZLE // GRID

    frames_originales.clear()
    frames_originales.extend([[] for _ in range(GRID**2)])

    for f in range(cuadros_totales):
        gif.seek(f)
        frame = gif.convert("L").resize((TAM_PUZZLE, TAM_PUZZLE), Image.Resampling.LANCZOS)
        for r in range(GRID):
            for c in range(GRID):
                idx = r*GRID + c
                recorte = frame.crop((c*pw, r*ph, (c+1)*pw, (r+1)*ph))
                frames_originales[idx].append(recorte)

    frame_actual = [0]*len(orden_actual)

# --- Crear grid ---
def crear_grid(ventana):
    global botones, imagenes_canvas
    for w in ventana.winfo_children():
        w.destroy()
    botones.clear()
    imagenes_canvas.clear()

    contenedor = Frame(ventana, bg=ventana.cget("bg"))
    contenedor.place(relx=0.5, rely=0.5, anchor="center")

    pw, ph = TAM_PUZZLE//GRID, TAM_PUZZLE//GRID

    for i, pieza in enumerate(orden_actual):
        r, c = divmod(i, GRID)
        frame_boton = Frame(contenedor, width=pw, height=ph, bg=ventana.cget("bg"))
        frame_boton.grid_propagate(False)
        frame_boton.grid(row=r, column=c)

        canvas = Canvas(frame_boton, width=pw, height=ph, highlightthickness=0)
        canvas.pack(fill="both", expand=True)
        img_tk = ImageTk.PhotoImage(frames_originales[pieza][0])
        canvas.img_id = canvas.create_image(0, 0, anchor="nw", image=img_tk)
        canvas.image = img_tk
        imagenes_canvas.append(img_tk)  # <-- referencia global
        canvas.border_id = None
        canvas.bind("<Button-1>", lambda e, i=i: click_pieza(i))
        botones.append(canvas)

# --- Click ---
def click_pieza(i):
    global pieza_seleccionada, orden_actual, botones_activos
    if not botones_activos:
        return  # ignorar clics si los botones están deshabilitados

    canvas = botones[i]

    if pieza_seleccionada is None:
        pieza_seleccionada = i
        w, h = canvas.winfo_width(), canvas.winfo_height()
        canvas.border_id = canvas.create_rectangle(2,2,w-2,h-2, outline="white", width=4)
        actualizar_canvas(i, brillante=True)
    else:
        orden_actual[pieza_seleccionada], orden_actual[i] = orden_actual[i], orden_actual[pieza_seleccionada]
        for idx, c in enumerate(botones):
            if c.border_id:
                c.delete(c.border_id)
                c.border_id = None
            actualizar_canvas(idx, brillante=False)
        pieza_seleccionada = None

        if puzzle_completo() and mostrar_victoria_callback:
            botones_activos = False  # <-- deshabilitar botones al ganar
            mostrar_victoria_callback()


# --- Actualizar canvas ---
def actualizar_canvas(idx, brillante=False):
    canvas = botones[idx]
    frame = frames_originales[orden_actual[idx]][frame_actual[orden_actual[idx]]]

    # Ajustar brillo sin modificar el frame original
    frame_mod = ImageEnhance.Brightness(frame).enhance(1.3 if brillante else FACTOR_BRILLO)

    # Convertir a RGBA y colorizar solo para mostrar
    frame_color = ImageOps.colorize(frame_mod.convert("L"), black="#FF0000", white="#FFFF00").convert("RGBA")

    # Crear imagen Tk y actualizar canvas
    img_tk = ImageTk.PhotoImage(frame_color)
    canvas.itemconfig(canvas.img_id, image=img_tk)
    canvas.image = img_tk
    if idx >= len(imagenes_canvas):
        imagenes_canvas.append(img_tk)
    else:
        imagenes_canvas[idx] = img_tk


# --- Animación ---
def animar(parent):
    global frame_actual, animacion_after_id
    for i, idx in enumerate(orden_actual):
        if idx >= len(frame_actual):
            frame_actual.append(0)
        frame_actual[idx] = (frame_actual[idx]+1)%cuadros_totales
        actualizar_canvas(i, brillante=(pieza_seleccionada==i))
    animacion_after_id = parent.after(FRAMERATE, lambda: animar(parent))

# --- Verificar victoria ---
def puzzle_completo():
    return orden_actual == orden_correcto
