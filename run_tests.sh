#!/usr/bin/env bash

set -euo pipefail

script_dir=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &> /dev/null && pwd)
venv_dir="${script_dir}"/venv

source ~/.bashrc
./scripts/ensure_venv.sh
source "${venv_dir}"/bin/activate

echo INFO Running lightcone tests

python3 -m pytest "${script_dir}"/tests