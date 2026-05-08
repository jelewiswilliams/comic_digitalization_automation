#!/usr/bin/env bash
# Set up a local virtual environment and install all Python dependencies.
set -e

cd "$(dirname "$0")"

PYTHON="${PYTHON:-python3}"

if [ ! -d ".venv" ]; then
    echo "Creating virtual environment in .venv..."
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
