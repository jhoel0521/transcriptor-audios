@echo off
rem Arrastra uno o varios audios (o una carpeta) encima de este archivo.
set PYTHONIOENCODING=utf-8
"%~dp0.venv\Scripts\python.exe" "%~dp0transcribir.py" %* --salida "%~dp0transcripciones"
pause
