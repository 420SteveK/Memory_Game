from tkinter import messagebox, font as tkfont
import tkinter as tk
from tkinter import font as tkfont
from tkinter import messagebox, simpledialog
import face_gui


class SakuraLogin(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sakura Login - Spotify Inspired")
        self.geometry("430x520")
        self.configure(bg="#1a1a1a")
        self.resizable(False, False)

        # Set up fonts
        self.font_large = tkfont.Font(family="Poppins", size=24, weight="bold")
        self.font_medium = tkfont.Font(family="Poppins", size=12)
        self.font_button = tkfont.Font(
            family="Poppins", size=11, weight="bold")

        # Container frame with slight glassmorphism effect
        self.container = tk.Frame(
            self, bg="#2c2c2c", bd=0, highlightthickness=0)
        self.container.place(relx=0.5, rely=0.5,
                             anchor="center", width=370, height=460)

        # Title label
        self.title_label = tk.Label(
            self.container,
            text="Welcome back",
            font=self.font_large,
            fg="#ffc0cb",
            bg="#2c2c2c"
        )
        self.title_label.pack(pady=(40, 30))

        # Username entry with label
        self.user_label = tk.Label(
            self.container, text="Username", font=self.font_medium, fg="#ffc0cb", bg="#2c2c2c")
        self.user_label.pack(anchor="w", padx=40)
        self.user_entry = tk.Entry(self.container, font=self.font_medium, bg="#1a1a1a", fg="#ffc0cb", insertbackground="#ffc0cb",
                                   relief="flat", bd=2, justify="left", highlightthickness=0, width=28)
        self.user_entry.pack(pady=(2, 20), padx=40, ipady=8)

        # Password entry with label
        self.pass_label = tk.Label(
            self.container, text="Password", font=self.font_medium, fg="#ffc0cb", bg="#2c2c2c")
        self.pass_label.pack(anchor="w", padx=40)
        self.pass_entry = tk.Entry(self.container, font=self.font_medium, bg="#1a1a1a", fg="#ffc0cb", insertbackground="#ffc0cb",
                                   relief="flat", bd=2, justify="left", show="*", highlightthickness=0, width=28)
        self.pass_entry.pack(pady=(2, 30), padx=40, ipady=8)

        # Buttons frame
        self.buttons_frame = tk.Frame(self.container, bg="#2c2c2c")
        self.buttons_frame.pack(pady=(0, 20))

        # Accept button
        self.accept_btn = tk.Button(
            self.buttons_frame,
            text="Accept",
            font=self.font_button,
            bg="#ffb6c1",
            fg="#1a1a1a",
            activebackground="#ff69b4",
            activeforeground="#fff",
            relief="flat",
            width=14,
            command=self.accept
        )
        self.accept_btn.grid(row=0, column=0, padx=7, pady=6)
        self._add_hover(self.accept_btn, "#ffb6c1", "#ff69b4")

        # Exit button
        self.exit_btn = tk.Button(
            self.buttons_frame,
            text="Exit",
            font=self.font_button,
            bg="#ffc0cb",
            fg="#1a1a1a",
            activebackground="#ff69b4",
            activeforeground="#fff",
            relief="flat",
            width=14,
            command=self.exit_app
        )
        self.exit_btn.grid(row=0, column=1, padx=7, pady=6)
        self._add_hover(self.exit_btn, "#ffc0cb", "#ff1493")

        # Register button for face registration
        self.register_btn = tk.Button(
            self.container,
            text="Ingresar mediante reconocimiento facial",
            font=self.font_button,
            bg="#ff69b4",
            fg="#1a1a1a",
            activebackground="#ff1493",
            activeforeground="#fff",
            relief="flat",
            width=30,
            command=self.login_face  # Usa el método que ya tienes
        )
        self.register_btn.pack(pady=(10, 12))
        self._add_hover(self.register_btn, "#ff69b4", "#ff1493")

        # New Register Credentials button
        self.register_credentials_btn = tk.Button(
            self.container,
            text="Registrar Credenciales",
            font=self.font_button,
            bg="#ff69b4",
            fg="#1a1a1a",
            activebackground="#ff1493",
            activeforeground="#fff",
            relief="flat",
            width=30,
            command=self.register_credentials_popup
        )
        self.register_credentials_btn.pack(pady=(10, 12))
        self._add_hover(self.register_credentials_btn, "#ff69b4", "#ff1493")

        # Login with facial recognition button
        self.face_btn = tk.Button(
            self.container,
            text=" Log in con reconocimiento facial  \U0001F464",
            font=self.font_button,
            bg="#ff69b4",
            fg="#1a1a1a",
            activebackground="#ff1493",
            activeforeground="#fff",
            relief="flat",
            width=30,
            command=self.login_face
        )
        self.face_btn.pack()
        self._add_hover(self.face_btn, "#ff69b4", "#ff1493")

        # Subtle shadow effect using empty label (fake shadow)
        self.shadow_label = tk.Label(
            self.container, bg="#000000", width=50, height=2)
        self.shadow_label.pack(side="bottom", pady=(30, 0))

    def _add_hover(self, button, normal_bg, hover_bg):
        def on_enter(e):
            button['background'] = hover_bg
            button['foreground'] = "#fff"
            button.configure(cursor="hand2")

        def on_leave(e):
            button['background'] = normal_bg
            button['foreground'] = "#1a1a1a"
            button.configure(cursor="")
        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)

    def accept(self):
        username = self.user_entry.get().strip()
        password = self.pass_entry.get().strip()
        if not username or not password:
            messagebox.showwarning(
                "Datos incompletos", "Por favor ingrese su nombre y contrasenia.")
            return

        encontrado = False
        try:
            with open("usuarios.txt", "r", encoding="utf-8") as f:
                for linea in f:
                    try:
                        datos = eval(linea.strip())
                        # datos es una lista de listas: [[usuario, contrasena]]
                        if isinstance(datos, list) and len(datos) > 0 and isinstance(datos[0], list):
                            if datos[0][0] == username and datos[0][1] == password:
                                encontrado = True
                                break
                    except Exception:
                        continue
        except FileNotFoundError:
            messagebox.showerror("Error", "No hay usuarios registrados.")
            return

        if encontrado:
            messagebox.showinfo("Confirmado", f"Bienvenid@, {username}!")
        else:
            messagebox.showerror("Usuario no encontrado",
                                 "Usuario o contraseña incorrectos.")

    def exit_app(self):
        self.destroy()

    def register_face_popup(self):
        # Popup window to simulate face registration
        popup = tk.Toplevel(self)
        popup.title("Registre cara nueva")
        popup.geometry("320x180")
        popup.configure(bg="#2c2c2c")
        popup.resizable(False, False)
        popup.grab_set()  # Modal behavior

        label = tk.Label(popup, text="Ingresa tu nombre para registrar tu cara: ",
                         font=self.font_medium, fg="#ffc0cb", bg="#2c2c2c")
        label.pack(pady=(20, 12))

        name_entry = tk.Entry(popup, font=self.font_medium, bg="#1a1a1a", fg="#ffc0cb", insertbackground="#ffc0cb",
                              relief="flat", bd=2, justify="left", highlightthickness=0, width=25)
        name_entry.pack(pady=(0, 20), ipady=6)
        name_entry.focus()

        def submit():
            name = name_entry.get().strip()
            if not name:
                messagebox.showwarning(
                    "Input Needed", "Por favor ingresa tu nombre.")
                return
            # Here, you might normally trigger actual face registration logic
            messagebox.showinfo(
                "Face Registered", f"Face for '{name}' has been registered successfully.")
            popup.destroy()

        submit_btn = tk.Button(popup, text="Register Face", font=self.font_button,
                               bg="#ff69b4", fg="#1a1a1a", activebackground="#ff1493", activeforeground="#fff",
                               relief="flat", width=24, command=submit)
        submit_btn.pack()

        def on_close():
            popup.destroy()
        popup.protocol("WM_DELETE_WINDOW", on_close)

    def register_credentials_popup(self):
        # Popup window for registering credentials
        popup = tk.Toplevel(self)
        popup.title("Registrar Credenciales")
        popup.geometry("320x240")
        popup.configure(bg="#2c2c2c")
        popup.resizable(False, False)
        popup.grab_set()  # Modal behavior

        label_username = tk.Label(popup, text="Ingresa tu nombre de usuario: ",
                                  font=self.font_medium, fg="#ffc0cb", bg="#2c2c2c")
        label_username.pack(pady=(20, 12))

        username_entry = tk.Entry(popup, font=self.font_medium, bg="#1a1a1a", fg="#ffc0cb", insertbackground="#ffc0cb",
                                  relief="flat", bd=2, justify="left", highlightthickness=0, width=25)
        username_entry.pack(pady=(0, 10), ipady=6)

        label_password = tk.Label(
            popup, text="Ingresa tu contraseña: ", font=self.font_medium, fg="#ffc0cb", bg="#2c2c2c")
        label_password.pack(pady=(10, 12))

        password_entry = tk.Entry(popup, font=self.font_medium, bg="#1a1a1a", fg="#ffc0cb", insertbackground="#ffc0cb",
                                  relief="flat", bd=2, justify="left", show="*", highlightthickness=0, width=25)
        password_entry.pack(pady=(0, 20), ipady=6)

        def submit():
            username = username_entry.get().strip()
            password = password_entry.get().strip()
            if not username or not password:
                messagebox.showwarning(
                    "Input Needed", "Por favor ingresa tu nombre de usuario y contraseña.")
                return
            # Guardar en texto plano como matriz
            with open("usuarios.txt", "a", encoding="utf-8") as f:
                f.write(str([[username, password]]) + "\n")
            messagebox.showinfo("Credenciales Registradas",
                                f"Credenciales para '{username}' han sido registradas exitosamente.")
            popup.destroy()

        submit_btn = tk.Button(popup, text="Registrar Credenciales", font=self.font_button,
                               bg="#ff69b4", fg="#1a1a1a", activebackground="#ff1493", activeforeground="#fff",
                               relief="flat", width=24, command=submit)
        submit_btn.pack()

        def on_close():
            popup.destroy()
        popup.protocol("WM_DELETE_WINDOW", on_close)

    def login_face(self):
        # Open the facial recognition window
        face_window = face_gui.face_gui(self)
        face_window.grab_set()  # Make it modal


