#!/bin/bash

# Define the file and section
CONFIG_FILE="setup.cfg"

# read build_ext/fcompiler

SECTION="build_ext"
KEY="fcompiler"

# Use sed to extract the value of fcompiler
fcompiler=$(sed -n "/^\[${SECTION}\]/,/^\[/ {/^${KEY}=/p}" $CONFIG_FILE | awk -F'=' '{print $2}')

export FCOMPILER="$fcompiler"

# Print the value to confirm it was successfully read
echo "Detected fcompiler value: $FCOMPILER"

# read user_options/install_anaconda

SECTION="user_options"
KEY="install_anaconda"

# Use sed to extract the value of fcompiler
install_anaconda=$(sed -n "/^\[${SECTION}\]/,/^\[/ {/^${KEY}=/p}" $CONFIG_FILE | awk -F'=' '{print $2}')

export INSTALL_ANACONDA="$install_anaconda"

# Print the value to confirm it was successfully read
echo "Detected install_anaconda value: $INSTALL_ANACONDA"