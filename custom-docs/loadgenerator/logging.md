## This doc should help you in setting up, configuring and build the loadgenerator with locust for monitoring your system

1. Get the logs of the system

```sh
kubectl get logs
```

2. Copy all logs into text-file

```sh
kubectl logs **pod-id** > /root/meine_logs.txt
```