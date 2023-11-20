### Solution to Exercise 1: Deploy a Load Balanced Web Service

```bash
kubectl create deployment web-server --image=nginx:1.18 --replicas=3 -n frontend
kubectl expose deployment web-server --type=LoadBalancer --port=80 -n frontend
```

Final Yaml file:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web-server
  namespace: frontend
spec:
  replicas: 3
  selector:
    matchLabels:
      app: web-server
  template:
    metadata:
      labels:
        app: web-server
    spec:
      containers:
      - name: nginx
        image: nginx:1.18
        ports:
        - containerPort: 80
---
apiVersion: v1
kind: Service
metadata:
  name: web-service
  namespace: frontend
spec:
  type: LoadBalancer
  ports:
  - port: 80
  selector:
    app: web-server
```