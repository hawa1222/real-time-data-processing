#!/usr/bin/env python3

import time
import os
import logging
import json

import requests
import kafka
from kafka import KafkaProducer
from kafka.errors import NoBrokersAvailable

# Configure logging to display messages at INFO level and above
LOGGING_LEVEL = os.getenv('LOGGING_LEVEL', 'INFO')
logging.basicConfig(level=LOGGING_LEVEL, format='%(asctime)s - %(levelname)s - %(message)s', 
                    datefmt='%Y-%m-%d %H:%M:%S')

# Set Kafka related logs to WARNING to reduce output verbosity
logging.getLogger('kafka').setLevel(LOGGING_LEVEL)

# Constants
API_KEY = os.getenv('API_KEY')
# Fetch the stock symbols from the environment variable and split it into a list
STOCK_SYMBOLS = os.getenv('STOCK_SYMBOLS', 'AAPL').split(',')
# Generate the list of URLs for each stock symbol
URLS = [f'https://financialmodelingprep.com/api/v3/quote/{symbol}?apikey={API_KEY}' for symbol in STOCK_SYMBOLS]

KAFKA_TOPIC = os.getenv('KAFKA_TOPIC', 'stock_prices')
KAFKA_SERVER = os.getenv('KAFKA_SERVER', 'kafka_broker:29092')
MAX_RETRIES = int(os.getenv('KAFKA_MAX_RETRIES', '5'))
RETRY_DELAY = int(os.getenv('KAFKA_RETRY_DELAY', '2'))

# Log the config variables
logging.info(f'Kafka-Python package version: {kafka.__version__}')

api_key_log = "set" if API_KEY else "not set"
logging.info(f"API_KEY is {api_key_log}.")
logging.info(f"STOCK_SYMBOL: {STOCK_SYMBOLS}")

logging.info(f"KAFKA_SERVER: {KAFKA_SERVER}, KAFKA_TOPIC: {KAFKA_TOPIC}")

# Initialize Kafka producer
def create_producer(server):
    return KafkaProducer(
        bootstrap_servers=[server],
        retries=5,
        retry_backoff_ms=1000,
        request_timeout_ms=30000,
        value_serializer=lambda x: json.dumps(x).encode('utf-8')
    )

for attempt in range(MAX_RETRIES):
    try:
        logging.info(f"Attempting to connect to Kafka broker: {KAFKA_SERVER}, Attempt: {attempt + 1}")
        producer = create_producer(KAFKA_SERVER)
        logging.info("Successfully connected to Kafka broker.")
        break  # Exit the loop on successful connection
    except NoBrokersAvailable as e:
        logging.error(f"Connection attempt {attempt + 1} failed: {str(e)}")
        if attempt < MAX_RETRIES - 1:
            logging.info(f"Retrying in {RETRY_DELAY} seconds...")
            time.sleep(RETRY_DELAY)
        else:
            logging.error("Exhausted all retries. Failed to connect to Kafka broker.")
            raise


# Rest of the producer code
logging.info(f"Producer config: {producer.config}")

def fetch_stock_data(url):
    """
    Fetch stock data from the API.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()  # Will raise an HTTP Error if the HTTP request returned an unsuccessful status code
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        logging.error(f'HTTP error occurred: {http_err}')
    except Exception as err:
        logging.error(f'An error occurred: {err}')

# Continuously fetch and send data
while True:
    logging.info("Current environment:", dict(os.environ))

    for url, symbol in zip(URLS, STOCK_SYMBOLS):
        stock_data = fetch_stock_data(url)

        if stock_data:
            try:
                # Add stock symbol to the data
                stock_data[0]['symbol'] = symbol  # Assuming the API returns a list with a single dictionary
                producer.send(KAFKA_TOPIC, value=stock_data[0])
                logging.info(f"Fetched and sent data for {symbol}: {stock_data}")
            except Exception as e:
                logging.error(f"An error occurred while sending data to Kafka for {symbol}: {e}")

    # Sleep for 60 seconds after each request to rate limit API calls
    time.sleep(60)