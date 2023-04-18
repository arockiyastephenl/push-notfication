# Push Notification

## Problem statements:

When working with a monitoring system that uses a pull-based model, it can be challenging to monitor short-lived or batch jobs that only run for a short period of time. In such cases, it becomes necessary to use a push-based model to collect metrics from these jobs and send them to the monitoring system. However, sending metrics directly from each job can be inefficient and can put additional load on the system. The push gateway is a solution to this problem, as it allows jobs to push their metrics to the gateway, which in turn forwards them to the monitoring system

## What is a push gateway?

  

Push Gateway is a component of the Prometheus monitoring system that allows users to push metrics from short-lived jobs or batch jobs that cannot be scrapped. It is essentially a bridge between non-Prometheus services and the Prometheus server, which enables the collection, storage, and querying of metrics data from these services.

  

With the help of Push Gateway, users can push metrics from their services into the gateway, which then aggregates and stores the data in memory until it is scraped by the Prometheus server. This way, Prometheus can collect metrics data from services that are not able to expose metrics via an HTTP endpoint.

  

Push Gateway is especially useful for collecting metrics data from batch jobs that run for a short period of time and do not have a persistent endpoint to scrape. It also enables users to collect metrics data from legacy systems that do not have native support for Prometheus metrics.

  

## What is a metrics?

Metrics are numerical values used to measure and quantify the performance of systems, applications, and processes. They are collected over time and can include measurements such as response time, CPU utilization, network traffic, and error rates. By analyzing metrics, trends and patterns can be detected, allowing performance issues to be identified and resolved before they impact users. Metrics can be used to optimize system performance, improve user experience, and ensure the reliability and availability of systems and applications.

  

## why do we use pushgateway?

We use the pushgateway to solve the problem of monitoring short-lived or batch jobs in a pull-based monitoring system. In a pull-based system, the monitoring system pulls metrics data from the monitored targets. However, short-lived or batch jobs that run for a short period of time do not have enough time for the monitoring system to pull data from them before they terminate. This leads to a gap in the monitoring data, which can make it difficult to troubleshoot issues.

  

The pushgateway solves this problem by allowing jobs to push their metrics data to the gateway, which acts as an intermediary between the job and the monitoring system. The pushgateway buffers the metrics data until the monitoring system is ready to collect it. This ensures that the monitoring system has access to all the data, even from short-lived or batch jobs.

  

Another benefit of using the pushgateway is that it reduces the load on the monitoring system. Instead of the monitoring system constantly polling for data, the pushgateway acts as a buffer, reducing the number of requests the monitoring system needs to make. This improves the scalability of the monitoring system, as it can handle more monitored targets without being overloaded.

## Architectural diagram:

