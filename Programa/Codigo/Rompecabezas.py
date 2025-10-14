# Rompecabezas.py

from tkinter import *
from PIL import Image, ImageTk, ImageEnhance
import random, os, sys

# --- Configuración ---
GRID = 0            # Tamaño del rompecabezas (GRID x GRID) Se actualiza en el menu principal
FRAMERATE = 80      # Milisegundos por frame
FACTOR_BRILLO = 0.9
TAM_PUZZLE = 600    # Tamaño total del rompecabezas en píxeles (cuadrado)

# --- Ruta de assets compatible con PyInstaller ---
if getattr(sys, 'frozen', False):
    CARPETA_BASE = os.path.join(sys._MEIPASS, 'Assets', 'Patrones')
else:
    CARPETA_BASE = os.path.join(os.path.dirname(__file__), "..", "Assets", "Patrones")

# --- Variables globales ---
frames_originales = []      # Solo PIL.Image
orden_correcto = []
orden_actual = []
botones = []
pieza_seleccionada = None
cuadros_totales = 0
frame_actual = []
mostrar_victoria_callback = None

animacion_after_id = None

# --- Función para elegir patrón ---
def obtener_patron(n):
    nombre_archivo = f"Patron{n}.gif"
    ruta = os.path.join(CARPETA_BASE, nombre_archivo)
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

# --- Cargar frames solo como PIL.Image ---
def cargar_frames(ruta):
    global frames_originales, cuadros_totales, frame_actual
    gif = Image.open(ruta)
    cuadros_totales = gif.n_frames

    # Cada pieza tendrá tamaño proporcional a TAM_PUZZLE / GRID
    pw, ph = TAM_PUZZLE // GRID, TAM_PUZZLE // GRID

    frames_originales.clear()
    frames_originales.extend([[] for _ in range(GRID**2)])

    for f in range(cuadros_totales):
        gif.seek(f)
        frame = gif.convert("L")  # Escala de grises
        # Redimensionar el frame completo al tamaño del puzzle
        frame = frame.resize((TAM_PUZZLE, TAM_PUZZLE), Image.Resampling.LANCZOS)
        for r in range(GRID):
            for c in range(GRID):
                idx = r*GRID + c
                recorte = frame.crop((c*pw, r*ph, (c+1)*pw, (r+1)*ph))
                frames_originales[idx].append(recorte)

    frame_actual = [0] * len(orden_actual)

# --- Crear grid de Canvas ---
def crear_grid(ventana):
    global botones
    for w in ventana.winfo_children():
        w.destroy()
    botones.clear()

    contenedor = Frame(ventana, bg=ventana.cget("bg"))
    contenedor.place(relx=0.5, rely=0.5, anchor="center")

    pw, ph = TAM_PUZZLE // GRID, TAM_PUZZLE // GRID

    for i, pieza in enumerate(orden_actual):
        r, c = divmod(i, GRID)

        frame_boton = Frame(contenedor, width=pw, height=ph, bg=ventana.cget("bg"))
        frame_boton.grid_propagate(False)
        frame_boton.grid(row=r, column=c)

        canvas = Canvas(frame_boton, width=pw, height=ph, highlightthickness=0)
        canvas.pack()
        img_tk = ImageTk.PhotoImage(frames_originales[pieza][0])
        img_id = canvas.create_image(0, 0, anchor="nw", image=img_tk)
        canvas.img_id = img_id
        canvas.border_id = None
        canvas.image = img_tk  # mantener referencia
        canvas.bind("<Button-1>", lambda e, i=i: click_pieza(i))
        botones.append(canvas)

# --- Click de pieza ---
def click_pieza(i):
    global pieza_seleccionada, orden_actual
    canvas = botones[i]

    if pieza_seleccionada is None:
        pieza_seleccionada = i
        w, h = canvas.winfo_width(), canvas.winfo_height()
        canvas.border_id = canvas.create_rectangle(2, 2, w-2, h-2, outline="white", width=4)
        actualizar_canvas(i, brillante=True)
    else:
        # Intercambiar piezas
        orden_actual[pieza_seleccionada], orden_actual[i] = orden_actual[i], orden_actual[pieza_seleccionada]
        for idx, c in enumerate(botones):
            if c.border_id:
                c.delete(c.border_id)
                c.border_id = None
            actualizar_canvas(idx, brillante=False)
        pieza_seleccionada = None

        # --- Verificar victoria ---
        if puzzle_completo():
            if 'mostrar_victoria_callback' in globals():
                mostrar_victoria_callback()


# --- Actualizar canvas de una pieza ---
def actualizar_canvas(idx, brillante=False):
    canvas = botones[idx]
    frame = frames_originales[orden_actual[idx]][frame_actual[orden_actual[idx]]]
    if brillante:
        frame_mod = ImageEnhance.Brightness(frame).enhance(1.3)
    else:
        frame_mod = ImageEnhance.Brightness(frame).enhance(FACTOR_BRILLO)

    img_tk = ImageTk.PhotoImage(frame_mod)
    canvas.itemconfig(canvas.img_id, image=img_tk)
    canvas.image = img_tk  # mantener referencia

# --- Animación ---
def animar(parent):
    global frame_actual, animacion_after_id
    for i, idx in enumerate(orden_actual):
        if idx >= len(frame_actual):
            frame_actual.append(0)
        frame_actual[idx] = (frame_actual[idx] + 1) % cuadros_totales
        brillante = (pieza_seleccionada == i)
        actualizar_canvas(i, brillante=brillante)
    animacion_after_id = parent.after(FRAMERATE, lambda: animar(parent))


def puzzle_completo():
    #Retorna True si el rompecabezas está resuelto
    return orden_actual == orden_correcto
