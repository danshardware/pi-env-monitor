#!/bin/bash

apt-get update -qq > /dev/null 2>&1
apt-get install -q -y python3-rpi.gpio 
pip3 install Pillow

# TODO: Check if we should install with links to here or copy to final folder

# Install required packages
# Copy/link files where they need to go
# Add startup scripts
