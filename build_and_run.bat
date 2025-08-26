@echo off
set SRC_DIR=engine
set BUILD_DIR=build

if not exist %BUILD_DIR% mkdir %BUILD_DIR%

REM Compila para DLL
gcc -shared %SRC_DIR%\compilehell.c -lSDL2 -lSDL2_image -o %BUILD_DIR%\compilehell.dll

echo Build concluída. Para rodar: python examples\demo.py
