# menu_principal.py

from tkinter import *
from PIL import Image, ImageTk, ImageEnhance, ImageOps, ImageEnhance
import Rompecabezas
import configuracion
import random, os, sys, time

# --- Configuración global ---
# --- Variables globales de fondo ---
COLOR_FONDO_NEGRO = "red"      # colores del overlay si quieres
COLOR_FONDO_BLANCO = "yellow"
ALPHA_OVERLAY = 1
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

def mostrar_menu_principal(ventana):
    global frames_preview, frame_preview, grid_var, indice

    # Limpiar ventana
    for w in ventana.winfo_children():
        w.destroy()

    ventana.update_idletasks()
    screen_w = ventana.winfo_width()
    screen_h = ventana.winfo_height()

    # Canvas principal para fondo
    canvas = Canvas(ventana, width=screen_w, height=screen_h, highlightthickness=0)
    canvas.pack(fill=BOTH, expand=True)

    # Cargar fondo principal
    ruta_fondo = os.path.join(os.path.dirname(__file__), "..", "Assets", "General", "fondo.png")
    fondo_img = Image.open(ruta_fondo).resize((screen_w, screen_h), Image.Resampling.LANCZOS)
    fondo_tk = ImageTk.PhotoImage(fondo_img)
    canvas.background = fondo_tk
    canvas.create_image(0, 0, anchor=NW, image=fondo_tk)

    # --- Frame central con widgets ---
    menu_frame = Frame(canvas, bg=None)
    canvas.create_window(screen_w//2, screen_h//2, window=menu_frame, anchor="center")

    # --- Después de renderizar widgets, colocar un fondo camuflado ---
    def colocar_fondo_camuflado():
        menu_frame.update_idletasks()
        fw, fh = menu_frame.winfo_width(), menu_frame.winfo_height()
        recorte = fondo_img.crop((
            (screen_w - fw)//2,
            (screen_h - fh)//2,
            (screen_w + fw)//2,
            (screen_h + fh)//2
        ))
        fondo_frame_tk = ImageTk.PhotoImage(recorte)
        label_fondo = Label(menu_frame, image=fondo_frame_tk, borderwidth=0)
        label_fondo.place(x=0, y=0, relwidth=1, relheight=1)
        label_fondo.image = fondo_frame_tk  # mantener referencia
        label_fondo.lower()  # que quede detrás de los botones

        # --- Selección de tamaño del Grid ---
    Label(menu_frame, text="Tamaño del Grid:", font=("Arial", 18), fg="white", bg=None).pack(pady=(20,5))
    tamanios = [2,4,6,8,10]
    grid_var = IntVar(value=2)

    botones_frame = Frame(menu_frame, bg=None)
    botones_frame.pack(pady=5)

    botones_tam = []
    def seleccionar_tamanio(t):
        grid_var.set(t)
        for b, val in zip(botones_tam, tamanios):
            b.config(bg="NONE" if val==t else "gray30")
            
    # Cambiamos el fondo del frame que contiene los botones de tamaño
    botones_frame.config(bg="#64070f")  # <--- color de fondo externo

    botones_tam = []
    for t in tamanios:
        b = Button(botones_frame, text=f"{t}x{t}", width=4, height=2,
                bg="gray30", fg="white", font=("Arial",14),
                activebackground="white", activeforeground="black",
                command=lambda x=t: seleccionar_tamanio(x))
        b.pack(side=LEFT, padx=8)  # separación horizontal
        botones_tam.append(b)


    # --- Patrón animado centrado con navegación ---
    canvas_size = 200
    patrones = [f"Patron{i}.gif" for i in range(1,6)]
    indice = IntVar(value=0)

    patron_frame = Frame(menu_frame, bg=None)
    patron_frame.pack(pady=10)  # menos espacio vertical arriba y abajo

      # Cambiamos el fondo del frame que contiene los botones
    patron_frame = Frame(menu_frame, bg="#64070f")  # <--- color de fondo externo
    patron_frame.pack(pady=10)

    # Botón "<"
    btn_prev = Button(patron_frame, text="<", width=2,
                    bg="gray30", fg="white",
                    activebackground="white", activeforeground="black",
                    command=lambda: cambiar_patron(-1, canvas_preview))
    btn_prev.pack(side=LEFT, padx=(0,2), pady=0)

    # Frame centrador para el canvas
    canvas_container = Frame(patron_frame, bg="#64070f")  # mismo color que el frame padre
    canvas_container.pack(side=LEFT, pady=0)

    # Canvas del patrón
    canvas_preview = Canvas(canvas_container, width=canvas_size, height=canvas_size,
                            highlightthickness=0, bg=None)
    canvas_preview.pack()

    # Botón ">"
    btn_next = Button(patron_frame, text=">", width=2,
                    bg="gray30", fg="white",
                    activebackground="white", activeforeground="black",
                    command=lambda: cambiar_patron(1, canvas_preview))
    btn_next.pack(side=LEFT, padx=(2,0), pady=0)


    # --- Botones verticales: Configuración → Jugar → Salir ---
    Button(menu_frame, text="Jugar", font=("Arial", 20),
       width=20, command=lambda: iniciar_juego_overlay(ventana, grid_var, indice)).pack(pady=10)
    Button(menu_frame, text="Configuración", font=("Arial", 20),
        width=20, command=lambda: configuracion.mostrar_configuracion(ventana)).pack(pady=10)
    Button(menu_frame, text="Salir", font=("Arial", 20),
        width=20, command=ventana.destroy).pack(pady=10)

    mostrar_patron(canvas_preview)

    # --- Finalmente colocar fondo camuflado ---
    ventana.after(50, colocar_fondo_camuflado)



def mostrar_patron(canvas):
    ruta = os.path.join(os.path.dirname(__file__), "..", "Assets", "Patrones", f"Patron{indice.get()+1}.gif")
    cargar_preview_recolor(ruta, canvas)

def cambiar_patron(d, canvas):
    indice.set((indice.get() + d) % 5)
    mostrar_patron(canvas)

def cargar_preview_recolor(ruta, canvas):
    global frames_preview, frame_preview
    canvas.update_idletasks()
    size = canvas.winfo_width() or 200

    gif = Image.open(ruta)
    frames_preview.clear()
    frame_preview = 0

    for f in range(gif.n_frames):
        gif.seek(f)
        frame = gif.convert("L").resize((size,size), Image.Resampling.LANCZOS)
        frame = ImageOps.colorize(frame, black=COLOR_FONDO_NEGRO, white=COLOR_FONDO_BLANCO)
        frames_preview.append(ImageTk.PhotoImage(frame))

    canvas.delete("all")
    canvas.create_image(size//2, size//2, image=frames_preview[0])
    canvas.image = frames_preview[0]
    animar_preview(canvas)

def animar_preview(canvas):
    global frames_preview, frame_preview
    if frames_preview:
        canvas.delete("all")
        canvas.create_image(canvas.winfo_width()//2, canvas.winfo_height()//2, image=frames_preview[frame_preview])
        frame_preview = (frame_preview + 1) % len(frames_preview)
        canvas.after(FRAMERATE, lambda: animar_preview(canvas))

def iniciar_juego_overlay(ventana, grid_var, indice):
    COLOR_BOTON = "#64070f"
    COLOR_FONDO_MENU = "#a81717"

    overlay = Frame(ventana)
    overlay.place(relx=0, rely=0, relwidth=1, relheight=1)

    # Fondo imagen
    screen_w, screen_h = ventana.winfo_width(), ventana.winfo_height()
    ruta_fondo = os.path.join(os.path.dirname(__file__), "..", "Assets", "General", "fondo.png")
    fondo_img = Image.open(ruta_fondo).resize((screen_w, screen_h), Image.Resampling.LANCZOS)
    fondo_tk = ImageTk.PhotoImage(fondo_img)
    Label(overlay, image=fondo_tk).place(x=0, y=0, relwidth=1, relheight=1)
    overlay.fondo_ref = fondo_tk

    # Contenedor central
    container = Frame(overlay, width=1000, height=700, bg=COLOR_FONDO_MENU)
    container.place(relx=0.5, rely=0.5, anchor="center")
    container.pack_propagate(False)

    # --- Panel izquierdo ---
    frame_izquierda = Frame(container, bg=COLOR_BOTON)
    frame_izquierda.pack(side="left", fill="y", padx=20, pady=20)
    frame_izquierda.config(width=250)  # Puedes ajustar el ancho aquí
    frame_izquierda.pack_propagate(False)
    frame_izquierda.lift()  # Sobre la imagen de fondo

    # Frame central para centrar verticalmente los labels
    frame_central = Frame(frame_izquierda, bg=COLOR_BOTON)
    frame_central.pack(expand=True, fill="both")  # ocupa todo el espacio vertical

    # Subframe que contendrá los labels y se centrará
    subframe_labels = Frame(frame_central, bg=COLOR_BOTON)
    subframe_labels.pack(expand=True)  # Centrado verticalmente

    # Label título del timer
    label_titulo = Label(subframe_labels, text="Tiempo transcurrido",
                        font=("Arial",16), fg="yellow", bg=COLOR_BOTON)
    label_titulo.pack(pady=(0,5))

    # Timer real
    label_timer = Label(subframe_labels, text="00:00",
                        font=("Arial",18), fg="yellow", bg=COLOR_BOTON)
    label_timer.pack(pady=(0,5))

    # Label de victoria (invisible al inicio)
    label_victoria = Label(subframe_labels, text="", font=("Arial",18,"bold"),
                        fg="yellow", bg=COLOR_BOTON, justify="center")
    label_victoria.pack(pady=(10,0))
    label_victoria.lower()  # Al inicio detrás del timer

    # Botón siempre abajo
    Button(frame_izquierda, text="Volver al menú", font=("Arial",14),
        bg=COLOR_BOTON, fg="white", command=overlay.destroy).pack(side="bottom", pady=10)
  
    # --- Rompecabezas centrado ---
    frame_juego = Frame(container, width=600, height=600, bg=COLOR_FONDO_MENU)
    frame_juego.pack(side="left", expand=True, padx=20, pady=20)
    frame_juego.pack_propagate(False)

    # Configurar rompecabezas
    Rompecabezas.GRID = grid_var.get()
    Rompecabezas.mezclar_piezas()
    patron = Rompecabezas.obtener_patron(indice.get() + 1)
    Rompecabezas.cargar_frames(patron)
    Rompecabezas.crear_grid(frame_juego)
    Rompecabezas.animar(frame_juego)

    # Timer en tiempo real
    inicio_tiempo = time.time()
    def actualizar_timer():
        segundos = int(time.time() - inicio_tiempo)
        mins, secs = divmod(segundos, 60)
        tiempo_actual = f"{mins:02d}:{secs:02d}"
        label_timer.config(text=tiempo_actual)
        label_timer.after(1000, actualizar_timer)
    actualizar_timer()

    # Callback de victoria
    def mostrar_victoria():
        global timer_after_id
        # Detener timer
        if timer_after_id is not None:
            label_timer.after_cancel(timer_after_id)
            timer_after_id = None

        # Destruir título y timer en tiempo real
        label_titulo.destroy()
        label_timer.destroy()

        # Mostrar victoria con tiempo final
        tiempo_final = time.strftime('%M:%S', time.gmtime(int(time.time() - inicio_tiempo)))
        label_victoria.config(text=f"¡Rompecabezas \ncompletado!\nTiempo total: {tiempo_final}")
        label_victoria.lift()
    Rompecabezas.mostrar_victoria_callback = mostrar_victoria



def mostrar_victoria_overlay(frame_juego, overlay):
    tiempo_total = int(time.time() - getattr(frame_juego, "inicio_tiempo", time.time()))
    mins, secs = divmod(tiempo_total, 60)

    overlay_victoria = Frame(overlay, bg="#64070f")
    overlay_victoria.place(relx=0.5, rely=0.5, anchor="center")

    Label(overlay_victoria, text="¡Rompecabezas resuelto!",
          font=("Arial", 16), fg="white", bg="#64070f").pack(pady=(10,5))
    Label(overlay_victoria, text=f"Tiempo total: {mins:02d}:{secs:02d}",
          font=("Arial", 14), fg="white", bg="#64070f").pack(pady=(0,10))

    Button(overlay_victoria, text="Volver al menú principal",
           font=("Arial", 14), bg="#64070f", fg="white",
           command=lambda: overlay.destroy()).pack(pady=10)


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
        if t:
            try: ventana.after_cancel(t)
            except: pass

    timer_after_id = None
    animacion_after_id = None
    inicio_tiempo = None
    frames_preview.clear()
    frame_preview = 0

    # Limpiar toda la ventana
    for widget in list(ventana.winfo_children()):
        try:
            widget.destroy()
        except: pass

    # Mostrar menú limpio
    mostrar_menu_principal(ventana)