#!/bin/bash

read -r -p "Accept running will remove all old cuda* nvidia* libnvidia* installations - Are you sure? [y/N] " response
if [[ ! "$response" =~ ^([yY][eE][sS]|[yY])$ ]]
then
    echo "Aborting"
    exit 0
fi

if [ $(lspci |grep -o NVIDIA |wc -l) == 0 ]; then
    echo "Your GPU is not a CUDA-capable"
    exit 0
fi

# https://docs.omniverse.nvidia.com/app_isaacsim/app_isaacsim/requirements.html

# set sources.list to http://us instead of http://il
sudo sed -i s/http:\\/\\/il/http:\\/\\/us/g /etc/apt/sources.list

sudo apt-get update

# remove old version
sudo apt purge -y cuda* nvidia* libnvidia*
sudo apt autoremove -y

# Install NVIDIA Driver:

wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/cuda-ubuntu2004.pin
sudo mv cuda-ubuntu2004.pin /etc/apt/preferences.d/cuda-repository-pin-600
wget https://developer.download.nvidia.com/compute/cuda/11.7.0/local_installers/cuda-repo-ubuntu2004-11-7-local_11.7.0-515.43.04-1_amd64.deb
sudo dpkg -i cuda-repo-ubuntu2004-11-7-local_11.7.0-515.43.04-1_amd64.deb
sudo cp /var/cuda-repo-ubuntu2004-11-7-local/cuda-*-keyring.gpg /usr/share/keyrings/
sudo apt-get update
sudo apt-get -y install cuda
rm cuda-*.deb

sudo restart





