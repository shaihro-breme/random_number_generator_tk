import tkinter as tk
from tkinter import ttk, messagebox
from random import randint, uniform

LANG = {
    "en": {
        "title": "Random Number Generator",
        "label_start": "Start number:",
        "label_end": "End number:",
        "label_type": "Number type:",
        "type_int": "Integer",
        "type_dec": "Decimal",
        "label_decimals": "Decimals (only for decimal):",
        "btn_generate": "Generate",
        "btn_clear": "Clear",
        "btn_history": "History",
        "btn_exit": "Exit",
        "result": "Result:",
        "err_invalid": "Please enter valid numbers.",
        "err_decimals": "Decimals must be a non-negative integer.",
        "history_title": "Generated Numbers History",
        "history_empty": "(history is empty)",
        "lang_label": "Language:",
        "btn_copy": "Copy",
    },
    "es": {
        "title": "Generador de Números Aleatorios",
        "label_start": "Número inicial:",
        "label_end": "Número final:",
        "label_type": "Tipo de número:",
        "type_int": "Entero",
        "type_dec": "Con coma",
        "label_decimals": "Decimales (solo para decimales):",
        "btn_generate": "Generar",
        "btn_clear": "Limpiar",
        "btn_history": "Historial",
        "btn_exit": "Salir",
        "result": "Resultado:",
        "err_invalid": "Por favor ingrese números válidos.",
        "err_decimals": "Los decimales deben ser un entero no negativo.",
        "history_title": "Historial de Números Generados",
        "history_empty": "(historial vacío)",
        "lang_label": "Idioma:",
        "btn_copy": "Copiar",
    }
}

def normalize_number_text(text: str) -> str:
    if text is None:
        return ""
    return text.strip().replace(",", ".")

def parse_float_safe(text: str):
    normalized = normalize_number_text(text)
    return float(normalized)

def parse_int_safe(text: str):
    normalized = normalize_number_text(text)
    return int(float(normalized))

class RandomGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.lang = "en"
        self.history = []
        self.history_window = None

        # UI variables
        self.var_start = tk.StringVar()
        self.var_end = tk.StringVar()
        self.type_var = tk.StringVar(value="Integer")
        self.var_decimals = tk.StringVar(value="2")
        self.var_result = tk.StringVar(value=LANG[self.lang]["result"])
        self.lang_var = tk.StringVar(value=self.lang)

        self.build_ui()
        self.update_texts()

    def build_ui(self):
        root = self.root
        root.title(LANG[self.lang]["title"])
        root.resizable(False, False)
        root.geometry("420x420")

        top_frame = ttk.Frame(root)
        top_frame.pack(fill="x", pady=8, padx=10)
        ttk.Label(top_frame, text=LANG[self.lang]["lang_label"]).pack(side="left")
        lang_menu = ttk.OptionMenu(top_frame, self.lang_var, self.lang, "en", "es", command=self.on_language_change)
        lang_menu.pack(side="left", padx=6)

        form = ttk.Frame(root)
        form.pack(fill="both", expand=True, padx=10)

        ttk.Label(form, text="").pack()  # spacer

        self.lbl_start = ttk.Label(form, text="")
        self.lbl_start.pack(anchor="w")
        self.entry_start = ttk.Entry(form, textvariable=self.var_start)
        self.entry_start.pack(fill="x")

        self.lbl_end = ttk.Label(form, text="")
        self.lbl_end.pack(anchor="w", pady=(8,0))
        self.entry_end = ttk.Entry(form, textvariable=self.var_end)
        self.entry_end.pack(fill="x")

        self.lbl_type = ttk.Label(form, text="")
        self.lbl_type.pack(anchor="w", pady=(8,0))
        type_frame = ttk.Frame(form)
        type_frame.pack(anchor="w")
        self.rb_int = ttk.Radiobutton(type_frame, text="", variable=self.type_var, value="Integer")
        self.rb_int.pack(side="left")
        self.rb_dec = ttk.Radiobutton(type_frame, text="", variable=self.type_var, value="Decimal")
        self.rb_dec.pack(side="left", padx=8)

        self.lbl_decimals = ttk.Label(form, text="")
        self.lbl_decimals.pack(anchor="w", pady=(8,0))
        self.entry_decimals = ttk.Entry(form, textvariable=self.var_decimals, width=6)
        self.entry_decimals.pack(anchor="w")

        btn_frame = ttk.Frame(form)
        btn_frame.pack(pady=12)
        self.btn_generate = ttk.Button(btn_frame, text="", command=self.on_generate)
        self.btn_generate.pack(side="left", padx=6)
        self.btn_clear = ttk.Button(btn_frame, text="", command=self.on_clear)
        self.btn_clear.pack(side="left", padx=6)
        self.btn_history = ttk.Button(btn_frame, text="", command=self.open_history)
        self.btn_history.pack(side="left", padx=6)
        self.btn_exit = ttk.Button(btn_frame, text="", command=root.destroy)
        self.btn_exit.pack(side="left", padx=6)

        self.lbl_result = ttk.Label(form, textvariable=self.var_result, font=("Arial", 12, "bold"))
        self.lbl_result.pack(pady=8)

        self.btn_copy = ttk.Button(form, text="", command=self.copy_result)
        self.btn_copy.pack(pady=4)

    def on_language_change(self, new_value=None):
        val = self.lang_var.get()
        if val not in LANG:
            return
        self.lang = val
        self.update_texts()

    def update_texts(self):
        t = LANG[self.lang]
        self.root.title(t["title"])
        self.lbl_start.config(text=t["label_start"])
        self.lbl_end.config(text=t["label_end"])
        self.lbl_type.config(text=t["label_type"])
        self.rb_int.config(text=t["type_int"])
        self.rb_dec.config(text=t["type_dec"])
        self.lbl_decimals.config(text=t["label_decimals"])
        self.btn_generate.config(text=t["btn_generate"])
        self.btn_clear.config(text=t["btn_clear"])
        self.btn_history.config(text=t["btn_history"])
        self.btn_exit.config(text=t["btn_exit"])
        self.btn_copy.config(text=t["btn_copy"])
        current = self.var_result.get()
        parts = current.split(":", 1)
        suffix = parts[1].strip() if len(parts) > 1 else ""
        if suffix:
            self.var_result.set(f"{t['result']} {suffix}")
        else:
            self.var_result.set(t["result"])

    def on_generate(self):
        t = LANG[self.lang]
        try:
            start_text = normalize_number_text(self.var_start.get())
            end_text = normalize_number_text(self.var_end.get())

            start = float(start_text)
            end = float(end_text)
            if start > end:
                start, end = end, start

            if self.type_var.get() == "Integer":
                start_i = int(float(start))
                end_i = int(float(end))
                if start_i > end_i:
                    start_i, end_i = end_i, start_i
                number = randint(start_i, end_i)
                display = str(number)
            else:
                try:
                    decimals = int(float(normalize_number_text(self.var_decimals.get())))
                    if decimals < 0:
                        raise ValueError
                except ValueError:
                    messagebox.showerror(t["err_decimals"], t["err_decimals"])
                    return
                number = uniform(start, end)
                display = f"{round(number, decimals):.{decimals}f}"

            self.var_result.set(f"{t['result']} {display}")
            self.history.append({
                "number": display,
                "start": start,
                "end": end,
                "type": self.type_var.get(),
                "decimals": int(float(normalize_number_text(self.var_decimals.get())))
            })
            if self.history_window and tk.Toplevel.winfo_exists(self.history_window):
                self.refresh_history_window()
        except Exception:
            messagebox.showerror(t["err_invalid"], t["err_invalid"])

    def on_clear(self):
        self.var_start.set("")
        self.var_end.set("")
        self.var_decimals.set("2")
        self.var_result.set(LANG[self.lang]["result"])

    def open_history(self):
        if self.history_window and tk.Toplevel.winfo_exists(self.history_window):
            self.history_window.lift()
            self.refresh_history_window()
            return

        t = LANG[self.lang]
        self.history_window = tk.Toplevel(self.root)
        self.history_window.title(t["history_title"])
        self.history_window.geometry("320x300")
        self.history_window.resizable(False, False)

        frame = ttk.Frame(self.history_window)
        frame.pack(fill="both", expand=True, padx=8, pady=8)

        self.history_listbox = tk.Listbox(frame, height=12)
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=self.history_listbox.yview)
        self.history_listbox.config(yscrollcommand=scrollbar.set)
        self.history_listbox.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        btn_frame = ttk.Frame(self.history_window)
        btn_frame.pack(fill="x", pady=6)
        ttk.Button(btn_frame, text=t["btn_clear"], command=self.clear_history).pack(side="left", padx=6)
        ttk.Button(btn_frame, text=t["btn_exit"], command=self.history_window.destroy).pack(side="right", padx=6)

        self.refresh_history_window()
        self.history_listbox.bind("<Button-1>", self.copy_from_history)
        self.history_listbox.bind("<Double-1>", self.load_seed_from_history)

    def refresh_history_window(self):
        t = LANG[self.lang]
        self.history_listbox.delete(0, tk.END)
        if not self.history:
            self.history_listbox.insert(tk.END, t["history_empty"])
        else:
            for idx, entry in enumerate(self.history, start=1):
                number_text = entry["number"] if isinstance(entry, dict) else str(entry)
                self.history_listbox.insert(tk.END, f"{idx}. {number_text}")

    def clear_history(self):
        self.history.clear()
        if self.history_window and tk.Toplevel.winfo_exists(self.history_window):
            self.refresh_history_window()

    def copy_result(self):
        text = self.var_result.get()
        parts = text.split(":", 1)
        value = parts[1].strip() if len(parts) > 1 else text.strip()
        if not value:
            return
        self.root.clipboard_clear()
        self.root.clipboard_append(value)

        self.var_result.set(f"{LANG[self.lang]['result']} {value} ✓")
        self.root.after(700, lambda: self.var_result.set(f"{LANG[self.lang]['result']} {value}"))

    def copy_from_history(self, event):
        try:
            sel = self.history_listbox.curselection()
            if not sel:
                return
            idx = sel[0]
            if idx >= len(self.history):
                return
            value = str(self.history[idx]["number"])

            self.root.clipboard_clear()
            self.root.clipboard_append(value)

            self.var_result.set(f"{LANG[self.lang]['result']} {value} ✓")
            self.root.after(700, lambda: self.var_result.set(f"{LANG[self.lang]['result']} {value}"))
        except Exception:
            pass

    def load_seed_from_history(self, event):
        try:
            sel = self.history_listbox.curselection()
            if not sel:
                return
            index = sel[0]
            if index >= len(self.history):
                return
            seed = self.history[index]

            if not isinstance(seed, dict):
                return

            self.var_start.set(str(seed["start"]))
            self.var_end.set(str(seed["end"]))
            self.type_var.set(seed["type"])
            self.var_decimals.set(str(seed["decimals"]))

            t = LANG[self.lang]
            self.var_result.set(f"{t['result']} {seed['number']} (config loaded)")
            self.root.after(1200, lambda: self.var_result.set(f"{t['result']} {seed['number']}"))
        except Exception:
            pass

def main():
    root = tk.Tk()
    app = RandomGeneratorApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()