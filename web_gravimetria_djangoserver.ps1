Invoke-Expression -Command "C:\ignGrav\.venv\Scripts\Activate.ps1"
Set-Location -Path "C:\ignGrav\igngrav"
Invoke-Expression "py manage.py runserver 0.0.0.0:8000"
