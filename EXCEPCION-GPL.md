# Permiso adicional de la licencia (GPL v3, sección 7)

Este programa se distribuye bajo la [GNU General Public License v3](LICENSE) o posterior,
con el siguiente permiso adicional. El texto en inglés es el que tiene validez legal.

## Additional permission under GNU GPL version 3 section 7

If you modify this Program, or any covered work, by linking or combining it with
OpenSSL (or a modified version of that library), or with the Intel(R) OpenMP* Runtime
Library (libiomp5, or a modified version of that library), containing parts covered by
the terms of the OpenSSL License, the original SSLeay License or the Intel Simplified
Software License, the licensors of this Program grant you additional permission to
convey the resulting work. Corresponding Source for a non-source form of such a
combination shall include the source code for the parts of OpenSSL used as well as
that of the covered work.

## Traducción (solo como referencia)

Si modificas este Programa, o cualquier obra cubierta, enlazándolo o combinándolo con
OpenSSL (o una versión modificada de esa biblioteca), o con la biblioteca Intel(R) OpenMP*
Runtime (libiomp5, o una versión modificada de ella), que contienen partes cubiertas por la
licencia de OpenSSL, la licencia original de SSLeay o la Intel Simplified Software License,
los licenciantes de este Programa te otorgan permiso adicional para distribuir la obra
resultante. La Fuente Correspondiente de una forma no fuente de dicha combinación deberá
incluir el código fuente de las partes de OpenSSL utilizadas, además del de la obra cubierta.

## Por qué existe este permiso

El programa compilado incluye esas bibliotecas de forma indirecta: OpenSSL 1.1 viene dentro
del FFmpeg que trae el paquete [PyAV](https://github.com/PyAV-Org/PyAV) (lo usa `libsrt`), y el runtime
de Intel viene dentro del paquete [CTranslate2](https://github.com/OpenNMT/CTranslate2).
Sus licencias no son compatibles con la GPL por sí solas; este permiso lo resuelve para el
código de este proyecto.
