# Transcriptor de audios

Convierte audios (por ejemplo, los de WhatsApp) a texto con Whisper, de forma local y gratis.
No necesita internet, salvo la primera vez para descargar el modelo, y los audios no salen de la PC.

## Instalación (una sola vez)

Requiere Python 3.10 o más reciente. Dentro de la carpeta del proyecto:

```bash
python -m venv .venv
.venv\Scripts\python -m pip install -r requirements.txt
```

## Uso

**Ventana:** doble clic en `Transcriptor.bat`. Arrastra los audios a la ventana o usa el botón
"Seleccionar audio...". El texto aparece en el cuadro y se puede copiar o guardar.

**Arrastrar sobre el archivo:** suelta audios encima de `transcribir.bat`. Los textos se guardan en `transcripciones/`.

**Terminal:**

```bash
.venv\Scripts\python transcribir.py "audio.ogg" --salida transcripciones
```

Opciones: `--tiempos` (marca el minuto de cada frase), `--mover carpeta` (mueve el audio al terminar),
`--modelo small` (más rápido, menos preciso), `--idioma auto`.
