class Jugador:
    def __init__(self, nombre, ):
        self.nombre = nombre
        self.puntaje = 0
        self.intentos = 0

    def aumentaIntentos(self):
        self.intentos += 1

    def agregarPuntaje(self, parejas):
        self.puntaje += parejas

    def reiniciar(self):
        self.puntaje = 0
        self.intentos = 0
