# Transcriptor de audios

Convierte audios (por ejemplo, los de WhatsApp) a texto con Whisper, en tu propia computadora y gratis.
Funciona sin internet y los audios no salen de tu equipo.

## Usar el programa (Windows)

El programa es **portable**: una carpeta `Transcriptor` con `Transcriptor.exe` adentro.
No hay que instalar nada. Se puede copiar a otra PC o a un USB y funciona igual.

1. Doble clic en **`Transcriptor.exe`** (el ícono del micrófono azul).
2. Haz clic en **"Seleccionar audio..."** y elige el audio. También puedes arrastrar el audio encima de la ventana,
   o encima del ícono de `Transcriptor.exe`.
3. Espera. El texto va apareciendo y el título de la ventana muestra el avance.
   Un audio de 2 minutos tarda alrededor de 1 minuto.
4. Cuando diga **"Listo"**, haz clic en **"Copiar todo"** y pega el texto donde quieras.

Otros botones:

- **Guardar .txt...** guarda el texto en un archivo.
- **Limpiar** borra el cuadro para empezar otro audio.
- **Cancelar** detiene una transcripción a la mitad.
- **Modelo:** "Preciso" (recomendado, ya incluido) o "Rápido" (más veloz pero se equivoca más;
  la primera vez lo descarga de internet, unos 500 MB).
- **Con tiempos** agrega el minuto de cada frase, por ejemplo `[01:22]`.

Para tenerlo a mano: clic derecho en `Transcriptor.exe` > **Enviar a** > **Escritorio (crear acceso directo)**.

## Compilar el programa (para desarrolladores)

Requiere Python 3.10 o más reciente. Dentro de la carpeta del proyecto:

```bash
python -m venv .venv
.venv\Scripts\python -m pip install -r requirements.txt pyinstaller
.venv\Scripts\python compilar.py
```

El resultado queda en `dist/Transcriptor/`. Si existe la carpeta `modelos/` en el proyecto, se copia adentro
para que funcione sin internet. Si no existe, el programa descarga el modelo la primera vez que se usa
y lo guarda en `modelos/`, junto al `.exe`.

## Linux y Mac

No hay `.exe`; se ejecuta con Python. En Linux instala antes `sudo apt install python3-venv python3-tk`.

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python app.pyw
```

No funciona en iPhone ni en Android.

## Uso desde la terminal (opcional)

Transcribe uno o varios audios, o una carpeta entera, y guarda los textos en `transcripciones/`:

```bash
.venv\Scripts\python transcribir.py "audio.ogg" --salida transcripciones
```

Opciones: `--tiempos`, `--mover carpeta`, `--modelo small`, `--idioma auto`.

## Privacidad

Los audios, las transcripciones, los modelos y el programa compilado están en `.gitignore`;
nunca se suben al repositorio.
