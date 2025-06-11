#!/usr/bin/env bash

# you can run a specific test function "test_something()"
# by running this script as
# run_tests.sh -k "test_something"

set -euo pipefail

script_dir=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &> /dev/null && pwd)
conda_env_dir="${script_dir}"/../conda-env

echo INFO Running lightcone tests

eval "$($HOME/miniforge3/bin/conda shell.bash hook)"
conda activate "${conda_env_dir}"

python3 -m pytest -n 8 "${script_dir}"/../tests "$@"