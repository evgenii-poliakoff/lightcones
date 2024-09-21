#! /bin/sh

. ./scripts/read_setup_cfg.sh
bash ./scripts/install_anaconda.sh
bash ./scripts/install_intel_oneapi.sh

# reload ~/.bashrc if anaconda python was installed
if [ -n "$INSTALL_ANACONDA" ] && [ "$INSTALL_ANACONDA" == "yes" ]; then
    source ~/.bashrc
    conda activate base
fi

python3 -m pip install -r requirements.txt
