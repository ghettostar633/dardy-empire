#!/data/data/com.termux/files/usr/bin/bash

echo "🚀 Starting Dardy Empire Fix Sequence..."

# Step 1: Git Fix
echo "🔧 Fixing Git remote and committing..."
cd ~/dardy_empire || exit 1

# Remove old origin if it exists
git remote remove origin 2>/dev/null

# Add your actual GitHub repo here 👇👇👇
git remote add origin https://github.com/YOUR_USERNAME/dardy_empire.git

# Initialize Git (if needed)
git init
git branch -M main
git add .
git commit -m "Initial commit"
git push -u origin main

# Step 2: Clean Node Modules and Lockfile
echo "🧹 Cleaning
