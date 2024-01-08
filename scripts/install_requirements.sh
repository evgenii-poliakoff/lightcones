#! /bin/sh

if [ -d "$CI_PREFIX_PATH" ]
then
  rm -r $CI_PREFIX_PATH
fi

mkdir -p $CI_PATH_PREFIX

./scripts/install_anaconda.sh
./scripts/install_intel_oneapi.sh

if [ $? -eq 0 ]
then
    SOURCE="./scripts/version.sh"
    DESTINATION="$CI_PATH_PREFIX/"
    cp $SOURCE $DESTINATION
    echo "Succesfully udpated requisites to version $CURRENT_DEVENV_VERSION."
else
    echo "There were errors while installing requisites: not updating version."
fi