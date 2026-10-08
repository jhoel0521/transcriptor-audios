# Componentes de terceros

El código de este repositorio es de sus autores y se distribuye bajo [GPL v3 o posterior](LICENSE)
con un [permiso adicional](EXCEPCION-GPL.md). El repositorio **no contiene** código ni binarios de terceros.

El **programa compilado** (los `.zip` de Releases) sí incluye copias de los componentes de abajo.
Cada `.zip` trae sus textos de licencia en la carpeta `licencias/`.

## Bibliotecas de Python

| Componente | Licencia | Código fuente |
|---|---|---|
| Python | PSF-2.0 | https://github.com/python/cpython |
| faster-whisper | MIT | https://github.com/SYSTRAN/faster-whisper |
| CTranslate2 | MIT | https://github.com/OpenNMT/CTranslate2 |
| ONNX Runtime | MIT | https://github.com/microsoft/onnxruntime |
| PyAV | BSD-3-Clause | https://github.com/PyAV-Org/PyAV |
| NumPy (incluye OpenBLAS) | BSD-3-Clause y otras permisivas | https://github.com/numpy/numpy |
| tokenizers | Apache-2.0 | https://github.com/huggingface/tokenizers |
| huggingface_hub, hf-xet | Apache-2.0 | https://github.com/huggingface/huggingface_hub |
| tkinterdnd2 (incluye tkdnd) | MIT / BSD | https://github.com/Eliav2/tkinterdnd2 |
| tqdm | MPL-2.0 y MIT | https://github.com/tqdm/tqdm |
| certifi | MPL-2.0 | https://github.com/certifi/python-certifi |
| protobuf, flatbuffers, httpx, httpcore, h11, anyio, idna, click, colorama, filelock, fsspec, packaging, PyYAML, typing_extensions | BSD / MIT / Apache-2.0 / PSF | Ver `licencias/` en el programa |

## Bibliotecas nativas

| Componente | Viene con | Licencia | Código fuente |
|---|---|---|---|
| FFmpeg 7.1 (avcodec, avformat, etc.) | PyAV | LGPL v3 o posterior | https://github.com/PyAV-Org/pyav-ffmpeg |
| x264 | PyAV | GPL v2 o posterior | https://code.videolan.org/videolan/x264 |
| x265 | PyAV | GPL v2 o posterior | https://bitbucket.org/multicoreware/x265_git |
| LAME, TwoLAME, libgmp | PyAV | LGPL | https://github.com/PyAV-Org/pyav-ffmpeg |
| Opus, Vorbis, Ogg, Speex, libvpx, libaom, dav1d, SVT-AV1, libwebp, OpenH264, zlib, libiconv, opencore-amr, SRT | PyAV | BSD / MIT / Apache-2.0 / MPL-2.0 / LGPL | https://github.com/PyAV-Org/pyav-ffmpeg |
| OpenSSL 1.1 | PyAV (lo usa SRT) | OpenSSL / SSLeay (ver [permiso adicional](EXCEPCION-GPL.md)) | https://github.com/openssl/openssl |
| OpenSSL 3 | Python | Apache-2.0 | https://github.com/openssl/openssl |
| Intel OpenMP Runtime (libiomp5) | CTranslate2 | Intel Simplified Software License (ver [permiso adicional](EXCEPCION-GPL.md)) | No disponible (binario de Intel) |
| Tcl/Tk 8.6 | Python | Licencia de Tcl/Tk (tipo BSD) | https://www.tcl.tk |
| Cargador de PyInstaller | PyInstaller | GPL v2 o posterior con excepción para programas compilados | https://github.com/pyinstaller/pyinstaller |

La versión exacta de FFmpeg y sus bibliotecas corresponde a la usada por el paquete `av`
indicado en [requirements.txt](requirements.txt).

## Modelo de voz

El modelo **Whisper large-v3-turbo** (OpenAI, licencia MIT; conversión de
[mobiuslabsgmbh](https://huggingface.co/mobiuslabsgmbh/faster-whisper-large-v3-turbo), MIT)
no se incluye en el repositorio ni en los `.zip`: el programa lo descarga la primera vez que se usa.
