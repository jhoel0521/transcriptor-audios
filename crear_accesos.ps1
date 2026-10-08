# Crea los accesos directos "Transcriptor de audios" en el escritorio y en el menú Inicio.
# Ejecutar una vez después de instalar (clic derecho > Ejecutar con PowerShell).
$dir = $PSScriptRoot
$shell = New-Object -ComObject WScript.Shell
$destinos = @(
  [Environment]::GetFolderPath("Desktop"),
  (Join-Path ([Environment]::GetFolderPath("Programs")) "")
)
foreach ($carpeta in $destinos) {
  $acceso = $shell.CreateShortcut((Join-Path $carpeta "Transcriptor de audios.lnk"))
  $acceso.TargetPath = Join-Path $dir ".venv\Scripts\pythonw.exe"
  $acceso.Arguments = '"' + (Join-Path $dir "app.pyw") + '"'
  $acceso.WorkingDirectory = $dir
  $acceso.IconLocation = Join-Path $dir "icono.ico"
  $acceso.Description = "Transcribe audios a texto con Whisper"
  $acceso.Save()
  Write-Host "Acceso directo creado en: $carpeta"
}
