#! /bin/sh

if [ -d "$CI_PREFIX_PATH" ]
then
  rm -r $CI_PREFIX_PATH
fi

mkdir -p $CI_PATH_PREFIX

#./scripts/install_anaconda.sh
#./scripts/install_intel_oneapi.sh

if [ $? -eq 0 ]
then
    SOURCE="./scripts/version.sh"
    DESTINATION="$CI_PATH_PREFIX/"
    cp $SOURCE $DESTINATION
fi