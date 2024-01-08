#!/bin/bash

wget https://apt.repos.intel.com/intel-gpg-keys/GPG-PUB-KEY-INTEL-SW-PRODUCTS.PUB
apt-key add GPG-PUB-KEY-INTEL-SW-PRODUCTS.PUB
sh -c 'echo deb https://apt.repos.intel.com/oneapi all main > /etc/apt/sources.list.d/oneAPI.list'
apt-get update
apt-get install intel-oneapi-dpcpp-cpp-compiler