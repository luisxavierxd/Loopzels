# audio.py
import pygame
import os

pygame.mixer.init()

BASE_PATH = os.path.dirname(__file__)
MUSICA_FONDO = os.path.join(BASE_PATH, "musica_fondo.mp3")
SFX_BOTON = os.path.join(BASE_PATH, "boton.wav")
SFX_VICTORIA = os.path.join(BASE_PATH, "victoria.wav")

sfx_boton = None
sfx_victoria = None
musica_iniciada = False

def inicializar_audio():
    """Carga música y SFX de forma segura."""
    global sfx_boton, sfx_victoria

    # Música de fondo
    global musica_iniciada
    if not musica_iniciada:
        if os.path.exists(MUSICA_FONDO):
            pygame.mixer.music.load(MUSICA_FONDO)
            pygame.mixer.music.set_volume(0.5)
            pygame.mixer.music.play(-1)
            musica_iniciada = True
        else:
            print(f"⚠️ Música de fondo no encontrada: {MUSICA_FONDO}")

    # SFX botón
    if os.path.exists(SFX_BOTON):
        sfx_boton = pygame.mixer.Sound(SFX_BOTON)
        sfx_boton.set_volume(0.7)
    else:
        print(f"⚠️ SFX de botón no encontrado: {SFX_BOTON}")

    # SFX victoria
    if os.path.exists(SFX_VICTORIA):
        sfx_victoria = pygame.mixer.Sound(SFX_VICTORIA)
        sfx_victoria.set_volume(0.8)
    else:
        print(f"⚠️ SFX de victoria no encontrado: {SFX_VICTORIA}")

# Funciones de reproducción
def reproducir_boton():
    if sfx_boton:
        sfx_boton.play()

def reproducir_victoria():
    if sfx_victoria:
        sfx_victoria.play()

def pausar_musica():
    pygame.mixer.music.pause()

def continuar_musica():
    pygame.mixer.music.unpause()

def detener_musica():
    pygame.mixer.music.stop()
