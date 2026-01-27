#!/usr/bin/env bash
# Render build script for PaCo API

set -o errexit  # Exit on error

echo "=================================="
echo "Starting Render Build Process"
echo "=================================="

# Install Python dependencies
echo "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "=================================="
echo "Build completed successfully!"
echo "=================================="
