#!/bin/bash

FILEPATH1="./dependencies/l_BaseKit_p_2023.0.0.25537_offline.sh"
RAW_URL1="https://registrationcenter-download.intel.com/akdlm/irc_nas/19079/l_BaseKit_p_2023.0.0.25537_offline.sh"
FILEPATH2="./dependencies/l_HPCKit_p_2023.0.0.25400_offline.sh"
RAW_URL2="https://registrationcenter-download.intel.com/akdlm/irc_nas/19084/l_HPCKit_p_2023.0.0.25400_offline.sh"


if ! command -v ifort -v &> /dev/null
then
    echo "Intel Fortran not found. Installing ..."
    curl --create-dirs -o $FILEPATH1 -L $RAW_URL1
    sh ./dependencies/l_BaseKit_p_2023.0.0.25537_offline.sh -l install1.log -a --silent --eula accept 
    curl --create-dirs -o $FILEPATH2 -L $RAW_URL2
    sh ./dependencies/l_HPCKit_p_2023.0.0.25400_offline.sh -l install2.log -a --silent --eula accept 
else
    echo "Intel Fortran is already installed."
fi
