Invoke-Expression -Command "C:\ignGrav\.venv\Scripts\Activate.ps1"
Set-Location -Path "C:\ignGrav\igngrav"
Invoke-Expression "hypercorn --bind 0.0.0.0:8000 igngrav.asgi:application"
