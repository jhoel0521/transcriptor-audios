# Transcriptor de audios - Copyright (C) 2026 jhoel0521
# Licencia: GPL v3 o posterior, con permiso adicional. Ver LICENSE y EXCEPCION-GPL.md.

"""Transcribe audios (WhatsApp .ogg, .mp3, .m4a, .wav...) a texto con Whisper local.

Uso:
    python transcribir.py "audio.ogg"
    python transcribir.py carpeta_con_audios
    python transcribir.py carpeta --mover procesados

Por cada audio crea un .txt con el mismo nombre al lado del archivo
(o en --salida si se indica).
"""

import argparse
import sys
import time
from pathlib import Path

from faster_whisper import WhisperModel

__version__ = "1.0.0"

EXTENSIONES = {".ogg", ".opus", ".mp3", ".m4a", ".wav", ".mp4", ".webm", ".flac", ".aac"}


def buscar_audios(rutas):
    audios = []
    for ruta in rutas:
        p = Path(ruta)
        if p.is_dir():
            audios += sorted(f for f in p.iterdir() if f.suffix.lower() in EXTENSIONES)
        elif p.is_file():
            audios.append(p)
        else:
            print(f"No existe: {p}", file=sys.stderr)
    return audios


def formato_tiempo(segundos):
    m, s = divmod(int(segundos), 60)
    return f"{m:02d}:{s:02d}"


def carpeta_programa():
    """Carpeta del .exe si está compilado; si no, la de este archivo."""
    if getattr(sys, "frozen", False):
        return Path(sys.executable).parent
    return Path(__file__).parent


def carpeta_modelos():
    # En Mac la app (.app) no debe escribirse por dentro: los modelos van a la carpeta de datos del usuario.
    if getattr(sys, "frozen", False) and sys.platform == "darwin":
        return Path.home() / "Library" / "Application Support" / "Transcriptor" / "modelos"
    return carpeta_programa() / "modelos"


def modelo_local(nombre):
    """Carpeta del modelo copiado a mano en "modelos/<nombre>", o None si no está."""
    local = carpeta_modelos() / nombre
    return local if (local / "model.bin").exists() else None


def cargar_modelo(nombre="large-v3-turbo"):
    # Los modelos viven en "modelos/" junto al programa, así la carpeta es portable.
    # Si no están, se descargan ahí la primera vez (después funciona sin internet).
    local = modelo_local(nombre)
    if local:
        return WhisperModel(str(local), device="cpu", compute_type="int8")
    modelos = carpeta_modelos()
    return WhisperModel(nombre, device="cpu", compute_type="int8", download_root=str(modelos))


def transcribir_audio(modelo, ruta, idioma="es"):
    """Devuelve (segmentos, info). Los segmentos se generan a medida que avanza."""
    return modelo.transcribe(
        str(ruta),
        language=None if idioma == "auto" else idioma,
        vad_filter=True,  # ignora silencios largos
        beam_size=5,
    )


def main():
    parser = argparse.ArgumentParser(description="Transcribe audios con Whisper local.")
    parser.add_argument("rutas", nargs="+", help="Archivos de audio o carpetas")
    parser.add_argument("--modelo", default="large-v3-turbo",
                        help="tiny, base, small, medium, large-v3, large-v3-turbo (por defecto)")
    parser.add_argument("--idioma", default="es", help="Código de idioma, 'auto' para detectar (por defecto: es)")
    parser.add_argument("--salida", help="Carpeta donde guardar los .txt (por defecto: junto al audio)")
    parser.add_argument("--mover", help="Mover cada audio a esta carpeta después de transcribirlo")
    parser.add_argument("--tiempos", action="store_true", help="Incluir marcas de tiempo [mm:ss] en el texto")
    args = parser.parse_args()

    audios = buscar_audios(args.rutas)
    if not audios:
        print("No se encontraron audios.")
        return 1

    print(f"Cargando modelo '{args.modelo}' (la primera vez se descarga)...")
    modelo = cargar_modelo(args.modelo)

    errores = 0
    for i, audio in enumerate(audios, 1):
        print(f"\n[{i}/{len(audios)}] {audio.name}")
        inicio = time.time()
        try:
            segmentos, info = transcribir_audio(modelo, audio, args.idioma)
            lineas = []
            for seg in segmentos:
                texto = seg.text.strip()
                print(f"  [{formato_tiempo(seg.start)}] {texto}")
                lineas.append(f"[{formato_tiempo(seg.start)}] {texto}" if args.tiempos else texto)
        except Exception as e:
            errores += 1
            print(f"  ERROR: {e}", file=sys.stderr)
            continue  # no se mueve el audio si falló

        carpeta_txt = Path(args.salida) if args.salida else audio.parent
        carpeta_txt.mkdir(parents=True, exist_ok=True)
        destino_txt = carpeta_txt / (audio.stem + ".txt")
        destino_txt.write_text("\n".join(lineas) + "\n", encoding="utf-8")

        duracion = time.time() - inicio
        print(f"  -> {destino_txt}  (audio {formato_tiempo(info.duration)}, tardó {duracion:.0f}s)")

        if args.mover:
            carpeta_mover = Path(args.mover)
            carpeta_mover.mkdir(parents=True, exist_ok=True)
            audio.rename(carpeta_mover / audio.name)

    print(f"\nListo: {len(audios) - errores} transcritos, {errores} con error.")
    return 1 if errores else 0


if __name__ == "__main__":
    sys.exit(main())
