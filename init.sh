#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

echo "Cloning submodules..."
git submodule update --init --recursive

echo "Entering rpi-rgb-led-matrix directory..."
cd rpi-rgb-led-matrix

echo "Updating package list and installing dependencies..."
sudo apt-get update
sudo apt-get install -y python3-dev python3-pillow

echo "Building and installing Python bindings..."
make build-python PYTHON=$(command -v python3)
sudo make install-python PYTHON=$(command -v python3)

cd ..

echo "Installing Python dependencies from requirements..."
pip install -r requirements.txt

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
EOL

sudo systemctl daemon-reload
sudo systemctl enable $SERVICE_NAME
sudo systemctl start $SERVICE_NAME
echo "Systemd service $SERVICE_NAME created, enabled, and started."

echo "Script completed successfully."
