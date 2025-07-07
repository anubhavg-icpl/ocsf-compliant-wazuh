# Create Dockerfile for Logstash pipeline
dockerfile_content = '''# Production-ready Wazuh to OCSF Transformation Pipeline
# Based on Elastic Logstash
FROM docker.elastic.co/logstash/logstash:8.11.0

# Set environment variables
ENV LOGSTASH_HOME=/usr/share/logstash
ENV PATH=$LOGSTASH_HOME/bin:$PATH
ENV LS_SETTINGS_DIR=$LOGSTASH_HOME/config

# Install required plugins
RUN logstash-plugin install logstash-input-opensearch
RUN logstash-plugin install logstash-output-opensearch  
RUN logstash-plugin install logstash-filter-json_encode
RUN logstash-plugin install logstash-filter-ruby

# Create directories
RUN mkdir -p /etc/logstash/conf.d \
    /etc/logstash/templates \
    /etc/logstash/certs \
    /opt/logstash/sincedb \
    /opt/logstash/output \
    /var/log/logstash

# Copy pipeline configuration
COPY wazuh-ocsf-pipeline.conf /etc/logstash/conf.d/
COPY templates/ /etc/logstash/templates/
COPY certs/ /etc/logstash/certs/

# Copy Logstash settings
COPY config/logstash.yml $LS_SETTINGS_DIR/
COPY config/pipelines.yml $LS_SETTINGS_DIR/
COPY config/jvm.options $LS_SETTINGS_DIR/

# Set proper permissions
RUN chown -R logstash:logstash /etc/logstash /opt/logstash /var/log/logstash \
    && chmod 755 /etc/logstash/certs/* \
    && chmod 644 /etc/logstash/conf.d/* \
    && chmod 644 /etc/logstash/templates/*

# Performance and memory optimization
ENV LS_JAVA_OPTS="-Xmx2g -Xms2g"
ENV LS_HEAP_SIZE="2g"

# Pipeline configuration
ENV PIPELINE_WORKERS="4"
ENV PIPELINE_BATCH_SIZE="1000"
ENV PIPELINE_BATCH_DELAY="50"

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
  CMD curl -f http://localhost:9600/_node/stats || exit 1

# Expose monitoring port
EXPOSE 9600

# Switch to logstash user
USER logstash

# Entry point
ENTRYPOINT ["/usr/local/bin/docker-entrypoint"]
CMD ["logstash", "-f", "/etc/logstash/conf.d/wazuh-ocsf-pipeline.conf"]'''

# Save Dockerfile
with open('Dockerfile.logstash', 'w') as f:
    f.write(dockerfile_content)

