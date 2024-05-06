## this documentation helps you in deleting and checking all clusters that were created in a given project in the gke on your g cloud console

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