## Setup kube state metrics to enable more queries

Kube State metrics is a service that talks to the Kubernetes API server to get all the details about all the API objects like deployments, pods, daemonsets, Statefulsets, etc.

## 1. Clone following repo into a subdirectory (you could f.e. name the subdirectory kube-state-metrics)

Note: it already exists in this project-dir or you could also just copy file by file

```sh
  git clone https://github.com/devopscube/kube-state-metrics-configs.git
```

## 2. Create all the objects for kubernetes by pointing to this file

```sh
  kubectl apply -f kube-state-metrics/
```

## 3. Check the deployment status

```sh
  kubectl get deployments kube-state-metrics -n kube-system
```

## 4. Edit your prometheus config map by adding following context

```sh
  - job_name: 'kube-state-metrics'
  static_configs:
    - targets: ['kube-state-metrics.kube-system.svc.cluster.local:8080']
```
