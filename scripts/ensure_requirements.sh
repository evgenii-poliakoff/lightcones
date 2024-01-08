#! /bin/sh

CURRENT_DEVENV_VERSION="0.0.0"
export CURRENT_DEVENV_VERSION="0.0.0"

CI_PATH_PREFIX = "$HOME/ci"
export CI_PATH_PREFIX

FILE_PATH="$CI_PATH_PREFIX/version.sh"

if [ ! -f "$FILE_PATH" ]
then
   ./scripts/install_requirements.sh
else
    $CI_PATH_PREFIX/version.sh
    if ["$CURRENT_DEVENV_VERSION" != "$DEVENV_VERSION"] then
        ./scripts/install_requirements.sh
    fi
fi



