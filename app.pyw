# Transcriptor de audios - Copyright (C) 2026 jhoel0521
# Licencia: GPL v3 o posterior, con permiso adicional. Ver LICENSE y EXCEPCION-GPL.md.

"""Ventana para transcribir audios con Whisper local.

Abrir con doble clic en "Transcriptor.bat" o:
    .venv\\Scripts\\pythonw.exe app.pyw
"""

import os
import queue
import sys
from pathlib import Path

# El Python de Laragon trae Tcl/Tk en <python>\tcl pero no lo busca ahí; se lo indicamos.
_tcl = Path(sys.base_prefix) / "tcl"
for _var, _dir in (("TCL_LIBRARY", "tcl8.6"), ("TK_LIBRARY", "tk8.6")):
    if _var not in os.environ and (_tcl / _dir).is_dir():
        os.environ[_var] = str(_tcl / _dir)

import threading
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from tkinter.scrolledtext import ScrolledText

from transcribir import (EXTENSIONES, __version__, buscar_audios, cargar_modelo, carpeta_modelos, formato_tiempo,
                         modelo_local, transcribir_audio)

try:
    from tkinterdnd2 import DND_FILES, TkinterDnD
except ImportError:  # sin la librería la ventana funciona igual, solo sin arrastrar y soltar
    TkinterDnD = None

TITULO = f"Transcriptor de audios {__version__}"

MODELOS = {
    "Preciso (large-v3-turbo)": "large-v3-turbo",
    "Rápido (small)": "small",
}


