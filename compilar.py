# Transcriptor de audios - Copyright (C) 2026 jhoel0521
# Licencia: GPL v3 o posterior, con permiso adicional. Ver LICENSE y EXCEPCION-GPL.md.

"""Compila el programa portable en dist/Transcriptor/.

Uso (con el entorno instalado):
    python compilar.py              # para uso propio: copia adentro los modelos de modelos/
    python compilar.py --publicar   # para Releases: sin modelos, y crea dist/Transcriptor-<Sistema>.zip

Cada sistema se compila en ese mismo sistema (Windows en Windows, Linux en Linux o con Docker).
"""

import argparse
import os
import platform
import re
import shutil
import sys
from importlib.metadata import distributions
from pathlib import Path

import PyInstaller.__main__

from transcribir import __version__

AQUI = Path(__file__).resolve().parent
DIST = AQUI / "dist"
SALIDA = DIST / "Transcriptor"
SISTEMA = {"win32": "Windows", "darwin": "Mac"}.get(sys.platform, "Linux")

# Herramientas de compilación: no van dentro del programa, así que sus licencias no se copian.
NO_INCLUIDAS = {"pip", "setuptools", "wheel", "pyinstaller", "pyinstaller-hooks-contrib", "altgraph",
                "pefile", "pywin32-ctypes", "macholib", "pillow"}
ARCHIVO_LICENCIA = re.compile(r"(licen[cs]e|copying|notice|authors)", re.IGNORECASE)


def compilar():
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
        "--distpath", str(DIST),
        "--workpath", str(AQUI / "build"),
        "--specpath", str(AQUI / "build"),
    ])


def copiar_licencias():
    """Pone en el programa la licencia propia y las de todos los componentes de terceros que lleva."""
    for nombre in ("LICENSE", "EXCEPCION-GPL.md", "TERCEROS.md"):
        shutil.copy2(AQUI / nombre, SALIDA / nombre)

    destino = SALIDA / "licencias"
    shutil.copytree(AQUI / "licencias", destino, dirs_exist_ok=True)  # LGPL (FFmpeg) y OpenSSL 1.1
    for dist in distributions():
        nombre = dist.metadata["Name"]
        if nombre.lower() in NO_INCLUIDAS:
            continue
        for archivo in dist.files or []:
            if ".dist-info" in str(archivo) and ARCHIVO_LICENCIA.search(archivo.name):
                origen = Path(dist.locate_file(archivo))
                if origen.is_file():
                    (destino / nombre).mkdir(parents=True, exist_ok=True)
                    shutil.copy2(origen, destino / nombre / origen.name)


def main():
    parser = argparse.ArgumentParser(description="Compila el programa portable.")
    parser.add_argument("--publicar", action="store_true",
                        help="Compilación para Releases: sin modelos y comprimida en un .zip")
    args = parser.parse_args()

    compilar()
    copiar_licencias()

    if args.publicar:
        zip_base = DIST / f"Transcriptor-{SISTEMA}"
        print(f"Comprimiendo {zip_base.name}.zip...")
        shutil.make_archive(str(zip_base), "zip", root_dir=DIST, base_dir="Transcriptor")
        print(f"\nListo: Transcriptor {__version__} para {SISTEMA} ({platform.machine()})")
        print(f"  {zip_base}.zip")
        return

    # Uso propio: copia los modelos ya descargados para que funcione sin internet.
    modelos = AQUI / "modelos"
    if modelos.is_dir():
        print("Copiando modelos (puede tardar)...")
        shutil.copytree(modelos, SALIDA / "modelos", dirs_exist_ok=True)
    print(f"\nListo: {SALIDA}")


if __name__ == "__main__":
    main()
