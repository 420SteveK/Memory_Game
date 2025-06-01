"""
Se define la clase jugador
atributos:
"""

class Jugador:
    def __init__(self, nombre):
        #define atributos
        self.nombre = nombre
        self.puntaje = 0
        self.intentos = 0
    
    def mostrar(self):
        return f"Jugador: {self.nombre}, Puntaje: {self.puntaje}, Intentos: {self.intentos}"

    def aumentaIntentos (self):
        #Acumula los intentos que le toma ganar
        self.intentos += 1

    def agregarPuntaje(self,parejas):
        #Aniade las parejas acertadas
        self.puntaje += parejas

    def reiniciar(self):
        #Reinicia el puntaje y el numero de intentos
        self.puntaje = 0
        self.intentos = 0

jugador1= Jugador('Avril')
jugador1.mostrar