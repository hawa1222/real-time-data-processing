FROM grafana/grafana:8.3.0

# Copy datasource and dashboard configuration files
COPY datasource.yml /etc/grafana/provisioning/datasources/
COPY stock_data_dashboard.json /etc/grafana/provisioning/dashboards/
COPY dashboard.yml /etc/grafana/provisioning/dashboards/

USER root
# Install MySQL client and dependencies
RUN apk add --no-cache mysql-client mariadb-connector-c

USER grafana