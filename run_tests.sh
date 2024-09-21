#!/bin/bash

./scripts/install_requirements.sh
./build.sh
#source ./venv/bin/activate
export PYTEST_TIMEOUT=120
strace python3 -m pytest ./tests