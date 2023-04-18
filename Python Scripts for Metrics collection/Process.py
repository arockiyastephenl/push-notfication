from prometheus_client import Gauge, push_to_gateway, CollectorRegistry
import random
import time

# Create a CollectorRegistry object
registry = CollectorRegistry()

# Create Prometheus Gauge object
gauge = Gauge('my_metric', 'My metric description', registry=registry)

# Set up Pushgateway address and job name
pushgateway_address = 'http://localhost:9091'
job_name = 'my_job'

while True:
    # Generate a random value for the metric
    metric_value = random.randint(0, 100)

    # Set the gauge value
    gauge.set(metric_value)

    # Push the gauge value to the Pushgateway
    push_to_gateway(pushgateway_address, job=job_name, registry=registry)

    # Sleep for a few seconds before generating the next metric
    time.sleep(5)
