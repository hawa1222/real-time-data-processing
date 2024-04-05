#!/usr/bin/env python3

import os
import logging

from pyspark.sql import SparkSession
from pyspark.sql.functions import explode, from_json, current_timestamp, from_unixtime
from pyspark.sql.types import StructField, StructType, StringType, DoubleType, ArrayType, LongType

# Configure logging to display messages at INFO level and above
LOGGING_LEVEL = os.getenv('LOGGING_LEVEL', 'INFO')
logging.basicConfig(level=LOGGING_LEVEL, format='%(asctime)s - %(levelname)s - %(message)s', 
                    datefmt='%Y-%m-%d %H:%M:%S')

# Constants
KAFKA_TOPIC = os.getenv('KAFKA_TOPIC', 'stock_prices')
KAFKA_SERVER = os.getenv('KAFKA_SERVER', 'kafka_broker:29092')

MYSQL_HOST = os.getenv('MYSQL_HOST')
MYSQL_PORT = os.getenv('MYSQL_PORT')
MYSQL_DATABASE = os.getenv('MYSQL_DATABASE')
MYSQL_USER = os.getenv('MYSQL_USER')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')

# Log the config variables
logging.info(f"KAFKA_SERVER: {KAFKA_SERVER}, KAFKA_TOPIC: {KAFKA_TOPIC}")

logging.info(f"MYSQL_HOST: {MYSQL_HOST}, MYSQL_PORT: {MYSQL_PORT}, "
             f"MYSQL_USER: {MYSQL_USER}, MYSQL_DATABASE: {MYSQL_DATABASE}")

password_log = "set" if MYSQL_PASSWORD else "not set"
logging.info(f"MYSQL_PASSWORD is {password_log}.")

# Initialise Spark Session for Structured Streaming
spark = SparkSession.builder \
    .appName("StockPricesProcessor") \
    .config("spark.jars.packages", 
            "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1,mysql:mysql-connector-java:8.0.27") \
    .getOrCreate()

# Set log level to WARN to reduce verbosity of logs
spark.sparkContext.setLogLevel("WARN")

# Define schema for stock data received from Kafka
schema = ArrayType(StructType([
    StructField("name", StringType()),
    StructField("symbol", StringType()),
    StructField("exchange", StringType()),
    StructField("price", DoubleType()),
    StructField("changesPercentage", DoubleType()),
    StructField("timestamp", LongType()),
    # Additional fields can be added here as needed
]))

# Read from Kafka topic as a stream
'''
This step initializes a streaming DataFrame df that connects to your Kafka topic. 
The data fetched from Kafka at this stage is in a binary format, 
with key components like key, value, topic, partition, offset, etc. 
The value field contains your actual message payload, which in your case, is a JSON string.
'''

df = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", KAFKA_SERVER) \
    .option("subscribe", KAFKA_TOPIC) \
    .option("startingOffsets", "earliest") \
    .load()

# Deserialize the JSON data from Kafka and explode the nested array
df_deserialized = df.selectExpr("CAST(value AS STRING)") \
    .select(from_json("value", schema).alias("data")) \
    .select(explode("data").alias("data_flat")) \
    .select("data_flat.*")

# Rename fields using withColumnRenamed
df_renamed = df_deserialized.withColumnRenamed("name", "company_name") \
                             .withColumnRenamed("changesPercentage", "change_percentage")     
                             
# Convert timestamp to readable format, add a timestamp column to indicate when the data was processed
df_with_time = df_renamed.withColumn("readable_timestamp", from_unixtime("timestamp")) \
                                     .withColumn("load_time", current_timestamp())

def process_and_write_batch_to_mysql(df, epoch_id):
    """
    This function processes each micro-batch (DataFrame) before writing it to MySQL.
    It logs the schema, count, and displays the content of the DataFrame.
    """
    
    try:
        # Print the schema of the DataFrame
        df.printSchema()
        
        # Log the count of records in the micro-batch
        record_count = df.count()
        logging.info(f"Batch {epoch_id} count: {record_count}")

        # Collect the data as a list and print it
        data_list = df.collect()
        for row in data_list:
            logging.info(f"Data: {row}")

        # Write the DataFrame to MySQL if it's not empty
        if record_count > 0:
            df.write \
              .format('jdbc') \
              .option("url", f'jdbc:mysql://{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}') \
              .option("dbtable", f'new_{KAFKA_TOPIC}') \
              .option("user", MYSQL_USER) \
              .option("password", MYSQL_PASSWORD) \
              .option("driver", "com.mysql.cj.jdbc.Driver") \
              .mode("append") \
              .save()
        else:
            logging.info(f"Batch {epoch_id} is empty. No data written to MySQL.")
    except Exception as e:
        # Log the error in case of an exception
        logging.info(f"An error occurred processing batch {epoch_id}: {str(e)}")


# Use the combined function with foreachBatch
df_with_time.writeStream \
    .foreachBatch(process_and_write_batch_to_mysql) \
    .outputMode("append") \
    .option("checkpointLocation", "./checkpoint") \
    .start() \
    .awaitTermination()
