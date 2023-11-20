### Solution to Exercise 2: Persistent Storage for a Database

*Note: StatefulSet and PVC are best created using declarative YAML files, but here's how to create the secret imperatively:*

```bash
kubectl create secret generic mysql-root-pass --from-literal=password=[BASE64_ENCODED_PASSWORD] -n database
```

Final Yaml file:

```yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: mysql-db
  namespace: database
spec:
  serviceName: "mysql"
  replicas: 1
  selector:
    matchLabels:
      app: mysql-db
  template:
    metadata:
      labels:
        app: mysql-db
    spec:
      containers:
      - name: mysql
        image: mysql:5.7
        ports:
        - containerPort: 3306
        volumeMounts:
        - name: mysql-persistent-storage
          mountPath: /var/lib/mysql
        env:
        - name: MYSQL_ROOT_PASSWORD
          valueFrom:
            secretKeyRef:
              name: mysql-root-pass
              key: password
  volumeClaimTemplates:
  - metadata:
      name: mysql-persistent-storage
    spec:
      accessModes: [ "ReadWriteOnce" ]
      resources:
        requests:
          storage: 10Gi
```