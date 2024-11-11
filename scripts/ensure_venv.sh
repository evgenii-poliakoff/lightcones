#!/usr/bin/env bash

script_dir=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &> /dev/null && pwd)

set -euo pipefail

venv_dir="${script_dir}"/../venv

is_force='false'

while [[ $# -gt 0 ]]; do
    case $1 in
        -f|--force)
            is_force='true'
            shift
            ;;
        *)
            echo ERROR "Unknown option: '$1'"
            echo "Usage: $(basename $0) [-f|--force]"
            exit 1
            ;;
    esac
done

if [[ -d "${venv_dir}" ]] ; then
    if [[ "${is_force}" == 'true' ]] ; then
        echo INFO "Removing '${venv_dir}' Python virtual environment directory"
        rm -rf "${venv_dir}"
    else
        echo INFO "Python virtual environment already exists at '${venv_dir}'. Skipping creating"
        exit 0
    fi
fi

echo INFO "Creating Python virtual environment in '${venv_dir}' directory"

mkdir -p  "${venv_dir}"
source ~/.bashrc
python3 -m venv "${venv_dir}"
source "${venv_dir}"/bin/activate
python3 -m pip install --upgrade pip
python3 -m pip install --upgrade -r "${script_dir}"/../requirements.txt