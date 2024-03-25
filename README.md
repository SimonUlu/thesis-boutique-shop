<p align="center">
<img src="/src/frontend/static/icons/Hipster_HeroLogoMaroon.svg" width="300" alt="Online Boutique" />
</p>

![Continuous Integration](https://github.com/GoogleCloudPlatform/microservices-demo/workflows/Continuous%20Integration%20-%20Main/Release/badge.svg)

**Online Boutique** is a cloud-first microservices demo application.
Online Boutique consists of an 11-tier microservices application. The application is a
web-based e-commerce app where users can browse items,
add them to the cart, and purchase them.

## Screenshots

| Home Page                                                                                                         | Checkout Screen                                                                                                    |
| ----------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------ |
| [![Screenshot of store homepage](/docs/img/online-boutique-frontend-1.png)](/docs/img/online-boutique-frontend-1.png) | [![Screenshot of checkout screen](/docs/img/online-boutique-frontend-2.png)](/docs/img/online-boutique-frontend-2.png) |

## Deploy to GKE
1. Create Google Cloud Account with billing enabled
2. activate following apis by looking for apis & services
   - Artifact Registry API
   - Kubernetes Engine API
3. Create a google kubernetes cluster


   ```sh
      gcloud services enable container.googleapis.com
      gcloud container clusters create demo --enable-autoupgrade \
      --enable-autoscaling --min-nodes=3 --max-nodes=10 --num-nodes=5 --zone=us-central1-a
      kubectl get nodes
   ```

4. Enable Google Container Registry (GCR) on your GCP project and configure the docker CLI to authenticate to GCR:

   ```sh
      gcloud services enable containerregistry.googleapis.com
      gcloud auth configure-docker -q
   ```

5. In the root of this repository, run

   ```sh
       skaffold run --default-repo=gcr.io/[PROJECT_ID], where [PROJECT_ID] is your GCP project ID.
   ```

    This command:
    
    builds the container images
    pushes them to GCR
    applies the ./kubernetes-manifests deploying the application to Kubernetes.
    Troubleshooting: If you get "No space left on device" error on Google Cloud Shell, you can build the images on Google Cloud Build: Enable the Cloud Build API, then run skaffold run -p gcb --default-repo=gcr.io/[PROJECT_ID] instead.

6. Find the IP address of your application, then visit the application on your browser to confirm installation.

   ```sh
      kubectl get service frontend-external
    ```


7. Navigate to http://EXTERNAL-IP to access the web frontend.

## Local Build

1. Ensure you have the following requirements:
   - Docker Desktop installed
   - Kind[Install Kind](https://kind.sigs.k8s.io/)
   - Skaffold [Install Skaffold](https://skaffold.dev/docs/install/#standalone-binary)
   - Shell environment `git` and `kubectl`.
   - Minimum of 6GB Memory allocated in Docker Desktop and 20 GB of free Diskspace (Open Docker Desktop -> Settings -> Resources)
   - Minikube installed (install via homebrew on mac)

2. Clone the repository.

  ```sh
   git clone git@github.com:SimonUnterlugauer/thesis-boutique-shop.git
   ```

3. Verify that you are connected to the respective control plane.
   ```sh
   kubectl get nodes
   ```

4. Build the application (build all docker containers and orchestrate them in the initialised kub cluster)

   ```sh
   skaffold run ## first time may take up to 30 mins
   ```
   if you want to make changes to any of the source code run:
  ```sh
   skaffold dev ## first time may take up to 30 mins
   ```
5. Verify pods are up and running

   ```sh
   kubectl get pods
   ```


6. Bind frontend to localhost:8080

   ```sh
   kubectl port-forward deployment/frontend 8080:8080
   ```
   
7. Open Browser and navigate to localhost:8080 to view the frontend

8. Locust Loadgenerator Port lokal auf Rechner weiterleiten

   ```sh
   kubectl port-forward deployment/loadgenerator 8089:8089
   ```

## Rebuild after downing

1. Go to Docker Desktop and start the Kind Control Plane to start up kubernetes

2. Build the application (build all docker containers and orchestrate them in the initialised kub cluster)

   ```sh
   skaffold run 
   ```
   if you want to make changes to any of the source code and have hot reloading in place run:
  ```sh
   skaffold dev 
   ```

3. Bind frontend to localhost:8080

   ```sh
   kubectl port-forward deployment/frontend 8080:8080
   ```

4. Locust Loadgenerator Port lokal auf Rechner weiterleiten

   ```sh
   kubectl port-forward deployment/loadgenerator 8089:8089
   ```

5. Bind Grafana to port 3000

   ```sh
   kubectl port-forward service/grafana 3000:80
   ```

6. Bind prometheus server to localhost (as it is the data source for the graphana dashboards

      ```sh
    kubectl port-forward service/prometheus-server 9090:80
   ```

## Install and integrate grafana and prometheus

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


  ``sh
       kubectl create namespace monitoring
       helm install my-prometheus prometheus-community/kube-prometheus-stack --namespace monitoring
     ```

3. Installation von grafana

  ``sh
       helm install my-grafana grafana/grafana --namespace monitoring
     ```

4. Admin Passwort für Grafana abrufen und in Password-Manager speichern

  ``sh
       kubectl get secret --namespace monitoring my-grafana -o jsonpath="{.data.admin-password}" | base64 --decode ; echo
     ```


## Configure grafana with prometheus

1. Bind prometheus and grafana to ports
2. Set data source to: http://prometheus-server:80 or http://localhost:9000

## Start Locust Load Generating

Open http://localhost:8089/ in browser of your choice

then weirdly fill the form as following
  - Number of users of your choice
  - spawn rate of your choice
  - Host = **http://frontend:80**
  - Run time of your choice


## Architecture

**Online Boutique** is composed of 11 microservices written in different
languages that talk to each other over gRPC.

[![Architecture of
microservices](/docs/img/architecture-diagram.png)](/docs/img/architecture-diagram.png)

Find **Protocol Buffers Descriptions** at the [`./protos` directory](/protos).

| Service                                              | Language      | Description                                                                                                                       |
| ---------------------------------------------------- | ------------- | --------------------------------------------------------------------------------------------------------------------------------- |
| [frontend](/src/frontend)                           | Go            | Exposes an HTTP server to serve the website. Does not require signup/login and generates session IDs for all users automatically. |
| [cartservice](/src/cartservice)                     | C#            | Stores the items in the user's shopping cart in Redis and retrieves it.                                                           |
| [productcatalogservice](/src/productcatalogservice) | Go            | Provides the list of products from a JSON file and ability to search products and get individual products.                        |
| [currencyservice](/src/currencyservice)             | Node.js       | Converts one money amount to another currency. Uses real values fetched from European Central Bank. It's the highest QPS service. |
| [paymentservice](/src/paymentservice)               | Node.js       | Charges the given credit card info (mock) with the given amount and returns a transaction ID.                                     |
| [shippingservice](/src/shippingservice)             | Go            | Gives shipping cost estimates based on the shopping cart. Ships items to the given address (mock)                                 |
| [emailservice](/src/emailservice)                   | Python        | Sends users an order confirmation email (mock).                                                                                   |
| [checkoutservice](/src/checkoutservice)             | Go            | Retrieves user cart, prepares order and orchestrates the payment, shipping and the email notification.                            |
| [recommendationservice](/src/recommendationservice) | Python        | Recommends other products based on what's given in the cart.                                                                      |
| [adservice](/src/adservice)                         | Java          | Provides text ads based on given context words.                                                                                   |
| [loadgenerator](/src/loadgenerator)                 | Python/Locust | Continuously sends requests imitating realistic user shopping flows to the frontend.                                              |

## Features

- **[Kubernetes](https://kubernetes.io)/[GKE](https://cloud.google.com/kubernetes-engine/):**
  The app is designed to run on Kubernetes (both locally on "Docker for
  Desktop", as well as on the cloud with GKE).
- **[gRPC](https://grpc.io):** Microservices use a high volume of gRPC calls to
  communicate to each other.
- **[Istio](https://istio.io):** Application works on Istio service mesh.
- **[Cloud Operations (Stackdriver)](https://cloud.google.com/products/operations):** Many services
  are instrumented with **Profiling** and **Tracing**. In
  addition to these, using Istio enables features like Request/Response
  **Metrics** and **Context Graph** out of the box. When it is running out of
  Google Cloud, this code path remains inactive.
- **[Skaffold](https://skaffold.dev):** Application
  is deployed to Kubernetes with a single command using Skaffold.
- **Synthetic Load Generation:** The application demo comes with a background
  job that creates realistic usage patterns on the website using
  [Locust](https://locust.io/) load generator.

## Development

See the [Development guide](/docs/development-guide.md) to learn how to run and develop this app locally.

## Demos featuring Online Boutique

- [The new Kubernetes Gateway API with Istio and Anthos Service Mesh (ASM)](https://medium.com/p/9d64c7009cd)
- [Use Azure Redis Cache with the Online Boutique sample on AKS](https://medium.com/p/981bd98b53f8)
- [Sail Sharp, 8 tips to optimize and secure your .NET containers for Kubernetes](https://medium.com/p/c68ba253844a)
- [Deploy multi-region application with Anthos and Google cloud Spanner](https://medium.com/google-cloud/a2ea3493ed0)
- [Use Google Cloud Memorystore (Redis) with the Online Boutique sample on GKE](https://medium.com/p/82f7879a900d)
- [Use Helm to simplify the deployment of Online Boutique, with a Service Mesh, GitOps, and more!](https://medium.com/p/246119e46d53)
- [How to reduce microservices complexity with Apigee and Anthos Service Mesh](https://cloud.google.com/blog/products/application-modernization/api-management-and-service-mesh-go-together)
- [gRPC health probes with Kubernetes 1.24+](https://medium.com/p/b5bd26253a4c)
- [Use Google Cloud Spanner with the Online Boutique sample](https://medium.com/p/f7248e077339)
- [Seamlessly encrypt traffic from any apps in your Mesh to Memorystore (redis)](https://medium.com/google-cloud/64b71969318d)
- [Strengthen your app's security with Anthos Service Mesh and Anthos Config Management](https://cloud.google.com/service-mesh/docs/strengthen-app-security)
- [From edge to mesh: Exposing service mesh applications through GKE Ingress](https://cloud.google.com/architecture/exposing-service-mesh-apps-through-gke-ingress)
- [Take the first step toward SRE with Cloud Operations Sandbox](https://cloud.google.com/blog/products/operations/on-the-road-to-sre-with-cloud-operations-sandbox)
- [Deploying the Online Boutique sample application on Anthos Service Mesh](https://cloud.google.com/service-mesh/docs/onlineboutique-install-kpt)
- [Anthos Service Mesh Workshop: Lab Guide](https://codelabs.developers.google.com/codelabs/anthos-service-mesh-workshop)
- [KubeCon EU 2019 - Reinventing Networking: A Deep Dive into Istio's Multicluster Gateways - Steve Dake, Independent](https://youtu.be/-t2BfT59zJA?t=982)
- Google Cloud Next'18 SF
  - [Day 1 Keynote](https://youtu.be/vJ9OaAqfxo4?t=2416) showing GKE On-Prem
  - [Day 3 Keynote](https://youtu.be/JQPOPV_VH5w?t=815) showing Stackdriver
    APM (Tracing, Code Search, Profiler, Google Cloud Build)
  - [Introduction to Service Management with Istio](https://www.youtube.com/watch?v=wCJrdKdD6UM&feature=youtu.be&t=586)
- [Google Cloud Next'18 London – Keynote](https://youtu.be/nIq2pkNcfEI?t=3071)
  showing Stackdriver Incident Response Management

---

This is not an official Google project.
