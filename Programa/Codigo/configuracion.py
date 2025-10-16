from tkinter import *
from PIL import Image, ImageTk
import audio  # tu módulo de audio con SFX y música
import os

color_actual = "#FFFFFF"

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

"""
# --- Slider personalizado comentado temporalmente ---
class VolumeSlider(Canvas):
    def __init__(self, master, width=250, height=50, bar_path=None, knob_path=None, mute_icon_path=None, **kwargs):
        super().__init__(master, width=width, height=height, bg=master["bg"], highlightthickness=0, **kwargs)
        self.width = width
        self.height = height
        self.value = 50
        self.knob_x = self.width * self.value / 100
        self.is_muted = False
        self.prev_value = self.value
        # Eventos, dibujado y actualizar_audio() quedan aquí...
"""

def mostrar_configuracion(ventana):
    config = cargar_config()
    overlay = Frame(ventana)
    overlay.place(relx=0, rely=0, relwidth=1, relheight=1)

    # --- Fondo imagen ---
    ruta_fondo = os.path.join(os.path.dirname(__file__), "..", "Assets", "General", "fondo.png")
    fondo_img = Image.open(ruta_fondo).resize((ventana.winfo_width(), ventana.winfo_height()), Image.Resampling.LANCZOS)
    fondo_tk = ImageTk.PhotoImage(fondo_img)
    Label(overlay, image=fondo_tk).place(x=0, y=0, relwidth=1, relheight=1)
    overlay.fondo_ref = fondo_tk

    panel = Frame(overlay, bg="gray20", bd=4, relief="ridge")
    panel.place(relx=0.5, rely=0.5, anchor="center")
    Label(panel, text="Configuración", font=("Arial", 26, "bold"), fg="white", bg="gray20").pack(pady=15)

    # --- Slider personalizado comentado temporalmente ---
    """
    slider = VolumeSlider(panel, width=250, height=50,
                          bar_path=None, knob_path=None, mute_icon_path=None)
    slider.pack(pady=20)
    Button(panel, text="🔇", font=("Arial", 16), command=slider.toggle_mute).pack(pady=5)
    """

    # --- Slider normal de Tkinter para volumen ---
    Label(panel, text="Volumen:", font=("Arial", 18), fg="white", bg="gray20").pack(pady=(10,0))
    volumen = DoubleVar(value=config.get("volumen", 0.8)*100)

    def actualizar_volumen(val):
        valor = float(val)
        print(f"Volumen actual: {valor}")
        pygame_vol = max(0.0, min(valor / 100, 1.0))
        if audio.musica_iniciada:
            import pygame
            pygame.mixer.music.set_volume(pygame_vol)
        if audio.sfx_boton:
            audio.sfx_boton.set_volume(pygame_vol)
        if audio.sfx_victoria:
            audio.sfx_victoria.set_volume(pygame_vol)
        # Guardar en config.json
        config["volumen"] = pygame_vol
        guardar_config(config)

    Scale(panel, from_=0, to=100, orient=HORIZONTAL, variable=volumen,
          command=actualizar_volumen, length=250).pack(pady=10)

    # --- Cerrar ---
    Button(panel, text="Cerrar", font=("Arial", 18), command=overlay.destroy).pack(pady=10)



class VolumeSlider(Canvas):
    def __init__(self, master, width=200, height=40, bar_path=None, knob_path=None, mute_icon_path=None, **kwargs):
        super().__init__(master, width=width, height=height, bg=master["bg"], highlightthickness=0, **kwargs)
        self.width = width
        self.height = height

        # --- Cargar assets ---
        if bar_path:
            bar_img = Image.open(bar_path).resize((width, 10))
            self.bar_tk = ImageTk.PhotoImage(bar_img)
        else:
            self.bar_tk = None

        if knob_path:
            knob_img = Image.open(knob_path).resize((30, 30))
            self.knob_tk = ImageTk.PhotoImage(knob_img)
        else:
            self.knob_tk = None

        # Icono mute
        self.mute_icon = None
        if mute_icon_path:
            img = Image.open(mute_icon_path).resize((30, 30))
            self.mute_icon = ImageTk.PhotoImage(img)

        # --- Estado ---
        self.value = 50  # 0-100
        self.knob_x = self.width * self.value / 100
        self.is_muted = False

        # --- Dibujar ---
        if self.bar_tk:
            self.create_image(width//2, height//2, image=self.bar_tk)
        if self.knob_tk:
            self.knob_id = self.create_image(self.knob_x, height//2, image=self.knob_tk)
        else:
            self.knob_id = self.create_oval(self.knob_x-10, height//2-10,
                                            self.knob_x+10, height//2+10,
                                            fill="white", outline="black")

        # Icono mute
        self.icon_id = None
        if self.mute_icon:
            self.icon_id = self.create_image(-20, height//2, image=self.mute_icon, anchor=W)
            self.current_icon_img = self.mute_icon

        # --- Eventos ---
        self.bind("<Button-1>", self.click)
        self.bind("<B1-Motion>", self.drag)

    def click(self, event):
        if not self.is_muted:
            self.update_value(event.x)

    def drag(self, event):
        if not self.is_muted:
            self.update_value(event.x)

    def update_value(self, x):
        x = max(0, min(x, self.width))
        self.knob_x = x
        if isinstance(self.knob_id, int):  # oval
            self.coords(self.knob_id, self.knob_x-10, self.height//2-10,
                        self.knob_x+10, self.height//2+10)
        else:  # imagen
            self.coords(self.knob_id, self.knob_x, self.height//2)

        self.value = int((self.knob_x / self.width) * 100)

    def toggle_mute(self):
        self.is_muted = not self.is_muted
        if self.is_muted:
            self.value = 0
            self.update_value(0)
        else:
            self.update_value(self.knob_x)  # restaurar valor anterior
