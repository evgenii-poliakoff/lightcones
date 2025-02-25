#!/usr/bin/env bash

# you can run a specific test function "test_something()"
# by running this script as
# run_tests.sh -k "test_something"

set -euo pipefail

script_dir=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &> /dev/null && pwd)
venv_dir="${script_dir}"/venv

source ~/.bashrc
./scripts/ensure_venv.sh
source "${venv_dir}"/bin/activate

echo INFO Running lightcone tests

python3 -m pytest -n 8 "${script_dir}"/tests "$@"