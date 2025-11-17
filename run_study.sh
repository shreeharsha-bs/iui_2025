#!/bin/bash
# Script to run the IUI 2025 User Study with Voila

echo "🚀 Starting IUI 2025 User Study with Voila..."
echo ""

# Check if voila is installed
if ! command -v voila &> /dev/null
then
    echo "⚠ Voila is not installed. Installing now..."
    pip install voila
fi

# Run voila
echo "✓ Starting Voila server..."
echo "📝 The study will open in your browser at http://localhost:8866"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

voila user_study_iui_2025.ipynb --port=8866
