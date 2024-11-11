#!/usr/bin/env bash

script_dir=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &> /dev/null && pwd)

set -euo pipefail

source "${script_dir}"/read_settings.sh

# Check if install_anacoda is set and if it's 'yes'
if [ -n "$install_anaconda3" ] && [ "$install_anaconda3" == "yes" ]; then
    echo "install_anaconda3 is set to yes, will check for Anaconda3 python dependency..."
    # reload ~/.bashrc if anaconda3 python was installed
    source ~/.bashrc
    # check for conda command
    if ! command -v conda list &> /dev/null
    then
        echo "Anaconda3 not found. Installing ..."
        FILEPATH=""${script_dir}"/dependencies/Anaconda3-2023.09-0-Linux-x86_64.sh"
        RAW_URL="https://repo.anaconda.com/archive/Anaconda3-2023.09-0-Linux-x86_64.sh"
        curl --create-dirs -o $FILEPATH -L $RAW_URL
        bash "${script_dir}"/dependencies/Anaconda3-2023.09-0-Linux-x86_64.sh -b -p $HOME/anaconda3
        eval "$($HOME/anaconda3/bin/conda shell.bash hook)"
        conda init
    else
        echo "Anaconda3 is already installed"
    fi
else
    echo "Iinstall_anaconda3 is not set to yes, will not check for Anaconda3 python dependency."
fi

"${script_dir}"/ensure_venv.sh
