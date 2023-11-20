### Solution to Exercise 5: Horizontal Pod Autoscaler

```bash
kubectl autoscale deployment api-server --cpu-percent=50 --min=2 --max=10 -n autoscale
```

Final Yaml file:

```yaml
apiVersion: autoscaling/v2beta2
kind: HorizontalPodAutoscaler
metadata:
  name: api-server-hpa
  namespace: autoscale
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: api-server
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 50
```