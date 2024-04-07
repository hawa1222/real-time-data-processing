# Real-time Financial Data Processing with Kafka, Spark, MySQL, and Grafana

This project demonstrates a real-time financial data processing pipeline using Apache Kafka, Apache Spark, MySQL, and Grafana, all orchestrated with Docker. The pipeline fetches stock data from the Financial Modeling Prep API, processes it using Spark, stores the processed data in MySQL, and visualises it using Grafana.

## Project Objectives

- Set up a real-time data ingestion system using Apache Kafka
- Process streaming data in real-time using Apache Spark
- Store processed data in a MySQL database
- Visualise the processed data using Grafana
- Orchestrate the entire pipeline using Docker

## Prerequisites

- Docker: Install Docker and Docker Compose on your machine.
- Financial Modeling Prep API Key: Sign up for a free API key at [Financial Modeling Prep](https://site.financialmodelingprep.com/).

## Setup Instructions

1. Clone the project repository:

   git clone https://github.com/your-username/real-time-data-processing.git

2. Navigate to the project directory:

   cd real-time-data-processing

3. Create a `.env` file in the project's root directory and provide the necessary environment variables:

   FINANCIAL_MODELING_PREP_API_KEY='your_api_key', MYSQL_HOST=database, MYSQL_PORT=3306, MYSQL_USER='your_username', MYSQL_PASSWORD='your_password', MYSQL_DATABASE='your_database', GRAFANA_ADMIN_PASSWORD='your_grafana_admin_password'.

   Replace `your_api_key`, `your_username`, `your_password`, `your_database`, and `your_grafana_admin_password` with your actual values.

4. Build and run the Docker containers:

   docker-compose up --build

   This command will build the Docker images and start the containers for each service (Kafka, Spark, MySQL, and Grafana).

5. Access the Grafana dashboard:

   Open your web browser and visit `http://localhost:3000`. Log in using the admin credentials you provided in the `.env` file.

6. Configure the Grafana dashboard:

   - The MySQL data source should be automatically configured based on the `datasource.yml` file.
   - The default dashboard for visualizing stock data should be imported automatically based on the `stock_data_dashboard.json` file.

## Project Architecture

The project consists of the following components:

- Kafka Producer: A Python script that fetches real-time stock data from the Financial Modeling Prep API and publishes it to a Kafka topic.
- Kafka: A distributed streaming platform that ingests real-time data from the Kafka Producer and makes it available for processing.
- Spark: A distributed computing system that consumes data from Kafka, processes it in real-time, and stores the processed data in a MySQL database.
- MySQL: A relational database management system used to store the processed stock data.
- Grafana: An open-source platform for data visualization and monitoring, used to create dashboards and visualise the processed stock data.

The project uses `requirements.txt` files to manage the Python dependencies for the Kafka producer and Spark processing scripts. The dependencies are installed within the respective Docker containers during the build process.

## Additional Configuration

- Update the `datasource.yml` file in the `grafana/` directory to change the MySQL connection details if required.
- Customise the `stock_data_dashboard.json` file in the `grafana/` directory to modify the default Grafana dashboard.

## License

This project is licensed under the MIT License - see the [LICENSE.txt](LICENSE.txt) file for details.
