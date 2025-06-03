class Gear:
    def __init__(self, nombre, tipo):
        self.nombre = nombre
        self.tipo = tipo

    def mostrar_info(self):
        print(f"Nombre: {self.nombre}, Tipo: {self.tipo}")