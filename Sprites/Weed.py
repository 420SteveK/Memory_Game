import tkinter as tk


class Moneda:
    def __init__(self, master, archivo="monedas.txt"):
        self.master = master
        self.archivo = archivo
        self.monedas = self.cargar_monedas()
        self.label = tk.Label(master, text=f"Monedas: {self.monedas}", font=(
            "Arial", 14), bg="#fff", fg="#ffb300")
        self.label.place(relx=1.0, y=10, anchor="ne")
        self.actualizar_label_periodicamente()  # Inicia el refresco automático

    def cargar_monedas(self):
        try:
            with open(self.archivo, "r", encoding="utf-8") as f:
                return int(f.read().strip())
        except (FileNotFoundError, ValueError):
            return 0

    def guardar_monedas(self):
        with open(self.archivo, "w", encoding="utf-8") as f:
            f.write(str(self.monedas))

    def actualizar_monedas(self, cantidad):
        self.monedas = cantidad
        self.label.config(text=f"Monedas: {self.monedas}")
        self.guardar_monedas()

    def calcular_monedas(self, cantidad):
        self.actualizar_monedas(self.monedas + cantidad)

    def actualizar_label_periodicamente(self):
        # Recarga el valor desde el archivo y actualiza el label cada 500 ms
        monedas_actual = self.cargar_monedas()
        if monedas_actual != self.monedas:
            self.monedas = monedas_actual
            self.label.config(text=f"Monedas: {self.monedas}")
        self.master.after(500, self.actualizar_label_periodicamente)
