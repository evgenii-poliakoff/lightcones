#!/usr/bin/env bash

set -euo pipefail

script_dir=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &> /dev/null && pwd)

echo INFO Cleaning up build artifacts in the repository

rm -rf "${script_dir}"/build
rm -rf "${script_dir}"/lightcones.egg-info
rm -rf "${script_dir}"/wheels
rm -rf "${script_dir}"/venv
find ./lightcones -name "*.so" -delete
