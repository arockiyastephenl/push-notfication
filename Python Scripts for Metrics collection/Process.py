from prometheus_client import Gauge, push_to_gateway

# Collect metric
metric_value = 123

# Create Prometheus Gauge object
gauge = Gauge('my_metric', 'My metric description')

# Set gauge value
gauge.set(metric_value)

# Push gauge value to Pushgateway
push_to_gateway('http://localhost:9091', job='my_job', registry=gauge._registry)
