# Build
## 1. Ensure you have the following requirements:
    - Google Cloud project.
    - Shell environment with gcloud, git, and kubectl.

## 2. Clone the last version 

```sh
    git clone <repo_url>
```

## 3. Enable container api on google cloud project (create project before if not done with step 1 in google cloud console)

```sh
gcloud services enable container.googleapis.com \
  --project=${PROJECT_ID}
```

## 4. Create the cluster for further details check docs 

#### Flags:

- `--disk-size=50GB`: Defines the size of the disk for each node in the cluster. In this example, it is set to 50GB.
- `--enable-autoupgrade`:  If set, Google Cloud allows the nodes in the cluster to be updated automatically when new versions of the Kubernetes Engine are available.
- `--enable-autoscaling`: Activates the automatic scaling of the number of nodes in the cluster based on the workload.
  - `--min-nodes=3`: Sets the minimum number of nodes in the cluster. Here set to 3.
  - `--max-nodes=10`: Sets the maximum number of nodes in the cluster. Here set to 10.
- `--num-nodes=5`: The initial number of nodes in the cluster before autoscaling starts. Set to 5 here.
- `--zone=us-central1-a`: The Google Cloud zone in which the cluster is created. In this example, it is `us-central1-a`.

These flags provide a flexible configuration for creating and managing your cluster in Google Cloud.

```sh
  gcloud container clusters create online-boutique \
  --disk-size=50GB \
  --enable-autoupgrade \
  --enable-autoscaling --min-nodes=3 --max-nodes=10 --num-nodes=5 \
  --zone=us-central1-a
```

**Warning:** If max nodes = 10 set disk-size to 50GB or smaller otherwise the nodes will have problems while autoscaling because all resources are already allocated

## 5. Start deployment (specify right path where your manifests lie)

#### By using kubectl

This command directly applies the Kubernetes manifests defined in kubernetes-manifests.yaml. It is a direct and explicit method to create or update resources in your cluster.

```sh
kubectl apply -f ./release/kubernetes-manifests.yaml
```

#### By using skaffold

For a simplified deployment process, you can use skaffold. Skaffold automates the build process when changes are made to the services and simplifies the complexity of Kubernetes deployments through simple configuration.

```sh
skaffold run -p gcb --default-repo=gcr.io/[PROJECT_ID]
```

- `-p gcb`: Set this flag to run build process of docker images on google cloud console and not on your machine. Especially helpful if you use a machine without x-amd architecture (like mine). If you want to build images that are based on x-amd on your local machine with different processor you have to do a lot of debugging before. The only disadvantage is that cloud build has to be run new every time you build so it may take a little longer sometimes when rebuilding 


## 6. Check pod health status

```sh
kubectl get pods
```

## 7. Get external ip-adress in kub cluster

```sh
kubectl get service frontend-external
```

## 8. Add locust load generator service (with ui) 

Follow the guide under [Locust_Setup](../system/loadgenerator/setup.md)

## 9. Add prometheus as external loadbalancer service to your cluster

Follow the guide under [Prometheus Setup](../system/monitoring/prometheus/prometheus-config.md)

## 10. Add grafana as nodeport service to your cluster

Follow the guide under [Grafana Setup](../system/monitoring/grafana/grafana-setup.md)

## 11. Make sure that non of your resource limits were reached
by visiting google cloud console -> apis -> compute engine api to check the current resource utilization
problems can lead to nodes not being able to scale up

When running 

```sh
kubectl get pods
```

All pods should be up and running. If not try to get the logs of the pods that are not running and see what went wrong when building. Normally it should be because of resource restrictions that are set within your google cloud console. Try updating your cluster to match the restrictions or try updating the restrictions under [Google Compute Engine](https://console.cloud.google.com/apis/api/compute.googleapis.com/)


# Reset or delete instance on the gke
## 1. Get all active clusters

```sh
  gcloud container clusters list
```

## 2. Delete existing cluster
```sh
gcloud container clusters delete online-boutique \
  --project=${PROJECT_ID} --region=${REGION}
```

## 3. Create Cluster 
```sh
gcloud container clusters create-auto online-boutique \
  --project=${PROJECT_ID} --region=${REGION}
```




