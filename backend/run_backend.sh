#!/usr/bin/env bash
# Optimized EAS build script: skip optional deps to avoid node-gyp issues

cd ~/askgodmobile

echo "🔧 Logging into Expo and starting cloud build (skipping optional deps)..."
# Skip optional dependencies like dtrace-provider
export npm_config_optional=false

# Login (if needed) then build
npx eas login
npx eas build --platform android --profile preview
