#!/usr/bin/env bash

script_dir=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &> /dev/null && pwd)
venv_dir="${script_dir}"/../venv

mkdir -p  "${venv_dir}"
source ~/.bashrc
python3 -m venv "${venv_dir}"
source "${venv_dir}"/bin/activate
python3 -m pip install --upgrade pip
python3 -m pip install --upgrade -r "${script_dir}"/../requirements.txt