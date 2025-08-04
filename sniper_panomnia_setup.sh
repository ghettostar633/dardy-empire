#!/bin/bash

echo "🔮 Installing Panomnia Sniper Requirements..."

# Update system
pkg update -y && pkg upgrade -y

# Python and pip
pkg install python git curl ffmpeg sox -y
pip install flask vosk numpy opencv-python pillow matplotlib

# Create sniper folder
mkdir -p ~/panomnia_sniper/static/uploads
cd ~/panomnia_sniper

# Download Vosk model (tiny)
curl -L -o vosk-model-small-en-us-0.15.zip https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip
unzip vosk-model-small-en-us-0.15.zip -d .
mv vosk-model-small-en-us-0.15 model

echo "✅ Panomnia Sniper Core Installed."
