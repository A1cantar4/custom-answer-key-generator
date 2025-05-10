@echo off
setlocal

:: Nome do executável final
set NOME_EXECUTAVEL=GeradorGabaritos

:: Nome do script principal
set SCRIPT=app.py

:: Ícone personalizado
set ICON=icon.ico

:: Empacotar com PyInstaller
pyinstaller ^
 --noconfirm ^
 --onefile ^
 --windowed ^
 --icon=icon.ico ^
 --add-data "icon.ico;." ^
 --add-data "background.png;." ^
 --name %NOME_EXECUTAVEL% ^
 %SCRIPT%

echo.
echo ==================================================
echo Executável gerado com sucesso!
echo Verifique a pasta dist\%NOME_EXECUTAVEL%.exe
echo ==================================================
pause