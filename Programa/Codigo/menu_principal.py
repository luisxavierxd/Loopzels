# menu_principal.py

from tkinter import *
from PIL import Image, ImageTk, ImageEnhance
import Rompecabezas
import configuracion
import random, os, sys, time

# --- Configuración global ---
FRAMERATE = 80
FACTOR_BRILLO = 0.9
TAM_PUZZLE = 600

timer_after_id = None
animacion_after_id = None
timer_window = None
label_timer = None
inicio_tiempo = None

# --- Variables para vista previa ---
frames_preview = []
frame_preview = 0

# -------------------- Menú Principal --------------------
def mostrar_menu_principal(ventana):
    global frames_preview, frame_preview

    # Limpiar ventana
    for w in ventana.winfo_children():
        w.destroy()

    menu_frame = Frame(ventana, bg="gray10")
    menu_frame.pack(fill=BOTH, expand=True)

    # --- Selección tamaño grid ---
    Label(menu_frame, text="Tamaño del Grid:", font=("Arial", 20), fg="white", bg="gray10").pack(pady=10)
    tamanios = [2, 4, 6, 8, 10]
    grid_var = IntVar(value=6)

    botones_frame = Frame(menu_frame, bg="gray10")
    botones_frame.pack(pady=10)

    botones_tam = []
    def seleccionar_tamanio(t):
        grid_var.set(t)
        for b, val in zip(botones_tam, tamanios):
            b.config(bg="white" if val == t else "gray30")

    for t in tamanios:
        b = Button(botones_frame, text=f"{t}x{t}", width=6, height=3,
                   bg="white" if t == 6 else "gray30",
                   fg="black", font=("Arial", 16),
                   command=lambda x=t: seleccionar_tamanio(x))
        b.pack(side=LEFT, padx=5)
        botones_tam.append(b)

    # --- Selección de patrones ---
    Label(menu_frame, text="Selecciona un patrón", fg="white", bg="gray10", font=("Arial", 18)).pack(pady=20)
    canvas_size = 200
    canvas = Canvas(menu_frame, width=canvas_size, height=canvas_size, bg="gray15", highlightthickness=0)
    canvas.pack(pady=20)

    patrones = [f"Patron{i}.gif" for i in range(1, 6)]
    indice = IntVar(value=0)

    def mostrar_patron():
        ruta = Rompecabezas.obtener_patron(indice.get() + 1)
        cargar_preview_animado(ruta, canvas)

    def anterior():
        indice.set((indice.get() - 1) % len(patrones))
        mostrar_patron()

    def siguiente():
        indice.set((indice.get() + 1) % len(patrones))
        mostrar_patron()

    nav_frame = Frame(menu_frame, bg="gray10")
    nav_frame.pack(pady=10)
    Button(nav_frame, text="<", font=("Arial", 20), command=anterior).pack(side=LEFT, padx=20)
    Button(nav_frame, text=">", font=("Arial", 20), command=siguiente).pack(side=RIGHT, padx=20)

    mostrar_patron()

    # --- Botones inferiores ---
    Button(menu_frame, text="Configuración", font=("Arial", 20),
           command=lambda: configuracion.mostrar_configuracion(ventana)).pack(pady=20)

    Button(menu_frame, text="Jugar", font=("Arial", 24),
           command=lambda: iniciar_juego(ventana, grid_var, indice, menu_frame)).pack(pady=20)

