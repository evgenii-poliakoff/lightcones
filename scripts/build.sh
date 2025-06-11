#!/usr/bin/env bash

set -euo pipefail

script_dir=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &> /dev/null && pwd)
conda_env_dir="${script_dir}"/../conda-env

eval "$($HOME/miniforge3/bin/conda shell.bash hook)"

echo INFO Building lightcones package

conda build "${script_dir}"/../conda-recipe