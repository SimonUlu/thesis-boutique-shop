# Prometheus Monitoring setup on kubernetes cluster

## 1. Connect to your kubernetes cluster and go to root dir (make sure you have admin privileges)

Note: if you are using GKE run this command to make sure you have admin privileges

```sh
  ACCOUNT=$(gcloud info --format='value(config.account)')
    kubectl create clusterrolebinding owner-cluster-admin-binding \
    --clusterrole cluster-admin \
    --user $ACCOUNT
```

## 2. Create namespace monitoring to make sure that the default namespace is only reserverd by application critical pods

```sh
  kubectl create namespace monitoring
```

## 3. Create a file clusterRole.yaml under prometheus-dir (already exists in our project)
   edit config to your needs

```sh
  apiVersion: rbac.authorization.k8s.io/v1
  kind: ClusterRole
  metadata:
    name: prometheus
  rules:
  - apiGroups: [""]
    resources:
    - nodes
    - nodes/proxy
    - services
    - endpoints
    - pods
    verbs: ["get", "list", "watch"]
  - apiGroups:
    - extensions
    resources:
    - ingresses
    verbs: ["get", "list", "watch"]
  - nonResourceURLs: ["/metrics"]
    verbs: ["get"]
  ---
  apiVersion: rbac.authorization.k8s.io/v1
  kind: ClusterRoleBinding
  metadata:
    name: prometheus
  roleRef:
    apiGroup: rbac.authorization.k8s.io
    kind: ClusterRole
    name: prometheus
  subjects:
  - kind: ServiceAccount
    name: default
    namespace: monitoring

```

## 4. Create the role using the following command

```sh
  kubectl create -f prometheus/clusterRole.yaml
```

## 5. Create a file named config-map.yaml (already exists under prometheus dir)

```sh
  apiVersion: v1
  kind: ConfigMap
  metadata:
    name: prometheus-server-conf
    labels:
      name: prometheus-server-conf
    namespace: monitoring
  data:
    prometheus.rules: |-
      groups:
      - name: devopscube demo alert
        rules:
        - alert: High Pod Memory
          expr: sum(container_memory_usage_bytes) > 1
          for: 1m
          labels:
            severity: slack
          annotations:
            summary: High Memory Usage
    prometheus.yml: |-
      global:
        scrape_interval: 5s
        evaluation_interval: 5s
      rule_files:
        - /etc/prometheus/prometheus.rules
      alerting:
        alertmanagers:
        - scheme: http
          static_configs:
          - targets:
            - "alertmanager.monitoring.svc:9093"
      scrape_configs:
        - job_name: 'node-exporter'
          kubernetes_sd_configs:
            - role: endpoints
          relabel_configs:
          - source_labels: [__meta_kubernetes_endpoints_name]
            regex: 'node-exporter'
            action: keep
        - job_name: 'kubernetes-apiservers'
          kubernetes_sd_configs:
          - role: endpoints
          scheme: https
          tls_config:
            ca_file: /var/run/secrets/kubernetes.io/serviceaccount/ca.crt
          bearer_token_file: /var/run/secrets/kubernetes.io/serviceaccount/token
          relabel_configs:
          - source_labels: [__meta_kubernetes_namespace, __meta_kubernetes_service_name, __meta_kubernetes_endpoint_port_name]
            action: keep
            regex: default;kubernetes;https
        - job_name: 'kubernetes-nodes'
          scheme: https
          tls_config:
            ca_file: /var/run/secrets/kubernetes.io/serviceaccount/ca.crt
          bearer_token_file: /var/run/secrets/kubernetes.io/serviceaccount/token
          kubernetes_sd_configs:
          - role: node
          relabel_configs:
          - action: labelmap
            regex: __meta_kubernetes_node_label_(.+)
          - target_label: __address__
            replacement: kubernetes.default.svc:443
          - source_labels: [__meta_kubernetes_node_name]
            regex: (.+)
            target_label: __metrics_path__
            replacement: /api/v1/nodes/${1}/proxy/metrics
        - job_name: 'kubernetes-pods'
          kubernetes_sd_configs:
          - role: pod
          relabel_configs:
          - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_scrape]
            action: keep
            regex: true
          - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_path]
            action: replace
            target_label: __metrics_path__
            regex: (.+)
          - source_labels: [__address__, __meta_kubernetes_pod_annotation_prometheus_io_port]
            action: replace
            regex: ([^:]+)(?::\d+)?;(\d+)
            replacement: $1:$2
            target_label: __address__
          - action: labelmap
            regex: __meta_kubernetes_pod_label_(.+)
          - source_labels: [__meta_kubernetes_namespace]
            action: replace
            target_label: kubernetes_namespace
          - source_labels: [__meta_kubernetes_pod_name]
            action: replace
            target_label: kubernetes_pod_name
        - job_name: 'kube-state-metrics'
          static_configs:
            - targets: ['kube-state-metrics.kube-system.svc.cluster.local:8080']
        - job_name: 'kubernetes-cadvisor'
          scheme: https
          tls_config:
            ca_file: /var/run/secrets/kubernetes.io/serviceaccount/ca.crt
          bearer_token_file: /var/run/secrets/kubernetes.io/serviceaccount/token
          kubernetes_sd_configs:
          - role: node
          relabel_configs:
          - action: labelmap
            regex: __meta_kubernetes_node_label_(.+)
          - target_label: __address__
            replacement: kubernetes.default.svc:443
          - source_labels: [__meta_kubernetes_node_name]
            regex: (.+)
            target_label: __metrics_path__
            replacement: /api/v1/nodes/${1}/proxy/metrics/cadvisor
        - job_name: 'kubernetes-service-endpoints'
          kubernetes_sd_configs:
          - role: endpoints
          relabel_configs:
          - source_labels: [__meta_kubernetes_service_annotation_prometheus_io_scrape]
            action: keep
            regex: true
          - source_labels: [__meta_kubernetes_service_annotation_prometheus_io_scheme]
            action: replace
            target_label: __scheme__
            regex: (https?)
          - source_labels: [__meta_kubernetes_service_annotation_prometheus_io_path]
            action: replace
            target_label: __metrics_path__
            regex: (.+)
          - source_labels: [__address__, __meta_kubernetes_service_annotation_prometheus_io_port]
            action: replace
            target_label: __address__
            regex: ([^:]+)(?::\d+)?;(\d+)
            replacement: $1:$2
          - action: labelmap
            regex: __meta_kubernetes_service_label_(.+)
          - source_labels: [__meta_kubernetes_namespace]
            action: replace
            target_label: kubernetes_namespace
          - source_labels: [__meta_kubernetes_service_name]
            action: replace
            target_label: kubernetes_name

```

