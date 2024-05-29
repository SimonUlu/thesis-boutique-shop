# Grafana Setup on kubernetes cluster

Note: All files for the setup are provided by Bibin Wilson on his git-repo (git clone https://github.com/bibinwilson/kubernetes-grafana.git)

## 1. Create a folder grafana

## 2. Create a file named grafana-datasource.yaml inside the prior created folder with following content

```sh
  apiVersion: v1
  kind: ConfigMap
  metadata:
    name: grafana-datasources
    namespace: monitoring
  data:
    prometheus.yaml: |-
      {
          "apiVersion": 1,
          "datasources": [
              {
                "access":"proxy",
                  "editable": true,
                  "name": "prometheus",
                  "orgId": 1,
                  "type": "prometheus",
                  "url": "http://prometheus-service.monitoring.svc:8080",
                  "version": 1
              }
          ]
      }
```

## 3. Execute following query to create the configmap needed for grafana service

```sh
  kubectl create -f grafana/grafana-datasource-config.yaml
```

## 4. Create a deployment file inside grafana-folder (this will create the kubernetes-deployment)

```sh
  apiVersion: apps/v1
  kind: Deployment
  metadata:
    name: grafana
    namespace: monitoring
  spec:
    replicas: 1
    selector:
      matchLabels:
        app: grafana
    template:
      metadata:
        name: grafana
        labels:
          app: grafana
      spec:
        containers:
        - name: grafana
          image: grafana/grafana:latest
          ports:
          - name: grafana
            containerPort: 3000
          resources:
            limits:
              memory: "1Gi"
              cpu: "1000m"
            requests:
              memory: 500M
              cpu: "500m"
          volumeMounts:
            - mountPath: /var/lib/grafana
              name: grafana-storage
            - mountPath: /etc/grafana/provisioning/datasources
              name: grafana-datasources
              readOnly: false
        volumes:
          - name: grafana-storage
            emptyDir: {}
          - name: grafana-datasources
            configMap:
                defaultMode: 420
                name: grafana-datasources
```

## 5. Create the deployment by executing following command

```sh
  kubectl create -f grafana/deployment.yaml -n monitoring
```

## 6. Create a service file under grafana-folder

```sh
  apiVersion: v1
  kind: Service
  metadata:
    name: grafana
    namespace: monitoring
    annotations:
        prometheus.io/scrape: 'true'
        prometheus.io/port:   '3000'
  spec:
    selector:
      app: grafana
    type: NodePort
    ports:
      - port: 3000
        targetPort: 3000
        nodePort: 32000
```

## 7. Create the service

```sh
  kubectl create -f grafana/service.yaml -n monitoring
```

## 8. Bind your pod to port

```sh
  ## find out the name of your pod
  kubectl get pods --namespace=monitoring
```

```sh
  ## bind it to port 3000
  kubectl port-forward -n monitoring <grafana-pod-name> 3000 &
```
