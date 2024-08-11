#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

echo -n "Cloning submodules..."
git submodule update --init --recursive >/dev/null
echo "Done."

echo -n "Updating package list and installing dependencies... "
cd rpi-rgb-led-matrix >/dev/null
echo "Done."

sudo apt-get update >/dev/null
sudo apt-get install -y python3-dev python3-pillow >/dev/null

echo -n "Building and installing Python bindings... "
make build-python PYTHON=$(command -v python3) >/dev/null
sudo make install-python PYTHON=$(command -v python3) >/dev/null

cd ..
echo "Done."

echo -n "Installing Python dependencies from requirements... "
pip install -r requirements.txt >/dev/null
echo "Done."

SERVICE_NAME="infomate"
COMMAND_TO_RUN="sudo uvicorn main:app --host 0.0.0.0 --port 8000"

WORKING_DIR="$HOME/Desktop/Infomate/src"
SERVICE_FILE="/etc/systemd/system/$SERVICE_NAME.service"

sudo bash -c "cat > $SERVICE_FILE" <<EOL
[Unit]
Description=Infomate
After=network.target

[Service]
User=$USER
WorkingDirectory=$WORKING_DIR
ExecStart=$COMMAND_TO_RUN
Restart=always

[Install]
WantedBy=multi-user.target
EOL >/dev/null

echo -n "Created systemd service $SERVICE_NAME... "
sudo systemctl daemon-reload >/dev/null
echo "Done."

echo -n "Enable systemd service $SERVICE_NAME... "
sudo systemctl enable $SERVICE_NAME >/dev/null
echo "Done."

echo -n "Start systemd service $SERVICE_NAME... "
sudo systemctl start $SERVICE_NAME >/dev/null
echo "Done."