Note: After changes restart pod by deleting old pod as follows:

```sh
  ## get pod name before and then delete
  kubectl delete pod prometheus-deployment-96898bbc9-tqmvg
```

## 6. Create config map on your kubernetes cluster

```sh
  ## make sure your file path matches
  kubectl create -f prometheus/config-map.yaml
```

## 7. Create a deployment.yaml file to deploy prometheus to a pod in your namespace monitoring

```sh
  apiVersion: apps/v1
  kind: Deployment
  metadata:
    name: prometheus-deployment
    namespace: monitoring
    labels:
      app: prometheus-server
  spec:
    replicas: 1
    selector:
      matchLabels:
        app: prometheus-server
    template:
      metadata:
        labels:
          app: prometheus-server
      spec:
        containers:
          - name: prometheus
            image: prom/prometheus
            args:
              - "--storage.tsdb.retention.time=12h"
              - "--config.file=/etc/prometheus/prometheus.yml"
              - "--storage.tsdb.path=/prometheus/"
            ports:
              - containerPort: 9090
            resources:
              requests:
                cpu: 500m
                memory: 500M
              limits:
                cpu: 1
                memory: 1Gi
            volumeMounts:
              - name: prometheus-config-volume
                mountPath: /etc/prometheus/
              - name: prometheus-storage-volume
                mountPath: /prometheus/
        volumes:
          - name: prometheus-config-volume
            configMap:
              defaultMode: 420
              name: prometheus-server-conf

          - name: prometheus-storage-volume
            emptyDir: {}
```

## 8. Create the deployment

```sh
  kubectl create  -f prometheus/prometheus-deployment.yaml
```

Note: check if the created deployment was created

```sh
  kubectl get deployments --namespace=monitoring
```

## 9. Now you are good to go to bind your cluster to a port. F.e. with kubectl port forwarding

### 9.1 Get the pod name:

```sh
  kubectl get pods --namespace=monitoring
```

### 9.2 (local) Bind pod to port xxx (change prometheus-monitoring-.. to actual pod name):

```sh
  kubectl port-forward prometheus-monitoring-3331088907-hm5n1 80:9090 -n monitoring
```

### 9.3 (Cloud deployment) Exposing Prometheus as a Service [NodePort & LoadBalancer] 

the service prometheus file generates a loadbalancer service to change to nodeport just change type and also add nodeport:30000

```sh
apiVersion: v1
kind: Service
metadata:
  name: prometheus-service
  namespace: monitoring
  annotations:
    prometheus.io/scrape: 'true'
    prometheus.io/port: '9090'
spec:
  selector:
    app: prometheus-server
  type: LoadBalancer // NodePort
  ports:
    - port: 80
      targetPort: 9090
      // nodePort: 30000
```



## 10. Create the service by using the prior created file

```sh
kubectl create -f prometheus-service.yaml --namespace=monitoring
```

## 11. Get external ip address

```sh
kubectl get services -n monitoring
```

## 12. Add prometheus service so grafana can access the data that is submitted (port binding alone is not enough)

## 13. Now you only have one slight problem:

Kube state metrics target will be down. Check with visiting the url you binded your prometheus server to and then
go to status->targets. This is due to it not being configured. Kube state metrics target is important for generating metrics such as cpu-usage and memory-usage or pod restart count. For further instance follow the docs under [Kube State Metrics Config](prometheus-kube-state-metrics.md)
