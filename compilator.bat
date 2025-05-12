@echo off
echo.
echo === Compilando o Gerador de Gabaritos Personalizados ===
echo.

REM Caminho do ícone e nome do executável
set ICON=assets\icon.ico
set MAIN=main.py
set NAME=GeradorDeGabaritosPersonalizados

REM Comando de compilação
pyinstaller ^
--noconfirm ^
--onefile ^
--windowed ^
--name "%NAME%" ^
--icon "%ICON%" ^
--add-data "assets;assets" ^
--hidden-import=tkinter ^
"%MAIN%"

echo.
echo === Compilação concluída ===
pause
