### Exercise 5: Horizontal Pod Autoscaler

**Task:**
Create a Horizontal Pod Autoscaler (HPA) for an existing deployment:

- The HPA should be in the `autoscale` namespace.
- Target the deployment named `api-server`.
- The HPA should maintain an average CPU utilization of `50%`.
- The number of replicas should scale between `2` and `10`.
- Assume the `api-server` deployment is already configured with resource requests and limits.