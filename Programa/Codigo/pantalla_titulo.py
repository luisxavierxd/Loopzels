import os
import sys
import threading
import tkinter as tk
import customtkinter as ctk
from PIL import Image, ImageTk, ImageSequence, ImageEnhance, ImageOps
import menu_principal

# --- CONFIGURACIÓN ---
TIEMPO_ROTACION = 10000
VELOCIDAD_GIF = 80
ALPHA_OVERLAY = 0.4
OVERLAY_WIDTH_RATIO = 0.7
OVERLAY_HEIGHT_RATIO = 0.7

if getattr(sys, 'frozen', False):
    CARPETA_BASE = os.path.join(sys._MEIPASS, 'Assets', 'Patrones')
else:
    CARPETA_BASE = os.path.join(os.path.dirname(__file__), "..", "Assets", "Patrones")


# --- Fondo animado ---
class FondoAnimado(tk.Label):
    def __init__(self, master, archivo):
        super().__init__(master)
        self.master = master
        # Tomar tamaño real de pantalla
        self.ancho = master.winfo_screenwidth()
        self.alto = master.winfo_screenheight()
        self.frames_gray = []
        self.frames_color = []
        self.idx = 0
        self.animando = True
        self.archivo = archivo
        self.place(x=0, y=0, width=self.ancho, height=self.alto)
        self.lower()
        self._cargar_frames(archivo)
        if self.frames_gray:
            self.configure(image=self.frames_gray[0])
            if len(self.frames_gray) > 1:
                self.animar()

    def _cargar_frames(self, archivo):
        self.frames_gray.clear()
        self.frames_color.clear()
        img = Image.open(archivo)
        size = (self.ancho, self.alto)

        if archivo.lower().endswith(".gif"):
            for frame in ImageSequence.Iterator(img):
                f_gray = ImageOps.grayscale(frame).convert("RGBA").resize(size, Image.Resampling.LANCZOS)
                f_color = frame.convert("RGBA").resize(size, Image.Resampling.LANCZOS)
                self.frames_gray.append(ImageTk.PhotoImage(f_gray))
                self.frames_color.append(f_color)
        else:
            f_gray = ImageOps.grayscale(img).convert("RGBA").resize(size, Image.Resampling.LANCZOS)
            f_color = img.convert("RGBA").resize(size, Image.Resampling.LANCZOS)
            self.frames_gray = [ImageTk.PhotoImage(f_gray)]
            self.frames_color = [f_color]

    def animar(self):
        if self.animando and self.frames_gray:
            self.configure(image=self.frames_gray[self.idx])
            self.idx = (self.idx + 1) % len(self.frames_gray)
            self.master.after(VELOCIDAD_GIF, self.animar)

    def actualizar_frames_nuevos(self, new_gray, new_color):
        old_idx = self.idx
        self.frames_gray = new_gray
        self.frames_color = new_color
        self.idx = old_idx % len(new_gray)


