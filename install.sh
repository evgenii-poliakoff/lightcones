#!/usr/bin/env bash

script_dir=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &> /dev/null && pwd)
venv_dir="${script_dir}"/venv

source ~/.bashrc
./scripts/ensure_venv.sh
source "${venv_dir}"/bin/activate

echo INFO Installing lightcones package

python3 -m pip install --force-reinstall ./wheels/lightcones-0.0.1-py3-none-any.whl