#!/usr/bin/env bash

set -euo pipefail

script_dir=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &> /dev/null && pwd)
venv_dir="${script_dir}"/venv

source ~/.bashrc
./scripts/ensure_venv.sh
source "${venv_dir}"/bin/activate

echo INFO Building lightcones package

mkdir -p  "${script_dir}"/build

pushd "${script_dir}"/build

python3 -m numpy.f2py -c --quiet -m _outer ../src/lightcones/outer.f90 --fcompiler=gfortran --f90flags="-Ofast -ffree-line-length-512"
python3 -m numpy.f2py -c --quiet -m _solve ../src/lightcones/solvers/schrodinger/solve.f90 --fcompiler=gfortran --f90flags="-Ofast -ffree-line-length-512"
python3 -m numpy.f2py -c --quiet -m _dlancz ../src/lightcones/linalg/dlancz.f --fcompiler=gfortran --f90flags="-Ofast -ffree-line-length-512"
python3 -m numpy.f2py -c --quiet -m _fastmul ../src/lightcones/linalg/fastmul.f90 --fcompiler=gfortran --f90flags="-Ofast -ffree-line-length-512"

cp _outer.*.so ../lightcones
cp _solve.*.so ../lightcones/solvers/schrodinger
cp _dlancz.*.so ../lightcones/linalg
cp _fastmul.*.so ../lightcones/linalg

popd

python3 setup.py bdist_wheel --dist-dir wheels