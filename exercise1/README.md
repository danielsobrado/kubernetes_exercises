### Exercise 1: Deploy a Load Balanced Web Service

**Task:**
Create a deployment and a service with the following characteristics:

- The deployment should be in the `frontend` namespace.
- Name the deployment `web-server`.
- Use the `nginx` image with the `1.18` tag.
- The deployment should have 3 replicas.
- Expose the deployment using a `LoadBalancer` service.
- The service should be named `web-service` and expose port `80`.