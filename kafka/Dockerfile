FROM python:3.9-slim-buster

# Install necessary packages
RUN apt-get update && apt-get install -y \
    openjdk-11-jre-headless \
    wget \
    gcc \
    g++ \
    make \
    build-essential \
    librdkafka-dev \
    && rm -rf /var/lib/apt/lists/*

# Install ping
RUN apt-get update && apt-get install -y iputils-ping
RUN apt-get update && apt-get install -y net-tools  # For netstat

# Install Python dependencies
COPY requirements.txt /app/requirements.txt
RUN pip3 install --upgrade pip
RUN pip3 install --no-cache-dir -r /app/requirements.txt

# Copy and set permissions for the wait-for-it script
COPY wait-for-it.sh /wait-for-it.sh
RUN chmod +x /wait-for-it.sh

# Copy Kafka configuration and producer script into the image
COPY kafka_producer.py /app/kafka_producer.py