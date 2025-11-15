#!/bin/bash
# Setup script for deploying IUI 2025 study to Modal

set -e  # Exit on error

echo "======================================"
echo "IUI 2025 Study - Modal Setup"
echo "======================================"

# Check if Modal is installed
if ! command -v modal &> /dev/null; then
    echo "Installing Modal..."
    pip install modal
else
    echo "✓ Modal already installed"
fi

# Check if user is authenticated
if ! modal token show &> /dev/null; then
    echo ""
    echo "You need to authenticate with Modal."
    echo "This will open a browser window..."
    modal setup
else
    echo "✓ Already authenticated with Modal"
fi

echo ""
echo "======================================"
echo "Testing Setup"
echo "======================================"

# Test the setup
echo "Running setup test..."
modal run modal_app.py::test_setup

echo ""
echo "======================================"
echo "Deployment Options"
echo "======================================"
echo ""
echo "Choose how you want to deploy:"
echo ""
echo "1. Development mode (you see logs, stops when you exit):"
echo "   modal serve modal_app.py"
echo ""
echo "2. Production mode (runs in background, persistent):"
echo "   modal deploy modal_app.py"
echo ""
echo "After deployment, you'll get a URL like:"
echo "https://yourname--iui-2025-voice-study-notebook.modal.run"
echo ""
echo "Share this URL with your study participants!"
echo ""
echo "======================================"
echo "Ready to Deploy"
echo "======================================"
echo ""
read -p "Deploy now in development mode? (y/n) " -n 1 -r
echo ""

if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "Starting deployment..."
    echo ""
    modal serve modal_app.py
else
    echo ""
    echo "Skipping deployment. Run manually when ready:"
    echo "  modal serve modal_app.py"
    echo ""
fi

echo ""
echo "======================================"
echo "Next Steps"
echo "======================================"
echo ""
echo "1. Share the URL with participants"
echo "2. Monitor with: modal app logs iui-2025-voice-study"
echo "3. Download results: modal volume get iui-study-results results/ ./local_results/"
echo ""
