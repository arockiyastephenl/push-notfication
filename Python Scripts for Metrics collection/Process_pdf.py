from prometheus_client import CollectorRegistry, Gauge, push_to_gateway
import random
import time

# Create a CollectorRegistry object
registry = CollectorRegistry()

# Define the processing status metric as a gauge
status_metric = Gauge('my_status_metric', 'My processing status metric', registry=registry)

# Define the number of processed PDFs, failed PDFs, and total PDFs metrics
num_total_metric = Gauge('my_num_total_metric', 'Total number of PDFs', registry=registry)
num_failed_metric = Gauge('my_num_failed_metric', 'Number of failed PDFs', registry=registry)
num_success_metric = Gauge('my_num_success_metric', 'Number of successful PDFs', registry=registry)

# Initialize the number of processed, failed, and total PDFs to 0
num_total = 0
num_failed = 0
num_success = 0

# Loop forever and randomly update the status metric based on PDF processing
while True:
    # Simulate PDF processing
    pdf_exists = random.choice([True, False])
    if pdf_exists:
        processing_successful = random.choice([True, False])
        if processing_successful:
            num_total += 1
            num_success += 1
            status_metric.set(1)
            print("PDF processing successful - status set to 1")
        else:
            num_total += 1
            num_failed += 1
            status_metric.set(0)
            print("PDF processing failed - status set to 0")
    else:
        print("No PDF to process")

    # Update the total PDF, failed PDF, and successful PDF metrics
    num_total_metric.set(num_total)
    num_failed_metric.set(num_failed)
    num_success_metric.set(num_success)

    # Push all three metrics to the Prometheus Pushgateway
    push_to_gateway('http://localhost:9091', job='my_job', registry=registry)

    # Wait for 5 seconds before processing the next PDF
    time.sleep(5)
