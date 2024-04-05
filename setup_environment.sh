#!/bin/bash

# Stop on the first sign of trouble
set -e

# Create a new conda environment named rtpenv with Python 3.8
echo "Creating a new Conda environment named rtpenv with Python 3.9..."
conda create --name rtpenv python=3.9 -y

# Activate the newly created environment
echo "Activating the rtpenv environment..."
conda activate rtpenv

echo "Installing spyder-kernels for compatibility with Spyder..."
conda install spyder-kernels=2.4 -y

# Install Python dependencies using pip
pip install -r /Users/hadid/GitHub/real-time-data-processing/requirements.txt

echo "Installing Python dependencies from Kafka requirements.txt..."
pip install -r /Users/hadid/GitHub/real-time-data-processing/kafka/requirements.txt

echo "Installing Python dependencies from Spark requirements.txt..."
pip install -r /Users/hadid/GitHub/real-time-data-processing/spark/requirements.txt

echo "Environment setup is complete."

