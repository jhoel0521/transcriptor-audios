# Transcriptor de audios

Convierte audios (por ejemplo, los de WhatsApp) a texto con Whisper, en tu propia computadora y gratis.
No necesita internet, salvo la primera vez para descargar el modelo (unos 800 MB), y los audios no salen de tu equipo.

Funciona en **Windows**, **Linux** y **Mac**. No funciona en iPhone ni en Android.

## 1. Descargar el proyecto

```bash
git clone https://github.com/jhoel0521/transcriptor-audios.git
cd transcriptor-audios
```

## 2. Instalar (una sola vez)

Necesitas Python 3.10 o más reciente.

### Windows

```bash
python -m venv .venv
.venv\Scripts\python -m pip install -r requirements.txt
powershell -ExecutionPolicy Bypass -File crear_accesos.ps1
```

La última línea crea el ícono **"Transcriptor de audios"** (un micrófono azul) en el escritorio y en el menú Inicio.

### Linux (Ubuntu, Debian, Mint)

Primero instala lo que Python necesita para abrir ventanas:

```bash
sudo apt install python3-venv python3-tk
```

Después:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
chmod +x transcriptor.sh
```

### Mac

Usa el Python de python.org (ya trae lo necesario para las ventanas).
Si usas el de Homebrew, instala antes `brew install python-tk`.

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
chmod +x transcriptor.sh
```

## 3. Abrir la ventana

- **Windows:** doble clic en el ícono **"Transcriptor de audios"** del escritorio, o búscalo en el menú Inicio escribiendo "Transcriptor".
  También puedes hacer doble clic en `Transcriptor.bat`.
- **Linux y Mac:** en la terminal, dentro de la carpeta del proyecto:

  ```bash
  ./transcriptor.sh
  ```

## 4. Usar la ventana

1. Haz clic en **"Seleccionar audio..."**, arriba a la izquierda, y elige tu audio. También puedes arrastrar el audio y soltarlo encima de la ventana.
2. Espera. El texto va apareciendo en el cuadro grande. Un audio de 2 minutos tarda unos 40 segundos.
3. Cuando arriba diga **"Listo"**, haz clic en **"Copiar todo"** y pega el texto donde quieras.

Otros botones:

- **Guardar .txt...** guarda el texto en un archivo.
- **Limpiar** borra el cuadro para empezar otro audio.
- **Cancelar** detiene una transcripción a la mitad.
- **Modelo:** "Preciso" (recomendado) o "Rápido" (unas 3 veces más veloz, pero se equivoca más).
- **Con tiempos** agrega el minuto de cada frase, por ejemplo `[01:22]`.

El primer audio tarda unos segundos más porque carga el modelo. Si dejas la ventana abierta, los siguientes van directo.

## Uso desde la terminal (opcional)

Transcribe uno o varios audios, o una carpeta entera, y guarda los textos en `transcripciones/`:

```bash
# Windows
.venv\Scripts\python transcribir.py "audio.ogg" --salida transcripciones

# Linux y Mac
.venv/bin/python transcribir.py "audio.ogg" --salida transcripciones
```

En Windows también puedes soltar audios encima de `transcribir.bat`.

Opciones:

- `--tiempos` agrega el minuto de cada frase.
- `--mover carpeta` mueve cada audio a esa carpeta al terminar.
- `--modelo small` es más rápido pero menos preciso.
- `--idioma auto` detecta el idioma solo. Por defecto usa español.

## Privacidad

Los audios y la carpeta `transcripciones/` están en `.gitignore`, así que nunca se suben al repositorio.
