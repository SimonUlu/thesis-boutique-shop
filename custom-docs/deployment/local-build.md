# Local Build

## 1. Ensure you have the following requirements:

   - Docker Desktop installed
   - Kind[Install Kind](https://kind.sigs.k8s.io/)
   - Skaffold [Install Skaffold](https://skaffold.dev/docs/install/#standalone-binary)
   - Shell environment `git` and `kubectl`.
   - Minimum of 6GB Memory allocated in Docker Desktop and 20 GB of free Diskspace (Open Docker Desktop -> Settings -> Resources)
   - Minikube installed (install via homebrew on mac)
   - if you run into problems using new macs with arm chips install rosetta with homebrew and active rosetta for emulation in docker desktop settings

## 2. Clone the repository.

```sh
 git clone git@github.com:SimonUnterlugauer/thesis-boutique-shop.git
```

## 3. Initialize kind cluster

```sh
 kind create cluster
```

## 4. Verify that you are connected to the respective control plane.

   ```sh
   kubectl get nodes
   ```

## 5. Build the application (build all docker containers and orchestrate them in the initialised kub cluster)

```sh
skaffold run ## first time may take up to 30 mins
```

   if you want to make changes to any of the source code run:

```sh
skaffold dev ## first time may take up to 30 mins
```

## 6. Verify pods are up and running

```sh
kubectl get pods
```

## 7. Bind frontend to localhost:8080

```sh
kubectl port-forward deployment/frontend 8080:8080
```

## 8. Open Browser and navigate to localhost:8080 to view the frontend

## 9. Locust Loadgenerator Port lokal auf Rechner weiterleiten

   ```sh
   kubectl port-forward deployment/loadgenerator 8089:8089
   ```

## 10. Integrate prometheus and grafana by following the docs under custom-docs/setup/...

## 11. Rebuild after downing

### 11.1 Go to Docker Desktop and start the Kind Control Plane to start up kubernetes

### 11.2 Build the application (build all docker containers and orchestrate them in the initialised kub cluster)
   note: errors while building often occure in unstable wifi-networks such as eduroam or brainfi. just execute more often or if still not working manually download stuff

```sh
skaffold run
```

if you want to make changes to any of the source code and have hot reloading in place run:

```sh
 skaffold dev
```

### 11.3 Bind frontend to localhost:8080

   ```sh
   kubectl port-forward deployment/frontend 8080:8080
   ```

### 11.4 Locust Loadgenerator Port lokal auf Rechner weiterleiten

   ```sh
   kubectl port-forward deployment/loadgenerator 8089:8089
   ```

## 12. Start Locust Load Generating

- Changing the locust config to simulate changing user traffic by rebuilding kubernetes cluster with skaffold run oder keeping it alive by running skaffold dev

Open http://localhost:8089/ in browser of your choice

then weirdly fill the form as following

- Number of users of your choice
- spawn rate of your choice
- Host = **http://frontend:80**
- Run time of your choice