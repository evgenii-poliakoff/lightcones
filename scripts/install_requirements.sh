#! /bin/sh

. ./scripts/read_setup_cfg.sh
bash ./scripts/install_anaconda.sh
bash ./scripts/install_intel_oneapi.sh
#python3 -m venv ./venv
#source ./venv/bin/activate

# reload ~/.bashrc if anaconda python was installed
if [ -n "$INSTALL_ANACONDA" ] && [ "$INSTALL_ANACONDA" == "yes" ]; then
    source ~/.bashrc
fi

python3 -m pip install -r requirements.txt
