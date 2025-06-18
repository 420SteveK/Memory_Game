import tkinter as tk
import os
import random
import Gear
from login2 import *
import GUI


if __name__ == "__main__":
    try:
        available_fonts = set(tkfont.families())
        if "Poppins" not in available_fonts:
            pass  # Puedes poner aquí lógica para usar otra fuente si lo deseas
    except Exception:
        pass

    app = SakuraLogin()
    app.mainloop()