# -------------------- Vista previa animada --------------------
def cargar_preview_animado(ruta, canvas):
    global frames_preview, frame_preview
    canvas.update_idletasks()
    size = canvas.winfo_width() or 200

    gif = Image.open(ruta)
    frames_preview.clear()
    frame_preview = 0
    total_frames = gif.n_frames

    for f in range(total_frames):
        gif.seek(f)
        frame = gif.convert("L")
        frame = frame.resize((size, size), Image.LANCZOS)
        frames_preview.append(ImageTk.PhotoImage(frame))

    canvas.delete("all")
    canvas.create_image(size//2, size//2, image=frames_preview[0])
    canvas.image = frames_preview[0]

    animar_preview(canvas)

def animar_preview(canvas):
    global frames_preview, frame_preview
    if frames_preview:
        canvas.delete("all")
        canvas.create_image(canvas.winfo_width()//2, canvas.winfo_height()//2,
                            image=frames_preview[frame_preview])
        frame_preview = (frame_preview + 1) % len(frames_preview)
        canvas.after(FRAMERATE, lambda: animar_preview(canvas))

def iniciar_juego(ventana, grid_var, indice, menu_frame):
    global inicio_tiempo, label_timer, frame_juego, frame_principal, timer_after_id

    # Limpiar cualquier frame previo
    if 'frame_principal' in globals() and frame_principal:
        frame_principal.destroy()

    menu_frame.destroy()

    # Configurar rompecabezas
    tamanio = grid_var.get()
    Rompecabezas.GRID = tamanio
    Rompecabezas.mezclar_piezas()
    patron = Rompecabezas.obtener_patron(indice.get() + 1)
    Rompecabezas.cargar_frames(patron)

    # --- Frame contenedor horizontal ---
    frame_principal = Frame(ventana, bg="#383838")
    frame_principal.pack(expand=True)  # expand para ocupar todo el espacio disponible

    # --- Columna izquierda: Timer ---
    frame_timer = Frame(frame_principal, width=200, height=100, bg="#383838")
    frame_timer.pack(side="left", padx=20, pady=20)

    Label(frame_timer, text="Tiempo transcurrido:", font=("Arial", 18), fg="white",
          bg="#383838", anchor="center").pack(fill="x")
    label_timer = Label(frame_timer, text="00:00", font=("Arial", 18), fg="white",
                        bg="#383838", anchor="center")
    label_timer.pack(fill="x")

    # --- Columna derecha: Rompecabezas ---
    frame_juego = Frame(frame_principal, width=TAM_PUZZLE, height=TAM_PUZZLE, bg="#383838")
    frame_juego.pack(side="left", padx=20, pady=20)

    Rompecabezas.crear_grid(frame_juego)
    Rompecabezas.animar(frame_juego)

    # Iniciar timer
    inicio_tiempo = time.time()
    actualizar_timer_interno(label_timer)

    # Callback de victoria
    Rompecabezas.mostrar_victoria_callback = lambda: mostrar_victoria(frame_juego)


def actualizar_timer_interno(label):
    global inicio_tiempo, timer_after_id
    segundos = int(time.time() - inicio_tiempo)
    mins, secs = divmod(segundos, 60)
    label.config(text=f"{mins:02d}:{secs:02d}")
    timer_after_id = label.after(1000, lambda: actualizar_timer_interno(label))

def mostrar_victoria(frame_juego):
    global inicio_tiempo, timer_after_id, animacion_after_id

    # Detener timer y animación
    for t in [timer_after_id, animacion_after_id]:
        if t is not None:
            try: frame_juego.after_cancel(t)
            except: pass
    timer_after_id = None
    animacion_after_id = None

    # Deshabilitar clics en las piezas
    for c in Rompecabezas.botones:
        c.unbind("<Button-1>")

    tiempo_total = int(time.time() - inicio_tiempo)
    mins, secs = divmod(tiempo_total, 60)

    frame_principal = frame_juego.master
    frame_timer = frame_principal.winfo_children()[0]  # columna timer
    frame_principal.update_idletasks()

    # Limpiar overlays anteriores
    for child in frame_principal.winfo_children():
        if getattr(child, "is_victoria_overlay", False):
            child.destroy()

    # Crear overlay sobre frame_principal
    overlay_width = frame_timer.winfo_width()
    overlay_height = 80 + 40  # texto + botón
    victoria_overlay = Frame(frame_principal, width=overlay_width, height=overlay_height, bg="#383838")
    victoria_overlay.is_victoria_overlay = True
    victoria_overlay.place(x=frame_timer.winfo_x(),
                           y=frame_timer.winfo_y(),
                           width=overlay_width,
                           height=overlay_height)

    contenedor = Frame(victoria_overlay, bg="#383838")
    contenedor.pack(expand=True)

    Label(contenedor, text="¡Rompecabezas resuelto!", font=("Arial", 14),
          fg="white", bg="#383838").pack(pady=(5,2))
    Label(contenedor, text=f"Tiempo total: {mins:02d}:{secs:02d}", font=("Arial", 12),
          fg="white", bg="#383838").pack(pady=(0,5))

    # Botón al primer click
    Button(contenedor, text="Volver al menú principal", font=("Arial", 14),
           command=lambda: volver_menu_principal(frame_juego.winfo_toplevel())).pack(pady=5)

    # Forzar que el overlay reciba eventos
    victoria_overlay.lift()
    victoria_overlay.focus_set()




def ejecutar_doble_volver(ventana):
    # Primera ejecución inmediata
    volver_menu_principal(ventana)
    # Segunda ejecución después de 50 ms
    ventana.after(1000, lambda: volver_menu_principal(ventana))

def volver_menu_principal(ventana):
    global frames_preview, frame_preview, inicio_tiempo, timer_after_id, animacion_after_id

    # Cancelar timers pendientes de forma segura
    for t in [timer_after_id, animacion_after_id]:
        if t is not None:
            try:
                ventana.after_cancel(t)
            except Exception:
                pass

    timer_after_id = None
    animacion_after_id = None

    # Limpiar variables globales
    frames_preview.clear()
    frame_preview = 0
    inicio_tiempo = None

    # Destruir TODO el contenido de la ventana raíz
    # Usamos una copia de la lista de widgets para evitar problemas al destruir
    for widget in list(ventana.winfo_children()):
        try:
            widget.destroy()
        except Exception:
            pass

    # Mostrar menú principal limpio
    mostrar_menu_principal(ventana)
