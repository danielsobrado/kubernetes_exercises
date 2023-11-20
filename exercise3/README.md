### Exercise 3: Configuring a Logging Sidecar

**Task:**
Create a pod with a logging sidecar container:

- The pod should be in the `logging` namespace.
- Name the pod `app-logger`.
- The main container should use the `alpine` image and run a dummy command like `tail -f /dev/null`.
- Add a sidecar container using the `busybox` image.
- The sidecar container should periodically (`every 5 seconds`) log the current date and time to a shared volume.
- The shared volume should be an `emptyDir`.