#!/bin/sh
# create docker group (if not already exists)
sudo groupadd docker

# add the current user to docker group
sudo usermod -aG docker $USER

# change docker group premissions
sudo chown "$USER":"$USER" /home/"$USER"/.docker -R
sudo chmod g+rwx "$HOME/.docker" -R

# log out and in from the current user to commit the cahges
su $USER
