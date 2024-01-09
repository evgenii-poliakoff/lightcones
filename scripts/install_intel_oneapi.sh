#!/bin/bash

if ! command -v ifort -v &> /dev/null
then
    echo "Intel Fortran not found. Installing ..."
    wget https://registrationcenter-download.intel.com/akdlm/irc_nas/19079/l_BaseKit_p_2023.0.0.25537_offline.sh
    sh ./l_BaseKit_p_2023.0.0.25537_offline.sh -l install1.log -a --silent --eula accept 
    wget https://registrationcenter-download.intel.com/akdlm/irc_nas/19084/l_HPCKit_p_2023.0.0.25400_offline.sh
    sh ./l_HPCKit_p_2023.0.0.25400_offline.sh -l install2.log -a --silent --eula accept 
else
    echo "Intel Fortran is already installed."
fi