class App:
    def __init__(self, root):
        self.root = root
        self.root.title(TITULO)
        self.root.geometry("820x600")
        self.root.minsize(560, 400)

        self.modelos_cargados = {}
        self.cola = queue.Queue()  # mensajes del hilo de trabajo hacia la ventana
        self.trabajando = False
        self.cancelar = threading.Event()

        self._armar_ventana()
        if hasattr(self.root, "drop_target_register"):
            self.root.drop_target_register(DND_FILES)
            self.root.dnd_bind("<<DropEnter>>", self._al_entrar_arrastre)
            self.root.dnd_bind("<<DropLeave>>", self._al_salir_arrastre)
            self.root.dnd_bind("<<Drop>>", self._al_soltar)
            self.var_estado.set("Selecciona o arrastra aquí uno o varios audios (o una carpeta).")
        self.root.after(100, self._revisar_cola)

    # ---------- interfaz ----------

    def _armar_ventana(self):
        barra = ttk.Frame(self.root, padding=(10, 10, 10, 5))
        barra.pack(fill="x")

        self.btn_abrir = ttk.Button(barra, text="Seleccionar audio...", command=self.seleccionar)
        self.btn_abrir.pack(side="left")

        self.btn_cancelar = ttk.Button(barra, text="Cancelar", command=self.cancelar.set, state="disabled")
        self.btn_cancelar.pack(side="left", padx=(6, 0))

        ttk.Label(barra, text="Modelo:").pack(side="left", padx=(16, 4))
        self.var_modelo = tk.StringVar(value=next(iter(MODELOS)))
        self.combo_modelo = ttk.Combobox(barra, textvariable=self.var_modelo, values=list(MODELOS),
                                         state="readonly", width=24)
        self.combo_modelo.pack(side="left")

        self.var_tiempos = tk.BooleanVar(value=False)
        ttk.Checkbutton(barra, text="Con tiempos", variable=self.var_tiempos).pack(side="left", padx=(12, 0))

        estado = ttk.Frame(self.root, padding=(10, 0, 10, 5))
        estado.pack(fill="x")
        self.var_estado = tk.StringVar(value="Selecciona uno o varios audios para transcribir.")
        ttk.Label(estado, textvariable=self.var_estado).pack(side="left")
        self.progreso = ttk.Progressbar(estado, length=200, maximum=100)
        self.progreso.pack(side="right")

        self.texto = ScrolledText(self.root, wrap="word", font=("Segoe UI", 11), undo=True)
        self.texto.pack(fill="both", expand=True, padx=10)

        abajo = ttk.Frame(self.root, padding=10)
        abajo.pack(fill="x")
        ttk.Button(abajo, text="Copiar todo", command=self.copiar).pack(side="left")
        ttk.Button(abajo, text="Guardar .txt...", command=self.guardar).pack(side="left", padx=6)
        ttk.Button(abajo, text="Limpiar", command=lambda: self.texto.delete("1.0", "end")).pack(side="left")

    def _bloquear(self, trabajando):
        self.trabajando = trabajando
        self.btn_abrir.config(state="disabled" if trabajando else "normal")
        self.combo_modelo.config(state="disabled" if trabajando else "readonly")
        self.btn_cancelar.config(state="normal" if trabajando else "disabled")

    # ---------- acciones ----------

    def seleccionar(self):
        patron = " ".join(f"*{e}" for e in sorted(EXTENSIONES))
        archivos = filedialog.askopenfilenames(
            title="Seleccionar audios",
            filetypes=[("Audios", patron), ("Todos los archivos", "*.*")],
        )
        if archivos:
            self.iniciar([Path(a) for a in archivos])

    def iniciar(self, archivos):
        self.cancelar.clear()
        self._bloquear(True)
        modelo = MODELOS[self.var_modelo.get()]
        threading.Thread(
            target=self._transcribir, args=(archivos, modelo, self.var_tiempos.get()), daemon=True,
        ).start()

    # ---------- arrastrar y soltar ----------

    def _al_entrar_arrastre(self, evento):
        if not self.trabajando:
            self._estado_previo = self.var_estado.get()
            self.var_estado.set("Suelta los audios para transcribirlos...")
        return evento.action

    def _al_salir_arrastre(self, evento):
        if not self.trabajando and hasattr(self, "_estado_previo"):
            self.var_estado.set(self._estado_previo)
        return evento.action

    def _al_soltar(self, evento):
        if self.trabajando:
            messagebox.showinfo("Ocupado", "Espera a que termine la transcripción actual (o cancélala).")
            return evento.action
        rutas = self.root.tk.splitlist(evento.data)  # separa rutas con espacios ({C:/a b.ogg})
        audios = [a for a in buscar_audios(rutas) if a.suffix.lower() in EXTENSIONES]
        if audios:
            self.iniciar(audios)
        else:
            self.var_estado.set("Lo que soltaste no contiene audios compatibles.")
        return evento.action

    def copiar(self):
        self.root.clipboard_clear()
        self.root.clipboard_append(self.texto.get("1.0", "end-1c"))
        self.var_estado.set("Texto copiado al portapapeles.")

    def guardar(self):
        ruta = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Texto", "*.txt")])
        if ruta:
            Path(ruta).write_text(self.texto.get("1.0", "end-1c"), encoding="utf-8")
            self.var_estado.set(f"Guardado en {ruta}")

    # ---------- trabajo en segundo plano ----------

    def _transcribir(self, archivos, nombre_modelo, con_tiempos):
        try:
            if nombre_modelo not in self.modelos_cargados:
                descargado = modelo_local(nombre_modelo) or any(
                    carpeta_modelos().glob(f"models--*{nombre_modelo}*/snapshots/*/model.bin"))
                if descargado:
                    self.cola.put(("estado", f"Cargando modelo {nombre_modelo}..."))
                else:
                    self.cola.put(("estado", "Descargando el modelo de voz (solo la primera vez, puede tardar "
                                             "varios minutos según tu internet)..."))
                    self.cola.put(("titulo", f"Descargando modelo - {TITULO}"))
                self.modelos_cargados[nombre_modelo] = cargar_modelo(nombre_modelo)
            modelo = self.modelos_cargados[nombre_modelo]

            for i, audio in enumerate(archivos, 1):
                if self.cancelar.is_set():
                    break
                self.cola.put(("estado", f"[{i}/{len(archivos)}] Transcribiendo {audio.name}..."))
                self.cola.put(("progreso", 0))
                if len(archivos) > 1:
                    self.cola.put(("texto", f"===== {audio.name} =====\n"))

                segmentos, info = transcribir_audio(modelo, audio, "es")
                for seg in segmentos:
                    if self.cancelar.is_set():
                        break
                    linea = seg.text.strip()
                    if con_tiempos:
                        linea = f"[{formato_tiempo(seg.start)}] {linea}"
                    self.cola.put(("texto", linea + ("\n" if con_tiempos else " ")))
                    if info.duration:
                        self.cola.put(("progreso", min(100, seg.end / info.duration * 100)))
                self.cola.put(("texto", "\n\n" if len(archivos) > 1 else "\n"))

            if self.cancelar.is_set():
                self.cola.put(("fin", "Cancelado."))
            else:
                self.cola.put(("progreso", 100))
                self.cola.put(("fin", "Listo. Puedes editar, copiar o guardar el texto."))
        except Exception as e:
            self.cola.put(("error", str(e)))

    def _revisar_cola(self):
        try:
            while True:
                tipo, valor = self.cola.get_nowait()
                if tipo == "texto":
                    self.texto.insert("end", valor)
                    self.texto.see("end")
                elif tipo == "estado":
                    self.var_estado.set(valor)
                elif tipo == "titulo":
                    self.root.title(valor)
                elif tipo == "progreso":
                    self.progreso["value"] = valor
                    self.root.title(f"{valor:.0f}% - {TITULO}")
                elif tipo == "fin":
                    self.var_estado.set(valor)
                    self.root.title(f"{valor.split('.')[0]} - {TITULO}")
                    self._bloquear(False)
                elif tipo == "error":
                    self.var_estado.set("Ocurrió un error.")
                    self.root.title(f"Error - {TITULO}")
                    self._bloquear(False)
                    messagebox.showerror("Error al transcribir", valor)
        except queue.Empty:
            pass
        self.root.after(100, self._revisar_cola)


if __name__ == "__main__":
    if sys.platform == "win32":
        # en la barra de tareas aparece como programa propio, no agrupado con Python
        import ctypes
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("transcriptor.audios")
    root = None
    if TkinterDnD:
        try:
            root = TkinterDnD.Tk()
        except RuntimeError:  # falta alguna biblioteca del sistema (ej. libXcursor en Linux)
            root = None
    if root is None:
        root = tk.Tk()
    icono = Path(getattr(sys, "_MEIPASS", Path(__file__).parent)) / "icono.ico"
    if sys.platform == "win32" and icono.exists():
        root.iconbitmap(default=str(icono))
    try:
        ttk.Style().theme_use("vista")
    except tk.TclError:
        pass
    app = App(root)
    # audios soltados encima del ícono del programa o abiertos con "Abrir con"
    iniciales = [a for a in buscar_audios(sys.argv[1:]) if a.suffix.lower() in EXTENSIONES]
    if iniciales:
        root.after(200, app.iniciar, iniciales)
    root.mainloop()
