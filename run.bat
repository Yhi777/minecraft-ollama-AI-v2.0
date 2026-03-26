@echo off
set VERSION=2.0
set ENV_NAME=minecraft_ai_bot_v2

echo ===================================================
echo   Minecraft Autonomous AI Bot - Upgraded v%VERSION%
echo ===================================================

:: Check for Conda
where conda >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Conda not found. Please install Miniconda or Anaconda.
    pause
    exit /b
)

:: Environment Setup
conda env list | findstr /C:"%ENV_NAME%" >nul
if %ERRORLEVEL% neq 0 (
    echo [INFO] Creating new Conda environment: %ENV_NAME%...
    conda env create -f environment.yml -n %ENV_NAME%
) else (
    echo [INFO] Conda environment %ENV_NAME% detected.
)

:: Activate Environment
echo [INFO] Activating environment...
call conda activate %ENV_NAME%

:: Check for Node.js
where node >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Node.js not found. Required for Minecraft connection.
    pause
    exit /b
)

:: Install Node.js Dependencies
if not exist node_modules (
    echo [INFO] Installing mineflayer and pathfinder plugins...
    npm install mineflayer mineflayer-pathfinder minecraft-data vec3
)

:: Launch Upgraded AI
echo [INFO] Starting Upgraded AI Bot v%VERSION%...
python main.py

if %ERRORLEVEL% neq 0 (
    echo [ERROR] Application crashed. Check console for details.
    pause
)

echo [INFO] Application closed.
pause
