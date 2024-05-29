## Prometheus Queries that can are helpful for monitoring the kub-cluster

1. CPU-Utilization of the whole system:

```sh
  sum(rate(container_cpu_usage_seconds_total{namespace="default", container!="POD", container!=""}[5m])) by (namespace)
  /
  on(namespace) group_left
  count(kube_pod_info{namespace="default"}) by (namespace)
```

2. CPU Utilization of the single pods

```sh
  sum(rate(container_cpu_usage_seconds_total{namespace="default", container!="POD", container!=""}[5m])) by (pod)
```

3. Memory utilization of the whole system

```sh
  (1 - (node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes)) * 100

  ##or

  sum (container_memory_working_set_bytes{id!="/",pod_name=~"^()()().*$",kubernetes_io_hostname=~"^.*$"}) by (pod_name,kubernetes_io_hostname)

  ##or 
  sum (container_memory_working_set_bytes{id!="/",pod_name=~"^()()().*$",kubernetes_io_hostname=~"^.*$"}) by (pod_name)
```

4. Pod Restart Count

```sh
rate(kube_pod_container_status_restarts_total{namespace="default", container!="POD", container!=""}[5m])
```

5. Network Throughput per Container incoming

```sh
  sum(rate(container_network_receive_bytes_total{namespace="default"}[5m])) by (pod)
```

6. Network throughput all pods

```sh
  sum(rate(container_network_receive_bytes_total{namespace="default"}[5m]))
```

7. Network throughput per container outgoing

```sh
  sum(rate(container_network_transmit_bytes_total{namespace="default"}[5m])) by (pod)
```

8. Network throughput all pods

```sh
  sum(rate(container_network_transmit_bytes_total{namespace="default"}[5m]))
```

9. I/O Metrics Write Speed data gets written to "festplatte" (only available for redis db)

```sh
  sum(rate(container_fs_writes_bytes_total{namespace="default"}[5m]))
```

10. Lesegeschwindigkeiten

```sh
  sum(rate(container_fs_reads_bytes_total{namespace="default"}[5m]))
```
