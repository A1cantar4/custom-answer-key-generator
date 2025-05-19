@echo off
echo.
echo === Compilando o Gerador de Gabaritos Personalizados ===
echo.

REM Caminho do ícone e nome do executável
set "ICON=assets\icon.ico"
set "MAIN=main.py"
set "NAME=GabaritoApp"

REM Verifica se o PyInstaller está instalado
where pyinstaller >nul 2>nul
if errorlevel 1 (
    echo [ERRO] PyInstaller não está instalado. Execute: pip install pyinstaller
    pause
    exit /b
)

REM Remove pastas anteriores
rmdir /s /q build >nul 2>nul
rmdir /s /q dist >nul 2>nul
del /q "%NAME%.spec" >nul 2>nul

REM Comando de compilação com dependências extras
pyinstaller ^
--noconfirm ^
--onefile ^
--windowed ^
--name "%NAME%" ^
--icon "%ICON%" ^
--hidden-import=lxml.etree ^
--hidden-import=docx ^
--add-data "assets;assets" ^
"%MAIN%"

echo.
echo === Compilação concluída com sucesso ===
echo Arquivo gerado em: dist\%NAME%.exe
pause
