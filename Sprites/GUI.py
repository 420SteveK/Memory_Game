from APIBCCR import TipoCambioBCCR
from tkinter import *
from PIL import Image, ImageTk
from Gear import MemoryGameLogic
import jugador
from Musica import Musica
from GUIPatrones import PatternMemoryGUI
from logicaPatrones import PatternMemoryLogic
import threading
from Weed import Moneda
from tkinter import messagebox


class MemoryGameMenu:
    def __init__(self):
        # Inicia la música al crear el menú
        self.musica = Musica(
            r"c:\Users\Kendall\Desktop\Memory_Game\Sprites\Cancion_Fondo.mp3"
        )

        self.Menu = Tk()
        self.Menu.title("Memory Game, by @Kendall_MA & @Avri_AS")
        self.Menu.minsize(1200, 675)
        self.Menu.resizable(width=NO, height=NO)

        # --- Fondo original ---
        FondoImg = Image.open(
            r"c:\Users\Kendall\Desktop\Memory_Game\Sprites\fondo_default.jpg")
        Fondo_Img = ImageTk.PhotoImage(FondoImg)
        self.canvas = Canvas(self.Menu, width=1200,
                             height=675, highlightthickness=0)
        self.canvas.place(x=0, y=0)
        self.canvas.create_image(0, 0, anchor=NW, image=Fondo_Img)
        self.canvas.image = Fondo_Img

        # --- Estilo de botones tipo login, pero más grandes ---
        btn_font = ("Poppins", 14, "bold")
        btn_bg = "#ff69b4"
        btn_fg = "#1a1a1a"
        btn_active_bg = "#ff1493"
        btn_active_fg = "#fff"
        btn_width = 36
        btn_relief = "flat"

        # --- Botón para 2 Jugadores ---
        btn_jugadores = Button(self.Menu, text="2 Jugadores", font=btn_font,
                               bg=btn_bg, fg=btn_fg, activebackground=btn_active_bg, activeforeground=btn_active_fg,
                               relief=btn_relief, width=btn_width,
                               command=lambda: self.iniciar_juego_modo(modo_bot=False))
        btn_jugadores.place(x=400, y=500)

        # --- Botón para jugar contra Bot ---
        btn_bot = Button(self.Menu, text="Jugar contra Bot", font=btn_font,
                         bg=btn_bg, fg=btn_fg, activebackground=btn_active_bg, activeforeground=btn_active_fg,
                         relief=btn_relief, width=btn_width,
                         command=lambda: self.iniciar_juego_modo(modo_bot=True))
        btn_bot.place(x=400, y=560)

        # --- Botón para Modo Patrones ---
        btn_patrones = Button(self.Menu, text="Modo Patrones", font=btn_font,
                              bg=btn_bg, fg=btn_fg, activebackground=btn_active_bg, activeforeground=btn_active_fg,
                              relief=btn_relief, width=btn_width,
                              command=self.abrir_modo_patrones)
        btn_patrones.place(x=400, y=620)

        self.monedas = Moneda(self.Menu)  # Label de monedas

        # Botón "Canjear monedas" en la esquina superior derecha
        self.btn_canjear = Button(
            self.Menu,
            text="Canjear monedas",
            font=("Arial", 12, "bold"),
            bg="#ffb300",
            fg="#1a1a1a",
            command=self.canjear_monedas
        )
        # Debajo del label de monedas
        self.btn_canjear.place(relx=1.0, y=40, anchor="ne")

    def abrir_modo_patrones(self):
        top = Toplevel(self.Menu)
        PatternMemoryGUI(top)

    def on_jugar_click(self, event):
        self.Classic_Win()

    def iniciar_juego_modo(self, modo_bot=False):
        Classic = Toplevel(self.Menu)
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

        MemoryGameLogic(canvas, Classic, timer_label, modo_bot=modo_bot)

    def Classic_Win(self):
        Classic = Toplevel(self.Menu)
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

        MemoryGameLogic(canvas, Classic, timer_label)

    def canjear_monedas(self):
        # Obtén la cantidad de monedas
        cantidad = self.monedas.monedas

        # Llama a la API para obtener el tipo de cambio de venta
        try:
            correo = "kendall840356@gmail.com"  # Tu correo
            token = "V0DS6MI08S"                # Tu token
            bccr = TipoCambioBCCR(correo, token)
            cambio = bccr.obtener_venta()
        except Exception as e:
            messagebox.showerror(
                "Error", f"No se pudo obtener el tipo de cambio:\n{e}")
            return

        # Calcula el premio
        premio = (1 / cantidad) * 100 * cambio if cantidad > 0 else 0

        # Muestra el premio
        messagebox.showinfo(
            "Premio",
            f"Tu premio actual es de: {premio:.2f} colones\n\n"
            f"(Fórmula: 1/{cantidad} * 100 * {cambio:.2f})"

        )

    def run(self):
        self.Menu.mainloop()
