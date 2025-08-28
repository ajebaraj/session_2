#!/bin/bash

echo "Starting Flask Full-Stack Application..."

# Check if Python is installed
if ! command -v python &> /dev/null; then
    echo "Error: Python is not installed or not in PATH"
    exit 1
fi

# Check if required packages are installed
echo "Checking dependencies..."
python -c "import flask, werkzeug, PIL" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "Installing dependencies..."
    pip install -r requirements.txt
fi

# Create uploads directory if it doesn't exist
mkdir -p uploads

# Check if images exist, create them if they don't
if [ ! -f "static/images/cat.jpg" ]; then
    echo "Creating placeholder images..."
    python create_images.py
fi

# Start the Flask server
echo "Starting Flask server on http://localhost:5000"
echo "Press Ctrl+C to stop the server"
python app.py
