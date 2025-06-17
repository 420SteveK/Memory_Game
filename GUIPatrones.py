import tkinter as tk
from tkinter import messagebox
from logicaPatrones import PatternMemoryLogic

class PatternMemoryGUI:
    BG_COLOR = "#080008"           # dark black/purple
    BUTTON_DEFAULT_COLOR = "#222222"
    BUTTON_HIGHLIGHT_COLOR = "#ff4da6"  # bright pink
    BUTTON_ACTIVE_USER = "#16f4f4"       # neon cyan user press
    TEXT_COLOR = "#ff4da6"
    
    def __init__(self, master):
        self.master = master
        master.title("Memory Pattern Game - Cyberpunk Mode")
        master.configure(bg=self.BG_COLOR)
        master.resizable(False, False)
        
        self.logic = PatternMemoryLogic()
        self.logic.on_show_pattern_callback = self.highlight_button
        self.logic.on_hide_pattern_callback = self.unhighlight_button
        self.logic.on_info_update_callback = self.update_info_label
        self.logic.on_fail_callback = self.on_fail
        self.logic.on_success_callback = self.on_success
        self.logic.on_enable_input_callback = self.enable_buttons
        self.logic.on_disable_input_callback = self.disable_buttons
        
        self.buttons = []
        
        self.info_label = tk.Label(master, text="Click Start Game to begin", font=("Inter", 14, "bold"), fg=self.TEXT_COLOR, bg=self.BG_COLOR)
        self.info_label.grid(row=0, column=0, columnspan=self.logic.GRID_SIZE, pady=(10,20))
        
        self.create_grid()
        
        self.start_button = tk.Button(master, text="Start Game", command=self.start_game, font=("Inter", 12, "bold"),
                                      bg="#ff66cc", fg="#111", activebackground="#ff66cc", relief="raised",
                                      padx=10, pady=5)
        self.start_button.grid(row=self.logic.GRID_SIZE+1, column=0, columnspan=self.logic.GRID_SIZE, pady=(15,20))
        self.disable_buttons()
    
    def create_grid(self):
        for r in range(self.logic.GRID_SIZE):
            row_buttons = []
            for c in range(self.logic.GRID_SIZE):
                btn = tk.Button(self.master, bg=self.BUTTON_DEFAULT_COLOR, activebackground=self.BUTTON_HIGHLIGHT_COLOR,
                                width=5, height=3, bd=2, relief="ridge",
                                command=lambda r=r, c=c: self.on_button_press(r, c))
                btn.grid(row=r+1, column=c, padx=4, pady=4)
                row_buttons.append(btn)
            self.buttons.append(row_buttons)
    
    def start_game(self):
        self.start_button.config(state="disabled")
        self.logic.start_game()
    
    def highlight_button(self, r, c):
        # Highlight pattern button with pink color
        def _highlight():
            self.buttons[r][c].config(bg=self.BUTTON_HIGHLIGHT_COLOR)
        self.master.after(0, _highlight)
    
    def unhighlight_button(self, r, c):
        # Remove highlight, restore default color
        def _unhighlight():
            self.buttons[r][c].config(bg=self.BUTTON_DEFAULT_COLOR)
        self.master.after(0, _unhighlight)
    
    def on_button_press(self, r, c):
        # When user clicks grid button
        if self.logic.input_enabled:
            self.flash_button_active(r, c)
            self.logic.user_press(r, c)
    
    def flash_button_active(self, r, c):
        btn = self.buttons[r][c]
        original = btn.cget("bg")
        btn.config(bg=self.BUTTON_ACTIVE_USER)
        self.master.after(300, lambda: btn.config(bg=original))
    
    def update_info_label(self, message):
        def _update():
            self.info_label.config(text=message)
        self.master.after(0, _update)
    
    def on_fail(self, message):
        def _fail_handler():
            messagebox.showinfo("Try Again!", message)
            self.info_label.config(text="Game Over! Click Start Game to try again.")
            self.start_button.config(state="normal")
            self.disable_buttons()
        self.master.after(0, _fail_handler)
    
    def on_success(self, level):
        def _success_handler():
            messagebox.showinfo("Success!", f"Great! You've completed level {level}. Next level loading...")
            self.update_info_label(f"Level {level+1}: Watch the pattern...")
        self.master.after(0, _success_handler)
    
    def enable_buttons(self):
        def _enable():
            for row in self.buttons:
                for btn in row:
                    btn.config(state="normal")
        self.master.after(0, _enable)
    
    def disable_buttons(self):
        def _disable():
            for row in self.buttons:
                for btn in row:
                    btn.config(state="disabled")
        self.master.after(0, _disable)


if __name__ == "__main__":
    root = tk.Tk()
    app = PatternMemoryGUI(root)
    root.mainloop()