if __name__ == "__main__":
    try:
        available_fonts = set(tkfont.families())
        if "Poppins" not in available_fonts:
            pass  # Puedes poner aquí lógica para usar otra fuente si lo deseas
    except Exception:
        pass

    app = SakuraLogin()
    app.mainloop()


class face_gui(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Reconocimiento Facial (LBPH)")
        self.geometry("430x400")
        self.configure(bg="#1a1a1a")
        self.resizable(False, False)

        self.font_large = tkfont.Font(family="Poppins", size=20, weight="bold")
        self.font_button = tkfont.Font(
            family="Poppins", size=11, weight="bold")

        card = tk.Frame(self, bg="#2c2c2c", bd=0, highlightthickness=0)
        card.place(relx=0.5, rely=0.5, anchor="center", width=370, height=320)

        tk.Label(card, text="Reconocimiento Facial\n(OpenCV + LBPH)",
                 font=self.font_large, bg="#2c2c2c", fg="#ffc0cb").pack(pady=(30, 18))

        tk.Button(card, text="Registrar nuevo rostro",
                  font=self.font_button, bg="#ff69b4", fg="#1a1a1a",
                  activebackground="#ff1493", activeforeground="#fff",
                  relief="flat", width=28, height=2,
                  command=self.register_face).pack(pady=10)

        tk.Button(card, text="Iniciar sesión con rostro",
                  font=self.font_button, bg="#ffc0cb", fg="#1a1a1a",
                  activebackground="#ff69b4", activeforeground="#fff",
                  relief="flat", width=28, height=2,
                  command=self.login_face).pack(pady=10)

        tk.Button(card, text="Salir", font=self.font_button,
                  bg="#1a1a1a", fg="#ffc0cb", activebackground="#ff1493",
                  activeforeground="#fff", relief="flat", width=28, height=2,
                  command=self.destroy).pack(pady=10)

    def register_face(self):
        messagebox.showinfo("Registrar rostro",
                            "Función de registro de rostro aquí.")

    def login_face(self):
        messagebox.showinfo(
            "Login rostro", "Función de login con rostro aquí.")