# --- Pantalla de título ---
class PantallaTitulo:
    def __init__(self, ventana):
        self.ventana = ventana
        self.archivos = self.obtener_archivos_fondo()
        self.indice = 0
        self.fondo = None
        self.overlay_canvas = None
        self.overlay_img = None

        self.screen_w = ventana.winfo_screenwidth()
        self.screen_h = ventana.winfo_screenheight()

        # Ocultar ventana hasta que el primer fondo esté listo
        self.ventana.withdraw()
        if self.archivos:
            self._precargar_primer_fondo()

    def obtener_archivos_fondo(self):
        permitidos = (".gif", ".png")
        archivos = []
        if os.path.exists(CARPETA_BASE):
            for f in os.listdir(CARPETA_BASE):
                if f.lower().endswith(permitidos):
                    archivos.append(os.path.join(CARPETA_BASE, f))
        return archivos

    def _precargar_primer_fondo(self):
        self.fondo = FondoAnimado(self.ventana, self.archivos[self.indice])
        self.indice = (self.indice + 1) % len(self.archivos)
        self.ventana.after(50, self._mostrar_primer_fondo)

    def _mostrar_primer_fondo(self):
        self.crear_overlay()
        self.ventana.deiconify()
        self.ventana.after(TIEMPO_ROTACION, self.rotar_fondo)

    def rotar_fondo(self):
        siguiente_archivo = self.archivos[self.indice]
        self.indice = (self.indice + 1) % len(self.archivos)

        def cargar_frames():
            temp_gray, temp_color = self._precargar_frames_gif(siguiente_archivo)
            self.ventana.after(0, lambda: self.fondo.actualizar_frames_nuevos(temp_gray, temp_color))

        threading.Thread(target=cargar_frames, daemon=True).start()
        self.ventana.after(TIEMPO_ROTACION, self.rotar_fondo)

    def _precargar_frames_gif(self, archivo):
        img = Image.open(archivo)
        size = (self.screen_w, self.screen_h)
        new_gray = []
        new_color = []

        if archivo.lower().endswith(".gif"):
            for frame in ImageSequence.Iterator(img):
                f_gray = ImageOps.grayscale(frame).convert("RGBA").resize(size, Image.Resampling.LANCZOS)
                f_color = frame.convert("RGBA").resize(size, Image.Resampling.LANCZOS)
                new_gray.append(ImageTk.PhotoImage(f_gray))
                new_color.append(f_color)
        else:
            f_gray = ImageOps.grayscale(img).convert("RGBA").resize(size, Image.Resampling.LANCZOS)
            f_color = img.convert("RGBA").resize(size, Image.Resampling.LANCZOS)
            new_gray = [ImageTk.PhotoImage(f_gray)]
            new_color = [f_color]

        return new_gray, new_color

    def crear_overlay(self):
        self.w_overlay = int(self.screen_w * OVERLAY_WIDTH_RATIO)
        self.h_overlay = int(self.screen_h * OVERLAY_HEIGHT_RATIO)
        self.x_offset = (self.screen_w - self.w_overlay) // 2
        self.y_offset = (self.screen_h - self.h_overlay) // 2

        if self.overlay_canvas:
            self.overlay_canvas.destroy()
        self.overlay_canvas = tk.Canvas(self.ventana, width=self.w_overlay, height=self.h_overlay, highlightthickness=0)
        self.overlay_canvas.place(x=self.x_offset, y=self.y_offset)

        ctk.CTkLabel(self.ventana,
                     text="ROMPECABEZAS ANIMADO",
                     font=ctk.CTkFont(size=48, weight="bold"),
                     fg_color=None,
                     text_color="white").place(relx=0.5, rely=0.45, anchor="center")

        ctk.CTkButton(self.ventana, text="JUGAR",
                      width=300, height=60,
                      font=ctk.CTkFont(size=26),
                      fg_color="#444444",
                      hover_color="#555555",
                      command=lambda: menu_principal.mostrar_menu_principal(self.ventana)).place(relx=0.5, rely=0.6, anchor="center")

        ctk.CTkButton(self.ventana, text="SALIR",
                      width=300, height=60,
                      font=ctk.CTkFont(size=26),
                      fg_color="#444444",
                      hover_color="#555555",
                      command=self.ventana.destroy).place(relx=0.5, rely=0.7, anchor="center")

        self.ventana.after(VELOCIDAD_GIF, self.animar_overlay)

    def actualizar_overlay(self):
        if self.fondo and self.fondo.frames_color:
            idx = self.fondo.idx
            x2 = self.x_offset + self.w_overlay
            y2 = self.y_offset + self.h_overlay
            frame = self.fondo.frames_color[idx].crop((self.x_offset, self.y_offset, x2, y2))
            img = ImageOps.grayscale(frame).convert("RGBA")
            img = ImageEnhance.Brightness(img).enhance(ALPHA_OVERLAY)
            self.overlay_img = ImageTk.PhotoImage(img)
            self.overlay_canvas.create_image(0, 0, anchor="nw", image=self.overlay_img)

    def animar_overlay(self):
        self.actualizar_overlay()
        self.ventana.after(VELOCIDAD_GIF, self.animar_overlay)


def mostrar_pantalla_titulo(ventana):
    PantallaTitulo(ventana)
