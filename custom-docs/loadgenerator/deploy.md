## Follow these docs to add locust-loadgenerator to your application (For current configuration check [config](../../src/loadgenerator))

1. Add external port to loadgenerator deployment to listen to und container
```sh
ports:
  - containerPort: 8089
```

2. Add external loadgenerator service to get in the web ui

```sh
##load balancer service
apiVersion: v1
kind: Service
metadata:
  name: loadgenerator-web-ui
spec:
  type: LoadBalancer
  ports:
  - port: 80
    targetPort: 8089
  selector:
    app: loadgenerator
```

3. Create external service for loadgenerator

```sh
kubectl apply -f loadgenerator/loadgenerator-service.yaml
```

4. Get external ui of loadgen service

```sh
kubectl get services
```

The response will be something like this:
NAME                    TYPE           CLUSTER-IP      EXTERNAL-IP    PORT(S)        AGE
loadgenerator-web-ui    LoadBalancer   10.26.153.251   34.68.77.173   80:32696/TCP   4h16m

visit external-ip in browser of your choice to see to loadgenerator