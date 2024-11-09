@echo off
setlocal enabledelayedexpansion

REM 
set "DATA_DIR=%~dp0"
set "VENV_DIR=%DATA_DIR%\env"
set "REQUIREMENTS_FILE=%DATA_DIR%\requirements.txt"
set "PAPERZ_FILE_EXE=%DATA_DIR%\dist\Paper-Z.exe"
set "BUILD_DIR=%DATA_DIR%\dist"


REM 
echo.
echo Checking for Python installation...
where python >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed. Please install Python and try again.
    pause
    exit /b 1
)
echo Python is installed.

REM 
echo Setting up Python virtual environment...
echo.
timeout /t 1 /nobreak >nul

python -m venv %VENV_DIR%
call %VENV_DIR%\Scripts\activate.bat
pip install -r %REQUIREMENTS_FILE%
pyinstaller ./main.spec
call %VENV_DIR%\Scripts\deactivate.bat

REM
echo.
echo Moving built executable to %DATA_DIR%...
if exist "%PAPERZ_FILE_EXE%" (
    move /y "%PAPERZ_FILE_EXE%" "%DATA_DIR%"
) else (
    echo Error: Executable not found in %BUILD_DIR%.
)

echo Build completed.
pause
