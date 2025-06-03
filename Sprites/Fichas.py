class Fichas:
    def __init__(self, Jugador_Pert, Estado, Color, Descubierto, X, Y):
        self.Jugador_Pert = Jugador_Pert
        self.Estado = Estado
        self.Color = Color
        self.Descubierto = Descubierto
        self.X = X
        self.Y = Y

    def CrearFicha(self):
        print("Hello")

    def CambiarEstado(self, Nuevo_Estado):


FichaX01 = Fichas("Jugador1", "Oculta", "Ficha01", "No_Suma")
FichaO01 = Fichas("Jugador1", "Oculta", "Ficha01", "No_Suma")
FichaX02 = Fichas("Jugador1", "Oculta", "Ficha02", "No_Suma")
FichaO02 = Fichas("Jugador1", "Oculta", "Ficha02", "No_Suma")

FichaX01 = Fichas("Jugador2", "Oculta", "Ficha01", "No_Suma")
FichaO01 = Fichas("Jugador2", "Oculta", "Ficha01", "No_Suma")
FichaX02 = Fichas("Jugador2", "Oculta", "Ficha02", "No_Suma")
FichaO02 = Fichas("Jugador2", "Oculta", "Ficha02", "No_Suma")
