import tkinter as tk
from tkinter import messagebox
from logicaPatrones import PatternMemoryLogic
from Weed import Moneda


class PatternMemoryGUI:
    BG_COLOR = "#080008"           # Fondo oscuro
    BUTTON_DEFAULT_COLOR = "#222222"
    BUTTON_HIGHLIGHT_COLOR = "#ff4da6"  # Rosa brillante
    BUTTON_ACTIVE_USER = "#16f4f4"      # Cian neón al presionar
    TEXT_COLOR = "#ff4da6"

    def __init__(self, master):
        self.master = master
        master.title("Memory Pattern Game - Cyberpunk Mode")
        master.configure(bg=self.BG_COLOR)
        master.resizable(False, False)
        master.geometry("403x500")

        self.logic = PatternMemoryLogic()
        self.logic.on_show_pattern_callback = self.highlight_button
        self.logic.on_hide_pattern_callback = self.unhighlight_button
        self.logic.on_info_update_callback = self.update_info_label
        self.logic.on_fail_callback = self.on_fail
        self.logic.on_success_callback = self.on_success
        self.logic.on_enable_input_callback = self.enable_buttons
        self.logic.on_disable_input_callback = self.disable_buttons

        self.buttons = []

        self.info_label = tk.Label(
            master,
            text="Click Start Game to begin",
            font=("Inter", 14, "bold"),
            fg=self.TEXT_COLOR,
            bg=self.BG_COLOR
        )
        self.info_label.grid(
            row=1, column=0, columnspan=self.logic.GRID_SIZE, pady=(10, 20)
        )

        self.create_grid()
        # Deshabilita los botones directamente al iniciar
        self.disable_buttons(direct=True)

        self.start_button = tk.Button(
            master,
            text="Start Game",
            font=("Inter", 12, "bold"),
            fg=self.TEXT_COLOR,
            bg="#222",
            command=self.start_game
        )
        self.start_button.grid(
            row=0, column=0, columnspan=self.logic.GRID_SIZE, pady=(10, 0)
        )

        self.monedas = Moneda(master)

    def create_grid(self):
        for r in range(self.logic.GRID_SIZE):
            row = []
            for c in range(self.logic.GRID_SIZE):
                btn = tk.Button(
                    self.master,
                    width=5,
                    height=2,
                    bg=self.BUTTON_DEFAULT_COLOR,
                    command=lambda r=r, c=c: self.on_button_press(r, c)
                )
                btn.grid(row=r+2, column=c, padx=2, pady=2)
                row.append(btn)
            self.buttons.append(row)

    def start_game(self):
        self.start_button.config(state="disabled")
        self.logic.start_game()

    def highlight_button(self, r, c):
        def _highlight():
            self.buttons[r][c].config(bg=self.BUTTON_HIGHLIGHT_COLOR)
        self.master.after(0, _highlight)

    def unhighlight_button(self, r, c):
        def _unhighlight():
            self.buttons[r][c].config(bg=self.BUTTON_DEFAULT_COLOR)
        self.master.after(0, _unhighlight)

    def on_button_press(self, r, c):
        if not self.logic.input_enabled:
            return
        self.flash_button_active(r, c)
        self.logic.user_press(r, c)

    def flash_button_active(self, r, c):
        def _flash():
            self.buttons[r][c].config(bg=self.BUTTON_ACTIVE_USER)
            self.master.after(200, lambda: self.buttons[r][c].config(
                bg=self.BUTTON_DEFAULT_COLOR))
        self.master.after(0, _flash)

    def update_info_label(self, message):
        def _update():
            self.info_label.config(text=message)
        self.master.after(0, _update)

    def on_fail(self, message):
        def _fail():
            messagebox.showinfo("Game Over", message)
            self.start_button.config(state="normal")
            self.disable_buttons()
        self.master.after(0, _fail)

    def on_success(self, level):
        def _success():
            self.monedas.calcular_monedas(1)
            messagebox.showinfo(
                "Level Complete", f"¡Bien hecho! Nivel {level} completado.")
            self.start_button.config(state="normal")
            self.disable_buttons()
        self.master.after(0, _success)

    def enable_buttons(self):
        def _enable():
            for row in self.buttons:
                for btn in row:
                    btn.config(state="normal")
        self.master.after(0, _enable)

    def disable_buttons(self, direct=False):
        def _disable():
            for row in self.buttons:
                for btn in row:
                    btn.config(state="disabled")
        if direct:
            _disable()
        else:
            self.master.after(0, _disable)

# Recuerda: No ejecutes este archivo directamente, siempre desde el menú principal.
