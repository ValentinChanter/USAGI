@echo off

REM ─────────────────────────────
REM Colors (may not render in standard CMD without ANSI support)
set "RED=[91m"
set "BLUE=[94m"
set "RESET=[0m"

REM ─────────────────────────────
REM Open a cmd with the venv activated
echo %BLUE%[INFO]%RESET% Activating virtual environment...
call "%cd%\venv\Scripts\activate.bat"

cd src
cmd /k