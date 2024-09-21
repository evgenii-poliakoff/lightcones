#!/bin/bash

./scripts/install_requirements.sh
./build.sh
source ~/.bashrc
conda activate base
python3 -m pytest ./tests