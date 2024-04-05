#!/bin/bash

# Stop on the first sign of trouble
set -e

# Print a message to indicate the start of the environment setup
echo "Starting environment setup..."

# Create a new Python virtual environment named rtpenv in the current directory
echo "Creating a new virtual environment named rtpenv with Python 3.9..."
python3 -m venv rtpenv

# Activate the newly created environment
# Note: The method of activation depends on your shell. The below command works for bash/sh.
echo "Activating the rtpenv environment..."
source rtpenv/bin/activate

# Update pip to its latest version within the virtual environment
echo "Upgrading pip to the latest version..."
pip install --upgrade pip

# Install Python dependencies using pip
echo "Installing Python dependencies from the main requirements.txt..."
pip install -r /Users/hadid/GitHub/real-time-data-processing/requirements.txt

# Below commands install dependencies from those additional requirements.txt files
echo "Installing Python dependencies from Kafka requirements.txt..."
pip install -r /Users/hadid/GitHub/real-time-data-processing/kafka/requirements.txt

echo "Installing Python dependencies from Spark requirements.txt..."
pip install -r /Users/hadid/GitHub/real-time-data-processing/spark/requirements.txt

# Indicate the completion of the environment setup
echo "Environment setup is complete. The virtual environment 'rtpenv' is now ready for use."
