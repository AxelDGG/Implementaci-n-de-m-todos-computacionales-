import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from regex_to_nfa import regex_to_nfa
from nfa_to_dfa import nfa_to_dfa
from visualize_automata import draw_dfa

class AFDApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Generador de AFD 🚀")
        self.geometry("800x700")

        # ——— Entradas ———
        frame_in = tk.Frame(self)
        frame_in.pack(pady=10)

        tk.Label(frame_in, text="Alfabeto Σ (ej: a,b,c):").grid(row=0, column=0, sticky="e")
        self.ent_sigma = tk.Entry(frame_in, width=40)
        self.ent_sigma.grid(row=0, column=1, padx=5)

        tk.Label(frame_in, text="Regex (. para concat):").grid(row=1, column=0, sticky="e")
        self.ent_regex = tk.Entry(frame_in, width=40)
        self.ent_regex.grid(row=1, column=1, padx=5)

        btn_gen = tk.Button(frame_in, text="🔧 Generar AFD", command=self.generar_dfa)
        btn_gen.grid(row=2, column=0, columnspan=2, pady=8)

        # ——— Lugar para mostrar el gráfico ———
        self.lbl_img = tk.Label(self)
        self.lbl_img.pack()

        # ——— Pruebas de cadena ———
        frame_test = tk.Frame(self)
        frame_test.pack(pady=10)

        tk.Label(frame_test, text="Palabra a probar:").grid(row=0, column=0)
        self.ent_test = tk.Entry(frame_test, width=30)
        self.ent_test.grid(row=0, column=1, padx=5)
        self.btn_test = tk.Button(frame_test, text="▶ Probar", state="disabled", command=self.probar_palabra)
        self.btn_test.grid(row=0, column=2)

        self.lbl_res = tk.Label(self, text="", font=("Arial", 16))
        self.lbl_res.pack(pady=5)

        # ——— Datos internos ———
        self.dfa_trans = {}
        self.dfa_start = 0
        self.dfa_accept = set()
        self.photo = None

    def generar_dfa(self):
        σ = [s.strip() for s in self.ent_sigma.get().split(",") if s.strip()]
        regex = self.ent_regex.get().strip()
        if not σ or not regex:
            messagebox.showerror("Error", "Debe llenar alfabeto y expresión.")
            return

        # Generamos AFN → AFD
        nfa = regex_to_nfa(regex)
        self.dfa_trans, self.dfa_start, self.dfa_accept = nfa_to_dfa(nfa, σ)

        # Dibujamos y cargamos la imagen
        nombre = "resultado_dfa"
        draw_dfa(self.dfa_trans, self.dfa_start, self.dfa_accept, filename=nombre)
        img = Image.open(f"{nombre}.png").resize((700,400), Image.ANTIALIAS)
        self.photo = ImageTk.PhotoImage(img)
        self.lbl_img.config(image=self.photo)

        # Activamos la sección de prueba
        self.btn_test.config(state="normal")
        self.lbl_res.config(text="")

    def probar_palabra(self):
        w = self.ent_test.get().strip()
        cur = self.dfa_start
        for c in w:
            cur = self.dfa_trans.get(cur, {}).get(c)
            if cur is None:
                break
        if cur in self.dfa_accept:
            self.lbl_res.config(text=f"'{w}': ACEPTADA ✅", fg="green")
        else:
            self.lbl_res.config(text=f"'{w}': RECHAZADA ❌", fg="red")

if __name__ == "__main__":
    # Asegúrate de haber instalado:
    # pip install graphviz pillow
    app = AFDApp()
    app.mainloop()
