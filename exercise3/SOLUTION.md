### Solution to Exercise 3: Configuring a Logging Sidecar

*Note: Creating a pod with a sidecar container is typically done declaratively.*

Final Yaml file:

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: app-logger
  namespace: logging
spec:
  containers:
  - name: alpine
    image: alpine
    command: ["tail", "-f", "/dev/null"]
  - name: sidecar
    image: busybox
    command: ["/bin/sh", "-c"]
    args: ["while true; do date; sleep 5; done"]
    volumeMounts:
    - name: shared-logs
      mountPath: /var/log
  volumes:
  - name: shared-logs
    emptyDir: {}
```