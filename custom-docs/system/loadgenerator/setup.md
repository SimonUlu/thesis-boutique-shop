# Deployment

for current config please check out: [config](../../src/loadgenerator)


## 1. Add external port to loadgenerator deployment to listen to und container
```sh
ports:
  - containerPort: 8089
```

## 2. Add external loadgenerator service to get in the web ui

```sh
##load balancer service
apiVersion: v1
kind: Service
metadata:
  name: loadgenerator-web-ui
spec:
  type: LoadBalancer
  ports:
  - port: 80
    targetPort: 8089
  selector:
    app: loadgenerator
```

## 3. Create external service for loadgenerator

```sh
kubectl apply -f loadgenerator/loadgenerator-service.yaml
```

## 4. Get external ui of loadgen service

```sh
kubectl get services
```

The response will be something like this:
NAME                    TYPE           CLUSTER-IP      EXTERNAL-IP    PORT(S)        AGE
loadgenerator-web-ui    LoadBalancer   10.26.153.251   34.68.77.173   80:32696/TCP   4h16m

visit external-ip in browser of your choice to see to loadgenerator


# Extract stats via logging or prometheus

## Logging


### 1. Get the logs of the system

```sh
kubectl logs **pod-id**
```

### 2. Copy all logs into text-file

```sh
kubectl logs **pod-id** > assets/locust_logs/meine_logs.txt
```

## Extract to prometheus

### 1. Define Prometheus metrics

Define for example the requests and response times metrics as your core metrics

```sh
from prometheus_client import start_http_server, Gauge

# Prometheus-Metriken definieren
REQUESTS = Gauge('locust_requests_total', 'Total number of requests made', ['method', 'name', 'response_code'])
RESPONSE_TIMES = Gauge('locust_response_time_seconds', 'Response times in seconds', ['method', 'name'])
```

### 2. Set up event handler for locust-events

To update the metrics, you need to register event handlers for Locust's request_success and request_failure events. These handlers update the metrics when a request is successful or fails.

```sh
from locust import events
def request_success_handler(request_type, name, response_time, response_length, **_):
    REQUESTS.labels(method=request_type, name=name, response_code="200").inc()
    RESPONSE_TIMES.labels(method=request_type, name=name).set(response_time / 1000.0)

def request_failure_handler(request_type, name, response_time, exception, response_length, response_code, **_):
    REQUESTS.labels(method=request_type, name=name, response_code=str(response_code)).inc()
    RESPONSE_TIMES.labels(method=request_type, name=name).set(response_time / 1000.0)

# Event-Handler an Locust-Events binden
events.request_success.add_listener(request_success_handler)
events.request_failure.add_listener(request_failure_handler)
```

### 3. Start prometheus exporter

To make the metrics available for Prometheus, you need to start an HTTP server that outputs the metrics. You can do this when you start your Locust test.

```sh
# Prometheus Exporter als separaten Thread starten
def start_exporter():
    start_http_server(9091)  # Port, auf dem der Prometheus-Exporter läuft
    while True:
        time.sleep(1)

exporter_thread = threading.Thread(target=start_exporter)
exporter_thread.start()
```



### 4. Delete pod to renew logs

```sh
kubectl delete pod **pod-id**
```
