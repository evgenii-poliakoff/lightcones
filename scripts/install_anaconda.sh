#! /bin/sh

wget https://repo.anaconda.com/archive/Anaconda3-2023.09-0-Linux-x86_64.sh
bash ~/Anaconda3-2023.09-0-Linux-x86_64.sh -b -p $HOME/anaconda3
eval "$($HOME/anaconda3/bin/conda shell.bash hook)"
conda init