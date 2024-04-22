# Real-time Financial Data Processing Pipeline

This project demonstrates a real-time financial data processing pipeline using Apache Kafka, Apache Spark, MySQL, and Grafana, all orchestrated with Docker. The pipeline fetches stock data from the Financial Modeling Prep API, processes it using Spark, stores the processed data in MySQL, and visualises it using Grafana.

## Project Objectives

- Set up a real-time data ingestion system using Apache Kafka
- Process streaming data in real-time using Apache Spark
- Store processed data in a MySQL database
- Visualise the processed data using Grafana
- Orchestrate the entire pipeline using Docker

## Project Architecture

The project consists of the following components:

- Kafka Producer: A Python script that fetches real-time stock data from the Financial Modeling Prep API and publishes it to a Kafka topic.
- Kafka: A distributed streaming platform that ingests real-time data from the Kafka Producer and makes it available for processing.
- Spark: A distributed computing system that consumes data from Kafka, processes it in real-time, and stores the processed data in a MySQL database.
- MySQL: A relational database management system used to store the processed stock data.
- Grafana: An open-source platform for data visualization and monitoring, used to create dashboards and visualise the processed stock data.

The project uses `requirements.txt` files to manage the Python dependencies for the Kafka producer and Spark processing scripts. The dependencies are installed within the respective Docker containers during the build process.


## Prerequisites

- Python (version 3.12)
- Docker: Install Docker and Docker Compose on your machine.
- Financial Modeling Prep API Key: Sign up for a free API key at [Financial Modeling Prep](https://site.financialmodelingprep.com/).

## Setup Instructions

1. Clone the project repository:
   ```
   git clone https://github.com/hawa1222/real-time-data-processing.git
   ```

2. Navigate to the project directory:
   ```
   cd real-time-data-processing
   ```

3. Set up your environment:

   Make the setup script executable (if it's not already):

   ```
   chmod +x setup_environment.sh
   ```

   Then run the `setup_environment.sh` script to create a virtual environment and install all necessary packages. Execute this script from the root directory of the project:

   ```
   ./setup_environment.sh
   ```

4. Create a `.env` file in the project root directory and provide the environment variables as specified in `.env_template`.


5. Running Spark and Kafka scripts as standalone (Optional):

   If you wish to run the Spark and Kafka Python scripts individually without using Docker, activate the virtual environment created by setup_environment.sh, run zookeeper & kafka locally, and run the scripts from the command line.

   For Kafka:
    ```
   python kafka/kafka_producer.py
   ```

   For Spark:
    ```
   python spark/process_data.py
   ```

6. Build and run the Docker containers:
   ```
   docker-compose up --build
   ```

   This command will build the Docker images and start the containers for each service (Kafka, Spark, MySQL, and Grafana).


7. Access the Grafana dashboard:

   Open your web browser and visit `http://localhost:3000`. Log in using the admin credentials you provided in the `.env` file.

8. Configure the Grafana dashboard:

   - The MySQL data source should be automatically configured based on the `datasource.yml` file.
   - The default dashboard for visualising stock data should be imported automatically based on the `stock_data_dashboard.json` file.


## Additional Configuration

- Update the `.env` file root directory to change the MySQL connection details if required.
- Customise the `stock_data_dashboard.json` file in the `grafana/` directory to modify the default Grafana dashboard.

## License

This project is licensed under the MIT License - see the [LICENSE.txt](LICENSE.txt) file for details.
