#! /bin/sh

FILEPATH="./dependencies/Anaconda3-2023.09-0-Linux-x86_64.sh"
RAW_URL="https://repo.anaconda.com/archive/Anaconda3-2023.09-0-Linux-x86_64.sh"

if ! command -v conda list &> /dev/null
then
    echo "Anaconda3 not found. Installing ..."
    curl --create-dirs -o $FILEPATH -L $RAW_URL
    bash ./dependencies/Anaconda3-2023.09-0-Linux-x86_64.sh -b -p $HOME/anaconda3
    eval "$($HOME/anaconda3/bin/conda shell.bash hook)"
    conda init
else
    echo "Anaconda3 is already installed"
fi
    