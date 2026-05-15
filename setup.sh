#!/usr/bin/env bash
# Set up a local virtual environment and install all Python dependencies.
set -e

cd "$(dirname "$0")"

# CustomTkinter requires Tk >= 8.6. Apple's system python3 ships with Tk 8.5,
# which causes a blank window. Prefer Homebrew python on macOS.
if [ -z "$PYTHON" ]; then
    if [ "$(uname)" = "Darwin" ] && [ -x /opt/homebrew/bin/python3.12 ]; then
        PYTHON=/opt/homebrew/bin/python3.12
    else
        PYTHON=python3
    fi
fi

# Verify the chosen interpreter has a usable Tk before building the venv.
if ! "$PYTHON" -c "import tkinter; assert tkinter.TkVersion >= 8.6" 2>/dev/null; then
    echo "Error: $PYTHON is built against Tk < 8.6, which causes a blank UI." >&2
    echo "On macOS, install Homebrew python: brew install python@3.12 python-tk@3.12" >&2
    echo "Then re-run with: PYTHON=/opt/homebrew/bin/python3.12 ./setup.sh" >&2
    exit 1
fi

if [ ! -d ".venv" ]; then
    echo "Creating virtual environment in .venv using $PYTHON..."
    "$PYTHON" -m venv .venv
fi

# shellcheck disable=SC1091
source .venv/bin/activate

echo "Upgrading pip..."
pip install --upgrade pip

echo "Installing requirements..."
pip install -r requirements.txt

echo
echo "Done. To run the app:"
echo "    source .venv/bin/activate"
echo "    python application.py"
