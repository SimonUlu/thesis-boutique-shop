## Prometheus Queries that can are helpful for monitoring the kub-cluster

#### All kubectl command will not work if the kubectl config in your zsh-file is not configured to be the gcloud kubectl 

1. Get all active clusters

```sh
  gcloud container clusters list
```

2. Delete existing cluster
```sh
gcloud container clusters delete online-boutique \
  --project=${PROJECT_ID} --region=${REGION}
```

3. Create Cluster 
```sh
gcloud container clusters create-auto online-boutique \
  --project=${PROJECT_ID} --region=${REGION}
```

4. Enable Container Services
```sh
gcloud services enable container.googleapis.com \
--project=${PROJECT_ID}
```

5. Install kubectl via gcloud and make sure path is set correctly in source ~/.zshrc

```sh
gcloud components install kubectl
```

6. Deploy Kubernetes Cluster to previously build google cloud cluster

```sh
kubectl apply -f ./release/kubernetes-manifests.yaml
```

7. Check pods health status

```sh
  kubectl get pods
```

8. Init service for loadgenerator

```sh
  
```