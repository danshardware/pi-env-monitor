#!/bin/bash

apt-get update -qq > /dev/null 2>&1
apt-get upgrade -qq > /dev/null 2>&1

# Install required packages
apt-get install -q -y python3-rpi.gpio 
pip3 install Pillow

# Create directories
mkdir -p /var/pi-env/captures/tsd
chown -R pi /var/pi-env/captures
touch /var/log/captures.log && chown pi /var/log/captures.log

# TODO: Check if we should install with links to here or copy to final folder
if [ "$DEVELOPMENT" -eq "" ]; then
    # real install, copy everything
else
    # make symlinks
fi

# Copy/link files where they need to go
# Add startup scripts
