from tkinter import *
from PIL import Image, ImageTk
from Gear import MemoryGameLogic

######## -------->Ventana Menu Principal<--------########


def on_jugar_click(event):
    Classic_Win()


def Menu_Win():
    # Configuración del menú principal
    Menu = Tk()
    Menu.title("Memory Game, by @Kendall_MA & @Avri_AS")
    Menu.minsize(1200, 675)
    Menu.resizable(width=NO, height=NO)

    canvas = Canvas(Menu, width=1200, height=675, highlightthickness=0)
    canvas.place(x=0, y=0)

    FondoImg = Image.open(
        r"c:\Users\Kendall\Desktop\Memory_Game\Sprites\fondo_default.jpg")
    Fondo_Img = ImageTk.PhotoImage(FondoImg)
    canvas.create_image(0, 0, anchor=NW, image=Fondo_Img)
    canvas.image = Fondo_Img

    jugar_img = ImageTk.PhotoImage(Image.open(
        r"c:\Users\Kendall\Desktop\Memory_Game\Sprites\Boton_Temp.png"))
    canvas.create_image(600, 337, image=jugar_img,
                        anchor=CENTER, tags="jugar_btn")
    canvas.jugar_img = jugar_img
    canvas.tag_bind("jugar_btn", "<Button-1>", on_jugar_click)

    Menu.mainloop()

######## -------->Ventana Modo Classic<--------########


def on_jugar_click(event):
    Classic_Win()


def Classic_Win():
    Classic = Toplevel()  # Cambia Tk() por Toplevel()
    Classic.title("Memory Game, by @Kendall_MA & @Avri_AS")
    Classic.minsize(1200, 675)
    Classic.resizable(width=NO, height=NO)

    canvas = Canvas(Classic, width=1200, height=675, highlightthickness=0)
    canvas.place(x=0, y=0)

    # Fondo
    FondoImg = Image.open(
        r"c:\Users\Kendall\Desktop\Memory_Game\Sprites\fondo_default.jpg")
    Fondo_Img = ImageTk.PhotoImage(FondoImg)
    canvas.create_image(0, 0, anchor=NW, image=Fondo_Img)
    canvas.image = Fondo_Img
    Classic.fondo_img = Fondo_Img

    # Aquí solo llamas a la lógica
    MemoryGameLogic(canvas, Classic)

    Classic.mainloop()
