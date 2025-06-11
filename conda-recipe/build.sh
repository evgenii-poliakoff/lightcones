#!/bin/bash

export VERSION=$(cat $SRC_DIR/VERSION)

mkdir -p  $SRC_DIR/build
pushd $SRC_DIR/build

export FC=gfortran
export FFLAGS="-Ofast -ffree-line-length-512"

$PYTHON -m numpy.f2py -c --quiet -m _outer $SRC_DIR/src/lightcones/outer.f90 --backend meson
$PYTHON -m numpy.f2py -c --quiet -m _solve $SRC_DIR/src/lightcones/solvers/schrodinger/solve.f90 --backend meson
$PYTHON -m numpy.f2py -c --quiet -m _dlancz $SRC_DIR/src/lightcones/linalg/dlancz.f --backend meson
$PYTHON -m numpy.f2py -c --quiet -m _fastmul $SRC_DIR/src/lightcones/linalg/fastmul.f90 --backend meson

cp _outer.*.so $SRC_DIR/lightcones
cp _solve.*.so $SRC_DIR/lightcones/solvers/schrodinger
cp _dlancz.*.so $SRC_DIR/lightcones/linalg
cp _fastmul.*.so $SRC_DIR/lightcones/linalg

popd

$PYTHON setup.py install