@echo off
REM Set up a local virtual environment and install all Python dependencies.

cd /d "%~dp0"

REM CustomTkinter requires Tk >= 8.6. Bail out early if the python on PATH
REM is built against an older Tk (the app would launch as a blank window).
python -c "import tkinter,sys; sys.exit(0 if tkinter.TkVersion>=8.6 else 1)" 2>nul
if errorlevel 1 (
    echo Error: python on PATH is built against Tk ^< 8.6, which causes a blank UI.
    echo Install Python 3.10+ from python.org and re-run setup.bat.
    exit /b 1
)

if not exist ".venv" (
    echo Creating virtual environment in .venv...
    python -m venv .venv
    if errorlevel 1 goto :error
)

call .venv\Scripts\activate.bat
if errorlevel 1 goto :error

echo Upgrading pip...
python -m pip install --upgrade pip
if errorlevel 1 goto :error

echo Installing requirements...
pip install -r requirements.txt
if errorlevel 1 goto :error

echo.
echo Done. To run the app:
echo     .venv\Scripts\activate
echo     python application.py
exit /b 0

:error
echo.
echo Setup failed. See messages above.
exit /b 1
