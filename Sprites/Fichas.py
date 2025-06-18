from tkinter import Canvas
from PIL import Image, ImageTk


class Fichas:
    def __init__(self, canvas, x, y, nombre_f, nombre_r):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.nombre_f = nombre_f  # Imagen oculta (Ficha_00.png)
        self.nombre_r = nombre_r  # Imagen real (Ficha_01.png ... Ficha_18.png)
        self.estado = "oculta"    # Puede ser "oculta", "revelada", "lograda"
        self.img_oculta = ImageTk.PhotoImage(Image.open(nombre_f))
        self.img_real = ImageTk.PhotoImage(Image.open(nombre_r))
        self.img_chk = ImageTk.PhotoImage(Image.open(
            "c:/Users/Kendall/Desktop/Memory_Game/Sprites/Ficha_Chk.png"))
        self.id = self.canvas.create_image(
            x, y, image=self.img_oculta, anchor="nw")
        self.canvas.tag_bind(self.id, "<Button-1>", self.revelar)

    def revelar(self, event):
        if self.estado == "oculta" and self.canvas.master.juego_activo:
            self.canvas.master.revelar_ficha(self)
