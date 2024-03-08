#!/bin/bash

# Define the file and section
CONFIG_FILE="setup.cfg"
SECTION="build_ext"
KEY="fcompiler"

# Use sed to extract the value of fcompiler
fcompiler=$(sed -n "/^\[${SECTION}\]/,/^\[/ {/^${KEY}=/p}" $CONFIG_FILE | awk -F'=' '{print $2}')

export FCOMPILER="$fcompiler"

# Print the value to confirm it was successfully read
echo "Detected fcompiler value: $FCOMPILER"