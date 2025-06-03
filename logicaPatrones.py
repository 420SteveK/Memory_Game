"""En esta clase se tiene la logica par el modo patrones """
import random

class LogicaPatrones:
    def __init__(self, opciones=None):
        if opciones is None:
            self.opciones = ['rojo', 'verde', 'azul', 'amarillo']
        else:
            self.opciones = opciones
        self.nivel = 1
        self.patron_actual = []
        self.generar_nuevo_patron()

    def generarNuevoPatron(self):
        #Genera un patron aleatorio dependiendo del nivel
        self.patron_actual = [random.choice(self.opciones) for _ in range(self.nivel)]

    def getPatronActual(self):
        #Regresa una copia del patron actual
        return list(self.patron_actual)
    
    def verificarPatron(self,intento):
        #Verifica si el intento del jugador coincide con el patron actual
        return intento == self.patron_actual
    
    def siguienteNivel (self):
        #Crea nuevo patron para el siguiente nivel
        self.nivel +=1
        self.generarNuevoPatron()

    def reiniciarJuego(self):
        #Regresa al nivel1
        self.nivel =1
        self.generarNuevoPatron