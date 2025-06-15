from tkinter import *


class PatternGameGUI(Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Memory Game - Modo Patrones, by @Kendall_MA & @Avri_AS")
        self.minsize(1200, 675)
        self.resizable(width=NO, height=NO)

        self.canvas = Canvas(self, width=1200, height=675, highlightthickness=0)
        self.canvas.place(x=0, y=0)

        # Fondo usando PhotoImage (solo PNG/GIF soportados por tkinter)
        try:
            self.fondo_Img = PhotoImage(file=r"Memory_Game\Sprites\Fondo_Default.jpg.png")
            self.canvas.create_image(0, 0, anchor=NW, image=self.fondo_Img)
        except Exception:
            self.canvas.create_rectangle(0, 0, 1200, 675, fill="#cccccc")


        # Temporizador
        self.timer_label = Label(self, text="Tiempo: 0", font=("Arial", 24), bg="#ffffff")
        self.timer_label.place(x=550, y=10)
        