![](https://lh3.googleusercontent.com/mOlxfJhjRukZguPP05OWdNmw9RGb_cIlwMfwIwec5QxDxqqg7ovBtSXAQiKLVZxBrCiyh8lqmJTBfSEz7QFXQUEl3MVhXumWeXZ8WMWDHz2Je-lDtNJ-ufPL4dYGXGAcu4DOY-ZB388oOcxdfz7KVw)

  

## How to run the Application:

  
  

We are using docker based environment to run the application

  
  

1.  Install Docker on your system if you haven't already. You can download and install Docker from the official Docker website ([https://www.docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop)).
    

  

2.  Clone the push-notification repository: Once Docker is installed, you can clone the push-notification repository by running the following command in your terminal or command
    

    https://github.com/arockiyastephenl/push-notfication.git

This will download the repository's contents into a new directory called "push-notfication" in your current working directory.

3.Add the pushgateway URL to the prometheus.yml config file: In the push-notification repository you just cloned, there should be a file called "prometheus.yml" in the root directory. Open this file in a text editor and add the following lines under the "scrape_configs" section:

prometheus.yml

  
  

    global:
    
    scrape_interval: 15s
    
    evaluation_interval: 15s
    
      
    
    rule_files:
    
    - ./alert.rules.yml
    
      
    
    alerting:
    
    alertmanagers:
    
    - scheme: http
    
    static_configs:
    
    - targets: [ '192.168.43.74:9093' ]
    
      
    
    scrape_configs:
    
    - job_name: 'prometheus'
    
    metrics_path: /metrics
    
    honor_labels: false
    
    honor_timestamps: true
    
    sample_limit: 0
    
    static_configs:
    
    - targets: ['192.168.43.74:9090']
    
      
    
    - job_name: 'pushgateway' # Need to add the target as a pushgateway url
    
    honor_labels: true
    
    metrics_path: '/metrics'
    
    scheme: 'http'
    
    static_configs:
    
    - targets:
    
    - '192.168.43.74:9091'

  

Replace the IP address and port number in the "targets" line with the URL of your pushgateway service.

  

4. Build the Docker services: In the root directory of the push-notification repository, run the following command to build the Docker services:

docker -compose build

5. Run the Docker services: Finally, run the following command to start the Docker services:

docker-compose up -d

The "-d" flag runs the services in detached mode, meaning that they will run in the background and not output any logs or console messages to your terminal. If you want to see the logs for the services, you can run the following command instead:

  

docker-compose up

  

This will start the services in the foreground and output their logs to your terminal. To stop the services, press Ctrl+C in your terminal.

  

## Verify the Services:

  
  

1.  Verify Prometheus service:
    

-   Open a web browser and navigate to [http://localhost:9090/graph](http://localhost:9090/graph)
    
-   This should open the Prometheus web UI, which allows you to explore and visualize the metrics collected by Prometheus.
    
-   In the query box at the top of the page, enter a query for a metric you expect to be collected by Prometheus (e.g. "up" to see the status of all targets).
    
-   Click the "Execute" button to run the query and view the results.
    
-   If you see data in the results, then Prometheus is successfully collecting metrics.
    

![](https://lh5.googleusercontent.com/IrWCp7XyteVPBkTOlbFqm3iCTAFpP8YUg_qzDTqAqN8GTYwJzw0dXxarWLxgPjmgFWz_ORLuZmJ_NugWoC5e6WdkKABqcqsiolz3IiLDui2phAiKzPvDVhFn6cbcLNTLEOJUV2RE35rPfWfMTINNdQ)

  

2. Verify Pushgateway service:

  

-   Open a web browser and navigate to [http://localhost:9091/metrics](http://localhost:9091/metrics)
    
-   This should display a page containing the metrics pushed to Pushgateway by your applications.
    
-   If you see data on this page, then Pushgateway is successfully receiving and storing metrics pushed to it by your applications.
    
-   You can also use a tool like cURL or Postman to send metrics to Pushgateway and verify that they are being received and stored correctly. Here's an example cURL
    

  

curl -X POST -d 'up{job="test"} 1' http://localhost:9091/metrics/job/test

  

This command sends a metric named "up" with a value of 1 and a job label of "test" to Pushgateway. You can then navigate to [http://localhost:9091/metrics](http://localhost:9091/metrics) in your web browser to verify that the metric was received and is being stored correctly.

![](https://lh5.googleusercontent.com/UVxbIaEme35-CnJ4p5aWBWYujf_G_q6yLXxWC2ngkLnkQGRMyligR7KDlqpb6i96NZ9ChpCyPsX6wnP4M1K_RYH-Rr-Em4iXgJeQMX25cJQkR9jxl6nqFPQkW4vYfjqYTB9dcdq9HSjMqQVmF856oQ)

## Illustrate with an Example program

Here is python script:

  

Process.py

from prometheus_client import Gauge, push_to_gateway, CollectorRegistry

import  random

import  time

  

# Create a CollectorRegistry object

registry = CollectorRegistry()

  

# Create Prometheus Gauge object

gauge = Gauge('my_metric', 'My metric description', registry=registry)

  

# Set up Pushgateway address and job name

pushgateway_address = 'http://localhost:9091'

job_name = 'my_job'

  

while  True:

# Generate a random value for the metric

metric_value = random.randint(0, 100)

  

# Set the gauge value

gauge.set(metric_value)

  

# Push the gauge value to the Pushgateway

push_to_gateway(pushgateway_address, job=job_name, registry=registry)

  

# Sleep for a few seconds before generating the next metric

time.sleep(5)

  

  

In this example, we import the necessary modules and create a CollectorRegistry object to hold our metrics. We then create a Gauge object named 'my_metric' with a description of 'My metric description' and associate it with the CollectorRegistry object.

We then set up the address of the Pushgateway and the name of the job we want to associate our metric with.

Finally, we enter an infinite loop where we generate a random value for our metric, set the value of the Gauge object to this value, and push the metric to the Pushgateway using the push_to_gateway() function. We then sleep for a few seconds before generating the next metric. You can modify this loop to generate and push your own custom metrics as needed.

  

### Grafana Dashboard for this sample:

## ![](https://lh4.googleusercontent.com/XKsQIspo3tIBPesHv_iDaUUlT3ori44cdCGvsyQcebEdp0ogPNSHculLAF1yl2Z1AtYjsa19yfxOMgWyoWNMSxZzdD9fOGQqvGQwNK8OKKzCPUYQSnjG8iPyeEu4U9ehQl0uj11ibqmAdRjfTJljCw)

  

Here is Dashboard exported as a JSON:

    {
    
    "annotations": {
    
    "list": [
    
    {
    
    "builtIn": 1,
    
    "datasource": {
    
    "type": "grafana",
    
    "uid": "-- Grafana --"
    
    },
    
    "enable": true,
    
    "hide": true,
    
    "iconColor": "rgba(0, 211, 255, 1)",
    
    "name": "Annotations & Alerts",
    
    "target": {
    
    "limit": 100,
    
    "matchAny": false,
    
    "tags": [],
    
    "type": "dashboard"
    
    },
    
    "type": "dashboard"
    
    }
    
    ]
    
    },
    
    "editable": true,
    
    "fiscalYearStartMonth": 0,
    
    "graphTooltip": 0,
    
    "id": 4,
    
    "links": [],
    
    "liveNow": false,
    
    "panels": [
    
    {
    
    "datasource": {
    
    "type": "prometheus",
    
    "uid": "oUxEgqYVk"
    
    },
    
    "fieldConfig": {
    
    "defaults": {
    
    "color": {
    
    "mode": "palette-classic"
    
    },
    
    "custom": {
    
    "axisCenteredZero": false,
    
    "axisColorMode": "text",
    
    "axisLabel": "",
    
    "axisPlacement": "auto",
    
    "barAlignment": 0,
    
    "drawStyle": "line",
    
    "fillOpacity": 0,
    
    "gradientMode": "none",
    
    "hideFrom": {
    
    "legend": false,
    
    "tooltip": false,
    
    "viz": false
    
    },
    
    "lineInterpolation": "smooth",
    
    "lineWidth": 1,
    
    "pointSize": 5,
    
    "scaleDistribution": {
    
    "type": "linear"
    
    },
    
    "showPoints": "auto",
    
    "spanNulls": false,
    
    "stacking": {
    
    "group": "A",
    
    "mode": "none"
    
    },
    
    "thresholdsStyle": {
    
    "mode": "off"
    
    }
    
    },
    
    "mappings": [],
    
    "thresholds": {
    
    "mode": "absolute",
    
    "steps": [
    
    {
    
    "color": "green",
    
    "value": null
    
    },
    
    {
    
    "color": "red",
    
    "value": 80
    
    }
    
    ]
    
    }
    
    },
    
    "overrides": []
    
    },
    
    "gridPos": {
    
    "h": 9,
    
    "w": 12,
    
    "x": 0,
    
    "y": 0
    
    },
    
    "id": 2,
    
    "options": {
    
    "legend": {
    
    "calcs": [],
    
    "displayMode": "list",
    
    "placement": "bottom",
    
    "showLegend": true
    
    },
    
    "tooltip": {
    
    "mode": "single",
    
    "sort": "none"
    
    }
    
    },
    
    "pluginVersion": "9.4.7",
    
    "targets": [
    
    {
    
    "datasource": {
    
    "type": "prometheus",
    
    "uid": "oUxEgqYVk"
    
    },
    
    "editorMode": "code",
    
    "expr": "my_metric",
    
    "legendFormat": "__auto",
    
    "range": true,
    
    "refId": "A"
    
    }
    
    ],
    
    "title": "Line chart for collected metrics",
    
    "type": "timeseries"
    
    }
    
    ],
    
    "refresh": "",
    
    "revision": 1,
    
    "schemaVersion": 38,
    
    "style": "dark",
    
    "tags": [],
    
    "templating": {
    
    "list": []
    
    },
    
    "time": {
    
    "from": "2023-04-18T06:53:09.509Z",
    
    "to": "2023-04-18T07:11:30.627Z"
    
    },
    
    "timepicker": {},
    
    "timezone": "",
    
    "title": "Demo",
    
    "uid": "ltXbK5E4k",
    
    "version": 1,
    
    "weekStart": ""
    
    }

  
  

## Illustrate with an PDF Process success or failure rate metrics Program:

  

Python script that simulates PDF processing and records metrics related to the processing using the Prometheus Python client library. It pushes these metrics to a Prometheus Pushgateway for later consumption by a Prometheus server.

  

-   Import the required libraries at the beginning of the script:
    

  

    from prometheus_client import CollectorRegistry, Gauge, push_to_gateway  
    import random  
    import  time

  

-   Create a CollectorRegistry object to store the metrics data:
    

    registry = CollectorRegistry()

  

-   Define the my_status_metric metric as a gauge to record the processing status:
    

  

    status_metric = Gauge('my_status_metric', 'My processing status metric', registry=registry)

  

-   Define the my_num_total_metric, my_num_failed_metric, and my_num_success_metric metrics as gauges to record the number of processed, failed, and total PDFs respectively:
    

  

    num_total_metric = Gauge('my_num_total_metric', 'Total number of PDFs', registry=registry)  
    num_failed_metric = Gauge('my_num_failed_metric', 'Number of failed PDFs', registry=registry)  
    num_success_metric = Gauge('my_num_success_metric', 'Number of successful PDFs', registry=registry)  

  

  

-   Initialize the number of processed, failed, and total PDFs to 0:
    

    num_total = 0  
    num_failed = 0  
    num_success = 0  

  

  

-   Start an infinite loop to simulate PDF processing:
    

    while  True:

  

-   Simulate PDF processing by randomly choosing whether a PDF exists and whether its processing was successful:
    

  

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

  
  
  

-   Update the my_num_total_metric, my_num_failed_metric, and my_num_success_metric gauges with the current values of the processed, failed, and total PDFs:
    

  

    num_total_metric.set(num_total)  
    num_failed_metric.set(num_failed)  
    num_success_metric.set(num_success)

  

-   Push all three metrics to the Prometheus Pushgateway for later consumption by a Prometheus server:
    

  

    push_to_gateway('http://localhost:9091', job='my_job', registry=registry)

  
  

-   Wait for 5 seconds before processing the next PDF:
    

  

    time.sleep(5)

  
  

To run the script, save it to a file (e.g. pdf_processor.py) and run it using the command python pdf_processor.py. Note that you will also need to have a Prometheus Pushgateway running at http://localhost:9091 to receive and store the metrics data.

  
  

  

Here is the Full code snippet:

  

Pdf_processor.py

  
  
  

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
  

  
  

### Grafana Dashboard for PDF success and failure:

  

![](https://lh4.googleusercontent.com/Rrmx96NrJKdeEF9mmQ4MWjinvz9UmaANUZlWZtRVv-BejB0JtUEwmoV4lMrbdeuk6vEi8L_VSUA8gh38kFECb5rN9Q3HyN2tT0ETQkGAyPKCjJKd0pSIxLw2GZa0J2WczPqmkmxOPUVvcxy8h_l1Cg)

  

Here is Dashboard exported as a JSON:

  

    {
    
    "annotations": {
    
    "list": [
    
    {
    
    "builtIn": 1,
    
    "datasource": {
    
    "type": "grafana",
    
    "uid": "-- Grafana --"
    
    },
    
    "enable": true,
    
    "hide": true,
    
    "iconColor": "rgba(0, 211, 255, 1)",
    
    "name": "Annotations & Alerts",
    
    "target": {
    
    "limit": 100,
    
    "matchAny": false,
    
    "tags": [],
    
    "type": "dashboard"
    
    },
    
    "type": "dashboard"
    
    }
    
    ]
    
    },
    
    "editable": true,
    
    "fiscalYearStartMonth": 0,
    
    "graphTooltip": 0,
    
    "id": 1,
    
    "links": [],
    
    "liveNow": false,
    
    "panels": [
    
    {
    
    "datasource": {
    
    "type": "prometheus",
    
    "uid": "oUxEgqYVk"
    
    },
    
    "fieldConfig": {
    
    "defaults": {
    
    "mappings": [],
    
    "thresholds": {
    
    "mode": "absolute",
    
    "steps": [
    
    {
    
    "color": "green",
    
    "value": null
    
    }
    
    ]
    
    }
    
    },
    
    "overrides": []
    
    },
    
    "gridPos": {
    
    "h": 8,
    
    "w": 10,
    
    "x": 8,
    
    "y": 0
    
    },
    
    "id": 2,
    
    "options": {
    
    "orientation": "auto",
    
    "reduceOptions": {
    
    "calcs": [
    
    "lastNotNull"
    
    ],
    
    "fields": "",
    
    "values": false
    
    },
    
    "showThresholdLabels": false,
    
    "showThresholdMarkers": true
    
    },
    
    "pluginVersion": "9.4.7",
    
    "targets": [
    
    {
    
    "datasource": {
    
    "type": "prometheus",
    
    "uid": "oUxEgqYVk"
    
    },
    
    "editorMode": "builder",
    
    "expr": "my_num_total_metric{job=\"my_job\"}",
    
    "legendFormat": "__auto",
    
    "range": true,
    
    "refId": "A"
    
    }
    
    ],
    
    "title": "Total Number of PDF",
    
    "type": "gauge"
    
    },
    
    {
    
    "datasource": {
    
    "type": "prometheus",
    
    "uid": "oUxEgqYVk"
    
    },
    
    "fieldConfig": {
    
    "defaults": {
    
    "mappings": [],
    
    "thresholds": {
    
    "mode": "absolute",
    
    "steps": [
    
    {
    
    "color": "green",
    
    "value": null
    
    }
    
    ]
    
    },
    
    "unit": "short"
    
    },
    
    "overrides": []
    
    },
    
    "gridPos": {
    
    "h": 4,
    
    "w": 5,
    
    "x": 8,
    
    "y": 8
    
    },
    
    "id": 8,
    
    "options": {
    
    "colorMode": "value",
    
    "graphMode": "area",
    
    "justifyMode": "auto",
    
    "orientation": "auto",
    
    "reduceOptions": {
    
    "calcs": [
    
    "lastNotNull"
    
    ],
    
    "fields": "",
    
    "values": false
    
    },
    
    "textMode": "auto"
    
    },
    
    "pluginVersion": "9.4.7",
    
    "targets": [
    
    {
    
    "datasource": {
    
    "type": "prometheus",
    
    "uid": "oUxEgqYVk"
    
    },
    
    "editorMode": "builder",
    
    "expr": "my_num_success_metric{job=\"my_job\"}",
    
    "legendFormat": "__auto",
    
    "range": true,
    
    "refId": "A"
    
    }
    
    ],
    
    "title": "Success PDF",
    
    "type": "stat"
    
    },
    
    {
    
    "datasource": {
    
    "type": "prometheus",
    
    "uid": "oUxEgqYVk"
    
    },
    
    "fieldConfig": {
    
    "defaults": {
    
    "mappings": [],
    
    "thresholds": {
    
    "mode": "percentage",
    
    "steps": [
    
    {
    
    "color": "green",
    
    "value": null
    
    }
    
    ]
    
    }
    
    },
    
    "overrides": []
    
    },
    
    "gridPos": {
    
    "h": 4,
    
    "w": 5,
    
    "x": 13,
    
    "y": 8
    
    },
    
    "id": 12,
    
    "options": {
    
    "orientation": "auto",
    
    "reduceOptions": {
    
    "calcs": [
    
    "lastNotNull"
    
    ],
    
    "fields": "",
    
    "values": false
    
    },
    
    "showThresholdLabels": false,
    
    "showThresholdMarkers": true
    
    },
    
    "pluginVersion": "9.4.7",
    
    "targets": [
    
    {
    
    "datasource": {
    
    "type": "prometheus",
    
    "uid": "oUxEgqYVk"
    
    },
    
    "editorMode": "code",
    
    "expr": "my_num_success_metric / my_num_total_metric * 100",
    
    "legendFormat": "__auto",
    
    "range": true,
    
    "refId": "A"
    
    }
    
    ],
    
    "title": "Success Percentage",
    
    "type": "gauge"
    
    },
    
    {
    
    "datasource": {
    
    "type": "prometheus",
    
    "uid": "oUxEgqYVk"
    
    },
    
    "fieldConfig": {
    
    "defaults": {
    
    "mappings": [],
    
    "thresholds": {
    
    "mode": "absolute",
    
    "steps": [
    
    {
    
    "color": "green",
    
    "value": null
    
    },
    
    {
    
    "color": "dark-red",
    
    "value": 0
    
    }
    
    ]
    
    },
    
    "unit": "short"
    
    },
    
    "overrides": []
    
    },
    
    "gridPos": {
    
    "h": 4,
    
    "w": 5,
    
    "x": 8,
    
    "y": 12
    
    },
    
    "id": 6,
    
    "options": {
    
    "colorMode": "value",
    
    "graphMode": "area",
    
    "justifyMode": "auto",
    
    "orientation": "auto",
    
    "reduceOptions": {
    
    "calcs": [
    
    "lastNotNull"
    
    ],
    
    "fields": "",
    
    "values": false
    
    },
    
    "textMode": "auto"
    
    },
    
    "pluginVersion": "9.4.7",
    
    "targets": [
    
    {
    
    "datasource": {
    
    "type": "prometheus",
    
    "uid": "oUxEgqYVk"
    
    },
    
    "editorMode": "builder",
    
    "expr": "my_num_failed_metric{job=\"my_job\"}",
    
    "legendFormat": "__auto",
    
    "range": true,
    
    "refId": "A"
    
    }
    
    ],
    
    "title": "Failure PDF",
    
    "type": "stat"
    
    },
    
    {
    
    "datasource": {
    
    "type": "prometheus",
    
    "uid": "oUxEgqYVk"
    
    },
    
    "fieldConfig": {
    
    "defaults": {
    
    "mappings": [],
    
    "thresholds": {
    
    "mode": "percentage",
    
    "steps": [
    
    {
    
    "color": "green",
    
    "value": null
    
    },
    
    {
    
    "color": "red",
    
    "value": 0
    
    }
    
    ]
    
    }
    
    },
    
    "overrides": []
    
    },
    
    "gridPos": {
    
    "h": 4,
    
    "w": 5,
    
    "x": 13,
    
    "y": 12
    
    },
    
    "id": 14,
    
    "options": {
    
    "orientation": "auto",
    
    "reduceOptions": {
    
    "calcs": [
    
    "lastNotNull"
    
    ],
    
    "fields": "",
    
    "values": false
    
    },
    
    "showThresholdLabels": false,
    
    "showThresholdMarkers": true
    
    },
    
    "pluginVersion": "9.4.7",
    
    "targets": [
    
    {
    
    "datasource": {
    
    "type": "prometheus",
    
    "uid": "oUxEgqYVk"
    
    },
    
    "editorMode": "code",
    
    "expr": "my_num_failed_metric / my_num_total_metric * 100",
    
    "legendFormat": "__auto",
    
    "range": true,
    
    "refId": "A"
    
    }
    
    ],
    
    "title": "Failure percentage",
    
    "type": "gauge"
    
    },
    
    {
    
    "datasource": {
    
    "type": "prometheus",
    
    "uid": "oUxEgqYVk"
    
    },
    
    "fieldConfig": {
    
    "defaults": {
    
    "color": {
    
    "mode": "continuous-BlPu"
    
    },
    
    "custom": {
    
    "fillOpacity": 65,
    
    "lineWidth": 4,
    
    "spanNulls": false
    
    },
    
    "decimals": 0,
    
    "displayName": "PDF",
    
    "mappings": [
    
    {
    
    "options": {
    
    "0": {
    
    "color": "dark-red",
    
    "index": 0,
    
    "text": "Failure"
    
    },
    
    "1": {
    
    "color": "dark-green",
    
    "index": 1,
    
    "text": "Success"
    
    }
    
    },
    
    "type": "value"
    
    }
    
    ],
    
    "thresholds": {
    
    "mode": "percentage",
    
    "steps": [
    
    {
    
    "color": "green",
    
    "value": null
    
    },
    
    {
    
    "color": "red",
    
    "value": 80
    
    },
    
    {
    
    "color": "#EAB839",
    
    "value": 90
    
    }
    
    ]
    
    }
    
    },
    
    "overrides": []
    
    },
    
    "gridPos": {
    
    "h": 7,
    
    "w": 23,
    
    "x": 1,
    
    "y": 16
    
    },
    
    "id": 10,
    
    "options": {
    
    "alignValue": "center",
    
    "legend": {
    
    "displayMode": "list",
    
    "placement": "bottom",
    
    "showLegend": true
    
    },
    
    "mergeValues": true,
    
    "rowHeight": 1,
    
    "showValue": "always",
    
    "tooltip": {
    
    "mode": "single",
    
    "sort": "none"
    
    }
    
    },
    
    "pluginVersion": "9.4.7",
    
    "targets": [
    
    {
    
    "datasource": {
    
    "type": "prometheus",
    
    "uid": "oUxEgqYVk"
    
    },
    
    "editorMode": "builder",
    
    "exemplar": false,
    
    "expr": "my_status_metric{job=\"my_job\"}",
    
    "format": "table",
    
    "instant": true,
    
    "interval": "",
    
    "legendFormat": "{{label_name}}",
    
    "range": true,
    
    "refId": "A"
    
    }
    
    ],
    
    "title": "success and failure with time series",
    
    "type": "state-timeline"
    
    }
    
    ],
    
    "refresh": "",
    
    "revision": 1,
    
    "schemaVersion": 38,
    
    "style": "dark",
    
    "tags": [],
    
    "templating": {
    
    "list": []
    
    },
    
    "time": {
    
    "from": "now-5m",
    
    "to": "now"
    
    },
    
    "timepicker": {},
    
    "timezone": "",
    
    "title": "PDF PROCESSING DASHBOARD",
    
    "uid": "wSFNOiPVz",
    
    "version": 12,
    
    "weekStart": ""
    
    }






