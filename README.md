# Real-time Financial Data Processing with Kafka, Spark, MySQL, and Grafana

This project demonstrates a real-time financial data processing pipeline using Apache Kafka, Apache Spark, MySQL, and Grafana, all orchestrated with Docker. The pipeline fetches stock data from the Alpha Vantage API, processes it using Spark, stores the processed data in MySQL, and visualizes it using Grafana.

## Project Objectives

- Set up a real-time data ingestion system using Apache Kafka
- Process streaming data in real-time using Apache Spark
- Store processed data in a MySQL database
- Visualize the processed data using Grafana
- Orchestrate the entire pipeline using Docker

## Prerequisites

- Docker: Install Docker and Docker Compose on your machine.
- Alpha Vantage API Key: Sign up for a free API key at [Alpha Vantage](https://www.alphavantage.co/support/#api-key).

## Project Structure

project/
├── .env
├── README.md
├── config.py
├── docker-compose.yml
├── requirements.txt
├── kafka/
│   ├── Dockerfile
│   ├── kafka_producer.py
│   └── kafka.properties
├── spark/
│   ├── Dockerfile
│   └── process_data.py
├── database/
│   └── Dockerfile
└── grafana/
    ├── Dockerfile
    ├── datasource.yml
    └── dashboard.yml

## Setup Instructions

1. Clone the project repository:

git clone https://github.com/your-username/your-project.git

2. Navigate to the project directory:

cd your-project

3. Create a `.env` file in the project's root directory and provide the necessary environment variables:

ALPHA_VANTAGE_API_KEY=your_api_key
MYSQL_HOST=database
MYSQL_PORT=3306
MYSQL_USER=your_username
MYSQL_PASSWORD=your_password
MYSQL_DATABASE=your_database

Replace `your_api_key`, `your_username`, `your_password`, and `your_database` with your actual values.

4. Build and run the Docker containers:

docker-compose up --build

This command will build the Docker images and start the containers for each service (Kafka, Spark, MySQL, and Grafana).

5. Access the Grafana dashboard:

Open your web browser and visit `http://localhost:3000`. Log in using the default credentials (admin/admin).

6. Configure the Grafana dashboard:

- Add a new data source by selecting MySQL and providing the necessary connection details (host: `database`, database: `your_database`, user: `your_username`, password: `your_password`).
- Import or create a new dashboard to visualize the processed stock data stored in the MySQL database.

## Project Architecture

The project consists of the following components:

- Kafka Producer: A Python script that fetches real-time stock data from the Alpha Vantage API and publishes it to a Kafka topic.
- Kafka: A distributed streaming platform that ingests real-time data from the Kafka Producer and makes it available for processing.
- Spark: A distributed computing system that consumes data from Kafka, processes it in real-time, and stores the processed data in a MySQL database.
- MySQL: A relational database management system used to store the processed stock data.
- Grafana: An open-source platform for data visualization and monitoring, used to create dashboards and visualize the processed stock data.

The project uses a single `requirements.txt` file to manage the Python dependencies for the Kafka producer and Spark processing scripts. The dependencies are installed within the respective Docker containers during the build process.

## Additional Configuration

- Modify the `kafka.properties` file in the `kafka/` directory to adjust Kafka configuration settings if needed.
- Update the `datasource.yml` file in the `grafana/` directory to change the MySQL connection details if required.
- Customize the `dashboard.yml` file in the `grafana/` directory to configure the default Grafana dashboard.

## License

This project is licensed under the [MIT License](LICENSE).
