#!/bin/bash

# Update & install essentials
sudo apt update && sudo apt upgrade -y
sudo apt install python3.10 python3.10-venv python3.10-dev python3-pip git unzip -y

# Navigate to project directory (assume it's in home dir)
cd ~/ 

# Setup Python virtual environment
python3.10 -m venv venv
source venv/bin/activate

# Install Python packages
pip install --upgrade pip
pip install -r requirements.txt

echo "Environment setup complete!"
