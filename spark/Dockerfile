FROM python:3.9-slim-buster

# Install necessary packages
# # Install OpenJDK 11
RUN apt-get update && apt-get upgrade -y && apt-get install -y openjdk-11-jre-headless wget

# Use ARG for specifying Spark and Hadoop versions
ARG SPARK_VERSION=3.3.0
ARG HADOOP_VERSION=3

# Download and install Apache Spark
RUN wget https://archive.apache.org/dist/spark/spark-${SPARK_VERSION}/spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz && \
    tar -xzf spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz && \
    mv spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION} /usr/local/spark && \
    rm spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz

# Set environment variables
ENV SPARK_HOME=/usr/local/spark
ENV PATH=$PATH:$SPARK_HOME/bin

# Install Python dependencies
COPY requirements.txt /app/requirements.txt
RUN pip3 install --no-cache-dir -r /app/requirements.txt

# Copy Spark processing script into the image
COPY process_data.py /app/process_data.py

CMD ["python3", "/app/process_data.py"]