#!/data/data/com.termux/files/usr/bin/bash
cd ~/dardy_empire/backend
echo "🚀 Launching Big Holmie Mode Backend..."
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
