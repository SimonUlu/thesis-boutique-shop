# These are the instructions to setup google cloud environment properly on your machine as well as configuring your google cloud console account to be able to deploy clusters


## 1. Enable Container Services
```sh
gcloud services enable container.googleapis.com \
--project=${PROJECT_ID}
```

## 2. Install kubectl via gcloud and make sure path is set correctly in source ~/.zshrc

```sh
gcloud components install kubectl
```

## 3. Check pods health status

```sh
  kubectl get pods
```