# Create docker-compose file
docker_compose_content = '''version: '3.8'

services:
  wazuh-ocsf-logstash:
    build:
      context: .
      dockerfile: Dockerfile.logstash
    container_name: wazuh-ocsf-logstash
    restart: unless-stopped
    environment:
      # Wazuh Indexer Connection
      - WAZUH_INDEXER_HOST=${WAZUH_INDEXER_HOST:-wazuh-indexer:9200}
      - WAZUH_INDEXER_USER=${WAZUH_INDEXER_USER:-admin}
      - WAZUH_INDEXER_PASSWORD=${WAZUH_INDEXER_PASSWORD:-SecurePassword123!}
      
      # Output OpenSearch Connection  
      - OUTPUT_OPENSEARCH_HOST=${OUTPUT_OPENSEARCH_HOST:-opensearch:9200}
      - OUTPUT_OPENSEARCH_USER=${OUTPUT_OPENSEARCH_USER:-admin}
      - OUTPUT_OPENSEARCH_PASSWORD=${OUTPUT_OPENSEARCH_PASSWORD:-SecurePassword123!}
      
      # External SIEM Integration (optional)
      - EXTERNAL_SIEM_ENABLED=${EXTERNAL_SIEM_ENABLED:-false}
      - EXTERNAL_SIEM_URL=${EXTERNAL_SIEM_URL:-}
      - EXTERNAL_SIEM_TOKEN=${EXTERNAL_SIEM_TOKEN:-}
      
      # Performance tuning
      - LS_JAVA_OPTS=-Xmx2g -Xms2g
      - PIPELINE_WORKERS=4
      - PIPELINE_BATCH_SIZE=1000
      - PIPELINE_BATCH_DELAY=50
    ports:
      - "9600:9600"  # Monitoring API
      - "5044:5044"  # Beats input (if needed)
    volumes:
      - ./config:/usr/share/logstash/config:ro
      - ./templates:/etc/logstash/templates:ro
      - ./certs:/etc/logstash/certs:ro
      - logstash_data:/opt/logstash
      - logstash_logs:/var/log/logstash
    networks:
      - wazuh-ocsf-network
    depends_on:
      - wazuh-indexer
      - opensearch
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:9600/_node/stats"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 60s
    logging:
      driver: "json-file"
      options:
        max-size: "100m"
        max-file: "5"

  # Mock Wazuh Indexer for testing
  wazuh-indexer:
    image: opensearchproject/opensearch:2.11.0
    container_name: wazuh-indexer
    environment:
      - cluster.name=wazuh-cluster
      - node.name=wazuh-indexer
      - discovery.type=single-node
      - bootstrap.memory_lock=true
      - "OPENSEARCH_JAVA_OPTS=-Xms1g -Xmx1g"
      - "DISABLE_INSTALL_DEMO_CONFIG=true"
      - "DISABLE_SECURITY_PLUGIN=false"
    ulimits:
      memlock:
        soft: -1
        hard: -1
    volumes:
      - wazuh_indexer_data:/usr/share/opensearch/data
    ports:
      - "9201:9200"
    networks:
      - wazuh-ocsf-network

  # Output OpenSearch for OCSF events
  opensearch:
    image: opensearchproject/opensearch:2.11.0
    container_name: ocsf-opensearch
    environment:
      - cluster.name=ocsf-cluster
      - node.name=ocsf-opensearch
      - discovery.type=single-node
      - bootstrap.memory_lock=true
      - "OPENSEARCH_JAVA_OPTS=-Xms2g -Xmx2g"
      - "DISABLE_INSTALL_DEMO_CONFIG=true"
      - "DISABLE_SECURITY_PLUGIN=false"
    ulimits:
      memlock:
        soft: -1
        hard: -1
    volumes:
      - opensearch_data:/usr/share/opensearch/data
    ports:
      - "9200:9200"
    networks:
      - wazuh-ocsf-network

  # OpenSearch Dashboards for visualization
  opensearch-dashboards:
    image: opensearchproject/opensearch-dashboards:2.11.0
    container_name: ocsf-dashboards
    ports:
      - "5601:5601"
    environment:
      - 'OPENSEARCH_HOSTS=["https://opensearch:9200"]'
      - "DISABLE_SECURITY_DASHBOARDS_PLUGIN=false"
    depends_on:
      - opensearch
    networks:
      - wazuh-ocsf-network

  # Prometheus for metrics collection
  prometheus:
    image: prom/prometheus:latest
    container_name: wazuh-ocsf-prometheus
    ports:
      - "9090:9090"
    volumes:
      - ./monitoring/prometheus.yml:/etc/prometheus/prometheus.yml:ro
      - prometheus_data:/prometheus
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.path=/prometheus'
      - '--web.console.libraries=/etc/prometheus/console_libraries'
      - '--web.console.templates=/etc/prometheus/consoles'
      - '--storage.tsdb.retention.time=200h'
      - '--web.enable-lifecycle'
    networks:
      - wazuh-ocsf-network

  # Grafana for monitoring dashboards
  grafana:
    image: grafana/grafana:latest
    container_name: wazuh-ocsf-grafana
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin123
    volumes:
      - grafana_data:/var/lib/grafana
      - ./monitoring/grafana/dashboards:/etc/grafana/provisioning/dashboards:ro
      - ./monitoring/grafana/datasources:/etc/grafana/provisioning/datasources:ro
    depends_on:
      - prometheus
    networks:
      - wazuh-ocsf-network

volumes:
  logstash_data:
  logstash_logs:
  wazuh_indexer_data:
  opensearch_data:
  prometheus_data:
  grafana_data:

networks:
  wazuh-ocsf-network:
    driver: bridge'''

# Save docker-compose file
with open('docker-compose.yml', 'w') as f:
    f.write(docker_compose_content)

print("Docker Configuration Created:")
print("=" * 40)
print("Files created:")
print("- Dockerfile.logstash")
print("- docker-compose.yml")
print(f"Dockerfile size: {len(dockerfile_content)} characters")
print(f"Docker Compose size: {len(docker_compose_content)} characters")