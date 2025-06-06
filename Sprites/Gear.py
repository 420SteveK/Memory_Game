from Fichas import Fichas
import random

class MemoryGameLogic:
    def __init__(self, canvas, master):
        self.canvas = canvas
        self.master = master
        self.juego_activo = True
        self.fichas = []
        self.fichas_reveladas = []

        # Generar lista de imágenes (2 de cada una del 01 al 18) para cada lado
        fichas_imgs_izq = [
            f"c:/Users/Kendall/Desktop/Memory_Game/Sprites/Ficha_{str(i).zfill(2)}.png" for i in range(1, 19)
        ] * 2  # 18 pares = 36 fichas
        fichas_imgs_der = [
            f"c:/Users/Kendall/Desktop/Memory_Game/Sprites/Ficha_{str(i).zfill(2)}.png" for i in range(1, 19)
        ] * 2  # 18 pares = 36 fichas
        random.shuffle(fichas_imgs_izq)
        random.shuffle(fichas_imgs_der)

        # Crear posiciones para dos cuadrículas de 6x6
        posiciones_izq = []
        posiciones_der = []
        for row in range(6):
            for col in range(6):
                posiciones_izq.append((100 + col*80, 100 + row*80))      # Izquierda
                posiciones_der.append((700 + col*80, 100 + row*80))     # Derecha

        # Crear las 36 fichas de la izquierda
        for i in range(36):
            f = Fichas(canvas, posiciones_izq[i][0], posiciones_izq[i][1],
                       "c:/Users/Kendall/Desktop/Memory_Game/Sprites/Ficha_00.png",
                       fichas_imgs_izq[i])
            self.fichas.append(f)

        # Crear las 36 fichas de la derecha
        for i in range(36):
            f = Fichas(canvas, posiciones_der[i][0], posiciones_der[i][1],
                       "c:/Users/Kendall/Desktop/Memory_Game/Sprites/Ficha_00.png",
                       fichas_imgs_der[i])
            self.fichas.append(f)

        # Asignar métodos al master para interacción con Fichas
        master.juego_activo = self.juego_activo
        master.fichas_reveladas = self.fichas_reveladas
        master.revelar_ficha = self.revelar_ficha

    def revelar_ficha(self, ficha):
        if ficha.estado != "oculta" or len(self.fichas_reveladas) == 2:
            return
        ficha.canvas.itemconfig(ficha.id, image=ficha.img_real)
        ficha.estado = "revelada"
        self.fichas_reveladas.append(ficha)

        if len(self.fichas_reveladas) == 2:
            f1, f2 = self.fichas_reveladas
            if f1.nombre_r == f2.nombre_r:
                # Coincidencia
                f1.canvas.itemconfig(f1.id, image=f1.img_chk)
                f2.canvas.itemconfig(f2.id, image=f2.img_chk)
                f1.estado = "lograda"
                f2.estado = "lograda"
                print("logrado")
                self.fichas_reveladas.clear()
            else:
                # No coincidencia, ocultar después de un corto tiempo
                self.juego_activo = False
                self.master.after(1000, self.ocultar_fichas)

    def ocultar_fichas(self):
        for ficha in self.fichas_reveladas:
            if ficha.estado == "revelada":
                ficha.canvas.itemconfig(ficha.id, image=ficha.img_oculta)
                ficha.estado = "oculta"
        self.fichas_reveladas.clear()
        self.juego_activo = True