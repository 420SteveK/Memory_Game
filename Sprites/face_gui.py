import tkinter as tk
from tkinter import simpledialog, messagebox, font as tkfont
import cv2
import os
import numpy as np
import threading
import time as time
USERS_DIR = "users_lbph"

# === Registrar rostro con OpenCV LBPH ===


class Register_Face:
    def __init__(self, ventana):
        self.ventana = ventana

    def register_face_gui(self):
        name = simpledialog.askstring(
            "Registro", "Ingresa tu nombre de usuario:")
        if not name:
            messagebox.showerror("Error", "Nombre inválido.")
            return

        name = name.strip().lower()

        if not os.path.exists(USERS_DIR):
            os.makedirs(USERS_DIR)

        cap = cv2.VideoCapture(0)
        face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
        count = 0
        faces_data = []

        messagebox.showinfo(
            "Instrucción", "Mira a la cámara. Se capturarán 10 imágenes automáticamente.")

        while True:
            ret, frame = cap.read()
            if not ret:
                messagebox.showerror(
                    "Error", "No se pudo acceder a la cámara.")
                break

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)

            for (x, y, w, h) in faces:
                face = gray[y:y+h, x:x+w]
                face_resized = cv2.resize(face, (100, 100))
                faces_data.append(face_resized)
                count += 1

                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                cv2.putText(frame, f"Captura {count}/10", (x, y - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

            cv2.imshow("Registrando rostro", frame)

            if count >= 10 or cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

        if faces_data:
            # Promediar las 10 capturas
            mean_face = np.mean(faces_data, axis=0)
            filepath = os.path.join(USERS_DIR, f"{name}.npy")
            np.save(filepath, mean_face)
            messagebox.showinfo(
                "Éxito", f"Rostro guardado correctamente como '{filepath}'")
        else:
            messagebox.showwarning(
                "Sin capturas", "No se capturó ningún rostro.")

    # === Entrenamiento del modelo LBPH ===

    def train_lbph_model(self):
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        faces = []
        labels = []
        label_map = {}
        label_count = 0

        for file in os.listdir(USERS_DIR):
            if file.endswith(".jpg"):
                path = os.path.join(USERS_DIR, file)
                img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
                name = file.split("_")[0]
                if name not in label_map:
                    label_map[name] = label_count
                    label_count += 1
                faces.append(img)
                labels.append(label_map[name])

        if not faces:
            return None, {}

        recognizer.train(faces, np.array(labels))
        return recognizer, {v: k for k, v in label_map.items()}

    def load_known_faces(self):
        encodings = []
        names = []

        for file in os.listdir(USERS_DIR):
            if file.endswith(".npy"):
                path = os.path.join(USERS_DIR, file)
                encoding = np.load(path).flatten()
                encodings.append(encoding)
                names.append(os.path.splitext(file)[0])

        return encodings, names
    # === Login con rostro ===
    # === Login con rostro automático usando OpenCV ===

    def login_with_face_gui(self):
        def login_thread():
            try:
                known_encodings, known_names = self.load_known_faces()  # <--- usa self aquí
                if not known_encodings:
                    messagebox.showerror(
                        "Error", "No hay rostros registrados.")
                    return

                cap = cv2.VideoCapture(0)
                face_cascade = cv2.CascadeClassifier(
                    cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

                start_time = time.time()
                recognized = False

                while True:
                    ret, frame = cap.read()
                    if not ret:
                        messagebox.showerror(
                            "Error", "No se pudo acceder a la cámara.")
                        break

                    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

                    for (x, y, w, h) in faces:
                        face = cv2.resize(
                            gray[y:y+h, x:x+w], (100, 100)).flatten()
                        distances = [np.linalg.norm(face - known_enc)
                                     for known_enc in known_encodings]
                        min_distance = min(distances)
                        best_match_index = np.argmin(distances)

                        if min_distance < 2000:
                            name = known_names[best_match_index]
                            label = f"Reconocido: {name}"
                            color = (0, 255, 0)
                            recognized = True
                        else:
                            label = "Desconocido"
                            color = (0, 0, 255)

                        # Dibujar recuadro y etiqueta
                        cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
                        cv2.putText(frame, label, (x, y - 10),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)

                        if recognized:
                            cv2.imshow("Login con rostro", frame)
                            cv2.waitKey(1000)
                            messagebox.showinfo(
                                "Login exitoso", f"Bienvenido, {name}!")
                            cap.release()
                            cv2.destroyAllWindows()
                            return

                    cv2.imshow("Login con rostro", frame)

                    if time.time() - start_time > 15:
                        break

                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break

                cap.release()
                cv2.destroyAllWindows()
                messagebox.showinfo(
                    "Login fallido", "No se reconoció ningún rostro o se canceló el login.")
            except Exception as e:
                messagebox.showerror("Error inesperado", str(e))

        threading.Thread(target=login_thread).start()

    # === Interfaz Tkinter ===

    def main_gui(self):
        root = tk.Tk()
        root.title("Sistema de Reconocimiento Facial (LBPH)")
        root.geometry("400x320")
        root.configure(bg="#000000")

        # Frame estilo tarjeta
        card = tk.Frame(root, bg="white", bd=2, relief="groove")
        card.place(relx=0.5, rely=0.5, anchor="center", width=340, height=260)

        tk.Label(card, text="Reconocimiento Facial\n(OpenCV + LBPH)",
                 font=("Arial", 15, "bold"), bg="white", fg="#333").pack(pady=(18, 10))

        tk.Button(card, text="Registrar nuevo rostro",
                  command=register_face_gui, width=28, height=2, bg="#4CAF50", fg="white", bd=0, font=("Arial", 11, "bold")).pack(pady=8)
        tk.Button(card, text="Iniciar sesión con rostro",
                  command=login_with_face_gui, width=28, height=2, bg="#2196F3", fg="white", bd=0, font=("Arial", 11, "bold")).pack(pady=8)
        tk.Button(card, text="Salir", command=root.destroy,
                  width=28, height=2, bg="#f44336", fg="white", bd=0, font=("Arial", 11, "bold")).pack(pady=8)

        root.mainloop()

    if __name__ == "__main__":
        if not os.path.exists(USERS_DIR):
            os.makedirs(USERS_DIR)


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

        # Instancia de la lógica facial
        self.logic = Register_Face(self)

        card = tk.Frame(self, bg="#2c2c2c", bd=0, highlightthickness=0)
        card.place(relx=0.5, rely=0.5, anchor="center", width=370, height=320)

        tk.Label(card, text="Reconocimiento Facial\n(OpenCV + LBPH)",
                 font=self.font_large, bg="#2c2c2c", fg="#ffc0cb").pack(pady=(30, 18))

        tk.Button(card, text="Registrar nuevo rostro",
                  font=self.font_button, bg="#ff69b4", fg="#1a1a1a",
                  activebackground="#ff1493", activeforeground="#fff",
                  relief="flat", width=28, height=2,
                  command=self.logic.register_face_gui).pack(pady=10)

        tk.Button(card, text="Iniciar sesión con rostro",
                  font=self.font_button, bg="#ffc0cb", fg="#1a1a1a",
                  activebackground="#ff69b4", activeforeground="#fff",
                  relief="flat", width=28, height=2,
                  command=self.logic.login_with_face_gui).pack(pady=10)

        tk.Button(card, text="Salir", font=self.font_button,
                  bg="#1a1a1a", fg="#ffc0cb", activebackground="#ff1493",
                  activeforeground="#fff", relief="flat", width=28, height=2,
                  command=self.destroy).pack(pady=10)

    def register_face(self):
        messagebox.showinfo("Registrar rostro",
                            "Función de registro de rostro aquí.")

    def login_face(self):
        face_window = face_gui.face_gui(self)
        face_window.grab_set()  # Hace modal la ventana
