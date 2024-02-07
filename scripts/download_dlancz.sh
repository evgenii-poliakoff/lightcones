#!/bin/bash

FILEPATH="./dependencies/dlancz.f"
RAW_URL="https://raw.githubusercontent.com/PredictiveScienceLab/py-orthpol/master/src/dlancz.f"
if ! [ -e "$FILEPATH" ]; then
    echo "Downloading file dlancz.f"
    curl --create-dirs -o $FILEPATH -L $RAW_URL
else
    echo "File dlancz.f already exists"
fi