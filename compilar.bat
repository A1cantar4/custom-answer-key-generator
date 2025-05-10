@echo off
set SCRIPT=app.py
set ICON=icon.ico
set NOME_EXECUTAVEL=GeradorDeGabaritosPersonalizados

echo.
echo 🔧 Compilando %SCRIPT% para %NOME_EXECUTAVEL%.exe com ícone %ICON%...

pyinstaller --noconfirm --onefile --windowed --icon=%ICON% --name %NOME_EXECUTAVEL% %SCRIPT%

echo.
echo ✅ Compilação concluída!
echo O executável está disponível em:
echo dist\%NOME_EXECUTAVEL%.exe
echo.
pause
