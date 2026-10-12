#!/bin/bash
set -e

REMOTE_VENV="$HOME/venv_numba"

echo "Creating clean virtual environment on remote machine: $REMOTE_VENV..."
rm -rf "$REMOTE_VENV"
python3 -m venv "$REMOTE_VENV"

echo "Installing numba and numpy..."
"$REMOTE_VENV/bin/pip" install --upgrade pip
"$REMOTE_VENV/bin/pip" install numba numpy

echo "Testing imports..."
"$REMOTE_VENV/bin/python" -c "import numba, numpy; print(f'Numba {numba.__version__}, Numpy {numpy.__version__} installed successfully!')"

echo "Running Numba experiment..."
"$REMOTE_VENV/bin/python" run_exp_d.py "$REMOTE_VENV/bin/python" results_exp_d_remote.csv

echo "Results:"
cat results_exp_d_remote.csv
