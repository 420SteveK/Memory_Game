import os
import pygame


class Musica:
    def __init__(self, ruta):
        # Si es otro archivo, nomas le cambia el nombre y ya, no sea huevon
        self.ruta = ruta

        # Inicializa el mixer de pygame
        pygame.mixer.init()

        # Carga la canción (ajusta la ruta si es necesario)
        pygame.mixer.music.load(self.ruta)

        # Reproduce la canción en bucle (-1 = infinito)
        pygame.mixer.music.play(-1)  # -1 para bucle infinito

    def detener(self):
        # Detén la música al salir
        pygame.mixer.music.stop()
