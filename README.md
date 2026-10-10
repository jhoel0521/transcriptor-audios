# Transcriptor de audios

Convierte audios a texto (por ejemplo, las notas de voz de WhatsApp) con [Whisper](https://github.com/openai/whisper),
**en tu propia computadora y gratis**. Los audios no salen de tu equipo: después de la primera vez funciona sin internet.

- Ventana simple: eliges o arrastras un audio y el texto aparece en pantalla, listo para copiar.
- Muy buena calidad en español (también detecta otros idiomas).
- Acepta audios de cualquier duración: `.ogg`, `.opus`, `.mp3`, `.m4a`, `.wav`, `.mp4`, `.webm`, `.flac`, `.aac`.
- Funciona en **Windows**, **Linux** y **Mac**.

## Descargar

Entra a **[Releases](../../releases/latest)** y baja el `.zip` de tu sistema:

| Sistema | Archivo | Cómo abrirlo |
|---|---|---|
| Windows 10 u 11 (64 bits) | `Transcriptor-Windows.zip` | Descomprime y doble clic en `Transcriptor.exe` |
| Linux (64 bits): Ubuntu 22.04+, Debian 12+, Mint 21+, Fedora 36+ | `Transcriptor-Linux.zip` | Descomprime y ejecuta `Transcriptor/Transcriptor` |
| Mac | No hay programa compilado todavía | Usa el programa desde el código (ver abajo) |

No hay que instalar nada: es una carpeta portable que puedes copiar a un USB o a otra PC.

**La primera vez** que transcribes, el programa descarga el modelo de voz (1,6 GB) y lo guarda junto al programa.
Puede tardar varios minutos según tu internet. Después ya no lo vuelve a descargar.

### Avisos de seguridad (normales en programas sin firma digital)

- **Windows** puede mostrar "Windows protegió su PC": haz clic en **Más información** y luego en **Ejecutar de todas formas**.

El programa se compila a partir del código de este repositorio, así que cualquiera puede revisar exactamente qué hace,
o compilarlo por su cuenta (ver "Compilar el programa").

## Cómo se usa

1. Abre el programa.
2. Haz clic en **"Seleccionar audio..."** o arrastra el audio encima de la ventana.
3. Espera: el texto va apareciendo y el título de la ventana muestra el avance.
   En una computadora normal, un audio de 2 minutos tarda alrededor de 1 minuto.
4. Cuando diga **"Listo"**, haz clic en **"Copiar todo"**.

Otras opciones: **Guardar .txt...**, **Limpiar**, **Cancelar**, **Con tiempos** (marca el minuto de cada frase)
y **Modelo** ("Preciso" o "Rápido", que es más veloz pero se equivoca más).

## Ejecutar desde el código

Requiere Python 3.10 o más reciente. En Linux instala antes `sudo apt install python3-venv python3-tk`.

```bash
git clone https://github.com/jhoel0521/transcriptor-audios.git
cd transcriptor-audios
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\python -m pip install -r requirements.txt
.venv\Scripts\python app.pyw
```

Mac y Linux:

```bash
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python app.pyw
```

### Desde la terminal

`transcribir.py` transcribe uno o varios audios, o una carpeta entera, y guarda los textos:

```bash
python transcribir.py "audio.ogg" --salida transcripciones
```

Opciones: `--tiempos`, `--mover carpeta`, `--modelo small`, `--idioma auto`.

### Compilar el programa

Cada sistema se compila en ese mismo sistema: PyInstaller no puede crear un programa de Mac desde Windows, ni al revés.
La excepción es Linux, que se puede compilar desde cualquier sistema con Docker.

**Windows** (y Mac), con el entorno instalado:

```bash
python -m pip install pyinstaller
python compilar.py
```

El programa queda en `dist/Transcriptor/`. Si existe la carpeta `modelos/` en el proyecto, se copia adentro
para que funcione sin internet.

Para armar el `.zip` que se publica en Releases (sin el modelo y con todas las licencias de terceros):

```bash
python compilar.py --publicar
```

**Linux**, con Docker, desde Windows, Mac o Linux:

```bash
docker build -f Dockerfile.linux -o dist .
```

Deja `dist/Transcriptor-Linux.zip`. Se compila sobre Ubuntu 22.04 para que funcione en Ubuntu 22.04 o superior,
Debian 12 o superior, Mint 21 o superior y Fedora 36 o superior.

## Archivos del proyecto

| Archivo | Qué hace |
|---|---|
| `app.pyw` | La ventana |
| `transcribir.py` | La transcripción (la usa la ventana, y también funciona sola desde la terminal) |
| `compilar.py` | Genera el programa portable con PyInstaller |
| `Dockerfile.linux` | Compila la versión de Linux dentro de Docker |
| `licencias/` | Textos de licencias de terceros que se copian al programa compilado |

## Planes a futuro

- **Programa compilado para Mac.** Hace falta alguien con una Mac que lo compile y lo pruebe.
- **App para Android y iPhone.** Este código no puede correr en teléfonos, pero se puede hacer una app aparte usando
  [whisper.cpp](https://github.com/ggerganov/whisper.cpp), que sí funciona en móviles. ¡Se aceptan ayudas!
- Abrir el programa directamente desde "Compartir" en WhatsApp de escritorio.
- Barra de progreso durante la descarga del modelo.

## Colaborar

¿Encontraste un error o tienes una idea? Abre un [issue](../../issues). Si quieres mejorar el código, mira [CONTRIBUTING.md](CONTRIBUTING.md).

## Licencia

[GPL v3 o posterior](LICENSE), con un [permiso adicional](EXCEPCION-GPL.md) para las bibliotecas OpenSSL e Intel OpenMP
que vienen incluidas en el programa compilado. Puedes usar, copiar y modificar este programa libremente.
Si distribuyes una versión modificada, debes publicar también su código bajo la misma licencia.

Los componentes de terceros que incluye el programa compilado y sus licencias están en [TERCEROS.md](TERCEROS.md).

## Créditos

- [faster-whisper](https://github.com/SYSTRAN/faster-whisper) y el modelo Whisper de OpenAI.
- Inspirado en [ogg-speech-to-text](https://github.com/danperrout/ogg-speech-to-text) de Daniel Perrout.
