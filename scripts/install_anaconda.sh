#! /bin/sh

# Check if INSTALL_ANACONDA is set and if it's 'yes'
if [ -n "$INSTALL_ANACONDA" ] && [ "$INSTALL_ANACONDA" == "yes" ]; then
    # Continue execution
    echo "INSTALL_ANACONDA is set to intelem, will check for Anaconda3 python dependency..."
else
    # Exit with a message if FCOMPILER is not 'intelem'
    echo "INSTALL_ANACONDA is not set to yes, will not check for Anaconda3 python dependency. Exiting"
    exit 0
fi

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
    