from tkinter import *
from PIL import Image, ImageTk
import audio  # tu módulo de audio con SFX y música
import os

color_actual = "#FFFFFF"
COLOR_BOTON = "#64070f"
COLOR_FONDO_MENU = "#a81717"

import json

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "config.json")

def cargar_config():
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"volumen": 0.8, "top_tiempos": {}}

def guardar_config(config):
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=4)


def mostrar_configuracion(ventana):
    config = cargar_config()
    overlay = Frame(ventana)
    overlay.place(relx=0, rely=0, relwidth=1, relheight=1)

    # --- Fondo ---
    ruta_fondo = os.path.join(os.path.dirname(__file__), "..", "Assets", "General", "fondo.png")
    fondo_img = Image.open(ruta_fondo).resize((ventana.winfo_width(), ventana.winfo_height()), Image.Resampling.LANCZOS)
    fondo_tk = ImageTk.PhotoImage(fondo_img)
    Label(overlay, image=fondo_tk).place(x=0, y=0, relwidth=1, relheight=1)
    overlay.fondo_ref = fondo_tk

    # --- Panel principal ---
    panel = Frame(overlay, bg=COLOR_FONDO_MENU, bd=5, relief="ridge")
    panel.place(relx=0.5, rely=0.5, anchor="center", width=460, height=420)

    Label(panel, text="Configuración", font=("Comic Sans MS", 26, "bold"),
          fg="white", bg=COLOR_FONDO_MENU).pack(pady=15)

    # --- Label de Volumen ---
    Label(panel, text="Volumen:", font=("Comic Sans MS", 18, "bold"),
          fg="white", bg=COLOR_FONDO_MENU).pack(pady=(15, 5))

    volumen = DoubleVar(value=config.get("volumen", 0.8) * 100)

    # --- Frame auxiliar para control de volumen (más abajo) ---
    frame_volumen = Frame(panel, bg=COLOR_FONDO_MENU)
    frame_volumen.pack(pady=(40, 0))  # se bajó toda la sección

    # --- Slider ---
    slider = Scale(
        frame_volumen, from_=0, to=100, orient=HORIZONTAL,
        variable=volumen, length=300, sliderlength=30,
        bg=COLOR_FONDO_MENU, fg="white",
        highlightthickness=0, troughcolor="#b83737",
        activebackground="#ff5050",
        showvalue=0
    )
    slider.pack()

    # --- Burbuja flotante (valor del volumen) ---
    burbuja = Label(
        frame_volumen,
        text=f"{int(volumen.get())}%",
        font=("Comic Sans MS", 14, "bold"),
        fg="white",
        bg=COLOR_BOTON,
        padx=8, pady=3,
        relief="flat"
    )

    # --- Función para actualizar volumen y burbuja ---
    def actualizar_volumen(val):
        valor = float(val)
        pygame_vol = max(0.0, min(valor / 100, 1.0))

        # Actualizar audio
        if audio.musica_iniciada:
            import pygame
            pygame.mixer.music.set_volume(pygame_vol)

        # Guardar configuración
        config["volumen"] = pygame_vol
        guardar_config(config)

        # Actualizar burbuja
        burbuja.config(text=f"{int(valor)}%")

        # Posición dinámica sobre el knob
        frame_volumen.update_idletasks()
        x_slider = slider.winfo_x() + (slider.winfo_width() * (valor / 100))
        y_slider = slider.winfo_y() - 25
        burbuja.place(x=x_slider, y=y_slider, anchor="s")

        # Color dinámico del canal
        intensidad = int(100 + (valor * 1.5))
        color = f"#{intensidad:02x}2020" if intensidad <= 255 else "#ff2020"
        slider.config(troughcolor=color)

    # --- Vincular función y mostrar valor inicial ---
    slider.config(command=actualizar_volumen)
    overlay.after(100, lambda: actualizar_volumen(volumen.get()))

    # --- Botón cerrar ---
    Button(
        panel,
        text="Cerrar",
        bg=COLOR_BOTON,
        fg="white",
        font=("Comic Sans MS", 18),
        activebackground="white",
        activeforeground="black",
        relief="flat",
        command=overlay.destroy
    ).pack(pady=30)
