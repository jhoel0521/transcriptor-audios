"""Compila la app portable en dist/Transcriptor/ (Transcriptor.exe + modelos/).

Uso (con el entorno instalado):
    .venv\\Scripts\\python compilar.py
"""

import os
import shutil
import sys
from pathlib import Path

import PyInstaller.__main__

AQUI = Path(__file__).parent
SALIDA = AQUI / "dist" / "Transcriptor"

# El Python de Laragon no encuentra Tcl/Tk por sí solo; PyInstaller lo necesita para empaquetarlo.
tcl = Path(sys.base_prefix) / "tcl"
for var, carpeta in (("TCL_LIBRARY", "tcl8.6"), ("TK_LIBRARY", "tk8.6")):
    if var not in os.environ and (tcl / carpeta).is_dir():
        os.environ[var] = str(tcl / carpeta)

PyInstaller.__main__.run([
    str(AQUI / "app.pyw"),
    "--name", "Transcriptor",
    "--icon", str(AQUI / "icono.ico"),
    "--add-data", f"{AQUI / 'icono.ico'}{os.pathsep}.",
    "--windowed",          # sin ventana de consola
    "--onedir",            # carpeta portable: arranca más rápido que un solo .exe gigante
    "--noconfirm",
    "--clean",
    "--collect-all", "faster_whisper",   # incluye el detector de silencios (assets/*.onnx)
    "--collect-all", "ctranslate2",
    "--collect-all", "tkinterdnd2",      # arrastrar y soltar
    "--collect-binaries", "onnxruntime",
    "--distpath", str(AQUI / "dist"),
    "--workpath", str(AQUI / "build"),
    "--specpath", str(AQUI / "build"),
])

# Copia los modelos ya descargados para que funcione sin internet.
modelos = AQUI / "modelos"
if modelos.is_dir():
    print("Copiando modelos (puede tardar)...")
    shutil.copytree(modelos, SALIDA / "modelos", dirs_exist_ok=True)

print(f"\nListo: {SALIDA / 'Transcriptor.exe'}")
