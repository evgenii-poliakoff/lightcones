#! /bin/sh

./scripts/version.sh
export CURRENT_DEVENV_VERSION=$DEVENV_VERSION

CI_PATH_PREFIX="$HOME/ci"
export CI_PATH_PREFIX

FILE_PATH="$CI_PATH_PREFIX/version.sh"

if [ ! -f "$FILE_PATH" ]
then
    echo "Version not found: Installing requirements."
   ./scripts/install_requirements.sh
else
    $CI_PATH_PREFIX/version.sh
    if ["$CURRENT_DEVENV_VERSION" != "$DEVENV_VERSION"] 
    then
        echo "Versions do not match: Installing requirements."
        ./scripts/install_requirements.sh
    else
        echo "Version is up to date: Do not installing requirements."
    fi
fi



