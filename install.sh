#!/bin/bash
DIR="$( cd "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
DEVELOPMENT=${DEVELOPMENT:=0}

# Install required packages
# we do it this way because it's idempotent
for package in python3-rpi.gpio; do
    export DEBIAN_FRONTEND=noninteractive
    dpkg -l ${package} > /dev/null 2>&1 || apt-get -y -qq install ${package} > /dev/null 2>&1 || echo "Failed to install ${package}"
done
for package in python3-rpi.gpio Adafruit-GPIO Adafruit-PureIO Adafruit-SSD1306 Pillow; do
    # pip3 install --upgrade --no-input -q ${package} || echo "Failed to install ${package}"
    echo "Skipping pip installations"
done

# Create directories
mkdir -p /var/pi-env/captures/tsd
mkdir -p /var/pi-env/captures/resized
mkdir -p /var/log/pi-env
chown -R pi /var/pi-env/captures
chown -R pi /var/log/pi-env

# check if someon forgot to set development mode. 
if [ -L /usr/local/bin/capture.sh ]; then
    echo "Found dev install present. Setting development mode. If you want a regular install, please remove the symlink to capture.sh in /usr/local/bin"
    DEVELOPMENT="1"
fi 

# TODO: Check if we should install with links to here or copy to final folder
if [ "$DEVELOPMENT" -eq "0" ]; then
    # real install, copy everything
    echo "Not Implemented"
else
    # make symlinks
    for f in capture.sh makeThumbnail.py calculateTimeSeries.py; do
        ln -sf "${DIR}/scripts/${f}" "/usr/local/bin/${f}"
    done
    ln -sf "${DIR}/supervisor/supervisor.service" "/etc/systemd/system/supervisor.service"
    ln -sf "${DIR}/scripts/capture.cron" "/etc/cron.d/capture"
    chown root "${DIR}/scripts/capture.cron"
    chmod 644 "${DIR}/scripts/capture.cron"
fi

systemctl daemon-reload

