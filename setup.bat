@echo off
REM Set up a local virtual environment and install all Python dependencies.

cd /d "%~dp0"

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
