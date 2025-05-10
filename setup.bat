@echo off
setlocal enabledelayedexpansion

REM ─────────────────────────────
REM Colors (may not render in standard CMD without ANSI support)
set "RED=[91m"
set "BLUE=[94m"
set "RESET=[0m"

REM ─────────────────────────────
REM Python version requirement
set "PYTHON_REQUIRED_MAJOR=3"
set "PYTHON_REQUIRED_MINOR=10"

REM ─────────────────────────────
REM Create venv if not exists
if not exist "venv" (
    REM ─────────────────────────────
    REM CUDA prompt
    set /p CUDA_PROMPT="Do you have a CUDA-capable GPU available? (y/n) [n]: "
    if /i "!CUDA_PROMPT!"=="y" (
        set "CUDA_AVAILABLE=True"
    ) else if /i "!CUDA_PROMPT!"=="yes" (
        set "CUDA_AVAILABLE=True"
    ) else (
        set "CUDA_AVAILABLE=False"
    )

    if "!CUDA_PROMPT!"=="" (
        set "CUDA_AVAILABLE=False"
    )

    if "!CUDA_AVAILABLE!"=="True" (
        echo Running installation for GPU.
        set "REQUIREMENTS_FILE=requirements-gpu.txt"
        set "TORCH_INDEX_URL=https://download.pytorch.org/whl/cu128"
    ) else (
        echo Running installation for CPU.
        set "REQUIREMENTS_FILE=requirements-cpu.txt"
    )

    echo !BLUE![INFO]!RESET! Creating virtual environment...

    where python >nul 2>nul
    if errorlevel 1 (
        echo !RED![ERROR]!RESET! Python is not installed. Please install Python and add it to your PATH.
        exit /b 1
    )

    REM ───── Get Python version
    for /f "delims=" %%i in ('python --version') do set "PYTHON_VERSION=%%i"
    for /f "tokens=2" %%i in ("!PYTHON_VERSION!") do set "VERSION_NUMBER=%%i"
    for /f "tokens=1,2,3 delims=." %%a in ("!VERSION_NUMBER!") do (
        set "MAJOR_VERSION=%%a"
        set "MINOR_VERSION=%%b"
        set "PATCH_VERSION=%%c"
    )

    echo !BLUE![INFO]!RESET! Python version detected: !MAJOR_VERSION!.!MINOR_VERSION!.!PATCH_VERSION!

    if !MAJOR_VERSION! LSS %PYTHON_REQUIRED_MAJOR% (
        echo !RED![ERROR]!RESET! Python 3.10 or higher is required.
        exit /b 1
    )
    if !MAJOR_VERSION!==3 if !MINOR_VERSION! LSS %PYTHON_REQUIRED_MINOR% (
        echo !RED![ERROR]!RESET! Python 3.10 or higher is required.
        exit /b 1
    )

    REM ───── Create virtual environment
    python -m venv venv
    if errorlevel 1 (
        echo !RED![ERROR]!RESET! Failed to create virtual environment.
        exit /b 1
    )

    REM ─────────────────────────────
    REM Install dependencies
    set "PYTHON_PATH=%cd%\venv\Scripts\python.exe"

    echo !BLUE![INFO]!RESET! Checking if dependencies are already installed...
    call "!PYTHON_PATH!" -c "import torch" >nul 2>nul
    if errorlevel 1 (
        echo !BLUE![INFO]!RESET! Installing dependencies...
        call "!PYTHON_PATH!" -m pip install --upgrade pip
        call "!PYTHON_PATH!" -m pip install --upgrade setuptools wheel

        if "!CUDA_AVAILABLE!"=="True" (
            REM Install PyTorch with CUDA support first, otherwise only CPU will be supported
            call "!PYTHON_PATH!" -m pip install torch torchvision torchaudio --index-url !TORCH_INDEX_URL!
            call "!PYTHON_PATH!" -m pip install onnxruntime-gpu
        )

        call "!PYTHON_PATH!" -m pip install -r !REQUIREMENTS_FILE!
    )

    echo !BLUE![INFO]!RESET! Dependencies installed successfully.
) else (
    echo !BLUE![INFO]!RESET! Virtual environment already exists.
    echo !BLUE![INFO]!RESET! If you want to recreate it, please delete the "venv" folder and run this script again.
)

echo.
echo Press any key to close this window...
pause >nul