# Cómo colaborar

¡Gracias por querer mejorar el Transcriptor! Cualquier ayuda suma: reportar errores, ideas, código o documentación.

## Reportar un error

Abre un [issue](../../issues) y cuenta:

- Tu sistema (Windows, Mac o Linux) y su versión.
- Qué hiciste, qué esperabas y qué pasó.
- El mensaje de error, si apareció.

No adjuntes audios con información privada.

## Mejorar el código

1. Haz un *fork* del repositorio y clónalo.
2. Prepara el entorno (ver "Ejecutar desde el código" en el README).
3. Crea una rama para tu cambio: `git checkout -b mi-mejora`
4. Prueba que funcione: abre la ventana con `python app.pyw` y transcribe un audio.
5. Haz commit y abre un *pull request* explicando qué cambiaste y por qué.

Todos los cambios entran a `main` por pull request: nadie sube directo a `main`.

Si agregas una biblioteca nueva, revisa que su licencia sea compatible con GPL v3 (MIT, BSD, Apache 2.0, LGPL, GPL)
y anótala en [TERCEROS.md](TERCEROS.md).

## Estilo

- El código, los comentarios y los mensajes del programa están en español.
- Mantén el programa simple: la idea es que cualquiera lo pueda usar sin saber de computadoras.
- La lógica de transcripción va en `transcribir.py`; la ventana, en `app.pyw`.
