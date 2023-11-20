### Exercise 2: Persistent Storage for a Database

**Task:**
Set up a StatefulSet for a database with persistent storage:

- The StatefulSet should be in the `database` namespace.
- Name the StatefulSet `mysql-db`.
- Use the `mysql` image with the `5.7` tag.
- Ensure the database uses a `PersistentVolumeClaim` with a size of `10Gi`.
- The database should be accessible within the cluster on port `3306`.
- Define a `Secret` for storing the MySQL root password.