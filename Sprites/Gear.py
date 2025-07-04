from jugador import Jugador
from Fichas import Fichas
import random
import jugador
from PIL import Image, ImageTk  # Asegúrate de tener Pillow instalado
from Weed import Moneda  # <--- Agrega esto


class MemoryGameLogic:
    def __init__(self, canvas, master, timer_label, modo_bot=False):
        self.canvas = canvas
        self.master = master
        self.timer_label = timer_label
        self.timer_value = 0
        self.timer_state = True
        self.update_timer()
        self.juego_activo = True
        self.fichas = []
        self.fichas_reveladas = []
        self.modo_bot = modo_bot
        self.monedas = Moneda(master)  # <--- Instancia de Moneda

        # Jugadores
        self.jugador_izq = Jugador("Izquierda")
        self.jugador_der = Jugador("Derecha")
        self.turno = "Izquierda"  # Comienza Izquierda

        # Fichas para cada lado
        fichas_imgs_izq = [
            f"c:/Users/Kendall/Desktop/Memory_Game/Sprites/Ficha_{str(i).zfill(2)}.png" for i in range(1, 19)
        ] * 2
        fichas_imgs_der = [
            f"c:/Users/Kendall/Desktop/Memory_Game/Sprites/Ficha_{str(i).zfill(2)}.png" for i in range(1, 19)
        ] * 2
        random.shuffle(fichas_imgs_izq)
        random.shuffle(fichas_imgs_der)

        self.lado_fichas = {}  # id de ficha: lado

        posiciones_izq = []
        posiciones_der = []
        for row in range(6):
            for col in range(6):
                posiciones_izq.append((100 + col*80, 100 + row*80))
                posiciones_der.append((700 + col*80, 100 + row*80))

        for i in range(36):
            f = Fichas(canvas, posiciones_izq[i][0], posiciones_izq[i][1],
                       "c:/Users/Kendall/Desktop/Memory_Game/Sprites/Ficha_00.png",
                       fichas_imgs_izq[i])
            self.fichas.append(f)
            self.lado_fichas[f.id] = "Izquierda"

        for i in range(36):
            f = Fichas(canvas, posiciones_der[i][0], posiciones_der[i][1],
                       "c:/Users/Kendall/Desktop/Memory_Game/Sprites/Ficha_00.png",
                       fichas_imgs_der[i])
            self.fichas.append(f)
            self.lado_fichas[f.id] = "Derecha"

        master.juego_activo = self.juego_activo
        master.fichas_reveladas = self.fichas_reveladas
        master.revelar_ficha = self.revelar_ficha

    def update_timer(self):
        self.timer_label.config(text=f"Tiempo: {self.timer_value}")
        self.timer_value += 1
        if self.timer_value > 10:
            self.timer_value = 0
            self.timer_state = not self.timer_state
            self.cambiar_turno()
        self.master.after(1000, self.update_timer)

    def jugar_contra_bot(self):
        # El bot elige aleatoriamente dos fichas de su lado que estén ocultas.
        if self.turno != "Derecha" or not self.juego_activo:
            return
        fichas_ocultas = [f for f in self.fichas if self.lado_fichas[f.id]
                          == "Derecha" and f.estado == "oculta"]
        if len(fichas_ocultas) < 2:
            return
        seleccion = random.sample(fichas_ocultas, 2)
        for ficha in seleccion:
            self.revelar_ficha(ficha)

    def cambiar_turno(self):
        self.turno = "Derecha" if self.turno == "Izquierda" else "Izquierda"
        self.timer_value = 0  # Reinicia el tiempo al cambiar turno
        # Si está activado el modo bot y es el turno del bot, juega automáticamente
        if self.modo_bot and self.turno == "Derecha":
            self.master.after(800, self.jugar_contra_bot)

    def restar_tiempo(self, segundos):
        self.timer_value = max(0, self.timer_value - segundos)
        self.timer_label.config(text=f"Tiempo: {self.timer_value}")

    def revelar_ficha(self, ficha):
        # Solo permite tocar fichas del lado correspondiente al turno
        lado = self.lado_fichas.get(ficha.id)
        if lado != self.turno or ficha.estado != "oculta" or len(self.fichas_reveladas) == 2:
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
                self.monedas.calcular_monedas(1)  # <--- Suma 1 moneda
                if self.turno == "Izquierda":
                    self.jugador_izq.agregarPuntaje(1)
                else:
                    self.jugador_der.agregarPuntaje(1)
                self.restar_tiempo(3)
                self.fichas_reveladas.clear()
                self.verificar_victoria()  # <-- Agrega esta línea
            else:
                # No coincidencia, ocultar después de un corto tiempo y cambiar turno
                self.juego_activo = False
                self.master.after(1000, self.ocultar_fichas_y_cambiar_turno)

    def ocultar_fichas_y_cambiar_turno(self):
        for ficha in self.fichas_reveladas:
            if ficha.estado == "revelada":
                ficha.canvas.itemconfig(ficha.id, image=ficha.img_oculta)
                ficha.estado = "oculta"
        self.fichas_reveladas.clear()
        self.juego_activo = True
        self.cambiar_turno()
        self.timer_value = 0  # Reinicia el tiempo al cambiar turno

    def verificar_victoria(self):
        # Cargar imágenes de victoria solo una vez
        img_win_izq = ImageTk.PhotoImage(Image.open(
            r"c:\Users\Kendall\Desktop\Memory_Game\Sprites\Imagen_WnIzq.png"))
        img_win_der = ImageTk.PhotoImage(Image.open(
            r"c:\Users\Kendall\Desktop\Memory_Game\Sprites\Imagen_WnDer.png"))

        # Verifica si todas las fichas de un lado están logradas
        for lado, img_win in [("Izquierda", img_win_izq), ("Derecha", img_win_der)]:
            fichas_lado = [
                f for f in self.fichas if self.lado_fichas[f.id] == lado]
            if all(f.estado == "lograda" for f in fichas_lado):
                # Cambia todas las imágenes de ese lado por la imagen de victoria
                for ficha in fichas_lado:
                    ficha.canvas.itemconfig(ficha.id, image=img_win)
                # Opcional: puedes limpiar la cuadrícula o mostrar un mensaje aquí
                # self.canvas.delete("all")  # Si quieres limpiar todo
                # messagebox.showinfo("¡Victoria!", f"¡{lado} ha ganado!")
                break  # Solo un lado puede ganar a la vez
