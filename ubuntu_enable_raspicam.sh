#!/bin/bash

sudo echo 'start_x=1'| sudo tee -a /boot/firmware/config.txt
sudo reboot
