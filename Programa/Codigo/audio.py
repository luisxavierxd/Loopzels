# audio.py
import pygame
import os
import json

pygame.mixer.init()

BASE_PATH = os.path.dirname(__file__)
AUDIO_PATH = os.path.join(BASE_PATH, "..", "Assets", "Audio")  # subir un nivel y entrar a Assets/Audio
MUSICA_FONDO = os.path.join(AUDIO_PATH, "musica_fondo.mp3")

musica_iniciada = False

# Ruta de configuración (desde tu proyecto/codigo)
CONFIG_PATH = os.path.join(BASE_PATH, "..", "Codigo", "config.json")

def cargar_volumen_guardado():
    """Lee el volumen guardado en config.json o devuelve 0.5 si no existe."""
    if os.path.exists(CONFIG_PATH):
        try:
            with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                config = json.load(f)
            return config.get("volumen", 0.5)
        except Exception as e:
            print(f"⚠️ Error leyendo config.json: {e}")
            return 0.5
    return 0.5

def inicializar_audio():
    """Carga música usando el volumen guardado en config.json."""
    global musica_iniciada

    volumen_guardado = cargar_volumen_guardado()

    # Música de fondo
    if not musica_iniciada:
        if os.path.exists(MUSICA_FONDO):
            pygame.mixer.music.load(MUSICA_FONDO)
            pygame.mixer.music.set_volume(volumen_guardado)
            pygame.mixer.music.play(-1)
            musica_iniciada = True
        else:
            print(f"⚠️ Música de fondo no encontrada: {MUSICA_FONDO}")

# --- Funciones de reproducción ---
def pausar_musica():
    pygame.mixer.music.pause()

def continuar_musica():
    pygame.mixer.music.unpause()

def detener_musica():
    pygame.mixer.music.stop()

def set_volumen(volumen: float):
    """
    Cambia el volumen de la música.
    volumen: float entre 0.0 y 1.0
    """
    volumen = max(0.0, min(volumen, 1.0))
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.set_volume(volumen)
