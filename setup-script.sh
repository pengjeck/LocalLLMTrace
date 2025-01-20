#!/bin/bash

# Required parameters:
# @raycast.schemaVersion 1
# @raycast.title local-llm
# @raycast.mode compact

# Optional parameters:
# @raycast.icon 🤖
# @raycast.packageName developer utils
# @raycast.needsConfirmation true

# Documentation:
# @raycast.author pen_sir
# @raycast.authorURL https://raycast.com/pen_sir

# Change to project directory
if ! cd /Users/zhiya.pj/code/LocalLLMTrace; then
    echo "Error: Failed to change directory to /Users/zhiya.pj/code/LocalLLMTrace" >&2
    exit 1
fi

# Activate poetry shell
if ! poetry shell; then
    echo "Error: Failed to activate poetry shell" >&2
    exit 1
fi

# Stop existing processes if running
if ! pm2 delete local-llm phoenix-serve; then
    echo "Warning: Failed to stop existing processes - continuing anyway" >&2
fi

# Start local-llm process with PM2
if ! pm2 start main.py --name local-llm --interpreter python3; then
    echo "Error: Failed to start local-llm with PM2" >&2
    exit 1
fi

# Start phoenix server process with PM2
if ! pm2 start "phoenix serve" --name phoenix-serve; then
    echo "Error: Failed to start phoenix server with PM2" >&2
    exit 1
fi

# Save PM2 process list
if ! pm2 save; then
    echo "Warning: Failed to save PM2 process list" >&2
fi

# Show PM2 status
if ! pm2 status; then
    echo "Error: Failed to get PM2 status" >&2
    exit 1
fi
