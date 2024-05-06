# This setup utilizes helm charts to setup grafana and prometheus

## This is recommended for testing purposes and standard use-cases as it is very quick but not configurable to receive data from external sources such as locust, etc.

1. Helm Repositorys für beide hinzufügen

   ```sh
    helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
    helm repo update
   ```

   ```sh
     helm repo add grafana https://grafana.github.io/helm-charts
     helm repo update
   ```

2. Installation von prometheus

   ```sh
      kubectl create namespace monitoring
      helm install my-prometheus prometheus-community/kube-prometheus-stack --namespace monitoring
   ```

3. Installation von grafana

   ```sh
      helm install my-grafana grafana/grafana --namespace monitoring
   ```

4. Admin Passwort für Grafana abrufen und in Password-Manager speichern

   ```sh
    kubectl get secret --namespace monitoring my-grafana -o jsonpath="{.data.admin-password}" | base64 --decode ; echo
   ```

5. configure prometheus for being able to receive data from locust

   ```sh
     ### create prometheus-values.yaml in helm-chart dir
     prometheus:
      prometheusSpec:
        additionalScrapeConfigs:
          - job_name: 'locust'
            static_configs:
              - targets: ['loadgenerator:8089']
   ```

   ```sh
    helm upgrade my-prometheus prometheus-community/prometheus -f custom-values.yaml
   ```
