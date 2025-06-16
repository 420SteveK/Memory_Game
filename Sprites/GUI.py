from tkinter import *
from PIL import Image, ImageTk
from Gear import MemoryGameLogic
import jugador

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

    """jugar_img = ImageTk.PhotoImage(Image.open(
        r"c:\Users\Kendall\Desktop\Memory_Game\Sprites\Boton_Temp.png"))
    canvas.create_image(600, 337, image=jugar_img,
                        anchor=CENTER, tags="jugar_btn")
    canvas.jugar_img = jugar_img
    canvas.tag_bind("jugar_btn", "<Button-1>", on_jugar_click)
    """
     # --- Botón para 2 Jugadores ---
    btn_jugadores = Button(Menu, text="2 Jugadores", font=("Arial", 16, "bold"),
                           bg="#ffb6c1", fg="#1a1a1a", width=16,
                           command=lambda: iniciar_juego_modo(Menu, modo_bot=False))
    btn_jugadores.place(x=450, y=500)

    # --- Botón para jugar contra Bot ---
    btn_bot = Button(Menu, text="Jugar contra Bot", font=("Arial", 16, "bold"),
                     bg="#b6eaff", fg="#1a1a1a", width=16,
                     command=lambda: iniciar_juego_modo(Menu, modo_bot=True))
    btn_bot.place(x=700, y=500)

    Menu.mainloop()

def iniciar_juego_modo(master, modo_bot=False):
    Classic = Toplevel(master)
    Classic.title("Memory Game, by @Kendall_MA & @Avri_AS")
    Classic.minsize(1200, 675)
    Classic.resizable(width=NO, height=NO)

    canvas = Canvas(Classic, width=1200, height=675, highlightthickness=0)
    canvas.place(x=0, y=0)

    FondoImg = Image.open(
        r"c:\Users\Kendall\Desktop\Memory_Game\Sprites\fondo_default.jpg")
    Fondo_Img = ImageTk.PhotoImage(FondoImg)
    canvas.create_image(0, 0, anchor=NW, image=Fondo_Img)
    canvas.image = Fondo_Img
    Classic.fondo_img = Fondo_Img

    timer_label = Label(Classic, text="Tiempo: 0",
                        font=("Arial", 24), bg="#ffffff")
    timer_label.place(x=550, y=10)

    # Pasa el modo_bot al constructor de la lógica
    MemoryGameLogic(canvas, Classic, timer_label, modo_bot=modo_bot)

    Classic.mainloop()

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

    # --- TEMPORIZADOR ---
    timer_label = Label(Classic, text="Tiempo: 0",
                        font=("Arial", 24), bg="#ffffff")
    timer_label.place(x=550, y=10)

    # Pasa el label al constructor de la lógica
    MemoryGameLogic(canvas, Classic, timer_label)

    Classic.mainloop()
